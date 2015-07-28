# The imparative convention: Let paths always end with a slash!

import os
import re
import shutil
import glob

#########
# FILES #
#########

def addFile(path, string='', OVERWRITE=False):
    if fileExists(path) and not OVERWRITE:
        exit("File %s exists already, skipping its creation."%path)
    else:
        with open(path, 'w') as fil:
            fil.write(string)

def addDirs(path):
    os.makedirs(path)

def delFile(path):
    os.remove(path)

def delDirs(path):
    shutil.rmtree(path)

def fileExists(path):
    if os.path.exists(path): return True
    else: return False

def getFirstChildrenDirPaths(path):
    return glob.glob(path + '*/')

def getFirstChildrenPaths(path):
    return glob.glob(path + '*')

def getRealPath(path):
    return os.path.realpath(path) + '/'

def getParentDirPath(path):
    path = os.path.realpath(path)
    parent_path = '/'.join((path.split('/')[:-1])) + '/'
    return parent_path

def readFile(path):
    fil = open(path)
    string = fil.read()
    fil.close()    
    return string

def fileHasStr(path, pattern):
    str = readFile(path)
    return hasStr(str, pattern)

########
# STRS #
########

def extractUrlsOfStr(string):
    """ Returns everything starting with 'http' and
        ending with a whitespace or '>', as a list.
    """

    # Looks for starting with 'http' and ends with space or linebreak:
    urls = re.findall('(http\S+)', string)

    # If urls end with '>', strip trailing garbage:
    trimmed_urls=[]
    for url in urls:
        url = url.split('>')[0]
        trimmed_urls.append(url)

    return trimmed_urls

def getLines(path):
    with open(path) as fil:
        lines = fil.readlines()
    return lines

def getIndent(line):
    indent = ''
    for char in line:
        if char == ' ':
            indent += char
        else:
            break
    return indent

def hasStr(str, pattern):
    if str.find(pattern) != -1: return True
    else: return False

def insertAfterLine(path, pattern, string, PRESERVE_INDENT=True):
    FOUND = False
    tmp_path = path + '.tmp'
    if not string.endswith('\n'):
        string + '\n'
    with open(path) as fin, open(tmp_path, 'w') as fout:
        for line in fin:
            if line.find(pattern) != -1:
                if PRESERVE_INDENT:
                    string = getIndent(line) + string
                FOUND = True
            fout.write(line)
            if FOUND:
                fout.write(string)
                FOUND = False
    shutil.move(tmp_path, path)

def insertBeforeLine(path, pattern, string):
    digest = ''
    indent = ''
    for line in getLines(path):
        if line.find(pattern) > -1:
            digest += indent + string
        digest += line
        if line != '\n':
            indent = getIndent(line)    
    addFile(path, digest, OVERWRITE=True)

def insertAfterFirstLine(path, string, PRESERVE_INDENT=True):
    digest = ''
    lines = open(path).readlines()
    FIRSTLINE_PASSED = False
    for line in lines:
        digest += line
        if not FIRSTLINE_PASSED:
            if PRESERVE_INDENT:
                string = getIndent(line) + string
            digest += string
            FIRSTLINE_PASSED = True
    addFile(path, digest, OVERWRITE=True)

def insertBeforeLastTag(path, string):
    tag_start_pos = 0
    digest = ''
    IN_TAG = False
    food = readFile(path)
    lenn = len(food) - 1
    pos = lenn
    while pos > 0:
        char = food[pos]
        if char == '>':
            IN_TAG = True
        if char == '<' and IN_TAG:
            tag_start_pos = pos
            break
        pos -= 1
    digest = food[0:tag_start_pos] + string + food[tag_start_pos:lenn+1]
    addFile(path, digest, OVERWRITE=True)

def replaceWords(words, string):
    """ Replace words, as defined in the passed 'words'-dict. Shamelessly stolen of:
        http://stackoverflow.com/questions/14028581/regex-how-to-replace-a-word-in-a-string-with-its-entry-in-a-python-dictionary#14030464
        Thanks to Ned Batchelder.
    """
    pat = re.compile(r"\b(%s)\b" % "|".join(words))
    new_string = pat.sub(lambda m: words.get(m.group()), string)
    return new_string

def removeHtmlComments(string):
    new_string = ''
    COMMENT = False
    pos = 0
    while pos < len(string):
        char = string[pos]
        if char == '<' and string[pos+1] == '!' and string[pos+2] == '-' and string[pos+3] == '-':
            COMMENT = True
            pos += 4
            char = string[pos]
        if char == '-' and COMMENT and string[pos+1] == '-' and string[pos+2] == '>':
            COMMENT = False
            pos += 2
            if(len(string) > pos+1):
                pos += 1
            else:
                break # str ends with last char of comment
            char = string[pos]
        if not COMMENT:
            new_string += char
        pos += 1
    return new_string

