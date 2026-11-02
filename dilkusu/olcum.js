/* Dilkuşu ölçümü: yalnızca kullanıcı izin verirse Google Analytics yüklenir.
   Ad, e-posta, cevap ya da çalışma içeriği gönderilmez. */
(function(){
  var C=window.KA_CONFIG||{},KEY='dk_olcum',ID=C.gaId,on=false,scr='',det='',sec=0,lastIn=Date.now();
  function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
  function set(v){try{localStorage.setItem(KEY,v)}catch(e){}}
  function start(){
    if(on||!ID)return;on=true;
    window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};
    gtag('js',new Date());gtag('config',ID,{send_page_view:false,allow_google_signals:false,allow_ad_personalization_signals:false});
    var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(ID);document.head.appendChild(s);
    if(scr)window.dkScreen(scr,det);else gtag('event','page_view',{page_location:location.origin+location.pathname,page_title:document.title});
  }
  function flush(){if(on&&scr&&sec>0){gtag('event','ekran_suresi',{ekran:scr,ayrinti:det,sure_sn:sec,transport_type:'beacon'})}sec=0}
  window.dkScreen=function(m,d){
    flush();scr=m;det=d||'';
    var path=location.pathname.replace(/[^/]*$/,'')+'ekran/'+m+(det?'/'+det:'');
    if(on)gtag('event','page_view',{page_location:location.origin+path,page_path:path,page_title:'Ekran: '+m+(det?' ('+det+')':'')});
  };
  // Yalnızca sayfa görünürken ve son 60 saniyede etkileşim varsa süre sayılır
  ['pointerdown','keydown','scroll','touchstart'].forEach(function(e){addEventListener(e,function(){lastIn=Date.now()},{passive:true,capture:true})});
  setInterval(function(){if(on&&scr&&!document.hidden&&Date.now()-lastIn<60000)sec++},1000);
  addEventListener('pagehide',flush);document.addEventListener('visibilitychange',function(){if(document.hidden)flush()});
  function banner(){
    if(!ID||get()||document.getElementById('dkb'))return;
    var d=document.createElement('div');d.id='dkb';d.setAttribute('role','dialog');d.setAttribute('aria-label','Ölçüm izni');
    d.style.cssText='position:fixed;left:12px;right:12px;bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:9999;max-width:460px;margin:0 auto;background:#fff;color:#2b2140;border:1px solid #f0e2d4;border-radius:14px;padding:14px;box-shadow:0 6px 24px rgba(43,33,64,.18);font:15px/1.45 Nunito,system-ui,sans-serif';
    d.innerHTML='<b>Hangi bölümler işe yarıyor, görmek istiyoruz.</b><br>İzin verirsen Google Analytics hangi ekranda ne kadar kaldığını anonim olarak sayar. Adın ve cevapların gönderilmez. Veriler yurt dışına aktarılabilir. <a href="'+(window.DK_ROOT||'')+'hakkinda.html#gizlilik" style="color:#1e6fe0">Ayrıntı</a><div style="display:flex;gap:8px;margin-top:10px"><button id="dkr" style="flex:1;padding:9px;border-radius:10px;border:1px solid #d8cdbf;background:#fff;color:#2b2140;font:inherit;font-weight:700">Hayır</button><button id="dka" style="flex:1;padding:9px;border-radius:10px;border:1px solid #d8cdbf;background:#fff;color:#2b2140;font:inherit;font-weight:700">İzin ver</button></div>';
    document.body.appendChild(d);
    d.querySelector('#dka').onclick=function(){set('evet');d.remove();start()};
    d.querySelector('#dkr').onclick=function(){set('hayir');d.remove()};
  }
  window.dkOlcumSifirla=function(){try{localStorage.removeItem(KEY)}catch(e){}location.reload()};
  try{if(typeof cur==='string')window.dkScreen(cur,'')}catch(e){}
  if(ID){if(get()==='evet')start();else addEventListener('load',banner)}
})();
