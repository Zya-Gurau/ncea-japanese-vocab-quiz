import json

class SharedVariables:
    def __init__(self):
        self.LEVEL = 0
        self.WORD_DICT = {}
        self.SCORE = 0
        self.CURRENT_PROGRESS_VALUE = 0
        self.WORD_LIST_LENGTH = 0
        self.CURRENT_ENGLISH_WORD = ""
        self.CURRENT_JAPANESE_WORD = ""
        self.REVISION_DICT = {}
        #self.save_variables()

    def create_dict(self):
        return_dict = {}
        return_dict["LEVEL"] = self.LEVEL
        return_dict["WORD_DICT"] = self.WORD_DICT
        return_dict["SCORE"] = self.SCORE
        return_dict["CURRENT_PROGRESS_VALUE"] = self.CURRENT_PROGRESS_VALUE
        return_dict["WORD_LIST_LENGTH"] = self.WORD_LIST_LENGTH
        return_dict["CURRENT_ENGLISH_WORD"] = self.CURRENT_ENGLISH_WORD
        return_dict["CURRENT_JAPANESE_WORD"] = self.CURRENT_JAPANESE_WORD
        return_dict["REVISION_DICT"] = self.REVISION_DICT
        return return_dict

    def save_variables(self):
        var_dict = self.create_dict()

        out_file = open("variables.json", "w") 
    
        json.dump(var_dict, out_file) 
        
        out_file.close()

    def load_variables(self):
        variables = open('variables.json')
        data = json.load(variables)

        self.LEVEL = data["LEVEL"]
        self.WORD_DICT = data["WORD_DICT"]
        self.SCORE = data["SCORE"]
        self.CURRENT_PROGRESS_VALUE = data["CURRENT_PROGRESS_VALUE"]
        self.WORD_LIST_LENGTH = data["WORD_LIST_LENGTH"]
        self.CURRENT_ENGLISH_WORD = data["CURRENT_ENGLISH_WORD"]
        self.CURRENT_JAPANESE_WORD = data["CURRENT_JAPANESE_WORD"]
        self.REVISION_DICT = data["REVISION_DICT"]

    def reset(self):
        self.LEVEL = 0
        self.WORD_DICT = {}
        self.SCORE = 0
        self.CURRENT_PROGRESS_VALUE = 0
        self.WORD_LIST_LENGTH = 0
        self.CURRENT_ENGLISH_WORD = ""
        self.CURRENT_JAPANESE_WORD = ""
        self.REVISION_DICT = {}
        self.save_variables()