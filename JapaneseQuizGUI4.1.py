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
from shared_variables import SharedVariables
Window.clearcolor = (1, 1, 1, 1)

SHARED_VARIABLES = SharedVariables()

def exit_handler():
   """ Saves the variables shared between screens"""

   SHARED_VARIABLES.save_variables() 

# Triggers the save function at the closing of the program
atexit.register(exit_handler)

class MainMenu(Screen):
       
    title = ("日本語クイズ") # This is the text for the title screen  (Japanese Quiz)
    buttonOne = ("プレー")  # This is the text for the play button    (play)
    buttonTwo = ("出口")    # Text for the quit button                 (exit)
    pass

# The vocab level menu
class GameMenuOne(Screen):   

    Title = "どの語彙レベルですか？" # This is the text for the title screen  (What level do you want?)
    LevelOne = "レベル一"           # Level one button
    LevelTwo = "レベル二"           # Level two button
    LevelThree = "レベル三"         # Level three button
    Back = "返る"                   # Back button
    DisplayLevel = StringProperty()

    def onStart(self):
        SHARED_VARIABLES.LEVEL = 0
        SHARED_VARIABLES.SCORE = 0
        SHARED_VARIABLES.WORD_DICT = {}
    
    # These functions set up what level word list the player will be quized with
    def levelOne(self):
        """Set to level one"""

        # Open the level one vocab file
        vocab_file = open('levelonevocab.json')
        SHARED_VARIABLES.LEVEL = 1 
        SHARED_VARIABLES.WORD_DICT = json.load(vocab_file) 
        SHARED_VARIABLES.WORD_LIST_LENGTH = len(SHARED_VARIABLES.WORD_DICT)
        self.DisplayLevel = "NCEA Level 2"
        SHARED_VARIABLES.save_variables()

    def levelTwo(self):
        """Set to level two"""

        # Open the level two vocab file
        vocab_file = open('leveltwovocab.json')
        SHARED_VARIABLES.LEVEL = 2 
        SHARED_VARIABLES.WORD_DICT = json.load(vocab_file) 
        SHARED_VARIABLES.WORD_LIST_LENGTH = len(SHARED_VARIABLES.WORD_DICT)
        self.DisplayLevel = "NCEA Level 2"
        SHARED_VARIABLES.save_variables()
        
    def levelThree(self):
        """Set to level three"""

        # Open the level three vocab file
        vocab_file = open('levelthreevocab.json')
        SHARED_VARIABLES.LEVEL = 3 
        SHARED_VARIABLES.WORD_DICT = json.load(vocab_file) 
        SHARED_VARIABLES.WORD_LIST_LENGTH = len(SHARED_VARIABLES.WORD_DICT)
        self.DisplayLevel = "NCEA Level 3"
        SHARED_VARIABLES.save_variables()

    pass

# Continue/Start , Reset , revision menu
class SecondaryMenu(Screen):

    #Menu text
    ConStart = "スタート/続ける"  # Continue/Start
    Revis = "リビジョン"         # Revision
    Reset = "リセット"              # Reset
    Title = "何をしたいですか？"  # (Title text) What would you like to do?      
    Back = "返る"                  # Back


    def ResetFunc(self):
        """ Resets shared variables to their defaults"""

        SHARED_VARIABLES.reset()

    def ConStartFunc(self):
        """Determines whether to start a new session or continue one 
            
        If the LEVEL variable is anything other than zero it is 
        assumed that a session has already been started and will move
        the player on to the game screen, otherwise variables will be reset
        and the player will be sent on to the level select menu
        """

        SHARED_VARIABLES.load_variables()

        if SHARED_VARIABLES.LEVEL == 0:
            self.ResetFunc()
            self.manager.current = "GameMenuOne"

        if SHARED_VARIABLES.LEVEL != 0:
            self.manager.current = "Game"
    
    pass

