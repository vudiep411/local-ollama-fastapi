import ollama
from typing import List
from langchain_ollama import ChatOllama

prompt_template = "You are an assistant, given provided tools. If the question does not require tools response as normal"
response = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 
        'Hi'}],

		# provide a weather checking tool to the model
    stream=True,
#     tools=[{
#       'type': 'function',
#       'function': {
#         'name': 'get_current_weather',
#         'description': 'Get the current weather for a city',
#         'parameters': {
#           'type': 'object',
#           'properties': {
#             'city': {
#               'type': 'string',
#               'description': 'The name of the city',
#             },
#           },
#           'required': ['city'],
#         },
#       },
#     },
#   ],
)
for chunk in response:
    print(chunk['message']['content'], end="")

