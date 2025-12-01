"""
Search server index view.

URLs: '/'
"""

import os
import pathlib
import sqlite3
import threading

import flask
import requests

bp = flask.Blueprint("index", __name__)

BASE_DIR = pathlib.Path(os.getcwd()).resolve()
OUTPUT_DB = BASE_DIR / "var" / "search.sqlite3"

"""def fetch(server, query, weight, out_list):
    try:
        response = requests.get(server,
            params={"q": query, "w": weight}, timeout=2)
        response.raise_for_status()
        hits = response.json().get("hits", [])
        out_list.extend(hits)
        print(f"OUT_LIST: {out_list}")
    except Exception as e:
        print(e)"""


@bp.route("/", methods=["GET"])
def index():
    """Show index page."""
    query = flask.request.args.get("q", "")
    weight = flask.request.args.get("w", 0.5)

    try:
        pagerank_weight = float(weight)
    except ValueError:
        pagerank_weight = 0.5

    results = []
    hits = []
    threads = []
    results_lock = threading.Lock()

    def fetch(server, query, weight, out_list):
        try:
            # Ensure the URL ends with /hits/
            if not server.endswith("/hits/"):
                url = server.rstrip("/") + "/hits/"
            else:
                url = server

            response = requests.get(
                url,
                params={"q": query, "w": weight},
                timeout=2
            )
            response.raise_for_status()
            hits = response.json().get("hits", [])
            with results_lock:
                out_list.extend(hits)
            # print(f"OUT_LIST: {out_list}")
        except requests.RequestException as e:
            print(e)

    for server in flask.current_app.config["SEARCH_INDEX_SEGMENT_API_URLS"]:
        t = threading.Thread(
            target=fetch,
            args=(server, query, pagerank_weight, results)
        )
        t.start()
        threads.append(t)
        # print(results)

    for t in threads:
        t.join()

    doc_scores = {}
    for hit in results:
        docid = hit['docid']
        score = hit['score']
        if docid not in doc_scores or score > doc_scores[docid]:
            doc_scores[docid] = score

    # Convert back to list and sort by score (descending),
    # then by docid (ascending)
    merged_results = [{'docid': docid, 'score': score}
                      for docid, score in doc_scores.items()]
    merged_results.sort(key=lambda x: (-x['score'], x['docid']))

    # Take top 10 results
    merged_results = merged_results[:10]

    # after getting hits,
    # we need to querry the search database
    # for title, summary, etc
    conn = sqlite3.connect(OUTPUT_DB)
    cur = conn.cursor()

    for hit in merged_results:
        docid = hit['docid']
        cur.execute("""
                    SELECT title, summary, url FROM documents
                    WHERE docid = ?
                    """, (docid, ))

        row = cur.fetchone()
        if row:
            title, summary, url = row
            hits.append({
                "docid": docid,
                "title": title,
                "summary": summary,
                "url": url})

    print(f"Results: {results}")

    return flask.render_template(
        "index.html",
        query=query,
        weight=weight,
        hits=hits
    )
