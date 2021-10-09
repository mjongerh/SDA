import ROOT
import numpy
from array import array
from math import *

################
# Global Settings
################

################
# Global Functions
################
def LogLikelihood (m, a, b) : #For function am+b
    SumL = 0
    for mi in m :
        SumL += log(a*mi+b)
    return SumL

################
# Assignment a
################
infile = ROOT.TFile('assignment5-dataset.root')
hData = infile.Get('hdata')
hData.Draw()
Nbins = hData.GetNbinsX()
BinWidthList = []
mList = []
yList = []
Expectedb = 0

for i in range(Nbins):  #Read the data and put in lists
    yList.append(hData.GetBinContent(i))
    mList.append(hData.GetBinCenter(i))
    BinWidthList.append(hData.GetBinWidth(i))
    Expectedb += hData.GetBinContent(i)/Nbins  #expected value of b is average height of histo

bRange = numpy.linspace(0.0, 10.0, 100) #range over which to test b
LbFit = array( 'd' )
bArray = array( 'd' )

for i in range(len(bRange)):
    LbFit.append(LogLikelihood(mList, 0, bRange[i]))
    bArray.append(bRange[i])

print("Expected value of b  is " + str(Expectedb))
CanvbFlatLikelihood = ROOT.TCanvas("CanvbFlatLikelihood","likelihood as function of value of b", 1000,1000 )
GraphbFlatLikelihood = ROOT.TGraph(len(bArray), bArray, LbFit)
GraphbFlatLikelihood.SetMarkerStyle(3)
GraphbFlatLikelihood.SetTitle( 'likelihood as function of value of b' )
GraphbFlatLikelihood.GetXaxis().SetTitle( 'Value of b' )
GraphbFlatLikelihood.GetYaxis().SetTitle( 'likelihood response' )
GraphbFlatLikelihood.Draw("ap")
CanvbFlatLikelihood.Update()
CanvbFlatLikelihood.Modified()
