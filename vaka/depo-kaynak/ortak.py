"""Dört adım sayfasının ortak parçaları: stil, başlık, adım çubuğu ve ilerleme kaydı (localStorage)."""

ADIMLAR = [
    ("sql", "SQL", "Veriyi hazırla", "/kesit-sql/vaka/depo/"),
    ("python", "Python", "Veriyi denetle", "/kesit-python/vaka/depo/"),
    ("pbi", "Power BI", "Panoda göster", "/kesit-powerbi/vaka/depo/"),
    ("istatistik", "İstatistik", "Karar sınırını açıkla", "/kesit-istatistik/vaka/depo/"),
]
RENK = {"sql": "#B3261E", "python": "#2A56B5", "pbi": "#7A5600", "istatistik": "#136B49"}

CSS = """
:root{--bg:#F1F0EC;--surface:#fff;--surface-2:#F7F6F2;--ink:#1B1A16;--muted:#5A574E;--line:#DEDBD2;--ok:#136B49;--bad:#B3261E;--warn:#7A5600;--f-d:'Bricolage Grotesque',system-ui,sans-serif;--f-b:'IBM Plex Sans',system-ui,sans-serif;--f-m:'JetBrains Mono',ui-monospace,monospace}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.6 var(--f-b)}
a{color:inherit}
.vk-skip{position:absolute;left:-999px;top:8px;z-index:9;background:var(--ink);color:#fff;padding:8px 12px;border-radius:6px}.vk-skip:focus{left:8px}
.vk-w{max-width:1040px;margin:0 auto;padding:0 20px 48px}
.vk-h{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:20px 0 6px;flex-wrap:wrap}
.vk-b{display:flex;align-items:center;gap:8px;font:800 1.15rem var(--f-d);text-decoration:none}
.vk-h nav{font-size:.9rem;display:flex;gap:14px;flex-wrap:wrap}.vk-h nav a{font-weight:600}
.vk-e{display:inline-block;font:600 .8rem var(--f-b);letter-spacing:.04em;text-transform:uppercase;color:var(--c);margin-top:18px}
h1{font:800 clamp(1.8rem,4.6vw,2.7rem)/1.1 var(--f-d);letter-spacing:-.02em;margin:6px 0 10px}
h2{font:800 1.3rem/1.25 var(--f-d);margin:0 0 8px}
h3{font:700 1.02rem var(--f-d);margin:16px 0 6px}
.vk-l{color:var(--muted);max-width:70ch;margin:0 0 6px;font-size:1.05rem}
.vk-adim{list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:20px 0;padding:0;counter-reset:a}
.vk-adim li{counter-increment:a}
.vk-adim a{display:flex;flex-direction:column;gap:2px;height:100%;padding:10px 12px;border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:10px;background:var(--surface);text-decoration:none;font-size:.85rem;color:var(--muted)}
.vk-adim a b{font:700 .98rem var(--f-d);color:var(--ink)}
.vk-adim a b::before{content:counter(a) ". "}
.vk-adim a[aria-current]{background:var(--surface-2);outline:2px solid var(--ac);outline-offset:-1px}
.vk-adim .ok{color:var(--ok);font-weight:600}
.vk-k{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:14px 0}
.vk-k.c{border-left:4px solid var(--c)}
.vk-k p{margin:0 0 8px}.vk-k p:last-child{margin:0}
.vk-k ul,.vk-k ol{margin:6px 0 8px;padding-left:20px}
.vk-iki{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}
table{border-collapse:collapse;width:100%;font-size:.92rem;font-variant-numeric:tabular-nums}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:.85rem}
td.n,th.n{text-align:right}
.vk-tw{overflow-x:auto;max-width:100%}
code,pre,textarea.vk-ed{font-family:var(--f-m);font-size:.88rem}
code{background:var(--surface-2);border:1px solid var(--line);border-radius:4px;padding:0 4px}
pre{background:#1F1E1A;color:#F4F2EA;border-radius:10px;padding:12px 14px;overflow-x:auto;margin:8px 0;white-space:pre-wrap;word-break:break-word}
textarea.vk-ed{width:100%;min-height:260px;border:1px solid var(--line);border-radius:10px;padding:12px;background:#FCFBF8;color:var(--ink);line-height:1.5;resize:vertical;tab-size:2}
textarea.vk-ed:focus{outline:2px solid var(--c);outline-offset:1px}
.vk-btn{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
button,.vk-go{font:600 .95rem var(--f-b);border-radius:8px;padding:9px 14px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
button.p,.vk-go{background:var(--c);border-color:var(--c);color:#fff}
button:disabled{opacity:.6;cursor:wait}
button:focus-visible,.vk-go:focus-visible,a:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
.vk-dur{font-size:.92rem;color:var(--muted);min-height:1.4em}
.vk-chk{list-style:none;padding:0;margin:8px 0}
.vk-chk li{padding:3px 0 3px 26px;position:relative}
.vk-chk li::before{position:absolute;left:0;font-weight:700}
.vk-chk li.ok::before{content:"✓";color:var(--ok)}
.vk-chk li.no::before{content:"✗";color:var(--bad)}
.vk-chk li.no{color:var(--bad)}
.vk-not{font-size:.88rem;color:var(--muted)}
.vk-son{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-top:18px;padding-top:16px;border-top:1px solid var(--line)}
.vk-gelen{border-left:4px solid var(--pc)}
.vk-et{display:inline-block;font-size:.8rem;font-weight:600;border-radius:999px;padding:1px 9px;border:1px solid currentColor}
.vk-et.ok{color:var(--ok)}.vk-et.no{color:var(--bad)}.vk-et.bek{color:var(--muted)}
details summary{cursor:pointer;font-weight:600}
.vk-kart{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:10px 0}
.vk-kart div{background:var(--surface-2);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.vk-kart span{display:block;font-size:.82rem;color:var(--muted)}
.vk-kart b{font:800 1.35rem var(--f-d);font-variant-numeric:tabular-nums}
footer.vk-f{border-top:1px solid var(--line);margin-top:28px;padding-top:14px;font-size:.85rem;color:var(--muted)}
.vk-sec{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 8px}
.vk-sec button[aria-pressed="true"]{background:var(--pc);border-color:var(--pc);color:#fff}
.vk-sec button:disabled,.vk-sec button[aria-disabled="true"]{cursor:not-allowed;opacity:.55}
.vk-uyar{color:var(--bad);background:#FBEDEC;border-radius:8px;padding:8px 12px}
.vk-lnk{padding:0 4px;border:0;background:none;color:var(--c);text-decoration:underline;font:inherit;font-variant-numeric:tabular-nums;min-height:24px}.vk-lnk[aria-current="true"]{font-weight:700;background:var(--surface-2)}
.vk-kay{padding:8px 12px;border-radius:8px;background:var(--surface-2);border-left:4px solid var(--warn)}.vk-kay.kendi{border-left-color:var(--ok)}
.vk-soru{counter-reset:s;margin:0}.vk-soru h3{margin:12px 0 4px}
@media (max-width:760px){.vk-adim{grid-template-columns:repeat(2,minmax(0,1fr))}.vk-iki{grid-template-columns:minmax(0,1fr)}.vk-kart{grid-template-columns:repeat(2,minmax(0,1fr))}.vk-w{padding:0 14px 40px}}
"""

