import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(page_title="Quick Math Game", layout="centered")

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'rounds' not in st.session_state:
    st.session_state['rounds'] = 0

# Sidebar for game settings
st.sidebar.header("Game Settings")
time_limit = st.sidebar.slider("Time limit (seconds)", 5, 30, 10)

# Function to start a new round
def start_round():
    st.session_state['numbers'] = [random.randint(10, 99) for _ in range(2)]
    st.session_state['correct_answer'] = sum(st.session_state['numbers'])
    st.session_state['game_started'] = True
    st.session_state['start_time'] = time.time()
    st.session_state['user_answer'] = ''
    st.session_state['feedback'] = ''

# Main Game UI
st.title("🧠 Quick Math Game")
st.write(f"Score: {st.session_state['score']} | Rounds Played: {st.session_state['rounds']}")

# Start the game
if not st.session_state['game_started']:
    if st.button("Start Game"):
        start_round()

# Display the game while it's running
if st.session_state['game_started']:
    time_left = time_limit - (time.time() - st.session_state['start_time'])
    
    if time_left > 0:
        st.subheader(f"Time left: {int(time_left)} seconds")
        st.write(f"**Add these numbers:** {st.session_state['numbers'][0]} + {st.session_state['numbers'][1]}")
        
        st.session_state['user_answer'] = st.text_input("Your answer:", value=st.session_state['user_answer'], key="answer_input")
        
        if st.button("Submit Answer"):
            if st.session_state['user_answer'].isdigit():
                user_answer = int(st.session_state['user_answer'])
                if user_answer == st.session_state['correct_answer']:
                    st.session_state['feedback'] = "✅ Correct!"
                    st.session_state['score'] += 1
                else:
                    st.session_state['feedback'] = f"❌ Wrong! Correct answer: {st.session_state['correct_answer']}"
            else:
                st.session_state['feedback'] = "Please enter a valid number."
            
            st.session_state['game_started'] = False
            st.session_state['rounds'] += 1
    else:
        st.error("⏰ Time's up!")
        st.write(f"The correct answer was {st.session_state['correct_answer']}")
        st.session_state['game_started'] = False
        st.session_state['rounds'] += 1

# Feedback and Play Again
if 'feedback' in st.session_state and st.session_state['feedback']:
    st.write(st.session_state['feedback'])

if not st.session_state['game_started']:
    if st.button("Play Again"):
        start_round()
