#! /usr/bin/python

import sys,os
from  ROOT import *
import fill_class as f
gROOT.SetBatch()


from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options ] fillNumber")
parser.add_option("-s", "--drawSB", dest="drawSB", action="store_true", default=False, help="Draw a line for Stable Beams start")


(options, args) = parser.parse_args()
if len(args) < 1:
  parser.print_usage()
  exit(1)

drawSB = options.drawSB

fillNumber = args[0]

if fillNumber == "0":
  #c = f.LHCFills(0, TDatime(2015,7,14,4,10,00), None, TDatime(2015,7,14,11,10,00))
  #TimeFormat ="%H:%M"
  # For the whole history plots.
  c = f.LHCFills(0, TDatime(2016,3,29,9,00,00), None, TDatime(2016,10,23,23,00,00))
  TimeFormat ="%d %b"
  #TimeFormat ="%H %M"
else:
  c = f.LHCFills(fillNumber)
  TimeFormat ="%H:%M"

fill = c.Fill()
plotTitle = ';'

beginTime  = c.Begin()
if (c.Stable()!=None):
  stableTime = c.Stable()
else:
  stableTime = c.Begin()
endTime    = c.End()
plotTitle  = c.Title()

'''
lines = [[TDatime(2012,9,10,18,18,00), "-Injection probe"],
         [TDatime(2012,9,10,20,11,00), "-Try led"],
         [TDatime(2012,9,10,20,48,00), "-p-Pb here?!"],
         [TDatime(2012,9,10,21,43,00), "-something"],
         [TDatime(2012,9,10,21,57,00), "-Dump"],
         ]

ll = []
tt = []
i=0
for l in lines:
    text = l[1]
    line_pos = l[0].Convert() - beginTime.Convert(); 
    line = TLine(line_pos,0,line_pos,20)
    line.SetLineColor(kGreen+2)
    line.SetLineWidth(2)
    ll.append(line)
    tt.append(TLatex(1.01*line_pos, 1.0+2.5*i, text))
    i+=1
'''

deltaT_lim      = [-0.05, 0.05]
deltaTsigma_lim = [0, 0.06]
beam_phase_lim  = [-0.6,0.6]
offset_lim      = [-1.4, 0.2]
gain_lim        = [0., 1.0]
scale_lim       = [0.4, 1.]
scopeGainCut = '0.01'

lim = {'bb_phase_mean':[-0.05, 0.05],
       'bb_phase_sigma':[0, 0.06],
       'phase_mean': [-0.2, 0.2],
       'phase_min':  [-0.2, 0.2],
       'phase_max':  [-0.2, 0.2]
       }


#path = "/afs/cern.ch/user/a/andrey/work/BPTXMONDATA/"
path = "/scratch/bptx_data_2016/"
chain = TChain("timeTree");
chain.Add(path+"root/all_timing_2016.root")

print chain.GetEntries()

#Create a firectory for the Fill
outDir = './timing/fill_'+str(fill)
if not os.path.exists(outDir):
  os.makedirs(outDir)
        

gROOT.ProcessLine(".L ~/tdrstyle.C")
#gROOT.ProcessLine(".L     ~/Dropbox/tdrstyle.C")
setTDRStyle()
gROOT.ForceStyle()
gStyle.SetTimeOffset(beginTime.Convert()) # A hack to go around stupid time differences
#gStyle.SetTimeOffset(beginTime.Convert()+7*3600) # A hack to go around stupid time differences

c1 = TCanvas('c1','c1', 1000, 500)

print '\t begin time:'
beginTime.Print()
print '\t end time:'
endTime.Print()


gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");
begin  = str(beginTime.Convert())
stable = str(stableTime.Convert())
end    = str(endTime.Convert())
print begin, end
duration = endTime.Convert() - beginTime.Convert()

leg = TLegend(0.80,0.8,0.95,0.9)

