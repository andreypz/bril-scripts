#! /usr/bin/python

import sys, csv
import re
from array import *
from  ROOT import *
gROOT.SetBatch()

DATAPATH = '/scratch/bptx_data_2016/'

gROOT.ProcessLine(
"struct MyStruct {\
Float_t version;\
Int_t  status;\
Double_t scale;\
Double_t b1_offset;\
Double_t b1_gain;\
Double_t b2_offset;\
Double_t b2_gain;\
Int_t nB1;\
Int_t nB2;\
Double_t b1_phase_min;\
Double_t b1_phase_max;\
Double_t b1_phase_mean;\
Double_t b1_phase_sigma;\
Double_t b2_phase_min;\
Double_t b2_phase_max;\
Double_t b2_phase_mean;\
Double_t b2_phase_sigma;\
Double_t bb_phase_min;\
Double_t bb_phase_max;\
Double_t bb_phase_mean;\
Double_t bb_phase_sigma;\
Float_t bcmain_jitter;\
Int_t b1_flag;\
Int_t b2_flag;\
Int_t nCol;\
Int_t bMode;\
ULong64_t daTime;\
};\
TDatime beginTime(2012,05,01,21,00,00);\
" );

from ROOT import MyStruct


def convertToROOT(path, ascii_file):
    try:
      ascifilename = path+'/'+ascii_file+'.txt'
      spamReader = csv.reader(open(ascifilename, 'rb'), delimiter=' ', skipinitialspace=True)
      print "ASCI file name =", ascifilename
    except IOError:
      print 'File %s does not exist' % (ascifilename)
      return

    stuff = MyStruct()

    root_fileName = path+'/root/'+ascii_file+'.root'
    print "Creating the file: ", root_fileName
    root_file    = TFile(root_fileName,"recreate")
    timeTree = TTree("timeTree","")

    timeTree.Branch("vars1", stuff, "version/F:status/I:scale/D:b1_offset:b1_gain:b2_offset:b2_gain:nB1/I:nB2/I:\
b1_phase_min/D:b1_phase_max:b1_phase_mean:b1_phase_sigma:\
b2_phase_min/D:b2_phase_max:b2_phase_mean:b2_phase_sigma:\
bb_phase_min/D:bb_phase_max:bb_phase_mean:bb_phase_sigma:\
bcmain_jitter/F:b1_flag/I:b2_flag/I:nCol/I:bMode/I")

    timeTree.Branch("vars5",  AddressOf( stuff, 'daTime' ), "daTime/l")

    i=0
    for row in spamReader:
        # if i>500: break
        #print row
        if (row[0] == "#" or row[4]=="?"): continue
        #if i>600:   print i, [row[a] for a in [16,17,18,8,9]]

        stuff.version = float(row[0])

        # Parse date and time, save as TDatime
        date = re.split("-|T|:|U|", row[1])
        # print date
        dt = TDatime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
        stuff.daTime = dt.Convert()
        # stuff.daTime = dt.Convert(kTRUE)
        # dt.Print()

        stuff.status    = bool(int(row[2]))
        try:
            stuff.scale     = float(row[3])
        except ValueError:
            stuff.scale = 1.0
        stuff.b1_offset = float(row[4])
        stuff.b1_gain   = float(row[5])
        stuff.b2_offset = float(row[6])
        stuff.b2_gain   = float(row[7])
        stuff.nB1   = int(row[8])
        stuff.nB2   = int(row[9])

        # print "N bunches = ", stuff.nB1, stuff.nB2

        if stuff.nB1!=0:
            if row[10]!="-": stuff.b1_phase_min   = float(row[10])
            if row[11]!="-": stuff.b1_phase_max   = float(row[11])
            if row[12]!="-": stuff.b1_phase_mean  = float(row[12])
            if row[13]!="-": stuff.b1_phase_sigma = float(row[13])
        if stuff.nB2!=0:
            if row[14]!="-": stuff.b2_phase_min   = float(row[14])
            if row[15]!="-": stuff.b2_phase_max   = float(row[15])
            if row[16]!="-": stuff.b2_phase_mean  = float(row[16])
            if row[17]!="-": stuff.b2_phase_sigma = float(row[17])
        if (stuff.nB1!=0 and stuff.nB2!=0):
            if row[18]!="-": stuff.bb_phase_min   = float(row[18])
            if row[19]!="-": stuff.bb_phase_max   = float(row[19])
            if row[20]!="-": stuff.bb_phase_mean  = float(row[20])
            if row[21]!="-": stuff.bb_phase_sigma = float(row[21])

            # print 'Delta T = ', stuff.bb_phase_mean

        # if (len(row)!=22): print "len(row) = ", len(row)
        if len(row)>21:
            stuff.bcmain_jitter = float(row[22])
            stuff.b1_flag = int(row[23])
            stuff.b2_flag = int(row[24])

        if stuff.version>=4.6:
            stuff.nCol  = int(row[25])
        if stuff.version>=4.8:
            #print row[25:]
            stuff.bMode = int(row[26])
        else:
            stuff.bMode = 0

        timeTree.Fill()
        i+=1

    timeTree.Write()
    print timeTree.GetEntries()

    root_file.Close()

    return 42

if __name__ == "__main__":  

    # Format: ['month','day']
    dates_to_add = [
        ["10","23"],
        ["10","25"],
        ["10","27"],
    ]
    
    for month in xrange(3,12+1):
        for day in xrange(1,31+1):
            a = str(day).zfill(2)
            m = str(month).zfill(2)
            dates_to_add.append([m, a])
    
    print dates_to_add


    from multiprocessing import Pool, TimeoutError
    pool = Pool(processes=8)

    for d in dates_to_add:
      fileName = "bptx_mon_timing_2016_"+d[0]+"_"+d[1]+"_UTC"
      pool.apply_async(convertToROOT, args = (DATAPATH, fileName,))
      # convertToROOT(DATAPATH, fileName)

    pool.close()
    pool.join()
    
    
