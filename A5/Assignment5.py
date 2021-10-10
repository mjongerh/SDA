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

def LogLikelihoodPol3 (a, b, c, d) : #For function am^3+bm^2 + cm +d
    LogL = 0
    index = 0
    while index < len(mList) :
        mui = (a*mList[index]**3 + b*mList[index]**2 + c*mList[index] + d)
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

    for i in range(npar) :
        ierflg = ctypes.c_int()
        minuit.mnparm( i, args[i] , start_values[i] , step_sizes[i], ranges[i][0], ranges[i][1], ierflg )

    def fcn( _npar, gin, f, par, iflag ):
        parlist = [ par[i] for i in range (npar) ] 
        f[0] = function( *parlist )
        if verbose :
            strpars = ",".join( str(x) for x in parlist )
            print ("evaluating %s(%s) = %g " % (function.__name__, strpars, f[0] ))
            
    minuit.SetFCN( fcn ) # tell minuit to use our wrapper
    arglist = array.array( 'd', [maxcalls, tollerance] )
    minuit.mnexcm( "MIGRAD", arglist , len(arglist) , ierflg )

    r, errs = [],[]
    for i in range( npar) :
        r.append( ctypes.c_double() )
        errs.append( ctypes.c_double() ) 
        minuit.GetParameter( i, r[-1], errs[-1] )
        
    return r


def fill_hist( func , nbinsx = 60, xmin = -5, xmax =5, nbinsy = 60, ymin= -5, ymax = 5 ):

    ROOT.gStyle.SetPalette( 1 ) # pretty colors
    h2 = ROOT.TH2D( 'h', func.__name__ , nbinsx, xmin, xmax, nbinsy, ymin, ymax )

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
print("Expected for for 0th degree pol: y= " + str(hData.GetEntries()/Nbins))  #Expected (approx) value for y=0m+b = Nevents/Nbins
#obtained: 5.0202
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


CanvbFlatLikelihood = ROOT.TCanvas("CanvbFlatLikelihood","-Log(L) as function of value of b", 1000,1000 )
GraphbFlatLikelihood = ROOT.TGraph(len(bArray), bArray, LbFit)
GraphbFlatLikelihood.SetMarkerStyle(3)
GraphbFlatLikelihood.SetTitle( '-Log(L) as function of value of b' )
GraphbFlatLikelihood.GetXaxis().SetTitle( 'Value of b' )
GraphbFlatLikelihood.GetYaxis().SetTitle( '-Log(likelihood)' )
GraphbFlatLikelihood.Draw("ap")
CanvbFlatLikelihood.Update()
CanvbFlatLikelihood.Modified()

################
# Assignment b
################
hABLogL = ROOT.TH2F("hABLogL", "-Log(L) as function of a and b", len(aRange)-1, aRange[0], aRange[-1], len(bRange)-1, bRange[0], bRange[-1])
i = 0
j = 0
while i < len(bRange): #loop over 2D parameter space
    j = 0
    while j < len(aRange):
        Value = LogLikelihood(aRange[j], bRange[i]) #calc Log L value and insert in histo
        hABLogL.SetBinContent(j, i, Value)
        j += 1
    i += 1

CanvABLogL = ROOT.TCanvas("CanvABLogL", "Log(L) for a fit y=am+b", 1000, 1000)

minbin = hABLogL.GetMinimumBin()
print("value of min bin is:")
minval = hABLogL.GetBinContent(minbin)

CanvABLogL.SetLogz()
hABLogL.SetMinimum(10.0)
hABLogL.SetMaximum(20.0)
hABLogL.SetTitle("-Log(L) for a fit y=am+b")
hABLogL.Draw("colz")
hABLogL.GetYaxis().SetTitle( 'value of b [1/GeV]' )
hABLogL.GetXaxis().SetTitle( 'Value of a [1/GeV^2]' )

CanvABLogL.Modified()
CanvABLogL.Update()

CanvABLogLcontrour = ROOT.TCanvas("CanvABLogLcontrour", "contour plot for delta -Log(L) < 0.5", 1000, 1000)
CanvABLogLcontrour.SetLogz()
hABLogLcontrour = hABLogL.Clone()
i, j = 0 , 0
while i < len(bRange):
    j = 0
    while j < len(aRange):
        if hABLogLcontrour.GetBinContent(j,i) > minval+0.5 : #Cut away all values outside the range of 1 sigma
            hABLogLcontrour.SetBinContent(j,i, 0.0)
        j += 1
    i += 1
hABLogLcontrour.Draw("colz")
hABLogLcontrour.GetYaxis().SetTitle( 'value of b [1/GeV]' )
hABLogLcontrour.GetXaxis().SetTitle( 'Value of a [1/GeV^2]' )
hABLogLcontrour.SetTitle("Area within #Delta (-Log(L)) <0.5 w.r.t minimum")
CanvABLogLcontrour.Modified()
CanvABLogLcontrour.Update()


CanvDataFitL = ROOT.TCanvas("CanvDataFitL", "Data with a fit y=am+b", 1000, 1000)
FitFunc = ROOT.TF1("FitFunc", "-0.00589*x+7.29", 100, 1000)
FitFuncAUTO = ROOT.TF1("FitFuncAUTO", "-0.005871357987983538*x+7.300526145705545", 100, 1000)
hData.Draw()
FitFunc.Draw("same")

################
# Assignment c
################
RangeValues = [[-0.0085, -0.0041], [6.0, 9.0]]
AutoFitResult = minimize(LogLikelihood, ranges = RangeValues)
print ("Log Likelihood is minimal at ", AutoFitResult)

CanvDataFitLAUTO = ROOT.TCanvas("CanvDataFitLAUTO", "Data with automatic fit y=am+b", 1000, 1000)
FitFuncAUTO = ROOT.TF1("FitFuncAUTO", "-0.005871357987983538*x+7.300526145705545", 100, 1000)
hData.Draw()
FitFuncAUTO.Draw("same")

StartNumbers = [0.0, 0.0, -0.005871357987983538, 7.300526145705545]
AutoFitResultPol3 = minimize(LogLikelihoodPol3,start_values = StartNumbers, maxcalls = 100000)
print ("Log Likelihood for Pol3 Fit is minimal at ", AutoFitResultPol3)
