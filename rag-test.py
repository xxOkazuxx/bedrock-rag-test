import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import BedrockChat
from langchain_community.retrievers.bedrock import AmazonKnowledgeBasesRetriever


retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id = 'xxxxxxxxxx',
    retrieval_config = {"vectorSearchConfiguration": {"numberOfResults": 10}}
)

prompt = ChatPromptTemplate.from_template("以下のcontextに基づいて回答してください。: {context} / 質問: {question}")

model = BedrockChat(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", model_kwargs={"max_tokens": 1000})

chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | model | StrOutputParser())

st.title("Bedrock Rag Test")
question = st.text_input("質問を入力")
button = st.button("質問する")

if button:
  st.write(chain.invoke(question))