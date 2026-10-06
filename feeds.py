# feeds.py
# Çin & Tayvan haber kaynakları listesi.
#
# Her kaynak şu alanlara sahip:
#   name        -> Görünen isim
#   url         -> RSS feed URL'si
#   region      -> "china", "taiwan", "xinjiang", "hongkong", "international"
#   perspective -> "official"      (devlet/parti medyası)
#                  "independent"   (bağımsız/yerel özel medya)
#                  "diaspora"      (sürgün/diaspora medyası)
#                  "international" (yabancı basın)
#   lang        -> Yayın dili (en, zh, vs.)
#
# Yeni kaynak eklemek için listeye aynı formatta bir dict ekle yeterli.

FEEDS = [
    # ---------------- TAYVAN ----------------
    {
        "name": "Taipei Times",
        "url": "https://www.taipeitimes.com/xml/index.rss",
        "region": "taiwan",
        "perspective": "independent",
        "lang": "en",
    },
    {
        "name": "Focus Taiwan",
        "url": "https://focustaiwan.tw/rssnews",
        "region": "taiwan",
        "perspective": "independent",
        "lang": "en",
    },
    {
        "name": "Taiwan Today (MOFA)",
        "url": "https://www.taiwantoday.tw/rss",
        "region": "taiwan",
        "perspective": "official",
        "lang": "en",
    },
    {
        "name": "The News Lens",
        "url": "https://www.thenewslens.com/rss",
        "region": "taiwan",
        "perspective": "independent",
        "lang": "en",
    },
    {
        "name": "Newtalk",
        "url": "https://newtalk.tw/rss/all",
        "region": "taiwan",
        "perspective": "independent",
        "lang": "zh",
    },

    # ---------------- ÇİN (GENEL / RESMİ) ----------------
    {
        "name": "Xinhua News (English)",
        "url": "http://www.xinhuanet.com/english/rss/worldrss.xml",
        "region": "china",
        "perspective": "official",
        "lang": "en",
    },
    {
        "name": "China Daily",
        "url": "https://www.chinadaily.com.cn/rss/china_rss.xml",
        "region": "china",
        "perspective": "official",
        "lang": "en",
    },
    {
        "name": "Global Times",
        "url": "https://www.globaltimes.cn/rss/china.xml",
        "region": "china",
        "perspective": "official",
        "lang": "en",
    },
    {
        "name": "Ecns.cn (China News Service)",
        "url": "http://www.ecns.cn/rss/rss.xml",
        "region": "china",
        "perspective": "official",
        "lang": "en",
    },

    # ---------------- ÇİN (BAĞIMSIZ / YARI-BAĞIMSIZ) ----------------
    {
        "name": "China Digital Times",
        "url": "https://chinadigitaltimes.net/feed/",
        "region": "china",
        "perspective": "independent",
        "lang": "en",
    },
    {
        "name": "South China Morning Post",
        "url": "https://www.scmp.com/rss/91/feed",
        "region": "china",
        "perspective": "independent",
        "lang": "en",
    },

    # ---------------- XINJIANG (UYGUR BÖLGESİ) ----------------
    {
        "name": "Tianshannet (Xinjiang, English)",
        "url": "http://english.ts.cn/rss/rss.xml",
        "region": "xinjiang",
        "perspective": "official",
        "lang": "en",
    },
    {
        "name": "Radio Free Asia - Uyghur",
        "url": "https://www.rfa.org/english/news/uyghur/rss.xml",
        "region": "xinjiang",
        "perspective": "diaspora",
        "lang": "en",
    },

    # ---------------- HONG KONG ----------------
    {
        "name": "Hong Kong Free Press",
        "url": "https://hongkongfp.com/feed/",
        "region": "hongkong",
        "perspective": "independent",
        "lang": "en",
    },
    {
        "name": "RTHK News",
        "url": "https://news.rthk.hk/rthk/en/latest-news.htm?rss=1",
        "region": "hongkong",
        "perspective": "official",
        "lang": "en",
    },

    # ---------------- ULUSLARARASI (ÇİN/TAYVAN ÖZEL BÖLÜMLERİ) ----------------
    {
        "name": "BBC News - China",
        "url": "https://feeds.bbci.co.uk/news/world/asia/china/rss.xml",
        "region": "china",
        "perspective": "international",
        "lang": "en",
    },
    {
        "name": "The Diplomat - China Power",
        "url": "https://thediplomat.com/category/china-power/feed/",
        "region": "china",
        "perspective": "international",
        "lang": "en",
    },
]
