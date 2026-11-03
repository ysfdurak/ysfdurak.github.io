"""Rapor sayfasını sonuçlardan üretir; sayfadaki sayılar elle yazılmaz."""
import json
S = json.load(open('sonuclar/sql.json', encoding='utf-8')); P = json.load(open('sonuclar/python.json', encoding='utf-8'))
oz = S['ozet'][0]; sen = S['senaryo'][0]; e = P['etki']
N, G = oz['siparis'], oz['gec']
tr = lambda x, d=1: f'{x:.{d}f}'.replace('.', ',')
sayi = lambda x: f'{x:,}'.replace(',', '.')
pct = lambda a, b, d=1: tr(a / b * 100, d)
H = {(h['gec'], h['anket_once']): h for h in S['dort_hucre']}
gec_puanli = H[(True, False)]['n'] + H[(True, True)]['n']; gec_kotu = H[(True, False)]['kotu'] + H[(True, True)]['kotu']
zam_puanli = H[(False, False)]['n'] + H[(False, True)]['n']; zam_kotu = H[(False, False)]['kotu'] + H[(False, True)]['kotu']
Y = S['yogun_paylar'][0]; SE = {x['satici_gec']: x for x in S['satici_etkisi']}

def bars(satirlar, ad, birim='%', ymax=None):
    """satirlar: (etiket, değer, vurgu, ipucu)"""
    W, Ht, L, B, T = 720, 260, 34, 44, 16
    ymax = ymax or max(s[1] for s in satirlar) * 1.12
    w = (W - L) / len(satirlar); o = [f'<svg viewBox="0 0 {W} {Ht}" role="img" aria-label="{ad}" class="ch">']
    for t in range(0, 5):
        v = ymax * t / 4; y = Ht - B - (Ht - B - T) * t / 4
        o.append(f'<line x1="{L}" x2="{W}" y1="{y:.1f}" y2="{y:.1f}" class="gr"/><text x="{L-6}" y="{y+4:.1f}" class="ax" text-anchor="end">{v:.0f}</text>')
    for i, (et, v, vur, ip) in enumerate(satirlar):
        bw = min(w - 2, 34); x = L + i * w + (w - bw) / 2; h = (Ht - B - T) * v / ymax; y = Ht - B - h; r = min(4, h)
        path = f'M{x:.1f} {Ht-B}V{y+r:.1f}Q{x:.1f} {y:.1f} {x+r:.1f} {y:.1f}H{x+bw-r:.1f}Q{x+bw:.1f} {y:.1f} {x+bw:.1f} {y+r:.1f}V{Ht-B}Z'
        o.append(f'<g class="b" tabindex="0" data-t="{ip}"><rect x="{L+i*w:.1f}" y="{T}" width="{w:.1f}" height="{Ht-B-T}" fill="transparent"/><path d="{path}" class="{"v" if vur else "n"}"/></g>')
        ly = et.split('|')
        for j, part in enumerate(ly): o.append(f'<text x="{L+i*w+w/2:.1f}" y="{Ht-B+16+j*13}" class="ax" text-anchor="middle">{part}</text>')
    o.append('</svg>'); return ''.join(o)

kov_ad = {'a': '15+ gün|erken', 'b': '8-14|erken', 'c': '1-7|erken', 'd': 'Tam|günü', 'e': '1-3 gün|geç', 'f': '4-7|geç', 'g': '8-14|geç', 'h': '15+|geç'}
kova = [(kov_ad[k['kova'][0]], k['kotu'] / k['n'] * 100, k['kova'][0] in 'efgh', f"{k['kova'][3:]}: kötü puan %{pct(k['kotu'], k['n'])} ({sayi(k['n'])} sipariş)") for k in S['gecikme_kova']]
ay_ad = dict(zip('01 02 03 04 05 06 07 08 09 10 11 12'.split(), 'Oca Şub Mar Nis May Haz Tem Ağu Eyl Eki Kas Ara'.split()))
aylar = [(ay_ad[a['ay'][5:]] + ('|' + a['ay'][:4] if a['ay'][5:] == '01' else ''), a['gec'] / a['n'] * 100, a['ay'] in ('2017-11', '2018-02', '2018-03'), f"{ay_ad[a['ay'][5:]]} {a['ay'][:4]}: %{pct(a['gec'], a['n'])} geç ({sayi(a['gec'])} / {sayi(a['n'])})") for a in S['ay']]

sen_sat = [('Satıcıların tamamı kargoya son tarihinde versin', 'Satıcı sürecinde iyileşme', sen['satici_zamaninda']),
           ('Yalnız Kasım, Şubat ve Mart siparişlerinde söz 3 gün uzasın', f"Siparişlerin %{pct(Y['yogun_siparis'], N)}'si için daha uzun söz", sen['yogun_ay_3_gun']),
           ('Yalnız RJ eyaletine söz 3 gün uzasın', 'Bir eyalette daha uzun söz', sen['rj_3_gun']),
           ('Bütün siparişlerde söz 3 gün kısalsın', 'Hızlı görünme baskısı', sen['soz_3_gun_kisa'])]
