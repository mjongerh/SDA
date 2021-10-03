import ROOT
import numpy
from array import array
from math import *
from datetime import datetime

# provide better print functionality for ROOT TVector3
ROOT.TVector3.__repr__ = ROOT.TVector3.__str__ = lambda v : "({:g},{:g},{:g})".format( v.X(), v.Y(), v.Z() )
#canv = ROOT.TCanvas("canv","Dummy Title", 1000,1000 ) #Create a canvas for the art to be shown
TestRanT = ROOT.TH1D("TestRanT", "distribution of random energy", 100, 1, 0)
################
# Global Settings
################
a= 8420 # meter
rho0=1.225 #kg/m^3 != g/cm^3
mc2 = 0.510998950 #* 299792458 * 299792458 # value of me *c^2
MaxGen = 1000 # Maximum generations computed
Column_density = []
Column_density.append(0)
Column_density.append(380) #photon
Column_density.append(263) #electron
Column_density.append(263) #positron
Simulations = []

def plot_shower( shower ,
                 title = "Worst title ever.",
                 xysize = 10, 
                 zsize = 50000, 
                 canvastitle = ""):

    """
    Plot a list of particles. 
    You may use and modify this function to make plots of your showers 
    """

    ROOT.gStyle.SetOptStat(0)

    # We use a dummy 3d histogram to define the 
    # 3d-axes and coordinate ranges.

    h = ROOT.TH3D("h",title, 
                  1, -xysize,xysize,
                  1, -xysize,xysize,
                  1, 0, zsize)
    
    h.GetXaxis().SetTitleOffset(1.7)
    h.SetXTitle("hello, I am the x-axis")

    # make canvas and draw our dummy histogram

    c = ROOT.TCanvas(canvastitle,"canvas title", 500,600)

    #c.linelist = []

    h.DrawCopy();
    
    for g in shower:
        for p in g :
             
            # create a line object to draw 
            line = ROOT.TPolyLine3D(2)
            line.SetPoint(0, p.start_pos.X(), p.start_pos.Y(), p.start_pos.Z() )
            line.SetPoint(1, p.end_pos.X(),   p.end_pos.Y(),   p.end_pos.Z()   )
            line.SetLineColor( p.kind ) #p.color
            line.Draw()
           
            # workaround:
            # for some reason, and for some student(s), the destructor
            # of TCanvas:fPrimitives takes a huge time unless we tell it
            # not to clean up the lines. (something with recursiveremove).
            line.ResetBit( ROOT.kMustCleanup )
        
            # The follwing tells python that line should not be cleaned up. 
            ROOT.SetOwnership(line, False ) 
        
    c.Update()
 
    ROOT.SetOwnership( c, False )
    return c

class Particle(object):

    "A class to store the information of a particle in our air shower."

    def __init__( self ) :

        self.direction  = ROOT.TVector3(0,0,0)
        self.energy     = 0.0
        self.kind       = 0 # 1 = gamma, 2 = electron, 3 = positron
        self.start_pos  = ROOT.TVector3(0,0,0)
        self.end_pos    = ROOT.TVector3(0,0,0)
        self.color      = 1
        
    def __str__(self):
        
        s = " Particle " 
        s+= " start: " +str( self.start_pos )
        s+= " end: " +str( self.end_pos )
        s+= " Energy: " +str(self.energy)
        return s

    def __repr__(self):
        return self.__str__()
  

def direction_at_angle( initial_direction, theta, phi ):

    """ 
    Return a vector that makes an angle theta with 
    respect to the TVector3 initial_direction. 
    The remaining degree of freedom is the angel phi.
    """
    v = ROOT.TVector3( sin(theta)* cos(phi), sin(theta)*sin(phi), cos(theta ))
    v.RotateY( initial_direction.Theta() )
    v.RotateZ( initial_direction.Phi()  )
    return v


def compute_height(start_height, column_density) :
    RanCd= ROOT.gRandom.Exp(column_density)
    life_length = -a* log(  (RanCd/(a*rho0)) + exp(-start_height.Z()/a) )
    
    return life_length

def RandomEnergy():
    failsafe = 0
    while failsafe < 1000:
        RanUni = ROOT.gRandom.Rndm()
        RanUni2 = ROOT.gRandom.Rndm()
        RanFunc = 1-(4/3)*RanUni2 * (1 - RanUni2)
        if RanFunc  >= RanUni :
            return RanUni2
        else: failsafe += 1
    print("Disaster happened, not a single energy was accepted")
    quit()

