import ROOT
from math import *

# provide better print functionality for ROOT TVector3
ROOT.TVector3.__repr__ = ROOT.TVector3.__str__ = lambda v : "({:g},{:g},{:g})".format( v.X(), v.Y(), v.Z() )


class Particle(object):

    "A class to store the information of a particle in our air shower."

    def __init__( self ) :

        self.direction  = ROOT.TVector3(0,0,0)
        self.energy     = 0
        self.kind       = 0 # 1 = gamma, 2 = electron
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


def plot_shower( particles ,
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
    
    for p in particles :
         
        # create a line object to draw 
        line = ROOT.TPolyLine3D(2)
        line.SetPoint(0, p.start_pos.X(), p.start_pos.Y(), p.start_pos.Z() )
        line.SetPoint(1, p.end_pos.X(),   p.end_pos.Y(),   p.end_pos.Z()   )
        line.SetLineColor( p.color )
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


def try_particle():
    
    " show/test the Particle class.. Returns a list of Particles "

    particles = []

    for i in range( 300 ):
        
        # make a Particle object
        p = Particle()
        p.energy = 1000
        p.start_pos = ROOT.TVector3( 0,0,50000 ) # start at 50 km height
        
        # Give the particle a direction that deviates by an angle
        # theta=0.0001 from straight down. The remaining degree of freedom
        # (phi) is randomly chosen.

        theta       = 0.0001
        phi         = ROOT.gRandom.Rndm() * 2 * pi
        p.direction = direction_at_angle( ROOT.TVector3(0,0,-1), theta, phi )
        
        # Compute the end point. let's say the particle lives for 40 km
        
        p.end_pos = p.start_pos + 40000 * p.direction
        p.color = int( phi )+2
        particles.append( p ) # put our particle in the list

    return particles



L = try_particle()
plot_shower( L , "Best Title Ever"  )



