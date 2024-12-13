import random

player_score = 0
computer_score = 0
hint_used = 0
max_hints = 3

class bcolors:
    HEADER = '\033[95m'     # Light magenta (purple)
    OKBLUE = '\033[94m'     # Light blue
    OKCYAN = '\033[96m'     # Light cyan
    OKGREEN = '\033[92m'    # Light green
    WARNING = '\033[93m'    # Light yellow
    FAIL = '\033[91m'       # Light red
    ENDC = '\033[0m'        # Resets all attributes (back to default color and format)
    UNDERLINE = '\033[4m'   # Underlines text

def easy_word():
    try:
        with open("C:/MyCodes/VSC/python_hangman/personal_work_1/easy_words.txt", "rt") as file:
            word_list = file.readlines()
    except FileNotFoundError:
        print("File not found: ./personal_work_1/easy_words.txt")
        return None

    random_number = random.randint(0, len(word_list) - 1)
    word = word_list[random_number].strip()
    return word

def medium_word():
    try:
        with open("C:/MyCodes/VSC/python_hangman/personal_work_1/medium_words.txt", "rt") as file:
            word_list = file.readlines()
    except FileNotFoundError:
        print("File not found: ./personal_work/medium_words.txt")
        return None

    random_number = random.randint(0, len(word_list) - 1)
    word = word_list[random_number].strip()
    return word

def hard_word():
    try:
        with open("C:/MyCodes/VSC/python_hangman/personal_work_1/hard_words.txt", "rt") as file:
            word_list = file.readlines()
    except FileNotFoundError:
        print("File not found: ./personal_work/hard_words.txt")
        return None

    random_number = random.randint(0, len(word_list) - 1)
    word = word_list[random_number].strip()
    return word

def hanged(man):
    graphic = [
    f"""{bcolors.OKCYAN}
           -----
           |   |
               |
               |
               |
               |
        --------
        {bcolors.ENDC}""", 
        f"""{bcolors.OKCYAN}
           -----
           |   |
           O   |
               |
               |
               |
        --------
        {bcolors.ENDC}""",
        f"""{bcolors.OKCYAN}
           -----
           |   |
           O   |
           |   |
               |
               |
        --------
        {bcolors.ENDC}"""
        ,
        f"""{bcolors.OKCYAN}
           -----
           |   |
           O   |
          /|   |
               |
               |
        --------
        {bcolors.ENDC}""", 
        f"""{bcolors.OKCYAN}
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        --------
        {bcolors.ENDC}""",
        f"""{bcolors.OKCYAN}
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        --------
        {bcolors.ENDC}""",
        f"""{bcolors.OKCYAN}
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        --------
    {bcolors.ENDC}"""]
    return graphic[man]

def start():
    print_hangman()
    print("")
    user_options = dif_options()
    print("")

    prev_player_score = player_score
    prev_computer_score = computer_score

    while True:
        if user_options == "easy" or user_options == "a":
            easy_game(easy_word())
        elif user_options == "medium" or user_options == "b":
            medium_game(medium_word())
        elif user_options == "hard" or user_options == "c":
            hard_game(hard_word())
        else:
            print(f"{bcolors.WARNING}Invalid Input. Select a level to play{bcolors.ENDC}")
        
        scores(prev_player_score, prev_computer_score)

        prev_player_score = player_score
        prev_computer_score = computer_score

        if not play_again():
            print("")
            print_centered(f"{bcolors.OKGREEN}Thank you for playing!{bcolors.ENDC}", total_width=90)
            print("")
            break

def easy_game(the_word):
    if the_word is None:
        return

    print("")
    print("The word has {} letters.".format(len(the_word)))
    clue = len(the_word) * ["_"]
    print("")
    print(" ".join(clue))
    tries = 6
    letters_tried = ""
    letters_wrong = 0
    global player_score, computer_score, hint_used, max_hints

    while (letters_wrong != tries) and ("".join(clue) != the_word):
        letter = guess_letter()

        if len(letter) == 1 and letter.isalpha():
            if letter in letters_tried:
                print("")
                print_centered(f"{bcolors.WARNING}You've already picked, '{letter}'{bcolors.ENDC}", total_width=90)
            else:
                if letter not in the_word:
                    print("")
                    print_centered(f"{bcolors.FAIL}Sorry, there isn't any '{letter}' in the word.{bcolors.ENDC}", total_width=90)
                    print_centered(f"{bcolors.FAIL}Choose Another!{bcolors.ENDC}", total_width=90)
                    letters_tried += letter
                    letters_wrong += 1
                else:
                    print("")  
                    print_centered(f"{bcolors.OKGREEN}Yay! '{letter}' is correct.{bcolors.OKGREEN}", total_width=90)
                    for i in range(len(the_word)):
                        if letter == the_word[i]:
                            clue[i] = letter
        elif letter == "hint" and hint_used < max_hints:
            hint_used += 1
            print_hint(the_word, clue)
            print("")
            print_centered(f"{bcolors.WARNING}You have {max_hints - hint_used} hint(s) left.{bcolors.ENDC}", total_width=90)
        elif letter == "hint" and hint_used >= max_hints:
            print("")
            print_centered(f"{bcolors.WARNING}No hints left{bcolors.ENDC}", total_width=90)

        print(hanged(letters_wrong))
        print(" ".join(clue))
        print("")
        print("Guesses: ", letters_tried)

        if letters_wrong == tries:
            print_game_over()
            print_centered(f"The word was '{the_word}'", total_width=90)
            computer_score += 1 
            break
        elif " ".join(clue) == the_word:
            print_win()
            print_centered(f"The word was '{the_word}'", total_width=90)
            player_score += 1  
            break
        elif len(letter) != 1 and letter != "hint":
            print_centered(f"{bcolors.WARNING}Put only 1 letter.{bcolors.ENDC}", total_width=90)
            
    
    if "".join(clue) == the_word:
        print_win()
        print_centered(f"The word was {the_word}", total_width=90)
        player_score += 1


