#
# It uses a python googleanalytics lib
#	You can download it at:
#	http://tinyurl.com/python-googleanalytics
#	
# By Johann Vivot
#


# Example to get Accounts
from googleanalytics import Connection

connection = Connection('xx@xxx.xxx', 'xxxx')
accounts = connection.get_accounts()

# Example to get Pageviews
account = connection.get_account('9060294')
start_date = datetime.date(2011, 10, 21)
end_date = datetime.date(2011, 10, 21)
data = account.get_data(start_date, end_date, metrics=['pageviews'])
data.list
