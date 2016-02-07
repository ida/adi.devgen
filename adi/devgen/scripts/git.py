from os import system as sis

from adi.commons.commons import addFile
from adi.commons.commons import appendToFile
from adi.commons.commons import delFile
from adi.commons.commons import fileExists
from adi.commons.commons import getStr
from adi.commons.commons import getFirstChildrenDirPaths

def checkForDiffs(path):
    """
    For each first-child-dir of path perform a git-diff
    and collect the diffs in a reportfile.
    Directories not containing a '.git'-dir are ignored.
    """
    fil = 'git-diff-report.txt'
    tmp = fil + '.tmp'
    sh = 'sh.sh'
    exe_prefix = ''
    DIFFS = False
    if not path.endswith('/'): path += '/'
    if path.startswith('./'): path = path[2:]
    if fileExists(fil): delFile(fil)
    paths = getFirstChildrenDirPaths(path)
    for p in paths:
        if path == './': path = ''
        p = path + p
        if fileExists(p + '/.git'):
            addFile( p + sh, 'cd ' + p + '; git diff >> ' + tmp + '; cd ..')
            sis('chmod +x ' + p + sh)
            sis('./' + p + sh)
            if getStr(p + tmp) != '':
                DIFFS = True
                appendToFile(fil, '" GIT-DIFF OF ' + p[:-1] + '\n'
                                      + getStr(p + tmp) + '\n')
            delFile(p + sh)
            delFile(p + tmp)
    if DIFFS:
        print "There are diffs, check './" + fil + ' for a full report.'

