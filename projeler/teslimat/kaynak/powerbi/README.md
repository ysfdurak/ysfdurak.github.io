# Power BI raporunu kurma

`.pbix` dosyası bu depoda yok. Power BI Desktop bu projeyi hazırlayan ortamda çalıştırılamadığı için **aşağıdaki DAX ve sayfa planı Desktop'ta denenmedi**. Kendi bilgisayarında kurup sayıları aşağıdaki kontrol tablosuyla karşılaştır, sonra `.pbix` ve ekran görüntüsünü depoya ekle.

## Veri
`sh indir.sh`, `npm install` ve `node sql/calistir.mjs` komutları `powerbi/teslimat_mart.csv` dosyasını üretir (sipariş başına bir satır). Power BI'da **Veri al > Metin/CSV** ile yükle. `siparis_tarihi` tarih, `tutar` ve `kargo` ondalık olsun; ondalık ayırıcı noktadır, gerekirse yerel ayarı "İngilizce (ABD)" seç. Tarih tablosunu `CALENDAR(DATE(2017,1,1), DATE(2018,8,31))` ile kur ve `siparis_tarihi` sütununa bağla.

## Ölçüler
```dax
Sipariş = COUNTROWS(teslimat_mart)
Geç Sipariş = SUM(teslimat_mart[gec])
Geç Oranı = DIVIDE([Geç Sipariş], [Sipariş])
Puanlı Sipariş = COUNT(teslimat_mart[kotu])
Kötü Puan = SUM(teslimat_mart[kotu])
Kötü Puan Oranı = DIVIDE([Kötü Puan], [Puanlı Sipariş])
Geçlerin Kötü Puan Payı = DIVIDE(CALCULATE([Kötü Puan], teslimat_mart[gec] = 1), [Kötü Puan])
Ürün Gelmeden Oranı = DIVIDE(CALCULATE(SUM(teslimat_mart[anket_once]), teslimat_mart[gec] = 1), CALCULATE([Puanlı Sipariş], teslimat_mart[gec] = 1))
Taşıma Medyan Gün = MEDIAN(teslimat_mart[tasima_gun])
```

## Sayfalar
1. **Karar:** dört kart (Sipariş, Geç Oranı, Kötü Puan Oranı, Geçlerin Kötü Puan Payı), `gecikme_gun` gruplarına göre Kötü Puan Oranı.
2. **Ne zaman, nerede:** `ay` için Geç Oranı sütun grafiği, `alici_eyalet` için Geç Sipariş çubuk grafiği, ay ve eyalet dilimleyicisi.
3. **Satıcı:** `satici_gec` için Geç Oranı, en çok geç siparişli 20 satıcı tablosu.

## Kontrol
| Ölçü | Filtresiz beklenen |
|---|---|
| Sipariş | 96.183 |
| Geç Sipariş | 6.530 |
| Geç Oranı | %6,8 |
| Puanlı Sipariş | 95.540 |
| Kötü Puan | 12.218 |
| Geçlerin Kötü Puan Payı | %32,6 |
