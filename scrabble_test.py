import scrabble_cheater as s

def scrabble_tester():
	word_list = s.getwordlist('static/dictionary.txt')
	test_cases = [('CHICKEN',''), ('TIDJCO','M'), ('T*fjeAB', ''), ('STREO*','L')]
	for case in test_cases:
		tiles_input, board_letter = case
		results = s.generate_possible_words(word_list, tiles_input, board_letter)
		s.pretty_print(results[:10])

scrabble_tester()
