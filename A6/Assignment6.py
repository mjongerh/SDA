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
PenaltyTerm = 100

################
# Global Functions
################
def ExpecBkg (mass, binW) :
    Nev = int(round(binW * normalizationBkg * exp(-mass)))
    if Random : return ROOT.gRandom.Poisson(Nev)
    else : return Nev

def ExpecSig(mass, binW) :
    Nev = int(round(binW * normalizationSig * exp(-(mass-2.1)**2 / (2*0.05**2)  )))
    if Random : return ROOT.gRandom.Poisson(Nev)
    else : return Nev

def FillBkg(histo) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    #Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = ExpecBkg(mass, binwidth)
        #Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, nevents)
        i += 1
    #print("total bkg events: " + str(Ntot))
    return histo

def FillSig(histo) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    #Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = ExpecSig(mass, binwidth)
        #Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, nevents)
        i += 1
    #print("total sig events: " + str(Ntot))
    return histo

def LogLH0 (histo) :
    binwidth = histo.GetBinWidth(0)
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass, binwidth)
        MeasNev = histo.GetBinContent(i+1)
        if ExpectedBkg <= 0 : 
            LogL += -ExpectedBkg - log(factorial(MeasNev)) - PenaltyTerm
            i+=1
            continue
        LogL += -ExpectedBkg - log(factorial(MeasNev)) + MeasNev*log(ExpectedBkg)
        i += 1
    return LogL

def LogLH1 (histo) :
    binwidth = histo.GetBinWidth(0)
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass, binwidth)
        ExpectedSig = ExpecSig(mass, binwidth)
        MeasNev = histo.GetBinContent(i+1)
        if (ExpectedBkg+ExpectedSig) <= 0 : 
            LogL += -ExpectedBkg -ExpectedSig - log(factorial(MeasNev)) - PenaltyTerm
            i+=1
            continue
        LogL += -ExpectedBkg -ExpectedSig - log(factorial(MeasNev)) + MeasNev*log(ExpectedBkg+ExpectedSig)
        i += 1
    return LogL

def LogLRTS (histo) :
    return (LogLH0(TestHisto)/LogLH1(TestHisto))

################
# Assignment a
################
TestHisto = ROOT.TH1F("TestHisto", "data histo", Nbins, 1.0 , 3.0)
TestHisto = FillBkg(TestHisto)
TestHisto = FillSig(TestHisto)
TestHisto.Draw("hist")
################
# Assignment b
################
print(LogLRTS(TestHisto))

################
# Assignment c
################
LLRHisto = ROOT.TH1F("LLRHisto", "data histo", Nbins, 1.0 , 0.0)
TempHisto = ROOT.TH1F("TempHisto", "data histo", Nbins, 1.0 , 3.0)

j = 0
while j < 1000 :
    TempHisto = FillBkg(TempHisto)
    TempHisto = FillSig(TempHisto)
    LLRHisto.Fill(LogLRTS(TempHisto))
    TempHisto.Reset("ICES")
    j += 1
LLRHisto.Draw()
################
# Assignment d
################
