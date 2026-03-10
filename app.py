"""
Web Aggregator - Multi-source data fetcher
"""
import time
from flask import Flask, jsonify
import requests
import feedparser

__version__ = "1.0.0"

app = Flask(__name__)

# 简单内存缓存
_cache = {}
_cache_ttl = 300  # 缓存5分钟

DEFAULT_SOURCES = {
    'hn': 'https://news.ycombinator.com/rss',
    'reddit': 'https://www.reddit.com/r/programming/.rss',
}

@app.route('/api/fetch/<source>')
def fetch_source(source):
    if source not in DEFAULT_SOURCES:
        return jsonify({"error": "Unknown source"}), 404
    
    # 检查缓存
    now = time.time()
    if source in _cache:
        cached_data, cached_time = _cache[source]
        if now - cached_time < _cache_ttl:
            return jsonify({"source": source, "entries": cached_data, "cached": True})
    
    try:
        feed = feedparser.parse(DEFAULT_SOURCES[source])
        entries = []
        for entry in feed.entries[:10]:
            entries.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            })
        # 更新缓存
        _cache[source] = (entries, now)
        return jsonify({"source": source, "entries": entries, "cached": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sources')
def sources():
    return jsonify({"sources": list(DEFAULT_SOURCES.keys())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8006)
