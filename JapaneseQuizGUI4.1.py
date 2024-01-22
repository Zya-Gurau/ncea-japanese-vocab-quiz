import json
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


#this is the saving function !!!!!!!!!!! CHANGE THIS !!!!!!!!!!!!!!!!
def exit_handler():
   with open('variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([WordList, revList, Level, wordAmount, maxIndex, score, unprostring, Word, MaxCounterVal, CorrectWord, ListLength, current], f) 

#this triggers the save function at the closing of the program
atexit.register(exit_handler)

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
        shared_variables.LEVEL = 0
        shared_variables.SCORE = 0
        shared_variables.WORD_DICT = {}
    
    #these functions set up what level word list the player will be quized with
    # [DisplayLevel] is the string that shows the player their choice
    def levelOne(self):
        # open the level one vocab file
        vocab_file = open('levelonevocab.json')
 
        shared_variables.LEVEL = 1 
        shared_variables.WORD_DICT = json.load(vocab_file) 
        shared_variables.WORD_LIST_LENGTH = len(shared_variables.WORD_DICT)
        self.DisplayLevel = "NCEA Level 2"

    def levelTwo(self):
        # open the level two vocab file
        vocab_file = open('leveltwovocab.json')
 
        shared_variables.LEVEL = 2 
        shared_variables.WORD_DICT = json.load(vocab_file) 
        shared_variables.WORD_LIST_LENGTH = len(shared_variables.WORD_DICT)
        self.DisplayLevel = "NCEA Level 2"
        
    def levelThree(self):
        # open the level three vocab file
        vocab_file = open('levelthreevocab.json')
 
        shared_variables.LEVEL = 3 
        shared_variables.WORD_DICT = json.load(vocab_file) 
        shared_variables.WORD_LIST_LENGTH = len(shared_variables.WORD_DICT)
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

    #sets all of the global variables to their default values and saves over any instance of them that already exists
    def ResetFunc(self):
        shared_variables.LEVEL = 0
        shared_variables.SCORE = 0
        shared_variables.WORD_DICT = {}

    #if there are already modified variables this function takes you to the game screen
    #if the variables are in their default states it sends you to the level selection menu
    def ConStartFunc(self):

        if shared_variables.LEVEL == 0:
            self.ResetFunc()
            self.manager.current = "GameMenuOne"

        if shared_variables.LEVEL != 0:
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
    
    Score = StringProperty() #Makes ScoreVal work with kivy
   
    #on start an unprocessed word is taken from WordList and is split inot its japanese display word and its correct english answer.
    def Start(self):
        answer_file = open('possibleanswers.json')
        PossibleAnswers = json.load(answer_file) 

        self.Score = str(shared_variables.SCORE)
        self.ids.my_progress_bar.value = shared_variables.CURRENT_PROGRESS_VALUE
        
        #if Start() is called and there are no more words left in the list it sends you to the end screen
        if len(shared_variables.WORD_DICT) == 0:
            self.manager.current = "EndScreen"

        japanese_word, english_word = random.choice(list(shared_variables.WORD_DICT.items()))
        
        #defines an empty list where the correct and incorrect answers will be added to
        AnswerList = []
        AnswerList.append(english_word) #adds correct answer
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        random.shuffle(AnswerList) #shuffles the list so correct and incorrect answers are in random order

        shared_variables.CURRENT_JAPANESE_WORD = japanese_word #sets the "display word" as the japanese of the random word chosen above
        shared_variables.CURRENT_ENGLISH_WORD = english_word #sets the "answer word" as the english of the random word chosen above
        self.JapaneseWord = shared_variables.CURRENT_JAPANESE_WORD

        self.AnswerOne = AnswerList[0]
        self.AnswerTwo = AnswerList[1]
        self.AnswerThree = AnswerList[2]
        self.AnswerFour = AnswerList[3]

    def ProgressUpdate(self):

        #gets the current progress value 
        shared_variables.CURRENT_PROGRESS_VALUE = self.ids.my_progress_bar.value

        #defines the maximum progress value as one 
        if shared_variables.CURRENT_PROGRESS_VALUE == 1:
            shared_variables.CURRENT_PROGRESS_VALUE = 0

        #adds on increment to the progress value 
        shared_variables.CURRENT_PROGRESS_VALUE += (1/shared_variables.WORD_LIST_LENGTH)

        #updates the progress bar with the current progress value
        self.ids.my_progress_bar.value = shared_variables.CURRENT_PROGRESS_VALUE


    #is called whenever an answer button is clicked
    def Submit(self, instance):
        
        #gets the text of the pressed button
        PressedButton = instance.text

        #if the text of the pressed button (with underscores instead of spaces) is equal to the CorrectWord then it adds one to score,
        #removes the unprocessed version of the word from the list, saves the new variables to the text file and sends you to the correct screen
        if PressedButton == CorrectWord:

            del shared_variables.WORD_DICT[shared_variables.CURRENT_JAPANESE_WORD]

            shared_variables.SCORE += 1
            self.Score = str(shared_variables.SCORE)
            self.manager.current = "CorrectScreen"

            #!!!!! SAVE SHARED VARIABLES  !!!!!#

            
        #if the text of the pressed button (with underscores instead of spaces) is not equal to the CorrectWord then it removes the uprocessed word from the list and adds it to the revision list, its saves the variaables ot the text file and send you to the incorrect screen  
        if PressedButton != CorrectWord:

            del shared_variables.WORD_DICT[shared_variables.CURRENT_JAPANESE_WORD]

            #revList.append(unprostring)

            self.manager.current = "InCorrectScreen"


            #!!!!! SAVE SHARED VARIABLES  !!!!!#

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
        #gets the current progres bar level
        self.ids.my_progress_bar.value = shared_variables.CURRENT_PROGRESS_VALUE

        #gets the current score
        self.ScoreVal = str(shared_variables.SCORE)
        


    
    
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