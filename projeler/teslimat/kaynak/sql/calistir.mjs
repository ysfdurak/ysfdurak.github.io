// Gerçek PostgreSQL (PGlite) üzerinde: ham veri yüklenir, analiz tablosu kurulur, sorgular sonuclar/sql.json'a yazılır.
import { PGlite } from '@electric-sql/pglite';
import fs from 'node:fs';
const db = new PGlite();
await db.exec(fs.readFileSync('sql/01_sema.sql', 'utf8'));
const dosyalar = { orders: 'orders', order_items: 'order_items', order_reviews: 'order_reviews', customers: 'customers', sellers: 'sellers' };
for (const [t, f] of Object.entries(dosyalar)) {
  const blob = new Blob([fs.readFileSync(`veri/datasets/olist_${f}_dataset.csv`)]);
  await db.query(`COPY ${t} FROM '/dev/blob' WITH (FORMAT csv, HEADER true)`, [], { blob });
  console.log(t, (await db.query(`SELECT COUNT(*)::int AS n FROM ${t}`)).rows[0].n);
}
await db.exec(fs.readFileSync('sql/02_mart.sql', 'utf8'));
const sonuc = {};
for (const parca of fs.readFileSync('sql/03_analiz.sql', 'utf8').split(/^-- @/m).slice(1)) {
  const ad = parca.split(/[\s:]/)[0], sql = parca.slice(parca.indexOf('\n') + 1);
  const r = await db.query(sql);
  sonuc[ad] = r.rows.map(x => Object.fromEntries(Object.entries(x).map(([k, v]) => [k, typeof v === 'bigint' ? Number(v) : v])));
}
fs.mkdirSync('sonuclar', { recursive: true });
fs.writeFileSync('sonuclar/sql.json', JSON.stringify(sonuc, null, 1));
const cikis = await db.query(`COPY (SELECT order_id, siparis_tarihi, ay, alici_eyalet, satici_eyalet, satici, kalem_sayisi, satici_sayisi, tutar, kargo, gecikme_gun, gec::int AS gec, satici_gec::int AS satici_gec, ROUND(tasima_gun::numeric, 2) AS tasima_gun, puan, kotu::int AS kotu, anket_once::int AS anket_once FROM mart ORDER BY order_id) TO '/dev/blob' WITH (FORMAT csv, HEADER true)`);
fs.mkdirSync('powerbi', { recursive: true });
fs.writeFileSync('powerbi/teslimat_mart.csv', Buffer.from(await cikis.blob.arrayBuffer()));
console.log(JSON.stringify(sonuc.ozet));
