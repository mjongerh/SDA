import ROOT
import numpy
from array import array
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
aRange = numpy.linspace(-0.0085, -0.0045, 100) #range over which to test a

################
# Global Functions
################
def Chi2Test (m, y, a, b, binwidth) : #For function am+b
    chi2 = 0
    index = 0
    while index < len(m) :
        mui = (a*m[index]*binwidth[index]+b) #*binwidth[index]
        chi2 += ((y[index]-mui)) / (mui)
        #print(mui)
        #print(chi2)
        index += 1
    return chi2

def LogLikelihood (m, y, a, b, binwidth) : #For function am+b
    LogL = 0
    index = 0
    while index < len(m) :
        mui = (a*m[index]+b) #*binwidth[index]
        LogL += ((y[index]-mui)**2) / (2*mui**2)
        #LogL += log(abs(mui))
        index += 1
    return LogL

################
# Assignment a
################
print("Expected for for 0th degree pol: y= " + str(sqrt(hData.GetEntries()/Nbins)))  #Expected (approx) value for y=0m+b = sqrt(Nevents/Nbins)

for i in range(Nbins):  #Read the data and put in lists
    yList.append(hData.GetBinContent(i+1))
    mList.append(hData.GetBinCenter(i+1))
    BinWidthList.append(hData.GetBinWidth(i+1))

LbFit = array( 'd' )
bArray = array( 'd' )
bFlatRange = numpy.linspace(3.0, 7.0, 100) #range over which to test b

for i in range(len(bFlatRange)):
    LbFit.append(LogLikelihood(mList, yList, 0, bFlatRange[i], BinWidthList))
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
hABLogL = ROOT.TH2F("hABLogL", "Chi^2 as function of a and b", len(aRange)-1, aRange[0], aRange[-1], len(bRange)-1, bRange[0], bRange[-1])
i = 0
j = 0
while i < len(bRange):
    j = 0
    while j < len(aRange):
        test = LogLikelihood(mList, yList, aRange[j], bRange[i], BinWidthList)
        #print(test)
        hABLogL.SetBinContent(j, i, test)
        #othertest = hABLogL.GetBinContent(j, i)
        #print(othertest)
        j += 1
    i += 1


CanvABLogL = ROOT.TCanvas("CanvABLogL", "Log(L) for a fit y=am+b", 1000, 1000)
minbin = hABLogL.GetMinimumBin()
print("value of min bin is:")
print(hABLogL.GetBinContent(minbin))
#x, y, z = ROOT.Long(), ROOT.Long(), ROOT.Long()
#hABLogL.GetBinXYZ( maxbin, x, y, z )
#print("x max = " + str(x) + "   y max = " + str(y))
CanvABLogL.SetLogz()
#hABLogL.GetBinXYZ(maxbin, xmax, ymax, zmax)
hABLogL.SetMinimum( hABLogL.GetBinContent(minbin)-0.01) #10.0)
hABLogL.SetMaximum(hABLogL.GetBinContent(minbin)+0.5) #20.0)
hABLogL.SetTitle("Log(L) for a fit y=am+b")
hABLogL.Draw("colz")
hABLogL.GetYaxis().SetTitle( 'value of b' )
hABLogL.GetXaxis().SetTitle( 'Value of a' )

CanvABLogL.Modified()
CanvABLogL.Update()


CanvDataFitL = ROOT.TCanvas("CanvDataFitL", "Data with a fit y=am+b", 1000, 1000)
#hData.Fit('pol1')
FitFunc = ROOT.TF1("FitFunc", "-0.0059*x+7.29", 100, 1000)
hData.Draw()
FitFunc.Draw("same")