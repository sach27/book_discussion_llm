import openai
import random
import re
from difflib import get_close_matches
import streamlit as st

# Hardcoded Books and Perspectives
books = {
    "Black Swan": {
        "Risk Management": "The book highlights how we underestimate the impact of rare, unpredictable events.",
        "Cognitive Biases": "Nassim Taleb explores how human psychology struggles with randomness and uncertainty.",
        "Market Crashes": "Black Swan events have historically caused financial turmoil, and this book discusses their significance."
    },
    "As a Man Thinketh": {
        "Power of Thought": "James Allen emphasizes how our thoughts shape our reality and future.",
        "Self-Improvement": "The book discusses how disciplined thinking leads to a better life.",
        "Mindset and Success": "Your mindset is the key driver behind success and personal growth."
    },
    "Homo Deus": {
        "Future of Humanity": "Yuval Noah Harari explores how humans might evolve with AI and biotechnology.",
        "Religion and Science": "The book discusses how religion and science will shape our future.",
        "Human vs AI": "Homo Deus questions what it means to be human in the age of artificial intelligence."
    },
    "Sixteen Stormy Days": {
        "Constitutional Debates": "The book covers the intense debates after India’s independence.",
        "Role of Ambedkar": "A deep dive into Ambedkar’s contributions to shaping India’s constitution.",
        "Democracy in India": "Examines how India transitioned into a democratic state."
    },
    "The Alchemist": {
        "Personal Legend": "Paulo Coelho emphasizes the journey to find one’s destiny.",
        "Spiritual Growth": "The novel explores spiritual enlightenment through Santiago’s journey.",
        "Dreams and Fate": "Fate and dreams are deeply intertwined in this philosophical novel."
    },
    "Atomic Habits": {
        "Habit Formation": "James Clear breaks down the science behind building good habits.",
        "Small Changes, Big Impact": "The power of small, consistent improvements is key to success.",
        "Behavioral Psychology": "Explores how habits are deeply rooted in human behavior."
    }
}

def get_closest_match(user_input, choices):
    matches = get_close_matches(user_input, choices, n=1, cutoff=0.6)
    return matches[0] if matches else None

def extract_book_name(user_input):
    words = re.findall(r'\b\w+\b', user_input)  # Extract words from input
    book_titles = list(books.keys())
    
    for size in range(3, 0, -1):  # Try longer phrases first
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i:i + size])
            match = get_closest_match(phrase, book_titles)
            if match:
                return match
    return None

# Streamlit UI
st.title("Book Perspective Chatbot")
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

if api_key:
    openai.api_key = api_key
    st.sidebar.success("API Key set successfully!")

if "book_selected" not in st.session_state:
    st.session_state["book_selected"] = None
if "perspective_selected" not in st.session_state:
    st.session_state["perspective_selected"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

book_selected = st.selectbox("Select a book to discuss:", list(books.keys()), index=0 if not st.session_state["book_selected"] else list(books.keys()).index(st.session_state["book_selected"]))
if book_selected:
    st.session_state["book_selected"] = book_selected
    perspective_selected = st.selectbox("Select a perspective:", list(books[book_selected].keys()), index=0 if not st.session_state["perspective_selected"] else list(books[book_selected].keys()).index(st.session_state["perspective_selected"]))
    if perspective_selected:
        st.session_state["perspective_selected"] = perspective_selected
        if not st.session_state["messages"]:
            context = books[book_selected][perspective_selected]
            st.session_state["messages"].append({"role": "system", "content": context})
        
        st.write(f"**Selected Book:** {book_selected}")
        st.write(f"**Selected Perspective:** {perspective_selected}")

user_input = st.text_input("You:")
if user_input:
    if user_input.lower() in ["exit", "quit"]:
        st.write("Chat ended. Refresh to start a new discussion.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"]
        )
        response_text = response["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "assistant", "content": response_text})
        
        for message in st.session_state["messages"][-5:]:  # Show last 5 messages
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**ChatGPT:** {message['content']}")
