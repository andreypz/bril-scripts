#! /usr/bin/python

import sys,os
import csv
from  ROOT import *
gROOT.SetBatch()

from datetime import datetime
import fill_class as f

def createDir(myDir):
  if not os.path.exists(myDir):
    try: os.makedirs(myDir)
    except OSError:
      if os.path.isdir(myDir): pass
      else:
        print myDir, 'already exists'


        
def readFBCT(file_fbct, fill):
  c = f.LHCFills(fill)
  
  beginTime  = c.Begin()
  stableTime = c.Stable()
  endTime    = c.End()
  plotTitle  = c.Title()

  fbct = []
  gr = TGraph()
  reader = csv.reader(open(file_fbct, 'rb'))

  bxs = [1,2,3,4]
  i=0
  for row in reader:
    myDateTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
    dt = TDatime(int(myDateTime.year), int(myDateTime.month), int(myDateTime.day), int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    for bx in bxs:
      gr.SetPoint(i,ddd, float(row[1]))
    i+=1

  return gr
  #gr.Draw("AP*")
  #c1.SaveAs("./fbct/fbct_fill_"+str(fill)+".png")

  


def readTIMBER_TOT_INT(fill, source="ATLAS", datatype='B1_INT_MEAN', ):
  # datatype = B1 or2 _INT_ MEAN or SUM
  # source = ATLAS, BCTDC.A6R4, BCTFR.A6R4

  file_data = "../DATA/TIMBER-FILL-"+str(fill)+"/TIMBER_"+source+"."+datatype+".csv"
  
  print " ... reading TIMBER data file", file_data 

  c = f.LHCFills(fill)
  beginTime  = c.Begin()

  gr = TGraph()
  reader = csv.reader(open(file_data, 'rb'))
  i=0
  
  for row in reader:
    i+=1
    if i<=3: continue
    myDateTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
    dt = TDatime(int(myDateTime.year), int(myDateTime.month), int(myDateTime.day),
                 int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    # print i, row[0], row[1]

    #if source==''
    gr.SetPoint(i-4,ddd, 1E-11*float(row[1]))

  return gr

if __name__ == "__main__":
  
  gROOT.ProcessLine(".L ~/tdrstyle.C")
  setTDRStyle()


  myFILL = 4381
  outDir = './timber-plots/fill_'+str(myFILL)
  createDir(outDir)

  c = f.LHCFills(myFILL)
  beginTime  = c.Begin()
  endTime     = c.End()
  print c.Fill(), c.Title()
  c.Begin().Print()
  print c.Begin().GetDay()
  plotTitle = ';'
  
  gStyle.SetTimeOffset(beginTime.Convert());
  duration = endTime.Convert() - beginTime.Convert()


  # file_fbct = "timber_FBCT_"+str(c.Fill())+".csv"
  #readFBCT(file_fbct)
  atl = readATLASint(4381)
 
    
  atl.GetXaxis().SetTimeDisplay(1);
  atl.GetXaxis().SetTimeFormat("%H:%M");
  atl.GetXaxis().SetLabelSize(0.03);
  atl.GetXaxis().SetLabelOffset(0.02);
  atl.GetXaxis().SetRangeUser(0, duration)
  atl.Draw("AP*")
  c1.SaveAs("./timber-plots/fill_"+str(myFILL)+"/ATL-INT-MEAN_fill_"+str(myFILL)+".png")

  
  '''
  gr[1].SetMarkerStyle(24);
  gr[1].SetMarkerSize(0.2);
  gr[1].SetMarkerColor(kRed+3);
  gr[1].SetFillColor(kRed+3);
  
  gr[1].Draw("AP*")
  leg = TLegend(0.60,0.72,0.85,0.83)
  leg.AddEntry(gr[1],"CMS (from timber)", "f")
  leg.AddEntry(gr_atl,"Atlas (from timber)", "f")
  #leg.SetFillColor(kWhite)
  leg.Draw()
  
  gr[1].SetTitle(plotTitle+"UTC time; deltaT, ns")
  
  c1.SaveAs("./fbct/fbct_fill_"+str(fill)+".png")
  
  '''
