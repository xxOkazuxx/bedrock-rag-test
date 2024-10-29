"""
Amazon Bedrock Knowledge BasesとClaude 3.5を使用したRAGアプリケーション

このスクリプトは、Amazon Bedrock Knowledge Basesを使用して文書検索を行い、
Claude 3.5を使用して質問応答を行うStreamlitアプリケーションです。

Requirements:
    - streamlit
    - langchain
    - boto3
"""

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

# プロンプトテンプレートの改善
prompt = ChatPromptTemplate.from_template("""
以下のcontextに基づいて回答してください。

Context:
{context}

質問:
{question}

回答は日本語で、簡潔かつ分かりやすく説明してください。
""")

model = BedrockChat(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0", model_kwargs={"max_tokens": 1000})

chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | model | StrOutputParser())

st.title("Bedrock RAG デモ")
st.caption("Amazon Bedrock Knowledge BasesとClaude 3.5を使用したQ&Aシステム")

# デバッグモードの追加
debug_mode = st.sidebar.checkbox("デバッグモードを有効化", False)

question = st.text_input("質問を入力してください")
button = st.button("質問する")

if button and question:
    try:
        with st.spinner("回答を生成中..."):
            response = chain.invoke(question)
            
            # 回答の表示
            st.write("### 回答")
            st.write(response)
            
            # デバッグ情報の表示
            if debug_mode:
                st.write("### 検索結果")
                retrieved_docs = retriever.get_relevant_documents(question)
                for i, doc in enumerate(retrieved_docs, 1):
                    st.write(f"**文書 {i}:**")
                    st.write(doc.page_content)
                    
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
elif button and not question:
    st.warning("質問を入力してください")
