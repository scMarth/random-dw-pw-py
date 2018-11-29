import random_dw_pw

word_list_path = r'diceware-word-list/diceware.wordlist.asc'
pw_gen = random_dw_pw.RandomDwPw(word_list_path, 15, num_capitals=1, num_numbers=1, num_spec_chars=1, pw_max_length=15)
pw = pw_gen.generate_easy_dw_pw()
print(pw)
print("length: " + str(len(pw)))