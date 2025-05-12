import streamlit as st
import os
import random

# ---------- CONFIGURATION ----------
st.set_page_config(page_title="Toddler Learning App", layout="centered")

# ---------- DATA ----------
letters = [chr(i) for i in range(97, 123)]
words = {
    "a": "apple", "b": "ball", "c": "cat", "d": "dog", "e": "elephant",
    "f": "fish", "g": "goat", "h": "hat", "i": "ice_cream", "j": "jar",
    "k": "kite", "l": "lion", "m": "monkey", "n": "nest", "o": "orange",
    "p": "pen", "q": "queen", "r": "rabbit", "s": "shoe", "t": "tree",
    "u": "umbrella", "v": "violin", "w": "watch", "x": "xylophone",
    "y": "yak", "z": "zebra"
}
image_path = "assets/images"
audio_path = "assets/audio"

# ---------- SESSION STATE INITIALIZATION ----------
if "page" not in st.session_state:
    st.session_state.page = "Alphabet Learning"
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_order" not in st.session_state:
    st.session_state.quiz_order = random.sample(letters, len(letters))
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "options" not in st.session_state:
    st.session_state.options = []

# ---------- SIDEBAR ----------
activity = st.sidebar.selectbox("Choose Activity", ["Alphabet Learning", "Word Matching Game"])
st.session_state.page = activity

# ---------- ALPHABET LEARNING ----------
if st.session_state.page == "Alphabet Learning":
    st.title("Learn the Alphabets")

    for letter in letters:
        st.subheader(f"Letter: {letter.upper()}")
        st.image(os.path.join(image_path, f"{letter}.png"), width=120)

        word = words[letter]
        st.image(os.path.join(image_path, f"{word}.png"), caption=word.capitalize(), width=120)

        audio_file = os.path.join(audio_path, f"{letter}.mp3")
        if os.path.exists(audio_file):
            st.audio(audio_file)

# ---------- WORD MATCHING GAME ----------
elif st.session_state.page == "Word Matching Game":
    st.title("Match the Word with the Image")

    letter = st.session_state.quiz_order[st.session_state.quiz_index]
    correct_word = words[letter]

    st.image(os.path.join(image_path, f"{letter}.png"), width=150)
    st.markdown(f"**Letter: {letter.upper()}**")

    # Generate options ONCE per question
    if not st.session_state.options:
        other_words = [w for w in words.values() if w != correct_word]
        st.session_state.options = random.sample(other_words, 2) + [correct_word]
        random.shuffle(st.session_state.options)

    # Radio input (track user selection)
    selected = st.radio("Select the matching word:", st.session_state.options, index=0)

    # Store user selection before clicking submit
    if selected != st.session_state.selected_option:
        st.session_state.selected_option = selected

    # SUBMIT BUTTON
    if st.button("Submit") and not st.session_state.submitted:
        st.session_state.submitted = True
        if st.session_state.selected_option == correct_word:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! The correct answer was: {correct_word.capitalize()}")

    # NEXT BUTTON
    if st.session_state.submitted:
        if st.button("Next"):
            st.session_state.quiz_index += 1
            st.session_state.submitted = False
            st.session_state.selected_option = None
            st.session_state.options = []
            if st.session_state.quiz_index >= len(letters):
                st.session_state.quiz_index = 0  # Restart
