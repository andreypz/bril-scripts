#! /usr/bin/python

import sys
sys.argv.append( '-b' )

from array import *
from  ROOT import *
import fill_class as f

c = f.LHCFills(2469)

c.Begin().Print()
fill = c.Fill()
beginTime  = c.Begin()
stableTime = c.Stable()
endTime    = c.End()
plotTitle  = c.Title()

chain = TChain("cogTree");
#chain.Add("root/bptx_mon_cogging_2012_04_04_UTC.root")
#chain.Add("root/bptx_mon_cogging_2012_04_05_UTC.root")
#chain.Add("root/bptx_mon_cogging_2012_04_06_UTC.root")
#chain.Add("root/bptx_mon_cogging_2011_12_05_UTC.root")
#chain.Add("root/bptx_mon_cogging_2011_12_06_UTC.root")


gROOT.ProcessLine(".L /home/andreypz/Documents/0work/tdrstyle.C")
setTDRStyle()
gStyle.SetTimeOffset(beginTime.Convert());
gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");
begin  = str(beginTime.Convert())
stable = str(stableTime.Convert())
end    = str(endTime.Convert())
duration = endTime.Convert() - beginTime.Convert()


gStyle.SetOptStat(1111)

gr_scope = []
chain.Draw('b1_gain:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
gr_scope.append(TGraph(gPad.GetPrimitive("Graph")))
chain.Draw('b2_gain:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
gr_scope.append(TGraph(gPad.GetPrimitive("Graph")))
chain.Draw('b1_offset:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
gr_scope.append(TGraph(gPad.GetPrimitive("Graph")))
chain.Draw('b2_offset:daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
gr_scope.append(TGraph(gPad.GetPrimitive("Graph")))

gr_scope[0].SetMaximum(0.08)
gr_scope[0].SetMinimum(0.0)
i=0
my_fav_colors = [kBlue, kRed, kGreen, kOrange]
for gr in gr_scope:
    gr.SetMarkerSize(0.4)
    gr.SetMarkerStyle(21+i)
    gr.SetMarkerColor(my_fav_colors[i])
    gr.SetFillColor(my_fav_colors[i])
    i+=1


gr_scope[0].GetXaxis().SetTimeDisplay(1)
gr_scope[0].GetXaxis().SetTimeFormat("%H:%M")
ymin = -0.2
ymax = 0.3
dy = float(ymax-ymin)/0.80

xmin = 0
xmax = duration
dx = float(xmax-xmin)/0.68
print ymin, ymax,dy, xmin, xmax,dx

gr_scope[0].GetXaxis().SetLimits(xmin, xmax)

pad1 = TPad("pad1","",0,0,1,1)
pad2 = TPad("pad2","",0,0,1,1)
pad2.SetFillStyle(4000)  #will be transparent
pad1.Draw()
pad1.cd()

pad1.SetTopMargin(0.06);
pad1.SetBottomMargin(0.14);
pad1.SetLeftMargin(0.16)
pad1.SetRightMargin(0.16);
pad1.SetTicky(0)

gr_scope[0].Draw("AP")
gr_scope[1].Draw("same P")
pad1.Update()

xx1 = pad1.GetX1()
xx2 = pad1.GetX2()
#print xx1,xx2
pad2.Range(xx1,ymin-0.14*dy,xx2,ymax+0.06*dy);
pad2.Draw()    
pad2.cd()

gr_scope[2].Draw("same P")
gr_scope[3].Draw("same P")
pad2.Update()

axis =  TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,510,"+L");
axis.SetLineColor(kGreen+3);
#    axis.SetTextColor(kGreen);
axis.SetTitle("Scope channel offset, V")
axis.Draw();
axis.SetTitleOffset(1.1)
axis.SetTitleSize(0.05)

pad1.cd()
                                        
leg = TLegend(0.57,0.70,0.83,0.88)
leg.AddEntry(gr_scope[0],"C1, gain", "f")
leg.AddEntry(gr_scope[1],"C2, gain", "f")
leg.AddEntry(gr_scope[2],"C1, offset", "f")
leg.AddEntry(gr_scope[3],"C2, offset", "f")
leg.SetFillColor(kWhite)
leg.Draw()
                                                           
gr_scope[0].SetTitle('Fill '+str(fill)+'; UTC time; scope channel gain, V/div ')
c1.SaveAs('./scope_para/fill_'+str(fill)+'_scope.png')

c1.Clear()

chain.Draw('1e9*cog_ddly_c1_c2>>h1(50, -2.65, -2.5)', 'daTime>'+ stable + '&& daTime<'+end)
h1.SetTitle('Fill '+str(fill)+'; delay (B2 - B1), ns; normalized')
hh=h1.DrawNormalized()
hh.SetMaximum(0.3)
c1.SaveAs('./scope_para/fill_'+str(fill)+'_cog_ddly_c1_c2.png')

chain.Draw('(abs(1e9*cog_ddly_c1_c3)-5500)>>h2(50, 3.0, 3.7)', 'daTime>'+ stable + '&& daTime<'+end)
h2.SetTitle('Fill '+str(fill)+';#bar{dly} (B1 - Orbit1), ns; normalized')
hh=h2.DrawNormalized()
hh.SetMaximum(0.3)
text = TLatex(3.1, 0.2,"delay_{true} = 5500 ns +  #bar{dly}")
text.SetTextSize(0.03)        
text.Draw()
h2.GetXaxis().SetTitleOffset(1.)
c1.SaveAs('./scope_para/fill_'+str(fill)+'_cog_ddly_c1_c3.png')

chain.Draw('(abs(1e9*cog_ddly_c2_c4)-37900)>>h3(50,18,18.8)', 'daTime>'+ stable + '&& daTime<'+end)
h3.SetTitle('Fill '+str(fill)+'; #bar{dly} (B2 - Orbit2), ns; normalized')
hh=h3.DrawNormalized()
hh.SetMaximum(0.3)
text = TLatex(18.1, 0.2,"delay_{true} = 37900 ns +  #bar{dly}")
text.SetTextSize(0.03)        
text.Draw()
c1.SaveAs('./scope_para/fill_'+str(fill)+'_cog_ddly_c2_c4.png')

chain.Draw('(-32400+1e9*cog_ddly_c3_c4)>>h4(50,12.4,12.6)', 'daTime>'+ stable + '&& daTime<'+end)
h4.SetTitle('Fill '+str(fill)+';#bar{dly} (Orbit 2 - Orbit 1), ns; normalized')
hh=h4.DrawNormalized()
hh.SetMaximum(0.3)
text = TLatex(12.42, 0.2,"delay_{true} = 32400 ns +  #bar{dly}")
text.SetTextSize(0.03)        
text.Draw()
c1.SaveAs('./scope_para/fill_'+str(fill)+'_cog_ddly_c3_c4.png')

chain.Draw('(-32400+1e9*orb_1_2)>>h5(50,12.4,12.6)', 'daTime>'+ stable + '&& daTime<'+end)
h5.SetTitle('Fill '+str(fill)+';#bar{dly} (Orbit 2 - Orbit 1), ns; normalized')
hh=h5.DrawNormalized()
hh.SetMaximum(0.3)
text = TLatex(12.42, 0.2,"delay_{true} = 32400 ns +  #bar{dly}")
text.SetTextSize(0.03)        
text.Draw()
c1.SaveAs('./scope_para/fill_'+str(fill)+'_orb_1_2.png')


chain.Draw('1e5*(scale-0.99999)>>h6(50, 0.66, 0.84)', 'daTime>'+ stable + '&& daTime<'+end)
h6.SetTitle('Fill '+str(fill)+'; #bar{scale}; normalized')
hh=h6.DrawNormalized()
hh.SetMaximum(0.3)
text = TLatex(0.68, 0.2,"scale_{true} = 0.99999 + 10^{  - 5} #times #bar{scale}")
text.SetTextSize(0.03)        
text.Draw()
c1.SaveAs('./scope_para/fill_'+str(fill)+'_timebase_scale_factor.png')


