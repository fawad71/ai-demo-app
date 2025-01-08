# AI Demo App

A comprehensive demonstration of various AI agent implementations using LangChain, including RAG (Retrieval-Augmented Generation), ReAct agents, and graph-based workflows.

## 🌟 Features

- Multiple AI agent implementations
- RAG-based knowledge retrieval
- Graph-based workflow orchestration
- Web-based UI interface
- Code interpretation capabilities
- CSV data processing

## 📁 Project Structure

```
ai-demo-app/
├── agents/                 # Different agent implementations
│   ├── rag/               # RAG-based agents
│   ├── react-agent/       # ReAct pattern agents
│   └── code-interpreter/  # Code interpretation agents
├── graphs/                # Graph-based workflows
│   ├── rag/              # RAG workflow implementations
│   ├── reflexion/        # Reflexion pattern implementations
│   ├── router/           # Routing logic
│   └── HITL_memory/      # Human-in-the-loop memory systems
├── ui/                    # Frontend interface
├── utils/                # Utility functions
├── docs/                 # Documentation
└── chroma_db/           # Vector database storage
```

## 🛠️ Prerequisites

- Python 3.12.7
- Poetry (Python package manager)
- Node.js (for UI components)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-demo-app
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install Python dependencies:
```bash
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` with your API keys and configuration.

5. Install UI dependencies:
```bash
cd ui
npm install
```

## 🚀 Running the Project

1. Activate the Poetry virtual environment:
```bash
poetry shell
```

2. Set up the Python path:
```bash
export PYTHONPATH=/path/to/ai-demo-app
```

3. Start the backend services using LangGraph:
```bash
langgraph up
```
This will start the LangGraph server and load all your graph-based workflows.

4. In a separate terminal, start the UI:
```bash
cd ui
npm run dev
```

## 🔑 Environment Variables

Required environment variables in your `.env` file:

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="your-project-name"
LANGSMITH_API_KEY="your_langsmith_api_key"
OPENAI_API_KEY="your_openai_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

## 📚 Documentation

For more detailed information about the project's components:

- [Agentic AI Overview](docs/agentic_ai_presentation.md)
- Check individual module directories for specific documentation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain team for the excellent framework
- OpenAI for their powerful language models
- All contributors to the project
