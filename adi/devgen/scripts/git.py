from os import system as sis

from adi.commons.commons import addFile
from adi.commons.commons import appendToFile
from adi.commons.commons import delFile
from adi.commons.commons import fileExists
from adi.commons.commons import hasStr
from adi.commons.commons import getStr
from adi.commons.commons import getFirstChildrenDirPaths

def checkForDiffs(path, report_file='git-diff-report.txt'):
    """
    For each first-child-dir of path perform a git-diff
    and collect the diffs in a reportfile.
    Directories not containing a '.git'-dir are ignored.
    """
    tmp = report_file + '.tmp'
    sh = report_file + '.sh.tmp'
    DIFFS = False
    if not path.endswith('/'): path += '/'
    if path.startswith('./'): path = path[2:]
    if fileExists(report_file): delFile(report_file)
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
                # Nota: We insert the info about dir-name prended with 'diff ',
                # so syntaxhighlighting keeps intact for diff-files:
                appendToFile(report_file,
                             'diff of "' + p[:-1] + '":\n'
                             + getStr(p + tmp) + '\n\n')
            delFile(p + sh)
            delFile(p + tmp)
    if DIFFS:
        print "There are diffs, check './" + report_file + '" for the full report.'

def checkForUnpushedCommits(path, report_file='git-unpushed-commits.txt'):
    """
    For each first-child-dir of path perform a git-status
    and collect the filenames of files with unpushed commits
    in the report-file.
    """
    tmp = report_file + '.tmp'
    sh = report_file + '.sh.tmp'
    DIFFS = False
    if not path.endswith('/'): path += '/'
    if path.startswith('./'): path = path[2:]
    if fileExists(report_file): delFile(report_file)
    paths = getFirstChildrenDirPaths(path)
    for p in paths:
        if path == './': path = ''
        p = path + p
        if fileExists(p + '/.git'):
            addFile( p + sh, 'cd ' + p + '; git status > ' + tmp + '; cd ..')
            sis('chmod +x ' + p + sh)
            sis('./' + p + sh)
            if hasStr(getStr(p + tmp), 'Your branch is ahead of '):
                DIFFS = True
                appendToFile(report_file, '    - ' + p[:-1])
            delFile(p + sh)
            delFile(p + tmp)
    if DIFFS:
        print "There are unpushed commits in:"
        print getStr(report_file)

