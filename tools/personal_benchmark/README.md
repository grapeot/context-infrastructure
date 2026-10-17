# Personal Benchmark：新模型对我的工作有什么意义

从自己的真实任务形成可重复的比较，记录模型更新是否解除旧障碍、减少返工、推进讨论，或使新用途值得尝试。任务类别、验收标准和重要性随证据修订。

这是可选的本地参考工具，Python 3.10+，仅用标准库。Agent 利用已有 context 搜索与会话归档发现任务；工具负责冻结输入、登记实验、导入运行回执、匿名评价和报告。模型执行沿用使用者自己的 CLI/API 或工具环境。

## 先体验

从仓库根目录运行：

```bash
python tools/personal_benchmark/demo.py
python -m unittest discover -s tools/personal_benchmark -p 'test_*.py' -v
```

Demo 用两份预写答案走完流程，明确标注合成来源与模拟审阅。它没有模型调用、网络访问或私人历史读取，不产生模型成绩。默认数据目录 `.personal_benchmark/` 已由 Git 忽略。

发现与选择任务的原则见 [Personal Benchmark 工作流](../../rules/skills/workflow_personal_benchmark.md)。

## 从真实任务开始

Agent 在 `.personal_benchmark/drafts/<task>/` 整理候选，参考 [case.json](examples/case.json)。每个任务需要：

- 当时的起点、目标和独立任务组，保留跨会话关联与已知材料缺口。
- `sources`：定位及归属 `record`、`recollection`、`inference` 或 `synthetic`。
- `criteria`：具体验收，每项标记来自原要求 `original`、澄清 `clarification` 或事后检查 `retrospective`。
- `prompt_file` 和可选 `attachments`：模型可见材料；`rubric_file` 与可选 `evidence_files`：隐藏验收与证据。
- `limitations` 和有依据的重要性。没有个人判断时，重要性保持 `unknown`。

引用文件必须位于草稿目录内，使用相对路径；单文件最多8 MiB，附件使用简单文件名。准备不充分或暂停的任务留在候选中，只有 `status: ready` 能冻结。

```bash
python tools/personal_benchmark/bench.py freeze .personal_benchmark/drafts/task/case.json
```

输出的 `case` 是 `task_id/<完整版本哈希>`。内容相同返回原版本；输入、验收或来源说明改变后得到新版本。冻结后每次操作都会核对文件内容。原始来源仍由原系统维护，工具只复制显式选中的材料。

## 计划、执行与导入

准备配置列表，格式见 [configurations.json](examples/configurations.json)。填写准确的 `requested_model`，并在 `conditions` 记录 effort、工具权限、运行环境及时间/token预算。模型配置文件只存非敏感参数，认证留在既有运行工具。

```bash
python tools/personal_benchmark/bench.py plan TASK_ID/VERSION configs.json --repeats 2 --max-attempts 4 --event "模型更新后的复测"
python tools/personal_benchmark/bench.py export PLAN_ID a001 .personal_benchmark/work/a001
```

计划只登记尝试，最多100次。导出目录仅含 `prompt.txt` 和可见附件；输出同时给出输入哈希和请求配置。让被测模型只访问导出目录，另行配置其环境、工具及调用预算。导出本身不创建沙箱。需要观察真实工具行为的任务，应由独立执行环境提供日志及产物。

运行后准备回执 JSON，`output_file` 相对回执目录，失败也必须记录：

```json
{
  "status": "completed",
  "input_sha256": "复制 export 返回的 input_sha256",
  "output_file": "answer.txt",
  "resolved_model": null,
  "runtime": "实际CLI/API版本、工具环境及时间",
  "assistance": "必要澄清、纠正、人工接管；未知则 null",
  "usage": null,
  "checks": null,
  "error": null
}
```

```bash
python tools/personal_benchmark/bench.py record PLAN_ID a001 receipt.json
```

终态允许 `completed`、`error`、`timeout`、`cancelled`；完成必须提供答案，失败可以保存部分输出。每个计划槽位只允许提交一次。意外中断后先核对记录，新的尝试使用新计划，并在事件说明中关联原计划，保留失败。

工具核对回执声明的输入哈希，保留请求型号与实际型号两个字段；它无法独立证明外部调用使用了这些输入和型号。`resolved_model` 没有证据时保留 `null`。`checks` 是导入的检查结果，需要另留检查器版本及证据。每个新实验应同时重跑对照，跨时期结果须检查环境变化。

## 匿名评价与报告

所有计划尝试都有终态后生成固定的匿名队列：

```bash
python tools/personal_benchmark/bench.py blind PLAN_ID
```

将输出的队列交给审阅者。它包含任务、验收及打乱次序的答案，省略配置身份和运行元数据；非完成尝试单独计数。身份映射保存在本地 `review_snapshot/mapping.json`，应由编排者保管。附件需从同一可见输入中提供。答案自述或审阅者已见过身份仍可能破坏盲态，须写入 `prior_exposure`。

审阅 JSON 示例：

```json
{
  "reviewer_kind": "ai",
  "reviewer": "reviewer configuration or human identifier",
  "verdict": "unknown",
  "rationale": "哪些要求已验证，哪些材料不足",
  "next_evidence": "哪条新证据会改变当前判断",
  "prior_exposure": "是否见过答案、身份或旧评语",
  "personal_value": "unknown"
}
```

```bash
python tools/personal_benchmark/bench.py review PLAN_ID A001 judgment.json
python tools/personal_benchmark/bench.py unblind PLAN_ID
python tools/personal_benchmark/bench.py report PLAN_ID
```

`verdict` 支持 `satisfied`、`gap`、`failed`、`unknown`。完成全部答案的评价后才能解盲；已提交判断不覆盖，解盲后关闭匿名审阅。AI 判断保留 AI 归属，个人价值由人校准。报告保留失败、重复次数、各次帮助、验收来源与下一证据，不生成跨任务的模型总分。

## 数据与范围

本工具面向单用户顺序写入；冻结文件、计划和运行记录的哈希用于发现意外变化。中断造成不完整文件时保留现场并另建计划，不自动修复或重试外部调用。目录分离与哈希不是权限隔离或防篡改认证，审阅者身份是声明值。

真实草稿、证据、模型输出与报告均留在 `.personal_benchmark/`。指定 `--store` 到其他位置时，使用者负责其访问和版本控制策略。公开示例全部为合成内容。CLI 不配置认证、不联网、不执行回答中的代码、不修改 Observer/Reflector、不创建周期任务。

当前范围是一项任务条件的重复实验和结果记录。跨来源自动发现由工作流指导 Agent 完成；模型自动运行、长程工具隔离、交互工作台以及真实学习/工程收益验证可作为后续扩展。
