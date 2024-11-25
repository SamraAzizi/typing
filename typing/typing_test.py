import streamlit as st
import time
import random
from datetime import datetime

# Sample text passages for typing test
sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "Life is like a box of chocolates, you never know what you're gonna get.",
    "In the end, it's not the years in your life that count. It's the life in your years."
]

def calculate_wpm(start_time, end_time, typed_text):
    time_elapsed = end_time - start_time
    words = len(typed_text.split())
    wpm = (words / time_elapsed) * 60
    return round(wpm)

def calculate_accuracy(original_text, typed_text):
    if len(typed_text) == 0:
        return 0
    
    correct_chars = sum(1 for a, b in zip(original_text, typed_text) if a == b)
    accuracy = (correct_chars / len(original_text)) * 100
    return round(accuracy, 2)

def main():
    st.set_page_config(page_title="Advanced Typing Test", page_icon="⌨️")
    
    st.title("⌨️ Advanced Typing Test")
    st.write("Test your typing speed and accuracy!")

    # Session state initialization
    if 'current_text' not in st.session_state:
        st.session_state.current_text = random.choice(sample_texts)
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'test_complete' not in st.session_state:
        st.session_state.test_complete = False

    # Display the text to type
    st.subheader("Type this text:")
    st.write(st.session_state.current_text)

    # Text input for typing
    typed_text = st.text_area("Start typing here:", key="typing_area", height=100)

    # Start timer when user starts typing
    if len(typed_text) == 1 and st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # Check if the test is complete
    if len(typed_text) >= len(st.session_state.current_text) and not st.session_state.test_complete:
        end_time = time.time()
        wpm = calculate_wpm(st.session_state.start_time, end_time, typed_text)
        accuracy = calculate_accuracy(st.session_state.current_text, typed_text)
        
        st.session_state.test_complete = True
        st.session_state.wpm = wpm
        st.session_state.accuracy = accuracy

    # Display results if test is complete
    if st.session_state.test_complete:
        st.success("Test Complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Words Per Minute", st.session_state.wpm)
        with col2:
            st.metric("Accuracy", f"{st.session_state.accuracy}%")

        if st.button("Try Again"):
            st.session_state.current_text = random.choice(sample_texts)
            st.session_state.start_time = None
            st.session_state.test_complete = False
            st.experimental_rerun()

    # Display live statistics
    if st.session_state.start_time and not st.session_state.test_complete:
        current_time = time.time()
        current_wpm = calculate_wpm(st.session_state.start_time, current_time, typed_text)
        current_accuracy = calculate_accuracy(st.session_state.current_text[:len(typed_text)], typed_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current WPM", current_wpm)
        with col2:
            st.metric("Current Accuracy", f"{current_accuracy}%")

    # Sidebar with instructions
    with st.sidebar:
        st.header("Instructions")
        st.write("""
        1. Start typing in the text area
        2. Your timer will start automatically
        3. Results will show when you complete the text
        4. Click 'Try Again' for a new test
        """)
        
        st.header("Tips")
        st.write("""
        - Focus on accuracy first, speed will come naturally
        - Keep your fingers on the home row keys
        - Look at the text, not your hands
        """)

if __name__ == "__main__":
    main() 