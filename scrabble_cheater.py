import os
from flask import Flask, render_template, request, redirect
cheater = Flask(__name__)

letter_scores = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2,
         "F": 4, "I": 1, "H": 4, "K": 5, "J": 8, "M": 3,
         "L": 1, "O": 1, "N": 1, "Q": 10, "P": 3, "S": 1,
         "R": 1, "U": 1, "T": 1, "W": 4, "V": 4, "Y": 4,
         "X": 8, "Z": 10}

def getwordlist(file):
	#creates wordlist of official scrabble words
	f = open(file)
	return [word[:-2] for word in f.readlines()]


def score(word, board_letter, blank_scores):
	#computes score of word
	score = sum(letter_scores[char] for char in word)
	if (len(word) == 7 and board_letter == "") or (len(word)==8):
		score += 50
	score -= blank_scores
	return score

def pretty_print(possible_words):
	for word in possible_words:
		print word[0], ': ', word[1]

def generate_possible_words(word_list, tiles_input, board_letter):
	possible_words = []
	for word in word_list:
		blank_scores = 0
		tiles = tiles_input[:]
		valid_word = True
		if board_letter:
			board_letter_used = False
			if board_letter not in word:
				valid_word = False
		if valid_word:
			for letter in word:
				if letter == board_letter and board_letter_used == False:
					board_letter_used = True
				elif letter in tiles:
					tiles = tiles.replace(letter, "", 1)
				elif '*' in tiles:
					tiles = tiles.replace('*', "", 1)
					blank_scores += letter_scores[letter]
				else:
					valid_word = False
		if valid_word:
			possible_words.append((word, score(word, board_letter, blank_scores)))
	possible_words.sort(key=lambda x: x[1], reverse=True)
	return possible_words

@cheater.route('/main_page', methods=['GET','POST'])
def main_page():
	if request.method == 'GET':
		return render_template('main_page.html', error1 = "", error2 = "")
	elif request.method == 'POST':
		word_list = getwordlist('static/dictionary.txt')
		tiles_input = str(request.form['rack']).upper()
		board_letter = str(request.form['board_letter']).upper()
		error1 = error2 = ""
		if len(tiles_input) < 2:
			error1 = "Please enter at least two tiles."
		if len(board_letter) > 1:
			error2 = "You may only put one board letter here."
		if error1 or error2:
			return render_template('main_page.html', error1=error1, error2=error2, rack=tiles_input, board_letter=board_letter)
		else:
			print tiles_input, board_letter
			print type(board_letter)
			print board_letter == ""
			results = generate_possible_words(word_list, tiles_input, board_letter)
			print results
			return render_template('results.html', results=results)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	cheater.run(host='0.0.0.0', port=port)
