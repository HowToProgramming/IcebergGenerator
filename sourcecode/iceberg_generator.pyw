from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from PIL import ImageTk

from helpers.draw_iceberg import draw_iceberg

class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        self.title("Iceberg Generator")
        self.iconphoto(False, ImageTk.PhotoImage(file='resources/iceberg.jpg'))
        self.geometry('1280x720')
        self.level = 0
        self.entries = []
        for i in range(3):
            self.add_level()
        self.add_level_button = ttk.Button(self, text='Add More Level', command=self._add_level)
        self.add_level_button.grid(column=1, row=self.level+1)
        self.generate_button = ttk.Button(self, text='Generate', command=self._generate)
        self.generate_button.grid(column=0, row=self.level+1)
        self.generate()
        self.save_button = ttk.Button(self, text='Save', command=self.save)
        self.save_button.grid(column=1, row=self.level+2)
    
    def save(self):
        levels = []
        for entry in self.entries:
            levels.append(entry.get("1.0", "end").split("\n")[:-1])
        f = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        draw_iceberg(levels, save=f.name)

    def generate(self):
        levels = []
        for entry in self.entries:
            levels.append(entry.get("1.0", "end").split("\n")[:-1])
        
        image = draw_iceberg(levels, save=False)
        image = image.resize((480, 640))
        image = ImageTk.PhotoImage(image)
        self.imshow = Label(self, image=image)
        self.imshow.image = image
        self.imshow.place(x=500, y=0)
    
    def _generate(self):
        self.generate()
        
    def add_level(self):
        self.level += 1
        label = ttk.Label(self, text=f"Level {self.level}")
        label.grid(column=0, row=self.level)
        entry = Text(height=5, width=50)
        # Initial Word
        if self.level == 1:
            entry.insert(INSERT, 'This is the Level 1 of the iceberg\nMost of people know this')
        if self.level == 2:
            entry.insert(INSERT, "This is the Level 2 of the iceberg\nSome of people know this")
        if self.level == 3:
            entry.insert(INSERT, "This is the Level 3 of the iceberg\na few people know this")
    
        entry.grid(column=1, row=self.level)
        self.entries.append(entry)
    
    def _add_level(self):
        self.add_level()
        self.add_level_button.grid(column=1, row=self.level+1)
        self.generate_button.grid(column=0, row=self.level+1)
        self.save_button.grid(column=1, row=self.level+2)

app = App()
app.mainloop()
