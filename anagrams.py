import enchant

global perms
def get_powerset(curr, remaining):
    global perms
    perms.add(curr)
    for letter in remaining:
    	remainingcopy = list(remaining)
    	remainingcopy.remove(letter)
    	get_powerset(curr + letter, "".join(remainingcopy))

def main():
	global perms
	checker = enchant.Dict("en_US")
	letters = input("Give me anagram letters:")
	letters = letters.lower().strip()
	perms = set()
	get_powerset("", letters)
	filtered_anagrams = [perm for perm in perms if perm != "" and len(perm) >= 3 and checker.check(perm)]
	filtered_anagrams = sorted(filtered_anagrams, key=lambda anagram: len(anagram), reverse=True)
	for anagram in filtered_anagrams:
		print(anagram)

if __name__ == "__main__":
	main()