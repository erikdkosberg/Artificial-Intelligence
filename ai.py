import openai
import json
from subprocess import PIPE, Popen


class API:
    """An interface to the 'openai' resources, allowing programmable control over generated responses
    with two examples of processing input to the models and remembering conversations"""

    def __init__(self):
        self.get_api_key()

    # Read in the API key and set the openai org/key
    def get_api_key(self):
        path = "path_to_your_api.txt"  # I put mine on a local text file
        with open(path, "r") as p:
            self.api_key = p.readlines()[1].replace("\n", "")

        openai.organization = "org-krOCbLDyKW8LAWh7LqfhkKWG"
        openai.api_key = self.api_key

    # Returns the output of command line
    def cmdline(self, command) -> str:
        process = Popen(args=command, stdout=PIPE, shell=True)
        return process.communicate()[0]

    # Ask a question manually creating the header files
    def ask_question(self, question, max_tokens) -> str:
        msg = """curl https://api.openai.com/v1/completions \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer %s" \
            -d '{"model": "text-davinci-003", "prompt": "%s", "temperature": 0, "max_tokens": %s}'
            """ % (
            self.api_key,
            question,
            max_tokens,
        )

        return self.cmdline(msg).decode("UTF-8")

    # Ask a question using API methods, allows you to remember current conversation
    def respond(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return response.choices[0].text

    # Every time we ask a question and get an answer, prefix our next question with that as the prompt
    def conversation(self):
        conversation_history = []
        while True:
            user_input = input("You: ")
            if user_input == "quit":
                break
            conversation_history.append(user_input)
            prompt = " ".join(conversation_history)
            response = self.respond(prompt)
            if len(response):
                print("AI:", response)
                conversation_history.append(response)
            else:
                print("Error please try again")
                break


def main(msg):
    p = API()

    # Start a conversation; end with 'quit' or invalid response - this method remembers earlier responses
    p.conversation()

    # Ask a single question - this method does NOT remember earlier responses
    answer = p.ask_question(msg, 4000)
    out = json.loads(answer)
    response = out["choices"][0]["text"]
    print(response)


if __name__ == "__main__":
    main("Write a poem in the style of Robert Frost")
