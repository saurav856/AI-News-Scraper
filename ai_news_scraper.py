"""
AI News Scraper
===============
Scrapes the latest AI-related news and discussions from Hacker News.
Fetches top stories filtered by AI-related keywords and displays
the title, score, and link for each story.

Requirements:
    pip install requests beautifulsoup4

Usage:
    python ai_news_scraper.py
"""

import requests
from bs4 import BeautifulSoup

AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "gpt", "chatgpt", "openai", "gemini", "claude", "neural",
    "ml", "nlp", "computer vision", "transformer", "diffusion", "robot"
]

HN_URL = "https://news.ycombinator.com/"


def fetch_page(url: str) -> BeautifulSoup:
    """
    Fetch a webpage and return a BeautifulSoup object.

    Parameters
    ----------
    url: str, the URL to fetch

    Returns
    -------
    BeautifulSoup: parsed HTML content
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def is_ai_related(title: str) -> bool:
    """
    Check if a title contains AI-related keywords.

    Parameters
    ----------
    title: str, the story title to check

    Returns
    -------
    bool: True if AI-related, False otherwise
    """
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in AI_KEYWORDS)


def scrape_ai_news() -> list[dict]:
    """
    Scrape AI-related stories from Hacker News.

    Returns
    -------
    list[dict]: list of AI stories with title, score, and link
    """
    soup = fetch_page(HN_URL)
    stories = []

    title_rows = soup.select("tr.athing")
    subtext_rows = soup.select("td.subtext")

    for title_row, subtext_row in zip(title_rows, subtext_rows):
        title_tag = title_row.select_one("span.titleline > a")
        if not title_tag:
            continue

        title = title_tag.get_text()
        link = title_tag.get("href", "")

        if link.startswith("item?"):
            link = HN_URL + link

        score_tag = subtext_row.select_one("span.score")
        score = score_tag.get_text() if score_tag else "0 points"

        if is_ai_related(title):
            stories.append({
                "title": title,
                "score": score,
                "link": link
            })

    return stories


def display_stories(stories: list[dict]) -> None:
    """
    Display the scraped AI stories in a readable format.

    Parameters
    ----------
    stories: list[dict], list of stories to display
    """
    if not stories:
        print("No AI-related stories found right now. Try again later!")
        return

    print(f"\n{'=' * 60}")
    print(f"  AI NEWS FROM HACKER NEWS ({len(stories)} stories found)")
    print(f"{'=' * 60}\n")

    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']}")
        print(f"   Score : {story['score']}")
        print(f"   Link  : {story['link']}")
        print()


if __name__ == "__main__":
    print("Fetching latest AI news from Hacker News...")
    stories = scrape_ai_news()
    display_stories(stories)