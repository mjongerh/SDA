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

canv = ROOT.TCanvas("canv","plots for SDA course - ROOT 1", 2400,2400 )

canv.Divide(2,2)  # See link above for documentation of the Divide method.
canv.cd(1)        # Switch to the first sub-canvas.

histogram_of_pt1 = ROOT.TH1D("histogram_of_pt1_pt2","histogram of Pt1 + Pt2",100, 0,7000 ) # name and title  # 100 bins between 0 and 7000 GeV, since it is now the sum, the range has to be increased beyond 3TeV

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
    histogram_of_pt1.Fill( pt1+pt2 )

    # print some progress indicator
    if line_counter % 1000 ==0 : print ("processed", line_counter," events.")

# Done with the event loop!

# Prepare the histogram for plotting

histogram_of_pt1.SetLineWidth(2)   # nice thick line
histogram_of_pt1.SetFillColor(5)   # yellow fill color
histogram_of_pt1.SetXTitle("tranverse momentum of #mu_{1}+#mu_{2} (GeV)")
histogram_of_pt1.SetYTitle("events per bin")

# switch to the first sub-canvas
canv.cd(1)
histogram_of_pt1.Draw()


# Assignment b
histogram_of_pt1_and_pt2 = ROOT.TH2D("histogram_of_pt1_and_pt2","histogram of Pt1 and Pt2", # 2D histogram to show correlation between pt1 and pt2
                             100, 0,4000, 100, 0, 4000 )  # 100 bins between 0 and 4000 GeV

line_counter = 0
input_file.seek(0) #go back to the start of the file
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
    # Fill our histogram with the values of Pt
    histogram_of_pt1_and_pt2.Fill( pt1,pt2 )
    # print some progress indicator
    if line_counter % 1000 ==0 : print ("processed", line_counter," events.")

# Done with the event loop!

# Prepare the histogram for plotting

histogram_of_pt1_and_pt2.SetLineWidth(2)   # nice thick line
histogram_of_pt1_and_pt2.SetFillColor(5)   # yellow fill color
histogram_of_pt1_and_pt2.SetXTitle("tranverse momentum of #mu_{1}+#mu_{2} (GeV)")
histogram_of_pt1_and_pt2.SetYTitle("events per bin")

# switch to the first sub-canvas
canv.cd(2)
histogram_of_pt1_and_pt2.Draw("colz")

# Assignment c&d
line_counterc = 0 #also functions as total number of events

Pt1_high_1TeV = 0 #counter of Pt1 > 1TeV
Pt2_high_1TeV = 0 #counter of Pt2 > 1TeV
any_high_1TeV = 0 #counter of Pt1 > 1TeV OR Pt2 > 1TeV
both_high_1TeV = 0 #counter of Pt1 > 1TeV AND Pt2 > 1TeV

input_file.seek(0)
for line in input_file :   # loop over every line in the input file

    # print the first 10 lines (always good to look at what your are doing)
    
    line_counterc += 1
    if line_counter < 10 : print (" line " , line.strip()) # strip away newline 

    # skip any comment lines which start with '#'
    if line.startswith("#") : continue  
    pt1, theta1, phi1, pt2, theta2, phi2 = [ float(x) for x in line.split() ]
    
    # look at what we are doing:

    if line_counterc < 10 : print (" data = " , pt1, theta1, phi1, pt2, theta2, phi2 )

    # Keep track of statistics
    if pt1 > 1000 : Pt1_high_1TeV += 1
    if pt2 > 1000 : Pt2_high_1TeV += 1
    if pt1 > 1000 or pt2 > 1000 : any_high_1TeV += 1
    if pt1 > 1000 and pt2 > 1000 : both_high_1TeV += 1

    # print some progress indicator
    if line_counterc % 1000 ==0 : print ("processed", line_counter," events.")

# Done with the event loop!
print ("Probability of event Pt1 > 1TeV = " + str(Pt1_high_1TeV/line_counterc))
print ("Probability of event Pt2 > 1TeV = " + str(Pt2_high_1TeV/line_counterc))
print ("Probability of event with pt1 or Pt2 > 1Tev " + str(any_high_1TeV/line_counterc))

#assignment d
print ("Probability of event Pt1 > 1TeV AND Pt2 > 1TeV= " + str(both_high_1TeV/line_counterc))
print ("Probability of event Pt2 > 1TeV given Pt1 > 1TeV = " + str(both_high_1TeV/Pt1_high_1TeV)) 

#comparison with equations and results from c
print ("From equations and results from c:")
# P(pt1>1TeV and pt2>1TeV) = P(pt1>1TeV) + P(pt2>1TeV) - P(pt1>1TeV or pt2>1TeV)
P_pt1_and_pt2 = Pt1_high_1TeV/line_counterc + Pt2_high_1TeV/line_counterc - any_high_1TeV/line_counterc
print ("Probability of event Pt1 > 1TeV AND Pt2 > 1TeV= " + str(P_pt1_and_pt2))
# P(pt2>1TeV | pt1>1TeV) = P(pt1>1TeV | pt2>1TeV) * P(pt2>1TeV) / P(pt1>1TeV)
P_pt2_lt1TeV_given_pt1_lt1TeV = (both_high_1TeV/Pt2_high_1TeV) * Pt2_high_1TeV / Pt1_high_1TeV
print ("Probability of event Pt2 > 1TeV given Pt1 > 1TeV= " + str(P_pt2_lt1TeV_given_pt1_lt1TeV))

# Assignment e
canv.cd(3)
histogram_of_Minv = ROOT.TH1D("histogram_of_Minv","histogram of invariant mass", # name and title
                             100, 0,7000 )  # 100 bins between 0 and 7000 GeV
line_countere = 0
input_file.seek(0)
for line in input_file :   # loop over every line in the input file

    # print the first 10 lines (always good to look at what your are doing)
    
    line_countere += 1
    if line_countere < 10 : print (" line " , line.strip()) # strip away newline 

    # skip any comment lines which start with '#'
    if line.startswith("#") : continue  

    pt1, theta1, phi1, pt2, theta2, phi2 = [ float(x) for x in line.split() ]
    
    # look at what we are doing:
    if line_countere < 10 : print (" data = " , pt1, theta1, phi1, pt2, theta2, phi2 )

    # Calaculate relevant variables and fill them into histogram
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
    if line_countere % 1000 ==0 : print ("processed", line_countere," events.")

# Done with the event loop!

# Prepare the histogram for plotting

histogram_of_Minv.SetLineWidth(2)   # nice thick line
histogram_of_Minv.SetFillColor(5)   # yellow fill color
histogram_of_Minv.SetXTitle("invariant mass (GeV)")
histogram_of_Minv.SetYTitle("events per bin")

# switch to the first sub-canvas
canv.cd(3)
histogram_of_Minv.Draw()


# Save the canvas to a jpg file. You may choose other extensions such as png or pdf if you wish a different format.
canv.SaveAs("assign_A1.png")

