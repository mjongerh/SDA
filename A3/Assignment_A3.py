import ROOT             # This will make root available in your script
from math import *      # Use math functions (cos, sin, etc) 


# -----------------------------
#  make root look a bit better
# -----------------------------
ROOT.gStyle.SetOptStat(0)           # Do not show statistics box 
ROOT.gStyle.SetPadLeftMargin(0.14)  # make room for y-title, adjust with pad.SetLeftMargin()
ROOT.gStyle.SetTitleOffset(1.8,"y") # adjust with histogram.GetYaxis().SetTitleOffset)

canv = ROOT.TCanvas("canv","plots for SDA course - ROOT 1", 2400,2400 )

canv.Divide(2,2)  # See link above for documentation of the Divide method.
canv.cd(1)        # Switch to the first sub-canvas.

histogram_of_x1 = ROOT.TH1D("histogram_of_x1","histogram of x1",100, 0, 1 ) # name and title  # 100 bins between 0 and 7000 GeV, since it is now the sum, the range has to be increased beyond 3TeV
histogram_of_x2 = ROOT.TH1D("histogram_of_x2","histogram of x2",100, 0, 1 )
histogram_of_u2 = ROOT.TH1D("histogram_of_u2","histogram of u2",100, 0, 1 )
histogram_of_un = ROOT.TH1D("histogram_of_un","histogram of un",100, 0, 1 )
Nval = 2
for i in range (5000) :
    x1 = ROOT.gRandom.Rndm()
    x2 = ROOT.gRandom.Rndm()
    u2 = (x1+x2)/2
    histogram_of_x1.Fill(x1)
    histogram_of_x2.Fill(x2)
    histogram_of_u2.Fill(u2)
    Xsum = 0
    for j in range(Nval) :
        Xsum += ROOT.gRandom.Rndm()
    Xsum /= Nval
    histogram_of_un.Fill(Xsum)


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
histogram_of_un.Draw()
MEANun = histogram_of_un.GetMean()
RMSun = histogram_of_un.GetRMS()
VARun = RMSun**2

print ("MEANx1 = %.2f\nMEANx2 = %.2f\nMEANu2 = %.2f\nMEANun = %.2f\n"%( MEANx1, MEANx2, MEANu2, MEANun))
print ("VARx1 = %.2f\nVARx2 = %.2f\nVARu2 = %.2f\nVARun = %.2f\n"%( VARx1, VARx2, VARu2, VARun))



