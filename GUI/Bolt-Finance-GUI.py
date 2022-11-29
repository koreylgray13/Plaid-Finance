from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook, Style
import customtkinter
from tksheet import Sheet
import matplotlib.pyplot as plt


class App(customtkinter.CTk):
    WIDTH = 1500
    HEIGHT = 750

    def __init__(self):
        super().__init__()

        self.title("Bolt Finance")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.iconbitmap(r"C:\Users\kgray\Projects\projectBolt\GUI\icon.ico")

        # Finance Data
        # totalChk, totalSav, totalDebt, netWorth = BoltxFinance().totalBalances()
        # totalInv = BoltxFinance.xrpBalance()
        #
        # loans = BoltxFinance().queryLoans()
        # loan_columns = list(loans.columns)
        # loans = loans.values.tolist()
        #
        # accounts = BoltxFinance().queryAccounts()
        # account_columns = list(accounts.columns)
        # accounts = accounts.values.tolist()
        #
        # transactions = BoltxFinance().queryTrans()
        # transactions_columns = list(transactions.columns)
        #
        # transByCategory = transactions.groupby('category').sum()
        # transByCategory = transByCategory.drop('Transfer')
        # transByCategory = transByCategory.amount
        # plt.style.use('classic')

        # Initialize Tabs
        self.tabControl = ttk.Notebook(self)

        # Style
        s = Style()
        s.theme_use('clam')

        self.overviewTab = ttk.Frame(self.tabControl)
        self.transTab = ttk.Frame(self.tabControl)
        self.debtTab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.overviewTab, text='Overview')
        self.tabControl.add(self.transTab, text='Transactions')
        self.tabControl.add(self.debtTab, text='Debt')

        self.tabControl.pack(expand=1, fill="both")

        # < ============ Overview Tab ============ >
        # Overview Tab Grid Layout (2x1)
        self.overviewTab.grid_columnconfigure(0, weight=1)
        self.overviewTab.grid_columnconfigure(1, weight=9)
        self.overviewTab.grid_rowconfigure(0, weight=1)

        # Create Two Frames
        self.t1LFrame = customtkinter.CTkFrame(master=self.overviewTab)
        self.t1LFrame.grid(row=0, column=0, sticky="nswe", padx=1, pady=1)

        self.t1RFrame = customtkinter.CTkFrame(master=self.overviewTab)
        self.t1RFrame.grid(row=0, column=1, sticky="nswe", padx=1, pady=1)

        # ============ Left Frame ============
        # Grid Layout (1x11)
        self.t1LFrame.grid_columnconfigure(0, weight=1)
        self.t1LFrame.grid_rowconfigure(5, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.t1LFrame, text="Manage Accounts",
                                              text_font=("Roboto Medium", -21))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=5)

        self.button_1 = customtkinter.CTkButton(master=self.t1LFrame, width=250, text="Refresh",
                                                command=None, fg_color='gray60', text_color='black')
        self.button_1.grid(row=2, column=0, pady=5, padx=5)

        self.button_2 = customtkinter.CTkButton(master=self.t1LFrame, width=250, text="Update Accounts",
                                                command=None, fg_color='gray60', text_color='black')
        self.button_2.grid(row=3, column=0, pady=5, padx=5)

        self.button_3 = customtkinter.CTkButton(master=self.t1LFrame, width=250, text="Update Transactions",
                                                command=None, fg_color='gray60', text_color='black')
        self.button_3.grid(row=4, column=0, pady=5, padx=5)

        # ============ Right Frame ============
        # Grid Layout (3x4)
        self.t1RFrame.rowconfigure(0, weight=1)
        self.t1RFrame.rowconfigure(1, weight=3)
        self.t1RFrame.rowconfigure(2, weight=2)
        self.t1RFrame.rowconfigure(3, weight=30)
        self.t1RFrame.columnconfigure((0, 1), weight=3)
        self.t1RFrame.columnconfigure(2, weight=1)

        # ============ Top Window ============
        self.t1RWindow1 = customtkinter.CTkFrame(master=self.t1RFrame, fg_color="gray60")
        self.t1RWindow1.grid(row=0, column=0, columnspan=3, rowspan=1, pady=5, padx=5,sticky="nsew")
        self.t1RWindow1.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.t1RWindow1.rowconfigure(1, weight=2)

        # Net Worth
        self.label_info_netWorth = customtkinter.CTkLabel(master=self.t1RWindow1, text="Net Worth",
                                                          text_font=("Arial Bold", 18), height=30, corner_radius=6,
                                                          text_color='black')
        self.label_info_netWorth.grid(column=0, row=0, sticky="nwe", padx=5, pady=5)
        self.label_netWorth = customtkinter.CTkLabel(master=self.t1RWindow1, text=None, text_font=("Arial Bold", 36),
                                                     height=75, corner_radius=6, fg_color=("white", "gray38"),
                                                     text_color='linen')
        self.label_netWorth.grid(column=0, row=1, sticky="nwe", padx=5, pady=5)

        # Total Checkings
        self.label_info_totalChk = customtkinter.CTkLabel(master=self.t1RWindow1, text="Checkings",
                                                          text_font=("Arial Bold", 18), height=30, corner_radius=6,
                                                          text_color='black')
        self.label_info_totalChk.grid(column=1, row=0, sticky="nwe", padx=5, pady=5)
        self.label_totalChk = customtkinter.CTkLabel(master=self.t1RWindow1, text=None, text_font=("Arial Bold", 36),
                                                     height=75, corner_radius=6, fg_color=("white", "gray38"),
                                                     text_color='linen')
        self.label_totalChk.grid(column=1, row=1, sticky="nwe", padx=5, pady=5)

        # Total Savings
        self.label_info_totalSav = customtkinter.CTkLabel(master=self.t1RWindow1, text="Savings",
                                                          text_font=("Arial Bold", 18), height=30, corner_radius=6,
                                                          text_color='black')
        self.label_info_totalSav.grid(column=2, row=0, sticky="nwe", padx=5, pady=5)
        self.label_totalSav = customtkinter.CTkLabel(master=self.t1RWindow1, text=None, text_font=("Arial Bold", 36),
                                                     height=75, corner_radius=6, fg_color=("white", "gray38"),
                                                     text_color='linen')
        self.label_totalSav.grid(column=2, row=1, sticky="nwe", padx=5, pady=5)

        # Total Investments
        self.label_info_totalInv = customtkinter.CTkLabel(master=self.t1RWindow1, text="Investments",
                                                          text_font=("Arial Bold", 18), height=30, corner_radius=6,
                                                          text_color='black')
        self.label_info_totalInv.grid(column=3, row=0, sticky="nwe", padx=5, pady=5)
        self.label_totalInv = customtkinter.CTkLabel(master=self.t1RWindow1, text=None, text_font=("Arial Bold", 36),
                                                     height=75, corner_radius=6, fg_color=("white", "gray38"),
                                                     text_color='linen')
        self.label_totalInv.grid(column=3, row=1, sticky="nwe", padx=5, pady=5)

        # Total Debts
        self.label_info_totalDebt = customtkinter.CTkLabel(master=self.t1RWindow1, text="Total Debt",
                                                           text_font=("Arial Bold", 18), height=30, corner_radius=6,
                                                           text_color='black')
        self.label_info_totalDebt.grid(column=4, row=0, sticky="nwe", padx=5, pady=5)
        self.label_totalDebt = customtkinter.CTkLabel(master=self.t1RWindow1, text=None, text_font=("Arial Bold", 36),
                                                      height=75, corner_radius=6, fg_color=("white", "gray38"),
                                                      text_color='linen')  #
        self.label_totalDebt.grid(column=4, row=1, sticky="nwe", padx=5, pady=5)

        # ============ Window 2 ============
        self.t1RWindow2 = customtkinter.CTkFrame(master=self.t1RFrame, fg_color="gray60")
        self.t1RWindow2.grid(row=1, column=0, columnspan=2, rowspan=6, pady=5, padx=5, sticky="nsew")

        # ============ Window 3 ============
        self.t1RWindow3 = customtkinter.CTkFrame(master=self.t1RFrame, fg_color="gray60")
        self.t1RWindow3.grid(row=1, column=2, columnspan=1, rowspan=1, pady=5, padx=5, sticky="nsew")

        self.t1RWindow3.columnconfigure((0, 1), weight=1)
        self.t1RWindow3.rowconfigure((0, 1), weight=1)

        self.t1RWindow3Label = customtkinter.CTkLabel(master=self.t1RWindow3, text="Connected Accounts", text_font=("Arial Bold", 12), text_color="black")
        self.t1RWindow3Label.pack()

        # ============ Window 4 ============
        self.t1RWindow4 = customtkinter.CTkFrame(master=self.t1RFrame, fg_color="gray60")
        self.t1RWindow4.grid(row=2, column=2, columnspan=1, rowspan=1, pady=5, padx=5, sticky="nsew")

        self.t1RWindow4.columnconfigure((0, 1), weight=1)
        self.t1RWindow4.rowconfigure((0, 1), weight=1)

        self.t1RWindow4Label = customtkinter.CTkLabel(master=self.t1RWindow4, text="Loans", text_font=("Arial Bold", 12), text_color="black")
        self.t1RWindow4Label.pack()

        # ============ Window 5 ============
        self.t1RWindow5 = customtkinter.CTkFrame(master=self.t1RFrame, fg_color="gray60")
        self.t1RWindow5.grid(row=3, column=2, columnspan=1, rowspan=1, pady=5, padx=5, sticky="nsew")

        self.t1RWindow5.columnconfigure((0, 1), weight=1)
        self.t1RWindow5.rowconfigure((0, 1), weight=1)

        self.t1RWindow5Label = customtkinter.CTkLabel(master=self.t1RWindow5, text="To Be Determined", text_font=("Arial Bold", 12), text_color="black")
        self.t1RWindow5Label.pack()

    # Functions
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()