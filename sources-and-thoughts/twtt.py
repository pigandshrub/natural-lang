# Last name: Cheung
# First Name: Daphne


# We want this program to take at least two command line arguments:  the raw tweet 
# files and the output file.
import sys

# To locate html tags and attributes.
import re
import HTMLParser

# To tag tokens.
import NLPlib


# Helper functions

# Mark off each individual tweet
def markIndividualTweets(mod):
    ind = r'[\n]'
    mod = re.sub(ind, '|', mod)
    return mod

# Function to replace Html character codes with an ASCII equivalent.
# We account for occurrence of &amp;amp; and &amp;quot; by using
# regex for one or more occurrences of amp; and handling all &amp;s
# before handling &quot;s.
def htmlTagRemover(mod):
    html = r'<[^>^<]+>'
    mod = re.sub(html,'', mod)
    
    amp = r'&(amp;)+'
    mod = re.sub(amp, '&', mod)
    
    quot = r'&quot;'
    mod = re.sub(quot, '"', mod)
    
    # Check for any other html codes.
    h = HTMLParser.HTMLParser()
    oth = re.findall(r'&#?\w+;', mod)
    for code in oth:
        mod = mod.replace(code, h.unescape(code))    
    return mod


# Remove website links.
def httpWebsiteRemover(mod):
    # Remove http website addresses
    http = r'http[^\s]+'
    mod = re.sub(http, '', mod)
    # Remove www website addresses
    www = r'www[^\s]+'
    mod = re.sub(www, '', mod)
    # Remove other possible websites
    oth = r'[\w]+\.\w\w+[\.\w+]*[//\w+]*'
    mod = re.sub(oth, '', mod)
    return mod


# Remove @ from twitter accounts and # from hashtags
def twitHashRemover(mod):
    twa = re.findall(r'@[\w]+', mod)
    for t in twa:
        mod = mod.replace(t, t.replace('@', ''))

    htag = re.findall(r'#[\w]+', mod) 
    for h in htag:
        mod = mod.replace(h, h.replace('#', ''))
    return mod
        

# Put each sentence in a given string on its own line.
# Please note the abbrev.txt and pn_abbrev.txt files have 
# been modified and are not the original files.  The location
# of these modified files have been hardcoded in this function. 
# THe files are located in the same directory as the twtt.py file.
def separateSentences(mod):
    #Place common abbreviations into a list
    abbrev = []
    f1 = file('./abbrev.english', 'r')
    for word in f1:
        abbrev.append(word.strip())
    f1.close()       
    
    pn_abbrev=[]
    f2 = file('./pn_abbrev.english', 'r')
    for word in f2:
        pn_abbrev.append(word.strip())
    f2.close()

    # Consider all occurrences of . ? !
    # which are followed by spaces and then a capital letter
    s1 = re.findall(r'([\w\.]+[\.\?\!\"]+)', mod)
    for end in s1:
        if (end not in abbrev) and (end not in pn_abbrev):
            mod = mod.replace(end, end + '\n')
    
    # Locate end quotation marks and swap position with neighbouring
    # punctuation.
    s2 = re.findall(r'([\.\?\!]+\")', mod)
    for end in s2:
        mod = mod.replace(end, '"' + end.replace('"','\n'))
    
    return mod


# Separate each token, including punctuation and clitics, by spaces.
def tokenSeparate(mod):
    #Place common abbreviations into a list
    abbrev = []
    f1 = file('./abbrev.english', 'r')
    for word in f1:
        abbrev.append(word.strip())
    f1.close()       
    
    pn_abbrev=[]
    f2 = file('./pn_abbrev.english', 'r')
    for word in f2:
        pn_abbrev.append(word.strip())
    f2.close()

    # Identify 'm, 've, 're, 's and similar as a token
    t1 = re.findall(r'(\'[a-z]+|\'\s)', mod)
    for tok in t1:
        mod = mod.replace(tok, ' ' + tok)

    # Group back and separate n't 
    t2 = re.findall(r'(n\s\'t)', mod)
    for tok in t2:
        mod = mod.replace(tok, " n\'t") 
        

    # Separate standard punctuations
    t3 = re.finditer(r'([\w\.]+)([\.\?\,\!\:\;]+)', mod)
    for match in t3:
        if (match.group() not in abbrev) and (match.group() not in pn_abbrev):
            mod = mod.replace(match.group(), match.group(1) + ' ' + match.group(2)\
                              + ' ') 

    # Separate quotation, dollars,  marks
    t4 = re.findall(r'([\"\(\)]+)', mod)
    for tok in t4:
        mod = mod.replace(tok, ' ' + tok + ' ')

    # Separate am and pm for time
    t5 = re.findall(r'[0-9]([ap]+m)', mod)
    for tok in t5:
        mod = mod.replace(tok, ' ' + tok + ' ')

    return mod


# Function to tag each token with its part-of-speech
# to output to twtt.py
def tagIt(mod, tagger):
    s = ''
    L = []
    # Tokenize
    mod = re.split(r'\s+', mod)
    
    # Remove excess white space from list of tokens
    for i in range(len(mod)):
        if (mod[i] != ''):
            L.append(mod[i].strip())
    
    tags = tagger.tag(L)  
    
    # Insert new line to distinguish between 
    # new tagged sentences and individual tweets.
    for i in range(0,len(tags)):
        if (i > 0) and (tags[i-1] == '.') and (L[i]== '|'):
            s += L[i] + '\n'
        elif (i > 0) and (tags[i-1] != '.') and (L[i] == '|'):
            s += '\n' + L[i] + '\n'
        elif (tags[i] == '.'):
            s += L[i] + '/' + tags[i] + '\n'
        else:
            s += L[i] + '/' + tags[i] + ' '
    return s



# This is the main code.  The helper functions for this code are given above.
if (len(sys.argv) < 3 ):
    print ('Err: Must have 3 args. python twtt.py input_file output_file')

else:
    
    out = file(sys.argv[2], 'w')        
    inp = file(sys.argv[1], 'r')
        
    tagger = NLPlib.NLPlib()

    for line in inp:
        mod0 = markIndividualTweets(line)
        mod1 = htmlTagRemover(mod0)
        mod2 = httpWebsiteRemover(mod1)
        mod3 = twitHashRemover(mod2)
        mod4 = separateSentences(mod3)  
        mod5 = tokenSeparate(mod4)
        mod6 = tagIt(mod5, tagger)
        out.write(mod6)
        
    inp.close()
    out.close()


#if __name__ == "__main__":
    