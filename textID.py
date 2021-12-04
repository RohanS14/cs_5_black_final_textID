import string
import math
from collections import Counter
from collections import defaultdict
from porter import create_stem
# makeWordLengths(self): should use the text in self.text to create the self.wordlengths dictionary.
# makeWords(self): should use the text in self.text to create the self.words dictionary.
# makeStems(self): should use the text in self.text to create the self.stems dictionary.
# makeMyParameter(s): should use the text in self.text to create the myparameter dictionary. This one is up to you (we used punctuation—feel free to use that or something else...!)
# This "other feature" isn't needed for the milestone, but it is needed for the final version. Note that you should choose a better name than myparameter!
# Be sure to have a milestone.txt that includes a short (3-4 sentence) reflection on how the project has gone so far (and what still remains, if anything!).

#
# textmodel.py
#
# TextModel project!
#
# Name(s): Saya Kim-Suzuki, Laney Goldman and Rohan Subramanian
PUNC = '.!?'


class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        
        # Create another dictionary of your own
        #
        self.punc = {}     # For counting punctuation
        

        self.wordListP = [] #has punctuation
        self.wordList = [] #no punctutation

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'punctuation:\n{str(self.punc)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:42]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:42]}\n'
        s += '+'*55 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.
            
           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='latin1')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """
        self.wordListP = self.text.split()
        counterList = []
        counter = 0
        for word in self.wordListP:
            counter +=1
            if word[-1] in PUNC:
                counterList.append(counter)
                counter = 0
            else:
                pass
        # dictionary of the form {sentence length: frequency}
        self.sentencelengths = dict(Counter(counterList))    

    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        s = s.encode("ascii", "ignore")   # Ignores non-ASCII characters
        s = s.decode()         # Decodes it back to a string (with the non-ACSII characters removed) 
        s = s.lower()    # convert to lower case
        for p in string.punctuation: # remove punctuation
            s = s.replace(p, '')
        #s = s.replace("\n", "") # strip new lines
        return s

    def makeWordLengths(self):
        """should use the text in self.text to create the self.wordlengths dictionary."""
        self.cleanedtext = self.cleanString(self.text)
        self.wordList = self.cleanedtext.split()
        for word in self.wordList:
            if len(word) not in self.wordlengths:
                self.wordlengths[len(word)] = 1
            else:
                self.wordlengths[len(word)] += 1
            
    def makeWords(self): 
        """should use the text in self.text to create the self.words dictionary."""
        self.cleanedtext = self.cleanString(self.text)
        self.wordList = self.cleanedtext.split()
        self.words = dict(Counter(self.wordList))
    
    def makeStems(self): 
        """should use the text in self.text to create the self.stems dictionary."""
        self.stems = defaultdict(int)
        for word in self.wordList:
            self.stems[create_stem(word)] += 1
        self.stems = dict(self.stems)
        
    def makePunctuation(self):
        ''' should use the text in self.txt to make the self.punc dictionary'''
        #string.punctuation:
        for letter in self.text:
            if letter in string.punctuation: #if letter is punctation
                if letter not in self.punc: 
                    self.punc[letter] = 1
                else:
                    self.punc[letter] +=1

    def normalizeDictionary(self, d):
        '''Accepts any single one of the model dictionaries d and return a normalized version,
         i.e., one in which the values add up to 1.0.'''
        return {k:d[k]/sum(list(d.values())) for k in d}

    def smallestValue(self, nd1, nd2):
        """Accepts any two model dictionaries nd1 and nd2 and returns the smallest positive (that is, non-zero) value across them both."""
        min1 = min(list(nd1.values()))
        min2 = min(list(nd2.values()))
        return min(min1, min2)

    def compareDictionaries(self, d, nd1, nd2):
        """Computes:
            - log probability that d arose from nd1 
            - log probability that d arose from nd2 
            Returns:
            - List [1p1, 1p2]: log probabilities """

        nd1 = self.normalizeDictionary(nd1)
        nd2 = self.normalizeDictionary(nd2)
        epsilon = self.smallestValue(nd1, nd2)/2

        #probability that d arose from nd1
        prob1 = 0
        for k in d:
            if k in nd1:
                prob1 += d[k]*math.log(nd1[k])
            else:
                prob1 += d[k]*math.log(epsilon)
                
        #probability that d arose from nd2
        prob2 = 0
        for k in d:
            if k in nd2:
                prob2 += d[k]*math.log(nd2[k])
            else:
                prob2 += d[k]*math.log(epsilon)
        return [prob1, prob2]

    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()
        self.makePunctuation()

    def compareTextWithTwoModels(self, model1, model2):
        """This method should run the compareDictionaries method, described above, for each of the feature dictionaries in self against the corresponding (normalized!) dictionaries in model1 and model2."""

        print("Overall comparison:\n")
        print(f"     {'name':>20s}   {'vsTM1':>10s}   {'vsTM2':>10s} ")
        print(f"     {'----':>20s}   {'-----':>10s}   {'-----':>10s} ")

        d1Score = 0
        d2Score = 0

        #checking words
        nd1_word = self.normalizeDictionary(model1.words)
        nd2_word = self.normalizeDictionary(model2.words)
        
        wordsProbs = self.compareDictionaries(self.words, nd1_word, nd2_word)
        if wordsProbs[0] > wordsProbs[1]:
            d1Score += 1
        else:
            d2Score += 1

        d_name = 'words used'
        print(f"     {d_name:>20s}   {wordsProbs[0]:>10.2f}   {wordsProbs[1]:>10.2f} ") 
            
        #print("Word probabilities is", LogProbs1)

        #checking word lengths

        nd1_wordlength = self.normalizeDictionary(model1.wordlengths)
        nd2_wordlength = self.normalizeDictionary(model2.wordlengths)

        wordlengthProbs = self.compareDictionaries(self.wordlengths, nd1_wordlength, nd2_wordlength)
        if wordlengthProbs[0] > wordlengthProbs[1]:
            d1Score += 1
        else:
            d2Score += 1
            
        d_name = 'word lengths'
        print(f"     {d_name:>20s}   {wordlengthProbs[0]:>10.2f}   {wordlengthProbs[1]:>10.2f} ") 

        #checking sentence lengths
        nd1_sentencelen = self.normalizeDictionary(model1.sentencelengths)
        nd2_sentencelen = self.normalizeDictionary(model2.sentencelengths)

        sentLenProbs = self.compareDictionaries(self.sentencelengths, nd1_sentencelen, nd2_sentencelen)
        if sentLenProbs[0] > sentLenProbs[1]:
            d1Score += 1
        else:
            d2Score += 1
            
        d_name = 'sentence lengths'
        print(f"     {d_name:>20s}   {sentLenProbs[0]:>10.2f}   {sentLenProbs[1]:>10.2f} ") 

        #checkings stems
        nd1_stems = self.normalizeDictionary(model1.stems)
        nd2_stems = self.normalizeDictionary(model2.stems)

        stemProbs = self.compareDictionaries(self.stems, nd1_stems, nd2_stems)
        if stemProbs[0] > stemProbs[1]:
            d1Score += 1
        else:
            d2Score += 1

        d_name = 'stems used'
        print(f"     {d_name:>20s}   {stemProbs[0]:>10.2f}   {stemProbs[1]:>10.2f} ") 


        #checking punctuation
        nd1_punc = self.normalizeDictionary(model1.punc)
        nd2_punc = self.normalizeDictionary(model2.punc)
        
        puncProbs = self.compareDictionaries(self.punc, nd1_punc, nd2_punc)
        if puncProbs[0] > puncProbs[1]:
            d1Score += 1
        else:
            d2Score += 1

        d_name = 'punctuation used'
        print(f"     {d_name:>20s}   {puncProbs[0]:>10.2f}   {puncProbs[1]:>10.2f} ") 

        #determining the winner
        print("\n")
        print(f"--> Model1 wins on {d1Score} features")
        print(f"--> Model2 wins on {d2Score} features")
        print("\n")

        if d2Score > d1Score:
            print("Model 2 is a better match!")
        else:
            print("Model 1 is a better match!")


# TEST #1: COMPARING HUNGER GAMES VS. MOTIVATIONAL BOOK AGAINST SAYA'S WRIT ESSAY (big files)

# print(" +++++++++++ Model1 +++++++++++ ")
# TM1 = TextModel()
# TM1.addFileText("hunger_games.txt")
# TM1.createAllDictionaries()  # provided in hw description
# print(TM1)

# print(" +++++++++++ Model2 +++++++++++ ")
# TM2 = TextModel()
# TM2.addFileText("motivation_book.txt")
# TM2.createAllDictionaries()  # provided in hw description
# print(TM2)


# print(" +++++++++++ Unknown text +++++++++++ ")
# TM_Unk = TextModel()
# TM_Unk.addFileText("writ_saya.txt")
# TM_Unk.createAllDictionaries()  # provided in hw description
# print(TM_Unk)

# TEST #2: COMPARING LANEY VS. ROHAN'S WRIT ESSAYS AGAINST BOTH REFLECTIVE ESSAYS

print(" +++++++++++ Laney's Essay +++++++++++ ")
TM1 = TextModel()
TM1.addFileText("laneyEssay.txt")
TM1.createAllDictionaries()  # provided in hw description
print(TM1)

print(" +++++++++++ Rohan's Essay +++++++++++ ")
TM2 = TextModel()
TM2.addFileText("essay_RS.txt")
TM2.createAllDictionaries()  # provided in hw description
print(TM2)


# print(" +++++++++++ Rohan's Reflective Essay +++++++++++ ")
# TM_Unk = TextModel()
# TM_Unk.addFileText("reflective_RS.txt")
# TM_Unk.createAllDictionaries()  # provided in hw description
# print(TM_Unk)

print(" +++++++++++ Laney's Reflective Essay +++++++++++ ")
TM_Unk = TextModel()
TM_Unk.addFileText("laneyReflective.txt")
TM_Unk.createAllDictionaries()  # provided in hw description
print(TM_Unk)

