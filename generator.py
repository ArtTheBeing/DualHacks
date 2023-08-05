from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

# LangChain Models
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import PromptTemplate
import openai

# Standard Helpers
import pandas as pd
import json
import os
key = os.environ.get('openaiapi')
openai.api_key=key

#Open AI Generator



# Text Helpers
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# For token counting
from langchain.callbacks import get_openai_callback


class Generator():
    def __init__(self, topic):
        self.textGeneration(topic)
        pass

    def returnOutput(self, output):
        return (json.dumps(output,sort_keys=True, indent=3))

    def textGeneration(self, topic):
        llm = OpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.0,
        openai_api_key=key)

        result = llm(f"Give me 10 flashcards in {topic}. Format with card number, front, and back. Make sure none of the flashcards have formulas")
        with open ('flashcards.txt', 'wb') as file:
            file.write(result.encode('utf-8'))

    def parser(self):
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            max_tokens=2000,
            openai_api_key=key
        )

        with open('flashcards.txt', 'rb') as file:
            text=file.read()
            text = text.decode('utf-8')

        set_schema = Object(
            id="flashcards",
            description="a set of flashcards",
            
            # Notice I put multiple fields to pull out different attributes
            attributes=[
                Number(
                    id="flashcard_number",
                    description="number corresponding to flash card"
                ),
                Text(
                    id="front",
                    description="The front of the flashcard."
                ),
                Text(
                    id="back",
                    description="The back of the flashcard."
                )
            ],
        )

        chain = create_extraction_chain(llm, set_schema)
        output = chain.run(text=(text))['data']

        return self.returnOutput(output)

z = Generator('Algebra')
x = z.parser()
print(x)