# The main game loop
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
    answer_file = open('possibleanswers.json')
    PossibleAnswers = json.load(answer_file) 

    Back = "返る" # Back 
    
    Score = StringProperty() # Makes ScoreVal work with kivy
   
    def create_answer_list(self, english_word):
        """Shuffles the correct word into a list with three random words"""
        
        AnswerList = []
        AnswerList.append(english_word)
        AnswerList.append(self.PossibleAnswers[random.randint(0, 894)]) 
        AnswerList.append(self.PossibleAnswers[random.randint(0, 894)]) 
        AnswerList.append(self.PossibleAnswers[random.randint(0, 894)]) 
        random.shuffle(AnswerList)
        return AnswerList

    def Start(self):
        """ Sets up the neccasary variables for one quiz round
        
        A random vocab word is chosen from the word dictionary the japanese
        is diplayed one the screen. The english word is shuffled into a list with
        three random english words, each of the items in this list is then asigned to
        a button"""

        SHARED_VARIABLES.load_variables()

        # If Start() is called and there are no more words left in the list it sends you to the end screen
        if len(SHARED_VARIABLES.WORD_DICT) == 0:
            self.manager.current = "EndScreen"

        self.Score = str(SHARED_VARIABLES.SCORE)
        self.ids.my_progress_bar.value = SHARED_VARIABLES.CURRENT_PROGRESS_VALUE

        # Choose a random vocab word from the dictionary
        japanese_word, english_word = random.choice(list(SHARED_VARIABLES.WORD_DICT.items()))
        
        # Create the list of possible answers
        AnswerList = self.create_answer_list(english_word)
        
        SHARED_VARIABLES.CURRENT_JAPANESE_WORD = japanese_word 
        SHARED_VARIABLES.CURRENT_ENGLISH_WORD = english_word # Sets the "answer word" as the english of the random word chosen above
        self.JapaneseWord = SHARED_VARIABLES.CURRENT_JAPANESE_WORD # Sets the "display word" as the japanese of the random word chosen above

        self.AnswerOne = AnswerList[0]
        self.AnswerTwo = AnswerList[1]
        self.AnswerThree = AnswerList[2]
        self.AnswerFour = AnswerList[3]

        SHARED_VARIABLES.save_variables()

    def ProgressUpdate(self):
        """Updates the progress bar
        
        Called for every round"""

        SHARED_VARIABLES.load_variables()

        # Gets the current progress value 
        SHARED_VARIABLES.CURRENT_PROGRESS_VALUE = self.ids.my_progress_bar.value

        # Defines the maximum progress value as one 
        if SHARED_VARIABLES.CURRENT_PROGRESS_VALUE == 1:
            SHARED_VARIABLES.CURRENT_PROGRESS_VALUE = 0

        # Adds on increment to the progress value 
        SHARED_VARIABLES.CURRENT_PROGRESS_VALUE += (1/SHARED_VARIABLES.WORD_LIST_LENGTH)

        # Updates the progress bar with the current progress value
        self.ids.my_progress_bar.value = SHARED_VARIABLES.CURRENT_PROGRESS_VALUE

        SHARED_VARIABLES.save_variables()


    # Is called whenever an answer button is clicked
    def Submit(self, instance):
        """Handles behaviour for submiting answers
        
        Increment score if correct, else add vocab word the the revsion list. 
        Remove vocab word from word dictionary"""

        SHARED_VARIABLES.load_variables()

        # Gets the text of the pressed button
        PressedButton = instance.text

        # If the text of the pressed button is equal to the CorrectWord then it adds one to score,
        # removes the the word from the dict, saves the new variables and sends you to the correct screen
        if PressedButton == SHARED_VARIABLES.CURRENT_ENGLISH_WORD:
            del SHARED_VARIABLES.WORD_DICT[SHARED_VARIABLES.CURRENT_JAPANESE_WORD]
            SHARED_VARIABLES.SCORE += 1
            self.Score = str(SHARED_VARIABLES.SCORE)
            self.manager.current = "CorrectScreen"
            SHARED_VARIABLES.save_variables()
            
        # If the text of the pressed button is not equal to the CorrectWord then it removes the word from 
        # the list and adds it to the revision list, its saves the variables and send you to the incorrect screen  
        if PressedButton != SHARED_VARIABLES.CURRENT_ENGLISH_WORD:
            del SHARED_VARIABLES.WORD_DICT[SHARED_VARIABLES.CURRENT_JAPANESE_WORD]
            SHARED_VARIABLES.REVISION_DICT[SHARED_VARIABLES.CURRENT_JAPANESE_WORD] = SHARED_VARIABLES.CURRENT_ENGLISH_WORD
            self.manager.current = "InCorrectScreen"
            SHARED_VARIABLES.save_variables()

    pass

