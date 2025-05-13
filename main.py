import streamlit as st
import random
from pathlib import Path

# ---------- CONFIGURATION ----------
st.set_page_config(
    page_title="Toddler Learning Fun",
    layout="centered",
    page_icon="🧒"
)

# ---------- CONSTANTS ----------
IMAGE_PATH = "assets/images"
AUDIO_PATH = "assets/audio"
COLORS = {
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#00FF00",
    "yellow": "#FFFF00",
    "orange": "#FFA500",
    "purple": "#800080"
}

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
    try:
        ext = "png" if asset_type == "image" else "mp3"
        path = Path(f"assets/{'images' if asset_type == 'image' else 'audio'}/{name}.{ext}")
        if not path.exists():
            return None
        return str(path)
    except:
        return None

def reset_game_state():
    st.session_state.quiz_index = 0
    st.session_state.quiz_order = random.sample(LETTERS, len(LETTERS))
    st.session_state.submitted = False
    st.session_state.selected_option = None
    st.session_state.options = []

    correct_color = random.choice(list(COLORS.keys()))
    other_colors = [c for c in COLORS.keys() if c != correct_color]
    options = random.sample(other_colors, 2) + [correct_color]
    random.shuffle(options)

    st.session_state.color_game = {
        "score": 0,
        "current_color": correct_color,
        "options": options
    }
    st.session_state.color_selected = None
    st.session_state.color_feedback = ""

def set_background_image(image_path):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_path}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- GAME COMPONENTS ----------
def letter_learning_page():
    st.title("🌟 ABC Fun Time!")
    cols = st.columns(4)
    for idx, letter in enumerate(LETTERS):
        with cols[idx % 4]:
            with st.expander(f"{letter.upper()}", expanded=True):
                if img_path := load_asset("image", letter):
                    st.image(img_path, use_container_width=True)
                word = WORDS[letter]
                if word_img := load_asset("image", word):
                    st.image(word_img, use_container_width=True)
                if audio_path := load_asset("audio", letter):
                    if st.button(f"🔊 Hear {letter.upper()}", key=f"sound_{letter}"):
                        st.audio(audio_path, format='audio/mp3')

def image_matching_game():
    st.title("🖼️ Picture Match Game")
    progress = (st.session_state.quiz_index + 1) / len(LETTERS)
    st.progress(progress)
    st.caption(f"Match {st.session_state.quiz_index + 1} of {len(LETTERS)}")

    letter = st.session_state.quiz_order[st.session_state.quiz_index]
    correct_word = WORDS[letter]

    if audio_path := load_asset("audio", letter):
        st.audio(audio_path, format='audio/mp3', autoplay=True)

    st.markdown(f"## Find the picture that starts with: {letter.upper()}")

    if not st.session_state.options:
        other_words = [w for w in WORDS.values() if w != correct_word]
        wrong_options = random.sample(other_words, 2)
        st.session_state.options = wrong_options + [correct_word]
        random.shuffle(st.session_state.options)

    cols = st.columns(3)
    for idx, option in enumerate(st.session_state.options):
        with cols[idx % 3]:
            if img_path := load_asset("image", option):
                if st.button("", key=f"opt_{idx}"):
                    st.session_state.selected_option = option
                st.image(img_path, use_container_width=True)
                st.caption(option.capitalize())

    if st.session_state.submitted:
        if st.session_state.selected_option == correct_word:
            st.success("🎉 Correct! Great job!")
            st.balloons()
        else:
            st.error(f"Try again! It's {correct_word.capitalize()}")

        if st.button("➡️ Next Picture"):
            next_question()

    elif st.session_state.selected_option and st.button("✅ Check Answer"):
        st.session_state.submitted = True
        st.rerun()

def next_question():
    st.session_state.quiz_index += 1
    st.session_state.submitted = False
    st.session_state.selected_option = None
    st.session_state.options = []

    if st.session_state.quiz_index >= len(LETTERS):
        st.balloons()
        st.success("🌈 You finished all letters!")
        if st.button("🔄 Play Again"):
            reset_game_state()
    st.rerun()

def color_recognition_game():
    st.title("🎨 Color Finder")

    if "color_selected" not in st.session_state:
        st.session_state.color_selected = None
    if "color_feedback" not in st.session_state:
        st.session_state.color_feedback = ""

    color = st.session_state.color_game['current_color']
    st.markdown(f"## Find the color: {color.capitalize()}")

    cols = st.columns(3)
    for idx, option in enumerate(st.session_state.color_game['options']):
        with cols[idx % 3]:
            if st.button("", key=f"color_{option}"):
                st.session_state.color_selected = option
                if option == color:
                    st.session_state.color_game['score'] += 1
                    st.session_state.color_feedback = "✅ Correct! 🎉"
                else:
                    st.session_state.color_feedback = f"❌ Oops! That's {option.capitalize()}."

            st.markdown(
                f"""<div style='background-color:{COLORS[option]}; 
                    height:100px; border-radius:10px;'></div>""",
                unsafe_allow_html=True
            )

    if st.session_state.color_selected:
        if "Correct" in st.session_state.color_feedback:
            st.success(st.session_state.color_feedback)
            st.balloons()
        else:
            st.error(st.session_state.color_feedback)

        if st.button("➡️ Next Color"):
            st.session_state.color_selected = None
            st.session_state.color_feedback = ""

            next_color = random.choice(list(COLORS.keys()))
            other_colors = [c for c in COLORS.keys() if c != next_color]
            new_options = random.sample(other_colors, 2) + [next_color]
            random.shuffle(new_options)

            st.session_state.color_game['current_color'] = next_color
            st.session_state.color_game['options'] = new_options

            st.rerun()

    st.markdown(f"**Score: {st.session_state.color_game['score']}**")

# ---------- MAIN APP ----------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "Alphabet Learning"
    if "color_game" not in st.session_state:
        reset_game_state()

    # Set background image here
    set_background_image("assets/images/background.jpg")  # Provide the correct path to your image

    with st.sidebar:
        st.title("🎮 Learning Fun")
        activity = st.radio(
            "Choose Game",
            ["Alphabet Learning", "Picture Match", "Color Finder"],
            index=["Alphabet Learning", "Picture Match", "Color Finder"].index(st.session_state.page)
        )
        st.session_state.page = activity

        st.markdown("---")
        if st.button("🔄 Reset All Games"):
            reset_game_state()
        st.caption("Made with ❤️ for little learners")

    try:
        if st.session_state.page == "Alphabet Learning":
            letter_learning_page()
        elif st.session_state.page == "Picture Match":
            image_matching_game()
        elif st.session_state.page == "Color Finder":
            color_recognition_game()
    except Exception:
        st.error("Oops! Something went wrong.")
        if st.button("Click to restart"):
            reset_game_state()
            st.rerun()

if __name__ == "__main__":
    main()
