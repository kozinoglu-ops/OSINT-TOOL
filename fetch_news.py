#!/usr/bin/env python3
"""
fetch_news.py
Çin & Tayvan gündemini takip etmek için basit bir RSS toplama aracı.

Kullanım:
    python3 fetch_news.py                # tüm kaynakları çek, DB'ye kaydet, HTML özet üret
    python3 fetch_news.py --region taiwan # sadece belirli bir bölgeyi çek
    python3 fetch_news.py --days 3        # son 3 günün özetini HTML'e yaz (DB'den, indirmeden)

Gereksinimler:
    pip install feedparser
"""

import argparse
import html
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import feedparser
except ImportError:
    sys.exit("Önce 'pip install feedparser' ile kütüphaneyi kurman gerekiyor.")

from feeds import FEEDS

DB_PATH = Path(__file__).parent / "news.db"
OUTPUT_HTML = Path(__file__).parent / "summary.html"


# ---------------------------------------------------------------------------
# Veritabanı
# ---------------------------------------------------------------------------

def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            region TEXT NOT NULL,
            perspective TEXT NOT NULL,
            published TEXT,
            fetched_at TEXT NOT NULL
        )
    """)
    conn.commit()


def save_article(conn: sqlite3.Connection, article: dict) -> bool:
    """Yeni makaleyi kaydeder. Zaten varsa (link tekrarı) False döner."""
    try:
        conn.execute(
            """INSERT INTO articles (link, title, source, region, perspective, published, fetched_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                article["link"],
                article["title"],
                article["source"],
                article["region"],
                article["perspective"],
                article["published"],
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Bu link zaten DB'de var -> duplicate, atla
        return False


# ---------------------------------------------------------------------------
# RSS çekme
# ---------------------------------------------------------------------------

def fetch_feed(feed_info: dict) -> list[dict]:
    """Tek bir RSS kaynağından makaleleri çeker. Hata olursa boş liste döner."""
    articles = []
    try:
        parsed = feedparser.parse(feed_info["url"])

        if parsed.bozo and not parsed.entries:
            print(f"  ⚠ {feed_info['name']}: feed okunamadı veya bozuk ({parsed.get('bozo_exception', 'bilinmeyen hata')})")
            return []

        for entry in parsed.entries:
            title = entry.get("title", "(başlıksız)")
            link = entry.get("link", "")
            published = entry.get("published", entry.get("updated", ""))

            if not link:
                continue

            articles.append({
                "title": title,
                "link": link,
                "published": published,
                "source": feed_info["name"],
                "region": feed_info["region"],
                "perspective": feed_info["perspective"],
            })

    except Exception as e:
        print(f"  ✗ {feed_info['name']}: hata -> {e}")

    return articles


def fetch_all(region_filter: str | None = None) -> tuple[int, int]:
    """Tüm (veya filtrelenmiş) kaynakları çeker, DB'ye kaydeder.
    Dönüş: (toplam_bulunan, yeni_eklenen)
    """
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    total_found = 0
    total_new = 0

    feeds_to_fetch = FEEDS
    if region_filter:
        feeds_to_fetch = [f for f in FEEDS if f["region"] == region_filter]
        if not feeds_to_fetch:
            print(f"'{region_filter}' bölgesi için tanımlı kaynak yok. "
                  f"Mevcut bölgeler: {sorted(set(f['region'] for f in FEEDS))}")
            return (0, 0)

    print(f"{len(feeds_to_fetch)} kaynak taranıyor...\n")

    for feed_info in feeds_to_fetch:
        print(f"→ {feed_info['name']} ({feed_info['region']} / {feed_info['perspective']})")
        articles = fetch_feed(feed_info)
        total_found += len(articles)

        new_count = 0
        for article in articles:
            if save_article(conn, article):
                new_count += 1
        total_new += new_count

        print(f"  {len(articles)} makale bulundu, {new_count} yeni")

    conn.close()
    return (total_found, total_new)


# ---------------------------------------------------------------------------
# HTML özet üretimi
# ---------------------------------------------------------------------------

PERSPECTIVE_LABELS = {
    "official": "🏛️ Resmi/Devlet Medyası",
    "independent": "📰 Bağımsız Medya",
    "diaspora": "🗣️ Diaspora/Sürgün Medyası",
    "international": "🌐 Uluslararası Basın",
}

REGION_LABELS = {
    "china": "Çin (genel)",
    "taiwan": "Tayvan",
    "xinjiang": "Xinjiang (Uygur Bölgesi)",
    "hongkong": "Hong Kong",
    "international": "Uluslararası",
}


def generate_html_summary(days: int = 1) -> None:
    """Son N günün makalelerini bölge + perspektife göre gruplayıp HTML üretir."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    rows = conn.execute(
        """SELECT * FROM articles WHERE fetched_at >= ? ORDER BY region, perspective, fetched_at DESC""",
        (cutoff,),
    ).fetchall()
    conn.close()

    if not rows:
        print("Bu tarih aralığında kayıtlı makale yok. Önce 'python3 fetch_news.py' ile veri çek.")
        return

    # region -> perspective -> [articles]
    grouped: dict[str, dict[str, list]] = {}
    for row in rows:
        grouped.setdefault(row["region"], {}).setdefault(row["perspective"], []).append(row)

    parts = [
        "<!DOCTYPE html><html lang='tr'><head><meta charset='utf-8'>",
        "<title>Çin & Tayvan Gündem Özeti</title>",
        "<style>",
        "body{font-family:system-ui,-apple-system,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;background:#f7f7f7;color:#1a1a1a}",
        "h1{font-size:1.6rem} h2{margin-top:2.5rem;border-bottom:2px solid #333;padding-bottom:.3rem}",
        "h3{color:#555;font-size:1rem;margin-top:1.5rem}",
        ".article{background:#fff;border-radius:6px;padding:.7rem 1rem;margin:.5rem 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}",
        ".article a{color:#1a4fa0;text-decoration:none;font-weight:600}",
        ".article a:hover{text-decoration:underline}",
        ".meta{color:#777;font-size:.8rem;margin-top:.2rem}",
        "</style></head><body>",
        f"<h1>Çin & Tayvan Gündem Özeti</h1>",
        f"<p>Son {days} gün · Üretim zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>",
    ]

    for region in sorted(grouped.keys()):
        parts.append(f"<h2>{html.escape(REGION_LABELS.get(region, region))}</h2>")
        for perspective in sorted(grouped[region].keys()):
            articles = grouped[region][perspective]
            parts.append(f"<h3>{html.escape(PERSPECTIVE_LABELS.get(perspective, perspective))} ({len(articles)})</h3>")
            for a in articles:
                parts.append(
                    f"<div class='article'>"
                    f"<a href='{html.escape(a['link'])}' target='_blank' rel='noopener'>{html.escape(a['title'])}</a>"
                    f"<div class='meta'>{html.escape(a['source'])}"
                    f"{' · ' + html.escape(a['published']) if a['published'] else ''}</div>"
                    f"</div>"
                )

    parts.append("</body></html>")

    OUTPUT_HTML.write_text("\n".join(parts), encoding="utf-8")
    print(f"\nÖzet oluşturuldu: {OUTPUT_HTML}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Çin & Tayvan RSS haber toplayıcı")
    parser.add_argument("--region", help="Sadece belirli bir bölgeyi çek (china, taiwan, xinjiang, hongkong)")
    parser.add_argument("--days", type=int, default=1, help="HTML özetine kaç günlük veri dahil edilsin (varsayılan: 1)")
    parser.add_argument("--summary-only", action="store_true", help="Yeni veri çekme, sadece mevcut DB'den HTML üret")
    args = parser.parse_args()

    if not args.summary_only:
        total_found, total_new = fetch_all(region_filter=args.region)
        print(f"\nToplam: {total_found} makale tarandı, {total_new} yeni kayıt eklendi.")

    generate_html_summary(days=args.days)


if __name__ == "__main__":
    main()
