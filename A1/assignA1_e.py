# author : Aart Heijboer
# 
# root1-example.py
# Example script for reading a data-file, and filling and plotting
# a ROOT histogram.
#
# run with python -i example1.py to see the output 

import ROOT             # This will make root available in your script
from math import *      # Use math functions (cos, sin, etc) 

 

# -----------------------------
#  make root look a bit better
# -----------------------------
ROOT.gStyle.SetOptStat(0)           # Do not show statistics box 
ROOT.gStyle.SetPadLeftMargin(0.14)  # make room for y-title, adjust with pad.SetLeftMargin()
ROOT.gStyle.SetTitleOffset(1.8,"y") # adjust with histogram.GetYaxis().SetTitleOffset)




# We start by making a ROOT canvas, which is a placeholder for plots
# and other graphics. This is on object of type TCanvas 
# (https://root.cern.ch/root/html/TCanvas.html). The following
# makes a canvas of 800x800 pixels.
# We want to make multiple plots in the canvas. So we divide the
# canvas into 4 sub-canvasses.

canv = ROOT.TCanvas("canv","plots for SDA course - ROOT 1", 800,800 )

#canv.Divide(2,2)  # See link above for documentation of the Divide method.
#canv.cd(3)        # Switch to the first sub-canvas.


# Now, we make our first histogram, to hold the value of the Pt
# of the first muon. The ROOT class TH1D represents histograms.
#canv.cd(3)
histogram_of_Minv = ROOT.TH1D("histogram_of_Minv","histogram of invariant mass", # name and title
                             100, 0,7000 )  # 100 bins between 0 and 3000 GeV


# We are ready to open the datafile and loop over the lines/event 
# (remember each line is an event). 

input_file = open("/data/stu21q3/datasets/dimuon-dataset.txt")       # open the file

line_counter = 0

for line in input_file :   # loop over every line in the input file

    # print the first 10 lines (always good to look at what your are doing)
    
    line_counter += 1
    if line_counter < 10 : print (" line " , line.strip()) # strip away newline 

    # skip any comment lines which start with '#'

    if line.startswith("#") : continue  

    # convert the line into a list of floating point numbers 
    # and passing those numbers to pt1, theta1, etc.
    # (this uses a python list comprehension - don't worry about
    #  it for the moment if this is cryptic ).

    pt1, theta1, phi1, pt2, theta2, phi2 = [ float(x) for x in line.split() ]
    
    # look at what we are doing:

    if line_counter < 10 : print (" data = " , pt1, theta1, phi1, pt2, theta2, phi2 )

    # Fill our histogram!
    px1 = pt1 * sin(phi1)
    py1 = pt1 * cos(phi1)
    pz1 = pt1*cos(theta1)/sin(theta1)
    E1 = 0.105*0.105 + pt1/sin(theta1)

    px2 = pt2 * sin(phi2)
    py2 = pt2 * cos(phi2)
    pz2 = pt2*cos(theta2)/sin(theta2)
    E2 = 0.105*0.105 + pt2/sin(theta2)

    Minv = sqrt( (E1+E2)**2 - (px1+px2)**2 - (py1+py2)**2 - (pz1+pz2)**2)
    histogram_of_Minv.Fill( Minv )

    
    # print some progress indicator

    if line_counter % 1000 ==0 : print ("processed", line_counter," events.")
    

    # while we are develloping, do only 5000 entries (remember to remove this!!)
    
    #if line_counter > 5000 : break

    
# Done with the event loop!

# Prepare the histogram for plotting

histogram_of_Minv.SetLineWidth(2)   # nice thick line
histogram_of_Minv.SetFillColor(5)   # yellow fill color
histogram_of_Minv.SetXTitle("invariant mass (GeV)")
histogram_of_Minv.SetYTitle("events per bin")

# switch to the first sub-canvas
canv.cd(1)
histogram_of_Minv.Draw()

# Save the canvas to a jpg file. You may choose other extensions such as png or pdf if you wish a different format.

canv.SaveAs("assign_e.png")


