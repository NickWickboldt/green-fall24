from huggingface_hub import InferenceClient

client = InferenceClient(
    "microsoft/Phi-3.5-mini-instruct",
    token="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",
)

def is_answer_correct(question, answer):
    ai_response = ""
    for message in client.chat_completion(
    	messages=[{
            "role": "user", 
            "content": f"I was given this question: {question}. I responded with this answer: {answer}. Respond with only yes or no if I was correct, say nothing else."
        }],
    	max_tokens=500,
    	stream=True,
    ):
        ai_response += message.choices[0].delta.content
    ai_response = get_answer_from_response(ai_response)
    return ai_response

def get_answer_from_response(response):
    response = response.strip()
    temp = ""
    for i in range(len(response)):
        if response[i] != ',' and response[i] != ' ':
            temp+=response[i]
        else:
            break
    return temp
        
# result = is_answer_correct("Name a vegetable", "aqua")
# concat_result = get_answer_from_response(result)
# print(concat_result)