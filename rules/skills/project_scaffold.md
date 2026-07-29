# 项目脚手架与重整 Skill

把一个临时目录、散装脚本目录，或结构不完整的小项目，整理成可长期维护的标准项目形态。

**触发词**: "bootstrap 一个 project"、"scaffold 一个 project"、"把这个目录整理成项目"、"补齐 PRD/RFC/working"、"给这个目录单独建 git repo"

## 这个 Skill 解决什么问题

当 AI agent 在 workspace 里反复创建临时脚本和 ad-hoc 目录时，这些散件积累成无法被其他 agent 接手的"技术债"。这个 Skill 让每次 scaffold 都遵循统一的结构、文档、测试和 Git 规范，确保后续 agent 不需要猜命令或翻 README 就能接手工作。

核心价值：
- 让每个项目有一个统一的结构约定，减少 agent 间的交接成本
- 在动代码之前先立骨架、先写文档，避免边写边改结构
- 通过 public/private intake gate 避免隐私泄漏到公开仓库
- 在交付前强制跑测试和隐私扫描，保证可验证状态

## 什么时候应该用这个 Skill

- 用户说"新建一个项目"、"scaffold"、"bootstrap"
- 一个目录里已经有 2+ 个脚本/模块，并且还会继续迭代
- 需要独立 git 历史，不能混在 workspace 大仓库里
- 用户要求补 PRD/RFC/working 文档
- 需要把散件整理成可测试、可部署的标准项目

## 什么时候不应该用

- 一次性脚本，跑完就丢 → 直接放 `tmp/` 或 `adhoc_jobs/tmp_*/`
- 用户明确要求快速原型，不需要文档和测试 → 先做，等稳定后再 scaffold
- 目录已有成熟结构，只需要小改 → 不要大搬家

---

## 1. 适用场景

当一个目录已经不再是一次性脚本，而是会被反复修改、需要多轮 AI 接手、需要测试、需要频繁提交时，就应该升级成标准项目结构。

典型信号：

- 目录里已经有 2 个以上脚本/模块
- 用户明确要求补文档、加 tests、频繁 commit
- 未来会继续迭代，不只是一次性任务
- 需要独立 git 历史，不能一直混在 workspace 大仓库里

---

## 2. Public/Private Repo Intake Gate

**在动目录结构之前，必须先确认一件事：这个 repo 将来会不会发布到公开 GitHub。**

因为 privacy、skill 拆分、`.env.example` 处理、fake fixture 这些东西全部取决于这个答案。如果 scaffolding 已经完成才发现是 public repo，回头改的成本高得多。

### 确认方式

脚手架开始时，问用户：

> 这个 repo 以后会发到公开 GitHub 吗？还是只在自己的 workspace/私人 Git 里用？

选项：`public（会开源/发 GitHub）` / `private（只在本地用）`。

不要跳过这步。用户不说，就问。

### Public repo 必须做的事

如果确认是 public repo，以下内容是强制要求，不属于可选的优化：

1. **`.gitignore` 必须阻塞私密文件**。至少覆盖 `.env`、`.env.*`（保留 `!.env.example`）、`__pycache__/`、`.pytest_cache/`、`*.pyc`、`dist/`、`build/`、`*.egg-info/`、本地数据目录、日志目录。对于 Python 项目，加 `py.typed` 标记。

2. **必须创建 `.env.example`**。所有环境变量用 fake 占位符，不要留空。live test 所需的 env var 必须在 `.env.example` 里列出并写入 fake 值，形式上和真实 `.env` 一致，这样抄过去就能用。

3. **所有公开文件用 fake handles / domains / keys**。`README.md`、docs、tests、fixtures、scripts 里不能出现真实的邮箱、手机号、API key、内部路径、服务器地址、1Password vault 引用。常用 fake 占位符：
   - 邮箱：`alice@example.com`、`bob@example.net`
   - 手机号：`+15555550123`（北美测试号段）
   - API key：`replace-with-your-real-key`
   - 1Password：`op://your-vault/your-item/your-field`
   - 域名：`example.com`、`example.org`

4. **README 必须声明 publishable**。在 README 的 Privacy 节写清楚：`This repository is designed to be publishable with only fake examples.`