def GenNewPart(oldparticle):
    #print("OLD" + str(oldparticle))
    NewParticle1 = Particle()
    NewParticle2 = Particle()
    if oldparticle.kind == 1 : #if old = photon, gen electron + positron
        NewParticle1.kind = 2
        NewParticle2.kind = 3
    else :
        NewParticle1.kind = oldparticle.kind #keep old
        NewParticle2.kind = 1 #create new photon
    NewParticle1.start_pos = oldparticle.end_pos
    NewParticle2.start_pos = oldparticle.end_pos
    NewParticle1.energy = RandomEnergy() * oldparticle.energy
    NewParticle2.energy = oldparticle.energy - NewParticle1.energy
    phiRan = ROOT.gRandom.Rndm() * 2 * pi #random direction for phi
    if NewParticle1.energy >= 85.0 :
        Theta1 = 0.510998950/NewParticle1.energy
        TestRanT.Fill(Theta1)
        if abs(Theta1) > 0.01 : print("T1= "+ str(Theta1) + "    E1= " + str(NewParticle1.energy))
        NewParticle1.direction = direction_at_angle(oldparticle.direction, Theta1, phiRan)
    else : 
        NewParticle1.direction = oldparticle.direction
        NewParticle1.end_pos = NewParticle1.start_pos
    
    if NewParticle2.energy >= 85.0 :
        Theta2 = -0.510998950/NewParticle2.energy
        TestRanT.Fill(Theta2)
        if abs(Theta2) > 0.01 : print("T2= "+ str(Theta2) + "    E2= " + str(NewParticle2.energy))
        NewParticle2.direction = direction_at_angle(oldparticle.direction, Theta2, pi + phiRan)
    else : 
        NewParticle2.direction = oldparticle.direction
        NewParticle2.end_pos = NewParticle2.start_pos
    #print("NEW"+str(NewParticle1) + str(NewParticle2))
    return NewParticle1, NewParticle2

def Shower(startenergy, startheight):
    Generations = []
    Particles = []
    
    p = Particle() #Generate first photon
    p.kind = 1
    p.energy = startenergy  #in MeV
    p.start_pos =  ROOT.TVector3( 0,0,startheight ) #0,0,startheight
    theta       = 0.0001
    phi         = ROOT.gRandom.Rndm() * 2 * pi
    p.direction = direction_at_angle( ROOT.TVector3(0,0,-1), theta, phi )
    Particles.append( p )
    Generations.append(Particles)
    
    for i in range(MaxGen) :
        NewParticles = []        #create list for newly generated particles
        for particle in Generations[i] :        #loop over particles in gen[i]
            EndOfShower = 0
            if particle.energy >= 85.0 :            #make them move if they have energy left
                HeightAtDecay = compute_height(particle.start_pos, Column_density[particle.kind] )
                particle.end_pos = particle.start_pos + (particle.start_pos.Z() - HeightAtDecay) * particle.direction.Unit()
                NewParts = GenNewPart(particle)                #create 2 new particles, calc their properties
                NewParticles.append(NewParts[0])
                NewParticles.append(NewParts[1])
                EndOfShower += 1
            else :
                particle.end_pos = particle.start_pos
        if EndOfShower==0 : break #Stop the loop when all particles are below 85 MeV
        Generations.append(NewParticles)
    return Generations

def CreateHeightDistribution(generations, nbins, startheight):
    BinWidth =startheight/nbins
    HeightDist = ROOT.TH1D(str(ROOT.gRandom.Rndm()), "distribution of particles at each height", nbins, 0, startheight)
    for Gen in generations :
        for Part in Gen :
            if Part.kind == 1: continue
            A = floor(Part.end_pos.Z()/BinWidth) #get the lowest bin the particle has been in
            B = floor(Part.start_pos.Z()/BinWidth) #get the highest bin
            i = A
            while i<=B: #add 1 to all bins in between
                HeightDist.Fill(i*BinWidth)
                i += 1
    return HeightDist

