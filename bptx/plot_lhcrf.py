#! /usr/bin/python

from  ROOT import *
gROOT.SetBatch()

#path = '/home/andrey/BPTXMONDATA/'
#path = '~/work/BPTXMONDATA/root/'
#path = "/scratch/bptx_data_2016/"
#path = 'root://eoscms//eos/cms/store/group/dpg_bril/comm_bril/bptx/bptx_data_2016/'
path = '/afs/cern.ch/user/a/andrey/public/BRIL/RF_LHC_Fill_5423/data/root/'

fill = '5423'

chain = TChain("bunchTree");
#chain.Add(path+"all_bunches_2016.root")
chain.Add(path+"bptx_mon_bunches_2016_10_22_UTC.root")
#chain.Add(path+"bptx_mon_bunches_2016_10_25_UTC.root")

gROOT.ProcessLine(".L ~/tdrstyle.C")
try:
  setTDRStyle()
except NameError:
  print "No tdrstyle.. Well, skip it then."
  
# These are for studies in FILL 5423:
T1 = TDatime(2016,10,18,12,40,00)
T2 = TDatime(2016,10,18,12,42,00)
#T3 = TDatime(2016,10,18,15,30,00)
#T4 = TDatime(2016,10,18,15,32,00)
T3 = TDatime(2016,10,18,16,30,00)
T4 = TDatime(2016,10,18,16,32,00)
T3txt = '16:30'

t1 = str(T1.Convert())
t2 = str(T2.Convert())
t3 = str(T3.Convert())
t4 = str(T4.Convert())


lim = [-140, 140]
constOffset = 6606.6 # It's in nanosecs
ORB = 88924.796
BXlength = ORB/3564
#BXlength = 24.95084

formula1 = '(1e12*b1_time_zc - 1e3*(%.2f  +  (b1_bunches-1)*%.6f ) +   40 ):b1_bunches' % (constOffset, BXlength)
formula2 = '(1e12*b2_time_zc - 1e3*(%.2f  +  (b2_bunches-1)*%.6f ) + 2600 ):b2_bunches' % (constOffset, BXlength)
#formula1 = '(1e12*b1_time_zc - 1e3*(%.2f  +  (b1_bunches-1)*%.6f ) +   20 ):b1_bunches' % (constOffset, BXlength)
#formula2 = '(1e12*b2_time_zc - 1e3*(%.2f  +  (b2_bunches-1)*%.6f ) + 2600 ):b2_bunches' % (constOffset, BXlength)

chain.Draw(formula1, 'daTime>'+ t1 + '&& daTime<'+t2)
g1 = TGraph(gPad.GetPrimitive("Graph"))
chain.Draw(formula2, 'daTime>'+ t1 + '&& daTime<'+t2)
g2 = TGraph(gPad.GetPrimitive("Graph"))
formula1 = '(1e12*b1_time_zc - 1e3*(%.2f  +  (b1_bunches-1)*%.6f ) +   40 ):b1_bunches' % (constOffset, BXlength)
formula2 = '(1e12*b2_time_zc - 1e3*(%.2f  +  (b2_bunches-1)*%.6f ) + 2600 ):b2_bunches' % (constOffset, BXlength)
#formula1 = '(1e12*b1_time_zc - 1e3*(%.2f  +  (b1_bunches-1)*%.6f ) +   60 ):b1_bunches' % (constOffset, BXlength)
#formula2 = '(1e12*b2_time_zc - 1e3*(%.2f  +  (b2_bunches-1)*%.6f ) + 2640 ):b2_bunches' % (constOffset, BXlength)

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

g1.SetMinimum(lim[0])
g1.SetMaximum(lim[1])
g1.SetTitle('FILL '+fill+';BX number;Phase offset, ps')

leg = TLegend(0.60,0.73,0.85,0.90)
leg.AddEntry(g1,"B1 @12:40 UTC", "f")
leg.AddEntry(g2,"B2 @12:40 UTC", "f")
leg.AddEntry(g3,"B1 @"+T3txt+" UTC", "f")
leg.AddEntry(g4,"B2 @"+T3txt+" UTC", "f")
leg.SetFillColor(kWhite)
leg.Draw()

lat = TLatex()
lat.SetNDC()
lat.SetTextSize(0.07)
lat.DrawLatex(0.20,0.85, 'CMS BPTX')

c1.SaveAs('./bunches/fill_'+fill+'/'+'_'.join(['fill',fill,'LHCRF','bptxmon.png']))


limOrb = [-0.1, 0.1]

#gStyle.SetTimeOffset(T1.Convert());
gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");
begin  = str(T1.Convert())
stable = str(T1.Convert())
end    = str(T4.Convert())
duration = T4.Convert() - T1.Convert()

formula1 = '(1e9*orb_len_1    - %.5f):daTime'%(ORB)
formula2 = '(1e9*( orb_len_trig) - %.5f):daTime'%(ORB)

chain.Draw(formula1, 'daTime>'+ t1 + '&& daTime<'+t4)
g1 = TGraph(gPad.GetPrimitive("Graph"))
#chain.Draw(formula2, 'daTime>'+ t1 + '&& daTime<'+t4)
#g2 = TGraph(gPad.GetPrimitive("Graph"))

g1.Draw('APL')
#g2.Draw('P same')

g1.SetMinimum(limOrb[0])
g1.SetMaximum(limOrb[1])
g1.GetXaxis().SetTimeDisplay(1)
g1.GetXaxis().SetTimeFormat("%H:%M")
g1.GetXaxis().SetRangeUser(0, duration)

g1.SetTitle('FILL '+fill+';UTC time;Orbit Length - Shift, ns')

c1.SaveAs('./bunches/fill_'+fill+'/'+'_'.join(['fill',fill,'Orbit_Length','.png']))