5. **如果项目包含 skill**，必须拆成两层。公开 repo 里放技术实现（CLI、测试、API contract、skill 的工作流文档），私有联系人、私有路由、私有 handle 放在 workspace 全局 skill 目录（如 `rules/skills/`）或私有 `.env` 中。公开 repo 的 skill 文档里要写清楚「私有 alias 在哪找」。参考 `adhoc_jobs/resend_email_skill/`（公开技术 skill）和 `rules/skills/imessage.md`（私有联系人路由）的拆分方式。

   Public skill repos should assume loose Markdown-based installation, not vendor-specific skill packaging. The README must explain how a human can hand the GitHub URL to Codex, Claude Code, Cursor, OpenCode, or another coding agent and ask it to install the skill. The AI installer should start from the target workspace's `AGENTS.md` or `CLAUDE.md`, follow any routing file such as `WORKSPACE.md`, and then add the public repo's root skill to the workspace discovery chain. If the workspace has `rules/skills/INDEX.md` or `skills/INDEX.md`, update that index; otherwise add a short pointer in `AGENTS.md` or `CLAUDE.md`.

   If the public repo contains multiple skills, expose exactly one root/router skill to the global workspace level. Use that root skill to link to focused local files inside the repo. Do not symlink every focused skill globally; that makes discovery noisy and makes private/public overlays harder to reason about.

6. **完成后的隐私检查**。在最终验证阶段（Phase 4），必须跑一次隐私扫描：

   ```bash
   rg -n "真实邮箱模式|真实手机号段|内部路径|op://" .
   ```

   零匹配才算通过。如果匹配到了，逐个修复后再扫。

### Private repo 的处理

如果确认是 private repo，不需要 fake fixtures 和隐私拆分。正常的 `.env.example` 和 `.gitignore` 仍然推荐，但不强制 fake 占位符。

---

## 3. 目标结构

最小推荐结构：

```text
project_root/
├── AGENTS.md
├── .gitignore
├── .env.example        # public repo 必须；private repo 推荐
├── docs/
│   ├── prd.md
│   ├── rfc.md
│   ├── working.md
│   └── test.md
├── src/
├── scripts/
├── tests/
└── <compat wrappers / entrypoints if needed>
```

### 每个目录/文件的职责

- `docs/prd.md`: 讲目标、用户、需求、成功标准
- `docs/rfc.md`: 讲架构、边界、关键设计决策、迁移策略
- `docs/working.md`: 两部分
  - `## Changelog`: 每天一个小标题，下面用简单 bullet 记当天改了什么
  - `## Lessons Learned`: 记录坑、约束、后续 agent 不该重复犯的错
- `docs/test.md`: 测试策略，写清 unit / integration / e2e 覆盖目标
- `src/`: 可复用源码，尽量放模块，不放面向用户的 shell 入口
- `scripts/`: 面向用户直接跑的 CLI、shell entrypoints、运维脚本
- `tests/`: 单测、集成测试、未来 e2e
- `AGENTS.md`: 这个项目自己的局部规则，尤其提醒更新 `working.md`、频繁 commit、环境要求

### 当前 workspace 推荐的前后端脚手架

如果项目明确是一个小到中等规模的 Web 应用，而且目标是**先快速做出可运行产品，再逐步演进**，当前 workspace 的默认推荐是：

- **后端**：FastAPI
- **前端**：React + Vite + TypeScript
- **本地存储**：优先 SQLite（除非用户明确要求更重的数据库）
- **生产部署**：先把前端 build 产物直接交给 FastAPI 统一 serve

推荐目录：

```text
project_root/
├── AGENTS.md
├── .gitignore
├── docs/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── scripts/
│   ├── start_backend.sh
│   ├── start_frontend.sh
│   └── build_frontend.sh
├── src/
│   └── <python package>
├── tests/
└── pyproject.toml
```

补充说明：

1. `frontend/` 独立维护 React/Vite 工程
2. `src/` 只放后端 Python 包，不把后端逻辑塞进根目录脚本
3. `scripts/` 提供面向人和 agent 的稳定入口，避免每次都现场猜命令
4. 生产模式优先走“FastAPI 同源托管前端 build”，这样 auth、prefix、部署路径都更容易保持一致

### 前后端项目至少要补齐的 3 个脚本

如果是 FastAPI + React 项目，默认应补齐：

