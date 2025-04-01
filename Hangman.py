import random
import time
import csv

def load_words():
    """Load words from predefined lists and a custom CSV file."""
    words = {
        'Easy': ['tree', 'fish', 'book', 'lamp', 'chair'],
        'Medium': ['python', 'guitar', 'planet', 'rocket'],
        'Hard': ['elephant', 'television', 'framework', 'kangaroo']
    }
    
    try:
        with open("custom_words.csv", "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2 and row[0] in words:
                    words[row[0]].append(row[1])
    except FileNotFoundError:
        pass
    
    return words

def choose_word(difficulty):
    """Select a random word from the chosen difficulty level."""
    words = load_words()[difficulty]
    return random.choice(words)

def display_word(word, guessed_letters):
    """Return the word display with guessed letters revealed."""
    return ' '.join(letter if letter in guessed_letters else '_' for letter in word)

def add_custom_word():
    """Allow the user to add a custom word to the CSV file."""
    difficulty = input("Enter difficulty for the new word (Easy/Medium/Hard): ").capitalize()
    while difficulty not in ['Easy', 'Medium', 'Hard']:
        difficulty = input("Invalid choice. Choose difficulty (Easy/Medium/Hard): ").capitalize()
    
    new_word = input("Enter a new word: ").lower()
    
    with open("custom_words.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([difficulty, new_word])
    
    print(f"Word '{new_word}' added to {difficulty} difficulty!")

def hangman():
    """Main function to run the Hangman game."""
    print("Welcome to Hangman!")
    difficulty = input("Choose difficulty (Easy/Medium/Hard): ").capitalize()
    while difficulty not in ['Easy', 'Medium', 'Hard']:
        difficulty = input("Invalid choice. Choose difficulty (Easy/Medium/Hard): ").capitalize()
    
    secret_word = choose_word(difficulty)
    guessed_letters = set()
    attempts = 6
    score = 100
    hint_used = False
    
    while attempts > 0:
        print("\nWord: ", display_word(secret_word, guessed_letters))
        print(f"Attempts left: {attempts} | Score: {score}")
        
        # Provide a hint when 3 or fewer attempts remain
        if attempts <= 3 and not hint_used:
            use_hint = input("Would you like a hint? (yes/no): ").lower()
            if use_hint == 'yes':
                for letter in secret_word:
                    if letter not in guessed_letters:
                        guessed_letters.add(letter)
                        hint_used = True
                        print(f"Hint used! A letter has been revealed: {display_word(secret_word, guessed_letters)}")
                        break
        
        guess = input("Enter a letter or guess the full word: ").lower()
        
        # Check if the player guessed the full word correctly
        if guess == secret_word:
            print("Congratulations! You guessed the word correctly.")
            print(f"Your final score: {score}")
            break
        
        # Ensure the guess is a single valid letter
        elif len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed that letter.")
            elif guess in secret_word:
                guessed_letters.add(guess)
                score += 10
                print("Good guess!")
            else:
                attempts -= 1
                score -= 10
                print("Wrong guess!")
        else:
            print("Invalid input. Enter a single letter or the full word.")
        
        # Check if the player has guessed all letters correctly
        if set(secret_word) == guessed_letters:
            print(f"Well done! The word was '{secret_word}'. Your final score: {score}")
            break
    else:
        print(f"Game over! The word was '{secret_word}'. Your final score: 0")

if __name__ == "__main__":
    option = input("Do you want to play Hangman or add a custom word? (play/add): ").lower()
    if option == "add":
        add_custom_word()
    else:
        hangman()