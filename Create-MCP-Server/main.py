import arxiv
import json 
import os 
from typing import List 
from mcp.server.fastmcp import FastMCP
# import logging

PAPER_DIR = "papers"

#init fastmcp server

mcp = FastMCP("research")

@mcp.tool()
def search_papers(topic:str , max_results:int = 3) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.
    """
    #initialize arxiv client to search for papers
    client = arxiv.Client()

    #search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query = topic,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.Relevance,#sort them by relevance
        sort_order = arxiv.SortOrder.Descending,
    )
    papers = client.results(search)
    path = os.path.join(PAPER_DIR , topic.lower().replace(" ", "_"))

    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "papers_info.json")

    #load existing papers info if they exist
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}
    
    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info
    
    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)
    
    return paper_ids

@mcp.tool()
def extract_paper_info(paper_id:str) -> str:
    """
    Extract information about a paper from arXiv.
    """
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    continue
    
    return f"There's no saved information related to paper {paper_id}."

@mcp.tool()
def get_paper_citations(paper_id: str) -> str:
    """
    Get citation information for a paper by its arXiv ID.
    Returns citation in multiple formats (APA, MLA, BibTeX).
    """
    # First, try to find the paper in our stored data
    paper_info = None
    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            paper_info = papers_info[paper_id]
                            break
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    continue
    
    # If not found in stored data, try to fetch from arXiv
    if not paper_info:
        try:
            client = arxiv.Client()
            search = arxiv.Search(id_list=[paper_id])
            papers = list(client.results(search))
            if papers:
                paper = papers[0]
                paper_info = {
                    'title': paper.title,
                    'authors': [author.name for author in paper.authors],
                    'summary': paper.summary,
                    'pdf_url': paper.pdf_url,
                    'published': str(paper.published.date())
                }
            else:
                return f"Paper with ID {paper_id} not found on arXiv."
        except Exception as e:
            return f"Error fetching paper {paper_id} from arXiv: {str(e)}"
    
    if not paper_info:
        return f"Paper with ID {paper_id} not found."
    
    # Generate citations in different formats
    title = paper_info['title']
    authors = paper_info['authors']
    published = paper_info['published']
    
    # Format authors for citations
    if len(authors) == 1:
        author_str = authors[0]
    elif len(authors) == 2:
        author_str = f"{authors[0]} & {authors[1]}"
    else:
        author_str = f"{authors[0]} et al."
    
    # APA Format
    apa_citation = f"{author_str} ({published[:4]}). {title}. arXiv preprint arXiv:{paper_id}."
    
    # MLA Format
    mla_citation = f'"{title}." arXiv preprint arXiv:{paper_id}, {published}.'
    
    # BibTeX Format
    bibtex_key = paper_id.replace('.', '').replace('v', '')
    bibtex_citation = f"""@misc{{{bibtex_key},
    title={{{title}}},
    author={{{' and '.join(authors)}}},
    year={{{published[:4]}}},
    eprint={{{paper_id}}},
    archivePrefix={{arXiv}},
    primaryClass={{cs.AI}}
}}"""
    
    citations = {
        "paper_id": paper_id,
        "title": title,
        "authors": authors,
        "published": published,
        "citations": {
            "APA": apa_citation,
            "MLA": mla_citation,
            "BibTeX": bibtex_citation
        }
    }
    
    return json.dumps(citations, indent=2)




if __name__ == "__main__":
    mcp.run(transport="stdio")