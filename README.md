# My BRIL scripts


## bptx
These are the scripts to analyze the datta from scope monitoring.

There are two steps in analyzing this data. The files called ```makeTree_bunches.pyy``` and ```makeTree_timing.py```
take the original .txt files as inputs and produce the .root files with TTree objects inside.

The scripts stariting with ```plot_``` run over theose root trees and make the plts.
The data files are available on lxplus at */afs/cern.ch/user/a/andrey/work*

In the scripts this path needs to be provided. Try to run eg the bunches script: ```./plot_bunches.py 4266``` 

