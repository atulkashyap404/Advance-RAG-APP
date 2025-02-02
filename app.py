import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_objectbox.vectorstores import ObjectBox
from langchain_community.document_loaders import PyPDFDirectoryLoader

## Loading the enviroment variables like all API's
from dotenv import load_dotenv
load_dotenv()


## Load the Groq And OpenAI API's Key
os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
groq_api_key=os.getenv('GROQ_API_KEY')


## web Application Heading
st.title("Your Physics Teacher- 👴🏻")


## Calling the LLm model from groq site

llm=ChatGroq(groq_api_key=groq_api_key,
             model="llama-3.1-70b-versatile")



## Creating the prompt for llm model

prompt=ChatPromptTemplate.from_template(
    """
    "Query the provided document to extract detailed and accurate information regarding specific topic or question. Ensure that the results include relevant excerpts from the document and highlight key points. Provide a comprehensive response that captures all pertinent details and context related to the query."
    <context>
    {context}
    <context>
    Questions:{input}
    """
)

## Vector Embedding and Object VectorStore DB

def vector_embedding():
    
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.loader=PyPDFDirectoryLoader("./data")  ## Data Ingestion
        st.session_state.docs=st.session_state.loader.load() ## Documents Loading
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        st.session_state.final_documents=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors=ObjectBox.from_documents(st.session_state.final_documents,st.session_state.embeddings,embedding_dimensions=768)
        
        
        
        
## Defining my input prompt
input_prompt=st.text_input("Enter Your Question")

if st.button("Activate Your Physics Teacher"):
    vector_embedding()
    st.write("Done- Hi, I am Your Personal Physics Teacher")
    
import time


if input_prompt:
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    start=time.process_time()
    
    response=retrieval_chain.invoke({'input':input_prompt})
    st.write("response time",start)
    st.write(response['answer'])
    


