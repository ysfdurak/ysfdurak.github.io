# Uçtan uca depo vakası: kaynak

Kesit'in dört uygulamasını tek bir iş sorusunda birleştiren vakanın verisi, beklenen sonuçları ve sayfa üreteci.

**Soru:** Anadolu Market Gebze deposunda Ekim 2026'da raf düzeni değişti. Satır başına toplama süresi kısaldı mı, kısaldıysa yeni düzeni diğer depolara yaymaya yeter mi? Yaymanın maliyeti satır başına en az **4 sn** kazançla geri dönüyor.

| Adım | Sayfa | Ne yapılır | Motor | CI denetimi |
|---|---|---|---|---|
| 1 SQL | `/kesit-sql/vaka/depo/` | 2.425 ham satırı `toplama_temiz` görünümüne indir (18 boş, 20 aralık dışı, 25 çift okutma, 70 yazım farkı), düzene göre özetle | sql.js (`vendor/sql-asm.js`) | `kesit-sql/tests/vaka-depo.cjs` |
| 2 Python | `/kesit-python/vaka/depo/` | 2.362 temiz satırı pandas ile denetle: temizlik, vardiya karışımı (%60/%40 iki dönemde aynı), vardiya içi fark | Pyodide (`pyworker.js`) | `kesit-python/tests/vaka_depo.py` |
| 3 Power BI | `/kesit-powerbi/vaka/depo/` | `Kazanc sn` ve `Kazanc %` ölçülerini yaz; kartlar, bölge grafiği, vardiya matrisi | Kesit DAX motoru (`vaka/depo/dax.js`, `kesit.js` kopyası) | `kesit-powerbi/tests/vaka-depo.cjs` |
| 4 İstatistik | `/kesit-istatistik/vaka/depo/` | Welch t-testi, güven aralığı, eşikle karşılaştırma | `docs/analysis-engine.js` (tP, tInv) | `kesit-istatistik/verify-vaka.cjs` |

**Beklenen sonuç:** eski 42,44 sn, yeni 41,17 sn, kazanç 1,26 sn (%2,98). Welch t = 2,11, p = 0,035; %95 güven aralığı 0,09–2,44 sn. İstatistiksel fark var, ama üst sınır 4 sn eşiğinin altında: **operasyonel olarak yeterli değil.** 4 sn'lik farkı %80 güçle görmek için grup başına yaklaşık 210 satır yeterdi; sorun örneklem değil, farkın küçüklüğü.

**İkinci örnek (İstatistik sayfası, İzmir deposu):** aynı görünen kazanç (toplamda 1,30 sn, p = 0,023), ama Ekim'de yavaş gece vardiyasının payı %45'ten %25'e indi. Vardiya içinde fark yok (gündüz 0,02 sn, gece −0,15 sn; iki aralık da sıfırı içerir); vardiya karışımı sabit tutulunca fark −0,04 sn. Öğrenci "ortalama süre düştü" (doğru) ile "raf değişikliği düşüşe yol açtı" (bu veri desteklemiyor) arasındaki farkı yazar, sonra uzman değerlendirmesi açılır. Veri `ornek2_izmir.csv`, beklenen değerler `beklenen.json › istatistik2` (SciPy); `kesit-istatistik/verify-vaka.cjs` tarayıcı motoruyla aynı değerleri denetler. İlk veri seti ve beklenenleri değişmedi (ayrı tohum).

## Nasıl doğrulandı?
- `uret.py` veriyi tohumlu üreteçle oluşturur ve beklenen sonuçları üç bağımsız yoldan hesaplar: SQLite (adım 1), pandas (adım 2–3), SciPy `ttest_ind(equal_var=False)` (adım 4).
- Aynı sayılar tarayıcıdaki motorlarla tekrar hesaplanır ve karşılaştırılır: Kesit DAX motoru pandas ile 1e-12, Kesit İstatistik motoru SciPy ile 1e-11 düzeyinde aynı.
- Dört sayfa Chrome'da 390 ve 1366 px'te baştan sona çözüldü (Python adımı gerçek Pyodide 0.27.8 + pandas ile); axe hatası yok, en küçük yazı 12 px.

## Adımlar arası bağ
- 1. adımı çözen kişinin `toplama_temiz` tablosu CSV olarak `localStorage['kesit.vaka.depo.csv']` içine yazılır. 2–4. adımlarda iki açık seçenek var: **Kendi çıktımla devam et** (kaydedilen tablo; kaynağı, satır sayısı ve kayıt zamanı yazılır) ve **Örnek veriyle dene** (1. adımın beklenen çıktısı; ekranda "senin SQL çalışmana ait değil" notu çıkar). 1. adımı çözmeyen kişi yalnızca örnek veriyle devam edebilir.
- Ortak ilerleme `localStorage['kesit.vaka.depo']` içindedir (dört uygulama aynı alan adında). Her adım hangi veriyle çözüldüğünü (`kaynak: kendi | ornek`) kaydeder. Ana sayfanın başındaki düğme ilk gelene "Depo vakasına başla", dönene "Kaldığım adıma git" der.
- 1. adımda beklenen sonuç kapalı başlar (önce keşif sorguları). 2. adımda "Bir kaydı incele" paneli elenen 63 ve düzeltilen 70 satırın her biri için çalışan kuralı, nedenini ve sonucunu gösterir (`incele_listesi()` üretir, sayıları `beklenen.json` ile denetler).
- 4. adım üç soruyu ayırır: ne gözlendi, hedef karşılandı mı, fark yeni düzene bağlanabilir mi. Üçüncüsünü test cevaplamaz: öğrenci kararını yazar, kaydedince uzman değerlendirmesi ve sözcük temelli öz değerlendirme açılır (p değeri ile etki büyüklüğü ayrı: ASA 2016 bildirgesi).

## Değiştirmek
Dört depo yan yana klonlu olmalı (`kesit-sql`, `kesit-python`, `kesit-powerbi`, `kesit-istatistik`, `ysfdurak.github.io`).
```bash
cd ysfdurak.github.io/vaka/depo-kaynak
python3 uret.py       # veri + beklenen.json (pandas, scipy gerekir)
python3 sayfalar.py   # dört index.html, beklenen.json ve Power BI dax.js kopyası
```
Sonra her depoda testi çalıştır ve SQL, Python, Power BI depolarında `release-manifest.json` dosya özetlerini güncelle (CI denetler). **Kaynak dalları da güncelle:** `kesit-sql` ve `kesit-python` depolarının `kaynak` dalında `vaka/depo/index.html`, `kesit-powerbi`'nin `kaynak` dalında `app/build/gh/static/vaka/depo/index.html` kopyası durur; derleme `main`'i bu kopyalardan üretir. Üretilen sayfaları oraya da kopyala, yoksa sonraki derleme eski sayfayı geri getirir. Sayfaları elle düzenleme: üreteç üzerine yazar.
