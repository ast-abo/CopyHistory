from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Copy History")
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

TextsFrame = ttk.Frame(tabs, padding="3 3 12 12")
TextList = Listbox(TextsFrame, height=6, width=25)
TextList.pack(expand=True, fill='both', padx=10, pady=10)

ImagesFrame = ttk.Frame(tabs, padding="3 3 12 12")
ImageList = Listbox(ImagesFrame, height=6, width=25)
ImageList.pack(side="left", expand=True, fill='both', padx=10, pady=10)
ImageDisplay = Label(ImagesFrame)
ImageDisplay.pack(side="right", expand=True, fill='both', padx=10, pady=10)

FilesFrame = ttk.Frame(tabs, padding="3 3 12 12")
FileList = Listbox(FilesFrame, height=6, width=25)
FileList.pack(expand=True, fill='both', padx=10, pady=10)

FavoritesFrame = ttk.Frame(tabs, padding="3 3 12 12")
FavoriteList = Listbox(FavoritesFrame, height=6, width=25)
FavoriteList.pack(expand=True, fill='both', padx=10, pady=10)

tabs.add(TextsFrame, text="Texts")
tabs.add(ImagesFrame, text="Images")
tabs.add(FilesFrame, text="Files")
tabs.add(FavoritesFrame, text="Favorites")