#####################
#assignment a
#####################
#canvAA = ROOT.TCanvas("canvAA","Dummy Title", 780,780 ) #Create a canvas for the art to be shown
#histogram = ROOT.TH1D("histogram_of_x1","histogram of x1",100, 100, 10 )
#for i in range(500) :
#    histogram.Fill(compute_height(ROOT.TVector3( 0,0,10000000 ), 380))
#    print(compute_height(ROOT.TVector3( 0,0,10000000 ), 380))

#histogram.Draw()
#canvAA.Modified()
#canvAA.Update()

#print("height at mean free path is: ",  -a* log((380/(a*rho0)) + exp(-10000000/a) )) #sanity check


#####################
#assignment b
#####################
startHeight = 50000 #in meter
startEnergy = 100000 #in MeV

Shower100GeV = Shower(startEnergy,startHeight)
plot1 = plot_shower(Shower100GeV, "Shower with photon of 100GeV", 10, startHeight, "canv100GeV")

startEnergy = 1000000 #in MeV
Shower1TeV = Shower(startEnergy,startHeight)
plot2 = plot_shower(Shower1TeV, "Shower with photon of 1TeV", 15, startHeight, "canv1TeV")

startEnergy = 10000000 #in MeV
Shower10TeV = Shower(startEnergy,startHeight)
plot3 = plot_shower(Shower10TeV, "Shower with photon of 10TeV", 20, startHeight, "canv10TeV")

#####################
#assignment c
#####################
Nbins = 100 #Slice the height in bins
HeightDistCanvA = ROOT.TCanvas("HeightDistCanvA","Height dist. of 100GeV photon", 1000,1000 )
Hdist100GeV = CreateHeightDistribution(Shower100GeV, Nbins, startHeight)
Hdist100GeV.Draw()

HeightDistCanvB = ROOT.TCanvas("HeightDistCanvB","Height dist. of 1TeV photon", 1000,1000 )
Hdist1TeV = CreateHeightDistribution(Shower1TeV, Nbins, startHeight)
Hdist1TeV.Draw()

HeightDistCanvC = ROOT.TCanvas("HeightDistCanvC","Height dist. of 10TeV photon", 1000,1000 )
Hdist10TeV = CreateHeightDistribution(Shower10TeV, Nbins, startHeight)
Hdist10TeV.Draw()

#####################
#assignment d
#####################
HeightDistCanvC = ROOT.TCanvas("HeightDistCanvC","Height dist. of 10TeV photon", 2000,500 )
HeightDistCanvC.Divide(5,2)
PANIC=0
EnergyList = numpy.logspace(5, 7, 1, dtype = 'float', endpoint=True).tolist()
print(EnergyList)
EnergyCoord =array( 'd' )
HeightCoord = array( 'd' )
BinRatio = startHeight/Nbins
DistE = []
for e in EnergyList:
    ShowerE = Shower(e, startHeight)
    DistE.append(CreateHeightDistribution(ShowerE, Nbins, startHeight))
    HeightDistCanvC.cd(PANIC+1)
    DistE[PANIC].Draw()
    HeightDistCanvC.Modified()
    HeightDistCanvC.Update()
    MaxBin = DistE[PANIC].GetMaximumBin()
    EnergyCoord.append(e)
    HeightCoord.append(float(MaxBin*BinRatio))
    PANIC += 1

CanvMaxParticles = ROOT.TCanvas("CanvMaxParticles","Height of max particles as function of E", 1000,1000 )
Graph = ROOT.TGraph(1, EnergyCoord, HeightCoord)
CanvMaxParticles.SetLogx()
Graph.SetLineColor( 2 )
Graph.SetLineWidth( 4 )
Graph.SetMarkerColor( 4 )
Graph.SetMarkerStyle( 21 )
Graph.SetTitle( 'a simple graph' )
Graph.GetXaxis().SetTitle( 'X title' )
Graph.GetYaxis().SetTitle( 'Y title' )
Graph.Draw( 'ACP' )
CanvMaxParticles.Update()
CanvMaxParticles.Modified()

###############
#TEST AREA ONLY, enter at your own risk
###############
TestCanvas = ROOT.TCanvas("TestCanvas","Dummy Title", 1000,1000 )
#TestRanE = ROOT.TH1D("TestRanE", "distribution of random energy", 100, 0, 1)
#for i in range(10000):
#    TestRanE.Fill(RandomEnergy())
TestRanT.Draw()