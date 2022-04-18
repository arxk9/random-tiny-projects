import enchant
from collections import deque

global checker

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Letter:
	def __init__(self, id_, letter):
		self.id = id_
		self.letter = letter
		self.neighbors = set()

	def addNeighbor(self, neighbor):
		self.neighbors.add(neighbor)

class Node:
	def __init__(self, id_, parents, depth):
		self.id = id_
		self.parents = parents
		self.depth = depth

	def getWord(self, graph):
		word = "".join([graph.letterMap[parent].letter for parent in self.parents])
		# for parent in self.parents:
		# 	word += graph.letterMap[parent].letter
		word += graph.letterMap[self.id].letter
		return word

class Graph:
	def __init__(self):
		self.letterMap = dict()
		self.letters = []
		for i in range(self.size ** 2):
			letter = Letter(i, "")
			self.letters.append(letter)
			self.letterMap[i] = letter

	def addPuzzle(self, letters):
		for i, letter in enumerate(self.letters):
			letter.letter = letters[i]

	def findWords(self, length):
		global checker
		final_words = set()
		# fringe = deque()
		# for i in range(self.size**2):
		# 	fringe.append(Node(i, [], 1))
		fringe = deque([Node(i, [], 1) for i in range(self.size ** 2)])

		while fringe:
			node = fringe.popleft()
			if node.depth >= length:
				word = node.getWord(self)
				if word not in final_words and checker.check(word):
					print("----------------------------------------------------------------")
					print(color.GREEN + word.upper() + color.END)
					for i in range(self.size):
						ids = list(range(i*self.size, i*self.size + self.size))
						ret = ""
						for id_ in ids:
							if id_ == node.parents[0]:
								ret += color.GREEN + self.letters[id_].letter.upper() + color.END + " "
							elif id_ == node.id:
								ret += color.RED + self.letters[id_].letter.upper() + color.END + " "
							elif id_ in node.parents:
								ret += color.YELLOW + self.letters[id_].letter.upper() + color.END + " "
							else:
								ret += self.letters[id_].letter.upper() + " "
						print(ret)
					final_words.add(word)
				continue
			letter = self.letterMap[node.id]
			neighbors = letter.neighbors
			for neighbor in neighbors:
				if neighbor.id in node.parents:
					continue
				fringe.appendleft(Node(neighbor.id, node.parents + [node.id], node.depth + 1))
		print("----------------------------------------------------------------")


class Graph4x4(Graph):
	def __init__(self):
		self.size = 4
		super().__init__()
		for letter in self.letters:
			isLeft = letter.id % 4 == 0
			isTop = letter.id < 4
			isBottom = letter.id >= 12
			isRight = letter.id % 4 == 3
			if isTop and isLeft:
				offsets = [1, 4, 5]
			elif isTop and isRight:
				offsets = [-1, 3, 4]
			elif isLeft and isBottom:
				offsets = [-4, -3, 1]
			elif isRight and isBottom:
				offsets = [-5, -4, -1]
			elif isTop:
				offsets = [-1, 1, 3, 4, 5]
			elif isLeft:
				offsets = [-4, -3, 1, 4, 5]
			elif isRight:
				offsets = [-5, -4, -1, 3, 4]
			elif isBottom:
				offsets = [-5, -4, -3, -1, 1]
			else:
				offsets = [-5, -4, -3, -1, 1, 3, 4, 5]

			for offset in offsets:
				neighbor_id = letter.id + offset
				letter.addNeighbor(self.letterMap[neighbor_id])

class Graph5x5(Graph):
	def __init__(self):
		self.size = 5
		super().__init__()
		for letter in self.letters:
			isLeft = letter.id % 5 == 0
			isTop = letter.id < 5
			isBottom = letter.id >= 20
			isRight = letter.id % 5 == 4
			if isTop and isLeft:
				offsets = [1, 5, 6]
			elif isTop and isRight:
				offsets = [-1, 4, 5]
			elif isLeft and isBottom:
				offsets = [-5, -4, 1]
			elif isRight and isBottom:
				offsets = [-6, -5, -1]
			elif isTop:
				offsets = [-1, 1, 4, 5, 6]
			elif isLeft:
				offsets = [-5, -4, 1, 5, 6]
			elif isRight:
				offsets = [-6, -5, -1, 4, 5]
			elif isBottom:
				offsets = [-6, -5, -4, -1, 1]
			else:
				offsets = [-6, -5, -4, -1, 1, 4, 5, 6]

			for offset in offsets:
				neighbor_id = letter.id + offset
				letter.addNeighbor(self.letterMap[neighbor_id])

def main():
	global checker
	checker = enchant.Dict("en_US")
	puzzle_input = input("Enter puzzle input:").strip().lower()

	if len(puzzle_input) == 16:
		print("Using 4x4 board")
		graph = Graph4x4()

	elif len(puzzle_input) == 25:
		print("Using 5x5 board")
		graph = Graph5x5()

	else:
		print("Not a valid board size")
		exit()

	graph.addPuzzle(puzzle_input)

	try:
		words9 = graph.findWords(9)
	except KeyboardInterrupt:
		print('Interrupted 9\n')
	input("see 8?")
	try:
		words8 = graph.findWords(8)
	except KeyboardInterrupt:
		print('Interrupted 8\n')
	input("see 7?")
	try:
		words7 = graph.findWords(7)
	except KeyboardInterrupt:
		print('Interrupted 7\n')
	input("see 6?")
	try:
		words6 = graph.findWords(6)
	except KeyboardInterrupt:
		print('Interrupted 6\n')
	input("see 5?")
	try:
		words5 = graph.findWords(5)
	except KeyboardInterrupt:
		print('Interrupted 5\n')
	input("see 4?")
	try:
		words4 = graph.findWords(4)
	except KeyboardInterrupt:
		print('Interrupted 4\n')
	input("see 3?")
	try:
		words3 = graph.findWords(3)
	except KeyboardInterrupt:
		print('Interrupted 3\n')


if __name__ == '__main__':
	main()