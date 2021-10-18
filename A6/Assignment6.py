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
PenaltyTerm = 10000
offset = 0

################
# Global Functions
################
def ExpecBkg (mass, binW) :
    Nev = binW * normalizationBkg * exp(-mass)
    return Nev

def ExpecSig(mass, binW, massguess = 2.1) :
    Nev = binW * normalizationSig * exp(-(mass-massguess)**2 / (2*0.05**2))
    return Nev

def FillBkg(histo) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    #Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = ExpecBkg(mass, binwidth)
        NEvents = ROOT.gRandom.Poisson(nevents)
        #Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, NEvents)
        i += 1
    #print("total bkg events: " + str(Ntot))
    return histo

def FillSig(histo, massguess = 2.1) :
    binwidth = histo.GetBinWidth(0) #assumed binwidth to be constant
    i=0
    #Ntot = 0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        nevents = ExpecSig(mass, binwidth, massguess)
        NEvents = ROOT.gRandom.Poisson(nevents)
        #Ntot += nevents #check if reasonable amount of events are used
        histo.Fill(mass, NEvents)
        i += 1
    #print("total sig events: " + str(Ntot))
    return histo

def LogLH0 (histo) : #Log likelihood guessing H0 is true
    binwidth = histo.GetBinWidth(1)
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass, binwidth) + offset
        MeasNev = histo.GetBinContent(i+1) + offset
        if ExpectedBkg <= 0 : 
            LogL += - PenaltyTerm
            i+=1
            continue
        LogL += -ExpectedBkg - log(factorial(MeasNev)) + MeasNev*log(ExpectedBkg)
        i += 1
    return LogL

def LogLH1 (histo) :#Log likelihood guessing H1 is true
    binwidth = histo.GetBinWidth(1)
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass, binwidth) + offset
        ExpectedSig = ExpecSig(mass, binwidth) + offset
        MeasNev = histo.GetBinContent(i+1) + offset
        if (ExpectedBkg + ExpectedSig) <= 0 : 
            LogL += - PenaltyTerm
            i+=1
            continue
        LogL += -ExpectedBkg -ExpectedSig - log(factorial(MeasNev)) + MeasNev*log(ExpectedBkg+ExpectedSig)
        i += 1
    return LogL

def LogLHM (histo, massguess) :
    binwidth = histo.GetBinWidth(1)
    i=0
    LogL = 0.0
    while i < Nbins :
        mass = histo.GetBinCenter(i+1)
        ExpectedBkg = ExpecBkg(mass, binwidth) + offset
        ExpectedSig = ExpecSig(mass, binwidth, massguess) + offset
        MeasNev = histo.GetBinContent(i+1) + offset
        if (ExpectedBkg + ExpectedSig) <= 0 : 
            LogL += - PenaltyTerm
            i+=1
            continue
        LogL += -ExpectedBkg -ExpectedSig - log(factorial(MeasNev)) + MeasNev*log(ExpectedBkg+ExpectedSig)
        i += 1
    return LogL

def LogLRTS (histo) :
    return LogLH1(histo) - LogLH0(histo)

def LLR(histo, massguess) :
    return LogLHM(histo, massguess) - LogLH0(histo)

def CalcPval(histo, nbins = Nbins) :
    j=0
    IntTot = 0.0
    IntP = 0.0
    IntStart = LogLRTS(histo)
    while j < nbins + 2 :  #include under- and overflow bins
        IntTot += LLRHistoH0.GetBinContent(j)
        if LLRHistoH0.GetBinCenter(j) >= IntStart :
            IntP += LLRHistoH0.GetBinContent(j)
        j += 1
    Pvalue = IntP / IntTot
    return Pvalue

def CalcPvalHM(histo, llrguess, nbins = Nbins) :
    j=0
    IntTot = 0.0
    IntP = 0.0
    IntStart = llrguess
    while j < nbins + 2 :  #include under- and overflow bins
        IntTot += LLRHistoH0M.GetBinContent(j)
        if LLRHistoH0M.GetBinCenter(j) >= IntStart :
            IntP += LLRHistoH0M.GetBinContent(j)
        j += 1
    Pvalue = IntP / IntTot
    return Pvalue

def GetBestLLRMass(histo, massarray) :
    k = 0
    BestLLR = -99999999.0
    BestMass = 0.0
    while k < len(massarray) :
        llr = LLR(histo, massarray[k])
        if llr > BestLLR :
            BestLLR = llr
            BestMass = MassArray[k]
        k += 1
    return BestLLR, BestMass

