import ROOT
import numpy
from array import array
from math import *

################
# Global Settings
################
bRange = numpy.linspace(1.0, 5.0, 100) #range over which to test b
aRange = numpy.linspace(-50.0, -0.2, 100) #range over which to test a

################
# Global Functions
################
def Chi2Test (m, y, a, b, binwidth) : #For function am+b
    chi2 = 0
    index = 0
    while index < len(m) :
        mui = (a*m[index]+b) #*binwidth[index]
        chi2 += ((y[index]-mui)**2) / (mui**2)
        #print(mui)
        #print(chi2)
        index += 1
    return chi2

################
# Assignment a
################
infile = ROOT.TFile('assignment5-dataset.root')
hData = infile.Get('hdata')
hData.Fit('pol1')
hData.Draw()
Nbins = hData.GetNbinsX()
print("Nbins = "+ str(Nbins) + "  with entries: " + str(hData.GetEntries()))
BinWidthList = []
mList = [] #mass at certain point
yList = [] #how often that mass is measured
print("Expected for for 0th degree pol: y= " + str(sqrt(hData.GetEntries()/Nbins)))  #Expected (approx) value for y=0m+b = sqrt(Nevents/Nbins)

for i in range(Nbins):  #Read the data and put in lists
    yList.append(hData.GetBinContent(i+1))
    mList.append(hData.GetBinCenter(i+1))
    BinWidthList.append(hData.GetBinWidth(i+1))

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

################
# Assignment b
################
hABchi2 = ROOT.TH2F("hABchi2", "Chi^2 as function of a and b", len(aRange), aRange[0], aRange[-1], len(bRange), bRange[0], bRange[-1])
i = 0
j = 0
while i < len(bRange):
    j = 0
    while j < len(aRange):
        test = Chi2Test(mList, yList, aRange[j], bRange[i], BinWidthList)
        #print(test)
        hABchi2.SetBinContent(j, i, 1/test)
        othertest = hABchi2.GetBinContent(j, i)
        #print(othertest)
        j += 1
    i += 1

CanvABchi2 = ROOT.TCanvas("CanvABchi2", "Chi^2 as function of a and b", 1000, 1000)
#hABchi2.SetMinimum(70);
#hABchi2.SetMaximum(100);
hABchi2.Draw("colz")
CanvABchi2.Modified()
CanvABchi2.Update()