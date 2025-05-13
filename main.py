import streamlit as st
import os
import random
from pathlib import Path
import traceback

# ---------- CONFIGURATION ----------
st.set_page_config(
    page_title="Toddler Learning App", 
    layout="centered",
    page_icon="🧒"
)

# ---------- CONSTANTS ----------
IMAGE_PATH = "assets/images"
AUDIO_PATH = "assets/audio"

# ---------- DATA ----------
LETTERS = [chr(i) for i in range(97, 123)]  # a-z
WORDS = {
    "a": "apple", "b": "ball", "c": "cat", "d": "dog", "e": "elephant",
    "f": "fish", "g": "goat", "h": "hat", "i": "ice_cream", "j": "jar",
    "k": "kite", "l": "lion", "m": "monkey", "n": "nest", "o": "orange",
    "p": "pen", "q": "queen", "r": "rabbit", "s": "shoe", "t": "tree",
    "u": "umbrella", "v": "violin", "w": "watch", "x": "xylophone",
    "y": "yak", "z": "zebra"
}

# ---------- HELPER FUNCTIONS ----------
def load_asset(asset_type, name):
    """Helper function to load assets with error handling"""
    try:
        ext = "png" if asset_type == "image" else "mp3"
        path = Path(f"assets/{'images' if asset_type == 'image' else 'audio'}/{name}.{ext}")
        if not path.exists():
            st.sidebar.warning(f"Missing {asset_type} for: {name}")
            return None
        return str(path)
    except Exception as e:
        st.sidebar.error(f"Error loading {asset_type}: {str(e)}")
        return None

def reset_quiz():
    """Reset quiz state"""
    st.session_state.quiz_index = 0
    st.session_state.quiz_order = random.sample(LETTERS, len(LETTERS))
    st.session_state.submitted = False
    st.session_state.selected_option = None
    st.session_state.options = []

# ---------- SESSION STATE INITIALIZATION ----------
if "page" not in st.session_state:
    st.session_state.page = "Alphabet Learning"

if "quiz_index" not in st.session_state:
    reset_quiz()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🧒 Toddler Learning")
    activity = st.radio(
        "Choose Activity", 
        ["Alphabet Learning", "Word Matching Game"],
        index=0 if st.session_state.get("page") == "Alphabet Learning" else 1
    )
    st.session_state.page = activity
    
    if activity == "Word Matching Game":
        if st.button("🔁 Restart Quiz"):
            reset_quiz()
    
    st.markdown("---")
    st.caption("Made with ❤️ for toddlers")

try:
    # ---------- ALPHABET LEARNING PAGE ----------
    if st.session_state.page == "Alphabet Learning":
        st.title("🌟 Learn the Alphabet")
        st.caption("Tap each letter to hear its sound!")
        
        # Display in a grid
        cols = st.columns(4)
        col_index = 0
        
        for letter in LETTERS:
            with cols[col_index]:
                # Letter card
                with st.expander(f"{letter.upper()}", expanded=True):
                    # Display letter image
                    image_path = load_asset("image", letter)
                    if image_path:
                        st.image(image_path, use_container_width=True)
                    
                    # Display word image
                    word = WORDS[letter]
                    word_image_path = load_asset("image", word)
                    if word_image_path:
                        st.image(word_image_path, caption=word.capitalize(), use_container_width=True)
                    
                    # Audio player with better error handling
                    audio_path = load_asset("audio", letter)
                    if audio_path:
                        if st.button(f"🔊 Play {letter.upper()} sound", key=f"audio_{letter}"):
                            try:
                                with open(audio_path, "rb") as f:
                                    audio_bytes = f.read()
                                st.audio(audio_bytes, format="audio/mp3")
                            except Exception as e:
                                st.error(f"Couldn't play audio: {str(e)}")
            
            col_index = (col_index + 1) % 4

    # ---------- WORD MATCHING GAME PAGE ----------
    elif st.session_state.page == "Word Matching Game":
        st.title("🎮 Word Matching Game")
        st.caption("Match the letter with the correct word!")
        
        # Progress indicator
        progress = (st.session_state.quiz_index + 1) / len(LETTERS)
        st.progress(progress)
        st.caption(f"Question {st.session_state.quiz_index + 1} of {len(LETTERS)}")
        
        # Current question
        letter = st.session_state.quiz_order[st.session_state.quiz_index]
        correct_word = WORDS[letter]
        
        # Display the letter
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"## {letter.upper()}")
            image_path = load_asset("image", letter)
            if image_path:
                st.image(image_path, width=200)
            
            # Play sound button with error handling
            audio_path = load_asset("audio", letter)
            if audio_path:
                if st.button("🔊 Play Sound", key=f"game_audio_{letter}"):
                    try:
                        with open(audio_path, "rb") as f:
                            audio_bytes = f.read()
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Couldn't play audio: {str(e)}")
        
        # Generate answer options if not already generated
        if "options" not in st.session_state or not st.session_state.options:
            other_words = [w for w in WORDS.values() if w != correct_word]
            st.session_state.options = random.sample(other_words, 2) + [correct_word]
            random.shuffle(st.session_state.options)
        
        # Display options
        with col2:
            st.markdown("### Which picture matches this letter?")
            
            # Show as radio buttons for better selection tracking
            selected_option = st.radio(
                "Select an option:",
                st.session_state.options,
                index=None,
                key=f"option_{letter}"
            )
            
            if selected_option:
                st.session_state.selected_option = selected_option
            
            # Submit button
            if st.session_state.get("selected_option") and not st.session_state.get("submitted", False):
                if st.button("✅ Submit Answer"):
                    st.session_state.submitted = True
        
        # Show results after submission
        if st.session_state.get("submitted", False):
            st.markdown("---")
            if st.session_state.selected_option == correct_word:
                st.success("🎉 Correct! Great job!")
                st.balloons()
            else:
                st.error(f"Oops! The correct answer was: {correct_word.capitalize()}")
            
            # Show the correct image
            correct_image_path = load_asset("image", correct_word)
            if correct_image_path:
                st.image(correct_image_path, caption=correct_word.capitalize(), width=200)
            
            # Next button
            if st.button("➡️ Next Question"):
                st.session_state.quiz_index += 1
                st.session_state.submitted = False
                st.session_state.selected_option = None
                st.session_state.options = []
                
                # Check if quiz is complete
                if st.session_state.quiz_index >= len(LETTERS):
                    st.balloons()
                    st.success("🌈 You completed the entire alphabet!")
                    if st.button("🔄 Play Again"):
                        reset_quiz()
                
                st.rerun()

except Exception as e:
    st.error("An unexpected error occurred")
    st.code(traceback.format_exc())
    if st.button("Restart App"):
        st.session_state.clear()
        st.rerun()
