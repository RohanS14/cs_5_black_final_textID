import string
from collections import Counter
from collections import defaultdict
from porter import create_stem
PUNC = '.!?'
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
        self.punc = {}     # For counting ___________

        self.wordListP = [] #has punctuation
        self.wordList = [] #no punctutation

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'MY PARAMETER:\n{str(self.punc)}\n\n'
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
            if letter in string.punctuation:
                if letter not in self.punc:
                    self.punc[letter] = 1
                else:
                    self.punc[letter] +=1

    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()
        self.makePunctuation()
        


# And let's test things out here...
#TMintro = TextModel()

# Add a call that puts information into the model
#TMintro.addRawText("""This is a small sentence. This isn't a small sentence, because this sentence contains more than 10 words and a number! This isn't a question, is it?""")

# Put the above triple-quoted string into a file named test.txt, then run this:
#  TMintro.addFileText("test.txt")   # "comment in" this line, once the file is created

# Print it out
# print("TMintro is", TMintro)


# Add more calls - and more models - here:
TM = TextModel()
TM.addFileText("test.txt")
TM.makeWordLengths()
TM.makeWords()
TM.makeStems()
TM.makePunctuation()
print("TMintro is", TM)