# Displays when the player chooses the correct answer
class CorrectScreen(Screen):

    def Skip(self):
        """Waits for an amount of time"""

        time.sleep(0.3)
        self.manager.current = "Game"
        # After 0.3 second you are sent back to the main game loop
        

    pass 

# Displays when the player chooses the incorrect answer
class InCorrectScreen(Screen):

    def Skip(self):
        """Waits for an amount of time"""
        time.sleep(0.3)
        self.manager.current = "Game"
        # After 0.3 second you are sent back to the main game loop

    pass

# When all of the words have been removed from the list player is sent to this screen
class EndScreen(Screen):

    ScoreVal = StringProperty() 

    Back = "返る"                 # Back
    Revis = "リビジョン"          # Revision

    # Called when you enter the screen
    def Start(self):
        """Displays Score """

        SHARED_VARIABLES.load_variables()
        # Gets the current progres bar level
        self.ids.my_progress_bar.value = SHARED_VARIABLES.CURRENT_PROGRESS_VALUE

        # Gets the current score
        self.ScoreVal = str(SHARED_VARIABLES.SCORE)
    pass

# A screen where you can look through all of the words on your revision list
class RevisionList(Screen):

    CurrentEnglishWord = StringProperty()
    CurrentJapaneseWord = StringProperty()
    RevisionCompareVal = 0
    Back = "返る" # Back
    
    def Start(self):
        """Displays a vocab word from the revision dictionary based on an index
        """

        SHARED_VARIABLES.load_variables()

        try:
            # Converts the revision dictionary to a list and gets the vocab word at the given index
            japanese_word, english_word = list(SHARED_VARIABLES.REVISION_DICT.items())[self.RevisionCompareVal]

            self.CurrentJapaneseWord = japanese_word # Sets the japanese display word 
            self.CurrentEnglishWord = english_word # Sets the english display word 
       
        except IndexError:
            # Sets the display words to be blank if there are no words in the revision dictionary
            self.CurrentJapaneseWord = ""
            self.CurrentEnglishWord = ""
    
    def NextWord(self):
        """Called when the next button is pressed

        If not at the end of the list increment the index to display the next word"""
        
        SHARED_VARIABLES.load_variables()

        # If not at the end of the revision list it adds one to the revisioncompareval and 
        # calls the start function updating the display
        if self.RevisionCompareVal < (len(SHARED_VARIABLES.REVISION_DICT)-1):
            self.RevisionCompareVal += 1
            self.Start()

        # If at the end of the revision list it calls the start function again without changing 
        # the variables meaning the displayed words will be the same
        else:
            self.Start()

    def LastWord(self):
        """Called when the previous button is pressed
        
        If not at the start of the list decrement the index to display the previous word"""

        SHARED_VARIABLES.load_variables()

        # If not at the start of the revision list it subtracts one to the revisioncompareval and 
        # calls the start function updating the display
        if self.RevisionCompareVal > 0:
            self.RevisionCompareVal -= 1
            self.Start()

        else: 
            # If at the start of the revision list it calls the start function again without changing 
            # the variables meaning the displayed words will be the same
            self.Start()

    pass

class WindowManager(ScreenManager):
    pass

# Defines the .kv file to run with what encoding to use
kv = Builder.load_file("GUICode4.1.kv" , encoding='utf-8')

# The main app class
class NCEAJapaneseQuizApp(App):
    
    #builds the app 
    def build(self):
       return kv

# Runs the built app
NCEAJapaneseQuizApp().run()