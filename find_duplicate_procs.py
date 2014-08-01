#!/usr/bin/python

"""
This utility file can be called as cvs commitinfo to go through the diff
and find the list of new tcl procs being committed and compare it with
the repository to detect the duplicate procs.
If duplicate proc detected, we can abort the commit.
"""
import sys, os, glob
import subprocess, re, itertools
import pdb

procToFile = dict()

def getNewProcsFromDiff(fileName, oldVer, newVer):
    """
    1- Go through each line of diff between oldVer and newVer
    2- find the list of proc in the diff and return it
    """
    p = subprocess.Popen('cvs diff -r ' + newVer + ' -r ' + oldVer + ' '\
      + changedFile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        match = re.search("> proc (\S+)", line)
        if match:
            procList =  match.groups()

    retval = p.wait()

    return procList

def getProcsFromFile(filename):
    """
    1- Go through each line in a given file.
    2- Find the list of all proc defined and return the proc list
    """
    procList = []
    for i, line in enumerate(open(filename)):
        match = re.search("^proc (\S+)", line)
        if match:
            tprocList = list(match.groups())
            for procName in tprocList:
                try:
                    procToFile[procName] = filename + " " + procToFile[procName]
                except KeyError, e:
                    procToFile[procName] = filename
            procList = procList + tprocList

    #print "file " + filename + " len " + str(len(procList))
    return procList

for arg in sys.argv[1:]:
    #print "arg is " + arg
    #changedFile, oldVer, newVer = arg.split(',')
    #print "changedFile is " + changedFile
    #print "oldVer is " + oldVer
    #print "newVer is " + newVer
    changedFile = arg

    procsToTest = ['SGV', 'isStringEqual']
    procsToCommit = getProcsFromFile(changedFile)
    existingProcs = getProcsFromRepo()
    #print str(procsToCommit) + "END+++"
    #print str(existingProcs) + "END+++"

    #for newProc in procsToTest:
    for newProc in procsToCommit:
        print "newPorc " + newProc
        if newProc in existingProcs:
            print "duplicate proc detected for " + newProc + " in " + str(procToFile[newProc])
            failFlag = 1
