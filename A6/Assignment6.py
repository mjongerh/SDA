import ROOT, inspect, array, ctypes
import numpy
import time
#from array import array
from math import *

################
# Global Settings
################
ROOT.gRandom.SetSeed(int(time.time()))
# normalization  200 events from 1 to 3 TeV
normalizationBkg = 200/(exp(-1)-exp(-3))
normalizationSig = 10/(0.05 * sqrt(2* pi))
Nbins = 50
Random = True  # use random events

################
# Global Functions
################
def ExpecBkg (mass) :
    Nev = int(round(binwidth * normalizationBkg * exp(-mass)))
    if Random : return ROOT.gRandom.Poisson(Nev)
    else : return Nev

def ExpecSig(mass) :
    Nev = int(round(binwidth * normalizationSig * exp(-(mass-2.1)**2 / (2*0.05**2)  )))
    if Random : return ROOT.gRandom.Poisson(Nev)
    else : return Nev

def FillBkg(histo) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = ExpecBkg(mass)
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
        nevents = ExpecSig(mass)
        Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, nevents)
        i += 1
    print("total sig events: " + str(Ntot))
    return histo

def LogLH0 (histo) :
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass)
        MeasNev = histo.GetBinContent(i+1)
        LogL += -ExpectedBkg - log(factorial(MeasNev)) + MeasNev*log(-ExpectedBkg)
        i += 1
    return LogL

def LogLH1 (histo) :
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass)
        ExpectedSig = ExpecSig(mass)
        MeasNev = histo.GetBinContent(i+1)
        LogL += -ExpectedBkg -ExpectedSig - log(factorial(MeasNev)) + MeasNev*log(-ExpectedBkg-ExpectedSig)
        i += 1
    return LogL

################
# Assignment a
################
TestHisto = ROOT.TH1F("TestHisto", "data histo", Nbins, 1.0 , 3.0)
TestHisto = FillBkg(TestHisto)
TestHisto = FillSig(TestHisto)
TestHisto.Draw("hist")

print("LogLH0 = " + str(LogLH0(TestHisto)))
print("LogLH1 = " + str(LogLH1(TestHisto)))