################
# Assignment a
################
TestCanv = ROOT.TCanvas("TestCanv","data test", 1000,1000 )
TestHisto = ROOT.TH1F("TestHisto", "data histo", Nbins, 1.0 , 3.0)
TestHisto = FillBkg(TestHisto)
TestHisto = FillSig(TestHisto, 2.9)
TestHisto.Draw("hist")
print("T1: " + str(LogLRTS(TestHisto)))


################
# Assignment b
################
print("LLR of test 1: " + str(LogLRTS(TestHisto)))

################
# Assignment c
################
LLRHistoH0 = ROOT.TH1F("LLRHistoH0", "LLR given H0 histo", Nbins, -10.0 , 10.0)
LLRHistoH1 = ROOT.TH1F("LLRHistoH1", "LLR given H1 histo", Nbins, -10.0 , 10.0)
TempHisto = ROOT.TH1F("TempHisto", "data histo", Nbins, 1.0 , 3.0)
TempHisto2 = ROOT.TH1F("TempHisto2", "data histo", Nbins, 1.0 , 3.0)

j = 0
while j < 10000 :
    TempHisto = FillBkg(TempHisto)
    #print("LLR H0 : " + str(LogLRTS(TempHisto)))
    LLRHistoH0.Fill(LogLRTS(TempHisto))
    TempHisto2 = FillSig(TempHisto2)
    TempHisto2 = FillBkg(TempHisto2)
    LLRHistoH1.Fill(LogLRTS(TempHisto2))
    #print("LLR H1 : " + str(LogLRTS(TempHisto2)))
    TempHisto.Reset("ICES")
    TempHisto2.Reset("ICES")
    j += 1
CanvLLRHistoH1 = ROOT.TCanvas("CanvLLRHistoH1","LLR given H1", 1000,1000 )
LLRHistoH1.Draw()

################
# Assignment d
################
CanvLLRHistoH0 = ROOT.TCanvas("CanvLLRHistoH0","LLR given H0", 1000,1000 )
LLRHistoH0.Draw()

TempHisto = FillBkg(TempHisto)
TempHisto = FillSig(TempHisto)
print("P value of test is: " + str(CalcPval(TempHisto)))
TempHisto.Reset("ICES")

infile = ROOT.TFile('assignment6-dataset.root')
hData = infile.Get('hdata')
print("P value of given data is: " + str(CalcPval(hData)))

################
# Assignment e
################
MassArray = numpy.linspace(1.0, 3.0, 20, endpoint = False)
LLRHistoHM = ROOT.TH1F("LLRHistoHM", "best LLR as function of mass histo", Nbins, -10.0 , 10.0)
LLRHistoH0M = ROOT.TH1F("LLRHistoH0M", "LLR of Hm given H0", Nbins, -10.0 , 10.0)
PvalHistoHM = ROOT.TH1F("PvalHistoHM", "p value as function of true mass", len(MassArray), 1.0 , 3.0)
LLRHistoH0
j = 0
NtestSim = 1000
while j < len(MassArray) :
    #TempHisto = FillBkg(TempHisto)
    #LLRHistoH0.Fill(LogLRTS(TempHisto))
    p=0 
    while p < NtestSim : # Generate LLR plot with mass j
        TempHisto2 = FillSig(TempHisto2, MassArray[j])
        TempHisto2 = FillBkg(TempHisto2)
        TempHisto = FillBkg(TempHisto)
        BestH0 = GetBestLLRMass(TempHisto, MassArray) # Get best LLR given H0
        LLRHistoH0M.Fill(BestResult[0])
        BestResult = GetBestLLRMass(TempHisto2, MassArray) # find best LLR for any mass
        LLRHistoHM.Fill(BestResult[0])
        
        TempHisto2.Reset("ICES")
        TempHisto.Reset("ICES")
        p += 1
    for x in range(NtestSim):
        TempHisto2 = FillSig(TempHisto2, MassArray[j]) #Generate a p value
        TempHisto2 = FillBkg(TempHisto2)
        PvalHM = CalcPvalHM(TempHisto2, BestResult[0])
        PvalHistoHM.Fill(MassArray[j], PvalHM/NtestSim)
        TempHisto2.Reset("ICES")
    j += 1

CanvLLRHistoHM = ROOT.TCanvas("CanvLLRHistoHM","LLR given HM", 1000,1000 )
LLRHistoHM.Draw()
CanvPvalHistoHM = ROOT.TCanvas("CanvPvalHistoHM","p value as function of true mass", 1000,1000 )
PvalHistoHM.Draw()

# loop over mass and generate LLR plot of H0 and HM
#          for each mass, loop over all masses and test their LLR, keep track of the best LLR and MASS
#          get P value for each best sets
