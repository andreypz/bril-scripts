#! /usr/bin/python

import sys
sys.argv.append( '-b' )

from array import *
from  ROOT import *
import fill_class as f

c = f.LHCFills(2343)

c.Begin().Print()
fill = c.Fill()
beginTime  = c.Begin()
stableTime = c.Stable()
endTime    = c.End()
plotTitle  = c.Title()

path = "/home/andreypz/Dropbox/BPTXmon_data/"

chain = TChain("cogTree");
chain.Add(path+"root/bptx_mon_cogging_2011_12_05_UTC.root")
chain.Add(path+"root/bptx_mon_cogging_2011_12_06_UTC.root")

nBunches = 354
b1_bunches  = array('i', 400*[0])
b2_bunches  = array('i', 400*[0])
chain.SetBranchAddress("b1_bunches",b1_bunches)
chain.SetBranchAddress("b2_bunches",b2_bunches)
chain.GetEntry(100)
b1_bunches = sorted(list(set(b1_bunches).difference(set([0]))))
b2_bunches = sorted(list(set(b2_bunches).difference(set([0]))))
bx_AND = sorted(list(set(b1_bunches) & set(b2_bunches)))
bx_OR  = sorted(list(set(b1_bunches) | set(b2_bunches)))
b1_XOR = sorted(list(set(b1_bunches).difference(set(b2_bunches))))
b2_XOR = sorted(list(set(b2_bunches).difference(set(b1_bunches))))

print bx_AND
print b1_XOR, b2_XOR
print "N_AND = ",len(bx_AND), "N_OR = ", len(bx_OR)

#print b1_bunches

#print 'N entries in chain=', chain.GetEntries()

gROOT.ProcessLine(".L     /home/andreypz/Dropbox/tdrstyle.C")
setTDRStyle()
gStyle.SetTimeOffset(beginTime.Convert());
gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");
begin  = str(beginTime.Convert())
stable = str(stableTime.Convert())
end    = str(endTime.Convert())
duration = endTime.Convert() - beginTime.Convert()


fileNameBase = "timber_FBCT_"+str(c.Fill())
f1 = TFile("root/"+fileNameBase+"_b1.root","open");
f2 = TFile("root/"+fileNameBase+"_b2.root","open");
fbctTree1 = f1.Get("fbctTree")
fbctTree2 = f2.Get("fbctTree")

bunches = {}
for n in range(0,nBunches):
    bunches[str(n+1)]= b1_bunches[n]
 
b1_int  = []
b2_int  = []
b1_fbct = []
b2_fbct = []

