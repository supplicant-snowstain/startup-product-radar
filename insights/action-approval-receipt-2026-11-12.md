# Action Approval Receipt — 2026-11-12

研究性质：INFERRED，尚无需求验证。来源：[Nod by n8n](https://www.producthunt.com/products/n8n-io)、[CALL-E](https://www.producthunt.com/products/call-e)、[Skillbox](https://www.producthunt.com/products/skillbox-5)。

## JTBD
独立开发者需要在Agent对真实世界执行不可逆操作前，低摩擦检查目标、参数、授权来源与回滚能力。旧替代为人工逐步操作、应用级权限和零散日志。

## 假设
本地HTML/JSON批准记录可减少不敢授权Agent的情况，而不明显降低任务完成效率。设计时默认不执行真实支付、电话或删除。

## 两周公开测试
访谈8名开发者收集最近30天实际失败/拒绝授权案例；用5名测试者模拟10类高风险动作；记录批准正确率、额外耗时、再次使用和假阳性。成功：至少4/8真实案例、3/5复用、额外耗时中位数≤30秒；失败：少于2/8案例或0/5复用。无数据前不能宣称PMF。

## 反证
现有权限系统已经足够；审批疲劳使用户盲点确认；错误来源或模型伪造的证据误导用户；审计数据泄露隐私。
