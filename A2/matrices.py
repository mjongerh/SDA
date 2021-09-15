import array, collections
from math import *
from copy import copy
import ROOT


# -----------------------------------------------------
# There are bugs in the matrix multiplication in 
# PyRoot. This is a workaround.
# -----------------------------------------------------

def matrix_mult( m1, m2 ) :

    if type(m2) == float or  type(m2) == int :
        r = copy(m1)
        r*=m2
        return r

    elif type(m2) == ROOT.TVectorD : 
        # turn it into a matrix and back again...
        m2_ = ROOT.TMatrixD( m2.GetNrows(),1 , m2.GetMatrixArray())
        prod = matrix_mult(m1,m2_)
        return ROOT.TVectorD( m2.GetNrows(), prod.GetMatrixArray() )

    if  m2.GetNrows() != m1.GetNcols() :
        print ("error in matrix multiplication: rows and columns don't match.")
        return None

    r=  ROOT.TMatrixD(m1.GetNrows(), m2.GetNcols() )
    r.Mult( m1, m2 )
    return r


def matrix_rmult( m1, m2 ) :    
    if type(m2) == float or  type(m2) == int :
        r = copy(m1)
        r*=m2
        return r

def matrix_add( m1, m2 ) :
    r = copy(m1)
    r+=m2
    return r

def matrix_sub( m1, m2 ) :
    r = copy(m1)
    r -= m2
    return r

ROOT.TMatrixD.__add__  = matrix_add
ROOT.TMatrixD.__sub__  = matrix_sub
ROOT.TVectorD.__add__  = matrix_add
ROOT.TVectorD.__sub__  = matrix_sub
ROOT.TMatrixD.__mul__  = matrix_mult
ROOT.TMatrixD.__rmul__ = matrix_rmult # for float * matrix
ROOT.TVectorD.__rmul__ = matrix_rmult


# decent printing for matrix

def matrix_to_string( M ) :

    r = ""
    for i in range( M.GetNrows() ):
        for j in range ( M.GetNcols() ):
            r += "%5g " % ( M[i][j] )
        r += "\n"

    return r

ROOT.TMatrixD.__str__ = matrix_to_string

# decent printing for vector

def vector_to_string( M ) :
    return "[" + ", ".join( str(M[i]) for i in range( M.GetNrows() )) + "]"

ROOT.TVectorD.__str__ = vector_to_string

# return new, transposed copy

def matrix_transposed( M ) :       
    return ROOT.TMatrixD(ROOT.TMatrixD.kTransposed, M)

ROOT.TMatrixD.trans = matrix_transposed


# Utility functions to make creating matrices and vectors
# a bit more pallatable.

def make_TMatrixD ( dim1, dim2, *args ) :
   """Utility function to make ROOT TMatrixD objects,
    
    The first two arguments are allways the dimensions of the matrix.

    The remaining arguments, can be a list, tuple, etc containing the
    elemants, or the elements directly.
    """


   if len(args)==1 and isinstance( args[0], collections.Iterable ) :

       
        
       if len( args[0] ) == dim1 == dim2 :
           # fill diagonal
           r = ROOT.TMatrixD( dim1, dim2 )
           for i,v in enumerate( args[0] ) :
               r[i][i] = v
           return r
               
       else :
           return ROOT.TMatrixD( dim1, dim2, array.array('d', args[0] ) )
            
   if len(args)==dim1*dim2 :
       return ROOT.TMatrixD( dim1, dim2, array.array('d', args ) )

   if dim1 == dim2 and len(args) == dim1 :
      
       return make_TMatrixD( dim1, dim1, tuple(args) )
   
    # fall back to the original ctor from root - zeros
   return ROOT.TMatrixD( dim1, dim2 )





def make_TVectorD( dim, *args ) :
    
    """Utility function to make ROOT TVectorD objects,
    
    The first argument is always the dimension of the vector.

    The remaining arguments, can be a list, tuple, etc containing the
    elemants, or the elements directly.
    """
    
    if len(args)==1 and isinstance( args[0], collections.Iterable ) :
        return ROOT.TVectorD( dim, array.array('d', args[0] ) )
    
    if len(args) == dim : 
        return ROOT.TVectorD( dim, array.array('d', args ) )
    
    return ROOT.TVectorD(dim, *args )



# -----------------------------------------------------
# The following are two utility funcitons for dealing
# with matrices and functions of matrices.
# -----------------------------------------------------

def numerical_derivative( F , X ) :

    """ Return the matrix of derivivatives of function F.
        F should be a function that takes a TVectorD X as 
        arugment, and that return a TVectorD.""" 
    
    h = 1e-6

    nrows = len( F(X) ) # note: len(TVector) just works - pyroot magic
    ncols = len(X)

    dF_dX = ROOT.TMatrixD( nrows, ncols ) # return value

    for i in range( ncols ):  

        # We produce two copies of X with it's i'th element
        # increased and decreased a bit.
        import copy
        XX = copy.copy(X) # do not modify X itself
 
        XX[i] = X[i] + h
        R2 = F(XX)

        XX[i] = X[i] -h
        R1 = F(XX)
        
        derivative = (R2-R1) # note this is a TVector
        derivative *= 1.0/(2*h)
    
        # fill column i
        for j in range( nrows ):
            dF_dX[j][i] = derivative[j]

    return dF_dX


def draw_contour( X, C ) :
    """ Draw an error-ellipse.
        X is a 2-d TVectorD describing the central values.
        C is the 2x2 covariance matrix """

    M_ = ROOT.TMatrixDEigen( C )
    ME = M_.GetEigenVectors()
    VE = M_.GetEigenValues()

    x,y,V = [],[], ROOT.TVectorD(2)

    # The idea is that there exist coordinates a,b where the
    # elipse is 'horizontal'. That is:
    # (a,b) form an elipse if we let phi run and do 
    # a = ea * sin(phi), b = eb * cos(phi), where ea and eb are 
    # the errors in these coordinates. They are the eigenvalues
    # of C. The eigenvectors tell us how a and b are related to 
    # x and y.

    for phi in range(361): 

        V[0] = sqrt(VE[0][0]) * sin(phi/180.0*pi)
        V[1] = sqrt(VE[1][1]) * cos(phi/180.0*pi)

        U = ME * V
        x.append(U[0]+X[0])
        y.append(U[1]+X[1])

    g = ROOT.TGraph( len(x), array.array('d',x), array.array('d',y) )
    g.SetLineWidth(2)
    g.SetLineColor(4)
    g.Draw("ALP") 
    ROOT.SetOwnership(g, False )
    return g