def medium_game(the_word):
    return easy_game(the_word)
    
def hard_game(the_word):
    return easy_game(the_word)

def print_centered(text, total_width=90):
    print(f"{text:^{total_width}}")

def dif_options():
    print("Select the level of difficulty:")
    level_dif = [
    "a. Easy - Are you weak? Why the heck do you still want to play?",
    "b. Medium - Okay? Someone wants a challenge. I commend you for it.",
    "c. Hard - You're a challenger in life. Long live to you!"
    ]
    for l_dif in level_dif:
        print(l_dif)
    options = input("-> ").lower()
    if options not in ["easy", "medium", "hard", "a", "b", "c"]:
        print("")
        print(f"{bcolors.WARNING}Invalid option. Please select from easy, medium, or hard.{bcolors.ENDC}")
        print("")
        return dif_options()
    return options

def guess_letter():
    print("")
    letter = input("Guess a letter or type 'hint': ").strip().lower()
    return letter

def print_hint(the_word, clue):
    unrevealed_letters = [i for i in range(len(the_word)) if clue[i] == "_"]
    if unrevealed_letters:
        hint_index = random.choice(unrevealed_letters)
        clue[hint_index] = the_word[hint_index]
        print("")
        print(f"Hint: Revealed the letter '{the_word[hint_index]}' at position {hint_index + 1}.")


def play_again():
    print("")
    answer = input("Would you like to play again? y/n: ").strip().lower()
    
    while answer not in ["yes", "y", "no", "n"]:
        print("")
        print_centered(f"{bcolors.WARNING}Invalid Input. Please enter 'y' or 'n'.{bcolors.ENDC}", total_width=90)
        print("")
        answer = input("Would you like to play again? y/n: ").strip().lower()
    
    return answer in ["yes", "y"]

def scores(prev_player_score, prev_computer_score):
    global player_score, computer_score
    print(f"{bcolors.HEADER}{bcolors.UNDERLINE}SCORES TRACKER{bcolors.ENDC}")

    if player_score > prev_player_score:
        print(f"{bcolors.OKGREEN}Player: {player_score}{bcolors.ENDC}")
        print(f"{bcolors.FAIL}Computer: {computer_score}{bcolors.ENDC}")
    elif computer_score > prev_computer_score:
        print(f"{bcolors.FAIL}Player: {player_score}{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}Computer: {computer_score}{bcolors.ENDC}")


def print_hangman():
    hang_man = [
    f'''{bcolors.OKGREEN}
     _   _      _      _   _    ____   __  __      _      _   _ 
    | | | |    / \    | \ | |  / ___| |  \/  |    / \    | \ | |
    | |_| |   / _ \   |  \| | | |  _  | |\/| |   / _ \   |  \| |
    |  _  |  / ___ \  | |\  | | |_| | | |  | |  / ___ \  | |\  |
    |_| |_| /_/   \_\ |_| \_|  \____| |_|  |_| /_/   \_\ |_| \_|
    {bcolors.ENDC}'''
    ]
    print("\n".join(hang_man))

def print_game_over():
    game_over = [
    f'''{bcolors.FAIL}
         _______      ___      .___  ___.  _______      ______   ____    ____  _______ .______      
        /  _____|    /   \\     |   \\/   | |   ____|    /  __  \\  \\   \\  /   / |   ____||   _  \\     
       |  |  __     /  ^  \\    |  \\  /  | |  |__      |  |  |  |  \\   \\/   /  |  |__   |  |_)  |    
       |  | |_ |   /  /_\\  \\   |  |\\/|  | |   __|     |  |  |  |   \\      /   |   __|  |      /     
       |  |__| |  /  _____  \\  |  |  |  | |  |____    |  `--'  |    \\    /    |  |____ |  |\\  \\----.
        \\______| /__/     \\__\\ |__|  |__| |_______|    \\______/      \\__/     |_______|| _| `._____|                                                                                                                                                                     
    {bcolors.ENDC}'''
    ]
    print("\n".join(game_over))

def print_win():
    win = [
    f'''{bcolors.OKGREEN}
         ____    ____  ______    __    __     ____    __    ____  __  .__   __. 
         \\   \\  /   / /  __  \\  |  |  |  |    \\   \\  /  \\  /   / |  | |  \\ |  | 
          \\   \\/   / |  |  |  | |  |  |  |     \\   \\/    \\/   /  |  | |   \\|  | 
           \\_    _/  |  |  |  | |  |  |  |      \\            /   |  | |  . `  | 
             |  |    |  `--'  | |  `--'  |       \\    /\\    /    |  | |  |\\   | 
             |__|     \\______/   \\______/         \\__/  \\__/     |__| |__| \\__| 
                                                                     
    {bcolors.ENDC}'''
    ]
    print("\n".join(win))

if __name__ == "__main__":
    start()