# İlerleme: aynı alan adında (ysfdurak.github.io) dört uygulama ortak localStorage kullanır.
JS_ORTAK = r"""
const VK_KEY='kesit.vaka.depo';
const vkOku=()=>{try{return JSON.parse(localStorage.getItem(VK_KEY)||'{}')||{}}catch(e){return {}}};
const vkYaz=(adim,veri)=>{try{const s=vkOku();s.v=1;s[adim]=Object.assign({tamam:true,at:new Date().toISOString()},veri);localStorage.setItem(VK_KEY,JSON.stringify(s))}catch(e){}};
const vkSay=(v,d=0)=>v==null||!isFinite(v)?'—':Number(v).toLocaleString('tr-TR',{minimumFractionDigits:d,maximumFractionDigits:d});
const vkEsc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function vkAdimlar(){const s=vkOku();document.querySelectorAll('.vk-adim [data-adim]').forEach(a=>{const k=a.dataset.adim,o=a.querySelector('.durum');if(o)o.textContent=s[k]&&s[k].tamam?'✓ çözüldü':'';});}
function vkTablo(cols,rows,num=[]){return '<div class="vk-tw"><table><thead><tr>'+cols.map((c,i)=>'<th'+(num.includes(i)?' class="n"':'')+'>'+vkEsc(c)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map((v,i)=>'<td'+(num.includes(i)?' class="n"':'')+'>'+(typeof v==='number'?vkSay(v,Number.isInteger(v)?0:2):vkEsc(v))+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';}
function vkCsvMetin(cols,rows){const q=v=>{if(v==null)return'';let s=String(v);/* Excel formül sanmasın: =,+,-,@ ile başlayan metne ' (sayılar olduğu gibi) */if(/^[=+\-@\t\r]/.test(s)&&!/^[-+]?\d[\d.,]*%?$/.test(s))s="'"+s;return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s};return [cols.join(','),...rows.map(r=>r.map(q).join(','))].join('\n')+'\n';}
function vkCsvIndir(ad,cols,rows){const t=vkCsvMetin(cols,rows);const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/csv'}));a.download=ad;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500);}
function vkCsvOku(t){const L=t.trim().split(/\r?\n/),h=L[0].split(',');return {cols:h,rows:L.slice(1).map(l=>l.split(','))};}
// Kendi çıktın: 1. adımı çözen kişinin toplama_temiz tablosu sonraki adımlarda seçilebilsin.
const VK_CSV='kesit.vaka.depo.csv', VK_SUTUN=['satir_id','tarih','vardiya','bolge','duzen','toplayici','sure_sn'];
const vkCiktiYaz=(csv,n)=>{try{localStorage.setItem(VK_CSV,JSON.stringify({csv,n,at:new Date().toISOString()}))}catch(e){}};
const vkCiktiOku=()=>{try{const o=JSON.parse(localStorage.getItem(VK_CSV)||'null');return o&&typeof o.csv==='string'?o:null}catch(e){return null}};
function vkKaynak(el,ornek,degisti){
  const kendi=vkCiktiOku(),eksik=kendi?VK_SUTUN.filter(c=>!kendi.csv.split(/\r?\n/,1)[0].split(',').includes(c)):[];
  let sec=kendi&&!eksik.length?'kendi':'ornek',uyar=false;
  const durum=()=>({kaynak:sec,csv:sec==='kendi'?kendi.csv:ornek});
  const ciz=()=>{const n=sec==='kendi'?kendi.n:ornek.trim().split(/\r?\n/).length-1;
    el.innerHTML='<div class="vk-sec" role="group" aria-label="Bu adımda hangi veriyle çalışacaksın?">'
      +'<button type="button" data-k="kendi" aria-pressed="'+(sec==='kendi')+'"'+(kendi?(eksik.length?' aria-disabled="true" aria-describedby="kaynakEksik"':''):' disabled')+'>Kendi çıktımla devam et</button>'
      +'<button type="button" data-k="ornek" aria-pressed="'+(sec==='ornek')+'">Örnek veriyle dene</button></div>'
      +'<p class="vk-kay '+sec+'" role="status"><b>Kullanılan veri:</b> '+(sec==='kendi'
        ?'senin 1. adım (SQL) çıktın · '+vkSay(n)+' satır · '+vkEsc(new Date(kendi.at).toLocaleString('tr-TR',{dateStyle:'short',timeStyle:'short'}))+' kaydı.'
        :'örnek veri, yani 1. adımın beklenen çıktısı · '+vkSay(n)+' satır. Bu adımda göreceğin sonuçlar senin SQL çalışmana ait değil.')+'</p>'
      +(!kendi?'<p class="vk-not">Kendi çıktınla devam etmek için önce <a href="/kesit-sql/vaka/depo/">1. adımı</a> çöz; temiz tablon bu tarayıcıda saklanır.</p>'
        :eksik.length?'<p class="vk-not'+(uyar?' vk-uyar':'')+'" id="kaynakEksik"'+(uyar?' role="alert"':'')+'>Kaydedilen SQL çıktında şu sütunlar yok: <b>'+eksik.map(vkEsc).join(', ')+'</b>. Bu adım bu sütunlarla çalışır; bu yüzden örnek veri seçili. <a href="/kesit-sql/vaka/depo/">1. adıma dön ve görünüme bu sütunları ekle →</a></p>':'');
    el.querySelectorAll('[data-k]').forEach(b=>b.onclick=()=>{if(b.disabled)return;
      // Eksik sütunlu çıktı seçilemez: neden ve SQL adımına dönüş bağlantısı vurgulanır.
      if(b.dataset.k==='kendi'&&eksik.length){uyar=true;ciz();const n=el.querySelector('#kaynakEksik a');if(n)n.focus();return;}
      if(b.dataset.k===sec)return;sec=b.dataset.k;ciz();degisti(durum());});};
  ciz();return durum();}
vkAdimlar();
"""


