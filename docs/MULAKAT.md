# Mülakatta sorulabilecek sorular · Kesit (SQL, Power BI, Python, İstatistik)

Bu kart, projeyi kendi ağzınla anlatabilmen için. Cevaplar kısa tutuldu; ayrıntısı belirtilen belgede. Kod yapay zekâ (Claude) ile yazıldı; kapsam, öncelik ve aşağıdaki kararlar senin. Bunu saklama, açıkça söyle: "Ürünü ve kararları ben belirledim, kodu yapay zekâyla yazdım, her kararın nedenini anlatabilirim."

**1. Bu proje ne yapıyor?**
SQL, Power BI, Python ve istatistiği Türkçe, kurulum ve hesap olmadan tarayıcıda öğreten dört uygulama ve onları birleştiren bir depo vakası.

**2. Kurulumsuz nasıl çalışıyor?**
SQL için tarayıcıda SQLite (sql.js), Python için Pyodide; her şey tarayıcıda, ilerleme cihazda kalıyor.

**3. Uçtan uca depo vakası ne?**
Tek bir depo sorusu dört adımda çözülüyor: SQL'de görünüm, Python'da temizlik ve kayıt incelemesi, Power BI'da gösterge, istatistikte 'farkı yeni düzene bağlayabilir miyiz' kararı.

**4. Önceki adımın çıktısı sonrakine geçiyor mu?**
Evet; kendi çıktınla devam edebiliyorsun. Çıktında gereken sütun eksikse hangi sütunun eksik olduğu ve ilk adıma dönüş bağlantısı gösteriliyor.

**5. İstatistik adımında ne öğretiyorsun?**
Ne gözlendi, hedef karşılandı mı ve fark nedensellik mi: üç ayrı soru. Kararını yazmadan uzman değerlendirmesi açılmıyor.

**6. Kaç içerik var?**
Kesit SQL'de 295 ders, 1.944 alıştırma, 578 pratik görevi, altı SQL türü ve 21 öğrenme yolu.

**7. Tutarlılığı nasıl koruyorsun?**
Sürüm bildirimi dosya özetleriyle tutuluyor; CI özetler ve 'kaynak' dalındaki kopya main ile aynı değilse duruyor (kopya bir kez bayatlamıştı).

**8. Kişisel veri?**
Toplanmıyor; ilerleme yalnız tarayıcıda, istenirse dosyaya yedekleniyor.

**9. Kimin için?**
Veri analisti, iş zekâsı, veri mühendisi gibi rollere hazırlanan ya da işinde veriyle çalışan Türkçe konuşanlar.

**10. Neyi farklı yapardın?**
'Kaynak' dalına kopyalamayı baştan otomatikleştirirdim.


## Bu projede verdiğim kararlar (sorun → karar → bedel)

- **Kendi çıktınla devam:** Gerçekçi akış için → eksik sütun kontrolü gerekiyor → kullanıcı ilk adıma dönmek zorunda kalabiliyor.
- **Karar yazmadan uzman görüşü yok:** Kopyalamayı önlemek için → en az 60 karakter → bazı kullanıcılar kısa cevap verip geçmek istiyor.

---
Son güncelleme: 19 Kasım 2026.
