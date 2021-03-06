import ROOT
import numpy
from array import array
from math import *

# provide better print functionality for ROOT TVector3
ROOT.TVector3.__repr__ = ROOT.TVector3.__str__ = lambda v : "({:g},{:g},{:g})".format( v.X(), v.Y(), v.Z() )
#canv = ROOT.TCanvas("canv","Dummy Title", 1000,1000 ) #Create a canvas for the art to be shown
for s in range(1234): ROOT.gRandom.Rndm() #scramble start seed
################
# Global Settings
################
a= 8420 # meter
rho0=1.225 #kg/m^3 != g/cm^3
mc2 = 0.510998950 #* 299792458 * 299792458 # value of me *c^2
MaxGen = 10000 # Maximum generations computed
Column_density = []
Column_density.append(0)
Column_density.append(380) #photon
Column_density.append(263) #electron
Column_density.append(263) #positron

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
    ROOT.TGaxis.SetMaxDigits(3)
    h.GetXaxis().SetTitleOffset(1.7)
    h.GetYaxis().SetTitleOffset(1.7)
    h.GetZaxis().SetTitleOffset(1.0)
    h.SetXTitle("x-axis (km)")
    h.SetYTitle("y-axis (km)")
    h.SetZTitle("Height (m)")

    # make canvas and draw our dummy histogram

    c = ROOT.TCanvas(canvastitle,"canvas title", 800,600)

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
    Theta1 = mc2/(NewParticle1.energy*2*pi)
    NewParticle1.direction = direction_at_angle(oldparticle.direction, Theta1, phiRan)
    Theta2 = -mc2/(NewParticle2.energy*2*pi)
    NewParticle2.direction = direction_at_angle(oldparticle.direction, Theta2, pi + phiRan)

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
                particle.end_pos = particle.start_pos + (particle.start_pos.Z() - HeightAtDecay) * particle.direction
                NewParts = GenNewPart(particle)                #create 2 new particles, calc their properties
                NewParticles.append(NewParts[0])
                NewParticles.append(NewParts[1])
                EndOfShower += 1
            else : #Otherwise they stop instantly
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

def HAWCmap(generations, heigthinput):
    hHAWCmap = ROOT.TH2D("hHAWCmap", "distribution of particles at height of HAWC", 100, -10, 10, 100, -10, 10)
    for Gen in generations:
        for Part in Gen:
            if Part.end_pos.Z() < heigthinput and Part.start_pos.Z() > heigthinput:
                X = (Part.end_pos.X()+Part.start_pos.X())/2
                Y = (Part.end_pos.Y()+Part.start_pos.Y())/2
                hHAWCmap.Fill(X,Y)
    return hHAWCmap

#####################
#assignment a
#####################
canvFirstInt = ROOT.TCanvas("canvFirstInt","Height of the first interaction", 780,780 ) #Create a canvas for the art to be shown
hFirstInt = ROOT.TH1D("histogram_of_x1","Height of the first interaction",100, 100, 10 )
for i in range(500) : hFirstInt.Fill(compute_height(ROOT.TVector3( 0,0,10000000 ), 380))
hFirstInt.GetXaxis().SetTitle( 'Height (m)' )
hFirstInt.GetYaxis().SetTitle( 'Number first events' )
hFirstInt.Draw()
canvFirstInt.Modified()
canvFirstInt.Update()

print("height at mean free path is: ",  -a* log((380/(a*rho0)) + exp(-10000000/a) )) #sanity check


#####################
#assignment b
#####################
startHeight = 50000 #in meter
startEnergy = 100000 #in MeV

Shower100GeV = Shower(startEnergy,startHeight)
plot1 = plot_shower(Shower100GeV, "Shower with photon of 100GeV", 10, startHeight*0.75, "canv100GeV")

startEnergy = 1000000 #in MeV
Shower1TeV = Shower(startEnergy,startHeight)
plot2 = plot_shower(Shower1TeV, "Shower with photon of 1TeV", 10, startHeight*0.75, "canv1TeV")

startEnergy = 10000000 #in MeV
Shower10TeV = Shower(startEnergy,startHeight)
plot3 = plot_shower(Shower10TeV, "Shower with photon of 10TeV", 10, startHeight*0.75, "canv10TeV")

#####################
#assignment c
#####################
Nbins = 100 #Slice the height in bins
HeightDistCanvA = ROOT.TCanvas("HeightDistCanvA","Height dist. of 100GeV photon", 1000,1000 )
Hdist100GeV = CreateHeightDistribution(Shower100GeV, Nbins, startHeight)
Hdist100GeV.GetXaxis().SetTitle( 'Height (m)' )
Hdist100GeV.GetYaxis().SetTitle( 'Number of charged particles' )
Hdist100GeV.Draw()

