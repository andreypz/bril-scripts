#! /usr/bin/python

import sys,os
from  ROOT import *
import fill_class as f
gROOT.SetBatch()
from array import *

#cable scope01 script 2.40 + 0.24 = 2.64

beginTime  = TDatime(2011,12,01,01,00,00)
stableTime = TDatime(2011,12,01,01,00,00)
endTime    = TDatime(2011,12,01,23,00,00)

c = f.LHCFills(3858)

def createDir(myDir):
  if not os.path.exists(myDir):
    try: os.makedirs(myDir)
    except OSError:
      if os.path.isdir(myDir): pass
  else: 
      print myDir, 'already exists'


print c.Fill()
print c.Title()
c.Begin().Print()
print c.Begin().GetDay()
fill = c.Fill()
plotTitle = ';'

beginTime  = c.Begin()
stableTime = c.Stable()
endTime    = c.End()
plotTitle = c.Title()

path = "./DATA/"
chain = TChain("bunchTree");
chain.Add(path+"root/all_bunches.root")

print 'Chain N entries = ', chain.GetEntries()

#nMaxBunches = 1000
b1_bunches = []
b2_bunches = []
#b1_bunches  = array('i', nMaxBunches*[0])
#b2_bunches  = array('i', nMaxBunches*[0])
#chain.SetBranchAddress("b1_bunches",b1_bunches)
#chain.SetBranchAddress("b2_bunches",b2_bunches)



orbit2_wrt_orbit1 = 32.4142744
bptx1_wrt_orbit1  = 6.621972
bptx2_wrt_orbit2  = -25.79339
bptx2_wrt_orbit1  = bptx2_wrt_orbit2+orbit2_wrt_orbit1
#print beginTime, str(beginTime.Convert())

gROOT.ProcessLine(".L     /home/andreypz/Dropbox/tdrstyle.C")
setTDRStyle()
gStyle.SetTimeOffset(beginTime.Convert());
gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");
begin  = str(beginTime.Convert())
stable = str(stableTime.Convert())
end    = str(endTime.Convert())
duration = endTime.Convert() - beginTime.Convert()


bunches = {'1': bptx1_wrt_orbit1  - 0.003,
           '3': bptx1_wrt_orbit1  + 0.2  -0.004,
           '5': bptx1_wrt_orbit1  + 0.2*2-0.005,
           #'4': bptx1_wrt_orbit1  + 0.2*9-0.007
           }

b1_int = []
b2_int = []

outDir = './bunches/fill_'+str(fill)
createDir(outDir)



