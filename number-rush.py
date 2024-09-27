import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(page_title="Math Practice Game", layout="centered")

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None
if 'countdown' not in st.session_state:
    st.session_state['countdown'] = 3
if 'user_submitted' not in st.session_state:
    st.session_state['user_submitted'] = False
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'rounds' not in st.session_state:
    st.session_state['rounds'] = 0
if 'answer_checked' not in st.session_state:
    st.session_state['answer_checked'] = False
if 'user_answer' not in st.session_state:
    st.session_state['user_answer'] = ''

# Sidebar: Game customization
st.sidebar.header("Customize your game:")
num_count = st.sidebar.slider("How many numbers to add?", 2, 10, 5)
num_digits = st.sidebar.slider("Max number of digits per number?", 1, 6, 2)
time_limit = st.sidebar.slider("Time limit (seconds)", 5, 60, 20)

# Generate new numbers at the start of a round
def generate_numbers():
    numbers = [random.randint(10**(num_digits-1), 10**num_digits - 1) for _ in range(num_count)]
    st.session_state['numbers'] = numbers
    st.session_state['correct_answer'] = sum(numbers)
    st.session_state['user_answer'] = ''
    st.session_state['answer_checked'] = False

# Reset game state for a new round
def reset_game():
    st.session_state['game_started'] = False
    st.session_state['countdown'] = 3
    st.session_state['start_time'] = None
    generate_numbers()

# Main Game UI
st.title("🧮 Math Addition Game")
st.write("Try to add up the numbers before time runs out!")

# Score display
st.write(f"**Score:** {st.session_state['score']} | **Rounds Played:** {st.session_state['rounds']}")

# Start Countdown
if not st.session_state['game_started']:
    if st.session_state['countdown'] > 0:
        st.subheader(f"Game starts in {st.session_state['countdown']} seconds...")
        time_now = time.time()
        if st.session_state['start_time'] is None:
            st.session_state['start_time'] = time_now
        elif time_now - st.session_state['start_time'] >= 1:
            st.session_state['countdown'] -= 1
            st.session_state['start_time'] = time_now
    else:
        st.session_state['game_started'] = True
        st.session_state['start_time'] = time.time()
        generate_numbers()

# During the game
if st.session_state['game_started']:
    # Display numbers to add
    st.subheader("Add the following numbers:")
    cols = st.columns(num_count)
    for i, num in enumerate(st.session_state['numbers']):
        cols[i].write(f"**{num}**")
    
    # Timer
    remaining_time = time_limit - (time.time() - st.session_state['start_time'])
    
    if remaining_time > 0:
        st.subheader(f"⏳ Time remaining: {int(remaining_time)} seconds")
        st.progress(remaining_time / time_limit)
        
        # Get user's answer
        st.session_state['user_answer'] = st.text_input("Enter your answer:", value=st.session_state['user_answer'], key="user_input")
        
        # Submit button
        if st.button("Submit") and not st.session_state['answer_checked']:
            if st.session_state['user_answer'].isdigit():
                if int(st.session_state['user_answer']) == st.session_state['correct_answer']:
                    st.success(f"✅ Correct! The sum is {st.session_state['correct_answer']}.")
                    st.session_state['score'] += 1
                else:
                    st.error(f"❌ Wrong! The correct answer was {st.session_state['correct_answer']}.")
            else:
                st.error("❌ Invalid input! Please enter a number.")
            
            st.session_state['answer_checked'] = True
            st.session_state['rounds'] += 1
    else:
        st.error("⏰ Time's up!")
        st.session_state['rounds'] += 1
        st.session_state['answer_checked'] = True

# Play Again button
if st.session_state['answer_checked']:
    if st.button("Play Again"):
        reset_game()
