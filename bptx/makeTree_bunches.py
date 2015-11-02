#! /usr/bin/python

import sys
sys.argv.append( '-b' )

import csv, sys
from array import *
from  ROOT import *
import re
import numpy as n

csv.field_size_limit(sys.maxsize)

gROOT.ProcessLine(
"struct MyStruct {\
Float_t version;\
Bool_t  status;\
Float_t scale;\
Float_t b1_offset;\
Float_t b1_gain;\
Float_t b2_offset;\
Float_t b2_gain;\
Float_t orb_len_trig;\
Float_t orb_len_1;\
Float_t orb_1_2;\
Float_t cog_ddly_c3_c4;\
Float_t cog_ddly_c1_c3;\
Float_t cog_ddly_c2_c4;\
Float_t cog_ddly_c1_c2;\
ULong64_t daTime;\
};\
TDatime beginTime(2011,12,01,13,00,00);\
" );

from ROOT import MyStruct


def convertToROOT(path, ascii_file):

    try:
        ascifilename = path+'/'+ascii_file+'.txt'
        spamReader = csv.reader(open(ascifilename, 'rb'), delimiter=' ', skipinitialspace=True)
    except IOError:
        print 'File %s does not exist' % (ascifilename)
        return


    stuff = MyStruct()

    ArrSize = 3700

    nB1          = array('i', [ 0 ] )
    nB2          = array('i', [ 0 ] )
    b1_bunches   = array('i', ArrSize*[0])
    b2_bunches   = array('i', ArrSize*[0])
    b1_time_zc   = array('f', ArrSize*[0])
    b2_time_zc   = array('f', ArrSize*[0])
    #b1_time_le   = array('f', ArrSize*[0])
    #b2_time_le   = array('f', ArrSize*[0])
    b1_amp       = array('f', ArrSize*[0])
    b2_amp       = array('f', ArrSize*[0])
    b1_half_int  = array('f', ArrSize*[0])
    b2_half_int  = array('f', ArrSize*[0])
    b1_len       = array('f', ArrSize*[0])
    b2_len       = array('f', ArrSize*[0])
    nCol         = array('i', [ 0 ] )
    deltaT       = array('f', [ 0 ] )


    rootFile    = TFile(path+'/root/'+ascii_file+'.root',"recreate")
    bunchTree = TTree("bunchTree","")

    bunchTree.Branch("vars", stuff, "version/F:status/i:scale/F:b1_offset:b1_gain:b2_offset:b2_gain:\
    orb_len_trig:orb_len_1:orb_1_2:cog_ddly_c3_c4:cog_ddly_c1_c3:cog_ddly_c2_c4:cog_ddly_c1_c2")
    bunchTree.Branch("time",  AddressOf( stuff, 'daTime' ), "daTime/l")

    bunchTree.Branch('nB1', nB1, 'nB1/I')
    bunchTree.Branch('nB2', nB2, 'nB2/I')
    bunchTree.Branch('b1_bunches', b1_bunches, 'b1_bunches[nB1]/I')
    bunchTree.Branch('b2_bunches', b2_bunches, 'b2_bunches[nB2]/I')
    bunchTree.Branch('b1_time_zc', b1_time_zc, 'b1_time_zc[nB1]/F')
    bunchTree.Branch('b2_time_zc', b2_time_zc, 'b2_time_zc[nB2]/F')
    #bunchTree.Branch('b1_time_le', b1_time_le, 'b1_time_le[nB1]/F')
    #bunchTree.Branch('b2_time_le', b2_time_le, 'b2_time_le[nB2]/F')
    bunchTree.Branch('b1_amp', b1_amp, 'b1_amp[nB1]/F')
    bunchTree.Branch('b2_amp', b2_amp, 'b2_amp[nB2]/F')
    bunchTree.Branch('b1_half_int', b1_half_int, 'b1_half_int[nB1]/F')
    bunchTree.Branch('b2_half_int', b2_half_int, 'b2_half_int[nB2]/F')
    bunchTree.Branch('b1_len', b1_len, 'b1_len[nB1]/F')
    bunchTree.Branch('b2_len', b2_len, 'b2_len[nB2]/F')
    bunchTree.Branch('nCol', nCol, 'nCol/I')
    bunchTree.Branch('deltaT', deltaT, 'deltaT/F')


    i=0
    for row in spamReader:
        #if i>500: break
        if (row[0] == "#" or row[2]!="1"): continue

        stuff.version = float(row[0])

        #Parse date and time, save as TDatime
        date = re.split("-|T|:|U|", row[1])
        #print date
        dt = TDatime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
        stuff.daTime = dt.Convert()

        stuff.status    = bool(row[2])
        try:
            stuff.scale     = float(row[3])
        except ValueError:
            stuff.scale = 1.0
        stuff.b1_offset = float(row[4])
        stuff.b1_gain   = float(row[5])
        stuff.b2_offset = float(row[6])
        stuff.b2_gain   = float(row[7])


        '''# Zero-crossing '''
        nB1[0]    = int(row[8])
        nB2[0]    = int(row[10])


        """
        if row[8]!=row[12]:
            print "Miss-match in number of bunches for beam 1 !!!\n",
            continue
        if row[10]!=row[14]:
            continue
            print "Miss-match in number of bunches for beam 2 !!!\n"

        if row[16]!= row[8] or row[18]!= row[10]:
            print "\n \t ---Leading edge and zc Number of bunches don't match --- \n"
            continue
        if row[20]!= row[8] or row[22]!= row[10]:
            print "\n \t --- Number of bunches don't match Amplitudes--- \n"
            continue
        if (nB1[0]!=0 and nB2[0]!=0) and (row[24]!= row[8] or row[27]!= row[10]):
            print "\n \t --- Number of bunches don't match Integrals--- \n"
            print i, [row[a] for a in [24,8,27, 10]]
            continue
        """

        #12,13 = foldovwer stuff

        # This is the arrays for B1
        bunchNum   = n.array(re.split(",",row[9]),  dtype = n.int)
        time_zc    = n.array(re.split(",",row[14]), dtype = n.float)
        amp        = n.array(re.split(",",row[16]), dtype = n.float)
        half_integ = n.array(re.split(",",row[18]), dtype = n.float)
        length     = n.array(re.split(",",row[20]), dtype = n.float)

        # Debugging the Intensity problems
        # n.set_printoptions(precision=3)
        # if i>2950 and i<2965:
            #print 'line number ', i, row[1]
            # print 'Int=', half_integ[0:10]*0.960E9
            #print 'Len=', length[0:3]*1E9
                # for a in range (0,29):
                #print a, row[a][:60]


        for j in range(nB1[0]):
            try:
                b1_bunches[j]  = bunchNum[j]
            except IndexError:
                print 'Warning: out of range... but will continue'
                print 'bunchNum', bunchNum

                for a in range (0,29):
                    print a, row[a][:40]
                return

            b1_time_zc[j]  = time_zc[j]
            b1_amp[j]      = amp[j]
            if nB1[0]!=0 and nB2[0]!=0:
                b1_half_int[j] = half_integ[j]
                b1_len[j]      = length[j]

        # now the same for B2
        bunchNum   = n.array(re.split(",",row[11]), dtype = n.int)
        time_zc    = n.array(re.split(",",row[15]), dtype = n.float)
        amp        = n.array(re.split(",",row[17]), dtype = n.float)
        half_integ = n.array(re.split(",",row[19]), dtype = n.float)
        length     = n.array(re.split(",",row[21]), dtype = n.float)

        for j in range(nB2[0]):
            try:
                b2_bunches[j]  = bunchNum[j]
            except IndexError:
                print 'Warning: out of range... but will continue'
                print 'bunchNum', bunchNum
                return
            b2_time_zc[j]  = time_zc[j]
            b2_amp[j]      = amp[j]
            if nB1[0]!=0 and nB2[0]!=0:
                b2_half_int[j] = half_integ[j]
                b2_len[j]      = length[j]



        '''Checks'''

        #if (nB1[0]==358):
        #    print b1_bunches

        '''
        if (nB1[0]==352 and nB2[0]==352):

            print "b1 po", b1_bunches[0], b1_bunches[1], b1_bunches[2]
            print "b2 po", b2_bunches[0], b2_bunches[1], b2_bunches[2]
            print "b1 zc", b1_time_zc[0], b1_time_zc[1], b1_time_zc[2]
            print "b2 zc", b2_time_zc[0], b2_time_zc[1], b2_time_zc[2]
            print "b1 le", b1_time_le[0], b1_time_le[1], b1_time_le[2]
            print "b2 le", b2_time_le[0], b2_time_le[1], b2_time_le[2]
        '''


        stuff.orb_len_trig = 0.0
        stuff.orb_len_1    = 0.0
        stuff.orb_1_2      = 0.0
        stuff.cog_ddly_c3_c4 = 0.0
        stuff.cog_ddly_c1_c3 = 0.0
        stuff.cog_ddly_c2_c4 = 0.0
        stuff.cog_ddly_c1_c2 = 0.0
        if nB1[0]!=0 and nB2[0]!=0:
            stuff.orb_len_trig = float(row[22])
            stuff.orb_len_1    = float(row[23])
            stuff.orb_1_2      = float(row[24])
            stuff.cog_ddly_c3_c4 = float(row[25])
            stuff.cog_ddly_c1_c3 = float(row[26])
            stuff.cog_ddly_c2_c4 = float(row[27])
            stuff.cog_ddly_c1_c2 = float(row[28])


        nCol[0]    = int(row[29])
        deltaT[0]  = float(row[30])


        bunchTree.Fill()
        i+=1

    bunchTree.Write()
    print 'Number of entries in this tree =', bunchTree.GetEntries()

    rootFile.Close()



