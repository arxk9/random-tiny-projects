import json
from dotenv import dotenv_values
from venmo_api import Client, string_to_timestamp
import csv

class DuesTracker:
	def __init__(self):
		config = dotenv_values(".env")
		self.access_token = config["VENMO_ACCESS_TOKEN"]
		self.client = Client(access_token=self.access_token)
		self.me = self.client.user.get_my_profile()
		beginning_of_2021_year = "2021-10-23T21:00:00"
		self.story_id_cutoff = 3351476852882408178
		# 3391260038495470417 triple threat
		self.initial_timestamp = string_to_timestamp(beginning_of_2021_year)
		self.indicator = ["chinavasian", "chinavasion"]

	def getTransactions(self):
		all_transaction_pages = []
		curr_transactions = self.client.user.get_user_transactions(user=self.me, limit=20)
		while curr_transactions:
			if int(curr_transactions[0].id) < self.story_id_cutoff:
				break
			all_transaction_pages.extend(curr_transactions)
			curr_transactions = curr_transactions.get_next_page()
		return all_transaction_pages

	def getUser(self, username):
		return self.client.user.get_user_by_username(username=username)

def prettyPrintUser(user, amount):
	return "Full Name: %s, username: %s, Amount: %.2f" % (user.first_name + " " + user.last_name, user.username, amount)
	
def buildHtml(user_tuples, tracker):
	total = 0
	ret = "<h1>CSA Transactions with \"" + str(tracker.indicator) + "\"</h1>"
	ret += "<table border=1 rules=all><tr><th>Full Name</th><th>Venmo Username</th><th>Amount Paid</th><th>Notes</th></tr>"
	for name, username, amount, notes in user_tuples:
		total += amount
		ret += "<tr>"
		ret += "<td>"
		ret += name
		ret += "</td>"
		ret += "<td>"
		ret += username
		ret += "</td>"
		ret += "<td>"
		ret += "%.2f"%amount
		ret += "</td>"
		ret += "<td>"
		ret += str(notes)
		ret += "</td>"
		ret += "</tr>"
	ret += "<tr><td></td><td>Total</td><td>"
	ret += "%.2f"%total
	ret += "</td><td></td></tr></table>"
	return ret

def commentsContainIndicator(comments, indicator):
	for comment in comments:
		for ind in indicator:
			if ind in comment.message.lower():
				return True
	return False
	
def isRelevantTransaction(transaction, tracker):
	note = transaction.note.lower()
	if transaction.status != "settled" or transaction.target.username != tracker.me.username or transaction.actor.username is None:
		return False
	for ind in tracker.indicator:
		if ind in note:
			return True
		if commentsContainIndicator(transaction.comments, tracker.indicator):
			return True
	
	# return ((tracker.indicator in transaction.note.lower() or 
	# commentsContainIndicator(transaction.comments, tracker.indicator)) and transaction.status == "settled" and 
	# transaction.target.username == tracker.me.username and transaction.actor.username is not None)

def lambda_handler(event, context):
	tracker = DuesTracker()
	transactions = tracker.getTransactions()
	filtered_transactions = [transaction for transaction in transactions if isRelevantTransaction(transaction, tracker)]
	dues_dict = dict()
	for transaction in filtered_transactions:
		thing = transaction.actor.username + " " + transaction.actor.first_name + " " + transaction.actor.last_name
		if thing in dues_dict:
			dues_dict[thing][0] += float(transaction.amount)
			dues_dict[thing][1].append(transaction.note)
		else:
			dues_dict[thing] = [float(transaction.amount), [transaction.note]]
		# dues_dict[thing] = dues_dict.get(thing, 0) + float(transaction.amount)
	# ret = "People who have paid at least some dues:<br>"
	user_tuples = []
	for user_first_last, amount_notes in dues_dict.items():
		i = user_first_last.index(" ")
		username = user_first_last[:i]
		name = user_first_last[i+1:]
		tup = (name, username, amount_notes[0], amount_notes[1])
		user_tuples.append(tup)
	user_tuples = sorted(user_tuples, key=lambda tup: tup[0].upper())
	html = buildHtml(user_tuples, tracker)
	return {
		'statusCode': 200,
		'body': html,
		"headers": {
			'Content-Type': 'text/html',
		}
	}


if __name__ == "__main__":
	tracker = DuesTracker()
	transactions = tracker.getTransactions()
	print("Transactions fetched")
	filtered_transactions = [transaction for transaction in transactions if isRelevantTransaction(transaction, tracker)]
	print("Transactions filtered")
	dues_dict = dict()
	for transaction in filtered_transactions:
		thing = transaction.actor.username + " " + transaction.actor.first_name + " " + transaction.actor.last_name
		if thing in dues_dict:
			dues_dict[thing][0] += float(transaction.amount)
			dues_dict[thing][1].append(transaction.note)
		else:
			dues_dict[thing] = [float(transaction.amount), [transaction.note]]
		# dues_dict[thing] = dues_dict.get(thing, 0) + float(transaction.amount)
	# ret = "People who have paid at least some dues:<br>"
	print("Amounts aggregated")
	user_tuples = []
	for user_first_last, amount_notes in dues_dict.items():
		i = user_first_last.index(" ")
		username = user_first_last[:i]
		name = user_first_last[i+1:]
		tup = (name, username, amount_notes[0], amount_notes[1])
		user_tuples.append(tup)
	user_tuples = sorted(user_tuples, key=lambda tup: tup[0].upper())
	# for thing in user_tuples:
	# 	print(thing)
	# print(user_tuples)
	# print("Users sorted")
	# total = 0
	# total_shirt = 0
	# total_charity = 0
	# for thing in user_tuples:
	# 	total += thing[2]
	# 	total_charity += min(thing[2], 9.5)
	# 	total_shirt += thing[2] - min(thing[2], 9.5)
	# print("Total raised", total)
	# print("Total shirt money", total_shirt)
	# print("Total donation", total_charity)
	
	filename = "chinavasian22.csv"
	with open(filename, 'w') as csvfile: 
		fields = ['First Name', "Last Name", "Username", "Amount"]
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields) 
		for user_tuple in user_tuples:
			i = user_tuple[0].index(" ")
			first = user_tuple[0][:i]
			last = user_tuple[0][i+1:]
			write_thing = [first, last, user_tuple[1], user_tuple[2], user_tuple[3]]
			csvwriter.writerow(write_thing)
		