HeightDistCanvB = ROOT.TCanvas("HeightDistCanvB","Height dist. of 1TeV photon", 1000,1000 )
Hdist1TeV = CreateHeightDistribution(Shower1TeV, Nbins, startHeight)
Hdist1TeV.GetXaxis().SetTitle( 'Height (m)' )
Hdist1TeV.GetYaxis().SetTitle( 'Number of charged particles' )
Hdist1TeV.Draw()

HeightDistCanvC = ROOT.TCanvas("HeightDistCanvC","Height dist. of 10TeV photon", 1000,1000 )
Hdist10TeV = CreateHeightDistribution(Shower10TeV, Nbins, startHeight)
Hdist10TeV.GetXaxis().SetTitle( 'Height (m)' )
Hdist10TeV.GetYaxis().SetTitle( 'Number of charged particles' )
Hdist10TeV.Draw()

#####################
#assignment d
#####################
Naverage = 10 #set to 10 to save computing time, 100 is used for analyses
EnergyList = [100000.0, 150000.0, 250000.0, 500000.0, 750000.0, 1250000.0, 2000000.0, 3500000.0, 6000000.0, 10000000.0]
print(EnergyList)
EnergyCoord =array( 'd' )
EnergyCoordErr =array( 'd' )
HeightCoord = array( 'd' )
HeightCoordErr = array( 'd' )
BinHeight = startHeight/Nbins
AverageHeight = [0]*len(EnergyList)
HAWCparticles = [0]*len(EnergyList)
HAWCCoord = array( 'd' )

for p in range(Naverage): #Generate showers, extract relevant values and average
    i=0
    for e in EnergyList:
        ShowerE = Shower(e, startHeight)
        DistE = (CreateHeightDistribution(ShowerE, Nbins, startHeight))
        MaxBin = DistE.GetMaximumBin()
        AverageHeight[i] += MaxBin*BinHeight/Naverage
        HAWCparticles[i] += DistE.GetBinContent(int(4100/BinHeight))/Naverage
        i += 1

for j in AverageHeight : #turn data into arrays for graph
    HeightCoord.append(j)
    HeightCoordErr.append(j/sqrt(Naverage))
for e in EnergyList: 
    EnergyCoord.append(e)
    EnergyCoordErr.append(0)
for h in HAWCparticles:
    HAWCCoord.append(h)

CanvMaxParticles = ROOT.TCanvas("CanvMaxParticles","Height of max particles as function of E", 1000,1000 )
Graph = ROOT.TGraphErrors(len(EnergyList), EnergyCoord, HeightCoord, EnergyCoordErr, HeightCoordErr)
CanvMaxParticles.SetLogx()
GraphFit = Graph.Fit("pol2")
Graph.SetMarkerStyle(3)
Graph.SetTitle( 'H_{max} versus Energy' )
Graph.GetXaxis().SetTitle( 'Energy initial photon (GeV/c^2)' )
Graph.GetYaxis().SetTitle( 'Height of maximum amount of charged particles' )
Graph.Draw("ap")
CanvMaxParticles.Update()
CanvMaxParticles.Modified()


CanvHAWC = ROOT.TCanvas("CanvHAWC","HAWC measured particles versus Energy", 1000,1000 )
GraphHAWC = ROOT.TGraph(len(EnergyList), EnergyCoord, HAWCCoord)
CanvHAWC.SetLogx()
GraphHAWCFit = GraphHAWC.Fit("expo")
GraphHAWC.SetMarkerStyle(3)
GraphHAWC.SetTitle( 'HAWC measured particles versus Energy' )
GraphHAWC.GetXaxis().SetTitle( 'Energy initial photon (GeV/c^2)' )
GraphHAWC.GetYaxis().SetTitle( 'Number of particles measured by HAWC' )
GraphHAWC.Draw("ap")
CanvHAWC.Update()
CanvHAWC.Modified()

#####################
#assignment e
#####################
Ntest = 100
XaverageRadius = 0.0
YaverageRadius = 0.0
map = 0
for k in range(Ntest):
    HAWCshower = Shower(2500000, startHeight) #Energy at approx 100 particles@HAWC
    map = HAWCmap(HAWCshower, 4100.0) #Generate XY maps of the showers
    XaverageRadius += map.GetRMS(1)/Ntest
    YaverageRadius += map.GetRMS(2)/Ntest
MapCanvas = ROOT.TCanvas("MapCanvas","Map of XY plane HAWC", 1000,1000 )
map.Draw("colz")
MapCanvas.Modified()
MapCanvas.Update()
print("entries " + str(map.GetEntries()))
print("HAWC radius results:")
print("X Average radius = " + str(XaverageRadius))
print("Y Average radius = " + str(YaverageRadius))


###############
#TEST AREA ONLY, enter at your own risk
###############
#TestCanvas = ROOT.TCanvas("TestCanvas","Dummy Title", 1000,1000 )
#TestRanE = ROOT.TH1D("TestRanE", "distribution of random energy", 100, 0, 1)
#for i in range(10000):
#    TestRanE.Fill(RandomEnergy())
#TestRanT.Draw()