import pandas as pd
import os
import json
import traceback
from langchain_openai import ChatOpenAI
#from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2
from dotenv import load_dotenv
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_chain
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data

with open('D:\GenAI\Projects\mcqgen\Response.json','r') as file:
    response_json=json.load(file)


st.title("MCQ Creator Application with LangChain")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a PDF or Text File")

    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=5)

    subject=st.text_input("Insert Subject", max_chars=25)

    tone=st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response=generate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone": tone,
                            "response_json": json.dumps(response_json)
                        }
                        )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            print(f"Total Tokens:{cb.total_tokens}")
            print(f"Prompt Tokens:{cb.prompt_tokens}")
            print(f"Completion Tokens:{cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")

            if isinstance(response, dict):
                quiz=response.get("quiz",None)
                if quiz is not None:
                    table_data=get_table_data(quiz)
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        df.index=df.index+1
                        st.table(df)
                        
                        st.text_area(label="Review",value=response["review"])
                    else:
                        st.eror("Error in the table data")

            else:
                st.write(response)