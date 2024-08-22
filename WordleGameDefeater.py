import requests
import random
import string
import itertools
import nltk
from nltk.corpus import words

# Download NLTK words corpus (ensure that nltk data is installed)
nltk.download('words')

BASE_URL = 'https://wordle.votee.dev:8000/random'

def make_guess(word, seed):
    url = f'{BASE_URL}?guess={word}&seed={seed}'
    print(f"Making GET request to: {url}")
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.json()}")
    return response.json()

def filter_words(words, guess, result):
    def match(word):
        word_list = list(word)
        for i, res in enumerate(result):
            if res == 'correct':
                if word[i] != guess[i]:
                    return False
                word_list[i] = None
            elif res == 'present':
                if guess[i] not in word_list or word[i] == guess[i]:
                    return False
                word_list[word_list.index(guess[i])] = None
            elif res == 'absent':
                if guess[i] in word_list:
                    return False
        return True
    return [word for word in words if match(word)]

def generate_initial_guesses():
    return ['abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy', 'zabcd']

def main():
    seed = 3516
    print(f"Starting the guessing game with seed: {seed}")

    # Load the NLTK words corpus and filter it for 5-letter words only
    nltk_words = [word.lower() for word in words.words() if len(word) == 5 and word.isalpha()]
    
    initial_guesses = generate_initial_guesses()
    found_letters = set()
    absent_letters = set()
    total_tries = 0

    # Initial guessing phase
    for guess in initial_guesses:
        total_tries += 1
        print(f"Trying '{guess}'... (Try {total_tries})")
        result = make_guess(guess, seed)
        for i, res in enumerate(result):
            if res['result'] in ['correct', 'present']:
                found_letters.add(guess[i])
            elif res['result'] == 'absent':
                absent_letters.add(guess[i])

    print(f"The letters that are either correct or present are: {', '.join(found_letters)}")

    # Filter the NLTK word list based on the found letters
    filtered_nltk_words = [word for word in nltk_words if all(letter in found_letters for letter in word) and not any(letter in absent_letters for letter in word)]

    if not filtered_nltk_words:
        # Brute-force combinations of found letters if no meaningful words are found
        filtered_nltk_words = [''.join(p) for p in itertools.permutations(found_letters, 5)]

    while filtered_nltk_words:
        total_tries += 1
        guess = filtered_nltk_words.pop(0)
        print(f"Trying '{guess}'... (Try {total_tries})")
        result = make_guess(guess, seed)
        guess_result = [item['result'] for item in result]
        if all(res == 'correct' for res in guess_result):
            print(f"Correct guess: {guess}!")
            print(f"This is the correct word: {guess}")
            print(f"Total tries: {total_tries}")
            return
        nltk_words = filter_words(nltk_words, guess, guess_result)
        for i, res in enumerate(guess_result):
            if res in ['correct', 'present']:
                found_letters.add(guess[i])
            elif res == 'absent':
                absent_letters.add(guess[i])

    print(f"Could not find the correct word. The letters found were: {', '.join(found_letters)}")
    print(f"Total tries: {total_tries}")

if __name__ == "__main__":
    main()