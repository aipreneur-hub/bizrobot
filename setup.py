from setuptools import setup, find_packages

setup(
    name="bizrobot",
    version="0.1.0",
    description="LLM-powered autonomous business operations agent",
    author="Cengiz (CK)",
    author_email="you@example.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "langchain>=0.2.14",
        "langchain-openai>=0.1.8",
        "langgraph>=0.0.15",
        "fastapi>=0.110.0",
        "uvicorn>=0.29.0",
        "requests>=2.32.0",
        "PyYAML>=6.0",
        "chromadb>=0.5.0",
        "pydantic>=2.8.0",
        "openai>=1.37.0",
        "playwright>=1.47.0",
        "tenacity>=8.3.0",
    ],
)
