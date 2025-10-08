# Research MCP Server

A Model Context Protocol (MCP) server for searching and managing research papers from arXiv. This server provides tools to search for academic papers, store their metadata, and retrieve information about previously searched papers.

## Features

- Search arXiv for papers by topic
- Store paper metadata locally in JSON format
- Retrieve information about previously searched papers
- Organize papers by topic in separate directories
- Get citation information for a paper in multiple academic formats (APA, MLA, BibTeX).

## Setup

### Prerequisites

- Python 3.11 or higher
- uv package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd Create-MCP-Server
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Verify installation:
```bash
python main.py --help
```

## Usage

### Running the Server

Start the MCP server:
```bash
python main.py
```

The server runs in stdio mode and is ready to accept MCP protocol messages.

### Testing with MCP Inspector

- Launch the inspector:
    - `npx @modelcontextprotocol/inspector uv run main.py`
    - If you get a message asking "need to install the following packages", type: `y`
    - Test the available tools in the inspector interface

### Available Tools

#### search_papers(topic: str, max_results: int = 3)
Search arXiv for papers on a specific topic and store their information locally.

**Parameters:**
- `topic`: The research topic to search for
- `max_results`: Maximum number of papers to retrieve (default: 3)

**Example:**
```json
{
  "topic": "machine learning",
  "max_results": 5
}
```

#### extract_paper_info(paper_id: str)
Retrieve detailed information about a previously searched paper.

**Parameters:**
- `paper_id`: The arXiv paper ID (e.g., "1909.03550v1")

**Example:**
```json
{
  "paper_id": "1909.03550v1"
}
```
#### get_paper_citations(paper_id: str)
Get citation information for a paper in multiple academic formats (APA, MLA, BibTeX).

**Parameters:**
- `paper_id`: The arXiv paper ID (e.g., "1909.03550v1")

**Example:**
```json
{
  "paper_id": "1909.03550v1"
}
```

**Returns:** JSON object with paper metadata and citations in APA, MLA, and BibTeX formats.


