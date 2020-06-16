import os
import basilica
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

if __name__ == "__main__":
    sentences = [
        "This is a sentence!",
        "This is a similar sentence!",
        "I don't think this sentence is very similar at all...",
]

connection = Connection(API_KEY)
print("CONNECTION", type(connection))


embeddings = list(connection.embed_sentences(sentences))
print(embeddings)

embedding = list(connection.embed_sentence("Hello world!", model=twitter))
print(type(embedding))
print(type(embedding[0]))
print(len(embedding))


breakpoint
[[0.8556405305862427, ...], ...]