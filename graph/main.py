from langchain_core.messages import AIMessage
from langgraph.graph import END, StateGraph, START

from graph.state import InterviewState
from graph.dialog import generate_question
from graph.answer import gen_answer
from graph.quiz import gen_quiz

max_num_turns = 5

def route_messages(state: InterviewState, name: str = "Subject_Matter_Expert"):
    messages = state["messages"]
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )
    if num_responses >= max_num_turns:
        return "gen_quiz"
    last_question = messages[-2]
    if last_question.content.endswith("Thank you so much for your help!"):
        return "gen_quiz"

    return "ask_question"


builder = StateGraph(InterviewState)

builder.add_node("ask_question", generate_question)
builder.add_node("answer_question", gen_answer)
builder.add_node("gen_quiz", gen_quiz)

builder.add_conditional_edges("answer_question", route_messages)
builder.add_edge("ask_question", "answer_question")

builder.add_edge(START, "ask_question")
builder.add_edge("gen_quiz", END)
interview_graph = builder.compile().with_config(run_name="Conduct Interviews")


if __name__ == "__main__":
    from graph.perspective import survey_subjects
    example_topic = "how to make the perfect nopolian pizza?"
    perspectives = survey_subjects.invoke(example_topic)
    initial_state = [
        {
            "editor": editor,
            "messages": [
                AIMessage(
                    content=f"So you said you were writing an article on {example_topic}?",
                    name="Subject_Matter_Expert",
                )
            ]
        }
        for editor in perspectives.editors
    ]

    quiz = interview_graph.batch(initial_state)
    print(quiz)