"""Dört adım sayfasını üretir ve uygulama depolarına yazar.

    python3 uret.py        # veri ve beklenen sonuçlar
    python3 sayfalar.py    # sayfalar → kesit-sql, kesit-python, kesit-powerbi, kesit-istatistik (yan yana klonlu)
"""

import json
import shutil
from pathlib import Path

from ortak import sayfa

K = Path(__file__).parent
ROOT = K.parents[2]  # depoların yan yana klonlandığı klasör
B = json.loads((K / "beklenen.json").read_text(encoding="utf-8"))
HAM = (K / "toplama_ham.json").read_text(encoding="utf-8")
CSV = (K / "toplama_temiz.csv").read_text(encoding="utf-8")
SQL, PY, PBI, ST = B["sql"], B["python"], B["powerbi"], B["istatistik"]
ST2 = B["istatistik2"]  # ikinci örnek: aynı kazanç, farklı vardiya dağılımı
CSV2 = (K / "ornek2_izmir.csv").read_text(encoding="utf-8")
E2, Y2 = ST2["eski"], ST2["yeni"]
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def tr(v, d=2):
    return f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


OZET_TABLO = (
    '<div class="vk-tw"><table><thead><tr><th>duzen</th><th class="n">satir</th><th class="n">ort_sure</th></tr></thead><tbody>'
    + "".join(f'<tr><td>{d}</td><td class="n">{tr(n, 0)}</td><td class="n">{tr(o)}</td></tr>' for d, n, o in SQL["ozet_sonuc"])
    + "</tbody></table></div>"
)
E = SQL["eleme"]


def incele_listesi():
    """Ham satırların hangi temizlik kuralına takıldığı (Python adımındaki kayıt inceleme paneli için)."""
    h = json.loads(HAM)
    c = h["cols"]
    goruldu, L = set(), []
    for r in h["rows"]:
        o = dict(zip(c, r))
        n = (o["satir_id"], o["tarih"], o["vardiya"], str(o["bolge"]).strip().upper(), str(o["duzen"]).strip().lower(), o["toplayici"], o["sure_sn"])
        if o["sure_sn"] is None:
            L.append([r, "bos", "sure_sn"])
        elif not 5 <= o["sure_sn"] <= 600:
            L.append([r, "aralik", "sure_sn"])
        elif n in goruldu:
            L.append([r, "cift", "satir_id"])
        else:
            goruldu.add(n)
            alan = [k for k in ("bolge", "duzen") if str(o[k]) != n[c.index(k)]]
            if alan:
                L.append([r, "yazim", alan[0]])
    say = {k: sum(1 for x in L if x[1] == k) for k in ("bos", "aralik", "cift", "yazim")}
    assert say == {"bos": E["bos_sure"], "aralik": E["aralik_disi"], "cift": E["cift"], "yazim": 70}, say
    return {"cols": c, "rows": L}


INCELE = incele_listesi()

# ----------------------------------------------------------------- 1. SQL
SQL_BASLANGIC = """-- 1) Temiz görünüm: toplama_temiz
--    · süresi boş olanları ve 5–600 sn dışını ele
--    · çift okutulan satırları tekille
--    · bölge ve düzen yazımını düzelt (boşluk, büyük/küçük harf)
CREATE VIEW toplama_temiz AS
SELECT satir_id, tarih, vardiya,
       bolge,      -- düzelt
       duzen,      -- düzelt
       toplayici, sure_sn
FROM toplama_ham;  -- koşulları ekle

-- 2) Özet: düzene göre satır sayısı ve ortalama süre
SELECT duzen,
       COUNT(*) AS satir,
       ROUND(AVG(sure_sn), 2) AS ort_sure
FROM toplama_temiz
GROUP BY duzen
ORDER BY duzen;
"""
SQL_COZUM = SQL["temiz"] + "\n\n" + SQL["ozet"] + "\n"

sql_govde = f"""<p class="vk-l">Anadolu Market Gebze deposunda Ekim'de raf düzeni değişti: hızlı dönen ürünler toplama hattının başına alındı. Operasyon müdürü yeni düzeni diğer depolara yaymadan önce şunu soruyor: <b>Satır başına toplama süresi gerçekten kısaldı mı, kısaldıysa yaymaya değecek kadar mı?</b> Dört adımda cevaplayacaksın. Bu adımda el terminali kayıtlarını analiz edilebilir hâle getiriyorsun.</p>
<section class="vk-k c" aria-labelledby="gorev"><h2 id="gorev">İlk görev: ham kayıtları temizle</h2>
<p>El terminalinden {tr(E["ham"], 0)} satır geldi. Kaçının, hangi nedenle analiz dışı kaldığını kendin bul; beklenen sonuç sayfanın sonunda kapalı duruyor.</p>
<ol><li><code>toplama_temiz</code> adlı bir görünüm (VIEW) oluştur: boş ve 5–600 sn dışındaki süreleri ele, çift satırları tekille, <code>bolge</code>'yi büyük harfe, <code>duzen</code>'i küçük harfe çevir ve boşlukları kırp.</li>
<li>Görünümden düzene göre satır sayısı ve ortalama süreyi veren özeti yaz. Son sorgu özetin kendisi olmalı.</li></ol>
<p class="vk-not" style="margin-top:10px">Önce keşfet (sorgun değişmez, sonuç aşağıda görünür):</p>
<div class="vk-btn"><button data-hazir="SELECT bolge, duzen, COUNT(*) AS satir FROM toplama_ham GROUP BY bolge, duzen ORDER BY 1, 2;">Yazım farklarını gör</button><button data-hazir="SELECT COUNT(*) AS bos FROM toplama_ham WHERE sure_sn IS NULL;">Boş süreleri say</button><button data-hazir="SELECT satir_id, COUNT(*) AS kez FROM toplama_ham GROUP BY satir_id HAVING COUNT(*) &gt; 1;">Çift okutmaları bul</button></div>
<label for="ed"><b>Sorgun</b> <span class="vk-not">(SQLite; her çalıştırmada veritabanı baştan kurulur)</span></label>
<textarea id="ed" class="vk-ed" spellcheck="false">{SQL_BASLANGIC}</textarea>
<div class="vk-btn"><button class="p" id="calistir">Çalıştır ve denetle</button><button id="cozum">Çözümü göster</button><button id="sifirla">Başa al</button></div>
<div class="vk-dur" id="dur" role="status" aria-live="polite">SQL motoru hazırlanıyor…</div>
<div id="sonuc"></div><ul class="vk-chk" id="kontrol" aria-label="Denetim"></ul></section>
<section class="vk-k" aria-labelledby="veri"><h2 id="veri">Veri: <code>toplama_ham</code></h2>
<p>Eylül (eski düzen) ve Ekim (yeni düzen) için {tr(E["ham"], 0)} toplama satırı. Her satır bir sipariş kaleminin raftan alınmasıdır.</p>
<div class="vk-tw"><table><thead><tr><th>Sütun</th><th>Anlamı</th></tr></thead><tbody>
<tr><td><code>satir_id</code></td><td>Toplama satırı numarası</td></tr><tr><td><code>tarih</code>, <code>vardiya</code></td><td>Gün ve vardiya (Gündüz / Gece)</td></tr>
<tr><td><code>bolge</code></td><td>Raf bölgesi: A, B, C</td></tr><tr><td><code>duzen</code></td><td>eski / yeni raf düzeni</td></tr>
<tr><td><code>toplayici</code></td><td>Toplayıcı kodu</td></tr><tr><td><code>sure_sn</code></td><td>Satırı toplama süresi (saniye)</td></tr></tbody></table></div>
<h3>Bilinen sorunlar</h3><ul><li>Okutulmayan satırlarda süre boş.</li><li>5 sn altı yanlış okutmadır; 600 sn üstü mola ya da kesintidir. İkisi de analiz dışı.</li><li>Terminal bağlantısı kopunca aynı satır iki kez gelmiş (bütün sütunlar aynı).</li><li>Bölge ve düzen metinlerinde boşluk ve büyük/küçük harf farkları var (<code> a</code>, <code>Yeni</code>).</li></ul>
</section>
<section class="vk-k" aria-labelledby="bek"><h2 id="bek">Beklenen çıktı</h2>
<details><summary>Beklenen sonucu aç (önce kendin dene)</summary>
<p>Ham {tr(E["ham"], 0)} satırdan {tr(E["bos_sure"], 0)} boş süre, {tr(E["aralik_disi"], 0)} aralık dışı süre ve {tr(E["cift"], 0)} çift okutma çıkar; <b>{tr(E["temiz"], 0)} temiz satır</b> kalır.</p>
{OZET_TABLO}
</details>
<p class="vk-not">Bu adımı çözünce <code>toplama_temiz</code> tablon bu tarayıcıda saklanır. 2. adımda “Kendi çıktımla devam et” ya da “Örnek veriyle dene” seçeneğinden birini seçersin; hangi veriyle çalıştığın orada yazar.</p>
<div class="vk-son"><button id="indir">toplama_temiz.csv indir</button><a class="vk-go" href="/kesit-python/vaka/depo/">2. adım: Python ile denetle →</a></div></section>"""

