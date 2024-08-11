
from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableConfig


from graph.llm import llm
from graph.state import InterviewState

class QuizAnswers(BaseModel):
    answer: str = Field(
        description="A possible answer to a given question. This is a string that represents one of the multiple choices available for the question."
    )
    correctness: bool = Field(
        description="Indicates whether the given answer is correct or not. This is a boolean value where True represents a correct answer and False represents an incorrect answer."
    )

class QuizQuestion(BaseModel):
    question: str = Field(
        description="The text of the question being asked. This is a string that contains the content of the question posed to the quiz taker."
    )
    answers: List[QuizAnswers] = Field(
        description="A list of possible answers to the question. Each item in the list is an instance of the QuizAnswers class, providing both the answer text and its correctness. Only one answer should be correct"
    )
    cited_urls: List[str] = Field(
        description="List of urls cited in the answer.",
    )

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(
        description="A list of questions included in the quiz. Each item in the list is an instance of the QuizQuestion class, containing the question text and its possible answers."
    )
    length: int = Field(
        description="The number of questions included in the quiz. This is an integer representing the total count of questions.",
        default=2
    )


direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific.",
        ),
        ("user", "{topic}"),
    ]
)

gen_quiz_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert quiz writer. write a quiz to the given article.\
You are asked to create a quiz in one of the following levels: [easy, medium, hard].\
The quiz should be as diverse as possible and hsould not repeat questions.\
If the chosen level is easy, the questions should be everyone knowledge and very broad.
here is an example for question in every level if the topic was "FIFA World Cup 2022":
easy - Who won the FIFA World Cup 2022?
medium - Who was the top scorer at FIFA World Cup 2022?
Hard - how many goals did the top scorer scored at FIFA World Cup 2022?
When you have no more questions to ask, say "Goodluck with the quiz!" to end the conversation.
The quiz is about the following article:
{article}
            """,
        ),
        ("user", "Please create a quiz for me in the following level: {level} of length {length}")
    ]
)

gen_quiz_chain = gen_quiz_prompt | llm.with_structured_output(Quiz, include_raw=True)

def gen_quiz(
    state: InterviewState,
    config: Optional[RunnableConfig] = None,
    max_str_len: int = 15000,
):
    context = "\n\n".join([msg.content for msg in state["messages"]])
    quiz = gen_quiz_chain.invoke({"article": context, "level": "easy", "length": 2})
    return {"messages": [quiz], "references": state["references"]}
    


if __name__ == "__main__":
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
    from graph.perspective import survey_subjects
    from graph.dialog import generate_question
    from graph.answer import gen_answer

    example_topic = "Impact of million-plus token context window language models on RAG"
    perspectives = survey_subjects.invoke(example_topic)
    messages = [
        HumanMessage(f"So you said you were writing an article on {example_topic}?")
    ]
    question = generate_question.invoke(
        {
            "editor": perspectives.editors[0],
            "messages": messages,
        }
    )

    example_answer = gen_answer(
        {"messages": [HumanMessage(content=question["messages"][0].content)]}
    )

    quiz = gen_quiz_chain.invoke({"article": example_answer, "level": "easy", "length": 10})
    print(quiz)