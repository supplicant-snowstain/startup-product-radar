(function () {
  "use strict";
  const host = document.getElementById("research-cards");
  const status = document.getElementById("research-status");
  const section = document.getElementById("daily-research");
  if (!host || !section) return;
  const copy = {
    zh:{title:"每日研究与真实问题",desc:"从产品出发，理解用户为什么需要它。研究观察 ≠ 已验证需求或正式新品。",read:"阅读原始报告",profile:"查看产品研究档案",label:"公开研究 · 待复核",fail:"研究数据暂不可用，请访问 GitHub 报告目录。",empty:"没有符合条件的研究。",search:"搜索产品、问题或行业",all:"全部",ai:"AI 相关",nonai:"非 AI",unknown:"AI 角色尚未确认",problem:"潜在用户任务（研究假设）",evidence:"证据边界",missing:"公开资料尚不足以证明留存、付费或 PMF。",observed:"观察于",count:"份研究报告"},
    en:{title:"Daily research & real problems",desc:"Explore the job behind each product. Research observations are not verified demand or launches.",read:"Read original report",profile:"Research profile",label:"Public research · provisional",fail:"Research data unavailable. Visit the GitHub reports directory.",empty:"No matching research.",search:"Search products, problems or industries",all:"All",ai:"AI-related",nonai:"Non-AI",unknown:"AI role unconfirmed",problem:"Possible user job (hypothesis)",evidence:"Evidence boundary",missing:"Public evidence does not establish retention, payment or PMF.",observed:"Observed",count:"research reports"},
    fr:{title:"Veille et besoins réels",desc:"Comprendre le problème derrière chaque produit. Une observation n'est ni une demande ni un lancement vérifié.",read:"Lire le rapport",profile:"Fiche de recherche",label:"Recherche publique · provisoire",fail:"Données indisponibles. Consultez les rapports sur GitHub.",empty:"Aucun résultat.",search:"Chercher produit, besoin ou secteur",all:"Tous",ai:"Lié à l'IA",nonai:"Sans IA",unknown:"Rôle de l'IA non confirmé",problem:"Besoin potentiel (hypothèse)",evidence:"Limite des preuves",missing:"Les sources ne prouvent ni rétention, ni paiement, ni PMF.",observed:"Observé",count:"rapports"}
  };
  const jobs = {
    "Agent Device Infrastructure":{zh:"在真实移动设备上测试或运行自动化操作",en:"Test and operate automations on real mobile devices",fr:"Tester des automatisations sur de vrais appareils"},
    "Agent Compute Infrastructure":{zh:"为自动化任务提供可持续的执行环境",en:"Run automated tasks in persistent computing environments",fr:"Exécuter des tâches dans des environnements persistants"},
    "Agent Governance":{zh:"让团队明确谁批准了自动化操作",en:"Track who authorized automated actions",fr:"Savoir qui autorise les actions automatisées"},
    "Developer Tools":{zh:"减少开发、集成与测试的重复工作",en:"Reduce repeated development, integration and testing work",fr:"Réduire les tâches répétitives de développement"},
    "Privacy Browser":{zh:"隔离不同工作身份和登录状态",en:"Keep work identities and sessions separate",fr:"Séparer identités et sessions de travail"},
    "Photography":{zh:"以更可控的方式创作影像",en:"Create photos with greater aesthetic control",fr:"Créer des images avec plus de contrôle"},
    "Interactive Entertainment":{zh:"通过交互体验而不只是观看内容获得乐趣",en:"Enjoy interactive experiences rather than passive content",fr:"Profiter d'expériences interactives"},
    "Cross-device Sharing":{zh:"在不同设备之间传输文件",en:"Move files between devices",fr:"Transférer des fichiers entre appareils"},
    "On-device AI":{zh:"在设备本地使用语言模型",en:"Use language models directly on a device",fr:"Utiliser des modèles de langage sur l'appareil"}
  };
  let reports=[], mode="all", query="";
  const toolbar=document.createElement("div");toolbar.className="research-toolbar";
  const input=document.createElement("input");input.type="search";input.id="research-search";input.setAttribute("aria-label","Search research");
  const controls=document.createElement("div");controls.className="research-filters";
  toolbar.append(input,controls);host.before(toolbar);
  const counter=document.createElement("p");counter.className="research-count";toolbar.after(counter);
  const locale=()=>["zh","en","fr"].includes(window.RadarI18n?.lang)?window.RadarI18n.lang:"en";
  const classification=p=>["none","none_confirmed"].includes(p.ai_role)?"nonai":p.ai_role&&p.ai_role!=="unknown"?"ai":"unknown";
  function render(){
    const l=locale(),c=copy[l];
    document.getElementById("research-title").textContent=c.title;
    document.getElementById("research-description").textContent=c.desc;
    input.placeholder=c.search;
    controls.replaceChildren();
    for(const [key,label] of [["all",c.all],["ai",c.ai],["nonai",c.nonai]]){
      const b=document.createElement("button");b.type="button";b.textContent=label;b.className=mode===key?"selected":"";b.setAttribute("aria-pressed",String(mode===key));
      b.onclick=()=>{mode=key;render()};controls.append(b);
    }
    host.replaceChildren();
    const q=query.toLocaleLowerCase();
    let visible=0;
    for(const report of reports){
      const matches=report.products.filter(p=>(mode==="all"||classification(p)===mode)&&[p.name,p.category,p.ai_role,jobs[p.category]?.[l]||""].join(" ").toLocaleLowerCase().includes(q));
      if((mode!=="all"||q)&&!matches.length)continue;
      visible++;
      const card=document.createElement("article");card.className="research-card";
      const top=document.createElement("small");top.textContent=c.observed+" "+report.observed_at+" · "+c.label;
      const h=document.createElement("h3");h.textContent=report.title;
      card.append(top,h);
      if(matches.length){
        const list=document.createElement("div");list.className="research-product-list";
        for(const p of matches){
          const item=document.createElement("div");item.className="research-product";
          const name=document.createElement("strong");name.textContent=p.name;
          const category=document.createElement("small");category.textContent=p.category+" · "+(classification(p)==="nonai"?c.nonai:classification(p)==="ai"?c.ai:c.unknown);
          const job=document.createElement("p");job.textContent=c.problem+": "+(jobs[p.category]?.[l]||c.unknown);
          item.append(name,category,job);
          if(p.profile_url){const link=document.createElement("a");link.href=p.profile_url;link.target="_blank";link.rel="noopener noreferrer";link.textContent=c.profile+" ↗";item.append(link)}
          list.append(item);
        }
        card.append(list);
      }
      const warning=document.createElement("p");warning.className="research-evidence";warning.textContent=c.evidence+": "+c.missing;card.append(warning);
      const link=document.createElement("a");link.href=report.report_url;link.target="_blank";link.rel="noopener noreferrer";link.textContent=c.read+" ↗";card.append(link);
      host.append(card);
    }
    counter.textContent=visible+" "+c.count;
    status.textContent=visible?"":reports.length?c.empty:c.fail;
  }
  input.addEventListener("input",()=>{query=input.value.trim();render()});
  window.addEventListener("radar-language-changed",render);
  fetch("./research.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("HTTP "+r.status);return r.json()}).then(feed=>{
    if(feed.kind!=="research_observations"||!Array.isArray(feed.reports))throw Error("Invalid research feed");
    reports=feed.reports.filter(r=>/^\d{4}-\d{2}-\d{2}$/.test(r.observed_at)&&r.evidence_status==="research_provisional"&&Array.isArray(r.products)&&r.report_url.startsWith("https://github.com/supplicant-snowstain/startup-product-radar/blob/main/reports/")).slice(0,14);
    render();
  }).catch(()=>render());
})();