sql_betik = (
    "const HAM="
    + HAM
    + ";const BEK="
    + J({"ozet": SQL["ozet_sonuc"], "eleme": E})
    + ";const COZUM="
    + J(SQL_COZUM)
    + ";const BAS="
    + J(SQL_BASLANGIC)
    + r""";
let SQLM=null,son=null;
const $=s=>document.querySelector(s), dur=t=>$('#dur').textContent=t;
function kur(){const db=new SQLM.Database();db.run('CREATE TABLE toplama_ham (satir_id INTEGER, tarih TEXT, vardiya TEXT, bolge TEXT, duzen TEXT, toplayici TEXT, sure_sn REAL)');const st=db.prepare('INSERT INTO toplama_ham VALUES (?,?,?,?,?,?,?)');db.run('BEGIN');for(const r of HAM.rows)st.run(r);db.run('COMMIT');st.free();return db;}
function goster(r){if(!r){$('#sonuc').innerHTML='<p class="vk-not">Sorgu satır döndürmedi.</p>';return;}const n=r.values.length;$('#sonuc').innerHTML='<h3>Son sorgunun sonucu · '+vkSay(n)+' satır</h3>'+vkTablo(r.columns,r.values.slice(0,50),r.values[0]?r.values[0].map((v,i)=>typeof v==='number'?i:-1).filter(i=>i>=0):[])+(n>50?'<p class="vk-not">İlk 50 satır gösteriliyor.</p>':'');}
function denetle(db,r){const L=[],ok=(c,t)=>L.push([c,t]);
  let var_=false;try{var_=db.exec("SELECT COUNT(*) FROM sqlite_master WHERE name='toplama_temiz'")[0].values[0][0]>0}catch(e){}
  ok(var_,'toplama_temiz görünümü (ya da tablosu) var');
  if(var_){try{const q=s=>db.exec(s)[0].values[0];
    const [n]=q('SELECT COUNT(*) FROM toplama_temiz');ok(n===BEK.eleme.temiz,'Temiz satır sayısı '+vkSay(n)+(n===BEK.eleme.temiz?'':' (beklenen '+vkSay(BEK.eleme.temiz)+')'));
    const [b]=q('SELECT COUNT(*) FROM toplama_temiz WHERE sure_sn IS NULL OR sure_sn < 5 OR sure_sn > 600');ok(b===0,'Boş ya da 5–600 sn dışı süre kalmadı'+(b?' ('+b+' satır kaldı)':''));
    const [d]=q('SELECT COUNT(*) - COUNT(DISTINCT satir_id) FROM toplama_temiz');ok(d===0,'Her satir_id bir kez geçiyor'+(d?' ('+d+' tekrar)':''));
    const [y]=q("SELECT COUNT(*) FROM toplama_temiz WHERE bolge NOT IN ('A','B','C') OR duzen NOT IN ('eski','yeni')");ok(y===0,'Bölge yalnız A/B/C, düzen yalnız eski/yeni'+(y?' ('+y+' satırda yazım farkı)':''));
  }catch(e){ok(false,'Görünüm okunamadı: '+e.message)}}
  const oz=r&&r.columns.length>=3&&r.values.length===BEK.ozet.length&&BEK.ozet.every(b=>r.values.some(v=>String(v[0])===b[0]&&v[1]===b[1]&&Math.abs(v[2]-b[2])<0.006));
  ok(!!oz,'Son sorgunun sonucu beklenen özetle aynı');
  $('#kontrol').innerHTML=L.map(([c,t])=>'<li class="'+(c?'ok':'no')+'">'+vkEsc(t)+'</li>').join('');
  return L.every(x=>x[0]);}
function calistir(){if(!SQLM)return;const db=kur();try{const rs=db.exec($('#ed').value);const r=rs[rs.length-1];goster(r);const tamam=denetle(db,r);
  if(tamam){const t=db.exec('SELECT * FROM toplama_temiz ORDER BY satir_id')[0];son=t;vkCiktiYaz(vkCsvMetin(t.columns,t.values),t.values.length);vkYaz('sql',{ozet:r.values,satir:t.values.length});vkAdimlar();dur('Tamam: çıktın beklenenle aynı ve bu tarayıcıya kaydedildi ('+vkSay(t.values.length)+' satır). 2. adımda “Kendi çıktımla devam et” ile kullanabilirsin.');}
  else dur('Bazı denetimler geçmedi; işaretli maddelere bak. Takılırsan “Çözümü göster”.');}
  catch(e){$('#sonuc').innerHTML='';$('#kontrol').innerHTML='';dur('SQL hatası: '+e.message);}finally{db.close();}}
$('#calistir').onclick=calistir;
$('#cozum').onclick=()=>{$('#ed').value=COZUM;dur('Çözüm yazıldı. “Çalıştır ve denetle” ile dene.');};
$('#sifirla').onclick=()=>{$('#ed').value=BAS;$('#sonuc').innerHTML='';$('#kontrol').innerHTML='';dur('Başlangıç sorgusu geri yüklendi.');};
document.querySelectorAll('[data-hazir]').forEach(b=>b.onclick=()=>{if(!SQLM)return;const db=kur();try{goster(db.exec(b.dataset.hazir).pop());dur('Keşif sorgusu: '+b.textContent+'. Sorgun değişmedi.');}catch(e){dur(e.message)}finally{db.close()}});
$('#indir').onclick=()=>{if(son)vkCsvIndir('toplama_temiz.csv',son.columns,son.values);else{const db=kur();try{db.exec(COZUM);const t=db.exec('SELECT * FROM toplama_temiz ORDER BY satir_id')[0];vkCsvIndir('toplama_temiz.csv',t.columns,t.values);}finally{db.close()}}};
initSqlJs().then(m=>{SQLM=m;dur('SQL motoru hazır. Sorguyu tamamla ve çalıştır.');},e=>dur('SQL motoru yüklenemedi: '+e.message));
"""
)

# ----------------------------------------------------------------- 2. Python
DEN = PY["denetim"]
GRUP = PY["grup"]
PY_BASLANGIC = '''import pandas as pd

df = pd.read_csv("toplama_temiz.csv")   # 1. adımın çıktısı

# 1) Temel denetim: SQL'in söz verdiği temizlik gerçekten yapıldı mı?
denetim = {
    "satir_sayisi": len(df),
    "bos_sure": int(df["sure_sn"].isna().sum()),
    "aralik_disi": int((~df["sure_sn"].between(5, 600)).sum()),
    "tekrar_eden_id": None,   # satir_id'de kaç tekrar var? (duplicated)
    "duzen_degerleri": sorted(df["duzen"].unique().tolist()),
    "bolge_degerleri": sorted(df["bolge"].unique().tolist()),
}
print(denetim)

# 2) Karşılaştırma adil mi? İki dönemde vardiya karışımı aynı olmalı.
pay = pd.crosstab(df["duzen"], df["vardiya"], normalize="index").round(3)
print(pay)

# 3) Fark her vardiyada aynı yönde mi? (karışım etkisi denetimi)
print(df.pivot_table(index="vardiya", columns="duzen", values="sure_sn", aggfunc="mean").round(2))

# 4) Sonraki adımlar için grup özeti
ozet = df.groupby("duzen")["sure_sn"].agg(["count", "mean", "std"])
print(ozet.round(3))
'''
PY_COZUM = PY_BASLANGIC.replace(
    '"tekrar_eden_id": None,   # satir_id\'de kaç tekrar var? (duplicated)',
    '"tekrar_eden_id": int(df["satir_id"].duplicated().sum()),',
)
assert PY_COZUM != PY_BASLANGIC
PY_TEST = f'''
assert isinstance(denetim, dict), "denetim bir sözlük olmalı"
assert denetim["satir_sayisi"] == {DEN["satir_sayisi"]}, "Satır sayısı 1. adımın çıktısıyla aynı olmalı"
assert denetim["bos_sure"] == 0 and denetim["aralik_disi"] == 0, "Boş ya da aralık dışı süre kalmamalı"
assert denetim["tekrar_eden_id"] == 0, "tekrar_eden_id: satir_id sütununda duplicated().sum() değeri"
assert denetim["duzen_degerleri"] == ["eski", "yeni"] and denetim["bolge_degerleri"] == ["A", "B", "C"], "Yazım farkı kalmamalı"
assert abs(pay.loc["eski", "Gündüz"] - pay.loc["yeni", "Gündüz"]) < 0.02, "Vardiya karışımı iki dönemde benzer olmalı"
assert abs(ozet.loc["eski", "mean"] - {GRUP["eski"]["mean"]:.6f}) < 1e-4 and abs(ozet.loc["yeni", "mean"] - {GRUP["yeni"]["mean"]:.6f}) < 1e-4, "Grup ortalamaları"
assert int(ozet.loc["eski", "count"]) == {GRUP["eski"]["count"]} and int(ozet.loc["yeni", "count"]) == {GRUP["yeni"]["count"]}, "Grup sayıları"
import json as _j
print("__VAKA__" + _j.dumps({{"denetim": denetim, "grup": {{k: {{"count": int(v["count"]), "mean": float(v["mean"]), "std": float(v["std"])}} for k, v in ozet.iterrows()}}}}))
'''
VP, VO = PY["vardiya_payi"], PY["vardiya_ort"]
py_govde = f"""<p class="vk-l">1. adımda SQL, ham kayıtları {tr(E["temiz"], 0)} temiz satıra indirdi. Panoya ve teste geçmeden önce bu çıktıya güvenebilir miyiz? Python ile iki şeyi denetliyorsun: temizlik gerçekten yapıldı mı ve iki dönem adil karşılaştırılabilir mi?</p>
<section class="vk-k vk-gelen" aria-labelledby="gelen"><h2 id="gelen">Önceki adımdan gelen: SQL çıktısı <span class="vk-et bek" id="gelenDurum">1. adım henüz çözülmedi</span></h2>
<p>Python motoruna <code>toplama_temiz.csv</code> olarak hangi tablonun yükleneceğini seç:</p><div id="kaynak"></div>
<details><summary>Beklenen SQL özeti (karşılaştırma için)</summary>{OZET_TABLO}</details></section>
<section class="vk-k" aria-labelledby="gorev"><h2 id="gorev">Görev</h2>
<ol><li><code>denetim</code> sözlüğündeki eksik satırı tamamla: <code>satir_id</code> sütununda kaç tekrar var?</li><li>Çıktıda üç şeye bak: temizlik (hepsi 0 olmalı), vardiya payları (iki dönemde benzer mi?) ve vardiya içi ortalamalar (fark iki vardiyada da aynı yönde mi?).</li></ol>
<label for="ed"><b>Kodun</b> <span class="vk-not">(gerçek Python, tarayıcıda Pyodide ile; ilk çalıştırmada motor ve pandas iner, 10–30 sn sürebilir)</span></label>
<textarea id="ed" class="vk-ed" spellcheck="false" style="min-height:420px">{PY_BASLANGIC}</textarea>
<div class="vk-btn"><button class="p" id="calistir">Çalıştır ve denetle</button><button id="cozum">Çözümü göster</button><button id="sifirla">Başa al</button></div>
<div class="vk-dur" id="dur" role="status" aria-live="polite">Python motoru ilk çalıştırmada yüklenecek.</div>
<pre id="cikti" hidden></pre><ul class="vk-chk" id="kontrol" aria-label="Denetim"></ul></section>
<section class="vk-k" aria-labelledby="incele"><h2 id="incele">Bir kaydı incele: neden elendi?</h2>
<p>SQL {tr(E["ham"] - E["temiz"], 0)} satırı eledi, {tr(70, 0)} satırın yazımını düzeltti. Bir kayıt seç; hangi kuralın çalıştığını ve sonucunu gör. Temizleme kararını tek kayıt üzerinde doğrula.</p>
<div class="vk-sec" role="group" aria-label="Kural seç" id="kurallar"></div>
<div class="vk-iki"><div class="vk-tw" style="max-height:340px;overflow:auto;border:1px solid var(--line);border-radius:8px"><table><thead><tr><th>satir_id</th><th>bolge</th><th>duzen</th><th class="n">sure_sn</th></tr></thead><tbody id="kayitlar"></tbody></table></div>
<div id="kayit" class="vk-k" style="margin:0" aria-live="polite"><p class="vk-not">Soldan bir kayıt seç.</p></div></div></section>
<section class="vk-k" aria-labelledby="bek"><h2 id="bek">Beklenen çıktı</h2>
<div class="vk-iki"><div><h3>Temizlik denetimi</h3><ul class="vk-chk"><li class="ok">satir_sayisi = {tr(DEN["satir_sayisi"], 0)}</li><li class="ok">bos_sure = 0, aralik_disi = 0, tekrar_eden_id = 0</li><li class="ok">düzen: eski, yeni · bölge: A, B, C</li></ul></div>
<div><h3>Vardiya payı (satır oranı)</h3><div class="vk-tw"><table><thead><tr><th>duzen</th><th class="n">Gündüz</th><th class="n">Gece</th></tr></thead><tbody>{"".join(f'<tr><td>{d}</td><td class="n">{tr(VP[d]["Gündüz"], 3)}</td><td class="n">{tr(VP[d]["Gece"], 3)}</td></tr>' for d in ("eski", "yeni"))}</tbody></table></div></div></div>
<h3>Vardiya içi ortalama süre (sn)</h3><div class="vk-tw"><table><thead><tr><th>vardiya</th><th class="n">eski</th><th class="n">yeni</th><th class="n">fark</th></tr></thead><tbody>{"".join(f'<tr><td>{v}</td><td class="n">{tr(VO[v]["eski"])}</td><td class="n">{tr(VO[v]["yeni"])}</td><td class="n">{tr(VO[v]["eski"] - VO[v]["yeni"])}</td></tr>' for v in ("Gündüz", "Gece"))}</tbody></table></div>
<h3>Grup özeti (sonraki adımların girdisi)</h3><div class="vk-tw"><table><thead><tr><th>duzen</th><th class="n">count</th><th class="n">mean</th><th class="n">std</th></tr></thead><tbody>{"".join(f'<tr><td>{d}</td><td class="n">{tr(GRUP[d]["count"], 0)}</td><td class="n">{tr(GRUP[d]["mean"], 3)}</td><td class="n">{tr(GRUP[d]["std"], 3)}</td></tr>' for d in ("eski", "yeni"))}</tbody></table></div>
<p><b>Yorum:</b> Temizlik tamam. Vardiya karışımı iki dönemde aynı (%60 gündüz), yani fark vardiya değişikliğinden gelmiyor. Yeni düzen iki vardiyada da daha hızlı. Veri panoya ve teste hazır.</p>
<div class="vk-son"><span class="vk-not">Panoda bu {tr(E["temiz"], 0)} satır ve ortalamalar kullanılacak.</span><a class="vk-go" href="/kesit-powerbi/vaka/depo/">3. adım: Power BI'da göster →</a></div></section>"""

