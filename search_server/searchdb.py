"""SearchDB py."""

import os
import pathlib
import sqlite3
from bs4 import BeautifulSoup


BASE_DIR = pathlib.Path(os.getcwd()).resolve()
INPUT_DIR = BASE_DIR / "inverted_index" / "crawl"
OUTPUT_DB = BASE_DIR / "var" / "search.sqlite3"

print(f"BASE_DIR: {BASE_DIR}")
print(f"INPUT_DIR: {INPUT_DIR}")
print(f"OUTPUT_DB: {OUTPUT_DB}")


def get_summary(soup):
    """Get summary."""
    summary = ""
    p_elts = soup.find_all("p", class_=False)
    for p in p_elts:
        p = p.text
        # If the body isn't empty and longer than 50 characters (arbitrary)
        if p.strip() and len(p) > 50:
            # Limit summary to 250 characters (including truncation)
            summary = p.strip()[0:247]

            # Replace newlines to format query string
            summary = summary.replace("\n", " ")

            # Truncate endings
            summary = summary + "..."
            break

    return summary


def main():
    """Func to populate DB."""
    if os.path.exists(OUTPUT_DB):
        print(f"Removing existing database at: {OUTPUT_DB}")
        os.remove(OUTPUT_DB)
    os.makedirs(os.path.dirname(OUTPUT_DB), exist_ok=True)

    if not INPUT_DIR.exists():
        print(f"ERROR: Input directory not found: {INPUT_DIR}")
        exit(1)

    conn = sqlite3.connect(OUTPUT_DB)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE documents (
            docid INTEGER PRIMARY KEY,
            title VARCHAR(150),
            summary VARCHAR(250),
            url VARCHAR(150)
        );
        """
    )

    for f1 in sorted(os.listdir(INPUT_DIR)):
        file_path = os.path.join(INPUT_DIR, f1)
        with open(file_path, "r", encoding="utf-8") as f2:
            soup = BeautifulSoup(f2, "html.parser")

            # extract metadata
            meta_tag = soup.find("meta", attrs={"eecs485_docid": True})
            docid = int(meta_tag["eecs485_docid"])
            url = soup.find("meta", attrs={"eecs485_url": True})["eecs485_url"]

            raw_title = soup.title.string.strip()

            summary = get_summary(soup)

            cur.execute(
                """INSERT INTO documents (docid, title, summary, url)
                VALUES (?, ?, ?, ?)""",
                (docid, raw_title, summary, url)
            )

    conn.commit()
    conn.close()
    exit(0)


if __name__ == "__main__":
    main()
