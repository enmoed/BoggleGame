import tkinter as tk

BUTTON_ACTIVE_COLOR = 'gray'
BUTTON_NORM_COLOR = 'lightgray'
LABEL_BG_COLOR = "ghostwhite"
DEFAULT_COLOR = "RoyalBlue3"
GAME_NAME = "BOGGLE!"
TOTAL_TIME = 180

LETTER_BUTTON_STYLE = {"font": ("Courier", 50), "borderwidth": 1,
                       "relief": tk.RAISED, "bg": BUTTON_NORM_COLOR,
                       "activebackground": BUTTON_ACTIVE_COLOR}

SMALL_BUTTON_STYLE = {"font": ("Courier", 20), "borderwidth": 1,
                      "relief": tk.RAISED, "bg": BUTTON_NORM_COLOR,
                      "activebackground": BUTTON_ACTIVE_COLOR}

TITLE_LABEL_STYLE = {"font": ("Courier", 50),
                     "bg": DEFAULT_COLOR, "width": 25,
                     "text": GAME_NAME, "fg": "yellow"}

DISPLAY_LABEL_STYLE = {"font": ("Courier", 30), "bg": LABEL_BG_COLOR,
                       "width": 25, "relief": "ridge"}

INNER_FRAME_STYLE = {"bg": DEFAULT_COLOR, "highlightbackground": DEFAULT_COLOR,
                     "highlightthickness": 10}

RIGHT_COL_LABEL = {"font": ("Courier", 30), "bg": LABEL_BG_COLOR, "width": 5,
                   "relief": "ridge"}


class BoggleBoard:
    def __init__(self, board):
        root = tk.Tk()
        root.title(GAME_NAME)
        #root.resizable(False, False)
        self._main_board = root
        self._main_board.geometry("700x700")
        self._board = board
        self._path = []
        self._time_remaining = TOTAL_TIME
        self._flash_time = 400
        self._title = tk.Label(self._main_board, **TITLE_LABEL_STYLE)
        self._l_side_frame = tk.Frame(self._main_board, **INNER_FRAME_STYLE)
        self._grid_frame = tk.Frame(self._l_side_frame)
        self._display_label = tk.Label(self._l_side_frame,
                                       **DISPLAY_LABEL_STYLE)
        self._submit_button = tk.Button(self._l_side_frame, text="SUBMIT",
                                        **SMALL_BUTTON_STYLE)
        self._r_side_frame = tk.Frame(self._main_board, **INNER_FRAME_STYLE)
        self._word_list = tk.Label(self._r_side_frame, **RIGHT_COL_LABEL)
        self._timer = tk.Label(self._r_side_frame, **RIGHT_COL_LABEL)
        self._points = tk.Label(self._r_side_frame, **RIGHT_COL_LABEL)
        self._pack_widgets()
        self._create_buttons()

    def _pack_widgets(self):
        self._title.pack(side=tk.TOP, fill=tk.BOTH)
        self._l_side_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._grid_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self._display_label.pack(side=tk.LEFT, fill=tk.BOTH)
        self._submit_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._r_side_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._timer.pack(side=tk.TOP, fill=tk.BOTH)
        self._points.pack(side=tk.TOP, fill=tk.BOTH)
        self._word_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def set_display(self, ind):
        self._display_label["text"] += self._board[ind[0]][ind[1]]

    def set_word_list(self, word_list):
        str_words = ""
        for word in word_list:
            str_words += word + "\n"
        self._word_list["text"] = str_words
        if len(word_list) > 12:
            word_size = 12
            if (40 - len(word_list)) > word_size:
                word_size = 40 - len(word_list)
            self._word_list["font"] = ("Courier", word_size)

    def set_points(self, points):
        self._points["text"] = str(points)

    def get_path(self):
        return self._path

    def set_submit_command(self, fun):
        self._submit_button["command"] = fun

    def clear_path(self):
        self._path = []

    def clear_label(self):
        self._display_label["text"] = ""

    def start_timer(self):
        self._timer["text"] = str(TOTAL_TIME // 60) + ":" + str(
            TOTAL_TIME % 60).zfill(2)
        self._timer.after(1000, self.set_time)

    def flash(self):
        if self._flash_time > 20:
            self._flash_time -= 10
        if self._l_side_frame["highlightbackground"] == "white":
            self._l_side_frame["highlightbackground"] = "black"
            self._r_side_frame["highlightbackground"] = "white"
        else:
            self._l_side_frame["highlightbackground"] = "white"
            self._r_side_frame["highlightbackground"] = "black"
        if self._time_remaining > 1:
            self._main_board.after(int(self._flash_time), self.flash)

    def set_time(self):
        self._time_remaining -= 1
        if self._time_remaining == 10:
            self.flash()
        self._timer["text"] = str(self._time_remaining // 60) + ":" + str(
            self._time_remaining % 60).zfill(2)
        if self._time_remaining == 0:
            self._main_board.destroy()
            return
        self._timer.after(1000, self.set_time)

    def _create_buttons(self):
        for i in range(len(self._board[0])):
            tk.Grid.columnconfigure(self._grid_frame, i, weight=1)

        for i in range(len(self._board)):
            tk.Grid.rowconfigure(self._grid_frame, i, weight=1)

        for i in range(len(self._board[0])):
            for j in range(len(self._board)):
                self._make_button(str(self._board[i][j]), i, j)

    def _make_button(self, button_char, row, col):
        button = tk.Button(self._grid_frame, text=button_char,
                           **LETTER_BUTTON_STYLE)
        button.grid(row=row, column=col, sticky=tk.NSEW)

        def _on_release(event):
            button['background'] = BUTTON_NORM_COLOR
            self.set_display((row, col))
            self._path.append((row, col))

        button.bind("<Button>", lambda event: button.configure(
            background=BUTTON_ACTIVE_COLOR))
        button.bind("<ButtonRelease>", _on_release)

    def run(self):
        self.start_timer()
        self._main_board.mainloop()


