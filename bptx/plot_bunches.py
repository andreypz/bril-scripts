#! /usr/bin/python

import sys,os,datetime
from  ROOT import *
import fill_class as f
import read_timber_data as tim

gROOT.SetBatch()
from array import *

fillNumber = sys.argv[1]
if len(sys.argv) < 2:
  print '\t ERROR. Provide the Fill number, like: plot_bunches.py 1234'
  sys.exit(1)


if fillNumber == "0":
  c = f.LHCFills(0, TDatime(2015,9,17,2,10,00), None, TDatime(2015,9,17,2,15,00))
  TimeFormat ="%H:%M"
  # For the whole history plots
  # c = f.LHCFills(0, TDatime(2015,6,10,1,00,00), None, TDatime(2015,10,14,1,00,00))
  # TimeFormat ="%d %b"
else:
  c = f.LHCFills(fillNumber)
  TimeFormat ="%H:%M"

# This will over-write the Times above:
#c = f.LHCFills(4565)

def createDir(myDir):
  if not os.path.exists(myDir):
    try: os.makedirs(myDir)
    except OSError:
      if os.path.isdir(myDir): pass
  else:
    print myDir, 'already exists'

print 'Fill = ', c.Fill()
# print c.Title()
c.Begin().Print()
# print 'Fill begin Day= ', c.Begin().GetDay()
fill = c.Fill()

beginTime  = c.Begin()
if (c.Stable()!=None): stableTime = c.Stable()
else:  stableTime = c.Begin()

endTime    = c.End()

path = "../../BPTXMONDATA/"
chain = TChain("bunchTree");
#chain.Add(path+"root/all_bunches.root")
chain.Add(path+"root/bptx_mon_bunches_2015_09_16_UTC.root")
chain.Add(path+"root/bptx_mon_bunches_2015_09_20_UTC.root")
chain.Add(path+"root/bptx_mon_bunches_2015_09_22_UTC.root")
chain.Add(path+"root/bptx_mon_bunches_2015_08_24_UTC.root")
chain.Add(path+"root/bptx_mon_bunches_2015_08_26_UTC.root")

# Integral to Intensity scale factors
ItoIfactor1 = '0.960';
ItoIfactor2 = '0.960';
# Area to intensity scale factor
AtoIfactor1 = '0.4951';
AtoIfactor2 = '0.5034';


print 'Chain N entries = ', chain.GetEntries()

b1_bunches = []
b2_bunches = []

#orbit2_wrt_orbit1 = 32.4142744
#bptx1_wrt_orbit1  = 6.621972
#bptx2_wrt_orbit2  = -25.79339
#bptx2_wrt_orbit1  = bptx2_wrt_orbit2+orbit2_wrt_orbit1

gROOT.ProcessLine(".L ~/tdrstyle.C")
#gROOT.ProcessLine(".L /home/andreypz/Dropbox/tdrstyle.C")

setTDRStyle()
gStyle.SetTimeOffset(beginTime.Convert());
gStyle.SetLabelSize(0.03,"X");
gStyle.SetLabelOffset(0.02,"X");
begin  = str(beginTime.Convert())
stable = str(stableTime.Convert())
end    = str(endTime.Convert())
duration = endTime.Convert() - beginTime.Convert()

# BX: time offset from Orbit
bunches = {'1':0, '51':0, '91':0}
''' bunches = {'1':  0,
           '39': 0,
           '79': 0,
           '80': 0,
           '81': 0,
           '82': 0,
           #'222': 0,
           #'333': 0,
           #'999': 0,
           #'1111': 0,
           #'': 0,
           #'': 0,
           }
'''
b1_int = []
b2_int = []

outDir = './bunches/fill_'+str(fill)
createDir(outDir)



