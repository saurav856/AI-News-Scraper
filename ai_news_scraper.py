import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

# keywords to filter AI related stories
AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "gpt", "chatgpt", "openai", "gemini", "claude", "neural",
    "ml", "nlp", "computer vision", "transformer", "diffusion", "robot"
]

HN_URL = "https://news.ycombinator.com/"


def fetch_page(url):
    # send a GET request to the url and return parsed html
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def is_ai_related(title):
    # check if the story title contains any AI related keyword
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in AI_KEYWORDS)


def scrape_ai_news():
    # scrape hacker news and return only AI related stories
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

        # if link is relative, make it absolute
        if link.startswith("item?"):
            link = HN_URL + link

        score_tag = subtext_row.select_one("span.score")
        score = score_tag.get_text() if score_tag else "0 points"

        # only add story if it is AI related
        if is_ai_related(title):
            stories.append({
                "title": title,
                "score": score,
                "link": link
            })

    return stories


def save_to_csv(stories):
    # save the stories to a csv file with timestamp in filename
    filename = f"ai_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "score", "link"])
        writer.writeheader()
        writer.writerows(stories)
    print(f"Saved to {filename}")


def display_stories(stories):
    # print all stories in a readable format
    if not stories:
        print("No AI stories found right now.")
        return

    print(f"\nFound {len(stories)} AI stories on Hacker News\n")
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']}")
        print(f"   Score: {story['score']}")
        print(f"   Link: {story['link']}")
        print()


if __name__ == "__main__":
    print("Fetching AI news from Hacker News...")
    stories = scrape_ai_news()
    display_stories(stories)
    save_to_csv(stories)