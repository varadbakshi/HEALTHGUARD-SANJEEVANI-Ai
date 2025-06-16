import streamlit as st

# Title of the login page
st.title('-User Authentication for Disease Prediction-')

# Prompt the user to enter their username
username = st.text_input('Username')

# Prompt the user to enter their password
password = st.text_input('Password', type='password')

# Create a login button
login_button = st.button('Login')

if login_button:
    # Redirect the user to the main page
    st.success('Login successful!')
    st.balloons()
else:
    st.warning("Please Enter Your Credentials!")