py_betik = (
    "const CSV="
    + J(CSV)
    + ";const BAS="
    + J(PY_BASLANGIC)
    + ";const COZUM="
    + J(PY_COZUM)
    + ";const TEST="
    + J(PY_TEST)
    + ";const BEK_SQL="
    + J(SQL["ozet_sonuc"])
    + ";const INC="
    + J(INCELE)
    + r""";
const $=s=>document.querySelector(s), dur=t=>$('#dur').textContent=t;
// Kayıt inceleme: her kural için ad, koşul ve sonuç
const KURAL={bos:{ad:'Boş süre',kosul:'sure_sn boş olmamalı (IS NOT NULL)',neden:'Satır okutulmamış; süre bilinmiyor.',sonuc:'Elendi'},
  aralik:{ad:'Aralık dışı süre',kosul:'sure_sn 5 ile 600 sn arasında olmalı (BETWEEN 5 AND 600)',neden:v=>v<5?'5 sn altı: yanlış ya da çift tıklamayla okutma.':'600 sn üstü: mola, kesinti ya da unutulan terminal.',sonuc:'Elendi'},
  cift:{ad:'Çift okutma',kosul:'Bütün sütunları aynı olan satır bir kez kalmalı (SELECT DISTINCT)',neden:'Terminal bağlantısı kopunca aynı satır ikinci kez gelmiş; ilk kopya tabloda kaldı, bu kopya düştü.',sonuc:'Elendi (kopya)'},
  yazim:{ad:'Yazım düzeltildi',kosul:'bolge büyük harf, duzen küçük harf ve boşluksuz olmalı (UPPER/LOWER + TRIM)',neden:'Metin farklı yazılmış; anlamı aynı olduğu için satır kaldı, değer düzeltildi.',sonuc:'Kaldı, düzeltildi'}};
const iC=k=>INC.cols.indexOf(k);let incSec='bos';
function incKurallar(){$('#kurallar').innerHTML=Object.keys(KURAL).map(k=>'<button type="button" data-kural="'+k+'" aria-pressed="'+(k===incSec)+'">'+KURAL[k].ad+' · '+INC.rows.filter(x=>x[1]===k).length+'</button>').join('');
  document.querySelectorAll('[data-kural]').forEach(b=>b.onclick=()=>{incSec=b.dataset.kural;incKurallar();incListe();});}
const gor=v=>v==null?'boş':typeof v==='string'?'“'+v+'”':Number.isInteger(v)&&v>9999?String(v):vkSay(v,1);
function incListe(){const L=INC.rows.map((x,i)=>[x,i]).filter(([x])=>x[1]===incSec);
  $('#kayitlar').innerHTML=L.map(([x,i])=>{const r=x[0];return '<tr><td><button type="button" class="vk-lnk" data-i="'+i+'">'+r[iC('satir_id')]+'</button></td><td>'+vkEsc(gor(r[iC('bolge')]))+'</td><td>'+vkEsc(gor(r[iC('duzen')]))+'</td><td class="n">'+vkEsc(gor(r[iC('sure_sn')]))+'</td></tr>';}).join('');
  document.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>incGoster(+b.dataset.i));if(L.length)incGoster(L[0][1]);}
function incGoster(i){const [r,k,alan]=INC.rows[i],K=KURAL[k],v=r[iC(alan)],neden=typeof K.neden==='function'?K.neden(v):K.neden,id=r[iC('satir_id')];
  document.querySelectorAll('[data-i]').forEach(b=>b.setAttribute('aria-current',+b.dataset.i===i?'true':'false'));
  const duz=k==='yazim'?(alan==='bolge'?String(v).trim().toUpperCase():String(v).trim().toLowerCase()):null;
  $('#kayit').innerHTML='<h3 style="margin-top:0">satir_id '+id+'</h3>'+vkTablo(['Sütun','Değer'],INC.cols.map((c,j)=>[c===alan?c+' ←':c,gor(r[j])]))
    +'<p><b>Çalışan kural:</b> '+vkEsc(K.ad)+'. <span class="vk-not">'+vkEsc(K.kosul)+'</span></p><p><b>Neden:</b> '+vkEsc(neden)+(duz!=null?' '+vkEsc(gor(v))+' → '+vkEsc(gor(duz))+'.':'')+'</p><p><b>Sonuç:</b> '+vkEsc(K.sonuc)+'.</p>'
    +'<p class="vk-not">Kendin doğrula: 1. adımdaki SQL editöründe <code>SELECT * FROM toplama_ham WHERE satir_id = '+id+';</code> ya da temiz tabloda <code>df[df["satir_id"] == '+id+']</code>'+(k==='yazim'||k==='cift'?' (bir satır döner)':' (boş döner)')+'.</p>';}
incKurallar();incListe();
// Kesit Python'un motoru (pyworker.js): aynı Pyodide, aynı uyumluluk katmanı.
const M={w:null,seq:0,pend:new Map(),hazir:null,dosya:false};
let KAY=vkKaynak($('#kaynak'),CSV,k=>{KAY=k;M.dosya=false;$('#cikti').hidden=true;$('#kontrol').innerHTML='';dur('Veri değişti: '+(k.kaynak==='kendi'?'kendi SQL çıktın':'örnek veri')+'. Kodu yeniden çalıştır.');});
function isci(){if(M.w)return M.w;const w=M.w=new Worker('../../pyworker.js');w.onmessage=ev=>{const m=ev.data;if(m.state){if(m.state==='yukleniyor')dur('Python motoru yükleniyor…');if(m.state==='paket')dur('Paketler hazırlanıyor (pandas)…');return;}if(m.id==null)return;const p=M.pend.get(m.id);if(!p)return;M.pend.delete(m.id);m.ok?p.ok(m.res):p.bad(new Error(m.msg));};w.onerror=e=>{e.preventDefault&&e.preventDefault();dur('Python motoru başlatılamadı. Bağlantını kontrol edip yeniden dene.');M.w=null;M.hazir=null;};return w;}
const cagir=(cmd,ek)=>new Promise((ok,bad)=>{const id=++M.seq;M.pend.set(id,{ok,bad});isci().postMessage(Object.assign({id,cmd},ek));});
async function hazirla(){if(!M.hazir)M.hazir=cagir('boot');await M.hazir;if(!M.dosya){const r=await cagir('run',{opt:{code:'open("toplama_temiz.csv","w",encoding="utf-8").write('+JSON.stringify(KAY.csv)+')',ns:''}});if(r.err)throw new Error(r.err.msg);M.dosya=true;}}
async function calistir(){const b=$('#calistir');b.disabled=true;$('#kontrol').innerHTML='';try{await hazirla();dur('Kod çalışıyor…');
  const r=await cagir('run',{opt:{code:$('#ed').value,tests:TEST,ns:''}});
  let out=String(r.out||''),veri=null;const i=out.lastIndexOf('__VAKA__');if(i>=0){try{veri=JSON.parse(out.slice(i+8).trim())}catch(e){}out=out.slice(0,i);}
  $('#cikti').hidden=false;$('#cikti').textContent=(out+(r.stderr?'\n'+r.stderr:'')).trim()||'(çıktı yok)';
  if(r.err){const t=r.err.phase==='test';$('#kontrol').innerHTML='<li class="no">'+vkEsc(t?'Denetim: '+r.err.msg:r.err.type+': '+r.err.msg+(r.err.line?' (satır '+r.err.line+')':''))+'</li>';dur(t?'Kod çalıştı ama bir denetim geçmedi.':'Kod hata verdi.');return;}
  $('#kontrol').innerHTML=['Satır sayısı 1. adımla aynı','Temizlik tamam: boş, aralık dışı ve tekrar yok','Yazım farkı yok','Vardiya karışımı iki dönemde benzer','Grup ortalamaları ve sayıları beklenenle aynı'].map(t=>'<li class="ok">'+t+'</li>').join('');
  if(veri)vkYaz('python',Object.assign(veri,{kaynak:KAY.kaynak}));vkAdimlar();dur('Tamam: denetim geçti ('+(KAY.kaynak==='kendi'?'senin SQL çıktınla':'örnek veriyle')+'). 3. adıma geçebilirsin.');}
 catch(e){dur('Çalıştırılamadı: '+e.message);}finally{b.disabled=false;}}
$('#calistir').onclick=calistir;
$('#cozum').onclick=()=>{$('#ed').value=COZUM;dur('Çözüm yazıldı. “Çalıştır ve denetle” ile dene.');};
$('#sifirla').onclick=()=>{$('#ed').value=BAS;$('#cikti').hidden=true;$('#kontrol').innerHTML='';dur('Başlangıç kodu geri yüklendi.');};
(function(){const s=vkOku().sql,e=$('#gelenDurum');if(!s||!s.tamam)return;const ayni=Array.isArray(s.ozet)&&BEK_SQL.every(b=>s.ozet.some(v=>v[0]===b[0]&&v[1]===b[1]&&Math.abs(v[2]-b[2])<0.006));e.className='vk-et '+(ayni?'ok':'no');e.textContent=ayni?'✓ senin SQL çıktın bununla aynı':'Senin SQL çıktın farklıydı; bu adım beklenen çıktıyla devam eder';})();
"""
)

