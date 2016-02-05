'''detectAuthor.py
    
    Martin Hoffman
    Sam Nozaki

    Created 1/30/2015
    Python Version: 3.5

    Attempts to determine the author of a text based on word and sentence
    metrics derived from known texts.

    CS111, Winter 2016
'''

import os
import os.path


# Functions for getting words and sentences
def getWords(text):
    '''Returns a list of the words (in order) that are stored
    in text.
    
    Parameters:
        text - A list of strings.
    '''
    wordList = []
    for line in text:
        for word in line.split():
            if cleanUp(word) != '':
                wordList.append(cleanUp(word))
        
    return wordList
    

def getSentences(text):
    '''Returns a list of the sentences (in order) that are stored
    in text. text is a list of strings; sentences may extend across
    multiple items in the list (e.g., text might be a list
    with each item corresponding to one line in a file; sentences
    don't automatically end with new lines in a file).
    
    Parameters:
        text - A list of strings
    '''
    sentences = []
    sentence = ''
    for line in text:
        for char in line:
            if char != '.' and char != '?' and char != '!':
                sentence += char
            elif sentence != '':
                sentences.append(sentence)
                sentence = ''
    
    return sentences


def cleanUp(s):
    '''Returns a string which is a copy of s in which all letters have been
    converted to lowercase and punctuation characters have been stripped 
    from both ends. Inner punctuation is left untouched. 
    '''
    punctuation = '''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result


# Functions for linguistic features
def averageWordLength(text):
    '''Returns a float representing the average word length in a given text.
    
    Parameters:
        text - A list of strings
    '''
    wordList = getWords(text)
    avg = 0
    for word in wordList:
        avg += len(word)
        
    return avg / len(wordList)


def averageSentenceLength(text):
    '''Returns a float representing the average sentence length in a given text.
    
    Parameters:
        text - A list of strings
    '''    
    sentenceList = getSentences(text)
    avg = 0
    for sentence in sentenceList:
        avg += len(getWords(sentence))
    
    return avg / len(sentenceList)


def averageSentenceComplexity(text):
    '''Returns a float representing the average number of phrases per sentence 
    in a given text.
    
    Parameters:
        text - A list of strings
    '''
    phrases = 0
    for line in text:
        for char in line:
            if char == ',' or char == ';' or char == ':':
                phrases += 1

    return (phrases + len(getSentences(text))) / len(getSentences(text))


def typeToTokenRatio(text):
    '''Returns the ratio between the number of distinct words in a text divided 
    by the total number of words in text. Gives a sense of the author's 
    repetitiveness.

    Parameters: 
        text - A list of strings
    '''
    distinctWords = []
    for word in getWords(text):
        if word not in distinctWords:
            distinctWords.append(word)
    
    return len(distinctWords) / len(getWords(text))


def hapaxLegomanaRatio(text):
    '''Returns the ratio between the total number of words that occur exactly 
    once divided by the total number of words in text. Again indicates 
    repetetiveness.

    Parameters:
        text - A list of strings
    '''
    uniqueWords = {}

    for word in getWords(text):
        if word not in uniqueWords:
            uniqueWords[word] = 1
        else:
            uniqueWords[word] += 1

    onceWords = 0
    for word in uniqueWords:
        if uniqueWords[word] == 1:
            onceWords += 1

    return onceWords / len(getWords(text))


def functionWordRatios(text):
    '''Returns a list of ratios for each function word given by getAllFunctionWords.
    
    Parameters:
        text - A list of strings
    '''
    functionWords = getAllFunctionWords()
    wordCount = {}
    ratios = []
    for word in functionWords:
        wordCount[word] = 0
    
    for word in getWords(text):
        if word in functionWords:
            wordCount[word] += 1
            
    for word in wordCount:
        ratios.append(wordCount[word] / len(getWords(text)))
        
    return ratios


def getAllFunctionWords():
    '''Returns a list of function words stored
    in the function word file ('FunctionWordList.txt').
    Each item in the list is a function word. This function
    does not check the format of the file, so make sure you 
    do not modify FunctionWordList.txt and that it is
    in the same directory as detectAuthor.py
    '''
    file = open('FunctionWordList.txt', 'r')
    wordList = []
    for line in file:
        wordList.append(line.strip().split()[0])
    file.close()
    return wordList


# Functions for calculating, reading, and writing signatures
def calculateSignatureFromURL(url):
    '''TODO: Implement this function, filling in this comment in an
    appropriate way. Make sure your function meets the specifications
    in the assignment.
    '''
    pass # remove this and add your own code instead


def calculateSignatureFromTextFile(filename):
    '''Returns a list of values for a given text file that represent its average word length,
    average sentence length, average sentence complexity, type to token ratio, hapax legomana
    ratio, and function word ratios, respectively.
    
    Parameters:
        filename - Name of the file whose signature is to be calculated
    '''
    file = open(filename, 'r')
    text = file.read()
    signature = ['']
    signature.append(averageWordLength(text))
    signature.append(averageSentenceLength(text))
    signature.append(averageSentenceComplexity(text))
    signature.append(typeToTokenRatio(text))
    signature.append(hapaxLegomanaRatio(text))
    signature.append(functionWordRatios(text))
    file.close()
    
    return signature


def readSignature(filename):
    '''Read a linguistic signature from filename and return it as
    list of features.
    '''
    file = open(filename, 'r')
    # The first feature is the name of the author (a string) so it
    # doesn't need casting to float
    result = [file.readline().strip()]
    # All remaining features are real numbers
    for line in file:
        result.append(float(line.strip()))
    file.close()
    return result


def writeSignature(signature, signatureFile):
    '''Writes the signature (list of feature weights) to a new file named 
    signatureFile.  Overwrites any existing file in that location.
    '''
    file = open(signatureFile, 'w')
    for i in range(len(signature)):
        file.write(str(signature[i]) + '\n')
    file.close()


# Functions related to similarity
def computeSimilarity(signature1, signature2, weights):
    '''Returns the similarity between signature1 and signature2,
    computed as the absolute value of the difference between the two
    signatures, multiplied by the weights and summed. signature1,
    signature2, and weights are all lists where the 0th value in
    the list is ignored.
    '''
    similarity = 0
    for i in range (1, len(weights)):
        similarity += abs(signature1[i] - signature2[i]) * weights[i]
        
    return similarity


def getWeights():
    '''Returns a list of weights for the similarity calculation.
    The weights are in the order of the features: average word
    length, average sentence length, average sentence complexity,
    type to token ratio, hapax legomana ratio, and then all of the
    function word weights. This function assumes FunctionWordList.txt
    is in the same directory as detectAuthor.py.
    '''
    featureWeights = [0, 11, 0.4, 4, 33, 50]
    file = open('FunctionWordList.txt', 'r')
    for line in file:
        featureWeights.append(float(line.strip().split()[1]))
    file.close()
    return featureWeights


def getMostSimilarAuthor(signatureDirectory, mysterySignature):
    '''Returns the author name for the signature
    that has the smallest similarity score (smaller = more similar).
    The code for going through a directory of files and reading the 
    signatures is provided for you. You need to modify this function
    to find and return the most similar author. 
    '''
    # The weights are a mixture of hardcoded weights for the non-function
    # word features and specified in the function word file.
    featureWeights = getWeights()
    
    # The line below lists all files that are in the directory
    # signature directory. Note that this means you must have
    # only signature files in that directory - either ones I
    # gave you or ones you've created.
    files = os.listdir(signatureDirectory)

    # You'll likely want to declare some variables prior to the
    # for loop to be able to compute author with the best similarity.
    # Make sure you have a good idea for the steps you want to take
    # to find the best similarity before you actually do it; make
    # sure you and your partner can explain the algorithm to one another.
    for currentFile in files:
        # The condition below ignores hidden files that may be created 
        # by your operating system
        if not currentFile.startswith('.'):
            # The line below calculates the signature for the current file
            signature = readSignature(signatureDirectory + os.sep + currentFile)
            
            # Now, compute the similarity between the signatures (you should
            # have a function to help you!) and do anything you need to be
            # able to return the most similar author at the end
    
    # Don't forget to return the most similar author at the end


# Printing and user interface
def printSignature(signature):
    '''Prints a signature to the console, one
    line per feature.
    '''
    features = ['Average word length', 'Average sentence length', 
                'Average sentence complexity','Type to token ratio',
                ' Hapax Legomana ratio']
    print('Signature:')
    # First, print all the features that are not related to fn words
    for i in range(1,len(features)):
        print(features[i-1] + ':', str(signature[i]))
        
    # Now, print all the function word features.
    # Note that the indices differ between where the word is in the
    # list of function words and where the value is for that feature
    # in the signature.
    fnWords = getAllFunctionWords()
    for i in range(len(features)+1,len(signature)):
        print(fnWords[i - (len(features)+1)] + ':', str(signature[i]))


def main():
    '''Implement this and add a comment describing what it does!
    '''
    filename = input('Please enter a filename: ')
    while os.path.exists(filename) != True:
        print('File not found...')
        filename = input('Please enter a filename: ')
   
    file = open(filename, 'r')
    text = file.readlines()
    file.close()

    print('### Statistics for the file', filename, '###\n')
    print('Average Word Length:', averageWordLength(text), 'characters.')
    print('Average Sentence Length:', averageSentenceLength(text), 'words.')
    print('Sentence Complexity:', averageSentenceComplexity(text), 
         'phrases per sentence.')
    print('Ratio of Distinct Words to Total Words:', typeToTokenRatio(text))
    print('Hapax Legomana ratio:', hapaxLegomanaRatio(text))