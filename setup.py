from setuptools import setup, find_packages

setup(
    name="gmail_ai_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "langchain-community",
        "langgraph",
        "fastapi",
        "uvicorn",
        "streamlit",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
        "faiss-cpu",
        "requests",
    ],
) 