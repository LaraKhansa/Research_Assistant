# Research Assistant Tool

This project is designed to assist users in gathering information for their research. It consists of four main components: Scraper, PDF Converter, Chatbot, and a user-friendly Gradio interface to integrate all functionalities.


## Components
### 1. Scraper:
Designed to help users gather information for their research. It performs the following steps:

- Takes a research topic as input from the user.
- Conducts a Google search to find relevant articles and information.
- Scrapes outlines from the retrieved URLs to provide an overview of the content.

### 2. PDF Converter:  
Using "weasyprint" library, this modules enables converting a selected webpage to a PDF document, so users can easily archive and share it and chat about it.

### 3. Chatbot:
This the heart of the project, where the magic happens. This module is responsible for creating a Conversational Retrieval Chain using langchain:

- Instantiate an LLM model, either from local source (Ollama phi model) or from HuggingFace (OpenAssistant)
- Load given pdf file
- Split it to chunks
- Create and apply an embedding function on those chunks
- Create a vector database and fill it with the embedded vectors
- Create a retriever chain which is "history aware", which given chat history and a question, can reformulate it by adding context to it.
- Create a stuff documents chain, used to pass documents into a model
- Create the main chain, retrieval chain, which is built over the previous 2 chains

Then, it provides answer_query method, which gets the answer from the retrieval chain and saves chat history.

### 4. App:
All the project functionalities  are integrated into one Gradio interface, to provide an intuitive and interactive experience for the users. The interface consists of 3 main tabs:

- **Scrape Google Tab:**
Allows users to input a research topic and specify the number of links to scrape from Google. Then the user can take a look at the outlines of any of the scraped websites to choose the most relevant for his research.
- **Convert To PDF Tab:**
Lets users input a webpage URL to convert it to PDF, or upload a pdf from their device. Then, they can load it to the chatbot.
- **Chat with your PDF:**
Represents the retriever chain interface, which accepts questions input from user and displays chatbot answers, preserving the chat history (which can be cleared by the user)        

## Getting Started

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/LaraKhansa/Research_Assistant.git

3. Install the necessary dependencies:

   ```sh
   pip install -r requirements.txt

## Running the App
 To start the Gradio interface, run the following command:
 ```sh
   python app.py
 ```

## Usage

1. **Scrape Google Tab**: Enter a research topic and specify the number of links to scrape. Review the outlines and choose the relevant articles.
2. **Convert To PDF Tab**: Enter a webpage URL to convert to PDF or upload a PDF file from your device.
3. **Chat with your PDF Tab**: Load the PDF into the chatbot, ask questions, and get answers while preserving the chat history.




   
      

