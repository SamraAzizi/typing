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