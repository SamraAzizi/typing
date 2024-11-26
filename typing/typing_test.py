<<<<<<< HEAD
import streamlit as st
import time
import random
from datetime import datetime

class TypingTest:
    def __init__(self):
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "To be or not to be, that is the question.",
            "All that glitters is not gold.",
            "Life is like a box of chocolates, you never know what you're gonna get.",
            "In the end, it's not the years in your life that count. It's the life in your years."
        ]
        self.mistake_details = []  # List to store mistake details
        self.reset()

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.current_text = self.get_random_text()
        self.typed_text = ""
        self.is_complete = False
        self.wpm = 0
        self.accuracy = 0
        self.mistakes = 0
        self.mistake_details = []

    def next_text(self):
        """Move to the next text without resetting stats"""
        current_index = self.sample_texts.index(self.current_text)
        next_index = (current_index + 1) % len(self.sample_texts)
        self.current_text = self.sample_texts[next_index]
        self.typed_text = ""
        self.start_time = None
        self.end_time = None
        self.is_complete = False
        self.mistake_details = []

    def get_random_text(self):
        return random.choice(self.sample_texts)

    def start_test(self):
        if not self.start_time:
            self.start_time = time.time()
            self.is_complete = False

    def update_typed_text(self, text):
        if not text:
            self.typed_text = ""
            return
            
        if not self.start_time:
            self.start_test()
            
        # Track mistakes in detail
        self.mistake_details = []
        self.mistakes = 0
        for i in range(min(len(text), len(self.current_text))):
            if text[i] != self.current_text[i]:
                self.mistakes += 1
                self.mistake_details.append({
                    'position': i + 1,
                    'expected': self.current_text[i],
                    'typed': text[i]
                })
        
        self.typed_text = text
        
        # Check if test is complete
        if len(text) >= len(self.current_text):
            if not self.is_complete:  # Only calculate once
                self.end_time = time.time()
                self.is_complete = True
                self.calculate_results()

    def calculate_results(self):
        self.wpm = self.calculate_wpm()
        self.accuracy = self.calculate_accuracy()

    def calculate_wpm(self):
        if not self.start_time:
            return 0
            
        end = self.end_time if self.end_time else time.time()
        time_elapsed = max(end - self.start_time, 1)  # Avoid division by zero
        
        # Calculate WPM: (characters typed / 5) / minutes elapsed
        # 5 characters is considered one word
        char_count = len(self.typed_text)
        minutes = time_elapsed / 60
        wpm = (char_count / 5) / minutes if minutes > 0 else 0
        return round(wpm)

    def calculate_accuracy(self):
        if not self.typed_text:
            return 0
            
        correct_chars = 0
        total_chars = min(len(self.typed_text), len(self.current_text))
        
        for i in range(total_chars):
            if self.typed_text[i] == self.current_text[i]:
                correct_chars += 1
                
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0
        return round(accuracy, 2)

    def get_current_stats(self):
        if not self.start_time:
            return {"wpm": 0, "accuracy": 0, "mistakes": 0}
            
        current_time = time.time()
        current_text_len = len(self.typed_text)
        
        # Calculate current WPM
        minutes_elapsed = max((current_time - self.start_time) / 60, 0.000001)  # Avoid division by zero
        current_wpm = (current_text_len / 5) / minutes_elapsed
        
        # Calculate current accuracy
        current_accuracy = 0
        if current_text_len > 0:
            correct_chars = sum(1 for i in range(current_text_len) 
                              if i < len(self.current_text) and self.typed_text[i] == self.current_text[i])
            current_accuracy = (correct_chars / current_text_len) * 100
            
        return {
            "wpm": round(current_wpm),
            "accuracy": round(current_accuracy, 2),
            "mistakes": self.mistakes
        }

    def get_mistake_summary(self):
        """Get a summary of mistakes made"""
        if not self.mistake_details:
            return "No mistakes! Perfect typing! 🎯"
            
        summary = []
        for mistake in self.mistake_details:
            summary.append(
                f"Position {mistake['position']}: "
                f"Expected '{mistake['expected']}', "
                f"typed '{mistake['typed']}'"
            )
        return summary

    def get_results(self):
        return {
            'wpm': self.wpm,
            'accuracy': self.accuracy,
            'mistakes': self.mistakes,
            'mistake_details': self.get_mistake_summary(),
            'is_complete': self.is_complete,
            'text_number': self.sample_texts.index(self.current_text) + 1,
            'total_texts': len(self.sample_texts)
        }

def main():
    st.set_page_config(page_title="Advanced Typing Test", page_icon="⌨️")
    
    st.title("⌨️ Advanced Typing Test")
    st.write("Test your typing speed and accuracy!")

    # Session state initialization
    if 'test' not in st.session_state:
        st.session_state.test = TypingTest()

    # Display the text to type
    st.subheader("Type this text:")
    st.write(st.session_state.test.current_text)

    # Text input for typing
    typed_text = st.text_area("Start typing here:", key="typing_area", height=100)

    # Update typed text
    st.session_state.test.update_typed_text(typed_text)

    # Display results if test is complete
    if st.session_state.test.is_complete:
        st.success("Test Complete!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Words Per Minute", st.session_state.test.wpm)
        with col2:
            st.metric("Accuracy", f"{st.session_state.test.accuracy}%")
        with col3:
            st.metric("Mistakes", st.session_state.test.mistakes)

        if st.button("Try Again"):
            st.session_state.test.reset()
            st.experimental_rerun()

        if st.button("Next Text"):
            st.session_state.test.next_text()
            st.experimental_rerun()

        st.write("Mistake Details:")
        st.write(st.session_state.test.get_mistake_summary())

    # Display live statistics
    if st.session_state.test.start_time and not st.session_state.test.is_complete:
        current_stats = st.session_state.test.get_current_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current WPM", current_stats["wpm"])
        with col2:
            st.metric("Current Accuracy", f"{current_stats['accuracy']}%")
        with col3:
            st.metric("Mistakes", current_stats["mistakes"])

    # Sidebar with instructions
    with st.sidebar:
        st.header("Instructions")
        st.write("""
        1. Start typing in the text area
        2. Your timer will start automatically
        3. Results will show when you complete the text
        4. Click 'Try Again' for a new test
        5. Click 'Next Text' to move to the next text
        """)
        
        st.header("Tips")
        st.write("""
        - Focus on accuracy first, speed will come naturally
        - Keep your fingers on the home row keys
        - Look at the text, not your hands
        """)

if __name__ == "__main__":
    main()
=======
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
>>>>>>> e6e3b8015e6ba59d5e408430fe28aaeb7aabd071