tablo = ''.join(f'<tr><td>{a}</td><td>{b}</td><td class="n">{sayi(c)}</td><td class="n">%{pct(c, N)}</td><td class="n">{"+" if c>G else "−"}{sayi(abs(c-G))}</td></tr>' for a, b, c in sen_sat)
uy = ''.join(f"<tr><td class=\"n\">{tr(u['esik'],1)} kat</td><td class=\"n\">%{tr(u['siparis_payi'])}</td><td class=\"n\">%{tr(u['gec_uyarili'])}</td><td class=\"n\">%{tr(u['gec_uyarisiz'])}</td></tr>" for u in P['uyari'])

html = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Teslimat analizi</title><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Gerçek bir e-ticaret verisinde geç teslimat, müşteri puanı ve hangi iyileştirmenin önce denenmesi gerektiği.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/vendor/fonts.css">
<style>
:root{{--bg:#F1F0EC;--surface:#fff;--ink:#1B1A16;--muted:#625F55;--line:#DEDBD2;--link:#2A56B5;--a:#C2410C;--n:#2A56B5;--warn:#8A6200;--f-d:'Bricolage Grotesque',system-ui,sans-serif;--f-b:'IBM Plex Sans',system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root{{--bg:#12110D;--surface:#1B1A15;--ink:#EEEBE2;--muted:#A39F92;--line:#34312A;--link:#8FB3FF;--a:#DD7230;--n:#5F8BE6;--warn:#F2C94C}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.65 var(--f-b);-webkit-font-smoothing:antialiased}}a{{color:var(--link)}}
.w{{max-width:800px;margin:0 auto;padding:28px 24px 56px}}.brand{{font:800 1.1rem var(--f-d);color:inherit;text-decoration:none}}
.eb{{font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
h1{{font:800 clamp(1.9rem,5vw,2.8rem)/1.1 var(--f-d);letter-spacing:-.025em;margin:8px 0 14px;text-wrap:balance}}h2{{font:800 1.35rem/1.25 var(--f-d);letter-spacing:-.015em;margin:38px 0 10px}}
.lead{{font-size:1.08rem;color:var(--muted);margin:0 0 20px}}p{{margin:0 0 12px}}ul,ol{{padding-left:20px;margin:0 0 12px}}li{{margin-bottom:7px}}
.k{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:18px 0}}.k div{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px}}.k b{{display:block;font:800 1.75rem/1.1 var(--f-d)}}.k span{{font-size:.84rem;color:var(--muted)}}
.karar{{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--a);border-radius:8px;padding:14px 18px;margin:12px 0}}
.fig{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:14px;margin:10px 0 6px;position:relative}}.fig h3{{margin:0 0 6px;font:600 .95rem var(--f-b)}}.ch{{width:100%;height:auto;display:block}}
.gr{{stroke:var(--line);stroke-width:1}}.ax{{fill:var(--muted);font-size:11px;font-family:var(--f-b)}}.n{{fill:var(--n)}}.v{{fill:var(--a)}}.b:hover path,.b:focus path{{opacity:.75}}.b:focus{{outline:none}}
.leg{{display:flex;gap:14px;font-size:.82rem;color:var(--muted);margin-top:6px;flex-wrap:wrap}}.leg i{{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px}}
#tip{{position:fixed;pointer-events:none;background:var(--ink);color:var(--bg);font-size:.8rem;padding:6px 9px;border-radius:6px;max-width:260px;opacity:0;transition:opacity .1s;z-index:9}}
.tw{{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:10px;margin:8px 0 14px}}table{{border-collapse:collapse;width:100%;font-size:.9rem}}th,td{{text-align:left;vertical-align:top;padding:9px 11px;border-bottom:1px solid var(--line)}}tr:last-child td{{border-bottom:0}}th{{font-size:.78rem;color:var(--muted);font-weight:600}}td.n{{fill:none;white-space:nowrap;font-variant-numeric:tabular-nums}}
details{{margin:6px 0 12px;font-size:.9rem}}summary{{cursor:pointer;color:var(--muted)}}footer{{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);font-size:.86rem;color:var(--muted)}}
@media (max-width:640px){{.w{{padding:20px 16px 40px}}}}
</style></head><body><div class="w"><a class="brand" href="/">Kesit</a>
<div style="padding-top:34px"><span class="eb">Portföy projesi · gerçek veri</span>
<h1>Geç teslimat puanı ne kadar bozuyor, önce neyi denemeli?</h1>
<p class="lead">Brezilya'daki Olist pazaryerinin gerçek {sayi(N)} teslim edilmiş siparişi (Ocak 2017 - Ağustos 2018). Soru bir operasyon yöneticisinin sorusu: sınırlı kaynakla önce hangi iyileştirmeyi denemeliyim?</p></div>
<div class="k"><div><b>%{pct(G, N)}</b><span>sipariş sözlenen tarihten sonra geldi</span></div><div><b>%{pct(gec_kotu, oz['kotu'])}</b><span>kötü puanın (1-2) geldiği yer bu siparişler</span></div><div><b>%{pct(Y['yogun_gec'], G)}</b><span>geç teslimat üç ayda toplandı (Kasım, Şubat, Mart)</span></div></div>
<h2>Önerim</h2>
<div class="karar"><ol style="margin:0">
<li><b>Önce değerlendirme zamanını ve iletişimi düzelt.</b> Geç siparişlerin %{pct(H[(True,True)]['n'], gec_puanli)}'inde değerlendirme kaydı ürün gelmeden oluşmuş. En ucuz deneme: sözlenen gün geldiğinde ürün yolda ise müşteriye haber ver, değerlendirmeyi teslimattan sonra iste.</li>
<li><b>Sonra yoğun dönem sözünü dene.</b> Kasım planlanabilir bir dönem. Söz süresini yoğun dönemde kontrollü olarak uzatmayı ve satışa etkisini A/B testiyle ölç.</li>
<li><b>Satıcı baskısını üçüncü sıraya al.</b> Her satıcı kargoya zamanında verse bile geç teslimatın yalnız %{pct(G-sen['satici_zamaninda'], G)}'i kalkıyor. Bütün satıcılara yeni kural yerine, sık geciken satıcılara odaklan.</li>
<li><b>Sözü genel olarak kısaltma.</b> Üç gün kısaltmak geç oranını %{pct(sen['soz_3_gun_kisa'], N)}'e çıkarıyor.</li></ol></div>
<h2>1. Puan, sözlenen günde kırılıyor</h2>
<p>Çok erken gelmek pek ödüllendirilmiyor: kötü puan oranı, 15 gün erken gelenle 8-14 gün erken gelende neredeyse aynı. Sözlenen günü geçince ise hızla yükseliyor.</p>
<div class="fig"><h3>Teslimat zamanına göre kötü puan (1-2) oranı, %</h3>{bars(kova, 'Teslimat zamanına göre kötü puan oranı', ymax=100)}<div class="leg"><span><i style="background:var(--n)"></i>Zamanında</span><span><i style="background:var(--a)"></i>Geç</span></div></div>
<h2>2. Ama bu etkinin büyüklüğü anket zamanına bağlı</h2>
<p>En önemli uyarı burada. Basit karşılaştırma geç siparişlerde kötü puanı %{pct(gec_kotu, gec_puanli)}, zamanında gelenlerde %{pct(zam_kotu, zam_puanli)} gösteriyor. Fark; ürün kategorisi, tutar, dönem ve eyalet sabitlenince {tr(e['kontrollu_puan'])} puan, aynı satıcı içinde {tr(e['ayni_satici_puan'])} puan kalıyor. Yani fark satıcı ya da ürün karışımından gelmiyor.</p>
<div class="tw"><table><tr><th>Sipariş</th><th>Değerlendirme kaydı</th><th>Sipariş sayısı</th><th>Kötü puan</th></tr>
<tr><td>Zamanında</td><td>Teslimattan sonra</td><td class="n">{sayi(H[(False,False)]['n'])}</td><td class="n">%{pct(H[(False,False)]['kotu'],H[(False,False)]['n'])}</td></tr>
<tr><td>Geç</td><td>Teslimattan sonra</td><td class="n">{sayi(H[(True,False)]['n'])}</td><td class="n">%{pct(H[(True,False)]['kotu'],H[(True,False)]['n'])}</td></tr>
<tr><td>Geç</td><td>Ürün gelmeden</td><td class="n">{sayi(H[(True,True)]['n'])}</td><td class="n">%{pct(H[(True,True)]['kotu'],H[(True,True)]['n'])}</td></tr></table></div>
<p>Ürünü almış müşteride fark {tr(e['anket_sonra_puan'])} puana iniyor. Bu yüzden gerçek etkiyi tek sayıyla söylemiyorum: {tr(e['anket_sonra_puan'])} ile {tr(e['kontrollu_puan'])} puan arasında. Teslimattan sonra değerlendirenler daha az geciken siparişler olduğu için alt sınır da tam temiz değil.</p>
<h2>3. Gecikme yılın her ayına eşit dağılmıyor</h2>
<div class="fig"><h3>Sipariş ayına göre geç teslimat oranı, %</h3>{bars(aylar, 'Aya göre geç teslimat oranı', ymax=20)}<div class="leg"><span><i style="background:var(--a)"></i>En yoğun üç ay</span><span><i style="background:var(--n)"></i>Diğer aylar</span></div></div>
<p>Siparişlerin %{pct(Y['yogun_siparis'], N)}'si bu üç ayda, geç teslimatın %{pct(Y['yogun_gec'], G)}'i de öyle. Elimdeki veri Şubat-Mart 2018'in nedenini söylemiyor; önce onu şirkete ve taşıyıcılara sorardım. Bu aylar veriye bakarak seçildiği için tek yılın örüntüsünü mevsimsellik sanmamak gerekir.</p>
<h2>4. Hangi kaldıraç ne kadar değiştirir?</h2>
<p>Bugünkü durum: {sayi(G)} geç sipariş, %{pct(G, N)}. Aşağıdakiler mekanik hesaptır, gözlenmiş etki değildir.</p>
<div class="tw"><table><tr><th>Senaryo</th><th>Bedeli</th><th>Geç sipariş</th><th>Oran</th><th>Fark</th></tr>{tablo}</table></div>
<p>Satıcı etkisi gerçek ama küçük: kargoya geç verilen siparişlerde geç teslimat %{pct(SE[True]['gec'],SE[True]['n'])}, diğerlerinde %{pct(SE[False]['gec'],SE[False]['n'])}. Yine de geç siparişlerin çoğu, satıcı zamanında verdiği halde geç kalıyor. Söz uzatmanın satışa zararını bu veri ölçemez; bu yüzden öneri A/B testi.</p>
<h2>5. Denediğim ve işe yaramayan: erken uyarı</h2>
<p>Son 7 günün taşıma süresi, önceki haftalara göre uzayınca alarm verip sözü uzatmak istedim. Yalnız o güne kadar görülebilen teslimatları kullanarak geçmişe karşı denedim. Alarm geç teslimatı öngörmedi. Bu kuralı önermiyorum.</p>
<div class="tw"><table><tr><th>Alarm eşiği</th><th>Alarmlı siparişler</th><th>Geç oranı, alarm varken</th><th>Geç oranı, alarm yokken</th></tr>{uy}</table></div>
<h2>Sınırlar</h2>
<ul><li>Gözlemsel veri; neden-sonuç kanıtı değil. Önerilerin her biri kontrollü denemeyle sınanmalı.</li>
<li>Brezilya, 2017-2018. Sonuçlar başka ülkeye ya da bugüne doğrudan taşınmaz. Maliyet, satış dönüşümü ve iade verisi yok.</li>
<li><code>review_creation_date</code> alanını değerlendirme talebinin oluştuğu tarih olarak yorumladım. Geç siparişlerde bu tarih çoğunlukla sözlenen tarihten 2 gün sonra. Bu yorumun şirkete doğrulatılması gerekir.</li>
<li>Kapsam teslim edilmiş siparişlerle sınırlı. İptal ve teslim edilmeyen siparişler ayrı bir kayıp olabilir.</li></ul>
<h2>Nasıl doğrulandı</h2>
<p>Hesaplar gerçek PostgreSQL motorunda SQL ile yapıldı, sonra pandas ile bağımsız olarak yeniden hesaplandı: {P['capraz_kontrol']} değerde fark 0. Veri seçimi, analiz kodu ve metin dâhil çalışmayı yapay zekâyla (Claude) hazırladım. Alan uzmanı incelemesi henüz yok.</p>
<footer>Veri: <a href="https://github.com/olist/work-at-olist-data">olist/work-at-olist-data</a>, Kaggle'da CC BY-NC-SA 4.0 olarak yayımlanıyor. Bu sayfa da aynı lisansla, ticari olmayan bir portföy çalışmasıdır. · <a href="https://github.com/ysfdurak/ysfdurak.github.io/tree/main/projeler/teslimat/kaynak">Kod ve yöntem</a> · <a href="/">Ana sayfa</a></footer>
</div><div id="tip" role="status"></div>
<script>(function(){{var t=document.getElementById('tip');function s(g,x,y){{t.textContent=g.dataset.t;t.style.opacity=1;var w=t.offsetWidth;t.style.left=Math.max(8,Math.min(innerWidth-w-8,x-w/2))+'px';t.style.top=Math.max(8,y-44)+'px'}}document.querySelectorAll('.b').forEach(function(g){{g.addEventListener('mousemove',function(e){{s(g,e.clientX,e.clientY)}});g.addEventListener('mouseleave',function(){{t.style.opacity=0}});g.addEventListener('focus',function(){{var r=g.getBoundingClientRect();s(g,r.left+r.width/2,r.top+30)}});g.addEventListener('blur',function(){{t.style.opacity=0}})}})}})();</script></body></html>'''
open('rapor/index.html', 'w', encoding='utf-8').write(html)
print('rapor', len(html))
