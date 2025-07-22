import streamlit as st
from time import sleep
import qdrant_client
from qdrant_client import models
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def initialize_models():
    embed_model = FastEmbedEmbedding(model_name="thenlper/gte-large")
    llm = Groq(model="deepseek-r1-distill-llama-70b")
    
    # Get credentials from environment variables
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in .env file")
    
    client = qdrant_client.QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )
    return embed_model, llm, client

message_templates = [
    ChatMessage(
    content="""
    Your name is Gitanjali, a divine assistant of the Bhagavad Gita.
    You are an enlightened guide who provides wisdom from the Bhagavad Gita in a clear, compassionate manner.
    
    Key Guidelines:
    1. Respond in the language of the question (English, Hindi, or Sanskrit)
    2. Always provide chapter and verse references for your answers
    3. Explain complex concepts in simple terms
    4. Maintain a spiritual yet practical tone
    5. If asked for opinions, clearly distinguish between scriptural teachings and personal advice
    
    Response Format:
    

<div class="think">[Analyze the question, identify relevant Gita teachings, and plan your response]</div>


    
    [Your response with proper formatting and verse references]
    """,
    role=MessageRole.SYSTEM
),
ChatMessage(
    content="""
    Context from the Bhagavad Gita:
    {context_str}
    
    Question: {query}
    
    Guidelines for response:
    1. If the question is about the Gita's teachings, provide a clear answer with relevant verses
    2. If the question is philosophical, relate it to Gita's wisdom
    3. If the context doesn't contain relevant information, say:
       "I don't have enough information from the Bhagavad Gita to answer this precisely. Would you like me to share general spiritual guidance on this topic?"
    4. For questions completely unrelated to spirituality or the Gita, politely guide the conversation back to spiritual topics
    """,
    role=MessageRole.USER
),
    
]

def search(query, client, embed_model, k=5):
    collection_name = "bhagavad-gita"
    query_embedding = embed_model.get_query_embedding(query)
    result = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=k
    )
    return result

def pipeline(query, embed_model, llm, client):
    # R - Retriever
    relevant_documents = search(query, client, embed_model)
    context = [doc.payload['context'] for doc in relevant_documents.points]
    context = "\n".join(context)

    # A - Augment
    chat_template = ChatPromptTemplate(message_templates=message_templates)

    # G - Generate
    response = llm.complete(
        chat_template.format(
            context_str=context,
            query=query)
    )
    return response

def extract_thinking_and_answer(response_text):
    """Extract thinking process and final answer from response"""
    try:
        thinking = response_text[response_text.find("<think>") + 7:response_text.find("</think>")].strip()
        answer = response_text[response_text.find("</think>") + 8:].strip()
        return thinking, answer
    except:
        return "", response_text

def main():
    # Set page config
    st.set_page_config(
        page_title="Gitanjali - Bhagavad Gita Guide",
        page_icon="🕉️",
        layout="wide"
    )
    
    # Custom CSS for spiritual theme
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: #f8f5f0;
            background-image: url('https://www.transparenttextures.com/patterns/rice-paper-3.png');
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(145deg, #4b6cb7 0%, #182848 100%);
            color: white;
            padding: 2rem 1rem;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(45deg, #4b6cb7, #182848);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Chat containers */
        .stChatFloatingInputContainer {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #4b6cb7;
            border-radius: 4px;
        }
        
        /* Thinking process box */
        .think {
            background-color: #f0f4ff;
            padding: 1rem;
            border-radius: 10px;
            border-right: 4px solid #4b6cb7;
            margin: 1rem 0;
            font-style: italic;
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main title with spiritual touch
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #2c3e50; font-family: 'Arial', sans-serif; font-weight: 700;">
            🕉️ Gitanjali - Bhagavad Gita Guide
        </h1>
        <p style="color: #7f8c8d; font-style: italic;">
            Wisdom from the Sacred Scriptures
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize models
    embed_model, llm, client = initialize_models()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar with clear chat button
    with st.sidebar:
        st.markdown("### 🏛️ Navigation")
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📜 About")
        st.markdown("""
        Ask any question about the Bhagavad Gita and receive enlightened guidance.
        """)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                thinking, answer = extract_thinking_and_answer(message["content"])
                with st.expander("Show thinking process"):
                    st.markdown(f'<div class="think">{thinking}</div>', unsafe_allow_html=True)
                st.markdown(answer)
            else:
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask Gitanjali about the Bhagavad Gita..."):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Reflecting on the Gita's wisdom..."):
                full_response = pipeline(prompt, embed_model, llm, client)
                thinking, answer = extract_thinking_and_answer(full_response.text)
                
                with st.expander("Show thinking process"):
                    st.markdown(f'<div class="think">{thinking}</div>', unsafe_allow_html=True)
                
                # Typewriter effect
                response = ""
                for chunk in answer.split():
                    response += chunk + " "
                    message_placeholder.markdown(response + "▌")
                    sleep(0.03)  # Slightly faster typing effect
                
                message_placeholder.markdown(answer)
                
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response.text})

if __name__ == "__main__":
    main()
