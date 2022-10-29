import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.    
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    '''
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    '''
    won = True
    for i in secret_word:
        if i not in letters_guessed:
            won = False
    return won


def get_word_progress(secret_word, letters_guessed):
    '''
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and plus signs (+) that represents
        which letters in secret_word have not been guessed so far
    '''
    progress = []
    for i in secret_word:
        if i in letters_guessed:
            progress.append(i)
        else:
            progress.append("+")
    return ''.join(progress)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    '''
    alphabet = list(string.ascii_lowercase)
    for i in letters_guessed:
        if i in alphabet:
            alphabet.remove(i)
    return ''.join(alphabet)
    
    
def get_help(secret_word, available_letters):
    choose_from = ""
    for i in available_letters:
        if i in secret_word:
            choose_from = choose_from+i
    hint = random.randint(0, len(choose_from)-1)
    revealed_letter = choose_from[hint]
    return revealed_letter
    
    
def hangman(secret_word, with_help):
    '''
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses they start with.
          
    * The user should start with 10 guesses.
          
    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.
          
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)
          
    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.
          
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.
          
    * After each guess, you should display to the user the
      partially guessed word so far.
          
    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.
          
    '''
    print("Welcome to Hangman!\n\nI am thinking of a word that is", len(secret_word), "letters long.\n")
    guesses_remaining = 10
    letters_guessed = []
    while guesses_remaining > 0:
        print("--------------\n\nYou currently have", guesses_remaining, "guesses left.\n\nAvailable letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter: ").lower()
        if letter == "!" and with_help is True:
            if guesses_remaining >= 3:
                revealed_letter = get_help(secret_word, get_available_letters(letters_guessed))
                letters_guessed.append(revealed_letter)
                print("\nLetter revealed: "+revealed_letter+"\n\n"+get_word_progress(secret_word, letters_guessed)+"\n") 
                guesses_remaining -= 3
            else:
                print("\nOops! Not enough guesses left:", get_word_progress(secret_word, letters_guessed), "\n")
        elif len(letter) > 1 or letter not in string.ascii_lowercase:
            print("\nOops! That is not a valid letter. Please input a letter from the alphabet:", get_word_progress(secret_word, letters_guessed), "\n")
        elif letter in letters_guessed:
            print("\nOops! You've already guessed that letter:", get_word_progress(secret_word, letters_guessed), "\n")
        else:
            letters_guessed.append(letter)
            if letter in secret_word:
                print("\nGood guess:", get_word_progress(secret_word, letters_guessed), "\n")
            else:
                print("\nOops! That letter is not in my word:", get_word_progress(secret_word, letters_guessed), "\n")
                vowels = "aeiou"
                if letter in vowels:
                    guesses_remaining -= 2
                else:
                    guesses_remaining -= 1
        if has_player_won(secret_word, letters_guessed):
            break
    if has_player_won(secret_word, letters_guessed):
        letters = list(secret_word)
        for i in letters:
            if letters.count(i) > 1:
                letters.remove(i)
        unique_letters = len(letters)
        score = (4*unique_letters*guesses_remaining)+(2*len(secret_word))
        print("--------------\n\nCongratulations, you won!\n\nYour total score for this game is:", score)
    else:
        print("--------------\n\nSorry, you ran out of guesses. The word was "+secret_word+".")

if __name__ == "__main__":
        secret_word = choose_word(wordlist)
        with_help = True
        hangman(secret_word, with_help)
