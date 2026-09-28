# decision-assistant

一个可独立使用的中文决策技能：**明确建议 + 现实行动**，不为拍板而假装确定。

用于日常选择、工作边界、投资权衡与工程变更。按撤销成本和风险选择分析深度；低风险尽快小步验证，高风险保留证据、替代方案和停止条件。允许条件推荐、暂缓或先问一个关键问题。

## 使用

把仓库放到支持 Agent Skills 的宿主技能目录，目录名使用 `decision-assistant`，并按宿主要求启用；或让助手读取根目录 [SKILL.md](SKILL.md)。具体自动发现/调用方式由宿主决定，本仓库未对所有宿主做集成测试。

无需 Council、其他技能、API 密钥或独立代理。浏览和隔离复核都是可选能力；不可用时必须如实说明。`agents/openai.yaml` 仅为支持该元数据的宿主提供展示信息，不是运行依赖。

示例请求（虚构）：

> 我每周最多有两小时，想试写短文但不知道是否喜欢。要不要开始？

预期给出有期限、有时间上限、有观察指标和停止/继续条件的小实验，而不是长篇哲学论证。重大投资或不可逆数据操作不能照搬轻量模板。

## 文件与验证

- [核心技能](SKILL.md) · [可选复核模板](agents/blind-review.md)
- 领域护栏：[投资](references/investment-decisions.md) / [工作](references/work-decisions.md) / [工程](references/engineering-decisions.md)
- [公开来源对照](references/design-review.md)：当日 stars、许可证、固定 commit、原文依据与取舍
- [评测协议与局限](evals/README.md) · [行为用例](evals/cases.yaml) · [实际本地测试记录](evals/validation-report.md)

开发检查（Python 3.10+；唯一测试依赖 PyYAML）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

运行技能本身不需要 Python。检查只验证结构、链接、用例约束和有限的隐私模式，**不证明模型行为正确或效果优于基线**。没有模型 A/B 胜率可报告。

## 隐私与权限

默认不保存个人决策记录；示例为虚构。用户批准建议不自动授权转账、部署、删除等操作。外部核验和可选审查不得发送未经允许的敏感内容。仓库提供决策支持，不替代医疗、法律、投资等专业服务。

MIT；研究中的简短引文见 [第三方声明](THIRD_PARTY_NOTICES.md)。
