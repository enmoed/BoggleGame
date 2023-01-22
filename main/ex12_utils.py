#################################################################
# FILE : ex12_utils.py
# WRITER : Michal Kellner , michal.kellner , 340978758
# WRITER : Eitan Moed , enmoed , 210016150
# EXERCISE : intro2cs2 ex12 2020
# DESCRIPTION: Logic functions for Boggle game.
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED: stackoverflow.com
# NOTES:
#################################################################

def load_words_dict(file_path):
    """
    loads words from file to dictionary
    :param file_path: file of word list
    :return: dictionary of words from file
    """
    with open(file_path, "r") as words_file:
        return {word[:-1]:True for word in words_file}

def _helper_valid(tuple_1, tuple_2):
    """
    checks if last two coordinates are valid
    :param tuple_1: last coordinate
    :param tuple_2: second to last coordinate
    :return: boolean if valid
    """
    if abs(tuple_1[0] - tuple_2[0]) > 1 or abs(tuple_1[1] - tuple_2[1]) > 1:
        return False
    return True

def check_board_size(board):
    """
    gets length and width of board
    :param board: board
    :return: # of rows, # of columns
    """
    return len(board), len(board[0])

def is_valid_path(board, path, words):
    """
    checks if path received is valid
    :param board: boggle board list of lists
    :param path: list of coordinates of word
    :param words: word dictionary
    :return: word if valid or None
    """
    # uses same coordinate twice?
    if len(set(path)) != len(path):
        return None
    # check tuples are neighbors
    for i in range(len(path) - 1):
        if not _helper_valid(path[i], path[i + 1]):
            return None
    # check its in radius of the board
    rows, columns = check_board_size(board)
    word_string = ""
    for y,x in path:
        if y > rows - 1 or x > columns - 1 or y < 0 or x < 0:
            return None
        word_string += board[y][x]
    # checks its in word dictionary
    if word_string in words:
        return word_string

def find_length_n_words(n, board, words):
    """
    finds words of n length in board
    :param n: length of words
    :param board: list of list of strings
    :param words: words from dictionary
    :return: list of tuples of word and path
    """
    # make a list of 16 coordinates
    coordinates_list = []
    for row in range(len(board)):
        for column in range(len(board[0])):
            coordinates_list.append((row, column))
    # write all combinations of length n from the list
    total_list = []
    _helper_permutations(find_words(words, n), coordinates_list, n, [],
                         total_list, board, "")
    return total_list

def _helper_permutations(smaller_list, coordinates_list, n, path,
                         total_list, board, word_candidate):
    """
    appends list of coordinates to total list if valid
    :param smaller_list: reduced valid list to search for
    :param coordinates_list: list of coordinates from board
    :param n: length of path
    :param path: path candidate
    :param total_list: list of all valid candidates
    :param board: list of list of board
    :param word_candidate: word candidate of path
    :return: None
    """
    if not smaller_list:
        return
    if len(path) > 1 and not _helper_valid(path[-2], path[-1]):
        return
    if len(word_candidate) == n:
        total_list.append((word_candidate, path))
    else:
        for coordinate in coordinates_list:
            if coordinate not in path:
                new_small_list = []
                board_letter = board[coordinate[0]][coordinate[1]]
                for word in smaller_list:
                    valid_candidate = True
                    for i in range(len(board_letter)):
                        if word[i+len(word_candidate)] != board_letter[i]:
                            valid_candidate = False
                            break
                    if valid_candidate:
                        new_small_list.append(word)
                _helper_permutations(new_small_list, coordinates_list, n,
                                     path + [coordinate], total_list, board,
                                     word_candidate+board_letter)

def find_words(words, n):
    """
    finds all words in dictionary of n length
    :param words: dictionary of words
    :param n: length of requested words
    :return: list of valid words
    """
    words_list = []
    for word in words:
        if len(word) == n:
            words_list.append(word)
    return words_list
