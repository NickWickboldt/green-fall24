class Hangman: 
    def __init__(self, word):
        self.word = word
        self.is_dead = False
        self.has_guessed = False
    
    def start_game(self):
        print("game has started")
        self.word = self.generate_word()
        self.game_loop()

    def generate_word(self):
        print("generating word")
        word = "placeholder" #get word from AI
        return word
    
    def game_loop(self):
        print("game is looping with word: ", self.word)
        print("player is dead: ", self.is_dead)
        print("player has guessed: ", self.has_guessed)

hangman = Hangman("temporary")
hangman.start_game()