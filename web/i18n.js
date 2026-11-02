(function(){
const LANGUAGES=["en","zh","fr"];
const bundles={};
function preferred(){
  try{const saved=localStorage.getItem("startup-radar-lang");if(LANGUAGES.includes(saved))return saved}catch(e){}
  const browser=(navigator.language||"en").toLowerCase();
  return browser.startsWith("zh")?"zh":browser.startsWith("fr")?"fr":"en";
}
let lang=preferred();
function t(key){return (bundles[lang]?.ui||bundles.en?.ui||{})[key]||bundles.en?.ui?.[key]||key}
function localSignal(signal){const localized=bundles[lang]?.signals?.[signal.id];return localized?{...signal,...localized}:signal}
function apply(){
  document.documentElement.lang=lang;
  document.querySelectorAll("[data-i18n]").forEach(node=>node.textContent=t(node.dataset.i18n));
  // This slot contains only repo-maintained, reviewed UI markup, never external feed content.
  document.querySelectorAll("[data-i18n-html]").forEach(node=>node.innerHTML=t(node.dataset.i18nHtml));
  document.querySelectorAll("[data-i18n-placeholder]").forEach(node=>node.placeholder=t(node.dataset.i18nPlaceholder));
  window.dispatchEvent(new Event("radar-language-changed"));
}
async function loadBundle(locale){
  const response=await fetch("./locales/"+locale+".json");
  if(!response.ok)throw new Error("Locale "+locale+" unavailable");
  const data=await response.json();
  if(!data||typeof data.ui!=="object"||typeof data.signals!=="object")throw new Error("Invalid locale "+locale);
  return data;
}
async function init(){
  const select=document.getElementById("language");
  if(select)select.value=lang;
  try{bundles.en=await loadBundle("en")}catch(err){console.error("Unable to load English locale",err)}
  if(lang!=="en"){try{bundles[lang]=await loadBundle(lang)}catch(err){console.warn("Locale fallback to English",err);lang="en";if(select)select.value="en"}}
  apply();
  if(select)select.addEventListener("change",async()=>{
    const next=select.value;
    if(!LANGUAGES.includes(next))return;
    if(!bundles[next]){try{bundles[next]=await loadBundle(next)}catch(err){console.warn("Locale change failed",err);select.value=lang;return}}
    lang=next;
    try{localStorage.setItem("startup-radar-lang",lang)}catch(e){}
    apply();
  });
}
window.RadarI18n={t,localSignal,get lang(){return lang},init};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();