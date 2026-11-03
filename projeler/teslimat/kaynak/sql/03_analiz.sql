-- @ozet
SELECT COUNT(*) AS siparis, SUM(gec::int) AS gec, SUM(kotu::int) AS kotu, SUM((kotu AND gec)::int) AS kotu_gec, COUNT(kotu) AS puanli FROM mart;
-- @dort_hucre: Gecikme ve anket zamanına göre kötü puan
SELECT gec, anket_once, COUNT(*) AS n, SUM(kotu::int) AS kotu FROM mart WHERE kotu IS NOT NULL GROUP BY 1, 2 ORDER BY 1, 2;
-- @gecikme_kova
SELECT CASE WHEN gecikme_gun <= -15 THEN 'a. 15+ gün erken' WHEN gecikme_gun <= -8 THEN 'b. 8-14 gün erken' WHEN gecikme_gun <= -1 THEN 'c. 1-7 gün erken' WHEN gecikme_gun = 0 THEN 'd. Tam günü' WHEN gecikme_gun <= 3 THEN 'e. 1-3 gün geç' WHEN gecikme_gun <= 7 THEN 'f. 4-7 gün geç' WHEN gecikme_gun <= 14 THEN 'g. 8-14 gün geç' ELSE 'h. 15+ gün geç' END AS kova,
       COUNT(kotu) AS n, SUM(kotu::int) AS kotu, SUM(anket_once::int) AS anket_once FROM mart GROUP BY 1 ORDER BY 1;
-- @ay
SELECT ay, COUNT(*) AS n, SUM(gec::int) AS gec, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tasima_gun) AS tasima_medyan, SUM(satici_gec::int) AS satici_gec FROM mart GROUP BY 1 ORDER BY 1;
-- @eyalet: Alıcı eyaletine göre
SELECT alici_eyalet, COUNT(*) AS n, SUM(gec::int) AS gec, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tasima_gun) AS tasima_medyan FROM mart GROUP BY 1 ORDER BY gec DESC, 1;
-- @satici_etkisi
SELECT satici_gec, COUNT(*) AS n, SUM(gec::int) AS gec FROM mart GROUP BY 1 ORDER BY 1;
-- @senaryo: Her senaryoda gecikme, sözlü tarihe göre yeniden hesaplanır
SELECT
  SUM(((teslim_zamani - satici_asim)::date > soz_tarihi::date)::int) AS satici_zamaninda,
  SUM((gecikme_gun - CASE WHEN ay IN ('2017-11','2018-02','2018-03') THEN 3 ELSE 0 END > 0)::int) AS yogun_ay_3_gun,
  SUM((gecikme_gun - CASE WHEN alici_eyalet = 'RJ' THEN 3 ELSE 0 END > 0)::int) AS rj_3_gun,
  SUM((gecikme_gun + 3 > 0)::int) AS soz_3_gun_kisa,
  SUM((gecikme_gun + 5 > 0)::int) AS soz_5_gun_kisa
FROM mart;
-- @kapsam_siparis: Kapsam dışı kalanlar
SELECT order_status, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC;
-- @yogun_paylar
SELECT SUM((ay IN ('2017-11','2018-02','2018-03'))::int) AS yogun_siparis, SUM((gec AND ay IN ('2017-11','2018-02','2018-03'))::int) AS yogun_gec FROM mart;
