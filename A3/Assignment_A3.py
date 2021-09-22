import ROOT             # This will make root available in your script
from math import *      # Use math functions (cos, sin, etc) 


# -----------------------------
#  make root look a bit better
# -----------------------------
ROOT.gStyle.SetOptStat(0)           # Do not show statistics box 
ROOT.gStyle.SetPadLeftMargin(0.14)  # make room for y-title, adjust with pad.SetLeftMargin()
ROOT.gStyle.SetTitleOffset(1.8,"y") # adjust with histogram.GetYaxis().SetTitleOffset)

Nval = 1000
class FunctionsForMe :
    def RanCauchy(mean = 0.0, sigma = 1.0):
        return (ROOT.gRandom.Gaus(mean,sigma)/ROOT.gRandom.Gaus(mean,sigma))

def GenNumbers(func, mean = 0.0, sigma =1.0) :
    canv = ROOT.TCanvas("canv","Dummy Title", 2400,2400 ) #Create a canvas for the art to be shown
    canv.Divide(3,2)

    histogram_of_x1 = ROOT.TH1D("histogram_of_x1","histogram of x1",100, 100, 10 )
    histogram_of_x2 = ROOT.TH1D("histogram_of_x2","histogram of x2",100, 100, 10 )
    histogram_of_u2 = ROOT.TH1D("histogram_of_u2","histogram of u2",100, 100, 10 )
    histogram_of_un = ROOT.TH1D("histogram_of_un","histogram of un",100, 100, 10 )
    histogram_of_u1 = ROOT.TH1D("histogram_of_u1","histogram of u1",100, 100, 10 )
    histogram_of_u10 = ROOT.TH1D("histogram_of_u10","histogram of u10",100, 100, 10 )

    if (func == 'Cauchy'):                              #Determine function for random numbers
        RanFunc = getattr(FunctionsForMe, 'RanCauchy')
    else :
        RanFunc = getattr(ROOT.gRandom, func)

    for i in range (5000) :
        x1 = 0
        Xsum = 0
        for j in range(Nval) :
            if (func == 'Rndm'):    #Pick correct way of feeding the input values
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
    canv.cd(1)        # Showing the resulting histograms and extracting relevant values
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
    MEANu10 = histogram_of_u10.GetMean()
    RMSu10 = histogram_of_u10.GetRMS()
    VARu10 = RMSu10**2
    canv.cd(5)
    histogram_of_un.Draw()
    MEANun = histogram_of_un.GetMean()
    RMSun = histogram_of_un.GetRMS()
    VARun = RMSun**2

    canv.Modified()
    canv.Update()
    title = "Graphs for distribution: " + func
    canv.SetTitle(title)
    canv.SaveAs(func+".png") #save histograms for the viewing party later on

    print ("For function: " + func + " the values are:")
    print ("MEANx1 = %.5f\nMEANx2 = %.5f\nMEANu2 = %.5f\nMEANu10 = %.5f\nMEANun = %.5f\n"%( MEANx1, MEANx2, MEANu2,MEANu10, MEANun))
    print ("RMSx1 = %.5f\nRMSx2 = %.5f\nRMSu2 = %.5f\nRMSu10 = %.5f\nRMSun = %.5f\n"%( RMSx1, RMSx2, RMSu2,RMSu10, RMSun))
    print ("VARx1 = %.5f\nVARx2 = %.5f\nVARu2 = %.5f\nVARu10 = %.5f\nVARun = %f\n"%( VARx1, VARx2, VARu2,VARu10, VARun))

GenNumbers('Rndm')  # 'Rndm'; 'Exp'; 'Gaus',mean,sigma; 'Cauchy',mean,sigma (of the underlying gaus distos)
GenNumbers('Exp')
GenNumbers('Gaus', 0.5, 0.1)
GenNumbers('Cauchy', 0.5, 0.1)


