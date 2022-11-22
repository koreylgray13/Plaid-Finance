import sqlite3

cols = "pending_transaction_id, category_id, category, location, payment_meta, account_owner, name, account_id, amount, iso_currency_code, unofficial_currency_code, date, pending, transaction_id, payment_channel, authorized_date, authorized_datetime, datetime, transaction_code, check_number, merchant_name, personal_finance_category, transaction_type"
transaction_columns = "pending_transaction_id, category_id, category, location, payment_meta, account_owner, name, account_id, amount, iso_currency_code, unofficial_currency_code, date, pending, transaction_id, payment_channel, authorized_date, authorized_datetime, datetime, transaction_code, check_number, merchant_name, personal_finance_category, transaction_type"

conn = sqlite3.connect('../finance.db')
c = conn.cursor()

c.execute(f'CREATE TABLE IF NOT EXISTS chase ({transaction_columns})')

conn.commit()
conn.close()