def vsTime(varName, plotName, yTitle):

  chain.Draw(varName+':daTime-'+begin, 'b1_gain>'+scopeGainCut+' && daTime>'+ begin + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  gr1.SetMarkerStyle(24);
  gr1.SetMarkerSize(0.2);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMinimum(lim[varName][0])
  gr1.SetMaximum(lim[varName][1])
  gr1.GetXaxis().SetRangeUser(0, duration)
  gr1.Draw("AP*")
  gr1.SetTitle(plotTitle+'UTC time;'+yTitle)
  line_pos = stableTime.Convert()-beginTime.Convert()
  line = TLine(line_pos,-0.1,line_pos,0.1)
  line.SetLineColor(kGreen+2)
  line.SetLineWidth(2)
  text = TLatex(1.01*line_pos, -0.1,"#rightarrow stable beam")
  if drawSB:
    line.Draw()
  if drawSB:
    text.Draw()
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_'+plotName+'.png')
  

def vsTime2B(varName, plotName, yTitle):
  chain.Draw('b1_'+varName+':daTime-'+begin, 'b1_gain>'+scopeGainCut+' && daTime>'+ begin + '&& daTime<'+end)
  gr01= TGraph(gPad.GetPrimitive("Graph"))
  chain.Draw('b2_'+varName+':daTime-'+begin, 'b2_gain>'+scopeGainCut+' && daTime>'+ begin + '&& daTime<'+end)
  gr02= TGraph(gPad.GetPrimitive("Graph"))
  gr01.GetXaxis().SetTimeDisplay(1);
  gr01.GetXaxis().SetTimeFormat(TimeFormat);
  
  gr01.SetMarkerStyle(25);
  gr01.SetMarkerSize(0.3);
  gr01.SetMarkerColor(kBlue+2);
  
  gr02.SetMarkerStyle(26);
  gr02.SetMarkerSize(0.3);
  gr02.SetMarkerColor(kRed+2);
  gr01.GetXaxis().SetTimeFormat(TimeFormat);
  gr01.GetXaxis().SetRangeUser(0, duration)
  
  gr01.Draw("AP")
  gr01.SetMinimum(lim[varName][0])
  gr01.SetMaximum(lim[varName][1])
  gr02.Draw("same P")
  
  leg.AddEntry(gr01,"Beam 1", "p")
  leg.AddEntry(gr02,"Beam 2", "p")
  leg.SetFillColor(kWhite)
  leg.Draw()
  
  gr01.SetTitle(plotTitle+'UTC time;'+yTitle)
  
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_'+plotName+'.png')
  


if __name__ == "__main__":
  
  vsTime('bb_phase_mean', 'deltaT', 'Delta T (B1 - B2), ns')

  vsTime('bb_phase_sigma', 'deltaT_sigma', '#sigma (#Delta T), ns')


  vsTime2B('phase_mean', 'beam_deltaT', 'Beam phase wrt BC-Main, ns')

  vsTime2B('phase_min', 'beam_deltaT_min', 'MIN Beam phase wrt BC-Main, ns')
  vsTime2B('phase_max', 'beam_deltaT_max', 'MAX Beam phase wrt BC-Main, ns')
  
  '''
  chain.Draw('bb_phase_sigma:daTime-'+begin, 'daTime>'+ begin + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  
  gr1.SetMarkerStyle(24);
  gr1.SetMarkerSize(0.2);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMinimum(deltaTsigma_lim[0])
  gr1.SetMaximum(deltaTsigma_lim[1])
  gr1.GetXaxis().SetRangeUser(0, duration)
  gr1.Draw("AP*")
  gr1.SetTitle(plotTitle+'UTC time; sigma of delta T, ns')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_sigma_deltaT.png')
  '''
  
  gStyle.SetOptStat(1111)
  chain.Draw('bb_phase_mean>>hh', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
  hhh=hh.DrawNormalized()
  hhh.SetTitle(plotTitle+'delta_t; normalized')
  hhh.SetLineColor(kBlue+2)
  hhh.SetMaximum(0.1)
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_deltaT_fill_hist.png')
  hh.Delete()
  
  gStyle.SetOptStat(0)
  
  '''
  for l in ll:
      l.Draw()
  for t in tt:
      t.SetTextSize(0.03)
      t.Draw()
  '''
  
  gStyle.SetOptStat(1111)
  chain.Draw('b1_phase_mean>>h1(50, '+str(beam_phase_lim[0])+','+str(beam_phase_lim[1])+')', 
             'daTime>'+ begin + '&& daTime<'+end, 'hist')
  chain.Draw('b2_phase_mean>>h2(50, '+str(beam_phase_lim[0])+','+str(beam_phase_lim[1])+')', 
             'daTime>'+ begin + '&& daTime<'+end, 'hist')
  hh1=h1.DrawNormalized()
  hh2=h2.DrawNormalized("same")
  hh1.SetMaximum(0.5)
  hh1.SetTitle(plotTitle+'phase, ns; normalized')
  hh1.SetLineColor(kBlue+2)
  hh2.SetLineColor(kRed+2)
  leg.Draw()
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_beam_phase_hist.png')
  
  
  gStyle.SetOptStat(0);
  chain.Draw('nB1:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  chain.Draw('nB2:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr2= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  gr1.SetMarkerStyle(25);
  gr1.SetMarkerSize(0.3);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMarkerColor(kRed+2);
  gr1.SetMaximum(3000)
  gr1.Draw("AP")
  gr1.Draw('same')
  leg.Draw()
  gr1.SetTitle(plotTitle+'UTC time; Number of bunches')
  '''
  for l in ll:
      l.Draw()
  for t in tt:
      t.SetTextSize(0.03)
      t.Draw()
  '''
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_nBeams.png')
  
  
  gStyle.SetOptStat(0);
  chain.Draw('b1_flag:daTime-'+begin, 'daTime>'+ begin + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  chain.Draw('b2_flag:daTime-'+begin, 'daTime>'+ begin + '&& daTime<'+end)
  gr2= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  gr1.SetMarkerStyle(25);
  gr1.SetMarkerSize(0.3);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMarkerColor(kRed+2);
  gr1.Draw("AP")
  gr2.Draw('same')
  leg.Draw()
  gr1.SetTitle(plotTitle+'UTC time; flag (0 or 1)')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_wrongBucketFlag.png')
  
  
  chain.Draw('b1_offset:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  chain.Draw('b2_offset:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr2= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  gr1.SetMarkerStyle(25);
  gr1.SetMarkerSize(0.3);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMarkerColor(kRed+2);
  gr1.Draw("AP")
  gr1.Draw('same')
  leg.Draw()
  gr1.SetMinimum(offset_lim[0])
  gr1.SetMaximum(offset_lim[1])
  gr1.SetTitle(plotTitle+'UTC time; scope offset, V')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_offset.png')
  
  chain.Draw('b1_offset>>hoffset1(50, '+str(offset_lim[0])+','+str(offset_lim[1])+')', 'daTime>'+ stable + '&& daTime<'+end)
  chain.Draw('b2_offset>>hoffset2(50, '+str(offset_lim[0])+','+str(offset_lim[1])+')', 'daTime>'+ stable + '&& daTime<'+end)
  hh1=hoffset1.DrawNormalized()
  hh2=hoffset2.DrawNormalized("same")
  hh1.SetMaximum(0.5)
  hh1.SetLineColor(kBlue+2)
  hh2.SetLineColor(kRed+2)
  leg.Draw()
  hh1.SetTitle(plotTitle+'scope offset, V; normalized')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_offset_fill_hist.png')
  
  
  
  chain.Draw('b1_gain:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  chain.Draw('b2_gain:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr2= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  gr1.SetMarkerStyle(25);
  gr1.SetMarkerSize(0.3);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMarkerColor(kRed+2);
  gr1.Draw("AP")
  gr1.Draw('same')
  leg.Draw()
  gr1.SetMinimum(gain_lim[0])
  gr1.SetMaximum(gain_lim[1])
  gr1.SetTitle(plotTitle+'UTC time; scope gain, V/div')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_gain.png')
  
  c1.Clear()
  
  gStyle.SetOptStat(1111)
  
  chain.Draw('b1_gain>>hgain1(50, '+str(gain_lim[0])+','+str(gain_lim[1])+')', 'daTime>'+ stable + '&& daTime<'+end)
  chain.Draw('b2_gain>>hgain2(50, '+str(gain_lim[0])+','+str(gain_lim[1])+')', 'daTime>'+ stable + '&& daTime<'+end)
  hh1=hgain1.DrawNormalized()
  hh2=hgain2.DrawNormalized("same")
  hh1.SetMaximum(0.5)
  hh1.SetLineColor(kBlue+2)
  hh2.SetLineColor(kRed+2)
  leg.Draw()
  hh1.SetTitle(plotTitle+'scope gain, V/div; normalized')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_gain_fill_hist.png')
  
  
  
  '''
  do the correlation plots
  chain.Draw('b1_gain>>hgain1(50, '+str(gain_lim[0])+','+str(gain_lim[1])+')', 'daTime>'+ stable + '&& daTime<'+end)
  chain.Draw('b2_gain>>hgain2(50, '+str(gain_lim[0])+','+str(gain_lim[1])+')', 'daTime>'+ stable + '&& daTime<'+end)
  hh1=hgain1.DrawNormalized()
  hh2=hgain2.DrawNormalized("same")
  hh1.SetMaximum(0.5)
  hh1.SetLineColor(kBlue+2)
  hh2.SetLineColor(kRed+2)
  leg.Draw()
  hh1.SetTitle(plotTitle+'scope gain, V/div; normalized')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_gain_fill_hist.png')
  '''
  
  
  
  chain.Draw('1e5*(scale-0.99999):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr1= TGraph(gPad.GetPrimitive("Graph"))
  gr1.GetXaxis().SetTimeDisplay(1);
  gr1.GetXaxis().SetTimeFormat(TimeFormat);
  
  gr1.SetMarkerStyle(24);
  gr1.SetMarkerSize(0.2);
  gr1.SetMarkerColor(kBlue+2);
  gr1.SetMinimum(scale_lim[0])
  gr1.SetMaximum(scale_lim[1])
  gr1.GetXaxis().SetRangeUser(0, duration)
  gr1.Draw("AP*")
  gr1.SetTitle(plotTitle+'UTC time; scope timebase factor')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_timebase_scale_factor.png')
  
  
  '''
  gStyle.SetOptStat(1111)
  chain.Draw('1e5*(scale-0.99999)>>h6(50, 0.64, 0.84)', 'daTime>'+ stable + '&& daTime<'+end)
  hh6=h6.DrawNormalized()
  hh6.SetMaximum(0.3)
  text = TLatex(0.66, 0.2,"scale_{true} = 0.99999 + 10^{  - 5} #times #bar{scale}")
  text.SetTextSize(0.03)
  text.Draw()
  hh6.SetTitle(plotTitle+'#bar{scale}; normalized')
  c1.SaveAs(outDir+'/fill_'+str(fill)+'_scope_timebase_scale_factor_fill_hist.png')
  
  '''
  
  chain.Draw('int(b1_flag)', 'daTime>'+ begin + '&& daTime<'+end, "hist")
  chain.Draw('int(b2_flag)', 'daTime>'+ begin + '&& daTime<'+end, "same")
  c1.SaveAs("h_2.png")
  
