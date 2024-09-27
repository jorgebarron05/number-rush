import streamlit as st
import random
import time

# Customization options
st.set_page_config(page_title="Math Practice Game", layout="centered")

# Apply custom CSS styles
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fb;
        padding: 20px;
    }
    .main-title {
        text-align: center;
        color: #2C3E50;
    }
    .number-box {
        display: inline-block;
        margin: 10px;
        padding: 20px;
        background-color: #ECF0F1;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        color: #2980B9;
        width: 100px;
        text-align: center;
    }
    .stSidebar {
        background-color: #D9E3F0;
    }
    .correct-answer {
        color: green;
        font-size: 24px;
        font-weight: bold;
    }
    .wrong-answer {
        color: red;
        font-size: 24px;
        font-weight: bold;
    }
    .play-again-button {
        background-color: #3498DB;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px 20px;
    }
    .submit-button {
        background-color: #2ECC71;
        color: white;
        font-size: 16px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Game states
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None
if 'countdown' not in st.session_state:
    st.session_state['countdown'] = 3
if 'user_submitted' not in st.session_state:
    st.session_state['user_submitted'] = False

# Game setup variables
st.sidebar.header("Customize your game:")
num_count = st.sidebar.slider("How many numbers to add?", 2, 10, 5)
num_digits = st.sidebar.slider("Max number of digits per number?", 1, 6, 2)
time_limit = st.sidebar.slider("Time limit (seconds)", 5, 60, 20)

st.sidebar.write("Adjust difficulty by changing the number of numbers, digit length, and time limit.")

# Generate random numbers
if not st.session_state['game_started']:
    numbers = [random.randint(10**(num_digits-1), 10**num_digits - 1) for _ in range(num_count)]
    st.session_state['numbers'] = numbers
    st.session_state['correct_answer'] = sum(numbers)

# Show title
st.markdown("<h1 class='main-title'>🧮 Math Addition Game</h1>", unsafe_allow_html=True)
st.write("Practice your math addition skills by solving problems within the time limit!")

# Countdown Before the Game
if not st.session_state['game_started']:
    if st.session_state['countdown'] > 0:
        st.subheader(f"Game starts in {st.session_state['countdown']} seconds...")
        time.sleep(1)
        st.session_state['countdown'] -= 1
        # No need for st.experimental_rerun(), Streamlit reruns automatically
    else:
        st.session_state['game_started'] = True
        st.session_state['start_time'] = time.time()

# Game starts
if st.session_state['game_started']:
    # Display the numbers
    st.subheader("Add the following numbers:")
    cols = st.columns(num_count)
    for i, num in enumerate(st.session_state['numbers']):
        cols[i].markdown(f"<div class='number-box'>{num}</div>", unsafe_allow_html=True)

    # Timer and progress bar
    remaining_time = time_limit - (time.time() - st.session_state['start_time'])

    if remaining_time > 0:
        st.subheader(f"⏳ Time remaining: {int(remaining_time)} seconds")
        st.progress(remaining_time / time_limit)
    else:
        st.subheader("⏰ Time's up!")
        st.session_state['game_started'] = False
        st.session_state['countdown'] = 3  # Reset countdown for next round

    # Get user's answer
    user_answer = st.text_input("Enter your answer:", key="user_input")

    # Check answer
    if st.button("Submit", key="submit_button") and not st.session_state['user_submitted']:
        st.session_state['user_submitted'] = True
        if remaining_time > 0:
            if user_answer.isdigit() and int(user_answer) == st.session_state['correct_answer']:
                st.markdown(f"<p class='correct-answer'>✅ Correct! The sum is {st.session_state['correct_answer']}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='wrong-answer'>❌ Wrong! The correct answer was {st.session_state['correct_answer']}</p>", unsafe_allow_html=True)
        else:
            st.error("⏱️ Time is up! Try again.")
        st.session_state['start_time'] = time.time()  # Reset timer after submission

# Option to play again
if st.button("Play Again", key="play_again_button"):
    st.session_state['game_started'] = False
    st.session_state['countdown'] = 3  # Reset countdown
    st.session_state['user_submitted'] = False
    # No need for st.experimental_rerun(), Streamlit reruns automatically
