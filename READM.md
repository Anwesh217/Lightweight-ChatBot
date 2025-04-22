# Ollama Qwen2.5 Chatbot with Streamlit

A lightweight, privacy-focused chatbot application that leverages Ollama's local LLMs and Streamlit's interactive UI to deliver real-time streaming responses.

## 🔧 Tech Stack

- **Ollama**: Open-source framework for running LLMs locally
- **Streamlit**: Python library for building interactive web apps
- **Qwen2.5**: High-quality open-source language model

## 📋 Prerequisites

- Python 3.12
- [Ollama](https://ollama.ai/) installed and running
- At least 8GB RAM (16GB recommended for optimal performance)

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Anwesh217/ollama-qwen-chatbot.git
   cd ollama-qwen-chatbot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Pull the Qwen2.5 model using Ollama:
   ```bash
   ollama pull qwen2:5b
   ```

4. Start the Ollama server (if not already running):
   ```bash
   ollama serve
   ```

5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

6. Open your browser and visit `http://localhost:8501`

## 📋 Requirements.txt

```
pip install -r requirements.txt

```

## 🔄 How It Works

1. The application uses Streamlit for the frontend UI
2. User messages are sent to the locally running Ollama server
3. The Qwen2.5 model processes the input and streams the response back
4. The UI displays the streaming tokens in real-time, creating a natural conversational experience



Contributions are welcome! Please feel free to submit a Pull Request.

