import streamlit as st

from langchain_core.messages import AIMessage

from graph.main import interview_graph
from graph.perspective import survey_subjects
from graph.quiz import Quiz, QuizAnswers, QuizQuestion

if "submit" not in st.session_state:
    st.session_state.submit = False
if "quiz" not in st.session_state:
    st.session_state.quiz = {}
if "validate" not in st.session_state:
    st.session_state.validate = False


def validate_quiz():
    st.session_state.validate = True

st.title("Quiz Generator")

with st.form(key="quiz_form"):
    topic = st.text_input("Enter the topic for the quiz:")
    level = st.selectbox("Select the difficulty level:", ["Easy", "Medium", "Hard"])
    submit_button = st.form_submit_button(label="Generate Quiz")

    if submit_button:
        st.session_state.submit = True
        st.session_state.quiz = {}

if st.session_state.submit:
    with st.form(key="generated_form"):
        st.write(f"Topic: {topic}")
        st.write(f"Difficulty Level: {level}")

        if not st.session_state.quiz:
            perspectives = survey_subjects.invoke(topic)
            initial_state = [
                {
                    "editor": editor, #perspectives.editors[0],
                    "messages": [
                        AIMessage(
                            content=f"So you said you were writing an article on {topic}?",
                            name="Subject_Matter_Expert",
                        )
                    ]
                }
                for editor in perspectives.editors
            ]

            generated_quiz = interview_graph.batch(initial_state)
            quiz = []
            for editor in generated_quiz:
                editor_questions = editor['messages'][-1]['parsed'].questions
                quiz += editor_questions
            st.session_state.quiz = quiz

        for q in st.session_state.quiz:
            st.write(q.question)
            options = [option.answer for option in q.answers]
            user_answer = st.radio("options", options=options, key=q.question)
            if st.session_state.validate:
                if user_answer == options[0]:
                    st.success("Correct!")
                else:
                    st.error("Wrong!")
            with st.expander("Learn more"):
                for url in q.cited_urls:
                    st.write(f"[{url}]({url})")
        validate = st.form_submit_button("Submit", on_click=validate_quiz)
