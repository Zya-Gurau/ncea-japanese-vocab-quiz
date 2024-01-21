import random
import time
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
import os, sys
from kivy.resources import resource_add_path, resource_find
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
import atexit
import pickle
import shared_variables
Window.clearcolor = (1, 1, 1, 1)

#Notes:
#Because kivy cannot  display japanese text within it's own code, any japanese that needs to displayed must be assigned to a
#variable which is then passed through to the kivy side of the program

# The strings in the word lists are structured with the japanese word and the english counterpart seperated by a space 
# the two words are seperateed into the display word and the answer during processing.


#Words of the chosen level are moved into this list 
#words are processed out of this list and not one of the original lists because an intact copy of all the words needs to exist
#during the program words are deleted from the list
WordList = []

#when the player answers incorrectly the word is deleted from WordList and put into revision list 
revList = []


Level = 0        # The current level of vocab 
wordAmount = 0   # this is a holdover variable used when debuging the program, it does nothing functionaly
maxIndex = 0     #stores the current length of the word list, (used when picking a random word)
score = 0        #stores the players score
unprostring = "" #stores the current un-processed string from WordList
Word = []        #stores the the english word and the japanese word as two seperate items in a list.
MaxCounterVal = 0  # A debug variable that serves no functional prupose
CorrectWord = ""   #is the string with the current correct english word
ListLength = 0     # is the full length of the chosen levels vocab list (once asigned it's a static value) (used for the progress bar)
current = 0        #is the current progress value which determines the length of the progress bar
RevisionCompareVal = 0  #used to determine what revision word should be diplayed



#Order of variable storage:
#   WordList, RevList, Level, WordAmount, MaxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current




#the saving and loading of variables is done using pickle


#this is the saving function
def exit_handler():
   with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

#this triggers the save function at the closing of the program
atexit.register(exit_handler)

#A load function that can be called from anywhere
def FullLoad():
    with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

class MainMenu(Screen):
       
    title = ("日本語クイズ") #this is the text for the title screen  (Japanese Quiz)
    buttonOne = ("プレー")  #this is the text for the play button    (play)
    buttonTwo = ("出口")    #text for the quit button                 (exit)
    pass

#the vocab level menu
class GameMenuOne(Screen):   

    Title = "どの語彙レベルですか？" #this is the text for the title screen  (What level do you want?)
    LevelOne = "レベル一"           # Level one button
    LevelTwo = "レベル二"           #Level two button
    LevelThree = "レベル三"         #Level three button
    Back = "返る"                   #Back button
    DisplayLevel = StringProperty()

    def onStart(self):
        global WordList 
        global revList 
        global Level
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal 
        global CorrectWord 
        global ListLength 
        global current 

        WordList = []
        revList = []
        Level = 0
        wordAmount = 0
        maxIndex = 0
        score = 0   
        unprostring = ""
        Word = ""
        MaxCounterVal = 0
        CorrectWord = ""
        ListLength = 0
        current = 0
    
    
    #these functions set up what level word list the player will be quized with
    # [DisplayLevel] is the string that shows the player their choice
    # [MaxIndex] is used as the max number for range od the random word chooser  (had to subtract by one to get the index right)
    def levelOne(self):
        global Level
        global WordList
        global LevelOneWordList
        global maxIndex
        global ListLength
        Level = 2
        WordList = LevelOneWordList
        ListLength = len(WordList)
        maxIndex = len(WordList) - 1
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
        self.DisplayLevel = "NCEA Level 2"

    def levelTwo(self):
        global Level
        global WordList
        global LevelTwoWordList
        global maxIndex
        global ListLength
        Level = 2
        WordList = LevelTwoWordList
        ListLength = len(WordList)
        maxIndex = len(WordList) - 1
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
        self.DisplayLevel = "NCEA Level 2"
        
    def levelThree(self):
        global Level
        global WordList
        global LevelThreeWordList
        global maxIndex
        global ListLength
        Level = 3
        WordList = LevelThreeWordList
        ListLength = len(WordList)
        maxIndex = len(WordList) - 1
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
        self.DisplayLevel = "NCEA Level 3"


    pass

