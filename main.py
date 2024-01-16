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
        "That's fantastic!",
        "Great news!",
        "I'm thrilled to hear that!",
        "Fantastic!",
        "You made my day with that positive energy!",
        "Brilliant!"
    ]
    return random.choice(positive_responses)

def get_negative_response():
    negative_responses = [
        "I'm sorry to hear that. How can I assist you?",
        "I understand, and I'm here to help. What's going on?",
        "I'm here to listen. What can I do for you?",
        "I'm sorry if things aren't going well. Let me know how I can support you."
    ]
    return random.choice(negative_responses)

def get_greetings_response():
    greetings_responses = [
        "Hello there!",
        "Hi! How can I assist you?",
        "Greetings! What can I do for you today?",
        "Hey! What's up?",
        "Howdy! What brings you here?",
        "Hi there! Ready for a chat?"
    ]
    return random.choice(greetings_responses)

def get_farewells_response():
    farewells_responses = [
        "Goodbye! Take care.",
        "Farewell! Have a great day!",
        "See you later!",
        "Bye for now!",
        "Until next time!",
        "Take care and goodbye!"
    ]
    return random.choice(farewells_responses)

def get_love_response():
    love_responses = [
        "I love you too! 😊",
        "Sending virtual hugs! ❤️",
        "You're awesome! 😍",
        "Love and positivity to you!",
        "Feeling the love! ❤️"
    ]
    return random.choice(love_responses)

def get_casual_response():
    casual_responses = [
        "It's okay not to know sometimes!",
        "No worries, I understand.",
        "Alright then! Anything else on your mind?",
        "Cool! Anything else I can help you with?",
        "Thanks for letting me know!",
        "That's interesting! Tell me more."
    ]
    return random.choice(casual_responses)

def get_time_response():
    time_responses = [
        f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}",
        f"It's currently {datetime.datetime.now().strftime('%I:%M %p')}",
        f"{datetime.datetime.now().strftime('%H:%M')} on the clock",
        f"The clock says {datetime.datetime.now().strftime('%I:%M %p')}",
        f"Now it's {datetime.datetime.now().strftime('%I:%M %p')}"
    ]
    return random.choice(time_responses)

def get_date_response():
    date_responses = [
        f"Today's date is: {datetime.date.today().strftime('%d/%m/%y')}",
        f"It's {datetime.datetime.now().strftime('%A, %B %d, %Y')}",
        f"The date is {datetime.datetime.now().strftime('%Y-%m-%d')}",
        f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}",
        f"The calendar says it's {datetime.datetime.now().strftime('%Y-%m-%d')}"
    ]
    return random.choice(date_responses)

def process_query(query):
    global user_sentiment
    user_sentiment = analyze_sentiment(query)
    print(f"Sentiment: {user_sentiment}")

    # Respond based on sentiment
    if user_sentiment == "Positive":
        return get_positive_response()
    elif user_sentiment == "Negative":
        return get_negative_response()

    # Check for Wikipedia-specific queries
    if any(keyword in query.lower() for keyword in ['what is', 'search for', 'who is', 'when', 'where is']):
        try:
            # Extract the query without the Wikipedia keyword
            wikipedia_query = query.lower().replace('what is', '').replace('search for', '').replace('who is', '').replace('when', '').replace('where is', '').strip()
            # Search Wikipedia
            search_result = wikipedia.summary(wikipedia_query, sentences=2)
            return search_result
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options
            return f"Please be more specific. Did you mean {', '.join(options)}?"
        except wikipedia.exceptions.PageError:
            return "Sorry, I don't know about that."

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
        f"The date is {datetime.datetime.now().strftime('%Y-%m-%d')}",
        f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}",
        f"The calendar says it's {datetime.datetime.now().strftime('%Y-%m-%d')}"
    ]
    time_responses = [
        f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}",
        f"It's currently {datetime.datetime.now().strftime('%I:%M %p')}",
        f"{datetime.datetime.now().strftime('%H:%M')} on the clock",
        f"The clock says {datetime.datetime.now().strftime('%I:%M %p')}",
        f"Now it's {datetime.datetime.now().strftime('%I:%M %p')}"
    ]

    for word, response in casual_responses.items():
        if word in doc.text.lower():
            return response



    if any(word in greetings for word in [token.text.lower() for token in doc]):
        return get_greetings_response()

    elif any(greeting in farewells for greeting in [token.text.lower() for token in doc]):
        return get_farewells_response()

    elif any(phrase in doc.text.lower() for phrase in love_phrases):
        return get_love_response()

    elif any(interaction in doc.text.lower() for interaction in ['how are you', 'what\'s up', 'tell me a joke']):
        return "I'm doing well, thank you! How can I assist you today?"

    elif "weather" in nouns:
        return "I am not equipped to provide weather details, but I can search for it."

    elif "time" in nouns:
        return get_time_response()

    elif "date" in nouns:
        return get_date_response()

    elif "play" in verbs:
        video_title = query.replace("play", "").strip()
        pywhatkit.playonyt(video_title)
        return f"Playing the first video for '{video_title}' on YouTube."

    else:
        return "Sorry, I don't have information on that. Would you like me to check Wikipedia for you?(for serching just type search for xxxx)"
