<<<<<<< HEAD
import streamlit as st
from typing_test import TypingTest
import time

def load_custom_css():
    st.markdown("""
        <style>
        .stTextArea textarea {
            font-family: 'Courier New', Courier, monospace;
            font-size: 18px;
        }
        
        .text-display {
            font-family: 'Courier New', Courier, monospace;
            font-size: 18px;
            line-height: 1.5;
        }
        
        /* Fixed button container at bottom with red background */
        .button-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 20px;
            background-color: #FF0000;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        
        /* Custom button styling */
        .big-button {
            display: inline-block;
            padding: 20px 40px;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            border-radius: 15px;
            margin: 10px;
            width: 300px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        
        .retry-button {
            background-color: #FFFFFF;
            color: #FF0000;
            border: 3px solid #FFFFFF;
        }
        
        .retry-button:hover {
            background-color: #FF0000;
            color: #FFFFFF;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.3);
            cursor: pointer;
        }
        
        .next-button {
            background-color: #FFFFFF;
            color: #FF0000;
            border: 3px solid #FFFFFF;
        }
        
        .next-button:hover {
            background-color: #FF0000;
            color: #FFFFFF;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.3);
            cursor: pointer;
        }
        
        /* Add padding to main content to prevent overlap with fixed buttons */
        .main-content {
            margin-bottom: 120px;
        }
        </style>
    """, unsafe_allow_html=True)

def generate_text_display(original_text, typed_text):
    if not typed_text:
        return original_text
        
    html = []
    for i, char in enumerate(original_text):
        if i < len(typed_text):
            if typed_text[i] == char:
                html.append(f'<span class="char-correct">{char}</span>')
            else:
                html.append(f'<span class="char-incorrect">{char}</span>')
        elif i == len(typed_text):
            html.append(f'<span class="char-current">{char}</span>')
        else:
            html.append(char)
    return ''.join(html)