1. `scripts/start_backend.sh`
   - 激活 `.venv`
   - 设置后端环境变量
   - 启动 `uvicorn`
2. `scripts/start_frontend.sh`
   - 设置前端 dev 所需环境变量
   - 启动 `npm run start_dev_server` 或等价命令
3. `scripts/build_frontend.sh`
   - 设置构建时 base path / token / api base 等变量
   - 执行 `npm run build`

不要把这些命令只写在 README 里。脚本本身就是 contract。

### URL prefix / root path 的默认建议

如果项目将来可能挂在子路径（例如 `/foo/bar`）下，必须在脚手架阶段就统一配置来源。

默认建议：

- 用**一个环境变量**统一驱动，比如 `APP_ROOT_PATH`
- 后端读取它并映射到 FastAPI `root_path`
- 前端读取它并映射到 Vite `base` 与 React Router `basename`
- `scripts/start_backend.sh`、`scripts/start_frontend.sh`、`scripts/build_frontend.sh` 都从这个单一变量派生各自配置

不要让后端、前端、反向代理分别维护三套前缀字符串。那样几乎一定会在部署到子路径时坏掉。

---

## 4. 推荐执行顺序

### Phase 0：确认 public/private

执行第 2 节的 intake gate：问用户这个 repo 将来会不会发公开 GitHub。

如果用户回答 public，整个 scaffolding 过程都要带着 public repo 的约束做（`.env.example` fake 值、`.gitignore` 阻塞私密文件、所有公开文件用 fake handles、skill 拆两层）。不要做完再回头改。

### Phase 1：确认项目边界

先判断三件事：

1. 这个目录是不是已经值得成为独立项目
2. 用户是否允许重整目录结构
3. 是否需要单独 nested git repo

如果用户没有授权重整现有项目结构，不要擅自大搬家。

### Phase 2：先立骨架，再迁代码

推荐顺序：

1. 建 `docs/ / src/ / scripts/ / tests/`
2. 写 `AGENTS.md`、`.gitignore`、`.env.example`
3. 先写 `prd.md` / `rfc.md` / `test.md`
4. 再把代码迁到 `src/`，把可执行入口放进 `scripts/`
5. 最后补 `working.md`
6. 在 `rules/WORKSPACE.md` 登记新项目的快捷路由。新增一行时同时写出读者会使用的别名、项目路径和一句用途，例如：`weather monitor` / `weather_monitor` → `adhoc_jobs/weather_monitor/`（家庭气象数据采集与告警）。

不要一边大改代码一边临时想目录结构。先把骨架立起来，后面的改动才会更稳。

### Phase 3：保兼容入口

如果外部已有 cron、脚本、用户习惯路径，不要第一刀就砍掉。优先保留兼容 wrapper：

- 老路径保留成 thin wrapper
- 新逻辑进 `src/` / `scripts/`

这样可以先完成重构，再逐步迁移调用方。

### Phase 4：验证与隐私检查

所有代码和测试完成后，必须跑一轮验证，顺序固定：

1. Lint（如果项目配置了 linter）。
2. 测试：先跑默认 offline 测试，再跑 opt-in integration test（如果有）。
3. Public repo 必须跑隐私扫描：

   ```bash
   rg -n "真实邮箱|真实手机号|内部服务器|op://|private key pattern" .
   ```

   零匹配才通过。如果匹配到了，逐个修复后再扫。

4. 把验证结果写进 `docs/working.md` 的当天 changelog，记录 xxx passed / xxx skipped / xxx found and fixed。

只有 Phase 4 全部通过，scaffolding 才算是交付完成。

---

## 5. Git 策略

如果目录需要长期维护，而且和 workspace 大仓库的历史无关，优先单独 `git init`。

推荐提交切法：

1. **scaffold commit**
   - docs/AGENTS/.gitignore/基础目录
2. **implementation commit**
   - 真正的代码迁移、模块化、测试
3. **validation commit**
   - `working.md` 记录、测试结果、回填或手工验证结果

不要把大重构、文档补齐、测试修复、历史 backfill 全塞进一个 commit。

---

## 5.5. CI / CD 配置

### CI（GitHub Actions）

如果项目有 tests，scaffold 阶段应默认配一个最小 CI workflow。不需要等用户要求。

最小 `.github/workflows/ci.yml`（Python + uv 项目示例）：

