import ROOT
from math import *

# provide better print functionality for ROOT TVector3
ROOT.TVector3.__repr__ = ROOT.TVector3.__str__ = lambda v : "({:g},{:g},{:g})".format( v.X(), v.Y(), v.Z() )
#canv = ROOT.TCanvas("canv","Dummy Title", 1000,1000 ) #Create a canvas for the art to be shown
TestRanE = ROOT.TH1D("TestRanE", "distribution of random energy", 100, 0, 1)
################
# Global Settings
################
a= 8420 # meter
rho0=1.225 #kg/m^3 != g/cm^3
mc2 = 0.510998950 #* 299792458 * 299792458 # value of me *c^2
MaxGen = 100 # Maximum generations computed
Column_density = []
Column_density.append(0)
Column_density.append(380) #photon
Column_density.append(263) #electron
Column_density.append(263) #positron
Generations = []

def plot_shower( shower ,
                 title = "Worst title ever.",
                 xysize = 10, 
                 zsize = 50000 ):

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

    c = ROOT.TCanvas("canv","canvas title", 500,600)

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
        self.energy     = 0
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
    NewParticle1.direction = direction_at_angle(oldparticle.direction, mc2/NewParticle1.energy, phiRan)
    NewParticle2.direction = direction_at_angle(oldparticle.direction, -mc2/NewParticle2.energy, 2*pi - phiRan)
    #print("NEW"+str(NewParticle1) + str(NewParticle2))
    return NewParticle1, NewParticle2



#####################
#assignment a
#####################
#canv = ROOT.TCanvas("canv","Dummy Title", 780,780 ) #Create a canvas for the art to be shown
#histogram = ROOT.TH1D("histogram_of_x1","histogram of x1",100, 100, 10 )
#for i in range(5000) :
#    histogram.Fill(compute_height(100000, 380))

#histogram.Draw()
#canv.Modified()
#canv.Update()

#print("height at mean free path is: ",  -a* log((380/(a*rho0)) + exp(-100000/a) )) #sanity check


#####################
#assignment b
#####################
Particles = []

p = Particle() #Generate first photon
p.kind = 1
p.energy = 1000000  #in MeV
StartHeight = 300000
p.start_pos =  ROOT.TVector3( 0,0,StartHeight ) #0,0,startheight
theta       = 0.0001
phi         = ROOT.gRandom.Rndm() * 2 * pi
p.direction = direction_at_angle( ROOT.TVector3(0,0,-1), theta, phi )
Particles.append( p )
Generations.append(Particles)

for i in range(MaxGen) :
    #create list for newly generated particles
    NewParticles = []
    #loop over particles in gen[i]
    for particle in Generations[i] :
        EndOfShower = 0
        #make them move if they have energy left
        if particle.energy >= 85.0 :
            particle.end_pos = particle.start_pos + compute_height(particle.start_pos, Column_density[particle.kind] ) * particle.direction
            #create 2 new particles, calc their properties
            NewParts = GenNewPart(particle)
            NewParticles.append(NewParts[0])
            NewParticles.append(NewParts[1])
            EndOfShower += 1
        else :
            particle.end_pos = particle.start_pos
    #gen[i+1] = NewParticles
    if EndOfShower==0 : break #Stop the loop when all particles are below 85 MeV
    Generations.append(NewParticles)

plot_shower(Generations, "Best Title ever", 150, StartHeight)

#####################
#assignment c
#####################
Nbins = 100 #Slice the height in bins
BinWidth =StartHeight/Nbins
HeightDist = ROOT.TH1D("HeightDist", "distribution of particles at each height", Nbins, 0, StartHeight)
for Gen in Generations :
    for Part in Gen :
        A = floor(Part.end_pos.Z()/BinWidth) #get the lowest bin the particle has been in
        B = floor(Part.start_pos.Z()/BinWidth) #get the highest bin
        print(Part.end_pos.Z()/BinWidth)
        print(A)
        i = A
        while i<=B: #add 1 to all bins in between
            HeightDist.Fill(i*BinWidth)
            i += 1
HeightDistCanv = ROOT.TCanvas("HeightDistCanv","Dummy Title", 1000,1000 )
HeightDist.Draw()


###############
#TEST AREA ONLY, enter at your own risk
###############
#TestCanvas = ROOT.TCanvas("TestCanvas","Dummy Title", 1000,1000 )
#for i in range(10000):
#    TestRanE.Fill(RandomEnergy())
#TestRanE.Draw()