#Continue/Start , Reset , revision menu
class SecondaryMenu(Screen):


    #Menu text
    ConStart = "スタート/続ける"  #Continue/Start
    Revis = "リビジョン"         # Revision
    Reset = "リセット"              #Reset
    Title = "何をしたいですか？"  #(Title text) What would you like to do?      
    Back = "返る"                  #Back

    #loads all of the global variables from the text file they're saved to
    def Load(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 

        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

    #sets all of the global variables to their default values and saves over any instance of them that already exists
    def ResetFunc(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        WordList = []
        revList = []
        Level = 0
        wordAmount = 0
        maxIndex = 0
        score = 0   
        unprostring = ""
        Word = ""
        MaxCounterVal = 0
        CorrectWord = ""
        ListLength = 0
        current = 0

        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

    #if there are already modified variables this function takes you to the game screen
    #if the variables are in their default states it sends you to the level selection menu
    def ConStartFunc(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global WordList

        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        if Level == 0:
            self.ResetFunc()
            self.manager.current = "GameMenuOne"

        if Level != 0:
            with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 
            self.manager.current = "Game"
    
    pass

#the main game loop
class Game(Screen):
    
    JapaneseWord = StringProperty()
    EnglishWord = StringProperty()
    englishanswer = ObjectProperty()
    TitleString = StringProperty()
    InputTextThing = StringProperty()
    AnswerOne = StringProperty()
    AnswerTwo = StringProperty()
    AnswerThree = StringProperty()
    AnswerFour = StringProperty()

    

    Back = "返る" #back 

    OtherCounterVal = 0 #debug
    
    Score = StringProperty() #Makes ScoreVal work with kivy
   
    #on start an unprocessed word is taken from WordList and is split inot its japanese display word and its correct english answer.
    def Start(self):
        global wordAmount
        global WordList
        global revList
        global maxIndex
        global unprostring
        global Word
        global score
        global current
        global CorrectWord
        global Level 
        global MaxCounterVal
        global ListLength 
        global PossibleAnswers

        #load in the saved global variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)
        


        self.Score = str(score)
        self.ids.my_progress_bar.value = current
        
        #if Start() is called and there are no more words left in the list it sends you to the end screen
        if len(WordList) == 1:
            print("wags")
            self.manager.current = "EndScreen"
        

        #max index is used to set the upper value of the random range used to pick the random word
        maxIndex = len(WordList) - 1

        #if Start() is called and there are no more words left in the list it sends you to the end screen
        if maxIndex == -1:
            self.manager.current = "EndScreen"

        #debug lines
        print(str(maxIndex))
        print(len(WordList))
        print(WordList)

        #picks a random word from the word list 
        unprostring = WordList[random.randint(0, maxIndex)]
        
        #splits the word into two items in a list (japanese - english)
        Word = unprostring.split()

        #defines an empty list where the correct and incorrect answers will be added to
        AnswerList = []
        AnswerList.append(Word[1]) #adds correct answer
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        random.shuffle(AnswerList) #shuffles the list so correct and incorrect answers are in random order

        self.JapaneseWord = Word[0] #sets the "display word" as the japanese of the random word chosen above
        CorrectWord = Word[1] #sets the "answer word" as the english of the random word chosen above

        self.AnswerOne = AnswerList[0].replace("_", " ") #replaces underscores in the answer with spaces
        self.AnswerTwo = AnswerList[1].replace("_", " ") #replaces underscores in the answer with spaces
        self.AnswerThree = AnswerList[2].replace("_", " ") #replaces underscores in the answer with spaces
        self.AnswerFour = AnswerList[3].replace("_", " ") #replaces underscores in the answer with spaces

        
        #if self.AnswerOne.replace(" ", "_") == Word[1]:
            #CorrectId = "One"

        #if self.AnswerTwo.replace(" ", "_") == Word[1]:
            #CorrectId = "Two"

        #if self.AnswerThree.replace(" ", "_") == Word[1]:
            #CorrectId = "Three"

        #if self.AnswerFour.replace(" ", "_") == Word[1]:
            #CorrectId = "Four"
    


    def ProgressUpdate(self):
        global WordList
        global ListLength
        global current

        #gets the current progress value 
        current = self.ids.my_progress_bar.value

        #defines the maximum progress value as one 
        if current == 1:
            current = 0

        #adds on increment to the progress value 
        current += (1/int(ListLength))

        #updates the progress bar with the current progress value
        self.ids.my_progress_bar.value = current

        #saves the new variables
        with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

    #is called whenever an answer button is clicked
    def Submit(self, instance):
        global score
        global streak
        global WordList
        global wordAmount
        global Word
        global MaxCounterVal
        global AttemptCounter
        global revList
        global unprostring
        global AttemptCounter
        global CorrectWord
        global ColourOne
        
        #gets the text of the pressed button
        PressedButton = instance.text

        #if the text of the pressed button (with underscores instead of spaces) is equal to the CorrectWord then it adds one to score,
        #removes the unprocessed version of the word from the list, saves the new variables to the text file and sends you to the correct screen
        if PressedButton.replace(" ", "_") == CorrectWord:
            WordList.remove(unprostring)
            score += 1
            self.Score = str(score)
            self.manager.current = "CorrectScreen"
            with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

            
        #if the text of the pressed button (with underscores instead of spaces) is not equal to the CorrectWord then it removes the uprocessed word from the list and adds it to the revision list, its saves the variaables ot the text file and send you to the incorrect screen  
        if PressedButton.replace(" ", "_") != CorrectWord:
            WordList.remove(unprostring)
            revList.append(unprostring)
            self.manager.current = "InCorrectScreen"
            with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

           
            
    

    
    

    pass

#these screen are to show whether or not you got answer correct or not
class CorrectScreen(Screen):

    def Skip(self):
        time.sleep(0.3)
        self.manager.current = "Game"
        #after 0.3 second you are sent back to the main game loop
        

    pass 

#these screen are to show whether or not you got answer correct or not
class InCorrectScreen(Screen):

    def Skip(self):
        time.sleep(0.3)
        self.manager.current = "Game"
        #after 0.3 second you are sent back to the main game loop

    pass

#when all of the words have been removed from the list you are sent to this screen
class EndScreen(Screen):
    

    ScoreVal = StringProperty() #makes ScoreVal word with kivy

    #title texts
    Back = "返る"                 #Back
    Revis = "リビジョン"          #revision

    #called when you enter the screen
    def Start(self):
        global current
        global score

        #gets the current progres bar level
        self.ids.my_progress_bar.value = current

        #gets the current score
        self.ScoreVal = str(score)
        


    
    
    pass

#a screen where you can look through all of the words on your revision list
class RevisionList(Screen):

    #makes the values work with kivy
    CurrentEnglishWord = StringProperty()
    CurrentJapaneseWord = StringProperty()

    Back = "返る" #Back
    
    #called on entry to the program
    def Start(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global revList
        global RevisionCompareVal

        #gets the saved variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        try:
            #gets the word in the revision list with the index value equal to RevisionCompareVal and splits it and makes a list out of the two items
            CurrentUnproWord = revList[RevisionCompareVal].split()

            self.CurrentJapaneseWord = CurrentUnproWord[0] #sets the japanese display word equal to the japanese item in the list
            self.CurrentEnglishWord = CurrentUnproWord[1].replace("_", " ") #sets the english display word equal to the english item in the list
        
        except:
            #sets the display words to be blank
            self.CurrentJapaneseWord = ""
            self.CurrentEnglishWord = ""

        
    #called when the next word button is pressed
    def NextWord(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global revList
        global RevisionCompareVal

        #updates the variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        #if you haven't reached the end of the revision list it adds one to the revisioncompareval and calls the start function updating the display
        if RevisionCompareVal < (len(revList)-1):
            RevisionCompareVal += 1
            self.Start()

        #if you have reached the end of the revision list it calls the start function again without changing the variables meaning the displayed words will be the same
        else:
            self.Start()

    #called when the previuos word button has been pressed
    def LastWord(self):
        global Level 
        global wordAmount 
        global maxIndex 
        global score   
        global unprostring 
        global Word 
        global MaxCounterVal
        global CorrectWord 
        global ListLength 
        global current 
        global revList
        global RevisionCompareVal

        #updates the variables
        with open('variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current = pickle.load(f)

        #if you haven't reached the end of the revision list it subtracts one to the revisioncompareval and calls the start function updating the display
        if RevisionCompareVal > 0:
            RevisionCompareVal -= 1
            self.Start()

        else: 
            #if you have reached the start of the revision list it calls the start function again without changing the variables meaning the displayed words will be the same
            self.Start()



    pass

#sorts all of the screens
class WindowManager(ScreenManager):
    pass

#defines the .kv file to run with what encoding to use
kv = Builder.load_file("GUICode4.1.kv" , encoding='utf-8')

#the main app class
class NCEAJapaneseQuizApp(App):
    
    #builds the app 
    def build(self):
       return kv


#runs the built app
NCEAJapaneseQuizApp().run()