# import transformers
import time
import json
import ollama
from file_retrieval import FileRetrieval
import re

import re


def parse_questions(text):
    questions_data = {}

    # Split the text by question blocks
    questions = re.split(r"Question \d+:", text.strip())

    for i, question_text in enumerate(questions[1:], start=1):
        question_info = {}

        # Extract question text until we reach "Options:" or a keyword marking options
        question_match = re.search(r"(.*?)(?=\nOptions:|\nAnswer:|\nExplanation:)", question_text, re.DOTALL)
        question = question_match.group(1).strip() if question_match else ""

        # Detect the type of options format to distinguish question types
        options_match = re.search(r"Options:\s*([A-E](?:\s*[,|\n]\s*[A-E])*)",
                                  question_text)  # Paragraph options format
        ynng_match = re.search(r"Options:\s*(YES|NO|NOT GIVEN)", question_text)  # Yes-No-Not-Given format
        mcq_options = re.findall(r"([A-D])\.\s*(.*?)\s*(?=[A-D]\.|Answer:|Explanation:|$)", question_text)  # MCQ format

        # Determine question type based on options found
        if options_match:
            # Paragraph-based question format (e.g., A, B, C, D, E)
            options = [opt.strip() for opt in options_match.group(1).split(',')]
            question_type = "paragraph-based"
            question_info["options"] = {opt: "" for opt in options}  # No specific text for paragraph options

        elif ynng_match:
            # Yes-No-Not-Given format
            options = ["YES", "NO", "NOT GIVEN"]
            question_type = "ynng"
            question_info["options"] = {opt: "" for opt in options}

        else:
            # Standard MCQ format with options text (A, B, C, D)
            question_type = "mcq"
            question_info["options"] = {opt: text for opt, text in mcq_options}

        # Extract correct answer and explanation
        correct_answer_match = re.search(r"Answer:\s*([A-E]|YES|NO|NOT GIVEN)", question_text)
        correct_answer = correct_answer_match.group(1) if correct_answer_match else "N/A"

        explanation_match = re.search(r"Explanation:\s*(.*?)(?:\n|$)", question_text, re.DOTALL)
        explanation = explanation_match.group(1).strip() if explanation_match else "Explanation not provided."

        # Build the dictionary for each question
        question_info.update({
            "question": question,
            "question_type": question_type,
            "correct_answer": correct_answer,
            "explanation": explanation
        })

        # Add parsed question data to the main dictionary
        questions_data[i] = question_info

    return questions_data


# Retrieve PDF content
file_retrieval = FileRetrieval()
pdf_files = file_retrieval.retrieve_pdf_files()
print(pdf_files)

if pdf_files:
    selected_file = pdf_files[3]  # Choose the first file or modify as needed
    content = file_retrieval.read_pdf_content(selected_file, paragraph_limit=6)
    pdf_content = "\n\n".join(content)  # Combine paragraphs for the LLM input
    print(pdf_content)

    # Generate questions using the extracted PDF content
    response = ollama.chat(model='test_model:latest', messages=[
      {
        'role': 'user',
        'content': f'''{pdf_content}
    
        Instruction: Based on the paragraphs above, generate 4 multiple-choice questions, 2 fill-in-the-blank questions and 2 yes-no-not-given questions, option can be optional.
        Please structure each question as follows:
        Question No:
        Question:
        Options:
        Correct answer:
        Explanation:
        '''
      },
    ])

    # Retrieve the response text
    response_text = response['message']['content']

    # Print the response content for verification
    print("Response content received:\n", response_text)

    # Parse and display the generated questions
    questions_data = parse_questions(response_text)

    # Display each question in a readable format
    for question_num, details in questions_data.items():
        print(f"Question {question_num}:")
        print(f"Question: {details['question']}")
        print(f"Type: {details['question_type']}")
        print("Options:")
        for option, text in details["options"].items():
            print(f"  {option}) {text}")
        print(f"Correct answer: {details['correct_answer']}")
        print(f"Explanation: {details['explanation']}\n")

