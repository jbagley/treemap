#! /usr/local/bin/python

import os
import re
import shlex
import subprocess
import sys

bugRegEx = re.compile(r'(9[0-9]{3}|1[0-9]{4})')

# Track which subdirectories have been created
parents = []

def AddCountsForFile(filePath, counts):
    '''Count bugs associated with filePath and return as list with the filename, parent, line count and bug count

       filePath - the path to the file in the repo, appended to svnURL.

    '''
    global bugRegEx
    global parents

    command = 'svn log %s' % filePath

    components=filePath.split('/')
    numComponents = len(components)
    name = components[numComponents - 1]
    root = ''
    if numComponents > 1:
        root = components[numComponents - 2]
        if root == '.':
            root = 'root'
        if not root in parents:
            parents.append(root)
            parent = 'root'
            if root == 'root':
                parent = None
            counts.append([root, parent, 0, 0])

    # Look for bug numbers 9xxx or 1xxxx, i.e. integers higher than 8999
    bugs = []
    logProc = subprocess.Popen(shlex.split(command),stdout=subprocess.PIPE)
    for line in iter(logProc.stdout.readline,''):
        bugs += bugRegEx.findall(line)
 
    try:
        lineCount = int(subprocess.check_output('wc -l ' + filePath, shell=True).lstrip().split(' ')[0])
    except ValueError as e:
        print >> sys.stderr, filePath, e
        raise

    name = os.path.basename(filePath)
    # Converting list to set removes duplicates
    bugCount = len(set(bugs))

    counts.append([name, root, lineCount, bugCount])
    return counts


def CountBugs(repositoryPath):
    '''Return list containing a list for each .cpp and .h file in repositoryPath. 
       The sublist contains the filename followed by the bug count.

    '''
    # Change into the repository so find returns relative paths
    prevPath = os.getcwd()
    os.chdir(repositoryPath)
    
    counts = [['File', 'Parent', 'Line Count', 'Bug Count']]

    # Shell out a find command to get files to process
    command = '/usr/bin/find . -depth 1 -name *.h -or -name *.cpp'
    findProc = subprocess.Popen(shlex.split(command),stdout=subprocess.PIPE)
    for filePath in iter(findProc.stdout.readline,''):
        counts = AddCountsForFile(filePath.rstrip(), counts)

    os.chdir(prevPath)

    return counts
    
path = sys.argv[1]
#print CountBugsForFile(path + '/Screens/AboutScreen.cpp')
print CountBugs(path)
