import re
import mmap

# The ascii representation of the honey comb
honeyCombRepr = '''
           ___
       ___/ {} \\___
      / {} \\___/ {} \\
      \\___/ {} \\___/
      / {} \\___/ {} \\
      \\___/ {} \\___/
          \\___/
'''


class HoneyComb():
    """Class to model instance of honeycomb from Spelling Bee game

    Spelling Bee is a game found in the New York Times in which
    letters are laid out in a honeycomb formation. The player
    attempts to create words using at least 4 characters and 
    including the center character.

    Attributes:
        center: The center letter of the honeycomb.
        letters: A list of all the letters in the honeycomb.
        guessedWords: A list of all of guessed words from the player.
        points: The total points earned by the player.
    """
    def __init__(self, centerLetter, otherLetters):
        """Initializes HoneyComb with letters, no guessed words, and 0 points.

        Args:
            centerLetter: The letter to be placed in the center of the honeycomb.
            otherLetters: The 6 other letters surrounding the center.

        Raises:
            Exception: if otherLetters is not 6 letters or center letter is not 1
                letter.
        """
        if len(otherLetters) != 6:
            raise Exception("There must be 6 otherletters : {} is not valid".format(otherLetters))
        if len(centerLetter) != 1:
            raise Exception("There must be 1 centerLetter : {} is not valid".format(centerLetter))

        self.center = centerLetter.upper()

        # insert center character into center of letters
        self.letters = [char.upper() for char in otherLetters]
        self.letters.insert(len(otherLetters) // 2, self.center)
        self.guessedWords = list()
        self.points = 0
    
    def disp(self):
        """Displays the honeycomb, points, and guessed words in the terminal."""
        honeyLines = honeyCombRepr.split("\n")
        copyLetters = self.letters.copy()

        # prints out the honeycomb using format strings to include letters
        # wherever needed
        for index, line in enumerate(honeyLines):
            x = re.findall(r'{(.*?)}', line)  # determines the number of {} in format string
            form = [copyLetters.pop() for _ in range(len(x))]
            print(line.format(*form))  # prints the line with the added letters
        
        # prints current points and guessed words
        print('Current Points: {}'.format(self.points))
        print('Guessed Words: {}\n'.format(", ".join(self.guessedWords)))

    def checkWord(self, word):
        """Checks if a word is valid.

        Word is valid if --- it includes the center, it has not been guessed
        before, it does not use any invalid characters (ones not in honeycomb),
        and it is in our dictionary of acceptable words.

        Args:
            word: The word to be checked.

        Returns:
            True or False depending on if the word is valid or invalid.
        """
        word = word.upper()
        wordSet = set(word)

        # check if word in our list of valid words
        with open('validwords.txt', 'rb', 0) as file, \
            mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(str.encode(word)) == -1:
                print("That word isn't in the dictionary.")
                return False
        
        # check if center included
        if self.center not in wordSet:
            print("That word doesn't include the center letter.")
            return False
        
        # check if any invalid letters used
        if len(wordSet - set(self.letters)) != 0:
            print("That word uses invalid letters.")
            return False
        
        # check if we already guessed that word
        if word in self.guessedWords:
            print("You've guessed that word before.")
            return False
        self.guessedWords.append(word)
        return True

    def getPoints(self, word):
        """Function gets the point value of a word.

        The point value of a word is determined as such---, length of the word
        - 3, unless the word uses all 7 characters in the honeycomb, in which
        case an extra 7 points are added to the value of the word.

        Args:
            word: The word to determine the point value for.

        Returns:
            An integer corresponding to the point value of the word.
        """
        word = word.upper()
        wPoints = 0
        
        # if they used all 7 characters, they get an extra 7 points
        if len(set(word)) == 7:
            wPoints += 7
        wPoints += len(word) - 3

        # increase point attribute
        self.points += wPoints
        return wPoints
