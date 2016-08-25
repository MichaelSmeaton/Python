import pprint
import os

class PythonView:

    def get(self, prompt):
        result = input(prompt)
        return result

    def say(self, message):
        print(message)

    def say_list(self, messages):
        for message in messages:
            print(message)

    def start(self):
        os.system('cls')

    def stop(self):
        os._exit(0)
