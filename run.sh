#!/bin/bash
source .venv/bin/activate
export PYTHONPATH=.
export OPENAI_API_KEY="your_key"
python -m bizrobot.examples.bizrobot_langchain_agent
