import enchant

global checker

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
		word = ""
		for parent in self.parents:
			word += graph.letterMap[parent].letter
		word += graph.letterMap[self.id].letter
		return word


class Graph4x4:
	def __init__(self):
		self.letterMap = dict()
		self.letters = []
		for i in range(16):
			letter = Letter(i, "")
			self.letters.append(letter)
			self.letterMap[i] = letter
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

	def addPuzzle(self, letters):
		for i, letter in enumerate(self.letters):
			letter.letter = letters[i]

	def findWords(self, length):
		global checker
		final_words = []
		fringe = []
		for i in range(16):
			fringe.append(Node(i, [], 1))

		while fringe:
			node = fringe.pop(0)
			if node.depth >= length:
				word = node.getWord(self)
				if checker.check(word) and word not in final_words:
					print(word)
					final_words.append(word)
				continue
			letter = self.letterMap[node.id]
			neighbors = letter.neighbors
			for neighbor in neighbors:
				if neighbor.id in node.parents:
					continue
				fringe.insert(0, Node(neighbor.id, node.parents + [node.id], node.depth + 1))


def main():
	global checker
	checker = enchant.Dict("en_US")

	graph = Graph4x4()
	puzzle_input = input("Enter puzzle input:").strip().lower()
	assert(len(puzzle_input) == 16)
	graph.addPuzzle(puzzle_input)

	words7 = graph.findWords(7)
	input("see 6?")
	words6 = graph.findWords(6)
	input("see 5?")
	words5 = graph.findWords(5)
	input("see 4?")
	words4 = graph.findWords(4)
	input("see 3?")
	words3 = graph.findWords(3)


if __name__ == '__main__':
	main()