import os
import random
from HoneyComb import HoneyComb


def main():
    """Main function runs the loop of the game.

    The loop of the game involves creation of a HoneyComb, 
    guessing of words, and adding necessary points. The player
    can end the game by typing 'game-end'.
    """
    # Startup message
    clearTerminal()
    print("-=" * 15 + " Welcome to Spelling Bee " + "=-" * 15)
    print("You must form words of at least 4 characters, always including the center letter.")
    print("The longer the word, the more points it's worth. A word using all 7 characters gets a bonus.")

    # Flag for the intial setup of the honeycomb
    initialRun = 1

    while True:
        # Set up honeycomb
        if initialRun:
            # honeycomb created with some random letters
            honeyComb = HoneyComb(*getLetters())
            honeyComb.disp()
            initialRun = 0
        
        guess = input("Enter a word (Enter 'game-end' to end this round): ")

        if guess == 'game-end':
            # player wants to end game
            choice = getNewGame()
            clearTerminal()
            if choice == "y":
                # Start new game
                initialRun = 1
            else:
                # End
                break
        elif honeyComb.checkWord(guess):
            # word is valid, add points and say congrats
            points = honeyComb.getPoints(guess)
            clearTerminal()
            honeyComb.disp()
            print('Congrats, that word was worth {} points'.format(points))
        else:
            # word invalid, say why
            clearTerminal()
            honeyComb.disp()
            honeyComb.checkWord(guess)
            print("Please try again...")


def clearTerminal():
    """Clears terminal on both UNIX style and Windows."""
    # if operating system is unix-based, the "cls" command is run
    # otherwise, "clear" if run (this handles windows terminal)
    os.system('cls' if os.name == 'nt' else 'clear')


def getLetters():
    """Gets 7 letters that have a valid pangram.

    Looks through list of words randomly to find a word with 7 letters,
    uses these letters as the basis for the letters to be played in the game.

    Returns:
        2 strings, the center letter of the HoneyComb and string of 6 
        other letters to be placed around the center letter.
    """
    # reads file of valid words
    with open("validWords.txt") as words:
        lines = words.readlines()
    
    # gets a random index
    ind = random.randint(0, len(lines))

    # finds a word with 7 characters
    while len(set(lines[ind])) != 8:
        ind = (ind + 1) % len(lines)
    
    # get a string of the 7 characters
    letters = "".join(set(lines[ind][:-1]))

    # return a character as center and the others
    return letters[-1], letters[:-1]


def getNewGame():
    """Determines if player wants to play again

    Returns:
        A 'y' or 'n' corresponding to the player wanting to play again
        or the player wanting to stop.
    """
    # Validates user input to see if they want to play again
    choice = input("Play again? y/n: ")
    while choice.lower() not in ["y", "n", "yes", "no"]:
        choice = input("Play again? y/n: ")
    
    # Return a "y" or "n" even if they said "yes"/"no"
    return choice[0]


if __name__ == '__main__':
    main()