def main():
    st.set_page_config(page_title="Typing Speed Test", page_icon="⌨️")
    load_custom_css()
    
    # Wrap all content except buttons in a div with margin-bottom
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.title("⌨️ Typing Speed Test")
    
    # Initialize the typing test
    if 'test' not in st.session_state:
        st.session_state.test = TypingTest()

    # Show text progress
    results = st.session_state.test.get_results()
    st.markdown(f"""
        <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px; margin: 10px 0;'>
            <h3 style='margin: 0;'>Text {results['text_number']} of {results['total_texts']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # Display the text to type
    st.markdown("### Text to Type:")
    display_text = generate_text_display(st.session_state.test.current_text, st.session_state.test.typed_text)
    st.markdown(f"""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; margin: 20px 0;">
            <div class="text-display" style="background-color: #ffffff; color: #333; font-weight: 500;">
                {display_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Text input for typing
    typed_text = st.text_area("Start typing here:", key="typing_area", height=100)

    # Update typed text and check progress
    st.session_state.test.update_typed_text(typed_text)

    # Create columns for metrics
    col1, col2, col3 = st.columns(3)

    # Display results if test is complete
    if st.session_state.test.is_complete:
        st.success("Test Complete! 🎉")
        
        with col1:
            st.metric("Final WPM", results['wpm'])
        with col2:
            st.metric("Final Accuracy", f"{results['accuracy']}%")
        with col3:
            st.metric("Total Mistakes", results['mistakes'])

        # Display mistake details
        if results['mistakes'] > 0:
            st.markdown("### ❌ Mistake Details")
            st.markdown("""
                <div style="background-color: #fff5f5; padding: 20px; border-radius: 10px; border: 2px solid #ffe0e0; margin: 20px 0;">
            """, unsafe_allow_html=True)
            
            if isinstance(results['mistake_details'], list):
                for mistake in results['mistake_details']:
                    st.write(mistake)
            else:
                st.write(results['mistake_details'])
                
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("### ✅ Perfect Score!")
            st.success("No mistakes! Excellent typing! 🎯")

        # Add some space before buttons
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Simple button container with two columns
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 TRY AGAIN", type="primary", use_container_width=True):
                st.session_state.test.reset()
                st.experimental_rerun()
        with col2:
            if st.button("➡️ NEXT TEXT", type="primary", use_container_width=True):
                st.session_state.test.next_text()
                st.experimental_rerun()

    # Display live statistics
    elif st.session_state.test.start_time:
        current_stats = st.session_state.test.get_current_stats()
        
        with col1:
            st.metric("Current WPM", current_stats["wpm"])
        with col2:
            st.metric("Current Accuracy", f"{current_stats['accuracy']}%")
        with col3:
            st.metric("Mistakes", current_stats["mistakes"])

        # Progress indicator
        progress = len(typed_text) / len(st.session_state.test.current_text)
        st.progress(min(progress, 1.0))

    # Sidebar with instructions and tips
    with st.sidebar:
        st.header("📝 Instructions")
        st.write("""
        1. Start typing in the text area
        2. Your timer will start automatically
        3. Results will show when you complete the text
        4. Use the buttons at the bottom:
           - 🔄 TRY AGAIN (Red)
           - ➡️ NEXT TEXT (Blue)
        """)
        
        st.header("💡 Tips")
        st.write("""
        - Focus on accuracy first, speed will come naturally
        - Keep your fingers on the home row keys (F and J have small bumps)
        - Look at the text, not your hands
        - Practice regularly to improve
        """)

    # Close the main content wrapper
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
=======
import streamlit as st
import time
import random
import json
from datetime import datetime
import os
from config import APP_SETTINGS, DB_CONFIG, THEMES

# Extended practice texts with categories
PRACTICE_TEXTS = {
    'Programming': [
        "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)",
        "for i in range(len(array)):\n    if array[i] > max_val:\n        max_val = array[i]",
        "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None",
        "SELECT customer_name, SUM(order_total) FROM orders GROUP BY customer_id HAVING COUNT(*) > 5;",
        "git commit -m 'feat: implement user authentication' && git push origin main",
    ],
    'Business': [
        "The quarterly revenue exceeded expectations, showing a 15% year-over-year growth.",
        "Please review the attached proposal and provide feedback by end of business day.",
        "The stakeholder meeting is scheduled for Thursday at 2 PM in Conference Room A.",
        "Our market analysis indicates a significant opportunity in the Asia-Pacific region.",
    ],
    'Literature': [
        "It was the best of times, it was the worst of times, it was the age of wisdom.",
        "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer.",
        "All happy families are alike; each unhappy family is unhappy in its own way.",
    ],
}

# Add this after the PRACTICE_TEXTS dictionary
def get_typing_guide():
    return """
    🎯 Follow these steps:
    1. Select a category above
    2. Look at the text displayed in the box
    3. Type the exact text in the input area below
    4. Watch for real-time feedback:
       • Green text = Correct typing
       • Red text = Mistakes
    5. Your stats will update as you type
    6. Complete the text to see your final score
    """

# Custom CSS for styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #f8f9fa;
        }
        
        /* Text display styling */
        .text-display {
            font-size: 1.2rem;
            line-height: 1.6;
            padding: 1.5rem;
            background-color: #ffffff;
            border-radius: 10px;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }
        
        /* Typing area styling */
        .stTextArea textarea {
            font-size: 1.2rem;
            line-height: 1.6;
            font-family: 'Courier New', monospace;
            padding: 1rem;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: border-color 0.3s ease;
        }
        
        .stTextArea textarea:focus {
            border-color: #1f77b4;
            box-shadow: 0 0 0 2px rgba(31, 119, 180, 0.2);
        }
        
        /* Character feedback styling */
        .char-correct {
            color: #28a745;
            background-color: #e6ffe6;
            transition: all 0.2s ease;
            padding: 0 1px;
            border-radius: 2px;
        }
        
        .char-incorrect {
            color: #dc3545;
            background-color: #ffe6e6;
            text-decoration: underline wavy #dc3545;
            transition: all 0.2s ease;
            padding: 0 1px;
            border-radius: 2px;
            animation: shake 0.5s ease-in-out;
        }
        
        /* Results styling */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s ease;
            border: 1px solid #e0e0e0;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        
        .metric-card h3 {
            color: #666;
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-card h2 {
            color: #1f77b4;
            font-size: 2rem;
            margin: 0;
        }
        
        /* Progress bar styling */
        .stProgress > div > div {
            background-color: #28a745;
            height: 8px;
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        /* Animation keyframes */
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-2px); }
            75% { transform: translateX(2px); }
        }
        
        /* Category selector styling */
        .stSelectbox {
            margin-bottom: 1rem;
        }
        
        .stSelectbox > div > div {
            background-color: white;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #1a5f8c;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Title styling */
        h1 {
            color: #1f77b4;
            margin-bottom: 1rem;
            font-weight: 800;
        }
        
        h3 {
            color: #666;
            margin-bottom: 2rem;
        }
        
        /* Performance feedback styling */
        .success {
            padding: 1rem;
            border-radius: 8px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            margin: 1rem 0;
        }
        
        .warning {
            padding: 1rem;
            border-radius: 8px;
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
            margin: 1rem 0;
        }
        
        /* Guide styling */
        .guide {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
            margin: 1rem 0;
        }
        
        .guide ul {
            list-style-type: none;
            padding-left: 1rem;
        }
        
        .guide li {
            margin: 0.5rem 0;
            color: #666;
        }
        
        /* Text to type styling */
        .text-to-type {
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
            line-height: 1.6;
            padding: 1.5rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            margin: 1rem 0;
        }
        
        /* Category selector enhancement */
        .category-select {
            margin: 1rem 0;
            padding: 1rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Instructions styling */
        .instructions {
            background-color: #e7f5ff;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .instructions h4 {
            color: #1f77b4;
            margin-bottom: 0.5rem;
        }
        
        /* Emoji emphasis */
        .emoji-guide {
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

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

def calculate_score(accuracy, wpm, mistakes):
    base_score = (accuracy * wpm) / 100
    penalty = mistakes * APP_SETTINGS['SCORING']['MISTAKE_PENALTY']
    final_score = max(0, base_score - penalty)
    return round(final_score)

def generate_colored_text(original_text, typed_text):
    """Generate HTML with color-coded feedback for each character"""
    html = []
    for i, orig_char in enumerate(original_text):
        if i < len(typed_text):
            if typed_text[i] == orig_char:
                html.append(f'<span class="char-correct">{orig_char}</span>')
            else:
                html.append(f'<span class="char-incorrect">{typed_text[i]}</span>')
        else:
            html.append(orig_char)
    
    # Add any extra characters typed by the user in red
    if len(typed_text) > len(original_text):
        for char in typed_text[len(original_text):]:
            html.append(f'<span class="char-incorrect">{char}</span>')
    
    return ''.join(html)

def typing_practice():
    st.markdown(get_typing_guide())
    
    if 'practice_text' not in st.session_state:
        st.markdown("### 📝 Choose your category:")
        category = st.selectbox("", list(PRACTICE_TEXTS.keys()))
        st.session_state.practice_text = random.choice(PRACTICE_TEXTS[category])
        st.session_state.mistakes = 0
        st.session_state.correct_chars = 0
    
    # Display original text with better formatting
    st.markdown("### ✨ Text to type:")
    st.markdown('<div class="text-display"><code>' + 
                st.session_state.practice_text + '</code></div>', 
                unsafe_allow_html=True)
    
    st.markdown("### ⌨️ Your typing area:")
    # Real-time feedback area
    feedback_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    typed_text = st.text_area("Start typing:", key="practice_area", height=100)
    
    if len(typed_text) == 1 and 'practice_start_time' not in st.session_state:
        st.session_state.practice_start_time = time.time()
        st.session_state.mistakes = 0
        st.session_state.correct_chars = 0
    
    if typed_text:
        # Update progress bar
        progress = len(typed_text) / len(st.session_state.practice_text)
        progress_placeholder.progress(min(progress, 1.0))
        
        # Show real-time colored feedback
        highlighted_text = generate_colored_text(
            st.session_state.practice_text, 
            typed_text
        )
        feedback_placeholder.markdown(
            f'<div class="text-display">{highlighted_text}</div>', 
            unsafe_allow_html=True
        )
        
        # Update stats
        if 'practice_start_time' in st.session_state:
            current_time = time.time()
            current_wpm = calculate_wpm(st.session_state.practice_start_time, current_time, typed_text)
            current_accuracy = calculate_accuracy(st.session_state.practice_text[:len(typed_text)], typed_text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current WPM", current_wpm)
            with col2:
                st.metric("Accuracy", f"{current_accuracy}%")
            with col3:
                st.metric("Mistakes", st.session_state.mistakes)
    
    # Check if practice is complete
    if len(typed_text) >= len(st.session_state.practice_text):
        show_results(typed_text)

def show_results(typed_text):
    end_time = time.time()
    wpm = calculate_wpm(st.session_state.practice_start_time, end_time, typed_text)
    accuracy = calculate_accuracy(st.session_state.practice_text, typed_text)
    score = calculate_score(accuracy, wpm, st.session_state.mistakes)
    
    st.markdown("### Results")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3>WPM</h3>
                <h2>{}</h2>
            </div>
        """.format(wpm), unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>Accuracy</h3>
                <h2>{}%</h2>
            </div>
        """.format(accuracy), unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>Mistakes</h3>
                <h2>{}</h2>
            </div>
        """.format(st.session_state.mistakes), unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-card">
                <h3>Score</h3>
                <h2>{}</h2>
            </div>
        """.format(score), unsafe_allow_html=True)
    
    # Performance feedback
    if score >= 90:
        st.balloons()
        st.success("🏆 Outstanding! You're a typing master!")
    elif score >= 70:
        st.success("🌟 Great job! Keep practicing!")
    elif score >= 50:
        st.info("💪 Good effort! You're improving!")
    else:
        st.warning("📈 Keep practicing to improve your speed and accuracy!")
    
    if st.button("Try Another Text", key="try_another"):
        reset_practice_session()
        st.experimental_rerun()

def main():
    st.set_page_config(page_title="Typing Master", page_icon="⌨️", layout="wide")
    load_custom_css()
    
    st.title("⌨️ Typing Master")
    st.markdown("### 🚀 Improve your typing speed and accuracy")
    
    # Add instructions
    st.markdown("""
        <div class="instructions">
            <h4>📝 How to use this typing test:</h4>
            <ul>
                <li>🎯 Choose a category that interests you</li>
                <li>👀 Read the text carefully</li>
                <li>⌨️ Type exactly what you see</li>
                <li>✅ Get instant feedback as you type</li>
                <li>📊 See your results and improve!</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    typing_practice()

if __name__ == "__main__":
    main()
>>>>>>> e6e3b8015e6ba59d5e408430fe28aaeb7aabd071
