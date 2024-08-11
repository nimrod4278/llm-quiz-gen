
# LLM-Powered Quiz Question Generator

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [LLM-Selection](#llm-selection)
- [Prompting-Techniques](#prompting-techniques)
- [Ideas](#ideas)

## Introduction

This project aims to develop a simple web-based tool that generates quiz questions on a general knowledge topic using a large language model (LLM) and advanced prompt engineering techniques.

The project was inspired from the STOM Web Research agent implementation of Langgraph docs:
https://langchain-ai.github.io/langgraph/tutorials/storm/storm

You can find more guidance about it in the following YouTube video here:
https://youtu.be/1uUORSZwTz4?si=XnFLRTlsUfZJkI45

## Getting Started

### Prerequisites

-   Install [Python 3.10](https://www.python.org/downloads/)
-   Additional dependencies listed in `requirements.txt`

### Installation

To install and set up this project, follow these steps:

1. Clone the repository:

   `git clone https://github.com/yourusername/project-name.git`
	
2.   Navigate to the project directory:
 
	`cd project-name`

3. create a virtual environment:

	`python3 -m venv venv`

4. Activate the virtual environment:

	`source venv/bin/activate`
    
5.  Install the required packages:
    
	`pip install -r requirements.txt`

### Usage
1. Insert your OpenAI API key to .env file

2. Start the app:
	`streamlit run app.py`

3. Open browser on http://localhost:8501/

## Features
1. Generate Quiz - Generates a quiz according to the topic given and level
2. Validate Quiz (Bonus) - See if you can answer the quiz correctly
3. Learn more (Bonus) - Refer to a knowledge article about the question asked

## LLM-Selection

### Open-source Vs. Proprietary

Since no limitations were presented as part of the assignment I chose to use
proprietary model for the ease of use and stability

### OpenAI Vs. Antropic

Since both companies models could be suitable for the assignment I chose OpenAI models since
I had more experience working with their earlier, cheaper and lightweight models.

The project structure is made such it is very easy to change models and requires changing only the `graph/llm.py` file.

### Model chosen

I chose to use **gpt-3.5-turbo** since it is cheaper and faster than OpenAI latest models and no multi-modality functionality is required

## Prompting-Techniques

### Few-shot
Providing prompt with examples to give guidance to the model on the desired output

### Role-playing

Created few "personas" each with its own role and task to create a diverse and an enriched process for the creation of the quiz.

Some of the personas examples are:

1. Quiz writer
2. Wiki writer
3. Editor

### Structured-output

I have used Langchain Pydantic classes to ensure the structure of the model outputs.
This helps with parsing of the model response and automation of the process


## Ideas

To enhance the tool the tool capabilities and performance I suggest the following steps:

1. Choosing stronger model for better results
2. Further implementing according to the STORM paper and the refine outline steps:
	https://langchain-ai.github.io/langgraph/tutorials/storm/storm/#refine-outline
3. Using `async` calls for better performance
4. Using a mix of different models for diversity in answer and knowledge
5. loading animation for better UX