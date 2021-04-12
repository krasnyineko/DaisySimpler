from os import stat_result, truncate
import tkinter as tk
from tkinter import Button, filedialog
from dataclasses import dataclass
from pathlib import Path
from tkinter.constants import LEFT, NONE, TOP


# def select_sample_folder():
#     ask = filedialog.askdirectory()
#     if not ask:
#         print("Directory selection was canceled")
#         return
#     directory = Path(ask)


# root = tk.Tk()
# root.title("Bank editor")
# root.geometry("500x600")

# # samplelist = tk.Listbox(root, selectmode=tk.EXTENDED, activestyle=tk.NONE)
# # samplelist.insert(1, bar)
# # samplelist.insert(2, "This is 2")
# # samplelist.insert(3, "This is 3")
# # samplelist.insert(4, "This is 4")
# # samplelist.insert(5, "This is 5")
# # samplelist.pack()

# # bar = tk.Canvas(root)
# # bar.create_rectangle(0, 0, 100, 100, fill="#F00")
# # bar.create_text(50, 15, text="Howdy do")
# # bar.pack()
# # filename = filedialog.askdirectory()
# # print(filename)
# btn_filedialog = tk.Button(root, command=select_sample_folder)
# btn_filedialog.pack()
# root.mainloop()


class SampleBrowser(tk.Frame):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master=master, *args, **kwargs)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=2)
        btn = Button(self, text="Select folder")
        btn.grid(column=0, row=0, sticky="nesw")
        lis = tk.Listbox(self)
        lis.grid(column=0, row=1, sticky=(tk.N, tk.E, tk.S, tk.W))

    def open_folder_dialog(self):
        answer = filedialog.askdirectory()
        if not answer:
            return
        selected_directory = Path(answer)


class MainApplication(tk.Frame):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master=master, *args, **kwargs)
        self.config(bg="red")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        SampleBrowser(self, bg="green").grid(column=0, row=0, sticky="nesw")
        SampleBrowser(self).grid(column=1, row=0, sticky="nesw")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bank editor")
    root.geometry("500x600")
    MainApplication(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()