```yaml
name: CI
on:
  push:
    branches: [master, main]
  pull_request:
    branches: [master, main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      - name: Set up Python
        run: uv python install 3.12
      - name: Create venv and install dependencies
        run: |
          uv venv
          uv pip install -e '.[dev]'
      - name: Run tests
        run: uv run python -m pytest tests/ -v
```

注意事项：
- **不要用 `uv pip install --system`**，GitHub Actions runner 的 Python 是 externally-managed，会报错。用 `uv venv` + `uv pip install` 代替。
- 分支名要兼容 `master` 和 `main`，不要假设只有一个。
- 如果项目有 lint 配置，CI 里加上 lint step。

### CD（持续部署）

CD 不属于 scaffold 默认配置。常见方式：
- **Vercel**：连接 GitHub repo 后自动部署，不需要 CI 配置
- **Koyeb / Railway**：类似，连接 repo 自动部署
- **自托管**：需要单独的 deploy workflow

如果用户要求配 CD，参考 `rules/skills/deployment_github_actions_koyeb.md`。

### Branch Protection

Private repo 的 branch protection 需要 GitHub Pro 或更高 plan。如果用户要求配但 plan 不够，告诉用户并跳过，不要卡住流程。

---

## 6. AGENTS.md 最少要写什么

项目局部 `AGENTS.md` 至少要覆盖：

1. 项目结构说明
2. `working.md` 更新要求
3. 频繁 commit 的要求
4. 本项目 Python / Node / shell 环境约束
5. 任何不能破坏的兼容约束

如果这个文件不写，后续 agent 很容易把项目重新写回临时脚本堆。

---

## 7. working.md 维护要求

### Changelog

- 每天一个日期小标题
- 每个 bullet 只写一个改动
- 不用 nested bullet points
- 不要写空话，比如“做了一些优化”

### Lessons Learned

只写真会帮助后续 agent 避坑的内容，例如：

- 哪些文件是兼容 wrapper，不能直接删
- 哪些输出格式是外部依赖的 contract
- 哪些本地数据源看起来像主数据源，其实只是辅助索引

---

## 8. test.md 应该写什么

至少要说明：

- unit tests 覆盖哪些纯逻辑
- integration tests 依赖哪些本地数据或服务
- e2e 是否存在，如果暂时没有，也要写清楚为什么没有
- 手工验证要看什么 artifact

`test.md` 的价值不是重复 pytest 命令，而是让后续 agent 知道“什么算验证完成”。

---

## 9. 重整已有项目时的硬规则

1. 没有用户许可，不要擅自大规模迁目录
2. 先建骨架，再搬代码
3. 先保兼容，再删旧入口
4. 每次阶段性完成后更新 `working.md`
5. 每个阶段都要有可运行或可验证状态

---

## 10. 一句话判断标准

如果一个目录未来还会被继续改，而且希望不同 AI/人能低成本接手，那它就不该继续保持“散装脚本目录”状态，而应该尽快升级成上面这套项目骨架。

如果这个 repo 将来要发公开 GitHub，Phase 0 必须问过用户，Phase 4 的隐私扫描不能跳过。

---

## 11. 常见坑

### Vercel Python 部署

- `vercel.json` 的 `builds` + `routes` 格式已废弃，用 `rewrites` 现代格式。旧格式会被当 Next.js 项目处理，返回 Vercel 默认页面而不是你的 app。
- Vercel Python runtime 不认 `src/` layout。如果包放在 `src/` 下，入口文件（如 `api/index.py`）需要手动 `sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))`。
- Vercel 需要一个 `requirements.txt`（或 `pyproject.toml` 会被自动识别）来安装 Python 依赖。
- Vercel team SSO / Deployment Protection 会保护随机 deployment URL，但 alias 域名（如 `project.vercel.app`）通常不受影响。

### GitHub Actions CI

- `uv pip install --system` 在 GitHub Actions runner 上会失败（externally-managed Python）。用 `uv venv` + `uv pip install` 代替。
- CI 里的分支名要同时覆盖 `master` 和 `main`，不要假设只有一个。

### Branch Protection

- Private repo 的 branch protection 需要 GitHub Pro。Free plan 只能对 public repo 设 branch protection。
- `gh api repos/.../rulesets` 和 `gh api repos/.../branches/.../protection` 都会返回 403 如果 plan 不够。
