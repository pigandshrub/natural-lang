# Last name: Cheung
# First Name: Daphne
# Assignment 1 Part 2

import sys
import re

# Determines if a number of tweets given in the command line.
# Returns the number of tweets given or None otherwise.
def optNumTweets(args):
    L = ["inf"]
    num = re.findall(r'-([0-9]+)', args)
    for n in num:
        L.append(int(n))
    return min(L)

# Determines if a class name was given.
# Returns tuple of class name given and a list of files to concatenate.
# If no class name given, return None.
def optclassName(arg):
    f = ''
    cl = ''
    cla = re.findall(r'[\w]+\:', arg)
    for c in cla:
        cl += re.sub(r"(\:)", '', c)
        
    fl = re.findall(r'\:[\w\.\+]*', arg)
    for c in fl:
        f += re.sub(r"(\:)", '', c)
        
    f = f.split("+")
    return (cl, f)


# Helps count the features in a given string.
# Returns the count.
def counter(s, reg):
    count = 0
    m = re.findall(reg, s)
    for it in m:
        count += 1 
    return count

# Avg length of sentence helper function
def avgLenSents(inp):
    count = 0
    sents = inp.split('/.')
    for sent in sents:
        tok = re.findall(r'(\/[A-Z]+)', sent)
        for t in tok:
            count += 1
    num = len(sents)
    return count//num

# Avg length of token helper function
def avgLenTokens(inp):
    count = 0
    num = 0
    tokens = inp.split(' ')
    for it in tokens:
        s = re.sub(r'(\/[A-Z]+)', '', it)
        count += len(s)
    num = len(tokens)
    return count//num




# Write out features to .arff file
# Input feature set list of tuples and output file and write in 
# proper format to output file. Return output file afterwards.
def writeFeatsToOut(fset, o):
    for i in range(len(fset)):
        o.write('@attribute ' + featureSet[i][0] + ' ' \
                  + featureSet[i][1] + '\n')
    return o


# Get class attribute and write in proper format to output file.
# Return output file afterwards.
def writeClassesToOut(args, o):
    s = '{'
    for i in range(1, len(args)-1):
        if (i==1) and ("-" in args[1]):
            pass
        else:
            (className, files) = optclassName(args[i])
            if className != '':
                s += className + ','
            else:
                s += args[i] + ','
    # Take off last ','
    s = s[:len(s)-1]
    s = s + '}'
    o.write('@attribute twit ' + s + '\n')
    return o


# Read one tweet and gather 20 features.
# Input list of lines and className for one tweet
# Return features as a list of integers.
def featureCollector(twt, className):
    
    # Set feature value array to zero
    # Each index in this array corresponds to the given list of
    # features in the order listed. (eg. index 0 is for
    # the number of first person pronouns, index 1 is for the number of
    # second person pronoun, etc.
    # **Feature list:**
    # 0 - First person pronouns count
    # 1 - Second person pronouns count
    # 2 - Third person pronouns count
    # 3 - Coordinating conjunctions count
    # 4 - Past-tense verbs count
    # 5 - Future-tense verbs count
    # 6 - Commas count
    # 7 - Colons and semi-colons count
    # 8 - Dashes count
    # 9 - Parentheses count
    # 10 - Ellipses count
    # 11 - Common nouns count
    # 12 - Proper nouns count
    # 13 - Adverbs count
    # 14 - wh-words count
    # 15 - Modern slang acroynms count
    # 16 - Words all in upper case (at least 2 letters long) count
    # 17 - Average length of sentences (in tokens)
    # 18 - Average length of tokens, excluding punctuation tokens (in characters) 
    # 19 - Number of sentences  
    
    # Set up list to store feature values plus class attribute
    feat = [0]*21
    
    fpp = r"\s(I|me|my|My|mine|we|We|us|our|Our|ours)\/PRP"
    # Count second person pronouns
    spp = r"\s(you|You|your|Your|yours|u|ur|urs)\/PRP"
    # Count third person pronouns
    tpp = r"\s(she|She|him|his|she|her|hers|it|its|they|them|" \
            + "His|She|Her|It|Its|They|Them|their|Their|theirs)\/PRP"
    # Coordinating conjunctions count
    cc = r"(\/CC\s)"
    # Past-tense verbs count
    ptv = r"\s([a-z]+ed|was|were|did|went)\/VBD"
    # Future-tense verbs count
    ftv = r"(\'ll|will|gonna|going\sto\s[\w]+\/VB)"
    # Commas count
    commas = r"(\/,)"
    # Colons and semi-colons count
    colons = r"(\/:|\/;)"
    # Dashes count
    dashes = r"(-)"
    # Parentheses count
    paren = r"(\/\))"
    # Ellipses count
    ellip = r"(\.\.\.)"
    # Common nouns count
    cn = r"\s([^A-Z][a-z])+\/NN"
    # Proper nouns count
    pn = r"\s[A-Z]([a-z])+\/NN"
    # Adverbs count
    adv = r"(\/RB|\/RBR|\/RBS)"
    # wh-words count
    wh = r"(\/WDT|\/WP|\/WP\$|\/WRB)"
    # Modern slang acroynms count
    slang = r"\s(smh|fwb|lmfao|lmao|lms|tbh|rofl|wtf|bff|wyd|" \
            + "lylc|brb|atm|imao|sml|btw|bw|imho|fyi|ppl|sob|" \
            + "ttyl|imo|ltr|thx|kk|omg|ttys|afn|bbs|cya|ez|f2f|" \
            + "gtr|ic|jk|k|ly|ya|nm|np|plz|ru|so|tc|tmi|ym|" \
            + "ur|u|sol)\/"
    # Words all in upper case (at least 2 letters long) count
    upper = r"\s([A-Z][A-Z])[A-Z]*\/"
    
    end = r"(\/.)"
    
    feat[0] = counter(twt, fpp)
    feat[1] = counter(twt, spp)
    feat[2] = counter(twt, tpp)
    feat[3] = counter(twt, cc)
    feat[4] = counter(twt, ptv)
    feat[5] = counter(twt, ftv)
    feat[6] = counter(twt, commas)
    feat[7] = counter(twt, colons)
    feat[8] = counter(twt, dashes)
    feat[9] = counter(twt, paren)
    feat[10] = counter(twt, ellip)
    feat[11] = counter(twt, cn)
    feat[12] = counter(twt, pn)
    feat[13] = counter(twt, adv)
    feat[14] = counter(twt, wh)
    feat[15] = counter(twt, slang)
    feat[16] = counter(twt, upper)
    feat[17] = avgLenSents(twt)
    feat[18] = avgLenTokens(twt)
    feat[19] = counter(twt, end)
    feat[20] = className

    return feat



