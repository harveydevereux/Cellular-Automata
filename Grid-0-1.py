import tkinter as tk
from tkinter import ttk
import numpy as np

class Menubar(tk.Menu):
    def __init__(self,parent,*args,**kwargs):
        self.parent=parent
        tk.Menu.__init__(self,parent,*args,**kwargs)

        # initialise menu vars
        self.menu_file=tk.Menu(self)
        self.menu_simulation=tk.Menu(self)
        self.menu_about=tk.Menu(self)

        self.menu_file.add_command(label="Save", command=self.save_gridfile)
        self.menu_file.add_command(label="Open", command=self.open_gridfile)

        #collect them in a list
        menus = ((self.menu_file,"File"),
                 (self.menu_simulation,"Simulation"),
                 (self.menu_about,"About"))
        # quickly deploy the menus
        for i,(var,lab) in enumerate(menus):
            self.add_cascade(menu=var,label=lab)
    def save_gridfile(self):
        pass
    def open_gridfile(self):
        pass


class Cell(tk.Button):
    def __init__(self,parent,*args,**kwargs):
        tk.Button.__init__(self, parent, bg="white",activebackground="white",
                           relief="flat", overrelief="flat", text="",
                           command=self.change_state,
                           *args, **kwargs)
    def change_state(self):
        if self.cget('bg') == 'white':
            self.configure(bg='black')
            self.configure(activebackground='black')
        else:
            self.configure(bg='white')
            self.configure(activebackground='white')


class App(tk.Canvas):
    def __init__(self, parent, n_rows, n_cols, *args, **kwargs):
        self.parent = parent
        tk.Canvas.__init__(self,parent, *args, **kwargs)

        self.menubar = Menubar(self)
        self.parent['menu'] = self.menubar

        self.n_rows = n_rows
        self.n_cols = n_cols

        self.cells = list()
        for i in range(0,self.n_rows*self.n_cols):
            self.cells.append(Cell(self))
            row,col = divmod(i,self.n_cols)
            self.cells[i].grid(sticky='nsew', row=row, column=col)
        self.grid_matrix = np.zeros((n_rows,n_cols))
        self.animate()
    def animate(self):
        r = np.random.randint(0,len(self.cells))
        self.cells[r].change_state()
        self.after(1,self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grid")
    root.resizable(tk.FALSE,tk.FALSE)
    root.option_add('*tearOff', tk.FALSE)
    main = App(root,n_rows=10,n_cols=10).grid(column=0,row=0,sticky='nesw')
    root.mainloop()
