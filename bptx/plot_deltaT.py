#! /usr/bin/python

import sys
sys.argv.append( '-b' )

import csv
from  ROOT import *
from datetime import datetime

import fill_class as f

c = f.LHCFills(2318)

path = "/home/andreypz/Dropbox/BPTXmon_data/"
file_atl = "timber_deltaT_atlas_"+str(c.Fill())+".csv"
file_cms = "timber_deltaT_cms_"+str(c.Fill())+".csv"


print c.Fill(), c.Title()
c.Begin().Print()
print c.Begin().GetDay()
fill = c.Fill()
plotTitle = ';'

beginTime  = c.Begin()
stableTime = c.Stable()
endTime    = c.End()
plotTitle  = c.Title()



reader_atl = csv.reader(open(file_atl, 'rb'))
reader_cms = csv.reader(open(file_cms, 'rb'))
gr_atl = TGraph();
gr_cms = TGraph();

i=0
for row in reader_atl:
    myDateTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
    dt = TDatime(int(myDateTime.year), int(myDateTime.month), int(myDateTime.day), int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    gr_atl.SetPoint(i,ddd, float(row[1]))
    i+=1

    
i=0
for row in reader_cms:
    myDateTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
    dt = TDatime(int(myDateTime.year), int(myDateTime.month), int(myDateTime.day), int(myDateTime.hour), int(myDateTime.minute), int(myDateTime.second))
    daTime = dt.Convert()
    ddd = float(dt.Convert()-beginTime.Convert())
    gr_cms.SetPoint(i,ddd, float(row[1]))
    i+=1


chain = TChain("timeTree");
chain.Add("root/bptx_mon_timing_2011_11_23_UTC.root")
chain.Add("root/bptx_mon_timing_2011_11_24_UTC.root")
chain.Add("root/bptx_mon_timing_2011_12_03_UTC.root")
chain.Add("root/bptx_mon_timing_2011_12_04_UTC.root")

begin = str(beginTime.Convert())
end   = str(endTime.Convert())

gROOT.ProcessLine(".L     /home/andreypz/Documents/0work/tdrstyle.C")
setTDRStyle()
gStyle.SetTimeOffset(beginTime.Convert());
gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");

gStyle.SetTimeOffset(beginTime.Convert());
duration = endTime.Convert() - beginTime.Convert()

chain.Draw('bb_phase_mean:daTime-'+begin, 'daTime>'+ begin + '&& daTime<'+end)
gr1= TGraph(gPad.GetPrimitive("Graph"))
gr1.GetXaxis().SetTimeDisplay(1);

gr1.GetXaxis().SetTimeFormat("%H:%M");
gr1.SetMarkerStyle(24);
gr1.SetMarkerSize(0.2);
gr1.SetMarkerColor(kBlue+2);
gr1.SetFillColor(kBlue+2);
gr1.SetMinimum(-0.2);
gr1.SetMaximum(0.4);
gr1.GetXaxis().SetRangeUser(0, duration)


#gr1.GetXaxis().SetLabelSize(0.03);
#gr_cms.GetXaxis().SetLabelOffset(0.02);

#gr_cms.GetXaxis().SetRangeUser(0, duration)

gr_cms.SetMarkerStyle(20);
gr_cms.SetMarkerSize(0.2);
gr_cms.SetMarkerColor(kRed+3);
gr_cms.SetFillColor(kRed+3);

gr_atl.SetMarkerStyle(21);
gr_atl.SetMarkerSize(0.2);
gr_atl.SetMarkerColor(kGreen+2);
gr_atl.SetFillColor(kGreen+2);

gr1.SetMarkerStyle(24);
gr1.SetMarkerSize(0.2);
gr1.SetMarkerColor(kBlue-1);
gr1.SetFillColor(kBlue-1);


gr1.Draw("AP*")
gr_cms.Draw("P same")
gr_atl.Draw("P same")

leg = TLegend(0.60,0.72,0.85,0.83)
leg.AddEntry(gr1,"CMS bptx_mon", "f")
leg.AddEntry(gr_cms,"CMS from timber", "f")
leg.AddEntry(gr_atl,"Atlas from timber", "f")
leg.SetFillColor(kWhite)
leg.Draw()
                        
gr1.SetTitle(plotTitle+"UTC time; deltaT, ns")

c1.SaveAs("./deltaT/timber_deltaT_fill_"+str(fill)+".png")
