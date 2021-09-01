from dotenv import dotenv_values
from venmo_api import Client, string_to_timestamp

class DuesTracker:
	def __init__(self):
		config = dotenv_values(".env")
		self.access_token = config["VENMO_ACCESS_TOKEN"]
		self.client = Client(access_token=self.access_token)
		self.me = self.client.user.get_my_profile()
		beginning_of_2021_year = "2021-09-01T00:00:00"
		self.story_id_cutoff = 3351476852882408178
		self.initial_timestamp = string_to_timestamp(beginning_of_2021_year)
		self.dues_indicator = "#csadues2021"

	def getTransactions(self):
		all_transaction_pages = []
		curr_transactions = self.client.user.get_user_transactions(user=self.me, limit=10)
		while curr_transactions:
			if int(curr_transactions[0].id) < self.story_id_cutoff:
				break
			all_transaction_pages.extend(curr_transactions)
			curr_transactions = curr_transactions.get_next_page()
		return all_transaction_pages

	def getUser(self, id):
		return self.client.user.get_user(user_id=id)

def prettyPrintTransaction(transaction):
	print("Transaction ID:", transaction.id)
	print("Payment ID:", transaction.payment_id)
	print("Date Completed:", transaction.date_completed)
	print("Payment Type:", transaction.payment_type)
	print("Amount:", transaction.amount)
	print("Audience:", transaction.audience)
	print("Status:", transaction.status)
	print("Note:", transaction.note)
	print("Device used:", transaction.device_used)
	print("Actor:", transaction.actor)
	print("Target:", transaction.target)

def prettyPrintUser(user, amount):
	print("Full Name: %s, username: %s, Amount: %.2f" % (user.first_name + " " + user.last_name, user.username, amount))

if __name__ == '__main__':
	tracker = DuesTracker()
	transactions = tracker.getTransactions()
	filtered_transactions = [transaction for transaction in transactions if tracker.dues_indicator in transaction.note.lower() 
								and transaction.status == "settled" and transaction.target.username == tracker.me.username]
	dues_dict = dict()
	
	for transaction in filtered_transactions:
		dues_dict[transaction.actor.id] = dues_dict.get(transaction.actor.id, 0) + float(transaction.amount)

	print("People who have paid at least some dues:")
	for user_id, amount in dues_dict.items():
		user = tracker.getUser(user_id)
		prettyPrintUser(user, amount)
