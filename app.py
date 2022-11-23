import tkinter

class MainApp(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.init_main


    def init_main(self):
        toolbar = tkinter.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tkinter.TOP, fill=tkinter.X)


if __name__ == '__main__':
    master = tkinter.Tk()
    app = MainApp(master)
    app.pack()
    master.title('My Finance')
    master.geometry('800x400+300+200')
    master.mainloop()
    