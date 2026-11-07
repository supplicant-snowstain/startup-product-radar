(function(){
"use strict";
const dict={
zh:{back:"← 每日研究",kicker:"公开研究 · 尚未验证需求",job:"用户想完成什么任务？",alternatives:"现有替代方案",workflow:"产品如何工作？",evidence:"证据质量",evidenceTitle:"哪些信息已经得到验证？",evidenceNote:"这里展示的是公开产品档案和研究报告中的观察；厂商主张、独立用户反馈与推测需要分别核查。",missing:"尚缺少什么证据？",missingNote:"尚不能从本记录推断真实留存、付费转化、收入或 PMF。观察日期不是产品首次发布日期。",sources:"追溯原始来源",website:"产品公开网站",profile:"GitHub 产品档案（含来源和风险）",report:"完整中文研究报告",experiment:"如何验证需求？",experimentNote:"访谈近期遇到此问题的用户，观察真实替代方案与完成任务的成本；设计小规模对照试验，预先定义成功与失败阈值。",alternativesNote:"替代方案及竞争对照请以原始产品档案和日报为准，避免凭产品类别推断。",workflowNote:"产品的实际工作流及能力限制请查阅原始资料；本页不将供应商功能宣传视为独立实测。",notfound:"没有找到该研究对象，请返回每日研究列表。",error:"研究数据无法加载，请查看 GitHub 原始研究报告。",ai:"AI 相关",nonai:"无明确 AI 功能",unknown:"AI 角色未核实",caution:"观察不等于已验证需求"},
en:{back:"← Daily research",kicker:"PUBLIC RESEARCH · PROVISIONAL",job:"What is the user trying to do?",alternatives:"Existing alternatives",workflow:"How does it work?",evidence:"EVIDENCE QUALITY",evidenceTitle:"What has been established?",evidenceNote:"This is a public research index. Vendor claims, user reports and hypotheses require separate verification.",missing:"What evidence is missing?",missingNote:"This record does not establish retention, conversion, revenue or PMF. Observation date is not launch date.",sources:"Trace the original sources",website:"Public product website",profile:"GitHub research profile (sources and risks)",report:"Full research report",experiment:"How to test demand?",experimentNote:"Interview users with recent experience of the problem, compare existing alternatives and run a small controlled test with predefined thresholds.",alternativesNote:"Consult the research profile and report for grounded competitors; category labels alone do not establish alternatives.",workflowNote:"Consult primary sources for workflow and limitations. Vendor feature claims are not independent tests.",notfound:"Research item not found. Return to daily research.",error:"Research data unavailable. Consult the original GitHub reports.",ai:"AI-related",nonai:"No confirmed AI role",unknown:"AI role unconfirmed",caution:"Observation ≠ validated demand"},
fr:{back:"← Veille quotidienne",kicker:"RECHERCHE PUBLIQUE · PROVISOIRE",job:"Quelle tâche veut accomplir l'utilisateur ?",alternatives:"Solutions existantes",workflow:"Comment fonctionne le produit ?",evidence:"QUALITÉ DES PREUVES",evidenceTitle:"Que sait-on réellement ?",evidenceNote:"Index de recherche publique. Les affirmations des éditeurs et les avis des utilisateurs demandent une vérification distincte.",missing:"Quelles preuves manquent ?",missingNote:"Cette fiche ne prouve ni rétention, ni conversion, ni revenus, ni adéquation produit-marché. Date d'observation ≠ lancement.",sources:"Consulter les sources",website:"Site public du produit",profile:"Fiche de recherche GitHub",report:"Rapport de recherche complet",experiment:"Comment tester le besoin ?",experimentNote:"Interroger des utilisateurs confrontés au problème, comparer les alternatives et définir des seuils de réussite et d'échec.",alternativesNote:"Consulter les sources pour les alternatives documentées.",workflowNote:"Consulter les sources primaires. Les affirmations de l'éditeur ne sont pas des tests indépendants.",notfound:"Produit introuvable. Retour à la veille.",error:"Données indisponibles. Consultez les rapports GitHub.",ai:"Lié à l'IA",nonai:"Pas de rôle IA confirmé",unknown:"Rôle IA non confirmé",caution:"Observation ≠ besoin validé"}
};
const jobs={
"Agent Device Infrastructure":{zh:"在真实移动设备上运行自动化任务，验证模拟器无法覆盖的能力",en:"Run automations on real mobile devices when simulators fall short",fr:"Exécuter des automatisations sur de vrais appareils"},
"Agent Compute Infrastructure":{zh:"在不同操作系统中可靠运行并恢复自动化任务",en:"Run and resume automations across operating systems",fr:"Exécuter et reprendre des tâches sur plusieurs systèmes"},
"Agent Governance":{zh:"让团队清楚知道自动化操作由谁授权",en:"Know who authorized automated actions",fr:"Identifier qui autorise les actions"},
"Privacy Browser":{zh:"隔离多个工作身份与登录会话",en:"Separate work identities and login sessions",fr:"Séparer les identités et sessions"},
"Developer Tools":{zh:"减少开发和维护集成时的重复劳动",en:"Reduce repetitive development and integration work",fr:"Réduire les tâches répétitives d'intégration"},
"Photography":{zh:"更直接地控制照片的风格和处理流程",en:"Control photo style and processing workflow",fr:"Contrôler le rendu et le flux photographique"}
};
const $=id=>document.getElementById(id);
const params=new URLSearchParams(location.search),slug=params.get("id")||"";
let data=null;
const locale=()=>["en","zh","fr"].includes(window.RadarI18n?.lang)?window.RadarI18n.lang:"en";
function link(id,url,label){const a=$(id);if(typeof url==="string"&&url.startsWith("https://")){a.href=url;a.textContent=label+" ↗";a.hidden=false}else a.hidden=true}
function render(){
const l=locale(),c=dict[l];
const mapping={"research-back":"back","research-return":"back","research-kicker":"kicker","job-label":"job","job-title":"job","alternatives-label":"alternatives","workflow-label":"workflow","evidence-label":"evidence","evidence-title":"evidenceTitle","evidence-note":"evidenceNote","missing-label":"missing","missing-note":"missingNote","source-title":"sources","experiment-title":"experiment","experiment-note":"experimentNote","alternatives-note":"alternativesNote","workflow-note":"workflowNote","research-caution":"caution"};
for(const [id,key] of Object.entries(mapping))$(id).textContent=c[key];
if(!data){$("research-error").hidden=false;$("research-error").textContent=c.notfound;return}
$("research-error").hidden=true;$("research-detail").hidden=false;
$("research-name").textContent=data.name;document.title=data.name+" — Startup Radar";
$("research-category").textContent=data.category;$("research-date").textContent=data.observed_at+" · "+c.kicker;
$("research-ai").textContent=["none","none_confirmed"].includes(data.ai_role)?c.nonai:data.ai_role==="unknown"?c.unknown:c.ai;
const intel=data.intelligence;
const localized=(field,fallback)=>intel&&intel[field]&&intel[field][l]||fallback;
const job=localized("job",jobs[data.category]?.[l]||c.unknown);
$("research-job").textContent=job;$("job-description").textContent=job;
$("workflow-note").textContent=localized("workflow",c.workflowNote);
$("alternatives-note").textContent=localized("alternatives",c.alternativesNote);
$("evidence-note").textContent=localized("evidence",c.evidenceNote);
$("missing-note").textContent=localized("counterevidence",c.missingNote)+" "+c.missingNote;
$("experiment-note").textContent=localized("experiment",c.experimentNote);
link("research-website",data.website,c.website);link("research-profile",data.profile_url,c.profile);link("research-report",data.report_url,c.report);
}
window.addEventListener("radar-language-changed",render);
fetch("./research.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error();return r.json()}).then(feed=>{
if(feed.kind!=="research_observations"||!Array.isArray(feed.reports))throw Error();
for(const report of feed.reports){const found=report.products.find(p=>p.slug===slug);if(found){data={...found,observed_at:report.observed_at,report_url:report.report_url};break}}
render();
}).catch(()=>{$("research-error").hidden=false;$("research-error").textContent=dict[locale()].error});
})();
