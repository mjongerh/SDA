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


def compute_height(start_height, column_density) :
    a= 8420 # meter
    rho0=1.225 #kg/m^3 != g/cm^3
    RanCd= ROOT.gRandom.Exp(column_density)
    end_height = -a* log(  (RanCd/(a*rho0)) + exp(-start_height/a) )

    return end_height

canv = ROOT.TCanvas("canv","Dummy Title", 780,780 ) #Create a canvas for the art to be shown
histogram = ROOT.TH1D("histogram_of_x1","histogram of x1",100, 100, 10 )
for i in range(5000) :
    histogram.Fill(compute_height(100000, 380))

histogram.Draw()
canv.Modified()
canv.Update()

a= 8420 # meter
rho0=1.225 #kg/m^3 != g/cm^3
print( -a* log((380/(a*rho0)) + exp(-100000/a) ))
