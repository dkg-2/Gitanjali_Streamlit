# Gitanjali - Bhagavad Gita AI Guide

An intelligent AI assistant that provides wisdom and guidance from the sacred Bhagavad Gita, powered by modern NLP and vector search technologies.

## 🌟 Features

- **Multilingual Support:** Get responses in English, Hindi, or Sanskrit.
- **Context-Aware Answers:** Responses include relevant chapter and verse references.
- **Natural Language Understanding:** Ask questions in your own words.
- **Spiritual Guidance:** Get insights based on the timeless wisdom of the Bhagavad Gita.


## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)


### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/dkg-2/Gitanjali_Streamlit.git
cd Gitanjali_Streamlit
```

2. **Create and Activate a Virtual Environment**

On Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
    - Create a `.env` file in the project root.
    - Add your Qdrant credentials:

```
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

5. **Run the Application**

```bash
streamlit run app2.py
```

    - The app will be available at [http://localhost:8501](http://localhost:8501).

## 🛠️ Tech Stack

- **Backend:** Python, Streamlit
- **AI/ML:**
    - llama-index for document processing
    - FastEmbed for text embeddings
    - Groq for LLM inference
- **Vector Database:** Qdrant
- **Frontend:** Streamlit UI


## 📂 Project Structure

```
Gitanjali_Streamlit/
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── app2.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
└── Bhagavad-Gita As It Is.pdf  # Source text
```


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

- Fork the repository
- Create your feature branch (`git checkout -b feature/AmazingFeature`)
- Commit your changes (`git commit -m 'Add some AmazingFeature'`)
- Push to the branch (`git push origin feature/AmazingFeature`)
- Open a Pull Request


## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- The timeless wisdom of the Bhagavad Gita
- All open-source libraries and tools used in this project

<div style="text-align: center">⁂</div>

[^1]: https://static.streamlit.io/badges/streamlit_badge_black_white.svg

[^2]: https://streamlit.io