# ----------------------------------------------------------------- 3. Power BI
OL = PBI["olcu"]
OLCULER = [
    ("Satir", "COUNTROWS(Toplama)", True),
    ("Ort Sure", "AVERAGE(Toplama[sure_sn])", True),
    ("Eski Ort", 'CALCULATE([Ort Sure], Toplama[duzen] = "eski")', True),
    ("Yeni Ort", 'CALCULATE([Ort Sure], Toplama[duzen] = "yeni")', True),
    ("Kazanc sn", "[Eski Ort] - [Yeni Ort]", False),
    ("Kazanc %", "DIVIDE([Kazanc sn], [Eski Ort])", False),
]
olcu_html = "".join(
    f'<div class="olcu"><label for="m{i}"><code>{ad} =</code>{"" if hazir else " <span class=vk-et>sen yaz</span>"}</label>'
    f'<textarea id="m{i}" class="vk-ed" data-olcu="{ad}" spellcheck="false" rows="2" style="min-height:0">{ifade if hazir else ""}</textarea><span class="hata" id="h{i}"></span></div>'
    for i, (ad, ifade, hazir) in enumerate(OLCULER)
)
PG = PY["grup"]
pbi_govde = f"""<p class="vk-l">Veri denetimden geçti. Şimdi operasyon ekibinin her gün bakacağı panoyu kuruyorsun: yeni düzen satır başına kaç saniye kazandırıyor, hangi bölgede daha çok? Ölçüleri DAX ile yaz; kartlar ve grafik ölçülerden çizilir.</p>
<section class="vk-k vk-gelen" aria-labelledby="gelen"><h2 id="gelen">Önceki adımdan gelen: Python denetimi <span class="vk-et bek" id="gelenDurum">2. adım henüz çözülmedi</span></h2>
<p>Modele <code>Toplama</code> tablosu olarak hangi verinin yükleneceğini seç:</p><div id="kaynak"></div>
<p>Python'un grup özeti panonun doğru olup olmadığını anlamak için referanstır:</p>
<div class="vk-tw"><table><thead><tr><th>duzen</th><th class="n">count</th><th class="n">mean</th><th class="n">std</th></tr></thead><tbody>{"".join(f'<tr><td>{d}</td><td class="n">{tr(PG[d]["count"], 0)}</td><td class="n">{tr(PG[d]["mean"], 3)}</td><td class="n">{tr(PG[d]["std"], 3)}</td></tr>' for d in ("eski", "yeni"))}</tbody></table></div></section>
<section class="vk-k" aria-labelledby="gorev"><h2 id="gorev">Görev: ölçüleri yaz</h2>
<p>İlk dört ölçü hazır. <code>Kazanc sn</code> (eski ortalama − yeni ortalama) ve <code>Kazanc %</code> (kazancın eski ortalamaya oranı; sıfıra bölmeye dayanıklı) ölçülerini sen yaz.</p>
<div class="olculer">{olcu_html}</div>
<div class="vk-btn"><button class="p" id="calistir">Ölçüleri çalıştır</button><button id="cozum">Çözümü göster</button></div>
<div class="vk-dur" id="dur" role="status" aria-live="polite">DAX motoru hazırlanıyor…</div>
<ul class="vk-chk" id="kontrol" aria-label="Denetim"></ul>
<div id="pano" hidden><h3>Pano</h3><div class="vk-kart" id="kartlar"></div>
<div class="vk-iki"><figure style="margin:0"><figcaption class="vk-not">Bölgeye göre kazanç (sn/satır) · kesik çizgi: yaymak için gereken 4 sn</figcaption><div id="grafik"></div></figure>
<div><h3 style="margin-top:0">Vardiyaya göre</h3><div id="matris"></div></div></div></div>
<p class="vk-not">Bu ekran Power BI Desktop değildir; Kesit Power BI'ın tarayıcıda çalışan DAX benzetim motorudur (aynı motor derslerde kullanılır). Aynı ölçüleri Desktop'ta yazmak için CSV'yi indir, <code>Toplama</code> adıyla içe al.</p></section>
<section class="vk-k" aria-labelledby="bek"><h2 id="bek">Beklenen çıktı</h2>
<div class="vk-kart"><div><span>Eski ort.</span><b>{tr(OL["Eski Ort"])} sn</b></div><div><span>Yeni ort.</span><b>{tr(OL["Yeni Ort"])} sn</b></div><div><span>Kazanç</span><b>{tr(OL["Kazanc sn"])} sn</b></div><div><span>Kazanç %</span><b>%{tr(OL["Kazanc %"] * 100)}</b></div></div>
<div class="vk-tw"><table><thead><tr><th>bölge</th><th class="n">Eski Ort</th><th class="n">Yeni Ort</th><th class="n">Kazanc sn</th></tr></thead><tbody>{"".join(f'<tr><td>{b}</td><td class="n">{tr(v["Eski Ort"])}</td><td class="n">{tr(v["Yeni Ort"])}</td><td class="n">{tr(v["Kazanc sn"])}</td></tr>' for b, v in PBI["bolge"].items())}</tbody></table></div>
<p><b>Panonun söylediği:</b> Yeni düzen satır başına ortalama {tr(OL["Kazanc sn"])} sn (%{tr(OL["Kazanc %"] * 100, 1)}) kazandırıyor; bütün bölgelerde kazanç 4 sn çizgisinin altında. <b>Panonun söyleyemediği:</b> Bu {tr(OL["Kazanc sn"])} sn gerçek bir etki mi, yoksa iki aylık rastlantı mı? Bunu 4. adım cevaplar.</p>
<div class="vk-son"><button id="indir">toplama_temiz.csv indir</button><a class="vk-go" href="/kesit-istatistik/vaka/depo/">4. adım: İstatistikle karar sınırını açıkla →</a></div></section>"""
PBI_CSS = "<style>.olculer{display:grid;gap:8px}.olcu label{display:block;font-size:.9rem;margin-bottom:2px}.olcu .hata{display:block;color:var(--bad);font-size:.85rem}#grafik svg{width:100%;height:auto;display:block}</style>"
pbi_betik = (
    "const CSV="
    + J(CSV)
    + ";const BEK="
    + J({"olcu": OL, "bolge": PBI["bolge"]})
    + ";const COZUM="
    + J({a: e for a, e, _ in OLCULER})
    + ";const BEK_PY="
    + J(PY["grup"])
    + r""";
const $=s=>document.querySelector(s), dur=t=>$('#dur').textContent=t;
const SAY=['satir_id','sure_sn'];let veri=null,MOTOR=null;
const modelKur=csv=>{veri=vkCsvOku(csv);return {tables:{Toplama:{rows:veri.rows.map(r=>{const o={};veri.cols.forEach((c,i)=>o[c]=SAY.includes(c)?Number(r[i]):r[i]);return o;}),cols:veri.cols,kind:'fact'}},rels:[]};};
let KAY=vkKaynak($('#kaynak'),CSV,k=>{KAY=k;window.PBI_MODEL=modelKur(k.csv);MOTOR=window.PBI_CREATE_DAX?window.PBI_CREATE_DAX(window.PBI_MODEL):null;$('#pano').hidden=true;$('#kontrol').innerHTML='';dur('Veri değişti: '+(k.kaynak==='kendi'?'kendi SQL çıktın':'örnek veri')+'. Ölçüleri yeniden çalıştır.');});
window.PBI_MODEL=modelKur(KAY.csv);
const sc=document.createElement('script');sc.src='dax.js';sc.onload=()=>dur('DAX motoru hazır. Eksik iki ölçüyü yaz ve çalıştır.');sc.onerror=()=>dur('DAX motoru yüklenemedi.');document.head.appendChild(sc);
function olculer(){const ms={};document.querySelectorAll('[data-olcu]').forEach(t=>ms[t.dataset.olcu]={name:t.dataset.olcu,expr:t.value.trim()});return ms;}
function grafik(rows){const W=Math.max(300,Math.round(document.querySelector('#grafik').clientWidth||520)),H=230,L=40,B=34,max=Math.max(5,...rows.map(r=>r.vals[2]||0))*1.1,y=v=>H-B-(v/max)*(H-B-12),bw=(W-L-20)/rows.length;
  let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Bölgeye göre kazanç: '+rows.map(r=>r.keys[0]+' '+vkSay(r.vals[2],2)+' sn').join(', ')+'">';
  for(let t=0;t<=max;t+=1){s+='<line x1="'+L+'" x2="'+(W-10)+'" y1="'+y(t)+'" y2="'+y(t)+'" stroke="#DEDBD2"/><text x="'+(L-6)+'" y="'+(y(t)+4)+'" text-anchor="end" font-size="12" fill="#5A574E">'+t+'</text>';}
  rows.forEach((r,i)=>{const v=r.vals[2]||0,x=L+10+i*bw;s+='<rect x="'+x+'" y="'+y(v)+'" width="'+(bw-20)+'" height="'+(H-B-y(v))+'" fill="#7A5600" rx="3"/><text x="'+(x+(bw-20)/2)+'" y="'+(y(v)-6)+'" text-anchor="middle" font-size="13" font-weight="600" fill="#1B1A16">'+vkSay(v,2)+'</text><text x="'+(x+(bw-20)/2)+'" y="'+(H-12)+'" text-anchor="middle" font-size="13" fill="#1B1A16">Bölge '+vkEsc(r.keys[0])+'</text>';});
  s+='<line x1="'+L+'" x2="'+(W-10)+'" y1="'+y(4)+'" y2="'+y(4)+'" stroke="#B3261E" stroke-width="2" stroke-dasharray="6 4"/><text x="'+(W-12)+'" y="'+(y(4)-6)+'" text-anchor="end" font-size="12" fill="#B3261E">eşik 4 sn</text></svg>';return s;}
function calistir(){if(!window.PBI_DAX){dur('DAX motoru daha yüklenmedi.');return;}const D=MOTOR||window.PBI_DAX,ms=olculer(),deg={},L=[];let hata=false;
  document.querySelectorAll('[data-olcu]').forEach((t,i)=>{const h=$('#h'+i);h.textContent='';try{if(!t.value.trim())throw new Error('Ölçü boş.');deg[t.dataset.olcu]=D.evalMeasure(ms,t.value.trim(),[]);}catch(e){h.textContent=e.message;hata=true;}});
  const yakin=(a,b,e)=>typeof a==='number'&&Math.abs(a-b)<e;
  L.push([!hata,'Bütün ölçüler hatasız çalıştı']);
  L.push([yakin(deg['Kazanc sn'],BEK.olcu['Kazanc sn'],5e-4),'Kazanc sn = '+vkSay(deg['Kazanc sn'],3)+' (beklenen '+vkSay(BEK.olcu['Kazanc sn'],3)+')']);
  L.push([yakin(deg['Kazanc %'],BEK.olcu['Kazanc %'],5e-5),'Kazanc % = %'+vkSay((deg['Kazanc %']||0)*100,2)+' (beklenen %'+vkSay(BEK.olcu['Kazanc %']*100,2)+')']);
  let q=null;try{q=D.query({rows:[{t:'Toplama',c:'bolge'}],measures:ms,values:['[Eski Ort]','[Yeni Ort]','[Kazanc sn]'],totals:false});}catch(e){}
  const bolgeOk=q&&q.rows.length===3&&q.rows.every(r=>yakin(r.vals[2],BEK.bolge[r.keys[0]]['Kazanc sn'],5e-4));
  L.push([!!bolgeOk,'Bölge kırılımı (bağlam geçişiyle) Python ile aynı']);
  $('#kontrol').innerHTML=L.map(([c,t])=>'<li class="'+(c?'ok':'no')+'">'+vkEsc(t)+'</li>').join('');
  if(!hata){$('#pano').hidden=false;$('#kartlar').innerHTML=[['Eski ort.',deg['Eski Ort'],' sn'],['Yeni ort.',deg['Yeni Ort'],' sn'],['Kazanç',deg['Kazanc sn'],' sn'],['Kazanç %',(deg['Kazanc %']||0)*100,'']].map(([a,v,b])=>'<div><span>'+a+'</span><b>'+(b?'':'%')+vkSay(v,2)+b+'</b></div>').join('');
    if(q)$('#grafik').innerHTML=grafik(q.rows);
    try{const m=D.query({rows:[{t:'Toplama',c:'vardiya'}],measures:ms,values:['[Eski Ort]','[Yeni Ort]','[Kazanc sn]'],totals:true});$('#matris').innerHTML=vkTablo(['vardiya','Eski Ort','Yeni Ort','Kazanc sn'],[...m.rows.map(r=>[r.keys[0],...r.vals]),['Toplam',...(m.total||[])]],[1,2,3]);}catch(e){$('#matris').textContent=e.message;}}
  const tamam=L.every(x=>x[0]);if(tamam){vkYaz('pbi',{kaynak:KAY.kaynak,olcu:{'Eski Ort':deg['Eski Ort'],'Yeni Ort':deg['Yeni Ort'],'Kazanc sn':deg['Kazanc sn'],'Kazanc %':deg['Kazanc %']}});vkAdimlar();dur('Tamam: pano beklenenle aynı ('+(KAY.kaynak==='kendi'?'senin SQL çıktınla':'örnek veriyle')+'). 4. adıma geçebilirsin.');}else dur(hata?'Bir ölçü hata verdi; kutunun altındaki mesaja bak.':'Ölçüler çalıştı ama sonuç beklenenden farklı.');}
$('#calistir').onclick=calistir;
$('#cozum').onclick=()=>{document.querySelectorAll('[data-olcu]').forEach(t=>t.value=COZUM[t.dataset.olcu]);dur('Çözüm yazıldı. “Ölçüleri çalıştır” ile dene.');};
$('#indir').onclick=()=>vkCsvIndir('toplama_temiz.csv',veri.cols,veri.rows);
(function(){const s=vkOku().python,e=$('#gelenDurum');if(!s||!s.tamam)return;const g=s.grup||{},ayni=['eski','yeni'].every(k=>g[k]&&g[k].count===BEK_PY[k].count&&Math.abs(g[k].mean-BEK_PY[k].mean)<1e-4);e.className='vk-et '+(ayni?'ok':'no');e.textContent=ayni?'✓ senin Python denetimin bununla aynı':'Senin denetimin farklıydı; bu adım beklenen veriyle devam eder';})();
"""
)

