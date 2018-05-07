import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcdefaults()
from PIL import Image, ImageTk
import pandas as pd

from cs_299.model import TweetQuery
tweet_query = TweetQuery()


def main():
    win = tk.Tk()
    win.title("Twitter Word Frequency")

    label = ttk.Label(win, text='User Handel')
    label.grid(column=0, row=0)

    ttk.Label(win, text="Enter a name:").grid(column=0, row=0)

    name = tk.StringVar()
    entry = ttk.Entry(win, width=12, textvariable=name)
    entry.grid(column=0, row=1)

    """Image making"""
    img = ImageTk.PhotoImage(Image.open("wordCount.png"))
    panel = tk.Label(win, image=img)
    panel.grid(column=0, row=2)

    but= ttk.Button(win, text="click", command=lambda: clicked(name.get(), panel))
    but.grid(column=1, row=1)

    win.mainloop()


def clicked(user, pan):
    global tweet_query
    print(user)
    wordCount = tweet_query.get_most_frequent_words(user, 5)
    print(wordCount)
    makeGraph(wordCount)

    imgUpdate = ImageTk.PhotoImage(Image.open("wordCountRELOAD.jpg"))
    pan.configure(image=imgUpdate)
    pan.image = imgUpdate


def makeGraph(dic):
    s = pd.Series(dic)
    s=s.sort_values(ascending=False)
    print(s)

    ax = s.iloc[:len(dic)].plot(kind="barh")
    ax.invert_yaxis()

    plt.savefig('wordCountRELOAD.jpg', bbox_inches='tight')
    plt.clf()


if __name__ == '__main__':
    main()
