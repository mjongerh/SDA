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
        mui= b*binwidth[i] #(a*m[i]+b)*binwidth[i]
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
print("Expected for for 0th degree pol: y= " + str(sqrt(hData.GetEntries()/Nbins)))  #Expected (approx) value for y=0m+b = sqrt(Nevents/Nbins)

for i in range(Nbins):  #Read the data and put in lists
    yList.append(hData.GetBinContent(i))
    mList.append(hData.GetBinCenter(i))
    BinWidthList.append(hData.GetBinWidth(i))

bRange = numpy.linspace(1.0, 4.0, 100) #range over which to test b
LbFit = array( 'd' )
bArray = array( 'd' )

for i in range(len(bRange)):
    LbFit.append(Chi2Test(mList, yList, 0, bRange[i], BinWidthList))
    bArray.append(bRange[i])


CanvbFlatLikelihood = ROOT.TCanvas("CanvbFlatLikelihood","chi^2  as function of value of b", 1000,1000 )
GraphbFlatLikelihood = ROOT.TGraph(len(bArray), bArray, LbFit)
GraphbFlatLikelihood.SetMarkerStyle(3)
GraphbFlatLikelihood.SetTitle( 'chi^2 as function of value of b' )
GraphbFlatLikelihood.GetXaxis().SetTitle( 'Value of b' )
GraphbFlatLikelihood.GetYaxis().SetTitle( 'likelihood response' )
GraphbFlatLikelihood.Draw("ap")
CanvbFlatLikelihood.Update()
CanvbFlatLikelihood.Modified()
