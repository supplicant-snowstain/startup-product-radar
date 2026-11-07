(function () {
  const host = document.getElementById("research-cards");
  const status = document.getElementById("research-status");
  const copy = {
    zh: {title:"每日研究动态",desc:"观察日期不是发布日期；报告中的产品不代表已审核新品。",read:"阅读完整报告",unknown:"尚无对应的产品索引",label:"研究观察 · 待复核",fail:"研究动态暂时无法加载。"},
    en: {title:"Daily research",desc:"Observation dates are not launch dates. Research entries are not verified launches.",read:"Read full report",unknown:"No indexed products for this report",label:"Research observation · provisional",fail:"Research feed unavailable."},
    fr: {title:"Veille quotidienne",desc:"La date d’observation n’est pas la date de lancement. Ces produits ne sont pas des lancements vérifiés.",read:"Lire le rapport",unknown:"Aucun produit indexé pour ce rapport",label:"Observation · provisoire",fail:"Flux de recherche indisponible."}
  };
  let data = [];
  function lang() { return ["zh","en","fr"].includes(window.RadarI18n?.lang) ? window.RadarI18n.lang : "en"; }
  function render() {
    const c = copy[lang()];
    document.getElementById("research-title").textContent = c.title;
    document.getElementById("research-description").textContent = c.desc;
    host.replaceChildren();
    for (const entry of data.slice(0,7)) {
      const article = document.createElement("article");
      article.className = "research-card";
      const date = document.createElement("small"); date.textContent = entry.observed_at + " · " + c.label;
      const h = document.createElement("h3"); h.textContent = entry.title;
      const p = document.createElement("p");
      p.textContent = entry.products.length ? entry.products.map(x=>x.name).join(" · ") : c.unknown;
      const a = document.createElement("a"); a.href = entry.report_url; a.target = "_blank"; a.rel = "noopener noreferrer"; a.textContent = c.read + " ↗";
      article.append(date,h,p,a); host.append(article);
    }
    status.textContent = data.length ? "" : c.fail;
  }
  window.addEventListener("radar-language-changed",render);
  fetch("./research.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(feed=>{
    if(feed.kind!=="research_observations"||!Array.isArray(feed.reports))throw Error("Invalid feed");
    data=feed.reports.filter(r=>/^\d{4}-\d{2}-\d{2}$/.test(r.observed_at)&&r.evidence_status==="research_provisional"&&Array.isArray(r.products)&&/^https:\/\/github\.com\/supplicant-snowstain\/startup-product-radar\/blob\/main\/reports\//.test(r.report_url));
    render();
  }).catch(()=>render());
})();
