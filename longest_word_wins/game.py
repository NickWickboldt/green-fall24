from questions import questions_list 
import random
from phi import is_answer_correct

class LongestWordWins:
    def __init__(self, word):
        self.word = word

    def question(self, question):
        print(question)
        self.start_timer(20)
        user_guess = input()
        response = is_answer_correct(question, user_guess)
        print(response)

    def game_start(self):
        number_of_questions = len(questions_list)
        random_question = int(random.random() * number_of_questions)
        self.question(questions_list[random_question])

    def start_timer(self, duration):
        print("This is a timer")

game = LongestWordWins("hi")
game.game_start()
