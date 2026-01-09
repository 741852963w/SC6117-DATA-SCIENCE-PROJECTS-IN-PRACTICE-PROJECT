<div align="center" id="top">



####




</div>

# VentureProof

VentureProof is a focused customization of this project for venture and industry analysis.

- Purpose: Enter a brief venture idea and generate a structured analysis report (market size, competition, unit economics, GTM, risks, roadmap) with citations.
- Minimal UI: The frontend defaults to a clean, brand‑less interface named “VentureProof”.
- No template or retriever changes are required; we constrain the writing stage with a business‑analysis prompt.

Quick notes
- Backend: BUSINESS_MODE is enabled by default to apply the business writing prompt.
- Frontend (Minimal UI): Home page provides optional fields for Target Region, Target Customer, and Competitors to guide report tone; these are sent to the backend as headers and reflected in the prompt only.
- All original features and installation steps below remain valid.

---

#  GPT Researcher

**GPT Researcher is an open deep research agent designed for both web and local research on any given task.** 

The agent produces detailed, factual, and unbiased research reports with citations. GPT Researcher provides a full suite of customization options to create tailor made and domain specific research agents. Inspired by the recent [Plan-and-Solve](https://arxiv.org/abs/2305.04091) and [RAG](https://arxiv.org/abs/2005.11401) papers, GPT Researcher addresses misinformation, speed, determinism, and reliability by offering stable performance and increased speed through parallelized agent work.

**Our mission is to empower individuals and organizations with accurate, unbiased, and factual information through AI.**

## Why GPT Researcher?

- Objective conclusions for manual research can take weeks, requiring vast resources and time.
- LLMs trained on outdated information can hallucinate, becoming irrelevant for current research tasks.
- Current LLMs have token limitations, insufficient for generating long research reports.
- Limited web sources in existing services lead to misinformation and shallow results.
- Selective web sources can introduce bias into research tasks.


## Architecture

The core idea is to utilize 'planner' and 'execution' agents. The planner generates research questions, while the execution agents gather relevant information. The publisher then aggregates all findings into a comprehensive report.

<div align="center">
<img align="center" height="600" src="https://github.com/assafelovic/gpt-researcher/assets/13554167/4ac896fd-63ab-4b77-9688-ff62aafcc527">
</div>

Steps:
* Create a task-specific agent based on a research query.
* Generate questions that collectively form an objective opinion on the task.
* Use a crawler agent for gathering information for each question.
* Summarize and source-track each resource.
* Filter and aggregate summaries into a final research report.


## Features

-  Generate detailed research reports using web and local documents.
-  Smart image scraping and filtering for reports.
-  Generate detailed reports exceeding 2,000 words.
-  Aggregate over 20 sources for objective conclusions.
-  Frontend available in lightweight (HTML/CSS/JS) and production-ready (NextJS + Tailwind) versions.
-  JavaScript-enabled web scraping.
-  Maintains memory and context throughout research.
-  Export reports to PDF, Word, and other formats.

##  Documentation

See the [Documentation](https://docs.gptr.dev/docs/gpt-researcher/getting-started) for:
- Installation and setup guides
- Configuration and customization options
- How-To examples
- Full API references

##  Getting Started

### Installation

1. Install Python 3.11 or later. [Guide](https://www.tutorialsteacher.com/python/install-python).
2. Clone the project and navigate to the directory:
3. Set up API keys by exporting them or storing them in a `.env` file.

    ```bash
    export OPENAI_API_KEY={Your OpenAI API Key here}
    export TAVILY_API_KEY={Your Tavily API Key here}
    ```
    For custom OpenAI-compatible APIs (e.g., local models, other providers), you can also set:
    
    ```bash
    export OPENAI_BASE_URL={Your custom API base URL here}
    ```

4. Install dependencies and start the server:

    ```bash
    pip install -r requirements.txt
    python -m uvicorn main:app --reload
    ```

Visit [http://localhost:8000](http://localhost:8000) to start.

For other setups (e.g., Poetry or virtual environments), check the [Getting Started page](https://docs.gptr.dev/docs/gpt-researcher/getting-started).


```

**For more examples and configurations, please refer to the [PIP documentation](https://docs.gptr.dev/docs/gpt-researcher/gptr/pip-package) page.**

###  MCP Client
GPT Researcher supports MCP integration to connect with specialized data sources like GitHub repositories, databases, and custom APIs. This enables research from data sources alongside web search.

```bash
export RETRIEVER=tavily,mcp  # Enable hybrid web + MCP research
```

```python
from gpt_researcher import GPTResearcher
import asyncio
import os

async def mcp_research_example():
    # Enable MCP with web search
    os.environ["RETRIEVER"] = "tavily,mcp"
    
    researcher = GPTResearcher(
        query="What are the top open source web research agents?",
        mcp_configs=[
            {
                "name": "github",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
            }
        ]
    )
    
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    return report
```

> For comprehensive MCP documentation and advanced examples, visit the [MCP Integration Guide](https://docs.gptr.dev/docs/gpt-researcher/retrievers/mcp-configs).



```bash
docker-compose up --build
```

If that doesn't work, try running it without the dash:
```bash
docker compose up --build
```

> **Step 4** - By default, if you haven't uncommented anything in your docker-compose file, this flow will start 2 processes:
 - the Python server running on localhost:8000<br>
 - the React app running on localhost:3000<br>

Visit localhost:3000 on any browser and enjoy researching!
