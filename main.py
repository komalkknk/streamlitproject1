import streamlit as st
import langchain_helper

st.title("Question Answer Generator")

form = st.form(key='my-form')
question = form.text_input('Enter your question')
submit = form.form_submit_button('Submit')

if submit:
    response = langchain_helper.generate_answer_by_question(question)
    st.header("Answer")
    st.write(response)
