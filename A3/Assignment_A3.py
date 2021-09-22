import ROOT             # This will make root available in your script
from math import *      # Use math functions (cos, sin, etc) 


# -----------------------------
#  make root look a bit better
# -----------------------------
ROOT.gStyle.SetOptStat(0)           # Do not show statistics box 
ROOT.gStyle.SetPadLeftMargin(0.14)  # make room for y-title, adjust with pad.SetLeftMargin()
ROOT.gStyle.SetTitleOffset(1.8,"y") # adjust with histogram.GetYaxis().SetTitleOffset)

canv = ROOT.TCanvas("canv","plots for SDA course - ROOT 1", 2400,2400 )

canv.Divide(3,3)  # See link above for documentation of the Divide method.
canv.cd(1)        # Switch to the first sub-canvas.

histogram_of_x1 = ROOT.TH1D("histogram_of_x1","histogram of x1",100, 100, 10 ) # name and title  # 100 bins between 0 and 7000 GeV, since it is now the sum, the range has to be increased beyond 3TeV
histogram_of_x2 = ROOT.TH1D("histogram_of_x2","histogram of x2",100, 100, 10 )
histogram_of_u2 = ROOT.TH1D("histogram_of_u2","histogram of u2",100, 100, 10 )
histogram_of_un = ROOT.TH1D("histogram_of_un","histogram of un",100, 100, 10 )
histogram_of_u1 = ROOT.TH1D("histogram_of_u1","histogram of u1",100, 100, 10 )
histogram_of_u10 = ROOT.TH1D("histogram_of_u10","histogram of u10",100, 100, 10 )

Nval = 1000
class FunctionsForMe :
    def RanCauchy(mean = 0.0, sigma = 1.0):
        return (ROOT.gRandom.Gaus(mean,sigma)/ROOT.gRandom.Gaus(mean,sigma))

def GenNumbers(func, mean = 0.0, sigma =1.0) :
    if (func == 'Cauchy'):                              #Determine function for random numbers
        RanFunc = getattr(FunctionsForMe, 'RanCauchy')
    else :
        RanFunc = getattr(ROOT.gRandom, func)

    for i in range (5000) :
        x1 = 0
        Xsum = 0
        for j in range(Nval) :
            if (func == 'Rndm'):
                Xsum += RanFunc()   #generate numbers
            elif (func == 'Exp'):
                Xsum += RanFunc(2)  #2, for exp(-x/2)
            else :
                Xsum += RanFunc(mean, sigma)

            if (j==0) :
                histogram_of_x1.Fill(Xsum)      #Fills histograms accordingly
                x1 = Xsum
            if (j==1):
                histogram_of_u2.Fill(Xsum/(j+1))
                histogram_of_x2.Fill(Xsum-x1)
            if (j==9):
                histogram_of_u10.Fill(Xsum/(j+1))
            if (j==Nval-1):
                histogram_of_un.Fill(Xsum/(j+1))

GenNumbers('Exp', 0.5, 0.1)  # 'Rndm' 'Gaus',mean,sigma 'Cauchy',mean,sigma (of the underlying gaus distos

histogram_of_x1.Draw()
MEANx1 = histogram_of_x1.GetMean()
RMSx1 = histogram_of_x1.GetRMS()
VARx1 = RMSx1**2
canv.cd(2)
histogram_of_x2.Draw()
MEANx2 = histogram_of_x2.GetMean()
RMSx2 = histogram_of_x2.GetRMS()
VARx2 = RMSx2**2
canv.cd(3)
histogram_of_u2.Draw()
MEANu2 = histogram_of_u2.GetMean()
RMSu2 = histogram_of_u2.GetRMS()
VARu2 = RMSu2**2
canv.cd(4)
histogram_of_u10.Draw()
canv.cd(5)
histogram_of_un.Draw()
MEANun = histogram_of_un.GetMean()
RMSun = histogram_of_un.GetRMS()
VARun = RMSun**2

canv.Modified()
canv.Update()


print ("MEANx1 = %.2f\nMEANx2 = %.2f\nMEANu2 = %.2f\nMEANun = %.2f\n"%( MEANx1, MEANx2, MEANu2, MEANun))
print ("VARx1 = %.2f\nVARx2 = %.2f\nVARu2 = %.2f\nVARun = %f\n"%( VARx1, VARx2, VARu2, VARun))