b1,b2=0,0
for bx in bx_OR:
    if len(b1_int)>nBunches or len(b2_int)>nBunches: break
    if bx in bx_AND:
        print bx
        b1+=1
        b2+=1
    elif bx in b1_XOR:
        b1+=1
        continue
    elif bx in b2_XOR:
        b2+=1
        continue
    else: print "bx is not in any list"

    chain.Draw('1e9*(b1_int['+str(b1)+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr1 = TGraph(gPad.GetPrimitive("Graph"))
    b1_int.append(gr1.Clone())
    chain.Draw('1e9*(b2_int['+str(b2)+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr2 = TGraph(gPad.GetPrimitive("Graph"))
    b2_int.append(gr2.Clone())

    fbctTree1.Draw('1e-9*fbct['+str(bx-1)+']:daTime-'+begin, 'daTime>'+ begin + '&& daTime<'+end)
    gr3 = TGraph(gPad.GetPrimitive("Graph"))
    b1_fbct.append(gr3.Clone())
        
    fbctTree2.Draw('1e-9*fbct['+str(bx-1)+']:daTime-'+begin, 'daTime>'+ begin + '&& daTime<'+end)
    gr4 = TGraph(gPad.GetPrimitive("Graph"))
    b2_fbct.append(gr4.Clone())

    chain.Draw('(b1_amp['+str(b1)+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr5 = TGraph(gPad.GetPrimitive("Graph"))
    #b1_amp.append(gr5.Clone())
    chain.Draw('(b2_amp['+str(b2)+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr6 = TGraph(gPad.GetPrimitive("Graph"))
    #b2_amp.append(gr6.Clone())

    c1.Clear()
    
    gr1.GetXaxis().SetTimeDisplay(1)
    gr1.GetXaxis().SetTimeFormat("%H:%M")

    gr1.SetMarkerStyle(24)
    gr2.SetMarkerStyle(25)
    gr3.SetMarkerStyle(26)
    gr4.SetMarkerStyle(27)
    gr5.SetMarkerStyle(28)
    gr6.SetMarkerStyle(28)
    gr1.SetMarkerSize(0.4)
    gr2.SetMarkerSize(0.4)
    gr3.SetMarkerSize(0.4)
    gr4.SetMarkerSize(0.4)
    gr5.SetMarkerSize(0.4)
    gr6.SetMarkerSize(0.4)
    gr1.SetMarkerColor(kBlue+1)
    gr2.SetMarkerColor(kRed+1)
    gr3.SetMarkerColor(kBlue+3)
    gr4.SetMarkerColor(kRed+3)
    gr5.SetMarkerColor(kGreen+1)
    gr6.SetMarkerColor(kOrange+1)
    gr1.SetFillColor(kBlue+1)
    gr2.SetFillColor(kRed+1)
    gr3.SetFillColor(kBlue+3)
    gr4.SetFillColor(kRed+3)
    gr5.SetFillColor(kGreen+1)
    gr6.SetFillColor(kOrange+1)

    gr1.SetMaximum(0.35)
    gr1.SetMinimum(0.1)


    # From    tutorials/hist/transpad.C
    ymin = 5
    ymax = 15
    dy = float(ymax-ymin)/0.80
    
    xmin = 0
    xmax = duration
    dx = float(xmax-xmin)/0.68
    print ymin, ymax,dy, xmin, xmax,dx

    gr1.GetXaxis().SetLimits(xmin, xmax)

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
    
    gr1.Draw("AP")
    gr2.Draw("P same")
    #pad1.Modified()
    pad1.Update()

    xx1 = pad1.GetX1()
    xx2 = pad1.GetX2()
    #print xx1,xx2
    pad2.Range(xx1,ymin-0.14*dy,xx2,ymax+0.06*dy);
    pad2.Draw()
    pad2.cd()

    gr3.Draw("same P")
    gr4.Draw("same P")
    pad2.Update()

    axis =  TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,510,"+L");    
    #    axis.SetLineColor(kGreen+3);
    #    axis.SetTextColor(kGreen);
    axis.SetTitle("FBCT, 1e9 protons")
    axis.Draw();
    axis.SetTitleOffset(1.1)
    axis.SetTitleSize(0.05)

    #axis2 =  TGaxis(xmin,ymin,xmin,ymax,ymin,ymax,510,"+L");    
    #axis2.SetLineColor(kGreen+3);
    #axis2.Draw();
  
    pad1.cd()

    #axis3 =  TGaxis(xmin,ymin,xmin,ymax,ymin,ymax,510,"+L");    
    #axis3.SetLineColor(kRed+3);
    #axis3.Draw();
   
    leg = TLegend(0.57,0.70,0.83,0.88)
    leg.AddEntry(gr3,"Beam 1, FBCT", "f")
    leg.AddEntry(gr4,"Beam 2, FBCT", "f")
    leg.AddEntry(gr1,"Beam 1, pulse integral", "f")
    leg.AddEntry(gr2,"Beam 2, pulse intgral", "f")
    leg.SetFillColor(kWhite)
    leg.Draw()

    line_pos = stableTime.Convert()-beginTime.Convert()
    line = TLine(line_pos,0.1,line_pos,0.3)
    line.SetLineColor(kGreen+2)
    line.SetLineWidth(2)
    line.Draw()
    text = TLatex(1.01*line_pos, 0.12,"#rightarrow stable beam")
    text.Draw()
    gr1.SetTitle('Fill '+str(fill)+', BX='+str(bx)+'; UTC time; Pulse Integral, ns*V')
    #gr1.GetYaxis().SetTitleOffset(1.2)
    #gr1.GetYaxis().SetTitleSize(0.06)

    #pad2.cd()
    #line.Draw()
    c1.SaveAs('./pulses/fill_'+str(fill)+'_pulse_integral_BX_'+str(bx)+'.png')
  
    #c1.Clear()
    
    '''  Amplitude  '''
    ymin = 0.0
    ymax = 0.35
    dy = float(ymax-ymin)/0.80
        
    xx1 = pad1.GetX1()
    xx2 = pad1.GetX2()
    
    c1.cd()
    pad2.Clear()
    pad2.Range(xx1,ymin-0.14*dy,xx2,ymax+0.06*dy);
    pad2.Draw()
    pad2.cd()

    gr5.Draw("same P")
    gr6.Draw("same P")
    pad2.Update()

    axis =  TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,510,"+L");    
    axis.SetTitle("Pulse Amplitude, V")
    axis.Draw();
    axis.SetTitleOffset(1.1)
    axis.SetTitleSize(0.05)
    line.Draw()
    pad1.cd()
   
    line.Draw()
    
    leg = TLegend(0.57,0.70,0.83,0.88)
    leg.AddEntry(gr1,"Beam 1, pulse integral", "f")
    leg.AddEntry(gr2,"Beam 2, pulse intgral", "f")
    leg.AddEntry(gr5,"Beam 1, pulse amplitude", "f")
    leg.AddEntry(gr6,"Beam 2, pulse amplitude", "f")
    leg.SetFillColor(kWhite)
    leg.Draw()

    c1.SaveAs('./pulses/fill_'+str(fill)+'_pulse_amplitude_BX_'+str(bx)+'.png')


    del(gr1)
    del(gr2)
    del(gr3)
    del(gr4)
    del(gr5)
    del(gr6)

    
c1.Clear()

print "number of b1: ", len(b1_int), len(b1_fbct)
print "number of b2: ", len(b2_int), len(b2_fbct)

hist_b1_par0 = TH1F('b1_par0','Fill '+str(fill)+'; crossing zero (par0); Entries', 50, -0.5, 0.6)
hist_b2_par0 = TH1F('b2_par0','Fill '+str(fill)+'; crossing zero (par0); Entries', 50, -0.5, 0.6)
hist_b1_par1 = TH1F('b1_par1','Fill '+str(fill)+'; slope (par1); Entries', 50, 44, 52)
hist_b2_par1 = TH1F('b2_par1','Fill '+str(fill)+'; slope (par1); Entries', 50, 44, 52)

it = 0
for bx in bx_AND:
    if it>=nBunches: break

    fbct_vs_int_b1 = TGraph()
    fbct_vs_int_b2 = TGraph()
    #b1_int[it].Draw("P same")
    #print b1_int[it].GetN(), b1_fbct[it].GetN()

    nPoints = b1_int[it].GetN()
    t1,t2, d1,d2 = Double(0),Double(0), Double(0), Double(0)
    for point in range(nPoints):
        b1_int[it].GetPoint(point, t1,d1)
        b2_int[it].GetPoint(point, t2,d2)
        #print t,d
        if t1!=t2: print "t1!=t2"
        fbct_vs_int_b1.SetPoint(point,d1, b1_fbct[it].Eval(t1))
        fbct_vs_int_b2.SetPoint(point,d2, b2_fbct[it].Eval(t2))

    
    fbct_vs_int_b1.GetXaxis().SetLimits(0.1, 0.35)
    fbct_vs_int_b1.SetMaximum(15)
    fbct_vs_int_b1.SetMinimum(5)
    fbct_vs_int_b1.SetMarkerStyle(24)
    fbct_vs_int_b2.SetMarkerStyle(25)
    fbct_vs_int_b1.SetMarkerColor(kBlue+1)
    fbct_vs_int_b1.SetFillColor(kBlue+1)
    fbct_vs_int_b2.SetMarkerColor(kRed+2)
    fbct_vs_int_b2.SetFillColor(kRed+2)
    fbct_vs_int_b1.SetMarkerSize(0.4)
    fbct_vs_int_b2.SetMarkerSize(0.4)
    
    fbct_vs_int_b1.Draw("AP")
    fbct_vs_int_b2.Draw("same P")
    
    ff1 = TF1("ff1","[0]+[1]*x",0,1)
    ff2 = TF1("ff2","[0]+[1]*x",0,1)

    ff1.SetLineColor(kCyan)
    ff2.SetLineColor(kRed)
    ff1.SetLineWidth(2)
    ff2.SetLineWidth(2)
    
    fbct_vs_int_b1.Fit(ff1,"QS")
    fbct_vs_int_b2.Fit(ff2,"QS")
    it+=1

    hist_b1_par0.Fill(ff1.GetParameter(0))
    hist_b1_par1.Fill(ff1.GetParameter(1))
    hist_b2_par0.Fill(ff2.GetParameter(0))
    hist_b2_par1.Fill(ff2.GetParameter(1))
    #st = TPaveStats()
    #st = fbct_vs_int_b2.GetListOfFunctions().FindObject("stats")
    #f1.GetListOfFunctions()
    #print f1.FindObject("stats")
    #st.Print()
    #st.SetX1NDC(0.2)
    #st.SetX2NDC(0.5)
    
    leg = TLegend(0.2,0.72,0.4,0.82)
    leg.AddEntry(fbct_vs_int_b1,"Beam 1", "f")
    leg.AddEntry(fbct_vs_int_b2,"Beam 2", "f")
    leg.SetFillColor(kWhite)
    leg.Draw()

    fbct_vs_int_b1.SetTitle('Fill '+str(fill)+', BX='+str(bx)+'; Pulse Integral, ns*V; fbct')
    c1.SaveAs('./pulses/fill_'+str(fill)+'_fbct_vs_integral_BX_'+str(bx)+'.png')

    del(fbct_vs_int_b1)
    del(fbct_vs_int_b2)
           

#print b1_par0
#print b1_par1

gStyle.SetOptStat(1111)
hist_b1_par0.Draw()
hist_b2_par0.Draw("same")
hist_b1_par0.SetLineColor(kBlue+1)
hist_b2_par0.SetLineColor(kRed+1)

leg = TLegend(0.2,0.72,0.4,0.82)
leg.AddEntry(hist_b1_par0,"Beam 1", "l")
leg.AddEntry(hist_b2_par0,"Beam 2", "l")
leg.SetFillColor(kWhite)
leg.Draw()
c1.SaveAs('./pulses/fit_fill_'+str(fill)+'_par0.png')


hist_b1_par1.Draw()
hist_b2_par1.Draw("same")
hist_b1_par1.SetLineColor(kBlue+1)
hist_b2_par1.SetLineColor(kRed+1)
leg.Draw()
c1.SaveAs('./pulses/fit_fill_'+str(fill)+'_par1.png')
