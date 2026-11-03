# Geç teslimat puanı ne kadar bozuyor, önce neyi denemeli?

Gerçek bir e-ticaret verisiyle (Olist, Brezilya) uçtan uca operasyon analizi. **[Raporu oku](https://ysfdurak.github.io/projeler/teslimat/)**

## Sonuç
Ocak 2017 - Ağustos 2018 arası 96.183 teslim edilmiş sipariş:

- Siparişlerin **%6,8**'i geç geldi; kötü puanların (1-2) **%32,6**'sı bu siparişlerden geliyor.
- Geç siparişlerin **%74,5**'inde değerlendirme kaydı ürün gelmeden oluşmuş. Bu kayıtlarda kötü puan %75,2; ürün geldikten sonrakilerde %25,1. Bu yüzden gecikmenin etkisini tek sayı değil, **16,3 ile 52,5 puan** aralığı olarak veriyorum.
- Geç teslimatın **%48,4**'ü üç ayda toplandı (Kasım 2017, Şubat ve Mart 2018).
- Bütün satıcılar kargoya zamanında verse bile geç teslimatın yalnız **%12,4**'ü kalkıyor.
- Denediğim erken uyarı kuralı işe yaramadı; raporda sonucuyla birlikte duruyor.

**Öneri sırası:** iletişim ve değerlendirme zamanı, yoğun dönem sözü (A/B testiyle), sık geciken satıcılar. Sözü genel olarak kısaltmak geç oranını %11,3'e çıkarır.

## Depo
| Yol | İçerik |
|---|---|
| `sql/` | Şema, analiz tablosu ve sorgular (PostgreSQL) |
| `python/analiz.py` | pandas ile bağımsız yeniden hesap, regresyon, erken uyarı denemesi |
| `sonuclar/` | Üretilen özet sonuçlar |
| `rapor/` | Sonuçlardan üretilen rapor sayfası |
| `powerbi/` | Power BI kurulumu, DAX ve kontrol sayıları |

## Çalıştırma
```sh
sh indir.sh                   # Ham veri Olist'in resmî deposundan, sabit sürümden
npm install
node sql/calistir.mjs         # PGlite: tarayıcı dışında çalışan gerçek PostgreSQL
pip install pandas numpy statsmodels
python python/analiz.py       # SQL ile 34 değeri karşılaştırır, fark varsa durur
python rapor/olustur.py
```

## Sınırlar
- Gözlemsel veri, neden-sonuç kanıtı değil. Maliyet, satış dönüşümü ve iade verisi yok.
- Brezilya, 2017-2018; sonuçlar bugüne veya başka ülkeye doğrudan taşınmaz.
- `review_creation_date` değerlendirme talebinin oluştuğu tarih olarak yorumlandı; şirkete doğrulatılmadı.
- En yoğun üç ay veriye bakılarak seçildi; tek yıllık örüntü mevsimsellik kanıtı değildir.
- Power BI adımları Desktop'ta denenmedi.
- Veri seçimi, analiz kodu ve metin yapay zekâyla (Claude) hazırlandı. Alan uzmanı incelemesi yok.

## Lisans
Kod MIT. Rapor ve özet sonuçlar CC BY-NC-SA 4.0, verinin Kaggle'daki lisansına uygun olarak. Ham veri bu depoya kopyalanmaz: [olist/work-at-olist-data](https://github.com/olist/work-at-olist-data).
