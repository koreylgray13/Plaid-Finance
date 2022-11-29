import cryptocompare
# from cefpython3 import cefpython as cef
import sys
from BoltxFinance.xPlaid import PlaidManager as xPlaid


class FinanceManager:

    def __init__(self):
        pass

    # ToDo
    def addItem(self):
        pass

    def updateItem(self):
        pass

    def deleteItem(self):
        pass

    def loanAmortization(self):
        pass

    @staticmethod
    def totalBalances():
        accounts = xPlaid.queryAccounts()
        totalChk = accounts.query("type == 'depository' and subtype == 'checking'")['current'].sum()
        totalSav = accounts.query("type == 'depository' and subtype == 'saving'")['current'].sum()
        totalCC = accounts.query("type == 'credit' and subtype == 'credit card'")['current'].sum()

        loans = xPlaid.queryLoans()
        totalLoans = loans['Balance'].sum()

        totalChk = int(totalChk)
        totalSav = int(totalSav)
        totalCC = int(totalCC)
        totalLoans = int(totalLoans)

        totalDebt = totalLoans + totalCC
        totalCash = totalChk + totalSav
        netWorth = totalCash - totalDebt

        return f'${totalChk:,}', f'{totalSav:,}', f'${totalDebt:,}', f'${netWorth:,}'

    @staticmethod
    def xrpBalance(tokens=1000):
        x = cryptocompare.get_price('XRP', currency='USD')
        xrpPrice = x['XRP']['USD']
        balance = xrpPrice * tokens
        balance = int(balance)
        return f'${balance:,}'

    @staticmethod
    def loanAmortization():
        pass

    # @staticmethod
    # def launchHTML(path):
    #     sys.excepthook = cef.ExceptHook
    #     cef.Initialize()
    #     cef.CreateBrowserSync(url=f"file:///link.html")
    #     cef.MessageLoop()
    #     cef.Shutdown()


