from tkinter import *
from cell import Cell
import settings
import utils

root = Tk()
# override the settings of the window
root.configure(bg="black")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Minesweeper Game")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg='black' , #change later to black
    width = settings.WIDTH,
    height = utils.height_perct(25)
)
top_frame.place(x=0,y=0)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Minesweeper Game',
    font=('', 48)
)
game_title.place(
    x=utils.width_perct(25), y=0
)

left_frame = Frame(
    root,
    bg='black' , #change later to black
    width = utils.width_perct(25),
    height = utils.height_perct(75)
)
left_frame.place(x=0,y=utils.height_perct(25))

center_frame = Frame(
    root,
    bg='black', #change later to black
    width = utils.width_perct(75),
    height = utils.height_perct(75)
)
center_frame.place(x=utils.width_perct(25),y=utils.height_perct(25))


for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        cxy = Cell(x,y)
        cxy.create_btn_object(center_frame)
        cxy.cell_btn_object.grid(
            column=y, row=x
        )
#call the label from the cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0,y=0)

# print(Cell.all)
Cell.randomize_mines()
# Run the window
root.mainloop()
