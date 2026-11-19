"""Kesit uçtan uca depo vakası: sentetik ham veri ve bütün adımların beklenen sonuçları.

Anadolu Market Gebze deposu. Eylül 2026'da eski raf düzeni, Ekim'de yeni düzen (hızlı dönen ürünler
toplama hattının başına alındı). Soru: yeni düzen satır başına toplama süresini kısalttı mı, kısalttıysa
diğer depolara yaymak için yeterli mi? Operasyon eşiği: satır başına en az 4 sn kazanç.

Çıktılar (bu klasöre):
  toplama_ham.json    — SQL adımının ham tablosu (kirli)
  toplama_temiz.csv   — SQL adımının beklenen çıktısı (Python, Power BI ve İstatistik adımlarının girdisi)
  beklenen.json       — her adımın beklenen sonuçları (pandas + scipy ile bağımsız hesap)
"""

import csv
import json
import random
import sqlite3
from pathlib import Path

import pandas as pd
from scipy import stats

OUT = Path(__file__).parent
R = random.Random(20261119)
BOLGE = {"A": -6.0, "B": 0.0, "C": 7.0}  # bölgeye göre ortalama farkı (sn)
VARDIYA = {"Gündüz": 0.0, "Gece": 3.0}
TOPLAYICI = [f"T{i:02d}" for i in range(1, 25)]
HIZ = {t: R.gauss(0, 3.0) for t in TOPLAYICI}  # kişi etkisi
TABAN = {"eski": 42.0, "yeni": 40.0}
N = 1200


def sure(duzen, bolge, vardiya, kisi):
    m = TABAN[duzen] + BOLGE[bolge] + VARDIYA[vardiya] + HIZ[kisi]
    # sağa çarpık süre: gamma, ortalama m, std ~ 0.3 m
    k = 11.0
    return round(R.gammavariate(k, m / k), 1)


def gunler(ay):
    return [f"2026-{ay:02d}-{g:02d}" for g in range(1, 29)]


rows = []
sid = 100000
for duzen, ay in (("eski", 9), ("yeni", 10)):
    # İki dönemde bölge ve vardiya karışımı aynı tutulur (bölge %40/%35/%25, vardiya %60/%40);
    # böylece fark düzen dışı bir karışım değişikliğinden gelmez. Python adımı bunu denetler.
    karisim = [(b, v) for b, nb in (("A", 480), ("B", 420), ("C", 300)) for v, nv in (("Gündüz", 0.6), ("Gece", 0.4)) for _ in range(round(nb * nv))]
    assert len(karisim) == N
    R.shuffle(karisim)
    for b, v in karisim:
        sid += 1
        t = R.choice(TOPLAYICI)
        rows.append(
            {
                "satir_id": sid,
                "tarih": R.choice(gunler(ay)),
                "vardiya": v,
                "bolge": b,
                "duzen": duzen,
                "toplayici": t,
                "sure_sn": sure(duzen, b, v, t),
            }
        )

# Kirli veri: el terminali kayıtlarında görülen tipik sorunlar
ham = [dict(r) for r in rows]
idx = list(range(len(ham)))
R.shuffle(idx)
it = iter(idx)
for _ in range(18):  # okutma yok: süre boş
    ham[next(it)]["sure_sn"] = None
for v in (0.0, 0.0, 1.2, 2.5, -3.0, 0.4):  # yanlış okutma: 5 sn altı
    ham[next(it)]["sure_sn"] = v
for v in (1250.0, 905.0, 1800.0, 640.0, 3600.0, 760.0, 2210.0, 615.0, 1500.0, 980.0, 700.0, 1320.0, 845.0, 2700.0):
    ham[next(it)]["sure_sn"] = v  # mola / kesinti: 600 sn üstü
for _ in range(40):  # yazım farkı: bölge ve düzen metni
    r = ham[next(it)]
    r["bolge"] = R.choice([" " + r["bolge"], r["bolge"].lower(), r["bolge"] + " "])
for _ in range(30):
    r = ham[next(it)]
    r["duzen"] = R.choice([r["duzen"].capitalize(), r["duzen"] + " ", r["duzen"].upper()])
dups = [dict(ham[next(it)]) for _ in range(25)]  # çift okutma: aynı satır iki kez
ham.extend(dups)
R.shuffle(ham)

