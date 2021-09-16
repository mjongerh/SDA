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

for i in range (2000) :
    x1 = ROOT.gRandom.Rndm()
    x2 = ROOT.gRandom.Rndm()
    u2 = (x1+x2)/2
    histogram_of_x1.Fill(x1)
    histogram_of_x2.Fill(x2)
    histogram_of_u2.Fill(u2)

histogram_of_x1.Draw()
canv.cd(2)
histogram_of_x2.Draw()
canv.cd(3)
histogram_of_u2.Draw()


