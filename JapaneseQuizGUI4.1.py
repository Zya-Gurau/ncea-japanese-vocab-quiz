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
from shared_variables import SharedVariables
Window.clearcolor = (1, 1, 1, 1)

SHARED_VARIABLES = SharedVariables()

#Notes:
#Because kivy cannot  display japanese text within it's own code, any japanese that needs to displayed must be assigned to a
#variable which is then passed through to the kivy side of the program

# The strings in the word lists are structured with the japanese word and the english counterpart seperated by a space 
# the two words are seperateed into the display word and the answer during processing.

#this is the saving function !!!!!!!!!!! CHANGE THIS !!!!!!!!!!!!!!!!
def exit_handler():
   SHARED_VARIABLES.save_variables() 

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
        SHARED_VARIABLES.LEVEL = 0
        SHARED_VARIABLES.SCORE = 0
        SHARED_VARIABLES.WORD_DICT = {}
    
    #these functions set up what level word list the player will be quized with
    # [DisplayLevel] is the string that shows the player their choice
    def levelOne(self):
        # open the level one vocab file
        vocab_file = open('levelonevocab.json')
        SHARED_VARIABLES.LEVEL = 1 
        SHARED_VARIABLES.WORD_DICT = json.load(vocab_file) 
        SHARED_VARIABLES.WORD_LIST_LENGTH = len(SHARED_VARIABLES.WORD_DICT)
        self.DisplayLevel = "NCEA Level 2"
        SHARED_VARIABLES.save_variables()

    def levelTwo(self):
        # open the level two vocab file
        vocab_file = open('leveltwovocab.json')
        SHARED_VARIABLES.LEVEL = 2 
        SHARED_VARIABLES.WORD_DICT = json.load(vocab_file) 
        SHARED_VARIABLES.WORD_LIST_LENGTH = len(SHARED_VARIABLES.WORD_DICT)
        self.DisplayLevel = "NCEA Level 2"
        SHARED_VARIABLES.save_variables()
        
    def levelThree(self):
        # open the level three vocab file
        vocab_file = open('levelthreevocab.json')
        SHARED_VARIABLES.LEVEL = 3 
        SHARED_VARIABLES.WORD_DICT = json.load(vocab_file) 
        SHARED_VARIABLES.WORD_LIST_LENGTH = len(SHARED_VARIABLES.WORD_DICT)
        self.DisplayLevel = "NCEA Level 3"
        SHARED_VARIABLES.save_variables()

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
        SHARED_VARIABLES.reset()

    #if there are already modified variables this function takes you to the game screen
    #if the variables are in their default states it sends you to the level selection menu
    def ConStartFunc(self):
        SHARED_VARIABLES.load_variables()

        if SHARED_VARIABLES.LEVEL == 0:
            self.ResetFunc()
            self.manager.current = "GameMenuOne"

        if SHARED_VARIABLES.LEVEL != 0:
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

        SHARED_VARIABLES.load_variables()

        answer_file = open('possibleanswers.json')
        PossibleAnswers = json.load(answer_file) 

        self.Score = str(SHARED_VARIABLES.SCORE)
        self.ids.my_progress_bar.value = SHARED_VARIABLES.CURRENT_PROGRESS_VALUE
        
        #if Start() is called and there are no more words left in the list it sends you to the end screen
        if len(SHARED_VARIABLES.WORD_DICT) == 0:
            self.manager.current = "EndScreen"

        japanese_word, english_word = random.choice(list(SHARED_VARIABLES.WORD_DICT.items()))
        
        #defines an empty list where the correct and incorrect answers will be added to
        AnswerList = []
        AnswerList.append(english_word) #adds correct answer
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        AnswerList.append(PossibleAnswers[random.randint(0, 894)]) #adds random incorrect answer from list of all possible answers
        random.shuffle(AnswerList) #shuffles the list so correct and incorrect answers are in random order

        SHARED_VARIABLES.CURRENT_JAPANESE_WORD = japanese_word #sets the "display word" as the japanese of the random word chosen above
        SHARED_VARIABLES.CURRENT_ENGLISH_WORD = english_word #sets the "answer word" as the english of the random word chosen above
        self.JapaneseWord = SHARED_VARIABLES.CURRENT_JAPANESE_WORD

        self.AnswerOne = AnswerList[0]
        self.AnswerTwo = AnswerList[1]
        self.AnswerThree = AnswerList[2]
        self.AnswerFour = AnswerList[3]

        SHARED_VARIABLES.save_variables()

    def ProgressUpdate(self):
        SHARED_VARIABLES.load_variables()
        #gets the current progress value 
        SHARED_VARIABLES.CURRENT_PROGRESS_VALUE = self.ids.my_progress_bar.value

        #defines the maximum progress value as one 
        if SHARED_VARIABLES.CURRENT_PROGRESS_VALUE == 1:
            SHARED_VARIABLES.CURRENT_PROGRESS_VALUE = 0

        #adds on increment to the progress value 
        SHARED_VARIABLES.CURRENT_PROGRESS_VALUE += (1/SHARED_VARIABLES.WORD_LIST_LENGTH)

        #updates the progress bar with the current progress value
        self.ids.my_progress_bar.value = SHARED_VARIABLES.CURRENT_PROGRESS_VALUE

        SHARED_VARIABLES.save_variables()


    #is called whenever an answer button is clicked
    def Submit(self, instance):
        SHARED_VARIABLES.load_variables()
        #gets the text of the pressed button
        PressedButton = instance.text

        #if the text of the pressed button (with underscores instead of spaces) is equal to the CorrectWord then it adds one to score,
        #removes the unprocessed version of the word from the list, saves the new variables to the text file and sends you to the correct screen
        if PressedButton == SHARED_VARIABLES.CURRENT_ENGLISH_WORD:

            del SHARED_VARIABLES.WORD_DICT[SHARED_VARIABLES.CURRENT_JAPANESE_WORD]

            SHARED_VARIABLES.SCORE += 1
            self.Score = str(SHARED_VARIABLES.SCORE)
            self.manager.current = "CorrectScreen"

            SHARED_VARIABLES.save_variables()

            
        #if the text of the pressed button (with underscores instead of spaces) is not equal to the CorrectWord then it removes the uprocessed word from the list and adds it to the revision list, its saves the variaables ot the text file and send you to the incorrect screen  
        if PressedButton != SHARED_VARIABLES.CURRENT_ENGLISH_WORD:

            del SHARED_VARIABLES.WORD_DICT[SHARED_VARIABLES.CURRENT_JAPANESE_WORD]

            SHARED_VARIABLES.REVISION_DICT[SHARED_VARIABLES.CURRENT_JAPANESE_WORD] = SHARED_VARIABLES.CURRENT_ENGLISH_WORD

            self.manager.current = "InCorrectScreen"


            SHARED_VARIABLES.save_variables()

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