# ---------- WORD MATCHING GAME IMPROVED ----------
elif st.session_state.page == "Word Matching Game":
    st.title("Match the Word with the Image")
    
    # Progress bar
    progress = (st.session_state.quiz_index + 1) / len(letters)
    st.progress(progress)
    st.caption(f"Question {st.session_state.quiz_index + 1} of {len(letters)}")

    letter = st.session_state.quiz_order[st.session_state.quiz_index]
    correct_word = words[letter]

    # Display letter and image in columns
    col1, col2 = st.columns(2)
    with col1:
        try:
            st.image(os.path.join(image_path, f"{letter}.png"), 
                    width=200, 
                    alt=f"Letter {letter.upper()}")
        except FileNotFoundError:
            st.error("Image not found!")
    
    with col2:
        st.markdown(f"## Letter: {letter.upper()}")
        if st.button("🔊 Play Sound"):
            audio_file = os.path.join(audio_path, f"{letter}.mp3")
            st.audio(audio_file, autoplay=True)

    # Generate options
    if not st.session_state.options:
        other_words = [w for w in words.values() if w != correct_word]
        st.session_state.options = random.sample(other_words, 2) + [correct_word]
        random.shuffle(st.session_state.options)

    # Display options as buttons for better touch support
    selected = None
    for option in st.session_state.options:
        if st.button(option.capitalize(), key=option):
            selected = option
            st.session_state.selected_option = option

    if st.session_state.submitted:
        if st.session_state.selected_option == correct_word:
            st.balloons()
            st.success("✅ Correct! Great job!")
        else:
            st.error(f"❌ Oops! The correct answer was: {correct_word.capitalize()}")
        
        # Show correct image
        st.image(os.path.join(image_path, f"{correct_word}.png"), 
                caption=correct_word.capitalize(),
                width=200)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit") and not st.session_state.submitted and selected:
            st.session_state.submitted = True
            st.experimental_rerun()
    
    with col2:
        if st.session_state.submitted:
            if st.button("Next ➡️"):
                st.session_state.quiz_index += 1
                if st.session_state.quiz_index >= len(letters):
                    st.balloons()
                    st.success("🎉 You finished the game!")
                    if st.button("Play Again"):
                        st.session_state.quiz_index = 0
                st.session_state.submitted = False
                st.session_state.selected_option = None
                st.session_state.options = []
                st.experimental_rerun()
