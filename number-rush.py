import streamlit as st
import random
import time

# Customization options
st.set_page_config(page_title="Math Practice Game", layout="centered")

# Game settings
st.title("🧮 Math Addition Game")
st.write("Practice your math addition skills!")

st.sidebar.header("Customize your game:")
num_count = st.sidebar.slider("How many numbers to add?", 2, 10, 5)
num_digits = st.sidebar.slider("Max number of digits per number?", 1, 6, 2)
time_limit = st.sidebar.slider("Time limit (seconds)", 5, 60, 20)

st.sidebar.write("Adjust difficulty by changing the number of numbers, digit length, and time limit.")

# Generate random numbers
numbers = [random.randint(10**(num_digits-1), 10**num_digits - 1) for _ in range(num_count)]
correct_answer = sum(numbers)

# Display numbers to add
st.subheader("Add the following numbers:")
for i, num in enumerate(numbers, 1):
    st.write(f"{i}. {num}")

# Start the timer
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

remaining_time = time_limit - (time.time() - st.session_state['start_time'])

if remaining_time > 0:
    st.subheader(f"Time remaining: {int(remaining_time)} seconds")
else:
    st.subheader("Time's up!")
    st.session_state['start_time'] = time.time()  # Reset timer for next round

# Get user's answer
user_answer = st.text_input("Enter your answer:")

# Check answer
if st.button("Submit"):
    if remaining_time > 0:
        if user_answer.isdigit() and int(user_answer) == correct_answer:
            st.success(f"✅ Correct! The sum is {correct_answer}")
        else:
            st.error(f"❌ Wrong! The correct answer was {correct_answer}")
    else:
        st.error("⏱️ Time is up! Try again.")
    st.session_state['start_time'] = time.time()  # Reset timer after submission

# Option to play again
if st.button("Play Again"):
    st.experimental_rerun()

# Custom styling for the app
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fb;
    }
    .stSidebar {
        background-color: #d9e3f0;
    }
    </style>
    """, unsafe_allow_html=True)
