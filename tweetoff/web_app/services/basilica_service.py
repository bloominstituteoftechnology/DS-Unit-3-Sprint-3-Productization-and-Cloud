# web_app/services/basilica_service.py
from dotenv import load_dotenv
import os
import basilica

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

connection = basilica.Connection(API_KEY)
# basilica_api = basilica_api_client()

if __name__ == "__main__":
    
    print("---------")
    sentence = "Hello again"
    sent_embeddings = connection.embed_sentence(sentence)
    print(list(sent_embeddings))

    print("---------")
    sentences = ["Hello world!", "How are you?"]
    print(sentences)
    # it is more efficient to make a single request for all sentences...
    embeddings = connection.embed_sentences(sentences)
    print("EMBEDDINGS...")
    print(type(embeddings))
    print(list(embeddings))  # [[0.8556405305862427, ...], ...]

    print("---------")
    tweet_text = "I love #ArtificialIntelligence"
    tweet_embedding = connection.embed_sentence(tweet_text, model="twitter")
    print(list(tweet_embedding))
