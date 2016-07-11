# The imparative convention: Let directory-paths always end with a slash!
# Reason: Less typing and have an immediate distinction of files.

import os
import re
import shutil
import glob

#########
# PATHS #
#########

def getHome():
    home = os.path.expanduser("~") + '/'
    return home

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

#########
# FILES #
#########

def addFile(path, string='', OVERWRITE=False):
    """
    If file exists already, don't do nothing and fail silently,
    unless OVERWRITE is True, then overwrite file with string.
    """
    if not fileExists(path) or OVERWRITE:
        addDirs( '/'.join( path.split('/')[:-1] ) )
        with open(path, 'w') as fil:
            fil.write(string)

def addDirs(path):
    if not fileExists(path): os.makedirs(path)

def delFile(path):
    """Fail silently, if file to remove doesn't exist."""
    if not fileExists(path): os.remove(path)

def delDirs(path):
    shutil.rmtree(path)

def fileExists(path):
    return os.path.exists(path)

def getStr(path):
    with open(path) as fil: string = fil.read()
    return string

def getLines(path):
    with open(path) as fil: lines = fil.readlines()
    return lines

def fileHasStr(path, pattern):
    str = getStr(path)
    return hasStr(str, pattern)

def writeFile(path, string):
    with open(path, 'w') as fil:
        fil.write(string)

def appendToFile(path, string):
    if fileExists(path):
        text = getStr(path)
        text += string
    else:
        text = string
    writeFile(path, text)

def prependToFile(path, string):
    if fileExists(path):
        text = getStr(path)
        text = string + text
    else:
        text = string
    writeFile(path, text)

########
# STRS #
########

def getIndent(string):
    indent = ''
    for char in string:
        if char == ' ':
            indent += char
        else:
            break
    return indent

def getUrls(string):
    """ Returns everything starting with 'http://' or 'https://' and
        ending with a whitespace or '>', as a list.
    """

    # Looks for starting with 'http://' or 'https://' and ends with space or linebreak:
    urls = re.findall('(https:\/\/\S+)', string)
    urls += re.findall('(http:\/\/\S+)', string)

    # If urls end with '>', strip trailing garbage:
    trimmed_urls=[]
    for url in urls:
        url = url.split('>')[0]
        trimmed_urls.append(url)

    return trimmed_urls

def hasStr(string, pattern):
    if string.find(pattern) != -1: return True
    else: return False

def insertAfterLine(path, pattern, string, KEEP_INDENT=True):
    nuline = None
    digest = ''
    indent = ''
    for line in getLines(path):
        if line.find(pattern) > -1:
            nuline = string
        digest += line
        if KEEP_INDENT and line != '\n':
            indent = getIndent(line)    
        if nuline: digest+= indent + nuline; nuline = None
    addFile(path, digest, OVERWRITE=True)

def insertAfterNthLine(path, string, n, KEEP_INDENT=True):
    if not string.endswith('\n'): string += '\n'
    lines = getLines(path)
    lines.insert(n, string)
    addFile(path, ''.join(lines), OVERWRITE=True)

def insertBeforeLine(path, pattern, string, KEEP_INDENT=True):
    digest = ''
    indent = ''
    for line in getLines(path):
        if line.find(pattern) > -1:
            digest += indent + string
        digest += line
        if KEEP_INDENT and line != '\n':
            indent = getIndent(line)    
    addFile(path, digest, OVERWRITE=True)

def insertAfterFirstLine(path, string, KEEP_INDENT=True):
    digest = ''
    lines = open(path).readlines()
    FIRSTLINE_PASSED = False
    for line in lines:
        digest += line
        if not FIRSTLINE_PASSED:
            if KEEP_INDENT:
                string = getIndent(line) + string
            digest += string
            FIRSTLINE_PASSED = True
    addFile(path, digest, OVERWRITE=True)

def insertBeforeLastTag(path, string):
    tag_start_pos = 0
    digest = ''
    IN_TAG = False
    food = getStr(path)
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

def iterToTags(list_, tag_type='div'):
    """Regard lists and tuples, for now."""
    list_ = str(list_)[1:-1]
    items = list_.split(',')
    html = '<div class="list">'
    for item in items:
        item = item.strip() # remove trailing spaces
        item = item[1:-1] # remove apostrophs
        html += '<div>' + item + '</div>'
    html += '</div>'
    return html

def newlinesToTags(string, tag_type='div'):
    """
    Turn linebreaks into tag-wrappers, f.e.:
    'Hi,\nwhazup?\nBye, Crow D.'
    becomes:
    '<div>Hi,</div><div>whazup?</div><div>Bye, Crow D.</div>'
    """
    html = ''
    splits = string.split('\n')
    for splitter in splits:
        html += '<' + tag_type+ '>' + splitter + '</' + tag_type + '>'
    return html

def replaceWords(words, string):
    """
Replace words, as defined in the passed 'words'-dict. Shamelessly stolen of:
http://stackoverflow.com/questions/14028581/
regex-how-to-replace-a-word-in-a-string-with-its-entry-in-a-python-dictionary
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

def removeLinesContainingPattern(file_name, pattern_str):
    """ Remove each line of a file containing the pattern."""
    string = ''
    lines = getLines(file_name)
    for line in lines:
        if line.find(pattern_str) == -1:
            string += line
    addFile(file_name, string, True)

########
# NRS  #
########

def isEven(number):
    return number % 2 == 0

def isOdd(number):
    return number % 2 != 0

