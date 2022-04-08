from tkinter import *

def change():
	entry = Entry(font=('Verdana', 16), width=4)
	entry=int(entry.get())
	entry=unos*100
	output_label.configure(text = 'Converted: {:.1f}'.format(entry))
	entry.delete(0,END)

root = Tk()
message_label = Label(text='Enter the number of meters',font=('Verdana', 16))
output_label = Label(font=('Verdana', 16))
entry = Entry(font=('Verdana', 16), width=4)
calc_button = Button(text='Ok', font=('Verdana', 16),command=change)
message_label.grid(row=0, column=0)
entry.grid(row=0, column=1)
calc_button.grid(row=0, column=2)
output_label.grid(row=1, column=0, columnspan=3)
mainloop()