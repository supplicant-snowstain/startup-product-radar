(function(){
const root=document.getElementById("opportunity-map");if(!root)return;
const I=window.RadarI18n;let feed,graph;
const copy={
en:{title:"Opportunity map",subtitle:"Navigate the connections between problems and original sources.",problem:"Problem",source:"Public source",relation:"Editorial link · not verified",same:"Shared discussion source (not independent confirmation)",none:"No documented adjacent-problem links.",open:"Open exploration ↗",view:"View source ↗",notice:"A shared source is not proof that two needs are the same.",unavailable:"Map data unavailable."},
zh:{title:"机会探索地图",subtitle:"沿着用户问题与公开来源之间的联系继续探索。",problem:"用户问题",source:"公开来源",relation:"研究关联假设 · 未验证",same:"来自同一讨论（不能算独立佐证）",none:"尚无明确记录的相邻问题关系。",open:"打开探索页 ↗",view:"查看来源 ↗",notice:"来自同一来源不代表需求相同。",unavailable:"无法加载关系数据。"},
fr:{title:"Carte des opportunités",subtitle:"Explorer les liens entre problèmes et sources publiques.",problem:"Problème",source:"Source publique",relation:"Lien éditorial · non vérifié",same:"Même discussion (pas de preuve indépendante)",none:"Aucun lien documenté entre problèmes voisins.",open:"Explorer ↗",view:"Voir la source ↗",notice:"Partager une source ne signifie pas partager le même besoin.",unavailable:"Données relationnelles indisponibles."}
};
function node(tag,className,label){const n=document.createElement(tag);if(className)n.className=className;n.textContent=label;return n}
function render(){if(!feed||!graph)return;const id=new URLSearchParams(location.search).get("id"),current=feed.signals.find(x=>x.id===id);if(!current)return;const t=copy[I.lang]||copy.en;root.replaceChildren();root.append(node("h2","",t.title),node("p","",t.subtitle));
const stage=node("div","map-stage",""),center=node("div","map-center","");
center.append(node("small","",t.problem),node("strong","",I.localSignal(current).title));stage.append(center);
const links=graph.edges.filter(e=>(e.from===id||e.to===id)&&e.verification==="editorial_hypothesis");
const others=[];for(const e of links){const other=feed.signals.find(s=>s.id===(e.from===id?e.to:e.from));if(other&&!others.some(x=>x.id===other.id))others.push(other)}
const nodes=node("div","map-neighbors","");for(const other of others){const a=node("a","map-node","");a.href="./explore.html?id="+encodeURIComponent(other.id);a.append(node("small","",t.relation),node("strong","",I.localSignal(other).title),node("span","",t.open));nodes.append(a)}
if(!others.length)nodes.append(node("p","",t.none));stage.append(nodes);
const refs=node("div","map-sources","");const byUrl=new Map();for(const s of [current,...others]){if(!byUrl.has(s.source_url))byUrl.set(s.source_url,[]);byUrl.get(s.source_url).push(s)}
for(const [url,items] of byUrl){if(!/^https:\/\//.test(url))continue;const article=node("div","map-source","");article.append(node("small","",t.source));const a=node("a","",t.view);a.href=url;a.target="_blank";a.rel="noopener noreferrer";article.append(a);if(items.length>1)article.append(node("p","",t.same));refs.append(article)}
stage.append(refs);root.append(stage,node("p","map-warning",t.notice));
}
Promise.all([fetch("./signals.json").then(r=>{if(!r.ok)throw Error("signals");return r.json()}),fetch("./opportunity-map.json").then(r=>{if(!r.ok)throw Error("graph");return r.json()})]).then(([f,g])=>{if(f.dataset_status!=="provisional_only"||g.review_state!=="editorial_hypothesis_not_verified"||!Array.isArray(g.edges))throw Error("schema");feed=f;graph=g;render()}).catch(()=>{root.textContent=(copy[I.lang]||copy.en).unavailable});window.addEventListener("radar-language-changed",render);
})();