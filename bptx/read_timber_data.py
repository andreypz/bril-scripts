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
    dt = TDatime(int(myDateTime.year), int(myDateTime.month), int(myDateTime.day),
                 int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    for bx in bxs:
      gr.SetPoint(i,ddd, float(row[1]))
    i+=1

  return gr
  #gr.Draw("AP*")
  #c1.SaveAs("./fbct/fbct_fill_"+str(fill)+".png")


def readTIMBER_TOT_INT(fill, source="ATLAS", datatype='B1_INT_MEAN', ):
  # source = ATLAS, BCTDC.A6R4, BCTFR.A6R4
  # datatype = B1 or2 _INT_ MEAN or SUM (this is hardcoded in the names of the .csv files)
  file_data = "../DATA/TIMBER-FILL-"+str(fill)+"/TIMBER_"+source+"."+datatype+".csv"

  print " ... reading TIMBER data file", file_data

  c = f.LHCFills(fill)
  beginTime  = c.Begin()

  gr = TGraph()
  try:
    reader = csv.reader(open(file_data, 'rb'))
  except IOError:
    return gr

  skiplines = 10
  i=0
  for row in reader:
    i+=1
    if i<=skiplines: continue

    try:
      myDateTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
      print i, 'Bad format:',row[0]
      print 'But we will continue'
      continue
      #exit(0)
      
    dt = TDatime(int(myDateTime.year), int(myDateTime.month), int(myDateTime.day),
                 int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    # print i, row[0], row[1]

    #if source==''
    gr.SetPoint(i-skiplines,ddd, 1E-11*float(row[1]))

  return gr





def readTIMBER_BX_INT(fill, BX='1', source="ATLAS", datatype='B1_INT_MEAN', ):
  # source and datatype: see comment for readTIMBER_TOT_INT()
  if fill==0: fill=4381
  file_data = "../DATA/TIMBER-FILL-"+str(fill)+"/TIMBER_"+source+"."+datatype+".csv"

  print " ... reading TIMBER data file", file_data

  c = f.LHCFills(fill)
  beginTime  = c.Begin()

  gr = TGraph()
  try:
    reader = csv.reader(open(file_data, 'rb'))
  except IOError:
    return gr

  scale = 1E-11
  if 'LEN' in file_data: scale = 1 
  skiplines = 10
  i=0
  for row in reader:
    i+=1
    if i<=skiplines: continue
    # if i<20: print len(row)

    try:
      myDateTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
    except IndexError:
      print 'Index Error in ', row
      print 'But will continue'
      continue
    dt = TDatime(int(myDateTime.year), int(myDateTime.month),  int(myDateTime.day),
                 int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    # print i, BX, row[0], row[int(BX)]

    # gr.SetPoint(i-6,ddd, float(1))
    gr.SetPoint(i-skiplines,ddd, scale*float(row[int(BX)]))

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
