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
def Chi2Test (m, y, a, b, binwidth) : #For function am+b
    chi2 = 0
    for i in range(len(m)) :
        mui= (a*m[i]+b)*binwidth[i]
        chi2 += ((y[i]-mui)**2) / (mui**2)
    return chi2

################
# Assignment a
################
infile = ROOT.TFile('assignment5-dataset.root')
hData = infile.Get('hdata')
hData.Fit('pol0')
hData.Draw()
Nbins = hData.GetNbinsX()
print("Nbins = "+ str(Nbins) + "  with entries: " + str(hData.GetEntries()))
BinWidthList = []
mList = [] #mass at certain point
yList = [] #how often that mass is measured
Expectedb = 0

for i in range(Nbins):  #Read the data and put in lists
    yList.append(hData.GetBinContent(i))
    mList.append(hData.GetBinCenter(i))
    BinWidthList.append(hData.GetBinWidth(i))
    Expectedb += hData.GetBinContent(i)/Nbins  #expected value of b is average height of histo

bRange = numpy.linspace(1.0, 4.0, 100) #range over which to test b
LbFit = array( 'd' )
bArray = array( 'd' )

for i in range(len(bRange)):
    LbFit.append(Chi2Test(mList, yList, 0, bRange[i], BinWidthList))
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
