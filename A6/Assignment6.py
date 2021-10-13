import ROOT, inspect, array, ctypes
import numpy
#from array import array
from math import *

################
# Global Settings
################
# normalization  200 events from 1 to 3 TeV
normalizationBkg = 200/(exp(-1)-exp(-3))
normalizationSig = 10/(0.05 * sqrt(2* pi))
Nbins = 50


################
# Global Functions
################
def FillBkg(histo) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = int(round(binwidth * normalizationBkg * exp(-mass)))
        Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, nevents)
        i += 1
    print("total bkg events: " + str(Ntot))
    return histo

def FillSig(histo) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = int(round(binwidth * normalizationSig * exp(-(mass-2.1)**2 / (2*0.05**2)  )))
        Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, nevents)
        i += 1
    print("total sig events: " + str(Ntot))
    return histo

################
# Assignment a
################
TestHisto = ROOT.TH1F("TestHisto", "data histo", Nbins, 1.0 , 3.0)
TestHisto = FillBkg(TestHisto)
TestHisto = FillSig(TestHisto)
TestHisto.Draw("hist")