class StartBoggle:
    def __init__(self):
        root = tk.Tk()
        root.title(GAME_NAME)
        root.resizable(False, False)
        self._main_board = root
        self._main_board.geometry("700x700")
        self._title = tk.Label(self._main_board, **TITLE_LABEL_STYLE)
        self._title.pack(side=tk.TOP)
        self._outer_frame = tk.Frame(self._main_board,
                                     bg=DEFAULT_COLOR,
                                     highlightbackground=DEFAULT_COLOR,
                                     highlightthickness=10)
        self._outer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._start_button = tk.Button(self._outer_frame, text="START",
                                       **LETTER_BUTTON_STYLE,
                                       command=self.start_game)
        self._start_button.pack(side=tk.BOTTOM, expand=True)

    def start_game(self):
        self._main_board.destroy()

    def run(self):
        self._main_board.mainloop()


class EndBoggle:
    def __init__(self, points):
        root = tk.Tk()
        root.title(GAME_NAME)
        root.resizable(False, False)
        self._main_board = root
        self._main_board.geometry("700x700")
        self._title = tk.Label(self._main_board, **TITLE_LABEL_STYLE)
        self._title.pack(side=tk.TOP)

        self._outer_frame = tk.Frame(self._main_board,
                                     bg=DEFAULT_COLOR,
                                     highlightbackground=DEFAULT_COLOR,
                                     highlightthickness=10)
        self._outer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._points = tk.Label(self._outer_frame,
                                font=("Courier", 50),
                                bg=DEFAULT_COLOR, width=25,
                                text="YOUR FINAL SCORE: " + str(points),
                                fg="black")
        self._points.pack(side=tk.TOP, expand=True)
        self._new_game_button = tk.Button(self._outer_frame, text="NEW GAME",
                                          **LETTER_BUTTON_STYLE)
        self._new_game_button.pack(side=tk.BOTTOM, expand=True)
        self._end_button = tk.Button(self._outer_frame, text="END",
                                     **LETTER_BUTTON_STYLE,
                                     command=self.end_game)
        self._end_button.pack(side=tk.BOTTOM, expand=True)

    def end_game(self):
        self._main_board.destroy()

    def new_game(self, fun):
        self._new_game_button["command"] = fun

    def run(self):
        self._main_board.mainloop()
