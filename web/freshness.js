(function(){
const root=document.getElementById("site-freshness");if(!root)return;
let status=null;
const messages={
en:{unavailable:"Build status has not been verified yet.",built:"Website rebuilt",products:"products",launches:"dated launches",signals:"problem signals",details:"This is the website build time, not the date a new product was discovered."},
zh:{unavailable:"尚未读取到网站发布状态。",built:"网站最近构建",products:"个产品",launches:"条已标注日期的新品",signals:"条问题线索",details:"这里显示的是网站构建时间，不代表当天发现或发布了新产品。"},
fr:{unavailable:"Statut de déploiement non disponible.",built:"Site reconstruit",products:"produits",launches:"lancements datés",signals:"signaux de problèmes",details:"Il s'agit de la date de construction du site, pas de découverte ou de lancement d'un produit."}
};
function render(){const t=messages[window.RadarI18n?.lang]||messages.en;root.replaceChildren();if(!status){root.textContent=t.unavailable;return}
const stamp=document.createElement("time");const date=new Date(status.generated_at_utc);stamp.dateTime=status.generated_at_utc;stamp.textContent=Number.isNaN(date.getTime())?status.generated_at_utc:date.toLocaleString(window.RadarI18n?.lang==="zh"?"zh-CN":window.RadarI18n?.lang==="fr"?"fr-FR":"en-GB",{dateStyle:"medium",timeStyle:"short",timeZone:"Europe/Paris"});
const main=document.createElement("strong");main.textContent=t.built+": ";main.append(stamp);
const counts=document.createElement("span");counts.textContent=" · "+status.products+" "+t.products+" · "+status.dated_launches+" "+t.launches+" · "+status.problem_signals+" "+t.signals;
const note=document.createElement("small");note.textContent=t.details;root.append(main,counts,note)}
fetch("./site-status.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Missing manifest");return r.json()}).then(d=>{if(d.schema_version!==1||typeof d.products!=="number"||typeof d.generated_at_utc!=="string")throw Error("Invalid manifest");status=d;render()}).catch(()=>render());
window.addEventListener("radar-language-changed",render)
})();