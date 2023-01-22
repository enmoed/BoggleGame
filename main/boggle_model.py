#################################################################
# FILE : boggle_model.py
# WRITER : Michal Kellner , michal.kellner , 340978758
# WRITER : Eitan Moed , enmoed , 210016150
# EXERCISE : intro2cs2 ex12 2020
# DESCRIPTION: Boggle model.
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED: stackoverflow.com
# NOTES:
#################################################################

import ex12_utils as utils

class BoggleModel:
    """
    class for logic of boggle game
    """
    def __init__(self, board, words):
        """
        init function for logic part of game
        :param board: list of list of strings for board of boggle
        :param words: list of current words
        """
        self.__board = board
        self.__points = 0
        self.__words_dict = words
        self.__current_words = []

    def valid_word(self, path):
        """
        checks if word guessed is valid
        :param path: path of word guessed
        :return: None
        """
        valid_word = utils.is_valid_path(self.__board, path, self.__words_dict)
        if valid_word:
            self.check_word(valid_word)

    def check_word(self, word):
        """
        adds word to word list
        :param word: word guessed
        :return: None
        """
        if word not in self.__current_words:
            self.__current_words.append(word)
            self.__points += len(word) ** 2

    def get_current_words(self):
        """
        :return: current word list
        """
        return self.__current_words

    def get_points(self):
        """
        :return: current points
        """
        return self.__points