# ----------------------------------------------------------------- 4. İstatistik
st_govde = f"""<p class="vk-l">Pano yeni düzenin satır başına {tr(OL["Kazanc sn"])} sn kazandırdığını gösteriyor. Müdürün iki sorusu var: <b>Bu fark gerçek mi?</b> ve <b>Diğer depolara yaymaya yeter mi?</b> İlki istatistiksel, ikincisi operasyonel bir sorudur; cevapları farklı olabilir.</p>
<section class="vk-k vk-gelen" aria-labelledby="gelen"><h2 id="gelen">Önceki adımdan gelen: pano ölçüleri <span class="vk-et bek" id="gelenDurum">3. adım henüz çözülmedi</span></h2>
<div class="vk-kart"><div><span>Eski ort.</span><b>{tr(OL["Eski Ort"])} sn</b></div><div><span>Yeni ort.</span><b>{tr(OL["Yeni Ort"])} sn</b></div><div><span>Kazanç</span><b>{tr(OL["Kazanc sn"])} sn</b></div><div><span>Kazanç %</span><b>%{tr(OL["Kazanc %"] * 100)}</b></div></div>
<p>Test hangi tabloyla yapılsın?</p><div id="kaynak"></div>
<p class="vk-not">Beklenen tabloda {tr(E["temiz"], 0)} satır var ({tr(PG["eski"]["count"], 0)} eski, {tr(PG["yeni"]["count"], 0)} yeni).</p></section>
<section class="vk-k" aria-labelledby="gorev"><h2 id="gorev">Görev: üç soruyu ayrı yanıtla</h2>
<ol><li><b>Ne gözlendi?</b> Eski ve yeni ortalama arasındaki fark ne kadar, belirsizliği ne kadar? Varyanslar eşit varsayılmadan (Welch) iki örneklem t-testi ve güven aralığı.</li>
<li><b>Hedef karşılandı mı?</b> Yeni düzeni yaymanın raf, etiket ve eğitim maliyeti, satır başına <b>en az 4 sn</b> kazançla geri dönüyor. Farkın güven aralığı bu eşiğe göre nerede?</li>
<li><b>Farkı yeni düzene bağlayabilir miyiz?</b> Eylül ile Ekim karşılaştırılıyor; iki dönem arasında düzenden başka ne değişmiş olabilir? Bunu test cevaplamaz, sen gerekçelendirirsin.</li></ol>
<div class="vk-iki"><label>Operasyon eşiği (sn/satır)<input id="esik" type="number" min="0.5" max="10" step="0.5" value="{ST["esik"]:g}" style="display:block;width:100%;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;margin-top:4px"></label>
<label>Güven düzeyi<select id="guven" style="display:block;width:100%;font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;margin-top:4px"><option value="0.90">%90</option><option value="0.95" selected>%95</option><option value="0.99">%99</option></select></label></div>
<div class="vk-btn"><button class="p" id="calistir">Testi çalıştır</button></div>
<div class="vk-dur" id="dur" role="status" aria-live="polite">İstatistik motoru hazırlanıyor…</div>
<div id="sonuc" hidden><div class="vk-kart" id="kartlar"></div><figure style="margin:8px 0"><figcaption class="vk-not">Farkın güven aralığı (sn/satır); 0 = fark yok, kesik çizgi = operasyon eşiği</figcaption><div id="aralik"></div></figure>
<div id="karar" class="vk-k c" style="margin:10px 0"></div><ul class="vk-chk" id="kontrol" aria-label="Denetim"></ul></div></section>
<section class="vk-k" aria-labelledby="bek"><h2 id="bek">Beklenen çıktı (%95, eşik 4 sn)</h2>
<div class="vk-tw"><table><tbody><tr><th>Fark (eski − yeni)</th><td class="n">{tr(ST["fark"], 3)} sn</td></tr><tr><th>Welch t · serbestlik derecesi</th><td class="n">{tr(ST["t"], 3)} · {tr(ST["df"], 1)}</td></tr><tr><th>p değeri (iki yönlü)</th><td class="n">{tr(ST["p"], 4)}</td></tr><tr><th>%95 güven aralığı</th><td class="n">{tr(ST["alt"], 2)} – {tr(ST["ust"], 2)} sn</td></tr><tr><th>Aylık kazanç ({tr(ST["satir_ay"], 0)} satır)</th><td class="n">≈ {tr(ST["aylik_saat"], 1)} saat (eşik {tr(ST["esik_saat"], 1)} saat)</td></tr></tbody></table></div>
<p class="vk-not">4 sn'lik farkı %80 güçle görmek için grup başına yaklaşık <span id="gerekN">—</span> satır yeterdi, elimizde {tr(PG["eski"]["count"], 0)} var. Sorun örneklem küçüklüğü değil, farkın küçüklüğü.</p></section>
<section class="vk-k c" aria-labelledby="yaz"><h2 id="yaz">Kararını yaz</h2>
<p>Müdüre gidecek iki üç cümleyi yaz: ne gözlendi, hedef karşılandı mı, fark yeni düzene bağlanabilir mi? Kaydedince uzman değerlendirmesi açılır ve kendi metninle karşılaştırırsın.</p>
<label for="metin" class="vk-not">Kararın ve gerekçen</label>
<textarea id="metin" class="vk-ed" style="min-height:130px;font-family:var(--f-b);font-size:1rem" placeholder="Örn. Ekim'de toplama süresi … sn kısaldı; …"></textarea>
<div class="vk-btn"><button class="p" id="kaydet" disabled>Kaydet ve uzman değerlendirmesini aç</button><span class="vk-not" id="metinNot" style="align-self:center">En az 60 karakter yaz.</span></div>
<div id="uzman" hidden>
<h3>Metnin üç soruyu karşılıyor mu?</h3><ul class="vk-chk" id="ozdeg" aria-label="Öz değerlendirme"></ul>
<p class="vk-not">Bu işaretler yalnızca metinde geçen sözcüklere bakar; puan değildir. Asıl karşılaştırmayı aşağıdaki değerlendirmeyle sen yap.</p>
<h3>Uzman değerlendirmesi</h3>
<p><b>1. Ne gözlendi?</b> Ekim'de (yeni düzen) satır başına toplama süresi ortalama {tr(ST["fark"], 3)} sn kısaldı; %95 güven aralığı {tr(ST["alt"], 2)}–{tr(ST["ust"], 2)} sn. p = {tr(ST["p"], 3)}, farkın sıfır olmadığına işaret ediyor; ama alt sınır {tr(ST["alt"], 2)} sn'ye kadar iniyor, yani etki çok küçük de olabilir. p değeri etkinin büyüklüğünü ya da önemini söylemez; büyüklüğü güven aralığı gösterir.</p>
<p><b>2. Hedef karşılandı mı?</b> Hayır. Aralığın tamamı 4 sn hedefinin altında; en iyimser tahmin ({tr(ST["ust"], 2)} sn) bile hedefin yarısı kadar. Aylık ≈ {tr(ST["aylik_saat"], 1)} saatlik kazanç, {tr(ST["esik_saat"], 1)} saatlik geri dönüş eşiğine yetmiyor.</p>
<p><b>3. Farkı yeni düzene bağlayabilir miyiz?</b> Ancak dikkatle. 2. adımda vardiya karışımının iki dönemde aynı olduğunu (%{tr(VP["eski"]["Gündüz"] * 100, 0)} gündüz) ve farkın iki vardiyada da aynı yönde olduğunu gördük; vardiya açıklaması zayıf. Ama bu bir önce–sonra karşılaştırması: Eylül ile Ekim arasında sipariş ve ürün karışımı, toplayıcıların deneyimi ya da sezon da değişmiş olabilir. Yeni düzenin katkısını ayırmak için aynı dönemde eski düzende kalan bir bölge ya da depoyla, benzer vardiya ve toplayıcılar üzerinden karşılaştırma gerekir.</p>
<p><b>Örnek karar metni:</b> “Ekim'de toplama süresi satır başına ortalama {tr(ST["fark"], 2)} sn kısaldı (%95 GA {tr(ST["alt"], 2)}–{tr(ST["ust"], 2)} sn). Aralığın tamamı 4 sn'lik yayma eşiğinin altında; yeni düzeni diğer depolara yaymak için yeterli değil. Gebze'de düzen kalsın; kazancın düzenden geldiğini ayırmak için benzer vardiyalarda, eski düzende kalan bir bölgeyle aynı dönemde karşılaştırma yapılsın.”</p>
<p class="vk-not">p değeri ile etki büyüklüğünü ayrı değerlendirme ilkesi için: <a href="https://doi.org/10.1080/00031305.2016.1154108" rel="noopener">Amerikan İstatistik Derneği, p değerleri bildirgesi (2016)</a>.</p>
</div>
</section>
<section class="vk-k" aria-labelledby="ornek2"><h2 id="ornek2">İkinci örnek: İzmir deposu, aynı görünen kazanç</h2>
<p>İzmir deposunda da Ekim'de aynı raf değişikliği yapıldı. Toplam ortalama yine düştü: eski {tr(E2)} sn, yeni {tr(Y2)} sn, fark <b>{tr(ST2["fark"], 2)} sn</b> (p = {tr(ST2["p"], 3)}, %95 GA {tr(ST2["alt"], 2)}–{tr(ST2["ust"], 2)} sn). Gebze'ye çok benziyor. Bir farkla: Ekim'de gece vardiyasının payı değişti ve gece vardiyasında satır başına süre daha uzun.</p>
<div class="vk-tw"><table><thead><tr><th>vardiya payı</th><th class="n">Eylül (eski)</th><th class="n">Ekim (yeni)</th></tr></thead><tbody><tr><td>Gündüz</td><td class="n">%{tr((1 - ST2["gece_payi"]["eski"]) * 100, 0)}</td><td class="n">%{tr((1 - ST2["gece_payi"]["yeni"]) * 100, 0)}</td></tr><tr><td>Gece</td><td class="n">%{tr(ST2["gece_payi"]["eski"] * 100, 0)}</td><td class="n">%{tr(ST2["gece_payi"]["yeni"] * 100, 0)}</td></tr></tbody></table></div>
<p><b>Görev:</b> “Ortalama süre düştü” ile “raf değişikliği düşüşe yol açtı” aynı cümle değil. Farkı vardiya içinde karşılaştır, sonra bu veride hangisini söyleyebileceğini yaz.</p>
<div class="vk-btn"><button class="p" id="katmanBtn">Vardiya içinde karşılaştır</button></div>
<div id="katman" hidden><div class="vk-tw"><table><thead><tr><th>vardiya</th><th class="n">eski</th><th class="n">yeni</th><th class="n">fark</th><th class="n">%95 GA</th><th class="n">p</th></tr></thead><tbody id="katmanSat"></tbody></table></div>
<div class="vk-kart" id="katmanKart"></div><ul class="vk-chk" id="katmanKontrol" aria-label="Denetim"></ul></div>
<label for="metin2" class="vk-not">İzmir için açıklaman</label>
<textarea id="metin2" class="vk-ed" style="min-height:110px;font-family:var(--f-b);font-size:1rem" placeholder="Örn. İzmir'de ortalama süre … sn düştü; ama vardiya içinde …"></textarea>
<div class="vk-btn"><button class="p" id="kaydet2" disabled>Kaydet ve uzman değerlendirmesini aç</button><span class="vk-not" id="metin2Not" style="align-self:center">En az 60 karakter yaz.</span></div>
<div id="uzman2" hidden>
<h3>Metnin iki ifadeyi ayırıyor mu?</h3><ul class="vk-chk" id="ozdeg2" aria-label="Öz değerlendirme"></ul>
<p class="vk-not">İşaretler yalnızca metindeki sözcüklere bakar; puan değildir.</p>
<h3>Uzman değerlendirmesi</h3>
<p><b>“Ortalama süre düştü”: doğru.</b> Toplamda {tr(ST2["fark"], 2)} sn düşüş var ve p = {tr(ST2["p"], 3)}; bu bir gözlem.</p>
<p><b>“Raf değişikliği düşüşe yol açtı”: bu veri desteklemiyor.</b> Vardiya içinde fark yok denecek kadar küçük: gündüz {tr(ST2["katman"]["Gündüz"]["fark"], 2)} sn (%95 GA {tr(ST2["katman"]["Gündüz"]["alt"], 2)}–{tr(ST2["katman"]["Gündüz"]["ust"], 2)}), gece {tr(ST2["katman"]["Gece"]["fark"], 2)} sn (%95 GA {tr(ST2["katman"]["Gece"]["alt"], 2)}–{tr(ST2["katman"]["Gece"]["ust"], 2)}); ikisi de sıfırı içeriyor. Vardiya karışımı sabit tutulunca fark {tr(ST2["duzeltilmis"], 2)} sn. Toplam düşüşün yaklaşık {tr(ST2["karisim_etkisi"], 2)} sn'si yavaş gece vardiyasının payının %{tr(ST2["gece_payi"]["eski"] * 100, 0)}'ten %{tr(ST2["gece_payi"]["yeni"] * 100, 0)}'e inmesinden geliyor (karışım etkisi). Toplam ortalama, grupların payı değiştiğinde grupların hiçbiri değişmeden de düşebilir.</p>
<p><b>Gebze ile farkı:</b> Gebze'de vardiya payları iki dönemde aynıydı ve fark iki vardiyada da aynı yöndeydi; orada vardiya açıklaması zayıftı. İzmir'de güçlü. Aynı t-testi sonucu iki depoda farklı karara götürür; karar testten değil, karşılaştırmanın adil olup olmadığından gelir.</p>
<p><b>Örnek metin:</b> “İzmir'de ortalama toplama süresi {tr(ST2["fark"], 2)} sn düştü, ama bu düşüş raf düzeninden değil vardiya karışımından geliyor: Ekim'de gece payı %{tr(ST2["gece_payi"]["eski"] * 100, 0)}'ten %{tr(ST2["gece_payi"]["yeni"] * 100, 0)}'e indi ve aynı vardiya içinde eski ile yeni düzen arasında fark yok. Bu veriyle düzenin işe yaradığı söylenemez; aynı vardiyalarda önce–sonra ölçüm gerekir.”</p>
</div>
<div class="vk-son"><span class="vk-not" id="bitis">Dört adımı da çözünce vaka tamamlanır.</span><a class="vk-go" href="/#vaka">Vakayı bitir, Kesit'e dön →</a></div></section>"""
st_betik = (
    "const CSV="
    + J(CSV)
    + ";const BEK="
    + J(ST)
    + ";const BEK_PBI="
    + J(OL)
    + ";const CSV2="
    + J(CSV2)
    + ";const BEK2="
    + J(ST2)
    + r""";
const $=s=>document.querySelector(s), dur=t=>$('#dur').textContent=t;
let eski=[],yeni=[];
const ayir=csv=>{const v=vkCsvOku(csv),iD=v.cols.indexOf('duzen'),iS=v.cols.indexOf('sure_sn');eski=v.rows.filter(r=>r[iD]==='eski').map(r=>+r[iS]);yeni=v.rows.filter(r=>r[iD]==='yeni').map(r=>+r[iS]);};
let KAY=vkKaynak($('#kaynak'),CSV,k=>{KAY=k;ayir(k.csv);gucN();$('#sonuc').hidden=true;dur('Veri değişti: '+(k.kaynak==='kendi'?'kendi SQL çıktın':'örnek veri')+'. Testi yeniden çalıştır.');});
ayir(KAY.csv);
const ort=a=>a.reduce((s,x)=>s+x,0)/a.length,vr=a=>{const m=ort(a);return a.reduce((s,x)=>s+(x-m)**2,0)/(a.length-1)};
// Kesit İstatistik motoru (docs/analysis-engine.js): t dağılımı (tP, tInv) ve normal ters fonksiyon.
// Motorun ttest() fonksiyonu alıştırmalar için en çok 500 gözlem alır; burada aynı Welch formülü motorun dağılım fonksiyonlarıyla kurulur.
function welch(a,b,g){const A=window.AnalysisEngine,va=vr(a)/a.length,vb=vr(b)/b.length,se=Math.sqrt(va+vb),df=(va+vb)**2/(va**2/(a.length-1)+vb**2/(b.length-1)),d=ort(a)-ort(b),t=d/se,k=A.tInv((1+g)/2,df);return {d,se,df,t,p:A.tP(t,df),alt:d-k*se,ust:d+k*se};}
function aralik(r,esik){const W=Math.max(300,Math.round(document.querySelector('#aralik').clientWidth||560)),H=96,lo=Math.min(-1,r.alt-.5),hi=Math.max(esik+1,r.ust+.5),x=u=>20+(u-lo)/(hi-lo)*(W-40);let s='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Güven aralığı '+vkSay(r.alt,2)+' ile '+vkSay(r.ust,2)+' sn arası; eşik '+esik+' sn" style="width:100%;height:auto">';
  for(let t=Math.ceil(lo);t<=hi;t++)s+='<line x1="'+x(t)+'" x2="'+x(t)+'" y1="66" y2="72" stroke="#5A574E"/><text x="'+x(t)+'" y="88" text-anchor="middle" font-size="12" fill="#5A574E">'+t+'</text>';
  s+='<line x1="20" x2="'+(W-20)+'" y1="66" y2="66" stroke="#5A574E"/><line x1="'+x(0)+'" x2="'+x(0)+'" y1="10" y2="66" stroke="#1B1A16"/><text x="'+(x(0)+4)+'" y="18" font-size="12" fill="#1B1A16">fark yok</text>';
  s+='<line x1="'+x(esik)+'" x2="'+x(esik)+'" y1="10" y2="66" stroke="#B3261E" stroke-width="2" stroke-dasharray="5 4"/><text x="'+(x(esik)-4)+'" y="18" text-anchor="end" font-size="12" fill="#B3261E">eşik '+vkSay(esik,1)+' sn</text>';
  s+='<line x1="'+x(r.alt)+'" x2="'+x(r.ust)+'" y1="42" y2="42" stroke="#136B49" stroke-width="6" stroke-linecap="round"/><circle cx="'+x(r.d)+'" cy="42" r="7" fill="#136B49"/></svg>';return s;}
function karar(r,esik,g){const a=1-g,anl=r.p<a&&r.alt>0;let op;
  if(r.ust<esik)op={k:'yetersiz',t:'Güven aralığının üst sınırı ('+vkSay(r.ust,2)+' sn) eşiğin altında: gerçek kazanç büyük olasılıkla '+vkSay(esik,1)+' sn’ye ulaşmıyor. <b>Operasyonel olarak yeterli değil.</b>'};
  else if(r.alt>=esik)op={k:'yeterli',t:'Güven aralığının alt sınırı ('+vkSay(r.alt,2)+' sn) eşiğin üstünde. <b>Operasyonel olarak yeterli.</b>'};
  else op={k:'belirsiz',t:'Eşik güven aralığının içinde ('+vkSay(r.alt,2)+' – '+vkSay(r.ust,2)+' sn). <b>Veri karar için yetmiyor;</b> ölçüme devam et ya da eşiği netleştir.'};
  const gozlem='Yeni düzende ortalama süre satır başına '+vkSay(r.d,3)+' sn daha '+(r.d>=0?'kısa':'uzun')+'; %'+vkSay(g*100,0)+' güven aralığı '+vkSay(r.alt,2)+' – '+vkSay(r.ust,2)+' sn. '+(anl?'p = '+vkSay(r.p,4)+' &lt; '+vkSay(a,2)+': farkın sıfır olmadığına işaret ediyor; büyüklüğünü aralık gösterir.':'p = '+vkSay(r.p,4)+' ≥ '+vkSay(a,2)+': aralık sıfırı içeriyor, farkın rastlantı olmadığını söyleyemeyiz.');
  return {anl,op,html:'<div class="vk-soru"><h3>1. Ne gözlendi?</h3><p>'+gozlem+'</p><h3>2. Hedef karşılandı mı?</h3><p>'+op.t+'</p><h3>3. Farkı yeni düzene bağlayabilir miyiz?</h3><p>Test bunu tek başına cevaplamaz: iki dönem arasında düzenden başka neyin değiştiğini düşün ve aşağıda <a href="#yaz">kararını yaz</a>.</p></div>'};}
function calistir(){if(!window.AnalysisEngine){dur('Motor daha yüklenmedi.');return;}const esik=Number($('#esik').value),g=Number($('#guven').value);if(!(esik>0)){dur('Eşik pozitif bir sayı olmalı.');return;}
  const r=welch(eski,yeni,g),k=karar(r,esik,g);$('#sonuc').hidden=false;
  $('#kartlar').innerHTML=[['Fark',vkSay(r.d,3)+' sn'],['t · sd',vkSay(r.t,3)+' · '+vkSay(r.df,0)],['p değeri',vkSay(r.p,4)],['%'+vkSay(g*100,0)+' GA',vkSay(r.alt,2)+' – '+vkSay(r.ust,2)]].map(([a,b])=>'<div><span>'+a+'</span><b>'+b+'</b></div>').join('');
  $('#aralik').innerHTML=aralik(r,esik);$('#karar').innerHTML=k.html;
  const std=g===.95&&esik===BEK.esik,L=[[Math.abs(r.d-BEK.fark)<1e-9,'Fark Power BI kazancıyla aynı ('+vkSay(r.d,4)+' sn)']];
  if(std)L.push([Math.abs(r.p-BEK.p)<1e-6&&Math.abs(r.ust-BEK.ust)<1e-6,'p ve güven aralığı SciPy ile aynı (p = '+vkSay(BEK.p,4)+', üst sınır '+vkSay(BEK.ust,3)+')']);
  $('#kontrol').innerHTML=L.map(([c,t])=>'<li class="'+(c?'ok':'no')+'">'+vkEsc(t)+'</li>').join('');
  if(std&&L.every(x=>x[0])){vkYaz('istatistik',Object.assign({},vkOku().istatistik,{karar:'istatistiksel fark var, operasyonel olarak yeterli değil',p:r.p,ust:r.ust,kaynak:KAY.kaynak}));vkAdimlar();bitis();dur('Tamam. Eşiği ya da güven düzeyini değiştirip kararın nasıl değiştiğine bak.');}
  else dur(std?'Sonuç beklenenden farklı.':'Farklı eşik/güven düzeyiyle hesaplandı; denetim %95 ve 4 sn için yapılır.');}
function bitis(){const s=vkOku(),n=['sql','python','pbi','istatistik'].filter(k=>s[k]&&s[k].tamam).length;$('#bitis').textContent=n===4?'✓ Dört adımın hepsi çözüldü: vaka tamamlandı.':n+'/4 adım çözüldü.';}
$('#calistir').onclick=calistir;
function gucN(){const A=window.AnalysisEngine;if(!A||!eski.length||!yeni.length)return;const z=A.normalInv,sd=Math.sqrt((vr(eski)+vr(yeni))/2),n=Math.ceil(2*((z(.975)+z(.8))*sd/BEK.esik)**2);$('#gerekN').textContent=vkSay(n);}
const metin=$('#metin'),kaydet=$('#kaydet');
const onceki=(vkOku().istatistik||{}).metin;if(onceki){metin.value=onceki;}
const metinDurum=()=>{const n=metin.value.trim().length;kaydet.disabled=n<60;$('#metinNot').textContent=n<60?'En az 60 karakter yaz ('+n+'/60).':'Hazır.';};
metin.addEventListener('input',metinDurum);metinDurum();
function uzmanAc(){const t=metin.value.toLocaleLowerCase('tr-TR'),M=[[/aral|güven|ga\b|\d/,'Farkın büyüklüğünü ve belirsizliğini (aralık) yazdın'],[/hedef|eşik|esik|4 ?sn|yeterli|yaym/,'Hedefle (4 sn) karşılaştırdın'],[/neden|bağla|bagla|vardiya|karışım|karisim|sipariş|siparis|mevsim|sezon|kontrol|ayır|ayir|başka|baska/,'Farkı düzene bağlamanın sınırını belirttin']];
  $('#ozdeg').innerHTML=M.map(([re,ad])=>{const v=re.test(t);return '<li class="'+(v?'ok':'no')+'">'+ad+(v?'':' : metninde göremedim')+'</li>';}).join('');$('#uzman').hidden=false;}
kaydet.onclick=()=>{const s=vkOku();s.v=1;s.istatistik=Object.assign({},s.istatistik,{metin:metin.value.trim()});try{localStorage.setItem(VK_KEY,JSON.stringify(s))}catch(e){}uzmanAc();$('#uzman').scrollIntoView({behavior:'smooth',block:'start'});};
if(onceki&&onceki.length>=60)uzmanAc();
// İkinci örnek (İzmir): vardiya içinde Welch farkı ve vardiya karışımı sabit tutulmuş fark; SciPy değerleriyle denetlenir.
function katmanla(){if(!window.AnalysisEngine){dur('Motor daha yüklenmedi.');return;}const v=vkCsvOku(CSV2),iV=v.cols.indexOf('vardiya'),iD=v.cols.indexOf('duzen'),iS=v.cols.indexOf('sure_sn');
  const al=(d,va)=>v.rows.filter(r=>r[iD]===d&&(!va||r[iV]===va)).map(r=>+r[iS]),sat=[],L=[];let duz=0;
  for(const va of ['Gündüz','Gece']){const r=welch(al('eski',va),al('yeni',va),.95),b=BEK2.katman[va],w=BEK2.agirlik[va];duz+=w*r.d;
    sat.push('<tr><td>'+va+'</td><td class="n">'+vkSay(ort(al('eski',va)),2)+'</td><td class="n">'+vkSay(ort(al('yeni',va)),2)+'</td><td class="n">'+vkSay(r.d,2)+'</td><td class="n">'+vkSay(r.alt,2)+' – '+vkSay(r.ust,2)+'</td><td class="n">'+vkSay(r.p,3)+'</td></tr>');
    L.push([Math.abs(r.d-b.fark)<1e-9&&Math.abs(r.p-b.p)<1e-6&&Math.abs(r.ust-b.ust)<1e-6,va+' vardiyası SciPy ile aynı']);}
  const top=welch(al('eski'),al('yeni'),.95);L.push([Math.abs(duz-BEK2.duzeltilmis)<1e-9,'Karışımı sabit fark SciPy/pandas ile aynı']);
  $('#katmanSat').innerHTML=sat.join('');
  $('#katmanKart').innerHTML=[['Toplam fark',vkSay(top.d,2)+' sn'],['Vardiya karışımı sabit',vkSay(duz,2)+' sn'],['Karışımdan gelen',vkSay(top.d-duz,2)+' sn']].map(([a,b])=>'<div><span>'+a+'</span><b>'+b+'</b></div>').join('');
  $('#katmanKontrol').innerHTML=L.map(([c,t])=>'<li class="'+(c?'ok':'no')+'">'+vkEsc(t)+'</li>').join('');$('#katman').hidden=false;}
$('#katmanBtn').onclick=katmanla;
const metin2=$('#metin2'),kaydet2=$('#kaydet2'),onceki2=((vkOku().istatistik||{}).ornek2||{}).metin;if(onceki2)metin2.value=onceki2;
const metin2Durum=()=>{const n=metin2.value.trim().length;kaydet2.disabled=n<60;$('#metin2Not').textContent=n<60?'En az 60 karakter yaz ('+n+'/60).':'Hazır.';};
metin2.addEventListener('input',metin2Durum);metin2Durum();
function uzman2Ac(){const t=metin2.value.toLocaleLowerCase('tr-TR'),M=[[/düş|dus|kısal|kisal|azal/,'Ortalamanın düştüğünü (gözlem) yazdın'],[/vardiya|gece|karışım|karisim|pay/,'Vardiya karışımının değiştiğini belirttin'],[/içinde|icinde|aynı vardiya|ayni vardiya|sabit|katman|ayrı ayrı|ayri ayri/,'Vardiya içi karşılaştırmaya dayandın'],[/söylenemez|soylenemez|bağlan|baglan|neden|yol aç|yol ac|kanıt|kanit|desteklem|değil|degil/,'Nedensellik iddiasının sınırını yazdın']];
  $('#ozdeg2').innerHTML=M.map(([re,ad])=>{const v=re.test(t);return '<li class="'+(v?'ok':'no')+'">'+ad+(v?'':' : metninde göremedim')+'</li>';}).join('');$('#uzman2').hidden=false;}
kaydet2.onclick=()=>{const s=vkOku();s.v=1;s.istatistik=Object.assign({},s.istatistik,{ornek2:{metin:metin2.value.trim(),zaman:new Date().toISOString()}});try{localStorage.setItem(VK_KEY,JSON.stringify(s))}catch(e){}uzman2Ac();$('#uzman2').scrollIntoView({behavior:'smooth',block:'start'});};
if(onceki2&&onceki2.length>=60)uzman2Ac();
const sc=document.createElement('script');sc.src='../../docs/analysis-engine.js';sc.onload=()=>{gucN();dur('Motor hazır. Testi çalıştır.');};sc.onerror=()=>dur('İstatistik motoru yüklenemedi.');document.head.appendChild(sc);
(function(){const s=vkOku().pbi,e=$('#gelenDurum');bitis();if(!s||!s.tamam)return;const ayni=s.olcu&&Math.abs(s.olcu['Kazanc sn']-BEK_PBI['Kazanc sn'])<5e-4;e.className='vk-et '+(ayni?'ok':'no');e.textContent=ayni?'✓ senin panon bununla aynı':'Senin panon farklıydı; test beklenen veriyle yapılır';})();
"""
)

