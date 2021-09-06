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

#canv = ROOT.TCanvas("canv","plots for SDA course - ROOT 1", 800,800 )

#canv.Divide(2,2)  # See link above for documentation of the Divide method.
#canv.cd(1)        # Switch to the first sub-canvas.



# We are ready to open the datafile and loop over the lines/event 
# (remember each line is an event). 

input_file = open("/data/stu21q3/datasets/dimuon-dataset.txt")       # open the file

line_counter = 0 #also functions as total number of events

Pt1_high_1TeV = 0 #counter of Pt1 > 1Tev
Pt2_high_1TeV = 0
any_high_1TeV = 0
both_high_1TeV = 0

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

    #histogram_of_pt1_and_pt2.Fill( pt1,pt2 )
    if pt1 > 1000 : Pt1_high_1TeV += 1
    if pt2 > 1000 : Pt2_high_1TeV += 1
    if pt1 > 1000 or pt2 > 1000 : any_high_1TeV += 1
    if pt1 > 1000 and pt2 > 1000 : both_high_1TeV += 1

    # print some progress indicator

    if line_counter % 1000 ==0 : print ("processed", line_counter," events.")
    

    # while we are develloping, do only 5000 entries (remember to remove this!!)
    
    #if line_counter > 5000 : break

    
# Done with the event loop!
print ("Probability of event Pt1 > 1TeV = " + str(Pt1_high_1TeV/line_counter))
print ("Probability of event Pt2 > 1TeV = " + str(Pt2_high_1TeV/line_counter))
print ("Probability of event with pt1 or Pt2 > 1Tev " + str(any_high_1TeV/line_counter))

#assignment d
print ("Probability of event Pt1 > 1TeV AND Pt2 > 1TeV= " + str(both_high_1TeV/line_counter))
print ("Probability of event Pt2 > 1TeV given Pt1 > 1TeV = " + str(both_high_1TeV/Pt1_high_1TeV)) 

#comparison with equations and results from c
print ("From equations and results from c:")
# P(pt1>1TeV and pt2>1TeV) = P(pt1>1TeV) + P(pt2>1TeV) - P(pt1>1TeV or pt2>1TeV)
P_pt1_and_pt2 = Pt1_high_1TeV/line_counter + Pt2_high_1TeV/line_counter - any_high_1TeV/line_counter
print ("Probability of event Pt1 > 1TeV AND Pt2 > 1TeV= " + str(P_pt1_and_pt2))
# P(pt2>1TeV | pt1>1TeV) = P(pt1>1TeV | pt2>1TeV) * P(pt2>1TeV) / P(pt1>1TeV)
P_pt2_lt1TeV_given_pt1_lt1TeV = (both_high_1TeV/Pt2_high_1TeV) * Pt2_high_1TeV / Pt1_high_1TeV
print ("Probability of event Pt2 > 1TeV given Pt1 > 1TeV= " + str(P_pt2_lt1TeV_given_pt1_lt1TeV))




