import re
import sys
import random

class RandomDwPw(object):
    """
    A class for creating diceware passwords

    Parameters
    ----------
    word_list_path : str
        A string containing the path to the diceware wordlist

    pw_min_length : int
        Specifies the minimum length for the generated password
    
    pw_max_length : int
        (Optional) Specifies the maximum length for the generated password. If not specified, the generated password will simply have random words added until the minimum length is specified. If a maximum length is specified, random words will be truncated to meet this requirement
    
    num_capitals : int
        (Optional) Specifies the minimum number of capitals in the generated password. If not specified, defaults to 0.

    num_spec_chars : int
        (Optional) Specifies the minimum number of required special characters in the generated password. If not specified, defaults to 0.

    num_numbers : int
        (Optional) Specifies the minimum number of numbers required in the generated password. If not specified, defaults to 0.
    
    Attributes
    ----------
    __word_list : str[]
        A list of strings containing a diceware wordlist

    """

    def __init__(self, word_list_path, pw_min_length, pw_max_length = -1, \
    num_capitals = 0, num_spec_chars = 0, num_numbers = 0):
        self.word_list_path = word_list_path
        self.pw_min_length = pw_min_length
        self.pw_max_length = pw_max_length
        self.num_capitals = num_capitals
        self.num_spec_chars = num_spec_chars
        self.num_numbers = num_numbers
        self.__spec_char_pool = { \
            0 : '!', \
            1 : '@', \
            2 : '#', \
            3 : '$', \
            4 : '%', \
            5 : '^', \
            6 : '&', \
            7 : '*', \
            8 : '(', \
            9 : ')' \
        }
        self.__load_word_list()

    def __load_word_list(self):
        self.__word_list = {}

        with open(self.word_list_path) as file:
            line = file.readline()
            while line:
                if re.search("^[0-9][0-9][0-9][0-9][0-9][\s]+.+$", line):
                    tokens = line.split()
                    self.__word_list[int(tokens[0])] = tokens[1]
                line = file.readline()

    def __dice_roll(self):
        return random.randint(1,6)

    def __get_random_word(self):
        random_number = ""
        # create random number by roll dice 5 times
        for i in range(0,5):
            random_number += str(self.__dice_roll())
        # convert string to int
        random_number = int(random_number)
        return self.__word_list[random_number]


    def generate_easy_dw_pw(self):
        """
        Generates an 'easy' diceware password, meaning one that sacrifices some security so that it is convenient to type.

        Parameters
        ----------
        (None)

        Returns
        -------
        diceware_password : String
            The string returned is a diceware password, a list of words separated by strings. If capitals are specified, random letters will be capitalized. If numbers or special characters are specified, they will be inserted at random locations either in front of or after a word.

        """
        curr_pw = ""
        curr_word_array = []
        curr_pw_len = 0
        curr_num_spec_chars = 0
        curr_num_nums = 0

        added_spec_chars = []
        added_nums = []

        while curr_pw_len + self.num_capitals < self.pw_min_length:
            word = self.__get_random_word()
            curr_word_array.append(word)
            # matches = re.findall("the", "the ether etheo eth thathe the")
            num_spec_chars_in_word = len(re.findall("[^0-9a-zA-Z]", word))
            num_numbers_in_word = len(re.findall("[0-9]", word))

            curr_num_spec_chars += num_spec_chars_in_word
            curr_num_nums += num_numbers_in_word

            curr_pw_len += len(word)

        # satisfy requirement for number of special characters
        while self.num_spec_chars > curr_num_spec_chars:
            rand_num = random.randint(0,9)
            rand_ind = random.randint(0,len(curr_word_array)-1)
            before_or_after = random.randint(0,1)
            rand_spec_char = self.__spec_char_pool[rand_num]
            added_spec_chars.append([rand_ind, before_or_after, rand_spec_char])
            curr_num_spec_chars += 1

        # number of numbers
        while self.num_numbers > curr_num_nums:
            rand_num = random.randint(0,9)
            rand_ind = random.randint(0,len(curr_word_array)-1)
            before_or_after = random.randint(0,1)
            added_nums.append([rand_ind, before_or_after, rand_num])
            curr_num_nums += 1

        # construct password
        for injection_list in [added_nums, added_spec_chars]:
            for item_injection in injection_list:
                rand_ind, before_or_after, rand_inj = item_injection

                if before_or_after == 0:
                    curr_word_array[rand_ind] = str(rand_inj) + curr_word_array[rand_ind]
                else:
                    curr_word_array[rand_ind] = curr_word_array[rand_ind] + str(rand_inj)

        for i in range(0, len(curr_word_array)):
            token = curr_word_array[i]
            curr_pw += token
            if i != (len(curr_word_array) - 1):
                curr_pw += " "

        # number of capitals
        num_letters = len(re.findall("[a-z]", curr_pw))

        # catch errors
        if self.pw_max_length != -1:
            if self.num_capitals > self.pw_max_length or self.num_capitals > num_letters:
                sys.stderr.write('Error generating password: Requiring too many capital letters for the specified password length. Change parameters and try again.')
                sys.exit()
                return None

        curr_caps = 0
        while curr_caps < self.num_capitals:
            rand_ind = random.randint(0,len(curr_pw)-1)
            pw_list = list(curr_pw)
            pw_list[rand_ind] = curr_pw[rand_ind].upper()
            curr_pw = "".join(pw_list)
            curr_caps += 1

        return curr_pw
