cols = ["satir_id", "tarih", "vardiya", "bolge", "duzen", "toplayici", "sure_sn"]
(OUT / "toplama_ham.json").write_text(
    json.dumps({"cols": cols, "rows": [[r[c] for c in cols] for r in ham]}, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)

# ---------- 1. adım: SQL (gerçek SQLite ile) ----------
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE toplama_ham (satir_id INTEGER, tarih TEXT, vardiya TEXT, bolge TEXT, duzen TEXT, toplayici TEXT, sure_sn REAL)")
con.executemany("INSERT INTO toplama_ham VALUES (?,?,?,?,?,?,?)", [[r[c] for c in cols] for r in ham])
SQL_TEMIZ = """CREATE VIEW toplama_temiz AS
SELECT DISTINCT
  satir_id,
  tarih,
  vardiya,
  UPPER(TRIM(bolge)) AS bolge,
  LOWER(TRIM(duzen)) AS duzen,
  toplayici,
  sure_sn
FROM toplama_ham
WHERE sure_sn IS NOT NULL
  AND sure_sn BETWEEN 5 AND 600;"""
SQL_OZET = """SELECT duzen,
       COUNT(*) AS satir,
       ROUND(AVG(sure_sn), 2) AS ort_sure
FROM toplama_temiz
GROUP BY duzen
ORDER BY duzen;"""
con.executescript(SQL_TEMIZ)
ozet_sql = [list(r) for r in con.execute(SQL_OZET)]
ham_say = con.execute("SELECT COUNT(*) FROM toplama_ham").fetchone()[0]
temiz = pd.read_sql("SELECT * FROM toplama_temiz ORDER BY satir_id", con)
assert temiz["satir_id"].is_unique, "DISTINCT sonrası tekrar kalmamalı"
temiz.to_csv(OUT / "toplama_temiz.csv", index=False, quoting=csv.QUOTE_MINIMAL)
eleme = {
    "ham": ham_say,
    "bos_sure": con.execute("SELECT COUNT(*) FROM toplama_ham WHERE sure_sn IS NULL").fetchone()[0],
    "aralik_disi": con.execute("SELECT COUNT(*) FROM toplama_ham WHERE sure_sn < 5 OR sure_sn > 600").fetchone()[0],
    "cift": ham_say
    - con.execute("SELECT COUNT(*) FROM (SELECT DISTINCT * FROM toplama_ham)").fetchone()[0],
    "temiz": len(temiz),
}

# ---------- 2. adım: Python (pandas ile denetim) ----------
df = pd.read_csv(OUT / "toplama_temiz.csv")
denetim = {
    "satir_sayisi": int(len(df)),
    "bos_sure": int(df["sure_sn"].isna().sum()),
    "aralik_disi": int((~df["sure_sn"].between(5, 600)).sum()),
    "tekrar_eden_id": int(df["satir_id"].duplicated().sum()),
    "duzen_degerleri": sorted(df["duzen"].unique().tolist()),
    "bolge_degerleri": sorted(df["bolge"].unique().tolist()),
}
pay = pd.crosstab(df["duzen"], df["vardiya"], normalize="index").round(3)
vardiya_ort = df.pivot_table(index="vardiya", columns="duzen", values="sure_sn", aggfunc="mean").round(2)
grup = df.groupby("duzen")["sure_sn"].agg(["count", "mean", "std"])

# ---------- 3. adım: Power BI ölçüleri (pandas ile bağımsız) ----------
eski = df.loc[df.duzen == "eski", "sure_sn"]
yeni = df.loc[df.duzen == "yeni", "sure_sn"]
olcu = {
    "Satir": int(len(df)),
    "Eski Ort": float(eski.mean()),
    "Yeni Ort": float(yeni.mean()),
}
olcu["Kazanc sn"] = olcu["Eski Ort"] - olcu["Yeni Ort"]
olcu["Kazanc %"] = olcu["Kazanc sn"] / olcu["Eski Ort"]
bolge_kazanc = {}
for b, g in df.groupby("bolge"):
    e, y = g.loc[g.duzen == "eski", "sure_sn"].mean(), g.loc[g.duzen == "yeni", "sure_sn"].mean()
    bolge_kazanc[b] = {"Eski Ort": float(e), "Yeni Ort": float(y), "Kazanc sn": float(e - y)}

# ---------- 4. adım: İstatistik (scipy Welch t-testi) ----------
t = stats.ttest_ind(eski, yeni, equal_var=False)
ci = t.confidence_interval(0.95)
ESIK = 4.0
SATIR_AY = 52000
istat = {
    "fark": float(eski.mean() - yeni.mean()),
    "t": float(t.statistic),
    "df": float(t.df),
    "p": float(t.pvalue),
    "alt": float(ci.low),
    "ust": float(ci.high),
    "esik": ESIK,
    "karar": "istatistiksel fark var, operasyonel eşiğin altında"
    if t.pvalue < 0.05 and ci.high < ESIK
    else "başka",
    "aylik_saat": float((eski.mean() - yeni.mean()) * SATIR_AY / 3600),
    "esik_saat": ESIK * SATIR_AY / 3600,
    "satir_ay": SATIR_AY,
}
assert istat["karar"] != "başka", istat

# ---------- 4b. İkinci örnek: aynı kazanç, farklı vardiya dağılımı (dış inceleme, Kasım 2026) ----------
# İzmir deposu, aynı raf değişikliği. Düzenin gerçek etkisi yok (iki dönemde taban aynı); gece vardiyası 6 sn yavaş.
# Ekim'de gece payı %45'ten %25'e düştü. Toplam ortalama yine ~1,2 sn düşer; ama vardiya içinde fark yoktur.
# Öğrenci "ortalama süre düştü" ile "raf değişikliği düşüşe yol açtı" arasındaki farkı bu veride açıklar.
R2 = random.Random(20261124)
GECE2 = 6.5
PAY2 = {"eski": 0.45, "yeni": 0.25}
N2 = 1200
ornek2 = []
sid2 = 500000
for duzen in ("eski", "yeni"):
    ng = round(N2 * PAY2[duzen])
    for i in range(N2):
        v = "Gece" if i < ng else "Gündüz"
        sid2 += 1
        m = 42.0 + (GECE2 if v == "Gece" else 0.0)
        ornek2.append({"satir_id": sid2, "vardiya": v, "duzen": duzen, "sure_sn": round(R2.gammavariate(11.0, m / 11.0), 1)})
d2 = pd.DataFrame(ornek2)
e2, y2 = d2.loc[d2.duzen == "eski", "sure_sn"], d2.loc[d2.duzen == "yeni", "sure_sn"]
t2 = stats.ttest_ind(e2, y2, equal_var=False)
ci2 = t2.confidence_interval(0.95)
katman = {}
for v in ("Gündüz", "Gece"):
    ee, yy = d2[(d2.duzen == "eski") & (d2.vardiya == v)].sure_sn, d2[(d2.duzen == "yeni") & (d2.vardiya == v)].sure_sn
    tv = stats.ttest_ind(ee, yy, equal_var=False)
    cv = tv.confidence_interval(0.95)
    katman[v] = {"n_eski": int(len(ee)), "n_yeni": int(len(yy)), "eski": float(ee.mean()), "yeni": float(yy.mean()),
                 "fark": float(ee.mean() - yy.mean()), "p": float(tv.pvalue), "alt": float(cv.low), "ust": float(cv.high)}
# Vardiya karışımı sabit tutulmuş fark: iki dönemin ortalama vardiya payıyla ağırlıklı vardiya içi farklar
agirlik = {v: float((d2.vardiya == v).mean()) for v in ("Gündüz", "Gece")}
duzeltilmis = sum(agirlik[v] * katman[v]["fark"] for v in agirlik)
istat2 = {
    "depo": "İzmir",
    "eski": float(e2.mean()), "yeni": float(y2.mean()),
    "fark": float(e2.mean() - y2.mean()), "t": float(t2.statistic), "df": float(t2.df), "p": float(t2.pvalue),
    "alt": float(ci2.low), "ust": float(ci2.high),
    "gece_payi": {k: float((d2[d2.duzen == k].vardiya == "Gece").mean()) for k in ("eski", "yeni")},
    "katman": katman, "agirlik": agirlik, "duzeltilmis": float(duzeltilmis),
    "karisim_etkisi": float((e2.mean() - y2.mean()) - duzeltilmis),
}
assert istat2["p"] < 0.05 and abs(istat2["fark"] - istat["fark"]) < 0.4, istat2  # aynı görünen kazanç
assert all(k["alt"] < 0 < k["ust"] for k in katman.values()), katman  # vardiya içinde fark yok
d2.to_csv(OUT / "ornek2_izmir.csv", index=False)

beklenen = {
    "sql": {"temiz": SQL_TEMIZ, "ozet": SQL_OZET, "ozet_sonuc": ozet_sql, "eleme": eleme},
    "python": {
        "denetim": denetim,
        "vardiya_payi": {k: {c: float(v) for c, v in r.items()} for k, r in pay.to_dict("index").items()},
        "vardiya_ort": {k: {c: float(v) for c, v in r.items()} for k, r in vardiya_ort.to_dict("index").items()},
        "grup": {k: {"count": int(r["count"]), "mean": float(r["mean"]), "std": float(r["std"])} for k, r in grup.iterrows()},
    },
    "powerbi": {"olcu": olcu, "bolge": bolge_kazanc},
    "istatistik": istat,
    "istatistik2": istat2,
}
(OUT / "beklenen.json").write_text(json.dumps(beklenen, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"eleme": eleme, "ozet": ozet_sql, "olcu": olcu, "istat": istat, "istat2": istat2}, ensure_ascii=False, indent=1))
print(pay)
print(vardiya_ort)
print(grup)
