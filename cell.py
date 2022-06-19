import sys
from tkinter import Button,Label
import random
import settings
import ctypes
import sys

class Cell:
    all=[]
    cell_count_label_object=None
    cell_count = settings.CELL_COUNT
    def __init__(self,x,y,):
        self.is_mine = False
        self.is_opened = False
        self.cell_btn_object = None
        self.is_mine_candidate = False
        self.x=x
        self.y=y
        #append the object to the Cell.all list
        Cell.all.append(self)
    def create_btn_object(self, location):
        btn= Button(
            location,
            width=12,
            height=4,
            # text=f"{self.x},{self.y}"
        )
        btn.bind('<Button-1>', self.left_click_actions)      #used to deal with events/actions
        btn.bind('<Button-3>', self.right_click_actions)      #button-1 left click
        self.cell_btn_object = btn                            #button-3 right click

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{settings.CELL_COUNT}",
            font=("", 30)

        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell in self.surrounded_cells:
                    cell.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'YOU WON', 0)

       # Cancel Left and Right Click events if cell is already opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self,x,y):
        #return a cell object based on the value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter=0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            # print(self.surrounded_cells_mines_length)
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            #Replace the text of cell count label with the newer count
            Cell.cell_count -= 1
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}" )
        #Config color back to systembuttonface from candidate mine color
        self.cell_btn_object.configure(bg='SystemButtonFace')
        #Mark the cell as opened(use is as the last line of this method)
        self.is_opened = True
        # Cancel Left and Right Click events if cell is already opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def show_mine(self):
        #A logic to interrupt the game and display a message that player is lost!
        ctypes.windll.user32.MessageBoxW(0, 'You Clicked on a mine', 'Game Over',0)
        # self.cell_btn_object.configure(bg='red')
        sys.exit()

    def right_click_actions(self, event):
        # print("I am right clicked")
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg='orange')
            self.is_mine_candidate=True
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_mine_candidate=False

    @staticmethod
    def randomize_mines():                               #randomly picking cell and converting it into mine
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        # print(picked_cells)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):                       #magic method to represent object
        return f"Cell({self.x}, {self.y})"    #automat. gets called when we print an object
                                              #we can return cell(object) reprst. in desired string format using this