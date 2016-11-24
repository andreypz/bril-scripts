#! /usr/bin/python

from  ROOT import *
gROOT.SetBatch()

path = '/afs/cern.ch/user/a/andrey/'
#path = "/scratch/bptx_data_2016/"
#path = 'root://eoscms//eos/cms/store/group/dpg_bril/comm_bril/bptx/bptx_data_2016/'

fill = '5423'

chain = TChain("bunchTree");
chain.Add(path+"bptx_mon_bunches_2016_10_22_UTC.root")
chain.Add(path+"bptx_mon_bunches_2016_10_25_UTC.root")

gROOT.ProcessLine(".L ~/tdrstyle.C")
setTDRStyle()

# These are for studies in FILL 5423:
T1 = TDatime(2016,10,18,12,40,00)
T2 = TDatime(2016,10,18,12,42,00)
T3 = TDatime(2016,10,18,16,30,00)
T4 = TDatime(2016,10,18,16,32,00)
t1 = str(T1.Convert())
t2 = str(T2.Convert())
t3 = str(T3.Convert())
t4 = str(T4.Convert())



constOffset = 6606.6 # It's in nanosecs
ORB = 88924.796
BXlength = ORB/3564
#BXlength = 24.95084

formula1 = '(1e12*b1_time_zc - 1e3*(%.2f  +  (b1_bunches-1)*%.6f ) +   30 ):b1_bunches' % (constOffset, BXlength)
formula2 = '(1e12*b2_time_zc - 1e3*(%.2f  +  (b2_bunches-1)*%.6f ) + 2600 ):b2_bunches' % (constOffset, BXlength)

chain.Draw(formula1, 'daTime>'+ t1 + '&& daTime<'+t2)
g1 = TGraph(gPad.GetPrimitive("Graph"))
chain.Draw(formula2, 'daTime>'+ t1 + '&& daTime<'+t2)
g2 = TGraph(gPad.GetPrimitive("Graph"))
formula1 = '(1e12*b1_time_zc - 1e3*(%.2f  +  (b1_bunches-1)*%.6f ) +   60 ):b1_bunches' % (constOffset, BXlength)
formula2 = '(1e12*b2_time_zc - 1e3*(%.2f  +  (b2_bunches-1)*%.6f ) + 2640 ):b2_bunches' % (constOffset, BXlength)

chain.Draw(formula1, 'daTime>'+ t3 + '&& daTime<'+t4)
g3 = TGraph(gPad.GetPrimitive("Graph"))
chain.Draw(formula2, 'daTime>'+ t3 + '&& daTime<'+t4)
g4 = TGraph(gPad.GetPrimitive("Graph"))

print formula1
print formula2

g1.SetMarkerColor(kBlue)
g2.SetMarkerColor(kRed)
g3.SetMarkerColor(kBlue+2)
g4.SetMarkerColor(kRed+2)
g1.SetFillColor(kBlue)
g2.SetFillColor(kRed)
g3.SetFillColor(kBlue+2)
g4.SetFillColor(kRed+2)

g1.SetMarkerStyle(6)
g2.SetMarkerStyle(6)
g3.SetMarkerStyle(6)
g4.SetMarkerStyle(6)

g1.Draw('AP')
g2.Draw('P same')
g3.Draw('P same')
g4.Draw('P same')

g1.SetMinimum(-90)
g1.SetMaximum(80)
g1.SetTitle('FILL '+fill+';BX number;Phase offset, ps')

leg = TLegend(0.60,0.73,0.85,0.90)
leg.AddEntry(g1,"B1 @12:40 UTC", "f")
leg.AddEntry(g2,"B2 @12:40 UTC", "f")
leg.AddEntry(g3,"B1 @16:30 UTC", "f")
leg.AddEntry(g4,"B2 @16:30 UTC", "f")
leg.SetFillColor(kWhite)
leg.Draw()

lat = TLatex()
lat.SetNDC()
lat.SetTextSize(0.07)
lat.DrawLatex(0.20,0.85, 'CMS BPTX')

c1.SaveAs('./bunches/fill_'+fill+'/'+'_'.join(['fill',fill,'LHCRF','bptxmon.png']))
