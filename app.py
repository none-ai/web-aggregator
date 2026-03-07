"""
Web Aggregator - Multi-source data fetcher
"""
from flask import Flask, jsonify
import requests
import feedparser

app = Flask(__name__)

DEFAULT_SOURCES = {
    'hn': 'https://news.ycombinator.com/rss',
    'reddit': 'https://www.reddit.com/r/programming/.rss',
}

@app.route('/api/fetch/<source>')
def fetch_source(source):
    if source not in DEFAULT_SOURCES:
        return jsonify({"error": "Unknown source"}), 404
    
    try:
        feed = feedparser.parse(DEFAULT_SOURCES[source])
        entries = []
        for entry in feed.entries[:10]:
            entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            })
        return jsonify({"source": source, "entries": entries})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sources')
def sources():
    return jsonify({"sources": list(DEFAULT_SOURCES.keys())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