HEDEF = {
    "sql": ROOT / "kesit-sql/vaka/depo",
    "python": ROOT / "kesit-python/vaka/depo",
    "pbi": ROOT / "kesit-powerbi/vaka/depo",
    "istatistik": ROOT / "kesit-istatistik/vaka/depo",
}
SAYFA = {
    "sql": sayfa("sql", "SQL ile veriyi hazırla", "Depo toplama vakası, 1. adım: el terminali kayıtlarını SQL ile temizle ve özetle.", sql_govde, sql_betik, '<script src="../../vendor/sql-asm.js"></script>'),
    "python": sayfa("python", "Python ile veriyi denetle", "Depo toplama vakası, 2. adım: SQL çıktısını pandas ile denetle; temizlik ve karşılaştırılabilirlik.", py_govde, py_betik),
    "pbi": sayfa("pbi", "Power BI'da göster", "Depo toplama vakası, 3. adım: DAX ölçüleriyle kazancı panoda göster.", pbi_govde, pbi_betik, PBI_CSS),
    "istatistik": sayfa("istatistik", "İstatistikle karar sınırını açıkla", "Depo toplama vakası, 4. adım: istatistiksel fark var ama operasyonel olarak yeterli mi?", st_govde, st_betik),
}
for k, d in HEDEF.items():
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(SAYFA[k], encoding="utf-8")
    # İkinci örnek (istatistik2) yalnız İstatistik sayfasında kullanılır; diğer depolara gerekmeyen anahtar yazılmaz.
    (d / "beklenen.json").write_text((K / "beklenen.json").read_text(encoding="utf-8") if k == "istatistik"
                                     else json.dumps({x: y for x, y in B.items() if x != "istatistik2"}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(k, d / "index.html", len(SAYFA[k]) // 1024, "KB")

# Power BI: DAX motorunun yayındaki paketle birebir kopyası (tests/vaka-depo.cjs aynılığı denetler)
_b = (ROOT / "kesit-powerbi/kesit.js").read_text(encoding="utf-8")
import re as _re
_p = _re.split(r"/\* ===== ([^\n]+) ===== \*/", _b)
_dax = _p[_p.index("dax.js") + 1]
(HEDEF["pbi"] / "dax.js").write_text(
    "/* Kesit Power BI DAX benzetim motoru: kesit.js paketindeki dax.js bölümünün birebir kopyası.\n"
    "   Elle düzenleme. kesit.js değişince: node tests/vaka-depo.cjs --yaz */" + _dax,
    encoding="utf-8",
)
print("dax.js", len(_dax))
