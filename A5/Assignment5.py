import ROOT, inspect, array, ctypes
import numpy
#from array import array
from math import *

################
# Global Settings
################
infile = ROOT.TFile('assignment5-dataset.root')
hData = infile.Get('hdata')
Nbins = hData.GetNbinsX()
print("Nbins = "+ str(Nbins) + "  with entries: " + str(hData.GetEntries()))
BinWidthList = []
mList = [] #mass at certain point
yList = [] #how often that mass is measured

bRange = numpy.linspace(6.0, 9.0, 100) #range over which to test b
aRange = numpy.linspace(-0.0085, -0.0041, 100) #range over which to test a

################
# Global Functions
################
def LogLikelihood (a, b) : #For function am+b
    LogL = 0
    index = 0
    while index < len(mList) :
        mui = (a*mList[index]+b)
        LogL += ((yList[index]-mui)**2) / (2*mui**2)
        index += 1
    return LogL

def minimize( function,
              start_values = None,
              ranges       = None,
              verbose      = False,
              maxcalls     = 10000,
              tollerance   = 1e-6 ):

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


################
# Assignment a
################
print("Expected for for 0th degree pol: y= " + str(sqrt(hData.GetEntries()/Nbins)))  #Expected (approx) value for y=0m+b = sqrt(Nevents/Nbins)

for i in range(Nbins):  #Read the data and put in lists
    yList.append(hData.GetBinContent(i+1))
    mList.append(hData.GetBinCenter(i+1))
    BinWidthList.append(hData.GetBinWidth(i+1))

LbFit = array.array( 'd' )
bArray = array.array( 'd' )
bFlatRange = numpy.linspace(3.0, 7.0, 100) #range over which to test b

for i in range(len(bFlatRange)):
    LbFit.append(LogLikelihood(0, bFlatRange[i]))
    bArray.append(bFlatRange[i])


CanvbFlatLikelihood = ROOT.TCanvas("CanvbFlatLikelihood","Log(L) as function of value of b", 1000,1000 )
GraphbFlatLikelihood = ROOT.TGraph(len(bArray), bArray, LbFit)
GraphbFlatLikelihood.SetMarkerStyle(3)
GraphbFlatLikelihood.SetTitle( 'Log(L) as function of value of b' )
GraphbFlatLikelihood.GetXaxis().SetTitle( 'Value of b' )
GraphbFlatLikelihood.GetYaxis().SetTitle( 'Log(likelihood)' )
GraphbFlatLikelihood.Draw("ap")
CanvbFlatLikelihood.Update()
CanvbFlatLikelihood.Modified()

################
# Assignment b
################
hABLogL = ROOT.TH2F("hABLogL", "Log(L) as function of a and b", len(aRange)-1, aRange[0], aRange[-1], len(bRange)-1, bRange[0], bRange[-1])
i = 0
j = 0
while i < len(bRange):
    j = 0
    while j < len(aRange):
        test = LogLikelihood(aRange[j], bRange[i])
        #print(test)
        hABLogL.SetBinContent(j, i, test)
        #othertest = hABLogL.GetBinContent(j, i)
        #print(othertest)
        j += 1
    i += 1


CanvABLogL = ROOT.TCanvas("CanvABLogL", "Log(L) for a fit y=am+b", 1000, 1000)
minbin = hABLogL.GetMinimumBin()
print("value of min bin is:")
minval = hABLogL.GetBinContent(minbin)
#x, y, z = ROOT.Long(), ROOT.Long(), ROOT.Long()
#hABLogL.GetBinXYZ( maxbin, x, y, z )
#print("x max = " + str(x) + "   y max = " + str(y))
CanvABLogL.SetLogz()
#hABLogL.GetBinXYZ(maxbin, xmax, ymax, zmax)
hABLogL.SetMinimum(10.0) #hABLogL.GetBinContent(minbin)-0.01) Use these values for delta log = 0.5
hABLogL.SetMaximum(20.0) #hABLogL.GetBinContent(minbin)+0.5)
hABLogL.SetTitle("Log(L) for a fit y=am+b")
hABLogL.Draw("colz")
hABLogL.GetYaxis().SetTitle( 'value of b [1/GeV]' )
hABLogL.GetXaxis().SetTitle( 'Value of a [1/GeV^2]' )

CanvABLogL.Modified()
CanvABLogL.Update()

CanvABLogLcontrour = ROOT.TCanvas("CanvABLogLcontrour", "contour plot for delta Log(L) < 0.5", 1000, 1000)
CanvABLogLcontrour.SetLogz()
hABLogLcontrour = hABLogL.Clone()
i, j = 0 , 0
while i < len(bRange):
    j = 0
    while j < len(aRange):
        if hABLogLcontrour.GetBinContent(j,i) > minval+0.5 :
            hABLogLcontrour.SetBinContent(j,i, 0.0)
        j += 1
    i += 1
hABLogLcontrour.Draw("colz")
hABLogLcontrour.GetYaxis().SetTitle( 'value of b [1/GeV]' )
hABLogLcontrour.GetXaxis().SetTitle( 'Value of a [1/GeV^2]' )

CanvABLogLcontrour.Modified()
CanvABLogLcontrour.Update()


CanvDataFitL = ROOT.TCanvas("CanvDataFitL", "Data with a fit y=am+b", 1000, 1000)
#hData.Fit('pol1')
FitFunc = ROOT.TF1("FitFunc", "-0.00589*x+7.29", 100, 1000)
#best fit -0.00589m + 7.29
#-0.00449 6.248
#-0.00749  +8.67885
# a= -0.00589 +-.00160
# b = 7.29 +-1.39 
hData.Draw()
FitFunc.Draw("same")


################
# Assignment c
################
ranges = [[-0.0085, -0.0041], [6.0, 9.0]]
AutoFitResult = minimize(LogLikelihood, range = ranges, verbose = True)
print ("Log Likelihood is minimal at ", AutoFitResult)