# Helper code to write out features to .arff file.
# Input file name and class name and output file.
# Output written output file.
def featsToOut(f, className, num, out):
    inp = file(f, 'r')
    s = ''
    for line in inp:
        s += line
    # Put each tweet in the file as an element in a list
    twtList = s.split('|')   
 
    # Collect features for each tweet in the file
    # and write out to the file
    loops = min(num, len(twtList))
    for i in range(loops):
        fL = featureCollector(twtList[i], className)
        featString = ','.join(str(n) for n in fL)
        out.write(featString + '\n')
    return out


# This is the main code.  The helper functions for this code are
# given above.
# Note that to add features, you only need to update the featureSet list
# in the main code below and the featureCollector function given above.
if (len(sys.argv) < 3 ):
    print ('Err: Must have at least 3 args. python builderarff.py' \
           + ' [-numTweets] [category:] file.twt [+] [optional other ' \
           + 'files.twt] file.arff')

else:
    
    out = file(sys.argv[len(sys.argv)-1], 'w')
    # Get name of file and use that (minus the extension) as table name
    fname = re.sub(r'(.arff)', '', sys.argv[len(sys.argv)-1])
    out.write('@relation ' + fname + '\n\n')
    
    featureSet = [ \
        ('firstPersonPronouns', 'numeric'), \
        ('secondPersonPronouns', 'numeric'), \
        ('thirdPersonPronouns', 'numeric'), \
        ('coordinatingConjunctions', 'numeric'), \
        ('pastTenseVerbs', 'numeric'), \
        ('futureTenseVerbs', 'numeric'), \
        ('commas', 'numeric'), \
        ('colons', 'numeric'), \
        ('dashes', 'numeric'), \
        ('parentheses', 'numeric'), \
        ('ellipses', 'numeric'), \
        ('commas', 'numeric'), \
        ('commonNouns', 'numeric'), \
        ('properNouns', 'numeric'), \
        ('adverbs', 'numeric'), \
        ('whWords', 'numeric'), \
        ('slang', 'numeric'), \
        ('upperCaseWords', 'numeric'), \
        ('avgLengthSentences', 'numeric'), \
        ('avgLengthTokens', 'numeric'), \
        ('numSentences', 'numeric')]
    
    out = writeFeatsToOut(featureSet, out)
    
    out = writeClassesToOut(sys.argv, out) 
    
    out.write('\n@data\n')
    
    # Handle optional command line argument
    num = optNumTweets(sys.argv[1])
    
    if (num == "inf"):
        # Start looking at files from the first argument
        k = 1
    else:
        # Start looking at the second argument
        k = 2
    
    # For rest of the arguments
    for i in range(k, len(sys.argv)-1):
        
        (className, files) = optclassName(sys.argv[i])

        # Check if a class name is given. If given, look at each
        # file under this class name.
        if (className != ''):
            for f in files:
                # For each file, collect features for each
                # tweet and write out to the file
                out = featsToOut(f, className, num, out)

        else: 
            out = featsToOut(sys.argv[i], sys.argv[i], num, out)
            
    out.close()


#if __name__ == "__main__":
    