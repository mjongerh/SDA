import ROOT
from math import *

import matrices

from matrices import make_TMatrixD
from matrices import make_TVectorD

# Data points
x    = [ 812, 1800, 400, 464, 818, 356, 289, 301, 164, 393 ]
xerr = [ 41,  50,   33,  35,  33,  22,  27,  29,  19,  24  ]

# Matrix
H =  [  0.675 , -0.607 , -0.119 ,  0.010,
       -0.282 ,  1.331 ,  0.027 , -0.049,
       -0.133 ,  0.060 ,  0.477 , -0.078,
        0.024 , -0.299 , -0.186 ,  0.185 ]
Hmatrix = make_TMatrixD (4,4, H)

def CreateR( x ):
    """ A function that takes a 2d vector X and 
        returns a 2d vector """ 

    K = ROOT.TVectorD(4)
    K[0] = x[2]/x[0]
    K[1] = x[3]/x[1]
    K[2] = (x[6]-x[8]*x[2]/x[0])/x[4]
    K[3] = (x[7]-x[9]*x[3]/x[1])/x[5]
    return K

R = CreateR(x)
#R[0] = x[2]/x[0]
#R[1] = x[3]/x[1]
#R[2] = (x[6]-x[8]*x[2]/x[0])/x[4]
#R[3] = (x[7]-x[9]*x[3]/x[1])/x[5]

Rerr = ROOT.TVectorD(4)
Rerr[0] = R[0] * sqrt( (xerr[2]/x[2])**2 + (xerr[0]/x[0])**2 )
Rerr[1] = R[1] * sqrt( (xerr[3]/x[3])**2 + (xerr[1]/x[1])**2 )
Rerr[2] = R[2] * sqrt( (((x[8]**2 * x[2]**2) / (x[0]**2))*((xerr[8]/x[8])**2 + (xerr[6]/x[6])**2 + (xerr[0]/x[0])**2)+xerr[6]**2) / (R[2]*x[4]) +(xerr[4]/x[4])**2 )
Rerr[3] = R[3] * sqrt( (((x[9]**2 * x[3]**2) / (x[1]**2))*((xerr[9]/x[9])**2 + (xerr[7]/x[7])**2 + (xerr[1]/x[1])**2)+xerr[7]**2) / (R[3]*x[5]) +(xerr[5]/x[5])**2 )


print ("R=", R)
print ("\nRerr = ", Rerr)

Mcovar_R = make_TMatrixD (4,4, [Rerr])
print ("Mcovar_R", Mcovar_R)
print ("Mcovar_R[0][0] = ", Mcovar_R[0][0])
Vcoupling = Hmatrix * R
Mcovar_coupling = Hmatrix * Mcovar_R * Hmatrix.trans()

print (Vcoupling)
print (Mcovar_coupling)
