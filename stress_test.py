import random_dw_pw

word_list_path = r'diceware-word-list/diceware.wordlist.asc'
pw_gen = random_dw_pw.RandomDwPw(word_list_path, 15, num_capitals=1, num_numbers=1, num_spec_chars=1, pw_max_length=15)
pw = pw_gen.generate_easy_dw_pw()
print(pw)
print("length: " + str(len(pw)))

len_cache = {}
for i in range(0,100000):
    pw = pw_gen.generate_easy_dw_pw()
    pw_len = len(pw)
    if pw_len in len_cache:
        len_cache[pw_len] = 1 + len_cache[pw_len]
    else:
        len_cache[pw_len] = 1
print(len_cache)