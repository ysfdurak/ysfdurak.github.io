-- Analiz tablosu: sipariş başına bir satır.
-- Kapsam: teslim edilmiş, taşıyıcı ve müşteri tarihi tutarlı, Ocak 2017 - Ağustos 2018 arası siparişler.
-- 2016 ve Eylül 2018 sonrası çok az sipariş içerdiği için dışarıda.
CREATE TABLE mart AS
WITH kalem AS (
  SELECT order_id,
         MAX(shipping_limit_date) AS teslim_son_tarih,
         COUNT(*) AS kalem_sayisi,
         COUNT(DISTINCT seller_id) AS satici_sayisi,
         SUM(price) AS tutar,
         SUM(freight_value) AS kargo,
         (ARRAY_AGG(seller_id ORDER BY order_item_id))[1] AS satici
  FROM order_items GROUP BY order_id
), yorum AS (
  -- Birden çok yorumu olan 547 siparişte en son cevaplanan yorum geçerli sayılır.
  SELECT DISTINCT ON (order_id) order_id, review_score, review_creation_date
  FROM order_reviews ORDER BY order_id, review_answer_timestamp DESC, review_id DESC
)
SELECT o.order_id,
       o.order_purchase_timestamp::date AS siparis_tarihi,
       to_char(o.order_purchase_timestamp, 'YYYY-MM') AS ay,
       c.customer_state AS alici_eyalet,
       s.seller_state AS satici_eyalet,
       k.satici, k.kalem_sayisi, k.satici_sayisi, k.tutar, k.kargo,
       o.order_delivered_customer_date::date - o.order_estimated_delivery_date::date AS gecikme_gun,
       o.order_delivered_customer_date::date > o.order_estimated_delivery_date::date AS gec,
       o.order_delivered_carrier_date > k.teslim_son_tarih AS satici_gec,
       GREATEST(o.order_delivered_carrier_date - k.teslim_son_tarih, interval '0') AS satici_asim,
       o.order_delivered_customer_date AS teslim_zamani,
       o.order_estimated_delivery_date AS soz_tarihi,
       EXTRACT(EPOCH FROM o.order_delivered_customer_date - o.order_delivered_carrier_date) / 86400 AS tasima_gun,
       y.review_score AS puan,
       CASE WHEN y.review_score IS NULL THEN NULL ELSE y.review_score <= 2 END AS kotu,
       CASE WHEN y.review_score IS NULL THEN NULL ELSE y.review_creation_date < o.order_delivered_customer_date::date END AS anket_once
FROM orders o
JOIN kalem k USING (order_id)
JOIN customers c USING (customer_id)
JOIN sellers s ON s.seller_id = k.satici
LEFT JOIN yorum y USING (order_id)
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_delivered_carrier_date IS NOT NULL
  AND o.order_delivered_customer_date >= o.order_delivered_carrier_date
  AND o.order_purchase_timestamp >= '2017-01-01' AND o.order_purchase_timestamp < '2018-09-01';
