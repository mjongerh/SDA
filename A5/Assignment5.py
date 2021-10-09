import ROOT
import numpy
from array import array
from math import *

infile = ROOT.TFile('assignment5-dataset.root')
hData = infile.Get('hdata')
hData.Draw()