MagicNumber = '3564'
chain.Draw('b1_bunches>>pat1('+MagicNumber+', 0,'+MagicNumber+')', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs(outDir+"/"+'fill_'+str(fill)+"_B1_pattern.png")
chain.Draw('b2_bunches>>pat2('+MagicNumber+', 0,'+MagicNumber+')', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs(outDir+"/"+'fill_'+str(fill)+"_B2_pattern.png")

Nbunches = 0
for binN in xrange(0,int(MagicNumber)):
  if pat1.GetBinContent(binN)>10:
    Nbunches+=1
    #print Nbunches, binN-1, pat1.GetBinContent(binN)
    b1_bunches.append(binN-1)

Nbunches = 0
for binN in xrange(0,int(MagicNumber)):
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
print "\n N_B1 = ",len(b1_bunches), "N_B2 = ", len(b2_bunches)
print "N_AND = ",len(bx_AND), "N_OR = ", len(bx_OR)


def getPositionInArray(myarray, BX=1):
  posb = [i for i,x in enumerate(myarray) if x == BX]
  try:
    b = str(posb[0])
  except IndexError:
    b=None

  return b


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



def drawVStime(formula1, formula2, BX, minmax, name="bunchIntegral",
               title = 'Intensity, protons #times 10^{11}', EXT1=None, EXT2=None, ):

  # This obe draws everything vs Time!

  chain.Draw(formula1+':daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
  gr1 = TGraph(gPad.GetPrimitive("Graph"))
  b1_int.append(gr1.Clone())
  chain.Draw(formula2+':daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
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

  gr1.SetMinimum(minmax[0])
  gr1.SetMaximum(minmax[1])

  gr1.Draw("AP")
  gr2.Draw("P same")
  gr1.SetTitle('Fill '+str(fill) +', BX = '+BX +';UTC time;'+title)

  if EXT1:
    if BX=='TOT':
      ext1 = tim.readTIMBER_TOT_INT(fill, EXT1[0], EXT1[1])
    else:
      ext1 = tim.readTIMBER_BX_INT(fill, BX, EXT1[0], EXT1[1])
    ext1.Draw('same')
    ext1.SetLineColor(kGray)
    ext1.SetLineWidth(2)

  if EXT2:
    if BX=='TOT':
      ext2 = tim.readTIMBER_TOT_INT(fill, EXT2[0], EXT2[1])
    else:
      ext2 = tim.readTIMBER_BX_INT(fill, BX, EXT2[0], EXT2[1])
    ext2.Draw('same')
    ext2.SetLineColor(kGray+2)
    ext2.SetLineWidth(2)

  if EXT1 and EXT2:
    leg = TLegend(0.70,0.70,0.90,0.90)
    leg.AddEntry(gr1,"CMS B1", "f")
    leg.AddEntry(gr2,"CMS B2", "f")
    if EXT1[0]=='ATLAS':
      leg.AddEntry(ext1,"ATLAS B1", "l")
      leg.AddEntry(ext2,"ATLAS B2", "l")
    elif EXT1[0]=='BCTDC.A6R4':
      leg.AddEntry(ext1,"BCTDC.A6R4 B1", "l")
      leg.AddEntry(ext2,"BCTDC.A6R4 B2", "l")
    elif EXT1[0]=='BCTFR.A6R4':
      leg.AddEntry(ext1,"BCTFR.A6R4 B1", "l")
      leg.AddEntry(ext2,"BCTFR.A6R4 B2", "l")
    elif EXT1[0]=='CMS.BPTX':
      leg.AddEntry(ext1,"CMS.BPTX B1", "l")
      leg.AddEntry(ext2,"CMS.BPTX B2", "l")

  else:
    leg = TLegend(0.70,0.70,0.85,0.80)
    leg.AddEntry(gr1,"Beam 1", "f")
    leg.AddEntry(gr2,"Beam 2", "f")

  leg.SetFillColor(kWhite)
  leg.Draw()

  c1.SaveAs(outDir+"/"+'_'.join(['fill',str(fill),name,'BX',BX,'bptxmon.png']))
  del(gr1)
  del(gr2)



def makeCSVfile(fname,btree, begin_t, end_t, Beam='B1'):
  print '\t ** Making the .csv file with per-bunch intensity data:', fname

  csv_file = open(fname, "w")  
  csv_file.write("# Bunch charges from CMS BPTX for Beam=%s \n"%Beam)
  csv_file.write("# Format: Time,array of ints\n")
  

  for e in btree:
    # print e.daTime, begin.Con, end_t

    if e.daTime < begin_t.Convert(): continue
    if e.daTime > end_t.Convert(): continue

    
    if Beam=='B1':
      tree_bunches = e.b1_bunches
      array_bunches = b1_bunches
      tree_amp = e.b1_amp
      tree_len = e.b1_len
      AtoIfactor = AtoIfactor1

    elif Beam=='B2':
      tree_bunches = e.b2_bunches
      array_bunches = b2_bunches
      tree_amp = e.b2_amp
      tree_len = e.b2_len
      AtoIfactor = AtoIfactor2
    else:
      print "Nope, This beam type is not supported:", Beam
      sys.exit()

    if len(tree_bunches)!=len(array_bunches):
      print '\t ** WARNING: Number of bunches dont agree', len(tree_bunches), len(array_bunches)
      continue 
    # print e.daTime, len(b1_bunches)
    charge_array=[0]*3564

    for b in tree_bunches:
      # print 'bunch in a tree =', b
      b_pos = int(getPositionInArray(array_bunches, b))
      # print 'Posiotion in array =', b_pos
      try: 
        isit = tree_bunches[b_pos]
      except IndexError:
        print len(tree_bunches)
        print '\t ** IndexError catch: Wrong bunch position:', b, b_pos
        continue 
      if isit!=int(b):
        print '\t ** WARNING: Wrong bunch position:', b, isit
      # print b, b_pos,isit
      charge_array[int(b)-1] = (int(float(AtoIfactor)*1E20*tree_amp[b_pos]*tree_len[b_pos]))
          
    if len(charge_array):
      line = ','.join([datetime.datetime.fromtimestamp(e.daTime).strftime('%Y-%m-%d %H:%M:%S.000')]+
                       [str(ch) for ch in charge_array])
      csv_file.write(line+'\n')

  csv_file.close()
  
  print '\t ** Finished with the file-making'


if __name__ == "__main__":

  formula1 = 'Sum$(b1_amp)'
  formula2 = 'Sum$(b2_amp)'
  drawVStime(formula1, formula2, 'TOT', [0,3000], name="sumOfAmplitudes", title='Sum of amplitudes')

  makeCSVfile('test-B1.csv',chain, beginTime, endTime, 'B1')
  makeCSVfile('test-B2.csv',chain, beginTime, endTime, 'B2')

  # If the integral data is good:
  #formula1 = '1E9*Sum$(b1_int)'
  #formula2 = '1E9*Sum$(b2_int)'
  # If the integral is bad, can use simple area:
  formula1 = AtoIfactor1+'*1E9*Sum$(b1_amp*b1_len)'
  formula2 = AtoIfactor2+'*1E9*Sum$(b2_amp*b2_len)'
  #drawVStime(formula1, formula2, 'TOT', [800,1100], name="totalCharge", title='Total beam charge, #times 10^{11}',
  #           EXT1=['BCTFR.A6R4','B1_TOTINT'], EXT2=['BCTFR.A6R4','B2_TOTINT'])
  drawVStime(formula1, formula2, 'TOT', [850,1100], name="totalCharge", title='Total beam charge, #times 10^{11}',
             EXT1=['BCTDC.A6R4','B1_TOTINT'], EXT2=['BCTDC.A6R4','B2_TOTINT'])

  formula1 = AtoIfactor1+'*1E9*Sum$(b1_amp*b1_len)/Length$(b1_amp)'
  formula2 = AtoIfactor2+'*1E9*Sum$(b2_amp*b2_len)/Length$(b2_amp)'
  drawVStime(formula1, formula2, 'AVG', [0,3], name="averageCharge", title='Average bunch charge, #times 10^{11}')


  for bb, sh in bunches.iteritems():

    print 'bb and sh =', bb, sh

    b1 = getPositionInArray(b1_bunches, int(bb))
    b2 = getPositionInArray(b2_bunches, int(bb))

    print 'Position of the BX=%s in the arrays, B1 and B2 ' % bb, b1,b2

    if b1==None or b2==None:
      print 'Sorry, no bunches are found for BX=',bb
      continue

    # formula1 = ItoIfactor1+'*0.5*1e9*(b1_int['+b1+'])'
    # formula2 = ItoIfactor2+'*0.5*1e9*(b2_int['+b2+'])'
    # drawVStime(formula1, formula2, [0,3], name="bunchIntegral", title='Intensity, protons #times 10^{11}')

    formula1 = AtoIfactor1+'*1e9*(b1_amp['+b1+']*b1_len['+b1+'])'
    formula2 = AtoIfactor2+'*1e9*(b2_amp['+b2+']*b2_len['+b2+'])'
    #drawVStime(formula1, formula2, bb, [0,3], name="bunchIntensity", title='Charge, protons #times 10^{11}')

    drawVStime(formula1, formula2, bb, [0.7,1.4], name="bunchIntensity", title='Charge, protons #times 10^{11}',
               EXT1=['CMS.BPTX','B1_INT'], EXT2=['CMS.BPTX','B2_INT'])

    #drawVStime(formula1, formula2, bb, [0.5,1.5], name="bunchIntensity", title='Charge, protons #times 10^{11}',
    #           EXT1=['BCTFR.A6R4','B1_INT'], EXT2=['BCTFR.A6R4','B2_INT'])


    formula1 = '1e9*(b1_len['+b1+'])'
    formula2 = '1e9*(b2_len['+b2+'])'
    drawVStime(formula1, formula2, bb, [1.0,1.4], name="bunchLength", title='Pulse length, ns')

    formula1 = '(b1_amp['+b1+'])'
    formula2 = '(b2_amp['+b2+'])'
    drawVStime(formula1, formula2, bb, [1,3], name="bunchAmplitude", title='Pulse amplitude, V')



    # This one is special, let's leave it as is for right now
    dTcalib = '2.65'
    chain.Draw('1e9*(b1_time_zc['+b1+']-b2_time_zc['+b2+']) - '+
               dTcalib+':daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
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

    gr1.SetMinimum(-0.5)
    gr1.SetMaximum(0.5)
    gr1.Draw("AP")
    #gr2.Draw("same P")
    gr1.SetTitle('Fill '+str(fill) +', BX = '+bb +';UTC time;deltaT (B1-B2), ns')

    leg = TLegend(0.20,0.73,0.45,0.83)
    leg.AddEntry(gr1,"Zero-cross", "p")
    #leg.AddEntry(gr2,"Leading-ed", "p")
    leg.SetFillColor(kWhite)
    # leg.Draw()

    c1.SaveAs(outDir+"/"+'fill_'+str(fill)+'_deltaT_b_'+str(bb)+'_bptxmon.png')
    del(gr1)
    #del(gr2)


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

    """ HIST
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

    chain.Draw('1e9*(b1_int['+b1+'])>>h1(100,0.,2.35)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
    chain.Draw('1e9*(b2_int['+b2+'])>>h2(100,0.,2.35)', 'daTime>'+ stable + '&& daTime<'+end, 'hist same')
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
    """

'''
chain.Draw('1e9*b1_time_zc>>hhh(1000, 0,100000)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs("h_1.png")

chain.Draw('1e9*b1_time_zc>>hhh(500, 0,12000)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs("h_2.png")

chain.Draw('1e9*b1_time_zc>>hhh(500, 83000,90000)', 'daTime>'+ stable + '&& daTime<'+end, 'hist')
c1.SaveAs("h_3.png")
'''

#chain.Draw("1e9*(b1_time_zc[4])>>hhh", 'daTime>'+ stable + '&& daTime<'+end, 'hist')
#mymax =  hhh.GetMaximum()
#hhh.SetMaximum(1.2*mymax)
#hhh.SetNdivisions(505,"X")
#c1.SaveAs("h_4.png")

#chain.Draw('1e9*(b1_time_zc-b2_time_zc):daTime-'+begin, 'daTime>'+ stable + '&& daTime<'+end)
#c1.SaveAs("h_5.png")
