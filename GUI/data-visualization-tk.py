import tkinter
import tkinter.messagebox
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from customtkinter import *
import sqlite3 as db
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from BoltxFinance.xFinance import BoltxPlaid
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from tkinter import ttk
from tkinter.ttk import Notebook, Style

df = BoltxPlaid().queryTrans()
x = df.groupby('category').sum()
x = x.drop('Transfer')
x = x.amount
labels = ['Community', 'Shops', 'Fees', 'Food & Drink', 'Investment', 'Payments', 'Recreation', 'Service', 'Shopping', 'Travel', 'Bank Fees', 'Payment', 'Food and Drink', 'Interest']

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    WIDTH = 1500
    HEIGHT = 750
    orange = "#ff461f"
    dark_red = "C40505"
    dark_gray = "898989"
    pink = 'FFB6B6'

    def __init__(self):
        super().__init__()

        self.title("Bolt Finance")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create tabs ============

        # Tab Theme
        style = Style()

        style.theme_create("dummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": self.dark_gray},
                "map": {"background": [("selected", self.dark_red)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use("dummy")

        self.overviewTab = ttk.Frame(self.tabControl)
        self.transTab = ttk.Frame(self.tabControl)
        self.debtTab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.overviewTab, text='Overview')
        self.tabControl.add(self.transTab, text='Transactions')
        self.tabControl.add(self.debtTab, text='Debt')

        self.tabControl.pack(expand=1, fill="both")

        # ============ create two frames per tab ============

        # Overview Tab Grid Layout Inside Tab (2x1)
        self.overviewTab.grid_columnconfigure(1, weight=5)
        self.overviewTab.grid_columnconfigure(0, weight=1)
        self.overviewTab.grid_rowconfigure(0, weight=1)

        self.frame1_left = customtkinter.CTkFrame(master=self.overviewTab)
        self.frame1_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.frame1_right = customtkinter.CTkFrame(master=self.overviewTab)
        self.frame1_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # Transactions Tab Grid Layout (2x1)
        self.transTab.grid_columnconfigure(1, weight=5)
        self.transTab.grid_columnconfigure(0, weight=1)
        self.transTab.grid_rowconfigure(0, weight=1)

        self.frame2_left = customtkinter.CTkFrame(master=self.transTab)
        self.frame2_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.frame2_right = customtkinter.CTkFrame(master=self.transTab)
        self.frame2_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame1_left.grid_columnconfigure(0, weight=1)  # empty row as spacing
        self.frame1_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame1_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame1_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame1_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame1_left, text="Manage", text_font=("Roboto Medium", -21))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=5)

        self.button_1 = customtkinter.CTkButton(master=self.frame1_left, width=300, text="Refresh", command=self.button_event)
        self.button_1.grid(row=2, column=0, pady=5, padx=5)

        self.button_2 = customtkinter.CTkButton(master=self.frame1_left, width=300, text="Update Accounts", command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=5, padx=5)

        self.button_3 = customtkinter.CTkButton(master=self.frame1_left, width=300, text="Update Transactions", command=self.button_event)
        self.button_3.grid(row=4, column=0, pady=5, padx=5)

        # ============ frame_right ============

        # configure grid layout (3x7)
        # self.frame_right.rowconfigure((0, 1), weight=1)
        self.frame1_right.rowconfigure((2, 3, 4, 5 ,6, 7), weight=3)
        self.frame1_right.columnconfigure((0, 1), weight=1)
        self.frame1_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame1_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=2, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_info.rowconfigure(1, weight=2)

        # Net Worth
        self.label_info_netWorth = customtkinter.CTkLabel(master=self.frame_info, text="Net Worth", text_font=("Arial Bold", 12), height=30, corner_radius=6)
        self.label_info_netWorth.grid(column=0, row=0, sticky="nwe", padx=5, pady=5)

        self.label_netWorth = customtkinter.CTkLabel(master=self.frame_info, text="$50000", text_font=("Arial Bold", 36), height=75, corner_radius=6, fg_color=("white", "gray38"))
        self.label_netWorth.grid(column=0, row=1, sticky="nwe", padx=5, pady=5)

        # Total Checkings
        self.label_info_totalChk = customtkinter.CTkLabel(master=self.frame_info, text="Total Checkings", text_font=("Arial Bold", 12), height=30, corner_radius=6)
        self.label_info_totalChk.grid(column=1, row=0, sticky="nwe", padx=5, pady=5)

        self.label_totalChk = customtkinter.CTkLabel(master=self.frame_info, text="1000", text_font=("Arial Bold", 36), height=75, corner_radius=6, fg_color=("white", "gray38"))
        self.label_totalChk.grid(column=1, row=1, sticky="nwe", padx=5, pady=5)

        # TTotal Savings
        self.label_info_totalSav = customtkinter.CTkLabel(master=self.frame_info, text="Total Savings", text_font=("Arial Bold", 12), height=30, corner_radius=6)
        self.label_info_totalSav.grid(column=2, row=0, sticky="nwe", padx=5, pady=5)

        self.label_totalSav = customtkinter.CTkLabel(master=self.frame_info, text="0", text_font=("Arial Bold", 36), height=75, corner_radius=6, fg_color=("white", "gray38"))
        self.label_totalSav.grid(column=2, row=1, sticky="nwe", padx=5, pady=5)

        self.label_info_totalInv = customtkinter.CTkLabel(master=self.frame_info, text="Total Investments", text_font=("Arial Bold", 12), height=30, corner_radius=6)
        self.label_info_totalInv.grid(column=3, row=0, sticky="nwe", padx=5, pady=5)

        self.label_totalInv = customtkinter.CTkLabel(master=self.frame_info, text="400", text_font=("Arial Bold", 36), height=75, corner_radius=6, fg_color=("white", "gray38"))
        self.label_totalInv.grid(column=3, row=1, sticky="nwe", padx=5, pady=5)

        self.label_info_totalDebt = customtkinter.CTkLabel(master=self.frame_info, text="Total Debt", text_font=("Arial Bold", 12), height=30, corner_radius=6)
        self.label_info_totalDebt.grid(column=4, row=0, sticky="nwe", padx=5, pady=5)

        self.label_totalDebt = customtkinter.CTkLabel(master=self.frame_info, text="20000", text_font=("Arial Bold", 36), height=75, corner_radius=6, fg_color=("white", "gray38"))
        self.label_totalDebt.grid(column=4, row=1, sticky="nwe", padx=5, pady=5)

        # ============ frame_right ============




    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()