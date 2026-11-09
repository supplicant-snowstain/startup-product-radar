(function(){ "use strict";
const frame=document.getElementById("network-preview"),title=document.getElementById("network-home-title"),desc=document.getElementById("network-home-desc"),link=document.getElementById("network-home-link");
if(!frame||!title||!desc||!link)return;
const copy={
en:{title:"Explore the relationships behind a product.",desc:"Choose a product or explore the network. Solid connections describe sourced material; dashed connections are hypotheses or missing evidence. Observation is not a launch date.",link:"Open full-screen relationship explorer ↗",frame:"Interactive startup product research network"},
zh:{title:"从关系网络看懂一个创业产品。",desc:"选择产品，探索创业者、用户问题、替代方案与原始来源。实线表示有资料描述的关系；虚线表示推测或证据缺失。观察日期不是发布日期。",link:"打开完整关系网络 ↗",frame:"创业产品交互式研究关系网络"},
fr:{title:"Explorer les relations derrière chaque produit.",desc:"Choisissez un produit et explorez besoins, alternatives et sources. Les liens en pointillés indiquent des hypothèses ou des preuves manquantes. Observation ≠ lancement.",link:"Ouvrir le réseau interactif ↗",frame:"Réseau interactif de recherche sur les startups"}
};
function render(){const lang=["zh","en","fr"].includes(window.RadarI18n?.lang)?window.RadarI18n.lang:"en",c=copy[lang];title.textContent=c.title;desc.textContent=c.desc;link.textContent=c.link;frame.title=c.frame;try{frame.contentWindow?.postMessage({type:"radar-set-language",lang},location.origin)}catch(_){}}
frame.addEventListener("load",render);window.addEventListener("radar-language-changed",render);render();
})();