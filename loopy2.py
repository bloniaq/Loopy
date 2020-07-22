from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import engine
import os


class Application():

    def __init__(self):

        self.looper = ''
        self.root = Tk()
        self.root.withdraw()

        self.mainwindow = Toplevel(self.root, height=600, width=600)
        self.folder_path = StringVar()

        self.mainwindow.title("Loopy2")
        # toplevel_1.withdraw()
        frame_main = Frame(self.mainwindow, height=200, padding=20, takefocus="false", width=200)
        frame_main.grid(row=0, column=0)
        self.tree_fileslist = Treeview(frame_main, selectmode="extended")
        self.tree_fileslist.grid(row=0, column=0)
        self.tree_fileslist.bind("<Double-1>", self.tree_doubleclick)
        frame_buttons = Frame(frame_main, height=200, padding=20, relief="groove", width=200)
        frame_buttons.grid(row=1, column=0)
        button_open = Button(frame_buttons, text="Browse", command=self.browse_button)
        button_open.grid(row=0, column=0, columnspan=2)
        btn_play = Button(frame_buttons, command=self.play, text="Play")
        btn_play.grid(row=1, column=0)
        btn_stop = Button(frame_buttons, command=self.stopping, text="Stop")
        btn_stop.grid(row=1, column=1)
        # dirpath = 

    def run(self):
        """ Makes infinite loop
        """
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainwindow.mainloop()

    def browse_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)
        print(filename)
        self.load_files(filename)
        return filename

    def play(self):
        if self.looper:
            if self.looper.loop:
                if self.tree_fileslist.focus() == self.file_id:
                    return
                else:
                    self.stopping()
        self.file_id = self.tree_fileslist.focus()
        if self.file_id != '':
            audiofile = self.fileslist[self.file_id]
        self.looper = engine.WavePlayerLoop(audiofile)
        self.looper.play()
        print("playing: ", audiofile)

    def stopping(self):
        print("stopping")
        self.looper.stop()

    def load_files(self, directory):
        self.fileslist = {}
        for row in self.tree_fileslist.get_children():
            self.tree_fileslist.delete(row)
        for file in os.listdir(directory):
            if file.endswith(".mp3") or file.endswith(".wav"):
                itemid = self.tree_fileslist.insert('', 'end', text=file)
                self.fileslist[itemid] = os.path.join(directory, file)
                print("\nzaładowano:")
                for key in self.fileslist.keys():
                    print(self.fileslist[key])

    def on_closing(self):
        if self.looper:
            if self.looper.loop:
                self.looper.stop()
        self.root.destroy()

    def tree_doubleclick(self, event):
        self.play()


if __name__ == '__main__':

    app = Application()
    app.run()
