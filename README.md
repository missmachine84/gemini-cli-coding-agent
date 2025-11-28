## gemini-cli-coding-agent

**Description:**

A command-line, LLM-powered coding agent that can read, edit, and execute Python code using Google’s Gemini API and structured tool-calling.
It supports file inspection, code refactoring, bug fixing, and running test suites through an iterative agentic loop.

This project recreates the core behavior of modern agentic coding tools—such as Cursor, Claude Code, and GitHub Copilot Labs—built entirely from scratch as part of the Boot.dev Agents course.

**Highlights:** 

This project is intentionally designed to demonstrate:

LLM tool-calling architecture

Multi-step agent planning loops

Safe code execution with sandboxed filesystem access

Integration with modern LLM SDKs (Gemini API, Google GenAI)

Systems engineering, orchestration, and message routing

Automated debugging + code manipulation driven by an LLM

**Table of Contents**

1. Project Overview

2. Technical Architecture

3. Agent Loop Diagram

4. Repository Structure
   
5. Features

6. Installation

7. Usage

8. Skills Demonstrated

9. License
    

**Project Overview**

This agent can:

1. Inspect files in a controlled project environment

2. Read and write Python source code

3. Execute Python modules safely

4. Iteratively debug and repair code using an LLM

5. Run test suites to validate its own fixes

6. Use multi-turn planning to solve tasks that require multiple steps

7. A common demonstration:

   uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"



**Technical Architecture**

The system is composed of three major layers:

*1. LLM Interface Layer (Gemini API)*

Responsible for:

Sending conversation state (messages)

Specifying available tools (function schemas)

Receiving structured responses

Handling model text + function_calls + candidates

Uses:

client.models.generate_content(model="gemini-2.0-flash-001", ...)

*2. Tool Execution Layer*

A set of Python functions the LLM can call:

Core tools exposed to the model:

get_files_info() — list directory contents

get_file_content() — read a file

write_file() — modify or create a file

run_python_file() — execute Python in a restricted subprocess

Each tool has a schema describing:

Function name

Parameters

Expected return format

These schemas are passed to Gemini as part of GenerateContentConfig.

*3. Agent Control Loop*

Implements:

Multi-step reasoning

Function dispatch

Conversation memory

Termination conditions

Runs up to 20 iterations:
for _ in range(20):
    response = model.generate(...)
    if model wants function calls:
         execute tools
         append outputs into messages
    else:
         print final response
         break
This transforms the model from a single-turn LLM into an iterative autonomous agent.


```
**Agent Loop Diagram**
┌──────────────────────────┐
│   User prompt (CLI)      │
└───────────────┬──────────┘
                │
                ▼
     ┌──────────────────────┐
     │  LLM (Gemini API)    │
     │ plan + function_calls│
     └───────────┬──────────┘
                 │
     For each function_call:
                 ▼
       ┌───────────────────┐
       │  Tool Dispatcher  │
       │ (call_function)   │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ Tool Implementations
       │  get_file_content
       │  run_python_file
       │  write_file
       │  get_files_info
       └───────────────────┘
                 │
                 ▼
       ┌──────────────────┐
       │   Tool Output    │
       └─────────┬────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │ Append to messages list  │
    └─────────────┬────────────┘
                  │
                  ▼
        Back to LLM (loop)


The loop ends only when:

No further function calls are included, and

The model returns a final natural-language answer.

**Repository Structure**
aiagent/
├── main.py                     # Agent loop + CLI
├── call_function.py            # Tool dispatch + schemas
├── prompts.py                  # System prompt logic
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python.py
│   └── write_file_content.py
├── calculator/
│   ├── main.py
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   ├── lorem.txt
│   └── tests.py
└── pyproject.toml
```

**Installation**

Create a .env:

GEMINI_API_KEY=your_key_here

**Usage**

Run the agent:

uv run main.py "fix the bug: operator precedence is wrong"


Verbose mode:

uv run main.py "how does the calculator work?" --verbose


Run the calculator directly:

uv run calculator/main.py "7 - 5"


Run calculator tests:

uv run calculator/tests.py

**Skills Demonstrated**
-Machine Learning / LLM Engineering

-Tool-calling architecture design

-Multi-turn generative agent systems

-Safe model–tool coordination

-Structured LLM inference using Gemini API

-Systems Engineering

-Subprocess orchestration

-Sandbox filesystem access

-Finite control loops for autonomous behavior

-Defensive error handling

Test-driven debugging (agent uses tests to validate fixes)

-CLI interface design

**License**

MIT License.
This project includes original agentic logic built for educational and professional demonstration purposes.


---

## What I Learned

(We’ll fill this out near the end — this is great for recruiters.)

---
