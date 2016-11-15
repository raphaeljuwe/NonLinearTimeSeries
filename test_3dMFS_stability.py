
from imfractal import *

from pylab import *

import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'imfractal', 'imfractal',  "Algorithm"))

import qs3D

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def do_test(_path, N, total_pixels):

    print "PATH: " + _path
    print "NUM_TRIALS: ", N
    print "TOTAL_PIXELS: ", total_pixels

    patients = ["32"]
    scans = ["1"]
    # amount of volumes of interest
    vois = 1
    dims = 10

    # BioAsset bone's multifractal spectra database
    mfss = np.zeros([len(patients),len(scans),vois,2*dims+1])

    aux = CSandbox3D(dims)

    params = {
        "zero": 1,
        "one": 0.75,
        "two": 3.7,
        "three": 1,
        "four": 15,
        "five": 0,
        "mask_filename": '',
        "seven": "no",
        "eight": 'S',
        "nine": 'M',
        "threshold": 200,
        "total_pixels": total_pixels
    }

    fmask = _path + "BA" + patients[0] + "_120_" + scans[0] + "Mask.mat"

    params["five"] = 0
    params["mask_filename"] = fmask

    aux.setDef(40, 1.02, True, params)

    slice_filename = _path + "BA" + patients[0] + "_120_" + scans[0] + "Slices.mat"

    print fmask
    print slice_filename

    if N > 1 :
        print "Repeating", N, " times"

        mfss = np.array(aux.getFDs(slice_filename)).astype(np.double)
        for i in range(1, int(N)):
            print "Computing ", i+1, " th time"
            mfss = np.vstack((mfss, aux.getFDs(slice_filename)))

        # show variations
        print ""
        print "Variation by dimension: in red is higher than 0.01 "
        for j in range(0, mfss.shape[1]):
            #print np.std(mfss[:, j]), " j: ", j # mmhh

            diff = max(mfss[:, j]) - min(mfss[:, j])
            diff_str = str(diff)
            dim = str(j-dims)
            msg = diff_str + " q: " + dim
            if diff > 0.01 :
                print bcolors.FAIL + msg + bcolors.ENDC
            else:
                print msg
    else:
        print "3D MFS should be computed more than once to show variations"


    
