"""SQL sonuçlarını pandas ile bağımsız olarak yeniden hesaplar, sağlamlık testlerini ve erken uyarı denemesini çalıştırır.
Kullanım: python python/analiz.py  (önce: sh indir.sh, node sql/calistir.mjs)"""
import json
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

D = 'veri/datasets/olist_'
PU, ON, CA, MU, ES = ('order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
                      'order_delivered_customer_date', 'order_estimated_delivery_date')
o = pd.read_csv(D + 'orders_dataset.csv', parse_dates=[PU, ON, CA, MU, ES])
i = pd.read_csv(D + 'order_items_dataset.csv', parse_dates=['shipping_limit_date']).sort_values(['order_id', 'order_item_id'])
r = pd.read_csv(D + 'order_reviews_dataset.csv', parse_dates=['review_creation_date', 'review_answer_timestamp'])
c = pd.read_csv(D + 'customers_dataset.csv')
s = pd.read_csv(D + 'sellers_dataset.csv')
p = pd.read_csv(D + 'products_dataset.csv')

m = o[(o.order_status == 'delivered') & o[MU].notna() & o[CA].notna() & (o[MU] >= o[CA])
      & (o[PU] >= '2017-01-01') & (o[PU] < '2018-09-01')].copy()
k = i.groupby('order_id').agg(son=('shipping_limit_date', 'max'), kalem=('order_item_id', 'size'), satici_n=('seller_id', 'nunique'),
                              satici=('seller_id', 'first'), urun=('product_id', 'first'), tutar=('price', 'sum')).reset_index()
y = r.sort_values(['order_id', 'review_answer_timestamp', 'review_id']).groupby('order_id').tail(1)[['order_id', 'review_score', 'review_creation_date']]
m = (m.merge(k, on='order_id').merge(c[['customer_id', 'customer_state']], on='customer_id')
     .merge(s[['seller_id', 'seller_state']], left_on='satici', right_on='seller_id')
     .merge(p[['product_id', 'product_category_name']], left_on='urun', right_on='product_id', how='left')
     .merge(y, on='order_id', how='left'))
m['t'] = m[MU].dt.normalize()
m['gun'] = (m.t - m[ES].dt.normalize()).dt.days
m['gec'] = m.gun > 0
m['kotu'] = (m.review_score <= 2).where(m.review_score.notna())
m['once'] = (m.review_creation_date < m.t).where(m.review_score.notna())
m['ay'] = m[PU].dt.strftime('%Y-%m')
m['asim'] = (m[CA] - m.son).clip(lower=pd.Timedelta(0))
m['tasima'] = (m[MU] - m[CA]).dt.total_seconds() / 86400
YOG = ['2017-11', '2018-02', '2018-03']
pu = m[m.kotu.notna()]

# 1. SQL ile çapraz kontrol
sql = json.load(open('sonuclar/sql.json', encoding='utf-8'))
sen = sql['senaryo'][0]
beklenen = {
    'siparis': (sql['ozet'][0]['siparis'], len(m)),
    'gec': (sql['ozet'][0]['gec'], int(m.gec.sum())),
    'kotu': (sql['ozet'][0]['kotu'], int(pu.kotu.sum())),
    'kotu_gec': (sql['ozet'][0]['kotu_gec'], int(pu[pu.gec].kotu.sum())),
    'satici_zamaninda': (sen['satici_zamaninda'], int(((m[MU] - m.asim).dt.normalize() > m[ES].dt.normalize()).sum())),
    'yogun_ay_3_gun': (sen['yogun_ay_3_gun'], int(((m.gun - 3 * m.ay.isin(YOG)) > 0).sum())),
    'rj_3_gun': (sen['rj_3_gun'], int(((m.gun - 3 * (m.customer_state == 'RJ')) > 0).sum())),
    'soz_3_gun_kisa': (sen['soz_3_gun_kisa'], int(((m.gun + 3) > 0).sum())),
    'soz_5_gun_kisa': (sen['soz_5_gun_kisa'], int(((m.gun + 5) > 0).sum())),
    'yogun_gec': (sql['yogun_paylar'][0]['yogun_gec'], int(m[m.ay.isin(YOG)].gec.sum())),
}
for h in sql['dort_hucre']:
    g = pu[(pu.gec == h['gec']) & (pu.once == h['anket_once'])]
    beklenen[f"hucre_{h['gec']}_{h['anket_once']}"] = (h['kotu'], int(g.kotu.sum()))
