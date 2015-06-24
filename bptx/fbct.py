#! /usr/bin/python

import sys
sys.argv.append( '-b' )

import csv
from  ROOT import *
from datetime import datetime

import fill_class as f

c = f.LHCFills(2344)

file_fbct = "timber_FBCT_"+str(c.Fill())+".csv"

print c.Fill(), c.Title()
c.Begin().Print()
print c.Begin().GetDay()
fill = c.Fill()
plotTitle = ';'

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


gROOT.ProcessLine(".L     /home/andreypz/Documents/0work/tdrstyle.C")
setTDRStyle()
gStyle.SetTimeOffset(beginTime.Convert());

gStyle.SetTimeOffset(beginTime.Convert());
duration = endTime.Convert() - beginTime.Convert()

#gr[1].SetMinimum(-0.2);
#gr[1].SetMaximum(0.1);

gr[1].GetXaxis().SetTimeDisplay(1);
gr[1].GetXaxis().SetTimeFormat("%H:%M");
gr[1].GetXaxis().SetLabelSize(0.03);
gr[1].GetXaxis().SetLabelOffset(0.02);

gr[1].GetXaxis().SetRangeUser(0, duration)

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