def testPlots(mytree):

    # print beginTime, str(beginTime.Convert())
    gROOT.ProcessLine(".L     /home/andreypz/Documents/0work/tdrstyle.C")
    setTDRStyle()
    #mytree.Draw('cog_ddly_c1_c2:nB1>>hh1',"nB1==358","")
    #mytree.Draw('1e9*b1_time_zc[0]>>hh(100,10,15)',"nB1==352","")
    mytree.Draw('1e9*b2_time_zc[0]',"nB2==352","")
    #mytree.Draw('b1_bunches_zc[1]:nB1>>hh2',"nB1>1 && nB1<100","colz")
    #mytree.Draw('b2_bunches_zc[0]:nB2>>hh2',"nB2>1 && nB2<100","colz")
    #mytree.Draw('nB2>>hh1',"","")
    #mytree.Draw('nB1>>hh2',"","")
    #hh1.Draw("colz");
    #hh2.Draw("colz");
    #hh2.SetLineColor(kRed)
    #hh2.Draw("same hist");
    c1.SaveAs("h_1.png")

    gStyle.SetTimeOffset(beginTime.Convert());
    begin = str(beginTime.Convert())
    mytree.Draw('nB1:daTime-'+begin)
    gr1= TGraph(gPad.GetPrimitive("Graph"))

    mytree.Draw('nB2:daTime-'+begin)
    gr2= TGraph(gPad.GetPrimitive("Graph"))

    gr1.GetXaxis().SetTimeDisplay(1);
    gr1.GetXaxis().SetTimeFormat("%H:%M");
    gr1.GetXaxis().SetLabelSize(0.03);
    gr1.GetXaxis().SetLabelOffset(0.02);
    gr1.SetMarkerStyle(24);
    gr1.SetMarkerSize(0.2);
    gr1.SetMarkerColor(kBlue+2);
    gr2.SetMarkerColor(kRed+2);

    gr1.Draw("AP*")
    gr2.Draw("same P")
    c1.SaveAs("h_2.png")


    '''
    mytree.Draw('bb_phase_mean:daTime-'+begin)
    gr2= TGraph(gPad.GetPrimitive("Graph"))
    #gr2 = gr.Clone("gr2")
    #gr2 = TGraph(gPad.GetPrimitive("Graph").Clone())
    gr2.SetMarkerStyle(24);
    gr2.SetMarkerSize(0.2);
    gr2.SetMarkerColor(kRed+2);

    gr1.Draw("APL")
    gr2.Draw("APL")
    c1.SaveAs("h_1.png")
    '''

# Add init here

dates_to_add = [
  ["11","02"],
  ]

for month in ['']:
    for day in xrange(1,31):
        if day<10:
            a = "0"+str(day)
        else:
            a = str(day)
        dates_to_add.append([month,a])

print dates_to_add

for d in dates_to_add:
    fileName = "bptx_mon_bunches_2015_"+d[0]+"_"+d[1]+"_UTC"

    DATAPATH = '/afs/cern.ch/user/a/andrey/work/BPTXMONDATA/'
    convertToROOT(DATAPATH, fileName)

# Do hadd here
#chain.Add(path+"root/all_bunches.root")
