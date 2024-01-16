import spacy
import datetime
import webbrowser
import pywhatkit
import wikipedia
import random
from spellchecker import SpellChecker
from difflib import get_close_matches
from bs4 import BeautifulSoup
from textblob import TextBlob  # Import TextBlob for sentiment analysis

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

# Global variable to store sentiment
user_sentiment = None

def correct_spelling(query):
    corrected_words = []
    for word in query.split():
        closest_match = get_close_matches(word, spell.word_frequency.words(), n=1, cutoff=0.7)
        corrected_word = closest_match[0] if closest_match else word
        corrected_words.append(corrected_word)
    return " ".join(corrected_words)

def analyze_sentiment(query):
    analysis = TextBlob(query)
    # Classify sentiment as positive, negative, or neutral
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def get_positive_response():
    positive_responses = [
        "That's great to hear!",
        "Awesome!",
        "I'm glad you're feeling positive!",
        "Fantastic!"
    ]
    return random.choice(positive_responses)

def get_negative_response():
    negative_responses = [
        "I'm sorry to hear that. How can I help?",
        "I apologize if something is wrong. Can I assist you?",
        "If there's anything I can do to improve, please let me know.",
        "I'm here for you. What's bothering you?"
    ]
    return random.choice(negative_responses)

def process_query(query):
    global user_sentiment
    user_sentiment = analyze_sentiment(query)
    print(f"Sentiment: {user_sentiment}")

    # Respond based on sentiment
    if user_sentiment == "Positive":
        return get_positive_response()
    elif user_sentiment == "Negative":
        return get_negative_response()

    # Continue with the rest of your existing code...
    doc = nlp(query)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    entities = [ent.text for ent in doc.ents]
    greetings = ['hi', 'hello', 'hola', 'hey', 'howdy', 'hi there', 'hey there']
    love_phrases = ['i love you', 'i love u', 'i luv u', 'love you', 'lub u', 'i lub u']
    farewells = ['bye', 'bi', 'goodbye', 'see you later', 'farewell']
    casual_responses = {'idk': "It's okay not to know sometimes!", 'i d k': "No worries, I understand.", 'whatever': "Alright then!",
                        'cool': "Cool! Anything else I can help you with?", 'thanks': "You're welcome!", 'awesome': "I'm glad you think so!"}
    date_responses = [
        f"Today's date is: {datetime.date.today().strftime('%d/%m/%y')}",
        f"It's {datetime.datetime.now().strftime('%A, %B %d, %Y')}",
        f"The date is {datetime.datetime.now().strftime('%Y-%m-%d')}"
    ]
    time_responses = [
        f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}",
        f"It's currently {datetime.datetime.now().strftime('%I:%M %p')}",
        f"{datetime.datetime.now().strftime('%H:%M')} on the clock"
    ]

    for word, response in casual_responses.items():
        if word in doc.text.lower():
            return response

    if any(word in greetings for word in [token.text.lower() for token in doc]):
        return random.choice(["Hello!", "Hey there!", "Hi!", "Greetings!"])

    elif any(greeting in farewells for greeting in [token.text.lower() for token in doc]):
        return random.choice(["Goodbye!", "Farewell!", "See you later!", "Take care!"])

    elif any(phrase in doc.text.lower() for phrase in love_phrases):
        return "I love you too! 😊"

    elif any(interaction in doc.text.lower() for interaction in ['how are you', 'what\'s up', 'tell me a joke']):
        return "I'm doing well, thank you! How can I assist you today?"

    elif "weather" in nouns:
        return "I am not equipped to provide weather details, but I can search for it."

    elif "time" in nouns:
        return random.choice(time_responses)
    elif "date" in nouns:
        return random.choice(date_responses)

    elif "play" in verbs:
        video_title = query.replace("play", "").strip()
        pywhatkit.playonyt(video_title)
        return f"Playing the first video for '{video_title}' on YouTube."

    else:
        try:
            search_result = wikipedia.summary(query, sentences=2)
            return search_result
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            return f"Please be more specific. Did you mean {', '.join(options)}?"
        except wikipedia.exceptions.PageError:
            return "Sorry, I don't know about that."
