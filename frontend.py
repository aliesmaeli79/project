import main
from main import *
from cProfile import label
from cgitb import text
from tkinter import *
from tkinter.ttk import Labelframe
from tkinter import filedialog




main.write_read()
root = Tk()

# root.iconbitmap("gui.ico")
root.title('search engine')
root.geometry("700x600")


def add_file():
    # root.filename = filedialog.askopenfilename(initialdir="", title="selecet a text file",
    #                                            filetype=[("txt", "*.txt"), ("all", "*.*")])
    # root.filename = filedialog.asksaveasfilename(initialdir="C:\Users\aesma\PycharmProjects\pythonProject1\document")
    pass


def search():
    if my_entry.get()=="":
        my_entry.delete(0, END)
        result_text.delete(0.0, END)
        result_text.insert(0.0, "لطفا کوئری را وارد نمایید")
    else:
        data = main.search(my_entry.get())
        if data==0:
            result="سندی یافت نشد "
            my_entry.delete(0, END)
            result_text.delete(0.0, END)
            result_text.insert(0.0, result)
        else:
            my_entry.delete(0, END)
            result_text.delete(0.0, END)
            result_text.insert(0.0, data)


search_frame = Labelframe(root, text="search in documents")
search_frame.pack(pady=20)

my_entry = Entry(search_frame, width=90)
my_entry.pack(pady=20, padx=20)

result_frame = Labelframe(root, text="result")
result_frame.pack(pady=5)

result_text = Text(result_frame, height=5, width=73)
result_text.pack(pady=5)

button_frame = Frame(root)
button_frame.pack(pady=5)

search_button = Button(button_frame, text="search", fg="#3a3a3a", command=search)
search_button.grid(row=0, column=0, padx=5)

add_button = Button(button_frame, text="add file", fg="#3a3a3a", command=add_file)
add_button.grid(row=0, column=1)

root.mainloop()