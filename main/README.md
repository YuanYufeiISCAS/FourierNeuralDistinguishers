## Description

This is the source code for implementing the paper `Fourier Analysis of Nerual Distinguishers`.



├─anonymous_submission
│
└─source_code
    │  README.md
    │
    ├─core `(The main code to reproduce our results)`
    │  │  FourierAlg.ipynb
    │  │  net.py
    │  │  net8_small.h5
    │  │  speck.py
    │  │
    │  ├─backup
    │  │
    │  └─data_Fourier
    │       
    └─example `(The example in CNF)`
            cnf.py



- source_code/core/FourierAlg.ipynb:

This file implement our Algorithm 1, which will take the nerual network (net8_small.h5 here) as input. And it will generate a backup file in core/backup, which is uesed to recovery the program. The results will output in core/data_Fourier

dependencies:

Tensorflow 2.10

Jupyter Lab 4.2.2



- source_code/example/cnf.py

We present a didactic implementation, which serves as a simplified example of the core code. A key modification in this version is the input mechanism; rather than processing a neural network, it operates on a predefined, hard-coded CNF Boolean function. This implementation is specifically designed to illustrate the case study detailed in our rebuttal.

dependency:

numpy 2.3.0



