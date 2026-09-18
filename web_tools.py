import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re
from html import unescape


# ============================================================
# CONFIG
# ============================================================

BING_RSS_URL = "https://www.bing.com/search"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/142.0.0.0 Safari/537.36"
)

MAX_RESULTS = 5


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# QUERY WORDS
# ============================================================

def query_words(query):
    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "what",
        "who",
        "when",
        "where",
        "how",
        "why",
        "which",
        "tell",
        "me",
        "about",
        "please",
        "give",
        "latest",
        "today",
        "news",
        "current",
    }

    words = re.findall(r"[a-zA-Z0-9]+", query.lower())

    return [
        word
        for word in words
        if len(word) > 2 and word not in stop_words
    ]


# ============================================================
# CURRENT INFORMATION DETECTION
# ============================================================

def is_current_query(query):
    current_words = {
        "latest",
        "today",
        "current",
        "recent",
        "new",
        "news",
        "update",
        "updates",
        "2026",
    }

    words = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))

    return bool(words.intersection(current_words))


# ============================================================
# RELEVANCE SCORE
# ============================================================

def relevance_score(query, title, description, url):
    query_lower = query.lower()

    title_lower = title.lower()
    description_lower = description.lower()
    url_lower = url.lower()

    words = query_words(query)

    score = 0

    # Exact query match
    if query_lower in title_lower:
        score += 10

    if query_lower in description_lower:
        score += 5

    # Individual keyword matches
    for word in words:
        if word in title_lower:
            score += 4

        if word in description_lower:
            score += 2

        if word in url_lower:
            score += 1

    # Current queries should prefer recent-looking content
    if is_current_query(query):
        current_terms = [
            "2026",
            "today",
            "latest",
            "recent",
            "update",
        ]

        for term in current_terms:
            if term in title_lower:
                score += 2

            if term in description_lower:
                score += 1

    return score


# ============================================================
# SINGLE BING RSS SEARCH
# ============================================================

def single_search(query):
    params = {
        "format": "rss",
        "q": query,
    }

    url = BING_RSS_URL + "?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, text/xml",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = response.read()

        root = ET.fromstring(data)

    except urllib.error.URLError as error:
        print(f"Web search error: {error}")
        return []

    except ET.ParseError:
        print("Web search error: Invalid RSS response.")
        return []

    except Exception as error:
        print(f"Web search error: {error}")
        return []

    results = []

    for item in root.findall(".//item"):
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        description = item.findtext("description", default="")

        title = clean_text(title)
        link = clean_text(link)
        description = clean_text(description)

        if not title or not link:
            continue

        results.append(
            {
                "title": title,
                "url": link,
                "snippet": description,
                "score": relevance_score(
                    query,
                    title,
                    description,
                    link,
                ),
            }
        )

    return results


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(results):
    unique = []
    seen = set()

    for result in results:
        url = result.get("url", "").strip().lower()

        if not url:
            continue

        if url in seen:
            continue

        seen.add(url)
        unique.append(result)

    return unique


# ============================================================
# FILTER RELEVANT RESULTS
# ============================================================

def filter_relevant(results, minimum_score=2):
    filtered = []

    for result in results:
        if result.get("score", 0) >= minimum_score:
            filtered.append(result)

    filtered.sort(
        key=lambda item: item.get("score", 0),
        reverse=True,
    )

    return filtered


# ============================================================
# BUILD SEARCH QUERIES
# ============================================================

def build_search_queries(query):
    queries = []

    query = query.strip()

    if not query:
        return queries

    queries.append(query)

    # Improve current/news searches
    if is_current_query(query):
        cleaned = re.sub(
            r"\b(latest|today|current|recent|news|updates?)\b",
            "",
            query,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        if cleaned:
            queries.append(f"{cleaned} latest news 2026")

    return list(dict.fromkeys(queries))


# ============================================================
# MAIN WEB SEARCH
# ============================================================

def web_search(query, max_results=MAX_RESULTS):
    if not query or not query.strip():
        return []

    search_queries = build_search_queries(query)

    all_results = []

    for search_query in search_queries:
        results = single_search(search_query)
        all_results.extend(results)

    all_results = remove_duplicates(all_results)

    relevant = filter_relevant(
        all_results,
        minimum_score=2,
    )

    return relevant[:max_results]


# ============================================================
# TEST SEARCH
# ============================================================

def test_search():
    print("=" * 60)
    print("RUDRA WEB INTELLIGENCE TEST")
    print("=" * 60)

    query = input("\nSearch > ").strip()

    if not query:
        print("No search query entered.")
        return

    print("\nSearching the web...\n")

    results = web_search(query)

    if not results:
        print("No relevant results found.")
        return

    for index, result in enumerate(results, start=1):
        print(f"[{index}] {result.get('title', '')}")
        print(f"    {result.get('snippet', '')}")
        print(f"    {result.get('url', '')}")
        print(f"    Relevance Score: {result.get('score', 0)}")
        print()

    print(f"Found {len(results)} relevant results.")


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    test_search()