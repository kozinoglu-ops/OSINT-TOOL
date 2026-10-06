# Çin & Tayvan Gündem Takip Aracı

Kişisel kullanım için basit bir RSS toplama aracı. Tayvan, Çin, Xinjiang ve
Hong Kong'dan haber kaynaklarını çeker, kaynağın **perspektifini** (resmi /
bağımsız / diaspora / uluslararası) etiketler, tekrarları önler ve okunabilir
bir HTML özeti üretir.

## Kurulum

```bash
pip install feedparser
```

Python 3.10+ gerekir (`str | None` gibi tip belirteçleri kullanılıyor).
Daha eski bir Python kullanıyorsan `fetch_news.py` içindeki `str | None` ve
`list[dict]` tip belirteçlerini `Optional[str]` ve `List[dict]` ile
değiştirmen gerekir (`from typing import Optional, List` ekleyerek).

## Kullanım

```bash
# Tüm kaynakları çek ve son 1 günün özetini üret
python3 fetch_news.py

# Sadece Tayvan kaynaklarını çek
python3 fetch_news.py --region taiwan

# Son 7 günün özetini üret (yeniden veri çekmeden, DB'den)
python3 fetch_news.py --summary-only --days 7
```

Çalıştırdıktan sonra `summary.html` dosyasını tarayıcında aç — bölgeye ve
kaynağın perspektifine göre gruplanmış haber listesini göreceksin.

## Dosyalar

- `feeds.py` — Kaynak listesi (isim, RSS URL, bölge, perspektif, dil).
  Yeni kaynak eklemek istersen buraya aynı formatta bir satır eklemen yeterli.
- `fetch_news.py` — Ana script: RSS çeker, `news.db` (SQLite) içine kaydeder,
  `summary.html` üretir.
- `news.db` — Otomatik oluşur, tüm geçmiş makaleleri tutar (link bazlı
  tekilleştirme yapılır, aynı haber iki kez eklenmez).

## Önemli notlar

1. **RSS URL'leri zamanla değişebilir/kırılabilir.** Script bir kaynağı
   çekemezse hatayı ekrana yazıp diğerlerine devam eder, durmaz. Bir kaynak
   sürekli hata veriyorsa `feeds.py` içinde o kaynağın güncel RSS adresini
   sitenin kendisinden kontrol et.
2. **Perspektif etiketleri benim değerlendirmem**, mutlak doğru değil —
   zamanla kendi gözlemlerine göre `feeds.py` içindeki etiketleri
   güncelleyebilirsin.
3. Bunu **cron** ile otomatikleştirebilirsin (örn. her sabah 08:00'de
   otomatik çalıştırıp güncel özeti hazır bulmak için):
   ```bash
   crontab -e
   # şu satırı ekle:
   0 8 * * * cd /path/to/china-taiwan-news && python3 fetch_news.py
   ```

## Sonraki adımlar (istersen genişletebileceğin yönler)

- Çince kaynaklar için otomatik çeviri (örn. `deep-translator` kütüphanesi)
- Anahtar kelime bazlı filtreleme/vurgulama (örn. belirli bir konu geçtiğinde)
- E-posta veya Telegram bot ile günlük özet gönderimi
- Basit bir web arayüzü (Flask) ile terminalden bağımsız erişim
