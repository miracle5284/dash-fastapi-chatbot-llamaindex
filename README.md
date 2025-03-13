# Chatbot Application

Welcome to the Chatbot Application project, a complete AI-powered chatbot solution featuring a robust backend and multiple user interfaces. This project demonstrates the seamless integration of machine learning capabilities and user-friendly interfaces, making it an excellent addition to any portfolio.

---

## **Overview**

This project consists of two main components and interfaces:

1. **Backend (`Chatbot` folder):**
   - Handles document indexing, query processing, and integration with the vector store for efficient responses
   - Built with Python and includes utilities for handling PDFs, FAQs, and other document formats
   - Integrates with OpenAI's ChatGPT for natural conversations

2. **User Interfaces:**
   - **RAG-powered FAQ Interface:**
     - Provides intelligent responses based on your document knowledge base
     - Built with Dash, offering responsive design and real-time communication
   - **ChatGPT Conversation Interface:**
     - Simple and intuitive chat interface for direct interactions with ChatGPT
     - Maintains conversation context for natural dialogue flow
     - No RAG integration, perfect for general queries and conversations

---

## **Features**

### **Backend Features**
- **Document Indexing**: Supports processing and indexing of documents (e.g., PDFs)
- **FAQ Handling**: Efficient FAQ vector store for quick and accurate responses
- **API Integration**: Serves as the foundation for seamless communication with the frontends
- **Modular Design**: Configurable settings using `config.py` and `.env` files
- **OpenAI Integration**: Direct integration with ChatGPT for natural language processing

### **Frontend Features**
- **Dual Interface Options**: Choose between RAG-powered FAQ bot or direct ChatGPT interactions
- **Interactive UI**: Sleek and user-friendly interfaces for both chat modes
- **Real-Time Interaction**: Facilitates real-time responses using state management tools
- **Conversation History**: Maintains chat context for more natural interactions
- **Error Handling**: Alerts users to invalid inputs or backend connection issues

---

## **Technologies Used**

- **Backend**:
  - Python 3.12+
  - FastAPI for API endpoints
  - LlamaIndex for document indexing
  - LangChain for AI interactions
  - OpenAI's ChatGPT integration

- **Frontend**:
  - Dash Framework
  - HTML/CSS for styling
  - REST API integration
  - Real-time state management

- **Development Tools**:
  - PowerShell automation
  - Python virtual environments
  - Environment variable management

---

## **Quick Start (Windows)**

The easiest way to get started is using our PowerShell automation script:

1. Clone the repository:
   ```bash
   git clone https://github.com/miracle5284/dash-fastapi-chatbot-llamaindex.git
   cd dash-fastapi-chatbot-llamaindex
   ```

2. Run the automation script:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\run_chatbot.ps1
   ```

The script will automatically:
- Check and install Python 3.12 if needed
- Create and configure a virtual environment
- Install all required dependencies
- Prompt for your OpenAI API key
- Set up environment variables
- Start both the FastAPI server and Dash UI
- Open your browser to the chat interface

To stop the application:
   - Press `Ctrl+C` in the terminal running the servers
   - Both servers (FastAPI and Dash UI) will shut down gracefully

---

## **Manual Setup**

If you prefer manual setup or are using a different operating system:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Create a `.env` file with:
     ```
     OPENAI_API_KEY=your_api_key_here
     OPENAI_MODEL_NAME=gpt-3.5-turbo
     ```

3. Start the servers:
   ```bash
   # Start FastAPI server
   uvicorn chatbot.server:app --reload

   # Start Dash UI (in another terminal)
   python chatbot-ui/dash-chat-ui.py
   ```

---

## **Usage**

1. Access the interfaces:
   - For ChatGPT-only interface (no RAG):
     ```
     http://127.0.0.1:5500
     ```
   - For RAG-powered FAQ interface:
     ```
     http://127.0.0.1:8050
     ```

2. Choose your interaction mode:
   - Use the FAQ interface (port 8050) for document-based queries
   - Use the ChatGPT interface (port 5500) for general conversations

3. Enter your queries and receive intelligent responses

4. To stop the application:
   - Press `Ctrl+C` on both terminal running the servers

Note: The PowerShell automation script (`run_chatbot.ps1`) is configured to launch the ChatGPT-only interface by default. To use the RAG-powered FAQ interface, you'll need to run:
```bash
python chatbot/dash-ui.py
```

---

## **Folder Structure**

```
chatbot/
├── chatbot/               # Backend code
│   ├── config.py         # Configuration settings
│   ├── server.py         # Main server script
│   ├── indexing.py       # Document indexing utilities
│   ├── schemas.py        # Data models
│   ├── utils.py          # Helper functions
│   └── documents/        # Input documents (e.g., PDFs)
├── chatbot-ui/           # Frontend code
│   ├── dash-chat-ui.py   # ChatGPT interface
│   ├── styles.py         # UI styling
│   └── config.py         # Frontend configuration
├── run_chatbot.ps1       # Windows automation script
├── .env                  # Environment variables
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

---

## **Screenshot**

Below is an example of the Chatbot UI in action:

![Chatbot UI Screenshot](assets/chatbot-ui.png)

---

## **Configuration**

The application can be configured through several files:

1. **Environment Variables** (`.env` file):
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL_NAME=gpt-3.5-turbo
   ```

2. **Server Configuration** (`chatbot-ui/config.py`):
   - Configure server URLs, ports, and debug settings
   - Settings for both FastAPI backend and Dash UI

3. **System Prompt** (`system_prompt.txt`):
   - Contains the instructions and behavior guidelines for the ChatGPT model
   - Customize the model's personality and response style
   - Modify the prompt to change how the chatbot interacts with users

---

## **Contributing**

We welcome contributions to enhance the functionality and design of this chatbot application! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork:
   ```bash
   git commit -m "Description of changes"
   git push origin feature-name
   ```
4. Open a pull request on the main repository.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Contact**

For questions, feedback, or collaboration opportunities, feel free to reach out:

- **Email**: miracle5284@users.noreply.github.com
- **GitHub**: [Miracle Mayowa Adebunmi](https://github.com/miracle5284)
