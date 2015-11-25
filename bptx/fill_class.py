from  ROOT import TDatime
import calendar

class LHCFills():
    def __init__(self, fill, begin= TDatime(), stable=TDatime(), end=TDatime()):
        self._fill   = fill
        self._begin  = begin
        self._stable = stable
        self._end    = end

        #Times in the dict below are approximate, to make the plots look better
        self._fillTimeDict = {
            # 0 - begin plot time
            # 1 - stable beams
            # 2 - end stable

            # Note: not all the Fills are in this list!

        '4634':
        [
        TDatime(2015,11,19, 8,00,00), 
        TDatime(2015,11,19,14,40,00), 
        TDatime(2015,11,20, 6,20,00)
        ],

        '4569':
        [
        TDatime(2015,11,2,16,40,00), 
        TDatime(2015,11,2,19,05,00), 
        TDatime(2015,11,3, 6,25,00)
        ],

        '4565':
        [
        TDatime(2015,11,2,7,30,00), 
        TDatime(2015,11,2,8,40,00), 
        TDatime(2015,11,2,10,55,00)
        ],

        '4463':
        [
        TDatime(2015,10,5,19,00,00), 
        TDatime(2015,10,5,20,13,00), 
        TDatime(2015,10,6,00,20,00)
        ],


        '4384':
        [
        TDatime(2015,9,17,18,00,00), 
        #TDatime(2015,9,17,20,00,00), 
        TDatime(2015,9,17,20,20,00), 
        TDatime(2015,9,18,10,20,00)
        ],

        '4381':
        [
        TDatime(2015,9,16,23,00,00), 
        TDatime(2015,9,17, 1,45,00), 
        TDatime(2015,9,17,13,15,00)
        ],


        '4269':
        [
        TDatime(2015,8,25,12,00,00), 
        TDatime(2015,8,25,14,30,00), 
        TDatime(2015,8,26, 3,36,00)
        ],

        '4266':
        [
        TDatime(2015,8,24,20,00,00), 
        TDatime(2015,8,24,21,05,00), 
        TDatime(2015,8,25, 7,00,00)
        ],

        '3858':
        [
        TDatime(2015,6,14,06,00,00), 
        TDatime(2015,6,14,06,35,00), 
        TDatime(2015,6,14,15,25,00)
        ],

        '3857':
        [
        TDatime(2015,6,13,16,00,00), 
        TDatime(2015,6,13,17,12,00), 
        TDatime(2015,6,14,04,00,00)
        ],

        '3855':
        [
        TDatime(2015,6,12,19,40,00), 
        TDatime(2015,6,12,20,18,00), 
        TDatime(2015,6,13,10,22,00)
        ],

        '3851':
        [
        TDatime(2015,6,11,02,00,00), 
        TDatime(2015,6,11,03,00,00), 
        TDatime(2015,6,11,14,10,00)
        ],


        '3474':
        [
        TDatime(2013,1,20,13,00,00), 
        TDatime(2013,1,20,14,10,00), 
        TDatime(2013,1,20,16,05,00)
        ],


        '3478':
        [
        TDatime(2013,1,20,23,00,00), 
        TDatime(2013,1,21,00,50,00), 
        TDatime(2013,1,21,03,05,00)
        ],


        '3378':
        [
        TDatime(2012,12,5,21,30,00), 
        TDatime(2012,12,5,22,00,00), 
        TDatime(2012,12,6,00,30,00)
        ],
        '3047':
        [
        TDatime(2012,9,9,14,50,00), 
        TDatime(2012,9,9,17,30,00), 
        TDatime(2012,9,10,04,00,00)
        ],

        '3053':
        [
        TDatime(2012,9,10,14,30,00), 
        TDatime(2012,9,10,15,00,00), 
        TDatime(2012,9,10,20,50,00)
        ],
        '3054':
        [
        TDatime(2012,9,10,21,00,00), 
        TDatime(2012,9,11,10,00,00), 
        TDatime(2012,9,11,13,15,00)
        ],

        '2872':
        [
        TDatime(2012,07,23,19,00,00), 
        TDatime(2012,07,23,20,15,00), 
        TDatime(2012,07,24,8,10,00)
        ],

        '2871':
        [
        TDatime(2012,07,22,9,00,00), 
        TDatime(2012,07,22,9,50,00), 
        TDatime(2012,07,22,14,45,00)
        ],

        '2825':
        [
        TDatime(2012,07,10,02,10,00), 
        TDatime(2012,07,10,02,30,00), 
        TDatime(2012,07,10,02,45,00)
        ],

        '2824':
        [
        TDatime(2012,07,10,05,00,00), 
        TDatime(2012,07,10,05,10,00), 
        TDatime(2012,07,10,05,35,00)
        ],

        '2798':
        [
        TDatime(2012,07,02,17,00,00), 
        TDatime(2012,07,02,17,25,00), 
        TDatime(2012,07,02,18,00,00)
        ],

        '2739':
        [
        TDatime(2012,06,18,8,00,00), 
        TDatime(2012,06,18,8,30,00), 
        TDatime(2012,06,18,11,00,00)
        ],
        '2723':
        [
        TDatime(2012,06,11,12,00,00), 
        TDatime(2012,06,11,12,35,00), 
        TDatime(2012,06,11,15,00,00)
        ],
        '2718':
        [
        TDatime(2012,06,10,06,30,00), 
        TDatime(2012,06,10,06,51,00), 
        TDatime(2012,06,10,21,40,00)
        ],

        '2698':
        [
        TDatime(2012,06,04,17,00,00), 
        TDatime(2012,06,04,17,30,00), 
        TDatime(2012,06,04,22,25,00)
        ],
        '2692':
        [
        TDatime(2012,06,02,05,00,00), 
        TDatime(2012,06,02,05,15,00), 
        TDatime(2012,06,03,03,50,00)
        ],

        '2635':
        [
        TDatime(2012,05,17,04,00,00), 
        TDatime(2012,05,17,04,50,00), 
        TDatime(2012,05,17,9,55,00)
        ],

        '2634':
        [
        TDatime(2012,05,17,01,00,00), 
        TDatime(2012,05,17,01,17,00), 
        TDatime(2012,05,17,02,38,00)
        ],

        '2632':
        [
        TDatime(2012,05,16,18,00,00), 
        TDatime(2012,05,16,18,55,00), 
        TDatime(2012,05,16,19,03,00)
        ],

        '2634':
        [
        TDatime(2012,05,17,01,00,00), 
        TDatime(2012,05,17,01,17,00), 
        TDatime(2012,05,17,02,38,00)
        ],

        '2630':
        [
        TDatime(2012,05,15,20,00,00), 
        TDatime(2012,05,15,21,00,00), 
        TDatime(2012,05,16,01,05,00)
        ],

        '2629':
        [
        TDatime(2012,05,15,12,00,00), 
        TDatime(2012,05,15,12,30,00), 
        TDatime(2012,05,15,18,20,00)
        ],

        '2616':
        [
        TDatime(2012,05,11,11,00,00), 
        TDatime(2012,05,11,12,05,00), 
        TDatime(2012,05,11,13,55,00)
        ],

        '2609':
        [
        TDatime(2012,05,10,18,00,00), 
        TDatime(2012,05,10,18,41,00), 
        TDatime(2012,05,10,23,00,00)
        ],

        '2608':
        [
        TDatime(2012,05,10,15,00,00), 
        TDatime(2012,05,10,15,36,00), 
        TDatime(2012,05,10,16,05,00)
        ],





        '2534':
        [
        TDatime(2012,04,19,3,00,00), 
        TDatime(2012,04,19,3,55,00), 
        TDatime(2012,04,19,8,05,00)
        ],

        '2523':
        [
        TDatime(2012,04,17,04,00,00), 
        TDatime(2012,04,17,04,25,00), 
        TDatime(2012,04,17,11,20,00)
        ],

        '2493':
        [
        TDatime(2012,04,9,07,00,00), 
        TDatime(2012,04,9,8,35,00), 
        TDatime(2012,04,9,14,50,00)
        ],
            
        
        '2491':
        [
        TDatime(2012,04,8,15,30,00), 
        TDatime(2012,04,8,16,25,00), 
        TDatime(2012,04,9,02,35,00)
        ],
        

        '2490':
        [
        TDatime(2012,04,8,11,00,00), 
        TDatime(2012,04,8,12,55,00), 
        TDatime(2012,04,8,14,10,00)
        ],

        '2489':
        [
        TDatime(2012,04,8,04,30,00), 
        TDatime(2012,04,8,05,15,00), 
        TDatime(2012,04,8,9,30,00)
        ],

        '2488':
        [
        TDatime(2012,04,07,22,00,00), 
        TDatime(2012,04,07,22,50,00), 
        TDatime(2012,04,8,03,00,00)
        ],

        '2486':
        [
        TDatime(2012,04,07,16,00,00), 
        TDatime(2012,04,07,17,20,00), 
        TDatime(2012,04,07,18,45,00)
        ],
        
        '2482':
        [
        TDatime(2012,04,06,22,00,00), 
        TDatime(2012,04,07,0,05,00), 
        TDatime(2012,04,07,03,35,00)
        ],

        '2479':
        [
        TDatime(2012,04,06,11,00,00), 
        TDatime(2012,04,06,12,55,00), 
        TDatime(2012,04,06,15,50,00)
        ],
        
        '2472':
        [
        TDatime(2012,04,05,16,30,00), 
        TDatime(2012,04,05,17,55,00), 
        TDatime(2012,04,05,22,15,00)
        ],

        '2471':
        [
        TDatime(2012,04,05,12,30,00), 
        TDatime(2012,04,05,13,30,00), 
        TDatime(2012,04,05,15,45,00)
        ],

        '2470':
        [
        TDatime(2012,04,05,03,10,00), 
        TDatime(2012,04,05,03,40,00), 
        TDatime(2012,04,05,07,40,00)
        ],

        '2469':
        [
        TDatime(2012,04,04,22,10,00), 
        TDatime(2012,04,04,22,40,00), 
        TDatime(2012,04,05,00,10,00)
        ],


        #Below are the Fills from HI data 2011

        '2318':
        [
        TDatime(2011,11,23,20,10,00), #0 begin plot time
        TDatime(2011,11,23,21,00,00), #1 stable beams
        TDatime(2011,11,24,2,30,00)   #2 end
        ],
        '2319':
        [
        TDatime(2011,11,24,8,00,00),
        TDatime(2011,11,24,8,10,00),
        TDatime(2011,11,24,17,00,00)
        ],
        '2320':
        [
        TDatime(2011,11,24,21,45,00),
        TDatime(2011,11,24,21,45,00),
        TDatime(2011,11,25,3,10,00)
        ],
        '2332':
        [
        TDatime(2011,11,28,17,45,00),
        TDatime(2011,11,28,18,15,00),
        TDatime(2011,11,28,19,20,00)
        ],
        '2334':
        [
        TDatime(2011,12,01,3,00,00),
        TDatime(2011,12,01,4,00,00),
        TDatime(2011,12,01,9,40,00)
        ],
        '2335':
        [
        TDatime(2011,12,01,13,00,00),
        TDatime(2011,12,01,14,35,00),
        TDatime(2011,12,01,20,10,00)
        ],
        '2336':
        [
        TDatime(2011,12,02, 2,00,00),
        TDatime(2011,12,02, 3,20,00),
        TDatime(2011,12,02, 9,30,00)
        ],
        '2337':
        [
        TDatime(2011,12,02, 11,30,00),
        TDatime(2011,12,02, 12,20,00),
        TDatime(2011,12,02, 16,30,00)
        ],
        '2338':
        [
        TDatime(2011,12,02, 22,30,00),
        TDatime(2011,12,02, 23,30,00),
        TDatime(2011,12,03, 07,05,00)
        ],
        '2339':
        [
        TDatime(2011,12,03, 12,00,00),
        TDatime(2011,12,03, 13,10,00),
        TDatime(2011,12,03, 19,00,00)
        ],
        '2340':
        [
        TDatime(2011,12,03, 21,00,00),
        TDatime(2011,12,03, 22,00,00),
        TDatime(2011,12,04, 05,00,00)
        ],
        '2341':
        [
        TDatime(2011,12,04, 10,10,00),
        TDatime(2011,12,04, 10,50,00),
        TDatime(2011,12,04, 13,55,00)
        ],
        '2342':
        [
        TDatime(2011,12,04, 16,40,00),
        TDatime(2011,12,04, 17,30,00),
        TDatime(2011,12,04, 22,55,00)
        ],
        '2343':
        [
        TDatime(2011,12,05, 1,30,00),
        TDatime(2011,12,05, 2,20,00),
        TDatime(2011,12,05, 8,35,00)
        ],
        '2344':
        [
        TDatime(2011,12,05, 21,00,00),
        TDatime(2011,12,05, 21,55,00),
        TDatime(2011,12,06, 4,55,00)
        ],
        '2349':
        [
        TDatime(2011,12,06, 19,20,00),
        TDatime(2011,12,06, 20,05,00),
        TDatime(2011,12,06, 21,35,00)
        ]
    }    
    def Fill(self):
        return self._fill
    
    def Begin(self):
        if str(self._fill) in self._fillTimeDict:
            return self._fillTimeDict[str(self._fill)][0]
        else:
            return self._begin

    def Stable(self):
        if str(self._fill) in self._fillTimeDict:
            return self._fillTimeDict[str(self._fill)][1]
        else:
            return self._stable
    def End(self):
        if str(self._fill) in self._fillTimeDict:
            return self._fillTimeDict[str(self._fill)][2]
        else:
            return self._end

    def Title(self):
        plotTitle = ';'
        
        if str(self._fill) in self._fillTimeDict:
            year  = self._fillTimeDict[str(self._fill)][1].GetYear()
            month = self._fillTimeDict[str(self._fill)][1].GetMonth()
            day1  = self._fillTimeDict[str(self._fill)][1].GetDay()
            day2  = self._fillTimeDict[str(self._fill)][2].GetDay()
            day = str(day1)
            if day1!=day2:
                day = str(day1)+'-'+str(day2)

            mon = calendar.month_abbr[month]
            plotTitle = 'Fill '+ str(self._fill)  +', '+day+' '+ mon+ ' ' + str(year)+';'
        return plotTitle    
