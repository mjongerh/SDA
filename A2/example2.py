import ROOT
from math import *

# This file shows you how to work with matrices in ROOT.
# For this to work, make sure to copy the file matrices.py from 
# /sda/examples/ to your working directory

import matrices

##------------------------------------------
## -- Creating ROOT Matrices and Vectors --
##------------------------------------------

# To construct ROOT matrix objects, you can use the 
# make_TMatrixD and make_TVectorD functions. They are
# defined in the module matrices. They
# return objects of class TMatrixT<double> and 
# TVectorT<double>, which are documented here
# http://root.cern.ch/root/html600/TVectorT_double_.html
# http://root.cern.ch/root/html600/TMatrixT_double_.html


from matrices import make_TMatrixD
from matrices import make_TVectorD

# Create 2x2 matrix with elements 4,1,0,4
M = make_TMatrixD(2,2, 4,1,0,4)    

D0 = make_TMatrixD( 3,3 )         # 3x3 matrix filled with zeroes

D1 = make_TMatrixD(3,3, 1,2,3 )   # diag(1,2,3)

D2 = make_TMatrixD(3,3, [4,5,6] ) # diag(4,5,6)

print (D0)
print (D1)
print (D2)
                                   
# The elements can also be in a list
N = make_TMatrixD(2,2, [0,0,2,1] ) 

# Create a vector with 2 elements, namely [1,2]
V = make_TVectorD(2,1, 2 )


##-------------------------------------
## -- Printing Matrices and Vectors ---
##-------------------------------------


# You can simply print matrices like this

print ("----M----" )
print (M)
print ("V=",V)


##---------------------------
## --- Matrix arithmetic ---
##---------------------------

# All normal operations are done with the normal notation
# Each of these create a new root matrix (or vector) object
# and leaves the original unchanged.

P = M + N    # matrix addition
Q = N - M    # matrix subtraction
R = M * N    # matrix multiplication
S = M * V    # matrix times a vector
T = 3 * M    # scalar times a matrix
U = (T + N) * M * V


##---------------------------
## --- Transposing       ---
##---------------------------

M.T() # this modifies (transposes) M

transposes_of_M = M.trans() # this leaves M as it is and returns a new matrix
                            # that is the transposed of M


## --- Access to individual elements ---

M[0][0] = 9999
U[1] = -5
print ( M[0][0], U[1] )


# note that in python, the "=" statement does not copy the object

V[0] = 1234
W = V        # W and V are different names for the same object
W2 = 1 * V   # You could abuse the fact that multiplication creates a new
             # matrix object.

V[0] = 99999 #


print ( W[0]  )  # also 99999.  
print ( W2[0] )  # the original 1234 



#--------------------------------------------------------------
# The matrices module provides a helper function to numerically
# compute derivatives of matrix functions.

def test_func( X ):
    """ A function that takes a 2d vector X and 
        returns a 2d vector """ 

    K = ROOT.TVectorD(2)
    K[0] = 3*X[0] + 2*X[1] + X[2]*X[3] + 1
    K[1] = X[0]
    return K

testx = make_TVectorD(4, 
                      [0,1,2,3] )

# the following return the derivative of test_func
D = matrices.numerical_derivative( test_func, testx )
print ( D )



#--------------------------------------------------------------
# The matrices module provides a helper to draw error-countours
# You may use it as a black box for now. (althoug it's well 
# worth studying how it works).

# test it with sigmax = 50 , sigmay-20 and rho=-0.5
graph = matrices.draw_contour( make_TVectorD(2,   [100,200]),
                               make_TMatrixD(2,2, [2500,-500,
                                                  -500,400] ))
graph.GetHistogram().SetXTitle("x-title")

#update the current canvas to redraw the graph
ROOT.gPad.Modified()
ROOT.gPad.Update()

#===================================================================
# As a reward for reading until the end of this file,  here 
# are the data from the excercise as python lists to save
# you some typing :)

x    = [ 812, 1800, 400, 464, 818, 356, 289, 301, 164, 393 ]
errx = [ 41,  50,   33,  35,  33,  22,  27,  29,  19,  24  ]

for i in range( len(x) ):
    print ( "x%d  = %f +/- %f " % (i,x[i],errx[i] ) )

# --- here is the matrix H (needed for the second part) that
#     relates R to u and d

H =  [  0.675 , -0.607 , -0.119 ,  0.010,
       -0.282 ,  1.331 ,  0.027 , -0.049,
       -0.133 ,  0.060 ,  0.477 , -0.078,
        0.024 , -0.299 , -0.186 ,  0.185 ]





