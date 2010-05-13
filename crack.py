#!/it/sw/python/bin/python
import hashlib #if the version of python is too old, use md5 instead
import sys
import time

#functions declarations

def reverseString(s):
	# reverses a string given to it.
	return s[::-1]
	
def leetize(string):
	# returns the leet speak version of string (that is with the characters selo replaced by 5310)
	return string.replace('e','3').replace('l','1').replace('s','5').replace('o','0')
		
def getVariations(word, batch):
	# returns a list including word and the possibles variations according to the following heuristics
	# 1) leet speak : the characters selo become 5310
	# 2) these words are reversed 
	# 3) a digit is appended at the end of the words (to deal with case such as password1)
	# 4) a number representing a year is appended to the end of all those words
	# the heuristics are divided into batches. During a batch, we try only some heuristics and not the others.
	# Thus, we will avoid to test everything on simple passwords. This speed our program up.
	variations = list()
	if batch == 1: # first batch, no heuristics
		variations.append(word)
		return variations

	leet_speak = leetize(word) # heuristic 1
	if batch == 2: # second batch, heuristics 1, 2, 3
		variations.append(word)	
		if leet_speak != word:
			variations.append(leet_speak)
		for variation in variations[:]: #since we add stuff to the list, we loop through a copy to avoid infinite loops
			reverse = reverseString(variation) # heuristic 2
			variations.append(reverse)
			for c in "0123456789": # heuristic 3
				variations.append(variation+c)
				variations.append(reverse+c)
		variations.remove(word)
	elif batch == 3: # third batch, heuristic 4
		reverse = reverseString(word)
		reverse_ls = reverseString(leet_speak)
		for y in range(2005,2015):# heuristic 4, we check only "recent" years since this is the most probable
			variations.append(word+str(y))
			variations.append(reverse+str(y))
			variations.append(leet_speak+str(y))
			variations.append(reverse_ls+str(y))
	return variations

def getMd5(unhashed):
	# returns the md5 hash of the string unhashed
	# if you want to use md5 instead of hashlib, replace the next line with hasher = md5.new()
	hasher = hashlib.md5()		
	hasher.update(unhashed)
	return hasher.hexdigest()

def loopThroughDictionary(salt, hash_pwd, dictionary,batch):
	# this function, used when salting is used, loops through the dictionary.  
	# The function tries to find a word in the dictionary whose the hash matches hash_pwd and exits when this is done. 
	global matches 
	for word in dictionary: 
		variations = getVariations(word,batch) # gets the variations of the word according to the heuristics and the current batch
		for variation in variations: # for each variation, we have to do the test
			hashed_word = getMd5(salt + variation)
			if hashed_word == hash_pwd:
				matches += 1 
				print "Match: "+variation+" => "+salt+":"+hash_pwd
				variations = None
				return True #No need to continue looping through the dictionary now that we've found the word
		variations = None # free the space used by the list variations
	return False

def loopThroughPasswords(word, passwords,batch):
	# this function, used when salting is not used, loops through the passwords' list
	# It tries to find a hashed password equals to the hash of word and exits when it is done.
	global matches
	variations = getVariations(word,batch) # gets the variations of word according to the current batch
	for variation in variations: # tries each variation we got
		hashed_word = getMd5(variation)
		for hash_pwd in passwords:
			if hashed_word == hash_pwd:
				passwords.remove(hash_pwd)
				matches += 1
				print "Match: "+variation+" => "+hash_pwd
				variations = None
				return #same as above
	variations = None # free used space


#body of the script

#we get the paths to the files and the falg indicating whether salting is used or not
dict_file = sys.argv[1]
pass_file = sys.argv[2]
salt_flag = sys.argv[3]


f_dictionary = open(dict_file, 'r')
f_passwords = open(pass_file, 'r')

# loads all the passwords in a list
passwords = list()
for password in f_passwords:
	passwords.append(password.rstrip())

# loads all the dictionary's word in a list
dictionary = list()
for word in f_dictionary:
	dictionary.append(word.rstrip())

f_dictionary.close()
f_passwords.close()

matches = 0 # this variable represents the number of passwords found
batch = 1

start = time.mktime(time.localtime())

if salt_flag == "1": #a salt has been used
	while batch <= 3 and passwords != []: # while we are not finished and there are still passwords to find
		for password in passwords[:]: # password is actually a line from the file. So, we need to parse it to get the information
			parts = password.split(":", 1) # a ':' separates the salt and the hash (salt:hash)
			salt = parts[0]
			hash_pwd = parts[1]
			if loopThroughDictionary(salt,hash_pwd,dictionary, batch): # tries to find this password
				passwords.remove(password)
		batch += 1 #next batch !
else: # no salt 
	while batch <= 3 and passwords != []:
		for word in dictionary:
			loopThroughPasswords(word, passwords,batch) # tries to find a password corresponding to this dictionary's word
			if passwords == []:
				break #we have found all the passwords, the attack is over
		batch += 1 # next batch !		

print "End. Total matches found: "+str(matches) # tells us how many passwords have been cracked !
print time.strftime("%M minutes and %S seconds",time.localtime(time.mktime(time.localtime())-start))