def sayfa(adim, baslik, aciklama, govde, betik, ek_bas=""):
    i = [a[0] for a in ADIMLAR].index(adim)
    kod, ad, gorev, yol = ADIMLAR[i]
    adim_html = "".join(
        f'<li><a href="{y}" data-adim="{k}" style="--ac:{RENK[k]}"{" aria-current=\"step\"" if k == adim else ""}>'
        f"<b>{a}</b>{g}<span class=\"durum ok\"></span></a></li>"
        for k, a, g, y in ADIMLAR
    )
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self' https://cdn.jsdelivr.net; worker-src 'self' blob:; object-src 'none'; base-uri 'self'; form-action 'self'"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{i + 1}. adım · {baslik} | Depo vakası | Kesit</title>
<meta name="description" content="{aciklama}">
<link rel="canonical" href="https://ysfdurak.github.io{yol}">
<meta property="og:type" content="article"><meta property="og:locale" content="tr_TR"><meta property="og:site_name" content="Kesit"><meta property="og:title" content="Depo vakası · {i + 1}. adım: {baslik}"><meta property="og:description" content="{aciklama}"><meta property="og:image" content="https://ysfdurak.github.io/og.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/vendor/fonts.css">
<style>{CSS}</style>{ek_bas}
</head><body style="--c:{RENK[adim]};--pc:{RENK[ADIMLAR[i - 1][0]] if i else RENK[adim]}"><a class="vk-skip" href="#icerik">İçeriğe geç</a>
<div class="vk-w"><header class="vk-h"><a class="vk-b" href="/"><img src="/favicon.svg" width="24" height="24" alt="">Kesit</a><nav aria-label="Vaka"><a href="/#vaka">Vaka tanıtımı</a><a href="{ADIMLAR[i][3].rsplit('/vaka/', 1)[0]}/">Kesit {ad}</a></nav></header>
<main id="icerik"><span class="vk-e">Uçtan uca vaka · {i + 1}/4 · Kesit {ad}</span>
<h1>{baslik}</h1>
<ol class="vk-adim" aria-label="Vaka adımları">{adim_html}</ol>
{govde}
</main>
<footer class="vk-f"><p>Anadolu Market ve Gebze deposu hayalidir; veri tohumlu bir üreteçle oluşturuldu. Beklenen sonuçlar SQLite, pandas ve SciPy ile ayrıca hesaplanıp bu sayfadaki motorla karşılaştırıldı. İlerlemen yalnız bu tarayıcıda saklanır.</p></footer></div>
<script>{JS_ORTAK}</script>
<script>{betik}</script>
</body></html>
"""
