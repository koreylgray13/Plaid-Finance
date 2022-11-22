# Plaid-Finance
Scope: The goal with this project is to have a full scale locally hosted Personal Finance application that I could use for long term historical analysis of my finances. 

<b>Note: This project is far from finished and is quite a mess with a fair amount of redundant code, but wanted to share for anyone having similar issues getting this to work well in Python.</b>




This project connects to the API and stores all financial data in local DB (I've chosen SQLite for various reasons.) Once everything is stored you can query the DB for any analytics you want to build. For simplicity I'm temporarily using a PowerBI visual for analytics so I can check for accuracy. Plaid requires you to verify/authenticate using their front-end "Link" so that is not something that can easily be modified. Other than that almost all of the Plaid functions are possible to implement with Python with some work.

![image](https://user-images.githubusercontent.com/87346809/203384596-8ea3dd22-11f6-43c6-8369-b87be67e5683.png)

Still considering JS or PyScript for additional functionality. Any comments or feedback is welcome!