for a in sql['ay']:
    beklenen['ay_' + a['ay']] = (a['gec'], int(m[m.ay == a['ay']].gec.sum()))
fark = {k: v for k, v in beklenen.items() if v[0] != v[1]}
print(f'SQL ve pandas: {len(beklenen)} değer, {len(fark)} fark', fark or '')
assert not fark

# 2. Gecikmenin kötü puana etkisi: farklı karşılaştırmalar
t = pu[pu.satici_n == 1].copy()
t['b'] = t.kotu.astype(int)
t['g'] = t.gec.astype(int)
t['coklu'] = (t.kalem > 1).astype(int)
t['lt'] = np.log(t.tutar)
t['kat'] = t.product_category_name.fillna('yok')
sy = t.kat.value_counts()
t['kat'] = t.kat.where(t.kat.map(sy) >= 200, 'diger')
t['ceyrek'] = t[PU].dt.to_period('Q').astype(str)
ham = smf.ols('b~g', t).fit().params['g']
kontrol = smf.ols('b~g+coklu+lt+C(kat)+C(ceyrek)+C(customer_state)', t).fit()
fe = t.groupby('satici').filter(lambda g: len(g) >= 20)
x, yy = fe.g - fe.groupby('satici').g.transform('mean'), fe.b - fe.groupby('satici').b.transform('mean')
beta_fe = (x * yy).sum() / (x * x).sum()
son = t[t.once == False]
etki = {
    'n': len(t), 'ham_puan': round(ham * 100, 1), 'kontrollu_puan': round(kontrol.params['g'] * 100, 1),
    'kontrollu_se': round(kontrol.bse['g'] * 100, 2), 'ayni_satici_puan': round(beta_fe * 100, 1), 'ayni_satici_n': len(fe),
    'anket_sonra_gec': round(son[son.gec].b.mean() * 100, 1), 'anket_sonra_zamaninda': round(son[~son.gec].b.mean() * 100, 1),
    'anket_sonra_gec_n': int(son.gec.sum()), 'anket_sonra_puan': round((son[son.gec].b.mean() - son[~son.gec].b.mean()) * 100, 1),
}

# 3. Erken uyarı denemesi: yalnız o güne kadar tamamlanmış teslimatları görür, geleceğe bakmaz
dl = m[['t', 'tasima']].sort_values('t')
sat = []
for gun in pd.date_range('2017-02-15', '2018-08-31'):
    a = dl[(dl.t >= gun - pd.Timedelta(days=35)) & (dl.t <= gun - pd.Timedelta(days=8))].tasima
    b = dl[(dl.t >= gun - pd.Timedelta(days=7)) & (dl.t <= gun - pd.Timedelta(days=1))].tasima
    sat.append((gun, b.median() / a.median() if len(a) > 50 and len(b) > 20 else np.nan))
al = pd.DataFrame(sat, columns=['g', 'oran'])
z = m.assign(g=m[PU].dt.normalize()).merge(al, on='g')
uyari = []
for esik in (1.1, 1.2, 1.3, 1.5):
    f = z.oran >= esik
    uyari.append({'esik': esik, 'siparis_payi': round(f.mean() * 100, 1), 'gec_uyarili': round(z[f].gec.mean() * 100, 1), 'gec_uyarisiz': round(z[~f].gec.mean() * 100, 1)})

json.dump({'etki': etki, 'uyari': uyari, 'capraz_kontrol': len(beklenen)}, open('sonuclar/python.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(etki, ensure_ascii=False))
print(uyari)