chain.Draw('b1_bunches>>pat1(3456, 0,3456)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs(outDir+"/"+'fill_'+str(fill)+"_B1_pattern.png")
chain.Draw('b2_bunches>>pat2(3456, 0,3456)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs(outDir+"/"+'fill_'+str(fill)+"_B2_pattern.png")

Nbunches = 0
for binN in xrange(0,3456):
  if pat1.GetBinContent(binN)>10:
    Nbunches+=1
    #print Nbunches, binN-1, pat1.GetBinContent(binN) 
    b1_bunches.append(binN-1)

Nbunches = 0
for binN in xrange(0,3456):
  if pat2.GetBinContent(binN)>10:
    Nbunches+=1
    #print Nbunches, binN-1, pat2.GetBinContent(binN) 
    b2_bunches.append(binN-1)

chain.Draw('nB1', 'daTime>'+ stable + '&& daTime<'+end)
c1.SaveAs(outDir+"/"+'fill_'+str(fill)+"_NB1.png")
chain.Draw('nB2', 'daTime>'+ stable + '&& daTime<'+end)
c1.SaveAs(outDir+"/"+'fill_'+str(fill)+"_NB2.png")


b1_bunches = sorted(list(set(b1_bunches).difference(set([0]))))
b2_bunches = sorted(list(set(b2_bunches).difference(set([0]))))
bx_AND = sorted(list(set(b1_bunches) & set(b2_bunches)))
bx_OR  = sorted(list(set(b1_bunches) | set(b2_bunches)))
b1_XOR = sorted(list(set(b1_bunches).difference(set(b2_bunches))))
b2_XOR = sorted(list(set(b2_bunches).difference(set(b1_bunches))))

print 'B1  = ', b1_bunches
print 'B2  = ', b2_bunches
print '\n\n AND  = ', bx_AND
print 'XORS = ', b1_XOR, b2_XOR
print "N_AND = ",len(bx_AND), "N_OR = ", len(bx_OR)
    


def makeHists(var, names, shift, lim, bunch):
  # This function does not work for some reason

  if shift!=None:
    queryb1 = '1e9*(b1_%s[%i]-%.6fe-6)>>hh1(150,%.1f,%.1f)' %(var, bunch, shift, lim[0], lim[1]) 
    queryb2 = '1e9*(b2_%s[%i]-%.6fe-6)>>hh2(150,%.1f,%.1f)' %(var, bunch, shift, lim[0], lim[1]) 

  print queryb1
  print queryb2

  #hh1 =  TH1F('n1','n1',150, lim[0], lim[1])
  #hh2 =  TH1F('n2','n2',150, lim[0], lim[1])

  chain.Draw(queryb1, 'daTime>'+ stable + '&& daTime<'+end, 'hist')
  chain.Draw(queryb2, 'daTime>'+ stable + '&& daTime<'+end, 'hist same')

  hh1.Print()
  hh2.Print()

  mymax =  hh1.GetMaximum()
  hh1.SetMaximum(1.5*mymax)
  hh1.SetLineColor(kBlue+1)
  hh2.SetLineColor(kRed+1)
  #hh3.SetLineColor(kBlue+3)
  #h4.SetLineColor(kRed+3)
  hh1.SetNdivisions(505,"X")
  hh1.SetTitle('Fill '+str(fill) +', BX = '+ bunch+';'+names[0]+'; entries')
  #chain.Draw('(1e9)*(b2_time_le['+b+']-'+shift+')', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
  #h2    =  gPad.GetPrimitive("htemp")
  #h2.Draw("hist")
  leg = TLegend(0.20,0.6,0.45,0.80)
  leg.AddEntry(hh1,"Beam 1, zero-cross", "l")
  leg.AddEntry(hh2,"Beam 2, zero-cross", "l")
  #leg.AddEntry(h2,"Beam 1, leading-ed", "l")
  #leg.AddEntry(h4,"Beam 2, leading-ed", "l")
  leg.SetFillColor(kWhite)
  leg.Draw()
  
  c1.SaveAs(outDir+"/"+'fill_'+str(fill)+names[1]+str(bunch)+'_bptxmon.png')
  del(hh1)
  #del(h2)
  del(hh2)
  #del(h4)


for bb, sh in bunches.iteritems():

    print bb, sh

    posb1 = [i for i,x in enumerate(b1_bunches) if x == int(bb)]
    posb2 = [i for i,x in enumerate(b2_bunches) if x == int(bb)]

    print posb1, posb2
    b1 = str(posb1[0])
    b2 = str(posb2[0])

    """
    shift = str(sh)+'e-6'

    time_min = 0.0
    time_max = 11.0
    
    
    query = '1e9*(b1_time_zc['+b+']-'+shift+')>>h1(150, 0.0,80.0)'
    print query

    chain.Draw(query, 'daTime>'+ stable + '&& daTime<'+end, 'hist')
    #chain.Draw('1e9*(b1_time_zc['+b+']-'+shift+')>>h1(150, 0.0,80.0)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
    # chain.Draw('1e9*(b1_time_le['+b+']-'+shift+')>>h2(150, 0.0,8.0)', 'daTime>'+ stable + '&& daTime<'+end, 'hist same')
    chain.Draw('1e9*(b2_time_zc['+b+']-'+shift+')>>h3(150, 0.0,80.0)', 'daTime>'+ stable + '&& daTime<'+end, 'hist same')
    # chain.Draw('1e9*(b2_time_le['+b+']-'+shift+')>>h4(150, 0.0,8.0)', 'daTime>'+ stable + '&& daTime<'+end, 'hist same')
   
    h1.Print()
    mymax =  h1.GetMaximum()
    #h1.GetMaximum()
    h1.SetMaximum(1.5*mymax)
    h1.SetLineColor(kBlue+1)
    #h2.SetLineColor(kRed+1)
    h3.SetLineColor(kBlue+3)
    #h4.SetLineColor(kRed+3)
    h1.SetNdivisions(505,"X")
    h1.SetTitle('Fill '+str(fill) +', bunch #'+bb +'; bunch arrival time - arbit. shift, ns; entries')
    #chain.Draw('(1e9)*(b2_time_le['+b+']-'+shift+')', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
    #h2    =  gPad.GetPrimitive("htemp")
    #h2.Draw("hist")
    leg = TLegend(0.20,0.6,0.45,0.80)
    leg.AddEntry(h1,"Beam 1", "l")
    leg.AddEntry(h3,"Beam 2", "l")
    #leg.AddEntry(h2,"Beam 1, leading-ed", "l")
    #leg.AddEntry(h4,"Beam 2, leading-ed", "l")
    leg.SetFillColor(kWhite)
    leg.Draw()
    
    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_bunchTime_'+str(bb)+'_bptxmon.png')
    del(h1)
    #del(h2)
    del(h3)
    #del(h4)

    #makeHists('time_zc', ['name_1', 'name_2'], sh, [0,80], int(bb))


    chain.Draw('1e9*(b1_time_zc['+b+']-'+shift+'):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr1 = TGraph(gPad.GetPrimitive("Graph"))
    #chain.Draw('1e9*(b1_time_le['+b+']-'+shift+'):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    #gr2 = TGraph(gPad.GetPrimitive("Graph"))
    chain.Draw('1e9*(b2_time_zc['+b+']-'+shift+'):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr3 = TGraph(gPad.GetPrimitive("Graph"))
    # chain.Draw('1e9*(b2_time_le['+b+']-'+shift+'):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    # gr4 = TGraph(gPad.GetPrimitive("Graph"))
    gr1.GetXaxis().SetTimeDisplay(1)
    
    gr1.SetMarkerStyle(25)
    #gr2.SetMarkerStyle(26)
    gr3.SetMarkerStyle(27)
    #gr4.SetMarkerStyle(28)
    gr1.SetMarkerSize(0.3)
    #gr2.SetMarkerSize(0.3)
    gr3.SetMarkerSize(0.3)
    #gr4.SetMarkerSize(0.3)
    gr1.SetMarkerColor(kBlue+1)
    #gr2.SetMarkerColor(kRed+1)
    gr3.SetMarkerColor(kBlue+3)
    #gr4.SetMarkerColor(kRed+3)
    
    gr1.GetXaxis().SetTimeFormat("%H:%M")
    gr1.GetXaxis().SetRangeUser(0, duration)
    gr1.SetMinimum(time_min)
    gr1.SetMaximum(time_max)
    
    gr1.Draw("AP")
    #gr2.Draw("same P")
    gr3.Draw("same P")
    #gr4.Draw("same P")

    leg = TLegend(0.20,0.66,0.45,0.83)
    leg.AddEntry(gr1,"Beam 1, zero-cross", "p")
    leg.AddEntry(gr3,"Beam 2, zero-cross", "p")
    #leg.AddEntry(gr2,"Beam 1, leading-ed", "p")
    #leg.AddEntry(gr4,"Beam 2, leading-ed", "p")
    leg.SetFillColor(kWhite)
    leg.Draw()

    gr1.SetTitle('Fill '+str(fill) +', bunch #'+bb +'; UTC time; bunch arrival time - arbit. shift, ns')
    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_bunchTime_vsUTC_'+str(bb)+'_bptxmon.png')
    del(gr1)
    #del(gr2)
    """

    chain.Draw('1e9*(b1_time_zc['+b1+']-b2_time_zc['+b2+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr1 = TGraph(gPad.GetPrimitive("Graph"))
    #chain.Draw('1e9*(b1_time_le['+b+']-b2_time_le['+b+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    #gr2 = TGraph(gPad.GetPrimitive("Graph"))
    gr1.GetXaxis().SetTimeDisplay(1)
    gr1.SetMarkerStyle(24)
    #gr2.SetMarkerStyle(25)
    gr1.SetMarkerSize(0.4)
    #gr2.SetMarkerSize(0.4)
    gr1.SetMarkerColor(kBlue+1)
    #gr2.SetMarkerColor(kRed+1)
    gr1.GetXaxis().SetTimeFormat("%H:%M")
    gr1.GetXaxis().SetRangeUser(0, duration)
    
    gr1.SetMinimum(1.)
    gr1.SetMaximum(5)
    gr1.Draw("AP")
    #gr2.Draw("same P")
    gr1.SetTitle('Fill '+str(fill) +', BX = '+bb +';UTC time;deltaT (B1-B2), ns')

    leg = TLegend(0.20,0.73,0.45,0.83)
    leg.AddEntry(gr1,"Zero-cross", "p")
    #leg.AddEntry(gr2,"Leading-ed", "p")
    leg.SetFillColor(kWhite)
    leg.Draw()

    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_deltaT_b_'+str(bb)+'_bptxmon.png')
    del(gr1)
    #del(gr2)


    chain.Draw('1e9*(b1_time_zc['+b1+']-b2_time_zc['+b2+'])>>h1(80,1,4)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
    #chain.Draw('1e9*(b1_time_le['+b+']-b2_time_le['+b+'])>>h2(80,1,4)', 'daTime>'+ stable + '&& daTime<'+end, 'hist same')
    mymax =  h1.GetMaximum()
    h1.GetMaximum()
    h1.SetMaximum(1.3*mymax)
    h1.SetLineColor(kBlue+1)
    #h2.SetLineColor(kRed+1)
    h1.SetNdivisions(508,"X")
    h1.SetTitle('Fill '+str(fill) +', BX = '+bb +';deltaT (B1-B2), ns; entries')

    leg = TLegend(0.20,0.73,0.45,0.83)
    leg.AddEntry(h1,"Zero-cross", "l")
    #leg.AddEntry(h2,"Leading-ed", "l")
    leg.SetFillColor(kWhite)
    leg.Draw()
    
    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_hist_deltaT_b_'+str(bb)+'_bptxmon.png')
    del(h1)
    #del(h2)


    chain.Draw('1e9*(b1_half_int['+b1+'])>>h1(100,0.,2.35)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
    chain.Draw('1e9*(b2_half_int['+b2+'])>>h2(100,0.,2.35)', 'daTime>'+ stable + '&& daTime<'+end, 'hist same')
    mymax =  h1.GetMaximum()
    h1.GetMaximum()
    h1.SetMaximum(1.5*mymax)
    h1.SetLineColor(kBlue+1)
    h2.SetLineColor(kRed+1)
    h1.SetNdivisions(505,"X")
    #h1.SetTitle('Fill '+str(fill) +', Bunch #'+bb +';Intensity, (protons x 10^{9});Entries')
    h1.SetTitle('Fill '+str(fill) +', BX = '+bb +';Integral, ns*V; entries')

    leg = TLegend(0.20,0.70,0.35,0.80)
    leg.AddEntry(h1,"Beam 1", "l")
    leg.AddEntry(h2,"Beam 2", "l")
    leg.SetFillColor(kWhite)
    leg.Draw()
    
    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_hist_bunchIntegral_'+str(bb)+'_bptxmon.png')
    del(h1)
    del(h2)

    ItoIfactor = '0.960';
 
    chain.Draw(ItoIfactor+'*1e9*(b1_half_int['+b1+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr1 = TGraph(gPad.GetPrimitive("Graph"))
    b1_int.append(gr1.Clone())
    chain.Draw(ItoIfactor+'*1e9*(b2_half_int['+b2+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr2 = TGraph(gPad.GetPrimitive("Graph"))
    b2_int.append(gr2.Clone())
    gr1.GetXaxis().SetTimeDisplay(1)
    gr1.SetMarkerStyle(24)
    gr2.SetMarkerStyle(25)
    gr1.SetMarkerSize(0.4)
    gr2.SetMarkerSize(0.4)
    gr1.SetMarkerColor(kBlue+1)
    gr2.SetMarkerColor(kRed+1)
    gr1.GetXaxis().SetTimeFormat("%H:%M")
    gr1.GetXaxis().SetRangeUser(0, duration)
    gr1.SetFillColor(kBlue+1)
    gr2.SetFillColor(kRed+1)

    gr1.SetMaximum(3.)
    gr1.SetMinimum(0.)

    gr1.Draw("AP")
    gr2.Draw("P same")
    #gr1.SetTitle('Fill '+str(fill) +', Bunch #'+bb +';UTC time; Pulse half Integral, ns*V')
    gr1.SetTitle('Fill '+str(fill) +', BX = '+bb +';UTC time;Intensity, protons #times 10^{11}')

    leg = TLegend(0.70,0.70,0.85,0.80)
    leg.AddEntry(gr1,"Beam 1", "f")
    leg.AddEntry(gr2,"Beam 2", "f")
    leg.SetFillColor(kWhite)
    leg.Draw()
    
    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_bunchIntegral_'+str(bb)+'_bptxmon.png')
    del(gr1)
    del(gr2)
    


    chain.Draw('1e9*(b1_len['+b1+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr1 = TGraph(gPad.GetPrimitive("Graph"))
    chain.Draw('1e9*(b2_len['+b2+']):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
    gr2 = TGraph(gPad.GetPrimitive("Graph"))
    gr1.GetXaxis().SetTimeDisplay(1)
    gr1.SetMarkerStyle(24)
    gr2.SetMarkerStyle(25)
    gr1.SetMarkerSize(0.4)
    gr2.SetMarkerSize(0.4)
    gr1.SetMarkerColor(kBlue+1)
    gr2.SetMarkerColor(kRed+1)
    gr1.GetXaxis().SetTimeFormat("%H:%M")
    gr1.GetXaxis().SetRangeUser(0, duration)
    gr1.SetFillColor(kBlue+1)
    gr2.SetFillColor(kRed+1)

    gr1.SetMaximum(1.4)
    gr1.SetMinimum(1.)

    gr1.Draw("AP")
    gr2.Draw("P same")
    gr1.SetTitle('Fill '+str(fill) +', BX = '+bb +';UTC time; Pulse length, ns')

    leg = TLegend(0.70,0.70,0.85,0.80)
    leg.AddEntry(gr1,"Beam 1", "f")
    leg.AddEntry(gr2,"Beam 2", "f")
    leg.SetFillColor(kWhite)
    leg.Draw()
    
    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_bunchLength_'+str(bb)+'_bptxmon.png')
    del(gr1)
    del(gr2)
    

chain.Draw('1e9*b1_time_zc>>hhh(1000, 0,100000)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs("h_1.png")

chain.Draw('1e9*b1_time_zc>>hhh(500, 0,12000)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs("h_2.png")

chain.Draw('1e9*b1_time_zc>>hhh(500, 83000,90000)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs("h_3.png")

#chain.Draw("1e9*(b1_time_zc[4])>>hhh", 'daTime>'+ stable + '&& daTime<'+end, 'hist')
#mymax =  hhh.GetMaximum()
#hhh.SetMaximum(1.2*mymax)
#hhh.SetNdivisions(505,"X")
#c1.SaveAs("h_4.png")

#chain.Draw('1e9*(b1_time_zc-b2_time_zc):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
#c1.SaveAs("h_5.png")

