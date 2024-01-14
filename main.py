import spacy
import datetime
import webbrowser
import sys
import pywhatkit
from bs4 import BeautifulSoup
import wikipedia
from spellchecker import SpellChecker
sys.path.append('path/to/your/venv/Lib/site-packages')
nlp = spacy.load("en_core_web_sm")

spell = SpellChecker()

def correct_spelling(query):
    words = query.split()
    corrected_words = [spell.correction(word) for word in words]
    return " ".join(corrected_words)

def process_query(query):
    doc = nlp(query)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    entities = [ent.text for ent in doc.ents]

    greetings = ['hi', 'hello', 'hola', 'hey', 'howdy', 'hi there', 'hey there']
    love_phrases = ['i love you', 'i love u', 'i luv u', 'love you','lub u','i lub u']
    if any(word in greetings for word in [token.text.lower() for token in doc]):
        return f"{query.capitalize()}, I'm your assistant. How can I help you?"
    elif any(phrase in doc.text.lower() for phrase in love_phrases):
        return "I love you too! 😊"
    elif any(interaction in doc.text.lower() for interaction in ['how are you', 'what\'s up', 'tell me a joke']):
        return "I'm doing well, thank you! How can I assist you today?"
    elif any(greeting in ['bi', 'goodbye', 'bye'] for greeting in [token.text.lower() for token in doc]):
        return "Goodbye! Have a great day."
    elif 'bye' in nouns:
        return "See you later."
    elif "time" in nouns:
        return f"It is {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif "weather" in nouns:
        return "I am not equipped to provide weather details, but I can search for it."
    elif "date" in nouns:
        return f"Today's date is: {datetime.date.today().strftime('%d/%m/%y')}"
    elif "play" in verbs:
        # Extract the video title from the query
        video_title = query.replace("play", "").strip()
        # Perform a YouTube search and play the first video
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
