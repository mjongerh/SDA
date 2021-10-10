import ROOT, inspect, array, ctypes


#========================================================================
# You may use this minimize and plot_func functions as-is in your 
# excercise. At the bottom of this file is an example how to use them.
#========================================================================

def minimize( function,
              start_values = None,
              ranges       = None,
              verbose      = False,
              maxcalls     = 10000,
              tollerance   = 1e-6 ):
    
    """ 
    Minimize a python function 'function'. The function should have
    any number of (float) arguments. Python instrospection is used
    to know the number (npar) and names of the arguments. 

    ROOT's TMinuit is used to minimize the function with respect
    to all its arguments. The return value is a list with the parameters
    for which 'function' is minimial.

    function     : the function to be minimized
    
    start_values : list of values to use for the initial parameters,
                   default [0.0, 0.0, ... , 0.0]
    
    ranges       : list of lists, defining the min and max values of the 
                   parameters: [ [par1min, par1max], .... , [parnmin, parnmax] ].
                   (Important when you take e.g. logarithms in your 'function'!)
                   
    maxcalls     : maximum number of iterations 

    tollerance   : tollerance, see ROOT.TMinuit().mnhelp("MIGrad")
    """

    args = inspect.getfullargspec( function )[0]  # list of functions arguments
    npar = len(args)
    
    if not start_values : start_values = [0.0] * npar
    if not ranges       : ranges       = [[0,0]] * npar

    step_sizes   = [0.1] * npar
    
    minuit = ROOT.TMinuit( npar )


    # set parameter names, start_values, ...

    for i in range(npar) :
        ierflg = ctypes.c_int()
        minuit.mnparm( i, args[i] , start_values[i] , step_sizes[i], ranges[i][0], ranges[i][1], ierflg )
        

    def fcn( _npar, gin, f, par, iflag ):
        "Wrapper around function, to provide signature expected by minuit."

        # the buffer objects we get passed in behave strangly/buggy ->
        # dont use _npar (but npar instead), and unpack par by hand:
        parlist = [ par[i] for i in range (npar) ] 

        f[0] = function( *parlist )

        if verbose :
            strpars = ",".join( str(x) for x in parlist )
            print ("evaluating %s(%s) = %g " % (function.__name__, strpars, f[0] ))

            
    # call migrad

    minuit.SetFCN( fcn ) # tell minuit to use our wrapper
    arglist = array.array( 'd', [maxcalls, tollerance] )
    minuit.mnexcm( "MIGRAD", arglist , len(arglist) , ierflg )

    # return a list of fitted values
    
    r, errs = [],[]
    for i in range( npar) :
        r.append( ctypes.c_double() )
        errs.append( ctypes.c_double() ) 
        minuit.GetParameter( i, r[-1], errs[-1] )
        
    return r


def fill_hist( func , nbinsx = 60, xmin = -5, xmax =5, nbinsy = 60, ymin= -5, ymax = 5 ):
    
    """ Helper funtion for plotting 2d-functions. Fill a root 
        TH2D with the values from a 2d function. """
    
    ROOT.gStyle.SetPalette( 1 ) # pretty colors
    
    h2 = ROOT.TH2D( 'h', func.__name__ , nbinsx, xmin, xmax, nbinsy, ymin, ymax )
    
    # loop over all the bins and assing the z-value exactly
    # once for each bin.

    for bx in range( 1, h2.GetNbinsX()+1 ):
        for by in range( 1, h2.GetNbinsY() +1 ):
            
            x = h2.GetXaxis().GetBinCenter( bx )
            y = h2.GetYaxis().GetBinCenter( by )        
            b = h2.GetBin( bx, by ) # global bin number

            z = func(x,y)
            h2.SetBinContent( b, z )


    args = inspect.getfullargspec( func )[0]  # list of functions arguments
    print ("args=",args)
    h2.SetXTitle( args[0] )
    h2.SetYTitle( args[1] )
    return h2



# To illustrate the use of 'minmize', we first define a function - with two
# parameters. The challenge is to find the minimim of this function. In this
# case, the answer is known : x=2, y=4
    
def F(x,y) :    
    "Rosenbrock banana function, minimum at (a,a**2)"
    a, b = 2, 100
    return (a-x)**2 + b*(y-x**2)**2


# To easily make plot of F, we abuse the root TH2D histogram class. The function
# fill_hist makes a new TH2D and simply sets the value of each bin to the
# value of the function F.

c = ROOT.TCanvas()
c.SetLogz()
h = fill_hist( F , xmin = 0, ymin =0 ) # turn function into a histogram
h.SetXTitle("x")   # don't forget proper axis labels, etc.
h.Draw('lego2')     # see draw options in root documentation



# -- minimize F --
results = minimize( F ,
                    verbose = True )  # note: named arugment syntax

print ("F is minimal at ", results)


