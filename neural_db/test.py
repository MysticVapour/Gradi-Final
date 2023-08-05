from thirdai import licensing, neural_db as ndb
import os
from pathlib import Path
import nltk
import streamlit as st
import openai
import pandas as pd
import cv2
import numpy as np
import easyocr
from PIL import Image
import PyPDF2

from model_bazaar import Bazaar
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

#Setup
licensing.deactivate()
licensing.activate(st.secrets["thirdai_license_key"])
openai.api_key = st.secrets["openai_api_key"]
st.set_page_config(page_title="Gradi", layout="wide")
reader = easyocr.Reader(['en'],gpu = True)

db = ndb.NeuralDB(user_id="adgoch11")

# Set up a cache directory
if not os.path.isdir("bazaar_cache"):
    os.mkdir("bazaar_cache")

# Fetch the model bazaar and load the db
bazaar = Bazaar(cache_dir=Path("bazaar_cache"))
bazaar.fetch()
db = bazaar.get_model("General QnA")
nltk.download('punkt')

#Setup helper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def fill():
    sample_answers = [
        "French Revolution:  All the people of France were scared. People did not like bastille or the king.", 
        
        "The struggle to survive: The increase in population led to a rapid increase in the requirement for food grains. Production of grains could not keep pace with the demand, due to which the price of bread rose rapidly. Due to the low wages paid to the labourers, the gap between the poor and the rich widened. Things became worse whenever drought or hail reduced the harvest.", 
        
        "A directory rules France: The collapse of the Jacobin government enabled the wealthier middle classes to take control. The revised constitution excluded non-propertied segments of society from voting rights. It established two elected legislative councils. To govern the nation, a Directory was formed, comprising five executive members appointed by the government. The prevailing political instability set the stage for the rise of a military dictator, Napoleon Bonaparte.", 
        
        "The rise of Napoleon: Napoleon Bonaparte was born in 1769 in Corsica. He joined the army at the age of 16. He was a brilliant military leader. He became the Emperor of France in 1804. He conquered many European countries. He was defeated in the Battle of Waterloo in 1815. He was exiled to the island of St. Helena, where he died in 1821."
    ]
    return sample_answers



with st.container():
    st.title("Gradi.ai: Redefining Academic Assessment with AI")
    st.subheader("Automate the grading process, accelerate academic assessments, and elevate educational outcomes with the power of Gradi.ai !")
st.divider()

col1, col2 =  st.columns(2, gap="large")
with col1:
    with st.container():
        st.header("Student Portal")
        studentFile = st.file_uploader("Upload Student Answer Sheet (.png) [Limited Functionality]", type=["png"], accept_multiple_files=False)

        sample_answers = []
        if studentFile != None:
            original_image = Image.open(studentFile)
            readFile = np.array(original_image)
            st.image(readFile, caption="Uploaded Image")

            gray = cv2.cvtColor(readFile, cv2.COLOR_BGR2GRAY)
            sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
            thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            r_easy_ocr=reader.readtext(thresh,detail=0)

            text = ""
            for i in r_easy_ocr:
                text += i + " "
            cleanedText = get_completion(f"""The text delimited by backticks has some errors, make it grammatically and punctually correct and also make it make sense. Do not overdo the changes, stay as original as possible. 
            ```{text}```
            """)
            st.code(cleanedText)
            sample_answers.append(cleanedText)
        else:
            if st.button("Prefill sample answers"):
                sample_answers = fill()
                text_contents = '''
                Question paper:

                Q1: How did the French Revolution begin?
                Q2: Explain how the people of France struggled to survive during the late 1700s.
                Q3: Write a short note about the directory that ruled France.
                Q4: Explain the rise of Napoleon Bonaparte in France.

                Teacher inputted Keywords:

                1: state of alarm, rumours of open fire, Bastille, hated the bastille, despotic power of the king, high price of bread, execution of the king
                2: Increase in population, rapid increase in the requirement for food grains, Production of grains could not keep pace with the demand, price of bread rose rapidly, low wages paid to the labourers, gap between the poor and the rich widened, drought or hail reduced the harvest
                3: Fall of the Jacobin government, wealthier middle classes to seize power, non-propertied sections of society were denied voting, two elected legislative councils, government appointed a Directory consisting of executives made up of five members, political instability, military dictator, Napoleon Bonaparte
                4: born in 1769, joined the army at the age of 16, brilliant military leader, Emperor of France in 1804, defeated in the Battle of Waterloo in 1815, exiled to the island of St. Helena
                '''
                st.download_button("Download Sample Answer Script (For Teacher Portal)", data=text_contents, file_name="answers.txt", mime="text/plain")

            for i in range(len(sample_answers)):
                st.subheader(f"Student Answer {i+1}:")
                st.code(sample_answers[i])
with col2:
    with st.container():
        st.header("Teacher Portal")
        keys = []
        marking_scheme = []
        totalPossibleMarks = 0
        uploadedFile = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=False)

        #Context Retrieval System [Teacher Portal]
        outputs = []
        insertable_docs = []
        if uploadedFile != None:
            save_folder = "D:\\Users\\Advay\\Desktop\\Work-Related\\Demos\\neural_db"
            save_path = Path(save_folder, uploadedFile.name)
            with open(save_path, mode='wb') as w:
                w.write(uploadedFile.getvalue())
            pdf_files = [uploadedFile]
        else:
            pdf_files = ['FrenchRev.pdf']

        for file in pdf_files:
            pdf_doc = ndb.PDF(file)
            insertable_docs.append(pdf_doc)

        source_ids = db.insert(insertable_docs, train=True)

        context = "Emergence of social groups"

        search_results = db.search(
            query=context,
            top_k=3,
            on_error=lambda error_msg: print(f"Error! {error_msg}"))
        
        st.subheader(context)

        for result in search_results:
            st.markdown(result.text)
            outputs.append(result.text)
            # print(result.context(radius=1))
            # print(result.source)
            # print(result.metadata)
            print('************')

        # for i in range(len(sample_answers)):
        #     #keys.append(st.text_input(f"""Answer {i+1}:"""))
        #     marking_scheme.append(st.number_input(f"""Marks for Answer {i+1}:""", min_value=1.0, max_value=8.0, step=0.5))
        #     if keys[i] != '' and keys[i] != None:
        #         totalPossibleMarks += marking_scheme[i]
st.divider()

with st.container():
    if sample_answers != []:
        prompt = f"""
            You are an AI Grading assistant, you will receive a student answer delimited by triple backticks and also the correct answer delimited by triple hashs. The evaluation should be heavily based on the correct answer. If the student's answer contains irrelevant context or lacks the vital keywords found in the correct answer, substantial marks should be deducted. Please adhere to the following guidelines:
            - Ignore all differences in phrasing, word order, punctuation, and grammar between the answers. They should have no impact on the score.
            - If the student's answer is mostly similar to the correct answer, containing all relevant keywords and context, assign a score of 0.9 or 1.
            - If the student's answer contains some of the correct keywords but includes irrelevant context or misses some important keywords, deduct marks substantially.
            - If there's almost no similarity in the context of the answers or if the student's answer is entirely irrelevant, assign a score of 0.
            Output just the score. Explain why you gave the score in the text box below. Also, suggest the topics the student should revise to improve their score.
            ```{sample_answers[0]}```
            ###{outputs[0]}###"""
        marks = get_completion(prompt)
        st.header(marks)
    