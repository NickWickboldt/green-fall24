from phi import get_trivia_question, get_answer_rating

class Trivia: 
    def __init__(self, question):
        self.question = question
        self.answer = ""

    def game_start(self):
        print("game has started")
        print("Enter a topic for the first trivia question: ")
        topic = input()
        self.answer = self.trivia_question(topic)
        rating = get_answer_rating(self.question, self.answer)
        print(rating)

    def trivia_question(self, topic):
        print("getting question with topic: ", topic)
        #Get AI trivia question
        question = get_trivia_question(topic)
        print("AI has given question: ", question)
        answer = input()
        return answer

trivia_game = Trivia("temporary")
trivia_game.game_start()