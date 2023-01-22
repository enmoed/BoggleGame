#################################################################
# FILE : boggle_controller.py
# EXERCISE : intro2cs2 ex12 2020
# DESCRIPTION: Boggle controller.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Michal Kellner Eitan Moed
# WEB PAGES I USED: stackoverflow.com
# NOTES:
#################################################################

from boggle_gui import BoggleBoard, StartBoggle, EndBoggle
from boggle_model import BoggleModel
import boggle_board_randomizer
import ex12_utils as utils

WORD_DICTIONARY_FILEPATH = "boggle_dict.txt"

class BoggleController:
    """
    class for main controller of boggle game
    """
    def __init__(self):
        """
        function for creating game
        """
        self._board = boggle_board_randomizer.randomize_board()
        self._words_dict = utils.load_words_dict(WORD_DICTIONARY_FILEPATH)
        self._model = BoggleModel(self._board, self._words_dict)


    def check_path(self):
        """
        Function checks if path from GUI is a good path in model and updates
        points and word list if so
        :return: None
        """
        self._model.valid_word(self._gui.get_path())
        self._gui.set_points(self._model.get_points())
        self._gui.set_word_list(self._model.get_current_words())
        self._gui.clear_path()
        self._gui.clear_label()

    def run(self):
        """
        Calls program flow until user ends game
        :return: None
        """
        start = StartBoggle()
        start.run()
        self.game_loop()
        self.end = EndBoggle(self._model.get_points())
        self.end.new_game(self.new_game)
        self.end.run()

    def new_game(self):
        """
        Runs new game
        :return: None
        """
        game = BoggleController()
        self.end.end_game()
        game.run()


    def game_loop(self):
        """
        Runs Gui part of game
        :return:
        """
        self._gui = BoggleBoard(self._board)
        self._gui.set_submit_command(self.check_path)
        self._gui.set_points(self._model.get_points())
        self._gui.run()


if __name__ == "__main__":
    game = BoggleController()
    game.run()
