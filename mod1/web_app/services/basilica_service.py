from basilica import Connection
import os
from dotenv import load_dotenv

load_dotenv()
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

sentences = [
"This is a sentence!",
"This is a similar sentence!",
"I don't think this sentence is very similar at all...",
]

connection = Connection(BASILICA_API_KEY)
print(type(Connection))

embeddings = list(connection.embed_sentences(sentences))
for embed in embeddings:
    print("----------")
    print(embed)

breakpoint()

