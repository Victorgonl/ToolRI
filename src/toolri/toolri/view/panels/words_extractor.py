from ..styles import *
from .panel import Panel

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController


class WordsExtractor(Panel):

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller)
        self.canvas = ToolRICanvas(self._master)
        self.canvas.pack(expand=True, fill="both", side="bottom")
        self.__entries_words = []
        self.__entries_labels = []
        self.__apply_button = None
        self.__cancel_button = None
        self.entity = None
        self.__init_frame()

    def __init_frame(self):
        label = ToolRILabel(master=self.canvas, text="Words Extractor")
        label.pack(pady=(10, 0))
        self.frame = ToolRIScrollableFrame(
            self.canvas,
            fg_color=TEXT_FG_COLOR,
            corner_radius=25,
        )
        self.frame.pack(expand=True, fill="both", side="bottom", padx=10, pady=(0, 10))
        self._bind_key("<Return>", self.__send_words)

    def __create_label(self, row, column, label_name):
        label = ToolRILabel(self.frame, label_name)
        label.grid(row=row, column=column)
        self.__entries_labels.append(label)

    def __create_entry(self, row, column, entry_value):
        entry = ToolRIEntry(self.frame, justify="center", width=175)
        entry.insert("end", entry_value)
        entry.grid(row=row, column=column, pady=2, sticky="nw")
        self.__entries_words.append(entry)

    def set_words_and_boxes(self, words, boxes):
        self.clear()
        self.__words = words
        self.__boxes = boxes
        for i, word in enumerate(words):
            self.__create_label(row=i, column=0, label_name=i + 1)
            self.__create_entry(row=i, column=1, entry_value=word)
        self.__apply_button = ToolRIButton(
            self.frame, text="Create", command=self.__send_words
        )
        self.__apply_button.grid(
            row=len(self.__entries_words),
            column=1,
            sticky="n",
            pady=(10, 0),
        )
        self.canvas.update_idletasks()
        self.__entries_words[0].focus()

    def __send_words(self, event=None):
        if not self.__entries_words or not self.__boxes:
            return
        words, boxes = [], []
        for entry_word, box in zip(self.__entries_words, self.__boxes):
            words.append(entry_word.get())
            boxes.append(box)
        self._toolri_controller.receive_words_and_boxes(words, boxes)

    def clear(self):
        self.frame._parent_canvas.yview_moveto(0.0)
        for label in self.__entries_labels:
            label.grid_forget()
        for entry in self.__entries_words:
            entry.grid_forget()
        if self.__apply_button is not None:
            self.__apply_button.destroy()
        if self.__cancel_button is not None:
            self.__cancel_button.destroy()
        self.__entries_words = []
        self.__entries_labels = []
        self.__words = None
        self.__boxes = None
