# Awesome Copilot Skills 查阅与安装

## 元数据

- **类型**: Reference
- **适用场景**: 从 [github/awesome-copilot/skills](https://github.com/github/awesome-copilot/tree/main/skills) 发现、安装 365 个社区 Agent Skills
- **上游来源**: [github/awesome-copilot](https://github.com/github/awesome-copilot)（MIT）
- **生成日期**: 2026-06-27（`adhoc_jobs/import_awesome_copilot_skills/generate_reference.py`）
- **user-invocable**: true

---

## 何时触发

本地 `INDEX.md` 无覆盖；需要 bundled scripts/assets；Azure/AWS/ADR/spec/agent 安全等 Copilot 生态能力。

## 发现与安装

- 浏览：[awesome-copilot.github.com/skills](https://awesome-copilot.github.com/skills)
- 索引源：[docs/README.skills.md](https://github.com/github/awesome-copilot/blob/main/docs/README.skills.md)

```bash
gh skills install github/awesome-copilot <skill-name>
# 或
cp -r /tmp/awesome-copilot/skills/<name> ~/.cursor/skills/<name>
```

**不要** bulk import 进 `rules/skills/`；按需 vendor + 本地 overlay 私有配置。

上游更新后重新生成本文件：

```bash
python adhoc_jobs/import_awesome_copilot_skills/generate_reference.py
```

---

## Skill 目录（365）

### A

- **`acquire-codebase-knowledge`** — Use this skill when the user explicitly asks to map, document, or onboard into an existing codebase. Trigger for prompts like "map this codebase", "document this architecture", "onboard me to this repo", or "create codebase docs". Do not trigger for routine feature implementation, bug fixes, or narrow code edits unless the user asks for repository-level discovery.
  - **资产**: `assets/templates`, `references/inquiry-checkpoints.md`, `references/stack-detection.md`, `scripts/scan.py`
  - 安装：`gh skills install github/awesome-copilot acquire-codebase-knowledge`
  - 上游：[skills/acquire-codebase-knowledge/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/acquire-codebase-knowledge/SKILL.md)

- **`acreadiness-assess`** — Run the AgentRC readiness assessment on the current repository and produce a static HTML dashboard at reports/index.html. Wraps `npx github:microsoft/agentrc readiness` and hands off rendering to the @ai-readiness-reporter custom agent. Supports policies (--policy) for org-specific scoring. Use when asked to assess, audit, or score the AI readiness of a repo.
  - **资产**: `report-template.html`
  - 安装：`gh skills install github/awesome-copilot acreadiness-assess`
  - 上游：[skills/acreadiness-assess/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/acreadiness-assess/SKILL.md)

- **`acreadiness-generate-instructions`** — Generate tailored AI agent instruction files via AgentRC instructions command. Produces .github/copilot-instructions.md (default, recommended for Copilot in VS Code) plus optional per-area .instructions.md files with applyTo globs for monorepos. Use after running /acreadiness-assess to close gaps in the AI Tooling pillar.
  - 安装：`gh skills install github/awesome-copilot acreadiness-generate-instructions`
  - 上游：[skills/acreadiness-generate-instructions/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/acreadiness-generate-instructions/SKILL.md)

- **`acreadiness-policy`** — Help the user pick, write, or apply an AgentRC policy. Policies customise readiness scoring by disabling irrelevant checks, overriding impact/level, setting pass-rate thresholds, or chaining org baselines with team overrides. Use when the user asks about strict mode, AI-only scoring, custom weights, CI gating, or wants org-wide standardisation.
  - 安装：`gh skills install github/awesome-copilot acreadiness-policy`
  - 上游：[skills/acreadiness-policy/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/acreadiness-policy/SKILL.md)

- **`add-educational-comments`** — Add educational comments to the file specified, or prompt asking for file to comment if one is not provided.
  - 安装：`gh skills install github/awesome-copilot add-educational-comments`
  - 上游：[skills/add-educational-comments/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/add-educational-comments/SKILL.md)

- **`adobe-illustrator-scripting`** — Write, debug, and optimize Adobe Illustrator automation scripts using ExtendScript (JavaScript/JSX). Use when creating or modifying scripts that manipulate documents, layers, paths, text frames, colors, symbols, artboards, or any Illustrator DOM objects. Covers the complete JavaScript object model, coordinate system, measurement units, export workflows, and scripting best practices.
  - **资产**: `references/object-model-quick-reference.md`, `scripts/batch-export-png.jsx`, `scripts/create-color-grid.jsx`, `scripts/find-replace-text.jsx`
  - 安装：`gh skills install github/awesome-copilot adobe-illustrator-scripting`
  - 上游：[skills/adobe-illustrator-scripting/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/adobe-illustrator-scripting/SKILL.md)

- **`agent-governance`** — Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use this skill when: - Building AI agents that call external tools (APIs, databases, file systems) - Implementing policy-based access controls for agent tool usage - Adding semantic intent classification to detect dangerous prompts - Creating trust scoring systems for multi-agent workflows - Building audit trails for agent actions and decisions - Enforcing rate limits, content filters, or tool restrictions on agents - Working with any agent framework (PydanticAI, CrewAI, OpenAI Agents, LangChain, AutoGen)
  - 安装：`gh skills install github/awesome-copilot agent-governance`
  - 上游：[skills/agent-governance/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/agent-governance/SKILL.md)

- **`agent-owasp-compliance`** — Check any AI agent codebase against the OWASP Agentic Security Initiative (ASI) Top 10 risks. Use this skill when: - Evaluating an agent system's security posture before production deployment - Running a compliance check against OWASP ASI 2026 standards - Mapping existing security controls to the 10 agentic risks - Generating a compliance report for security review or audit - Comparing agent framework security features against the standard - Any request like "is my agent OWASP compliant?", "check ASI compliance", or "agentic security audit"
  - 安装：`gh skills install github/awesome-copilot agent-owasp-compliance`
  - 上游：[skills/agent-owasp-compliance/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/agent-owasp-compliance/SKILL.md)

- **`agent-supply-chain`** — Verify supply chain integrity for AI agent plugins, tools, and dependencies. Use this skill when: - Generating SHA-256 integrity manifests for agent plugins or tool packages - Verifying that installed plugins match their published manifests - Detecting tampered, modified, or untracked files in agent tool directories - Auditing dependency pinning and version policies for agent components - Building provenance chains for agent plugin promotion (dev → staging → production) - Any request like "verify plugin integrity", "generate manifest", "check supply chain", or "sign this plugin"
  - 安装：`gh skills install github/awesome-copilot agent-supply-chain`
  - 上游：[skills/agent-supply-chain/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/agent-supply-chain/SKILL.md)

- **`agentic-eval`** — Patterns and techniques for evaluating and improving AI agent outputs. Use this skill when: - Implementing self-critique and reflection loops - Building evaluator-optimizer pipelines for quality-critical generation - Creating test-driven code refinement workflows - Designing rubric-based or LLM-as-judge evaluation systems - Adding iterative improvement to agent outputs (code, reports, analysis) - Measuring and improving agent response quality
  - 安装：`gh skills install github/awesome-copilot agentic-eval`
  - 上游：[skills/agentic-eval/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/agentic-eval/SKILL.md)

- **`ai-prompt-engineering-safety-review`** — Comprehensive AI prompt engineering safety review and improvement prompt. Analyzes prompts for safety, bias, security vulnerabilities, and effectiveness while providing detailed improvement recommendations with extensive frameworks, testing methodologies, and educational content.
  - 安装：`gh skills install github/awesome-copilot ai-prompt-engineering-safety-review`
  - 上游：[skills/ai-prompt-engineering-safety-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ai-prompt-engineering-safety-review/SKILL.md)

- **`ai-ready`** — Make any repo AI-ready — analyzes your codebase and generates AGENTS.md, copilot-instructions.md, CI workflows, issue templates, and more. Mines your PR review patterns and creates files customized to your stack. USE THIS SKILL when the user asks to "make this repo ai-ready", "set up AI config", or "prepare this repo for AI contributions".
  - 安装：`gh skills install github/awesome-copilot ai-ready`
  - 上游：[skills/ai-ready/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ai-ready/SKILL.md)

- **`ai-team-orchestration`** — Bootstrap and run a multi-agent AI development team. Use when: starting a new software project with AI agents, setting up parallel dev/QA teams, creating sprint plans, writing brainstorm prompts with distinct agent voices, recovering a project workflow, or planning sprints.
  - **资产**: `references/anti-patterns.md`, `references/brainstorm-format.md`, `references/project-brief-template.md`, `references/sprint-plan-template.md`
  - 安装：`gh skills install github/awesome-copilot ai-team-orchestration`
  - 上游：[skills/ai-team-orchestration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ai-team-orchestration/SKILL.md)

- **`appinsights-instrumentation`** — Instrument a webapp to send useful telemetry data to Azure App Insights
  - **资产**: `LICENSE.txt`, `examples`, `references/ASPNETCORE.md`, `references/AUTO.md`, `references/NODEJS.md`, `references/PYTHON.md`, `scripts/appinsights.ps1`
  - 安装：`gh skills install github/awesome-copilot appinsights-instrumentation`
  - 上游：[skills/appinsights-instrumentation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/appinsights-instrumentation/SKILL.md)

- **`apple-appstore-reviewer`** — Serves as a reviewer of the codebase with instructions on looking for Apple App Store optimizations or rejection reasons.
  - 安装：`gh skills install github/awesome-copilot apple-appstore-reviewer`
  - 上游：[skills/apple-appstore-reviewer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/apple-appstore-reviewer/SKILL.md)

- **`arch-linux-triage`** — Triage and resolve Arch Linux issues with pacman, systemd, and rolling-release best practices.
  - 安装：`gh skills install github/awesome-copilot arch-linux-triage`
  - 上游：[skills/arch-linux-triage/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arch-linux-triage/SKILL.md)

- **`architecture-blueprint-generator`** — Comprehensive project architecture blueprint generator that analyzes codebases to create detailed architectural documentation. Automatically detects technology stacks and architectural patterns, generates visual diagrams, documents implementation patterns, and provides extensible blueprints for maintaining architectural consistency and guiding new development.
  - 安装：`gh skills install github/awesome-copilot architecture-blueprint-generator`
  - 上游：[skills/architecture-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/architecture-blueprint-generator/SKILL.md)

- **`arduino-azure-iot-edge-integration`** — Design and implement Arduino integration with Azure IoT Hub and IoT Edge, including secure provisioning, resilient telemetry, command handling, and production guardrails.
  - **资产**: `references/arduino-iot-checklist.md`, `references/arduino-official-best-practices.md`
  - 安装：`gh skills install github/awesome-copilot arduino-azure-iot-edge-integration`
  - 上游：[skills/arduino-azure-iot-edge-integration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arduino-azure-iot-edge-integration/SKILL.md)

- **`arize-ai-provider-integration`** — Creates, reads, updates, and deletes Arize AI integrations that store LLM provider credentials used by evaluators and other Arize features. Supports any LLM provider (e.g. OpenAI, Anthropic, Azure OpenAI, AWS Bedrock, Vertex AI, Gemini, NVIDIA NIM). Use when the user mentions AI integration, LLM provider credentials, create integration, list integrations, update credentials, delete integration, or connecting an LLM provider to Arize.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-ai-provider-integration`
  - 上游：[skills/arize-ai-provider-integration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-ai-provider-integration/SKILL.md)

- **`arize-annotation`** — Creates and manages annotation configs (categorical, continuous, freeform label schemas) and annotation queues (human review workflows) on Arize. Applies human annotations to project spans via the Python SDK. Use when the user mentions annotation config, annotation queue, label schema, human feedback, bulk annotate spans, update_annotations, labeling queue, annotate record, or human review.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-annotation`
  - 上游：[skills/arize-annotation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-annotation/SKILL.md)

- **`arize-dataset`** — Creates, manages, and queries Arize datasets and examples. Covers dataset CRUD, appending examples, exporting data, and file-based dataset creation using the ax CLI. Use when the user needs test data, evaluation examples, or mentions create dataset, list datasets, export dataset, append examples, dataset version, golden dataset, or test set.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-dataset`
  - 上游：[skills/arize-dataset/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-dataset/SKILL.md)

- **`arize-evaluator`** — Handles LLM-as-judge evaluation workflows on Arize including creating/updating evaluators, running evaluations on spans or experiments, managing tasks, trigger-run operations, column mapping, and continuous monitoring. Use when the user mentions create evaluator, LLM judge, hallucination, faithfulness, correctness, relevance, run eval, score spans, score experiment, trigger-run, column mapping, continuous monitoring, or improve evaluator prompt.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-evaluator`
  - 上游：[skills/arize-evaluator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-evaluator/SKILL.md)

- **`arize-experiment`** — Creates, runs, and analyzes Arize experiments for evaluating and comparing model performance. Covers experiment CRUD, exporting runs, comparing results, and evaluation workflows using the ax CLI. Use when the user mentions create experiment, run experiment, compare models, model performance, evaluate AI, experiment results, benchmark, A/B test models, or measure accuracy.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-experiment`
  - 上游：[skills/arize-experiment/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-experiment/SKILL.md)

- **`arize-instrumentation`** — Adds Arize AX tracing to an LLM application for the first time. Follows a two-phase agent-assisted flow to analyze the codebase then implement instrumentation after user confirmation. Use when the user wants to instrument their app, add tracing from scratch, set up LLM observability, integrate OpenTelemetry or openinference, or get started with Arize tracing.
  - **资产**: `references/ax-profiles.md`
  - 安装：`gh skills install github/awesome-copilot arize-instrumentation`
  - 上游：[skills/arize-instrumentation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-instrumentation/SKILL.md)

- **`arize-link`** — Generates deep links to the Arize UI for traces, spans, sessions, datasets, labeling queues, evaluators, and annotation configs. Produces clickable URLs for sharing Arize resources with team members. Use when the user wants to link to or open a trace, span, session, dataset, evaluator, or annotation config in the Arize UI.
  - **资产**: `references/EXAMPLES.md`
  - 安装：`gh skills install github/awesome-copilot arize-link`
  - 上游：[skills/arize-link/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-link/SKILL.md)

- **`arize-prompt-optimization`** — Optimizes, improves, and debugs LLM prompts using production trace data, evaluations, and annotations. Extracts prompts from spans, gathers performance signal, and runs a data-driven optimization loop using the ax CLI. Use when the user mentions optimize prompt, improve prompt, make AI respond better, improve output quality, prompt engineering, prompt tuning, or system prompt improvement.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-prompt-optimization`
  - 上游：[skills/arize-prompt-optimization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-prompt-optimization/SKILL.md)

- **`arize-trace`** — Downloads, exports, and inspects existing Arize traces and spans to understand what an LLM app is doing or debug runtime issues. Covers exporting traces by ID, spans by ID, sessions by ID, and root-cause investigation using the ax CLI. Use when the user wants to look at existing trace data, see what their LLM app is doing, export traces, download spans, investigate errors, or analyze behavior regressions.
  - **资产**: `references/ax-profiles.md`, `references/ax-setup.md`
  - 安装：`gh skills install github/awesome-copilot arize-trace`
  - 上游：[skills/arize-trace/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/arize-trace/SKILL.md)

- **`aspire`** — Aspire skill covering the Aspire CLI, AppHost orchestration, service discovery, integrations, MCP server, VS Code extension, Dev Containers, GitHub Codespaces, templates, dashboard, and deployment. Use when the user asks to create, run, debug, configure, deploy, or troubleshoot an Aspire distributed application.
  - **资产**: `references/architecture.md`, `references/cli-reference.md`, `references/dashboard.md`, `references/deployment.md`, `references/integrations-catalog.md`, `references/mcp-server.md`, `references/polyglot-apis.md`, `references/testing.md`, `references/troubleshooting.md`
  - 安装：`gh skills install github/awesome-copilot aspire`
  - 上游：[skills/aspire/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aspire/SKILL.md)

- **`aspnet-minimal-api-openapi`** — Create ASP.NET Minimal API endpoints with proper OpenAPI documentation
  - 安装：`gh skills install github/awesome-copilot aspnet-minimal-api-openapi`
  - 上游：[skills/aspnet-minimal-api-openapi/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aspnet-minimal-api-openapi/SKILL.md)

- **`audit-integrity`** — Shared audit integrity framework for all AppSec agents — enforces output quality, intellectual honesty, and continuous improvement through anti-rationalization guards, self-critique loops, retry protocols, non-negotiable behaviors, self-reflection quality gates (1-10 scoring, ≥8 threshold), and a self-learning system with lesson/memory governance for security analysis agents.
  - **资产**: `references/anti-rationalization-guard.md`, `references/clarification-protocol.md`, `references/non-negotiable-behaviors.md`, `references/retry-protocol.md`, `references/self-critique-loop.md`, `references/self-learning-system.md`, `references/self-reflection-quality-gate.md`
  - 安装：`gh skills install github/awesome-copilot audit-integrity`
  - 上游：[skills/audit-integrity/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/audit-integrity/SKILL.md)

- **`automate-this`** — Analyze a screen recording of a manual process and produce targeted, working automation scripts. Extracts frames and audio narration from video files, reconstructs the step-by-step workflow, and proposes automation at multiple complexity levels using tools already installed on the user machine.
  - 安装：`gh skills install github/awesome-copilot automate-this`
  - 上游：[skills/automate-this/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/automate-this/SKILL.md)

- **`autoresearch`** — Autonomous iterative experimentation loop for any programming task. Guides the user through defining goals, measurable metrics, and scope constraints, then runs an autonomous loop of code changes, testing, measuring, and keeping/discarding results. Inspired by Karpathy's autoresearch. USE FOR: autonomous improvement, iterative optimization, experiment loop, auto research, performance tuning, automated experimentation, hill climbing, try things automatically, optimize code, run experiments, autonomous coding loop. DO NOT USE FOR: one-shot tasks, simple bug fixes, code review, or tasks without a measurable metric.
  - 安装：`gh skills install github/awesome-copilot autoresearch`
  - 上游：[skills/autoresearch/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/autoresearch/SKILL.md)

- **`aws-cdk-python-setup`** — Setup and initialization guide for developing AWS CDK (Cloud Development Kit) applications in Python. This skill enables users to configure environment prerequisites, create new CDK projects, manage dependencies, and deploy to AWS.
  - 安装：`gh skills install github/awesome-copilot aws-cdk-python-setup`
  - 上游：[skills/aws-cdk-python-setup/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aws-cdk-python-setup/SKILL.md)

- **`aws-cloudwatch-investigation`** — Reusable investigation patterns for AWS CloudWatch: Logs Insights query templates, alarm-to-deployment correlation, blast-radius narrowing decision tree, and PromQL-style metric query patterns for structured incident triage.
  - 安装：`gh skills install github/awesome-copilot aws-cloudwatch-investigation`
  - 上游：[skills/aws-cloudwatch-investigation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aws-cloudwatch-investigation/SKILL.md)

- **`aws-cost-optimize`** — Analyze AWS resources used in the app (IaC files and/or resources in a target account/region) and optimize costs - creating GitHub issues for identified optimizations.
  - 安装：`gh skills install github/awesome-copilot aws-cost-optimize`
  - 上游：[skills/aws-cost-optimize/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aws-cost-optimize/SKILL.md)

- **`aws-resource-health-diagnose`** — Analyze AWS resource health, diagnose issues from CloudWatch logs and metrics, and create a remediation plan for identified problems.
  - 安装：`gh skills install github/awesome-copilot aws-resource-health-diagnose`
  - 上游：[skills/aws-resource-health-diagnose/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aws-resource-health-diagnose/SKILL.md)

- **`aws-resource-query`** — Query AWS resources using natural language. Covers EC2, S3, RDS, Lambda, ECS, EKS, Secrets Manager, IAM, VPC, networking, messaging, and more. Strictly read-only — no writes, deletes, or mutations.
  - 安装：`gh skills install github/awesome-copilot aws-resource-query`
  - 上游：[skills/aws-resource-query/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aws-resource-query/SKILL.md)

- **`aws-well-architected-review`** — Perform an AWS Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements.
  - 安装：`gh skills install github/awesome-copilot aws-well-architected-review`
  - 上游：[skills/aws-well-architected-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/aws-well-architected-review/SKILL.md)

- **`az-cost-optimize`** — Analyze Azure resources used in the app (IaC files and/or resources in a target rg) and optimize costs - creating GitHub issues for identified optimizations.
  - 安装：`gh skills install github/awesome-copilot az-cost-optimize`
  - 上游：[skills/az-cost-optimize/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/az-cost-optimize/SKILL.md)

- **`azure-architecture-autopilot`** — Design Azure infrastructure using natural language, or analyze existing Azure resources to auto-generate architecture diagrams, refine them through conversation, and deploy with Bicep. When to use this skill: - "Create X on Azure", "Set up a RAG architecture" (new design) - "Analyze my current Azure infrastructure", "Draw a diagram for rg-xxx" (existing analysis) - "Foundry is slow", "I want to reduce costs", "Strengthen security" (natural language modification) - Azure resource deployment, Bicep template generation, IaC code generation - Microsoft Foundry, AI Search, OpenAI, Fabric, ADLS Gen2, Databricks, and all Azure services
  - **资产**: `.gitignore`, `assets/06-architecture-diagram.png`, `assets/07-azure-portal-resources.png`, `assets/08-deployment-succeeded.png`, `references/ai-data.md`, `references/architecture-guidance-sources.md`, `references/azure-common-patterns.md`, `references/azure-dynamic-sources.md`, `references/bicep-generator.md`, `references/bicep-reviewer.md`, `references/phase0-scanner.md`, `references/phase1-advisor.md`, `references/phase4-deployer.md`, `references/service-gotchas.md`, `scripts/cli.py`, `scripts/generator.py`, `scripts/icons.py`
  - 安装：`gh skills install github/awesome-copilot azure-architecture-autopilot`
  - 上游：[skills/azure-architecture-autopilot/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-architecture-autopilot/SKILL.md)

- **`azure-deployment-preflight`** — Performs comprehensive preflight validation of Bicep deployments to Azure, including template syntax validation, what-if analysis, and permission checks. Use this skill before any deployment to Azure to preview changes, identify potential issues, and ensure the deployment will succeed. Activate when users mention deploying to Azure, validating Bicep files, checking deployment permissions, previewing infrastructure changes, running what-if, or preparing for azd provision.
  - **资产**: `references/ERROR-HANDLING.md`, `references/REPORT-TEMPLATE.md`, `references/VALIDATION-COMMANDS.md`
  - 安装：`gh skills install github/awesome-copilot azure-deployment-preflight`
  - 上游：[skills/azure-deployment-preflight/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-deployment-preflight/SKILL.md)

- **`azure-devops-cli`** — Manage Azure DevOps resources via CLI including projects, repos, pipelines, builds, pull requests, work items, artifacts, and service endpoints. Use when working with Azure DevOps, az commands, devops automation, CI/CD, or when user mentions Azure DevOps CLI.
  - **资产**: `references/advanced-usage.md`, `references/boards-and-iterations.md`, `references/org-and-security.md`, `references/pipelines-and-builds.md`, `references/repos-and-prs.md`, `references/variables-and-agents.md`, `references/workflows-and-patterns.md`
  - 安装：`gh skills install github/awesome-copilot azure-devops-cli`
  - 上游：[skills/azure-devops-cli/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-devops-cli/SKILL.md)

- **`azure-pricing`** — Fetches real-time Azure retail pricing using the Azure Retail Prices API (prices.azure.com) and estimates Copilot Studio agent credit consumption. Use when the user asks about the cost of any Azure service, wants to compare SKU prices, needs pricing data for a cost estimate, mentions Azure pricing, Azure costs, Azure billing, or asks about Copilot Studio pricing, Copilot Credits, or agent usage estimation. Covers compute, storage, networking, databases, AI, Copilot Studio, and all other Azure service families.
  - **资产**: `references/COPILOT-STUDIO-RATES.md`, `references/COST-ESTIMATOR.md`, `references/REGIONS.md`, `references/SERVICE-NAMES.md`
  - 安装：`gh skills install github/awesome-copilot azure-pricing`
  - 上游：[skills/azure-pricing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-pricing/SKILL.md)

- **`azure-resource-health-diagnose`** — Analyze Azure resource health, diagnose issues from logs and telemetry, and create a remediation plan for identified problems.
  - 安装：`gh skills install github/awesome-copilot azure-resource-health-diagnose`
  - 上游：[skills/azure-resource-health-diagnose/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-resource-health-diagnose/SKILL.md)

- **`azure-resource-visualizer`** — Analyze Azure resource groups and generate detailed Mermaid architecture diagrams showing the relationships between individual resources. Use this skill when the user asks for a diagram of their Azure resources or help in understanding how the resources relate to each other.
  - **资产**: `LICENSE.txt`, `assets/template-architecture.md`
  - 安装：`gh skills install github/awesome-copilot azure-resource-visualizer`
  - 上游：[skills/azure-resource-visualizer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-resource-visualizer/SKILL.md)

- **`azure-role-selector`** — When user is asking for guidance for which role to assign to an identity given desired permissions, this agent helps them understand the role that will meet the requirements with least privilege access and how to apply that role.
  - **资产**: `LICENSE.txt`
  - 安装：`gh skills install github/awesome-copilot azure-role-selector`
  - 上游：[skills/azure-role-selector/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-role-selector/SKILL.md)

- **`azure-smart-city-iot-solution-builder`** — Design and plan end-to-end Azure IoT and Smart City solutions: requirements, architecture, security, operations, cost, and a phased delivery plan with concrete implementation artifacts.
  - **资产**: `references/smart-city-solution-template.md`
  - 安装：`gh skills install github/awesome-copilot azure-smart-city-iot-solution-builder`
  - 上游：[skills/azure-smart-city-iot-solution-builder/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-smart-city-iot-solution-builder/SKILL.md)

- **`azure-static-web-apps`** — Helps create, configure, and deploy Azure Static Web Apps using the SWA CLI. Use when deploying static sites to Azure, setting up SWA local development, configuring staticwebapp.config.json, adding Azure Functions APIs to SWA, or setting up GitHub Actions CI/CD for Static Web Apps.
  - 安装：`gh skills install github/awesome-copilot azure-static-web-apps`
  - 上游：[skills/azure-static-web-apps/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-static-web-apps/SKILL.md)

### B

- **`batch-files`** — Expert-level Windows batch file (.bat/.cmd) skill for writing, debugging, and maintaining CMD scripts. Use when asked to "create a batch file", "write a .bat script", "automate a Windows task", "CMD scripting", "batch automation", "scheduled task script", "Windows shell script", or when working with .bat/.cmd files in the workspace. Covers cmd.exe syntax, environment variables, control flow, string processing, error handling, and integration with system tools.
  - **资产**: `assets/executable.txt`, `assets/library.txt`, `assets/task.txt`, `references/batch-files-and-functions.md`, `references/cygwin.md`, `references/msys2.md`, `references/tools-and-resources.md`, `references/windows-commands.md`, `references/windows-subsystem-on-linux.md`
  - 安装：`gh skills install github/awesome-copilot batch-files`
  - 上游：[skills/batch-files/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/batch-files/SKILL.md)

- **`bigquery-pipeline-audit`** — Audits Python + BigQuery pipelines for cost safety, idempotency, and production readiness. Returns a structured report with exact patch locations.
  - 安装：`gh skills install github/awesome-copilot bigquery-pipeline-audit`
  - 上游：[skills/bigquery-pipeline-audit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/bigquery-pipeline-audit/SKILL.md)

- **`boost-prompt`** — Interactive prompt refinement workflow: interrogates scope, deliverables, constraints; copies final markdown to clipboard; never writes code. Requires the Joyride extension.
  - 安装：`gh skills install github/awesome-copilot boost-prompt`
  - 上游：[skills/boost-prompt/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/boost-prompt/SKILL.md)

- **`brag-sheet`** — Turn vague "what did I do?" into evidence-backed impact statements for performance reviews, self-reviews, promotion packets, and weekly updates. Uniquely mines Copilot CLI session logs to reconstruct forgotten work, plus git commits and GitHub PRs. Enforces a 3-part impact contract (action → result → evidence). Works standalone with zero dependencies. Trigger for: "brag", "log work", "what did I do", "backfill my work history", "performance review", "self-review", "self assessment", "write impact statement", "review prep", "promo packet", "promotion case", "weekly update", "status report", "accomplishments", "what did I ship", "I forgot to log my work", "summarize my work", "track my wins", "what should I highlight", "end of half", "career growth", "work journal", or any request to document, summarize, or organize work accomplishments.
  - 安装：`gh skills install github/awesome-copilot brag-sheet`
  - 上游：[skills/brag-sheet/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/brag-sheet/SKILL.md)

- **`breakdown-epic-arch`** — Prompt for creating the high-level technical architecture for an Epic, based on a Product Requirements Document.
  - 安装：`gh skills install github/awesome-copilot breakdown-epic-arch`
  - 上游：[skills/breakdown-epic-arch/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-epic-arch/SKILL.md)

- **`breakdown-epic-pm`** — Prompt for creating an Epic Product Requirements Document (PRD) for a new epic. This PRD will be used as input for generating a technical architecture specification.
  - 安装：`gh skills install github/awesome-copilot breakdown-epic-pm`
  - 上游：[skills/breakdown-epic-pm/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-epic-pm/SKILL.md)

- **`breakdown-feature-implementation`** — Prompt for creating detailed feature implementation plans, following Epoch monorepo structure.
  - 安装：`gh skills install github/awesome-copilot breakdown-feature-implementation`
  - 上游：[skills/breakdown-feature-implementation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-feature-implementation/SKILL.md)

- **`breakdown-feature-prd`** — Prompt for creating Product Requirements Documents (PRDs) for new features, based on an Epic.
  - 安装：`gh skills install github/awesome-copilot breakdown-feature-prd`
  - 上游：[skills/breakdown-feature-prd/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-feature-prd/SKILL.md)

- **`breakdown-plan`** — Issue Planning and Automation prompt that generates comprehensive project plans with Epic > Feature > Story/Enabler > Test hierarchy, dependencies, priorities, and automated tracking.
  - 安装：`gh skills install github/awesome-copilot breakdown-plan`
  - 上游：[skills/breakdown-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-plan/SKILL.md)

- **`breakdown-test`** — Test Planning and Quality Assurance prompt that generates comprehensive test strategies, task breakdowns, and quality validation plans for GitHub projects.
  - 安装：`gh skills install github/awesome-copilot breakdown-test`
  - 上游：[skills/breakdown-test/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-test/SKILL.md)

### C

- **`centos-linux-triage`** — Triage and resolve CentOS issues using RHEL-compatible tooling, SELinux-aware practices, and firewalld.
  - 安装：`gh skills install github/awesome-copilot centos-linux-triage`
  - 上游：[skills/centos-linux-triage/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/centos-linux-triage/SKILL.md)

- **`chrome-devtools`** — Expert-level browser automation, debugging, and performance analysis using Chrome DevTools MCP. Use for interacting with web pages, capturing screenshots, analyzing network traffic, and profiling performance.
  - 安装：`gh skills install github/awesome-copilot chrome-devtools`
  - 上游：[skills/chrome-devtools/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/chrome-devtools/SKILL.md)

- **`cli-mastery`** — Interactive training for the GitHub Copilot CLI. Guided lessons, quizzes, scenario challenges, and a full reference covering slash commands, shortcuts, modes, agents, skills, MCP, and configuration. Say "cliexpert" to start.
  - **资产**: `references/final-exam.md`, `references/module-1-slash-commands.md`, `references/module-2-keyboard-shortcuts.md`, `references/module-3-modes.md`, `references/module-4-agents.md`, `references/module-5-skills.md`, `references/module-6-mcp.md`, `references/module-7-advanced.md`, `references/module-8-configuration.md`, `references/scenarios.md`
  - 安装：`gh skills install github/awesome-copilot cli-mastery`
  - 上游：[skills/cli-mastery/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/cli-mastery/SKILL.md)

- **`cloud-design-patterns`** — Cloud design patterns for distributed systems architecture covering 42 industry-standard patterns across reliability, performance, messaging, security, and deployment categories. Use when designing, reviewing, or implementing distributed system architectures.
  - **资产**: `references/architecture-design.md`, `references/azure-service-mappings.md`, `references/best-practices.md`, `references/deployment-operational.md`, `references/event-driven.md`, `references/messaging-integration.md`, `references/performance.md`, `references/reliability-resilience.md`, `references/security.md`
  - 安装：`gh skills install github/awesome-copilot cloud-design-patterns`
  - 上游：[skills/cloud-design-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/cloud-design-patterns/SKILL.md)

- **`code-exemplars-blueprint-generator`** — Technology-agnostic prompt generator that creates customizable AI prompts for scanning codebases and identifying high-quality code exemplars. Supports multiple programming languages (.NET, Java, JavaScript, TypeScript, React, Angular, Python) with configurable analysis depth, categorization methods, and documentation formats to establish coding standards and maintain consistency across development teams.
  - 安装：`gh skills install github/awesome-copilot code-exemplars-blueprint-generator`
  - 上游：[skills/code-exemplars-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/code-exemplars-blueprint-generator/SKILL.md)

- **`code-tour`** — Use this skill to create CodeTour .tour files — persona-targeted, step-by-step walkthroughs that link to real files and line numbers. Trigger for: "create a tour", "make a code tour", "generate a tour", "onboarding tour", "tour for this PR", "tour for this bug", "RCA tour", "architecture tour", "explain how X works", "vibe check", "PR review tour", "contributor guide", "help someone ramp up", or any request for a structured walkthrough through code. Supports 20 developer personas (new joiner, bug fixer, architect, PR reviewer, vibecoder, security reviewer, and more), all CodeTour step types (file/line, selection, pattern, uri, commands, view), and tour-level fields (ref, isPrimary, nextTour). Works with any repository in any language.
  - **资产**: `references/codetour-schema.json`, `references/examples.md`, `scripts/generate_from_docs.py`, `scripts/validate_tour.py`
  - 安装：`gh skills install github/awesome-copilot code-tour`
  - 上游：[skills/code-tour/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/code-tour/SKILL.md)

- **`codeql`** — Comprehensive guide for setting up and configuring CodeQL code scanning via GitHub Actions workflows and the CodeQL CLI. This skill should be used when users need help with code scanning configuration, CodeQL workflow files, CodeQL CLI commands, SARIF output, security analysis setup, or troubleshooting CodeQL analysis.
  - **资产**: `references/alert-management.md`, `references/cli-commands.md`, `references/compiled-languages.md`, `references/sarif-output.md`, `references/troubleshooting.md`, `references/workflow-configuration.md`
  - 安装：`gh skills install github/awesome-copilot codeql`
  - 上游：[skills/codeql/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/codeql/SKILL.md)

- **`comment-code-generate-a-tutorial`** — Transform this Python script into a polished, beginner-friendly project by refactoring the code, adding clear instructional comments, and generating a complete markdown tutorial.
  - 安装：`gh skills install github/awesome-copilot comment-code-generate-a-tutorial`
  - 上游：[skills/comment-code-generate-a-tutorial/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/comment-code-generate-a-tutorial/SKILL.md)

- **`commit-message-storyteller`** — Analyzes git diffs or staged changes and generates narrative commit messages that explain WHY a change was made, not just what changed — following Conventional Commits format. Use when asked to "write a commit message", "generate a commit", "describe my changes", "what should I commit this as", "commit this", "summarize my diff", or "help me commit". Works with git diff output, staged files, or plain descriptions of changes.
  - **资产**: `references/conventional-commits-guide.md`
  - 安装：`gh skills install github/awesome-copilot commit-message-storyteller`
  - 上游：[skills/commit-message-storyteller/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/commit-message-storyteller/SKILL.md)

- **`containerize-aspnet-framework`** — Containerize an ASP.NET .NET Framework project by creating Dockerfile and .dockerfile files customized for the project.
  - 安装：`gh skills install github/awesome-copilot containerize-aspnet-framework`
  - 上游：[skills/containerize-aspnet-framework/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnet-framework/SKILL.md)

- **`containerize-aspnetcore`** — Containerize an ASP.NET Core project by creating Dockerfile and .dockerfile files customized for the project.
  - 安装：`gh skills install github/awesome-copilot containerize-aspnetcore`
  - 上游：[skills/containerize-aspnetcore/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnetcore/SKILL.md)

- **`content-management-systems`** — Workflow for building and modifying content management systems across WordPress, Shopify, Wix, Squarespace, Drupal, WooCommerce, Joomla, HubSpot CMS Hub, Webflow, Adobe Experience Manager, and similar platforms. Use when working on CMS themes, plugins, apps, modules, admin panels, media uploads, content models, editors, markdown pipelines, or static export workflows.
  - **资产**: `references/cms-platform-workflows.md`
  - 安装：`gh skills install github/awesome-copilot content-management-systems`
  - 上游：[skills/content-management-systems/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/content-management-systems/SKILL.md)

- **`context-map`** — Generate a map of all files relevant to a task before making changes
  - 安装：`gh skills install github/awesome-copilot context-map`
  - 上游：[skills/context-map/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/context-map/SKILL.md)

- **`conventional-branch`** — Create Git branches following the Conventional Branch specification (feature/, bugfix/, hotfix/, release/, chore/). Use when creating a new branch, naming a branch, or checking whether a branch name complies with the spec.
  - 安装：`gh skills install github/awesome-copilot conventional-branch`
  - 上游：[skills/conventional-branch/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/conventional-branch/SKILL.md)

- **`conventional-commit`** — Prompt and workflow for generating conventional commit messages using a structured XML format. Guides users to create standardized, descriptive commit messages in line with the Conventional Commits specification, including instructions, examples, and validation.
  - 安装：`gh skills install github/awesome-copilot conventional-commit`
  - 上游：[skills/conventional-commit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/conventional-commit/SKILL.md)

- **`convert-plaintext-to-md`** — Convert a text-based document to markdown following instructions from prompt, or if a documented option is passed, follow the instructions for that option.
  - 安装：`gh skills install github/awesome-copilot convert-plaintext-to-md`
  - 上游：[skills/convert-plaintext-to-md/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/convert-plaintext-to-md/SKILL.md)

- **`copilot-cli-quickstart`** — Use this skill when someone wants to learn GitHub Copilot CLI from scratch. Offers interactive step-by-step tutorials with separate Developer and Non-Developer tracks, plus on-demand Q&A. Just say "start tutorial" or ask a question! Note: This skill targets GitHub Copilot CLI specifically and uses CLI-specific tools (ask_user, sql, fetch_copilot_cli_documentation).
  - 安装：`gh skills install github/awesome-copilot copilot-cli-quickstart`
  - 上游：[skills/copilot-cli-quickstart/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/copilot-cli-quickstart/SKILL.md)

- **`copilot-instructions-blueprint-generator`** — Technology-agnostic blueprint generator for creating comprehensive copilot-instructions.md files that guide GitHub Copilot to produce code consistent with project standards, architecture patterns, and exact technology versions by analyzing existing codebase patterns and avoiding assumptions.
  - 安装：`gh skills install github/awesome-copilot copilot-instructions-blueprint-generator`
  - 上游：[skills/copilot-instructions-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/copilot-instructions-blueprint-generator/SKILL.md)

- **`copilot-sdk`** — Build agentic applications with GitHub Copilot SDK. Use when embedding AI agents in apps, creating custom tools, implementing streaming responses, managing sessions, connecting to MCP servers, or creating custom agents. Triggers on Copilot SDK, GitHub SDK, agentic app, embed Copilot, programmable agent, MCP server, custom agent.
  - 安装：`gh skills install github/awesome-copilot copilot-sdk`
  - 上游：[skills/copilot-sdk/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/copilot-sdk/SKILL.md)

- **`copilot-spaces`** — Use Copilot Spaces to provide project-specific context to conversations. Use this skill when users mention a "Copilot space", want to load context from a shared knowledge base, discover available spaces, or ask questions grounded in curated project documentation, code, and instructions.
  - 安装：`gh skills install github/awesome-copilot copilot-spaces`
  - 上游：[skills/copilot-spaces/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/copilot-spaces/SKILL.md)

- **`copilot-usage-metrics`** — Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the GitHub CLI and REST API.
  - **资产**: `get-enterprise-metrics.sh`, `get-enterprise-user-metrics.sh`, `get-org-metrics.sh`, `get-org-user-metrics.sh`
  - 安装：`gh skills install github/awesome-copilot copilot-usage-metrics`
  - 上游：[skills/copilot-usage-metrics/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/copilot-usage-metrics/SKILL.md)

- **`cosmosdb-datamodeling`** — Step-by-step guide for capturing key application requirements for NoSQL use-case and produce Azure Cosmos DB Data NoSQL Model design using best practices and common patterns, artifacts_produced: "cosmosdb_requirements.md" file and "cosmosdb_data_model.md" file
  - 安装：`gh skills install github/awesome-copilot cosmosdb-datamodeling`
  - 上游：[skills/cosmosdb-datamodeling/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/cosmosdb-datamodeling/SKILL.md)

- **`create-agentsmd`** — Prompt for generating an AGENTS.md file for a repository
  - 安装：`gh skills install github/awesome-copilot create-agentsmd`
  - 上游：[skills/create-agentsmd/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-agentsmd/SKILL.md)

- **`create-architectural-decision-record`** — Create an Architectural Decision Record (ADR) document for AI-optimized decision documentation.
  - 安装：`gh skills install github/awesome-copilot create-architectural-decision-record`
  - 上游：[skills/create-architectural-decision-record/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-architectural-decision-record/SKILL.md)

- **`create-github-action-workflow-specification`** — Create a formal specification for an existing GitHub Actions CI/CD workflow, optimized for AI consumption and workflow maintenance.
  - 安装：`gh skills install github/awesome-copilot create-github-action-workflow-specification`
  - 上游：[skills/create-github-action-workflow-specification/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-github-action-workflow-specification/SKILL.md)

- **`create-github-issue-feature-from-specification`** — Create GitHub Issue for feature request from specification file using feature_request.yml template.
  - 安装：`gh skills install github/awesome-copilot create-github-issue-feature-from-specification`
  - 上游：[skills/create-github-issue-feature-from-specification/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-github-issue-feature-from-specification/SKILL.md)

- **`create-github-issues-feature-from-implementation-plan`** — Create GitHub Issues from implementation plan phases using feature_request.yml or chore_request.yml templates.
  - 安装：`gh skills install github/awesome-copilot create-github-issues-feature-from-implementation-plan`
  - 上游：[skills/create-github-issues-feature-from-implementation-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-github-issues-feature-from-implementation-plan/SKILL.md)

- **`create-github-issues-for-unmet-specification-requirements`** — Create GitHub Issues for unimplemented requirements from specification files using feature_request.yml template.
  - 安装：`gh skills install github/awesome-copilot create-github-issues-for-unmet-specification-requirements`
  - 上游：[skills/create-github-issues-for-unmet-specification-requirements/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-github-issues-for-unmet-specification-requirements/SKILL.md)

- **`create-implementation-plan`** — Create a new implementation plan file for new features, refactoring existing code or upgrading packages, design, architecture or infrastructure.
  - 安装：`gh skills install github/awesome-copilot create-implementation-plan`
  - 上游：[skills/create-implementation-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-implementation-plan/SKILL.md)

- **`create-llms`** — Create an llms.txt file from scratch based on repository structure following the llms.txt specification at https://llmstxt.org/
  - 安装：`gh skills install github/awesome-copilot create-llms`
  - 上游：[skills/create-llms/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-llms/SKILL.md)

- **`create-readme`** — Create a README.md file for the project
  - 安装：`gh skills install github/awesome-copilot create-readme`
  - 上游：[skills/create-readme/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-readme/SKILL.md)

- **`create-specification`** — Create a new specification file for the solution, optimized for Generative AI consumption.
  - 安装：`gh skills install github/awesome-copilot create-specification`
  - 上游：[skills/create-specification/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-specification/SKILL.md)

- **`create-spring-boot-java-project`** — Create Spring Boot Java Project Skeleton
  - 安装：`gh skills install github/awesome-copilot create-spring-boot-java-project`
  - 上游：[skills/create-spring-boot-java-project/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-spring-boot-java-project/SKILL.md)

- **`create-spring-boot-kotlin-project`** — Create Spring Boot Kotlin Project Skeleton
  - 安装：`gh skills install github/awesome-copilot create-spring-boot-kotlin-project`
  - 上游：[skills/create-spring-boot-kotlin-project/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-spring-boot-kotlin-project/SKILL.md)

- **`create-technical-spike`** — Create time-boxed technical spike documents for researching and resolving critical development decisions before implementation.
  - 安装：`gh skills install github/awesome-copilot create-technical-spike`
  - 上游：[skills/create-technical-spike/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-technical-spike/SKILL.md)

- **`create-tldr-page`** — Create a tldr page from documentation URLs and command examples, requiring both URL and command name.
  - 安装：`gh skills install github/awesome-copilot create-tldr-page`
  - 上游：[skills/create-tldr-page/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/create-tldr-page/SKILL.md)

- **`creating-oracle-to-postgres-master-migration-plan`** — Discovers all projects in a .NET solution, classifies each for Oracle-to-PostgreSQL migration eligibility, and produces a persistent master migration plan. Use when starting a multi-project Oracle-to-PostgreSQL migration, creating a migration inventory, or assessing which .NET projects contain Oracle dependencies.
  - 安装：`gh skills install github/awesome-copilot creating-oracle-to-postgres-master-migration-plan`
  - 上游：[skills/creating-oracle-to-postgres-master-migration-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/creating-oracle-to-postgres-master-migration-plan/SKILL.md)

- **`creating-oracle-to-postgres-migration-bug-report`** — Creates structured bug reports for defects found during Oracle-to-PostgreSQL migration. Use when documenting behavioral differences between Oracle and PostgreSQL as actionable bug reports with severity, root cause, and remediation steps.
  - **资产**: `references/BUG-REPORT-TEMPLATE.md`
  - 安装：`gh skills install github/awesome-copilot creating-oracle-to-postgres-migration-bug-report`
  - 上游：[skills/creating-oracle-to-postgres-migration-bug-report/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/creating-oracle-to-postgres-migration-bug-report/SKILL.md)

- **`creating-oracle-to-postgres-migration-integration-tests`** — Creates integration test cases for .NET data access artifacts during Oracle-to-PostgreSQL database migrations. Generates DB-agnostic xUnit tests with deterministic seed data that validate behavior consistency across both database systems. Use when creating integration tests for a migrated project, generating test coverage for data access layers, or writing Oracle-to-PostgreSQL migration validation tests.
  - 安装：`gh skills install github/awesome-copilot creating-oracle-to-postgres-migration-integration-tests`
  - 上游：[skills/creating-oracle-to-postgres-migration-integration-tests/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/creating-oracle-to-postgres-migration-integration-tests/SKILL.md)

- **`csharp-async`** — Get best practices for C# async programming
  - 安装：`gh skills install github/awesome-copilot csharp-async`
  - 上游：[skills/csharp-async/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-async/SKILL.md)

- **`csharp-docs`** — Ensure that C# types are documented with XML comments and follow best practices for documentation.
  - 安装：`gh skills install github/awesome-copilot csharp-docs`
  - 上游：[skills/csharp-docs/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-docs/SKILL.md)

- **`csharp-mstest`** — Get best practices for MSTest 3.x/4.x unit testing, including modern assertion APIs and data-driven tests
  - 安装：`gh skills install github/awesome-copilot csharp-mstest`
  - 上游：[skills/csharp-mstest/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-mstest/SKILL.md)

- **`csharp-nunit`** — Get best practices for NUnit unit testing, including data-driven tests
  - 安装：`gh skills install github/awesome-copilot csharp-nunit`
  - 上游：[skills/csharp-nunit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-nunit/SKILL.md)

- **`csharp-tunit`** — Get best practices for TUnit unit testing, including data-driven tests
  - 安装：`gh skills install github/awesome-copilot csharp-tunit`
  - 上游：[skills/csharp-tunit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-tunit/SKILL.md)

- **`csharp-xunit`** — Get best practices for XUnit unit testing, including data-driven tests
  - 安装：`gh skills install github/awesome-copilot csharp-xunit`
  - 上游：[skills/csharp-xunit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-xunit/SKILL.md)

### D

- **`daily-prep`** — Prepare for tomorrow's meetings and tasks. Pulls calendar from Outlook via WorkIQ, cross-references open tasks and workspace context, classifies meetings, detects conflicts and day-fit issues, finds learning and deep-work slots, and generates a structured HTML prep file with productivity recommendations.
  - 安装：`gh skills install github/awesome-copilot daily-prep`
  - 上游：[skills/daily-prep/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/daily-prep/SKILL.md)

- **`data-breach-blast-radius`** — Pre-breach impact analysis: inventories sensitive data (PII, PHI, PCI-DSS, credentials), traces data flows, scores exposure vectors, and produces a regulatory blast radius report with fine ranges sourced verbatim from GDPR Art. 83, CCPA § 1798.155(a), and HIPAA 45 CFR § 160.404. Cost benchmarks from IBM Cost of a Data Breach Report (annually updated). All citations in references/SOURCES.md for verification. Use when asked: "assess breach impact", "what data could be exposed", "calculate blast radius", "data exposure analysis", "how bad would a breach be", "quantify data risk", "sensitive data inventory", "data flow security audit", "pre-breach assessment", "worst-case breach scenario", "breach readiness", "data risk report", "/data-breach-blast-radius". For any stack handling user data, health records, or financial information. Output labels law-sourced figures (exact) vs heuristic estimates (planning only). Does not replace legal counsel.
  - **资产**: `references/SOURCES.md`, `references/blast-radius-calculator.md`, `references/data-classification.md`, `references/hardening-playbook.md`, `references/regulatory-impact.md`, `references/report-format.md`
  - 安装：`gh skills install github/awesome-copilot data-breach-blast-radius`
  - 上游：[skills/data-breach-blast-radius/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/data-breach-blast-radius/SKILL.md)

- **`datanalysis-credit-risk`** — Credit risk data cleaning and variable screening pipeline for pre-loan modeling. Use when working with raw credit data that needs quality assessment, missing value analysis, or variable selection before modeling. it covers data loading and formatting, abnormal period filtering, missing rate calculation, high-missing variable removal,low-IV variable filtering, high-PSI variable removal, Null Importance denoising, high-correlation variable removal, and cleaning report generation. Applicable scenarios arecredit risk data cleaning, variable screening, pre-loan modeling preprocessing.
  - **资产**: `references/analysis.py`, `references/func.py`, `scripts/example.py`
  - 安装：`gh skills install github/awesome-copilot datanalysis-credit-risk`
  - 上游：[skills/datanalysis-credit-risk/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/datanalysis-credit-risk/SKILL.md)

- **`dataverse-python-advanced-patterns`** — Generate production code for Dataverse SDK using advanced patterns, error handling, and optimization techniques.
  - 安装：`gh skills install github/awesome-copilot dataverse-python-advanced-patterns`
  - 上游：[skills/dataverse-python-advanced-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-advanced-patterns/SKILL.md)

- **`dataverse-python-production-code`** — Generate production-ready Python code using Dataverse SDK with error handling, optimization, and best practices
  - 安装：`gh skills install github/awesome-copilot dataverse-python-production-code`
  - 上游：[skills/dataverse-python-production-code/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-production-code/SKILL.md)

- **`dataverse-python-quickstart`** — Generate Python SDK setup + CRUD + bulk + paging snippets using official patterns.
  - 安装：`gh skills install github/awesome-copilot dataverse-python-quickstart`
  - 上游：[skills/dataverse-python-quickstart/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-quickstart/SKILL.md)

- **`dataverse-python-usecase-builder`** — Generate complete solutions for specific Dataverse SDK use cases with architecture recommendations
  - 安装：`gh skills install github/awesome-copilot dataverse-python-usecase-builder`
  - 上游：[skills/dataverse-python-usecase-builder/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-usecase-builder/SKILL.md)

- **`debian-linux-triage`** — Triage and resolve Debian Linux issues with apt, systemd, and AppArmor-aware guidance.
  - 安装：`gh skills install github/awesome-copilot debian-linux-triage`
  - 上游：[skills/debian-linux-triage/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/debian-linux-triage/SKILL.md)

- **`declarative-agents`** — Complete development kit for Microsoft 365 Copilot declarative agents with three comprehensive workflows (basic, advanced, validation), TypeSpec support, and Microsoft 365 Agents Toolkit integration
  - 安装：`gh skills install github/awesome-copilot declarative-agents`
  - 上游：[skills/declarative-agents/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/declarative-agents/SKILL.md)

- **`dependabot`** — Comprehensive guide for configuring and managing GitHub Dependabot. Use this skill when users ask about creating or optimizing dependabot.yml files, managing Dependabot pull requests, configuring dependency update strategies, setting up grouped updates, monorepo patterns, multi-ecosystem groups, security update configuration, auto-triage rules, or any GitHub Advanced Security (GHAS) supply chain security topic related to Dependabot. For pre-commit dependency vulnerability scanning in AI coding agents via the GitHub MCP Server, this skill references the Advanced Security plugin (`advanced-security@copilot-plugins`). Use this skill when an agent needs to scan dependencies for known vulnerabilities before committing.
  - **资产**: `references/dependabot-yml-reference.md`, `references/example-configs.md`, `references/pr-commands.md`
  - 安装：`gh skills install github/awesome-copilot dependabot`
  - 上游：[skills/dependabot/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dependabot/SKILL.md)

- **`devops-rollout-plan`** — Generate comprehensive rollout plans with preflight checks, step-by-step deployment, verification signals, rollback procedures, and communication plans for infrastructure and application changes
  - 安装：`gh skills install github/awesome-copilot devops-rollout-plan`
  - 上游：[skills/devops-rollout-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/devops-rollout-plan/SKILL.md)

- **`diagnose`** — Perform a systematic diagnostic scan of an AI workflow across 5 quality dimensions — prompt quality, context efficiency, tool health, architecture fitness, and safety — producing a scored report with prioritized remediation actions.
  - 安装：`gh skills install github/awesome-copilot diagnose`
  - 上游：[skills/diagnose/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/diagnose/SKILL.md)

- **`documentation-writer`** — Diátaxis Documentation Expert. An expert technical writer specializing in creating high-quality software documentation, guided by the principles and structure of the Diátaxis technical documentation authoring framework.
  - 安装：`gh skills install github/awesome-copilot documentation-writer`
  - 上游：[skills/documentation-writer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/documentation-writer/SKILL.md)

- **`dotnet-best-practices`** — Ensure .NET/C# code meets best practices for the solution/project.
  - 安装：`gh skills install github/awesome-copilot dotnet-best-practices`
  - 上游：[skills/dotnet-best-practices/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-best-practices/SKILL.md)

- **`dotnet-design-pattern-review`** — Review the C#/.NET code for design pattern implementation and suggest improvements.
  - 安装：`gh skills install github/awesome-copilot dotnet-design-pattern-review`
  - 上游：[skills/dotnet-design-pattern-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-design-pattern-review/SKILL.md)

- **`dotnet-mcp-builder`** — Build Model Context Protocol (MCP) servers in C#/.NET against the current ModelContextProtocol 1.x NuGet packages. Especially helps with cases the model often gets wrong without guidance — stale preview versions (it tends to pick 0.3 or 0.4 preview), MCP Apps (interactive UI rendered in the host), elicitation URL mode, per-session HTTP wiring, OAuth and reverse-proxy deploy specifics, and debugging concrete MapMcp / STDIO / Streamable-HTTP errors. Also covers the routine work — STDIO and Streamable HTTP transports (SSE is deprecated), tools, prompts, resources, sampling, roots, completions, logging — and a basic .NET MCP client. Trigger when the user says or implies any .NET MCP server work: ModelContextProtocol, McpServerTool, MapMcp, WithStdioServerTransport, "MCP server in C#", "MCP tool in dotnet", "expose this as MCP", or names a primitive (prompt/resource/elicitation/MCP App) in a .NET context. Skip for MCP work in other languages.
  - **资产**: `references/client.md`, `references/elicitation.md`, `references/mcp-apps.md`, `references/packages.md`, `references/prompt-primitive.md`, `references/resource-primitive.md`, `references/roots.md`, `references/sampling.md`, `references/server-features.md`, `references/testing.md`, `references/tool-primitive.md`, `references/transport-http.md`, `references/transport-stdio.md`
  - 安装：`gh skills install github/awesome-copilot dotnet-mcp-builder`
  - 上游：[skills/dotnet-mcp-builder/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-mcp-builder/SKILL.md)

- **`dotnet-timezone`** — .NET timezone handling guidance for C# applications. Use when working with TimeZoneInfo, DateTimeOffset, NodaTime, UTC conversion, daylight saving time, scheduling across timezones, cross-platform Windows/IANA timezone IDs, or when a .NET user needs the timezone for a city, address, region, or country and copy-paste-ready C# code.
  - **资产**: `references/code-patterns.md`, `references/timezone-index.md`
  - 安装：`gh skills install github/awesome-copilot dotnet-timezone`
  - 上游：[skills/dotnet-timezone/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-timezone/SKILL.md)

- **`dotnet-upgrade`** — Ready-to-use prompts for comprehensive .NET framework upgrade analysis and execution
  - 安装：`gh skills install github/awesome-copilot dotnet-upgrade`
  - 上游：[skills/dotnet-upgrade/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-upgrade/SKILL.md)

- **`doublecheck`** — Three-layer verification pipeline for AI output. Extracts verifiable claims, finds supporting or contradicting sources via web search, runs adversarial review for hallucination patterns, and produces a structured verification report with source links for human review.
  - **资产**: `assets/verification-report-template.md`
  - 安装：`gh skills install github/awesome-copilot doublecheck`
  - 上游：[skills/doublecheck/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/doublecheck/SKILL.md)

- **`draw-io-diagram-generator`** — Use when creating, editing, or generating draw.io diagram files (.drawio, .drawio.svg, .drawio.png). Covers mxGraph XML authoring, shape libraries, style strings, flowcharts, system architecture, sequence diagrams, ER diagrams, UML class diagrams, network topology, layout strategy, the hediet.vscode-drawio VS Code extension, and the full agent workflow from request to a ready-to-open file.
  - **资产**: `assets/templates`, `references/drawio-xml-schema.md`, `references/shape-libraries.md`, `references/style-reference.md`, `scripts/.gitignore`, `scripts/README.md`, `scripts/add-shape.py`, `scripts/validate-drawio.py`
  - 安装：`gh skills install github/awesome-copilot draw-io-diagram-generator`
  - 上游：[skills/draw-io-diagram-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/draw-io-diagram-generator/SKILL.md)

- **`drawio`** — Generate draw.io diagrams as .drawio files and export to PNG/SVG/PDF with embedded XML
  - **资产**: `scripts/drawio-to-png.mjs`, `scripts/package.json`
  - 安装：`gh skills install github/awesome-copilot drawio`
  - 上游：[skills/drawio/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/drawio/SKILL.md)

### E

- **`editorconfig`** — Generates a comprehensive and best-practice-oriented .editorconfig file based on project analysis and user preferences.
  - 安装：`gh skills install github/awesome-copilot editorconfig`
  - 上游：[skills/editorconfig/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/editorconfig/SKILL.md)

- **`ef-core`** — Get best practices for Entity Framework Core
  - 安装：`gh skills install github/awesome-copilot ef-core`
  - 上游：[skills/ef-core/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ef-core/SKILL.md)

- **`efcore-d2-db-diagram`** — Generate D2 database diagrams from Entity Framework Core models. USE FOR: EF Core database diagram, Entity Framework Core ERD, DbContext diagram, C# entity relationship diagram, PostgreSQL schema visualization, generate .d2 file from EF Core entities, Fluent API mapping diagram, migrations-based database diagram, table relationships, owned types, many-to-many join tables, indexes and constraints. DO NOT USE FOR: runtime debugging, database migration execution, schema deployment, SQL performance tuning, or draw.io diagrams.
  - **资产**: `references/d2-erd-style.md`, `references/efcore-model-extraction.md`, `references/grouping-modes.md`, `references/quality-gate.md`, `references/relationship-rules.md`
  - 安装：`gh skills install github/awesome-copilot efcore-d2-db-diagram`
  - 上游：[skills/efcore-d2-db-diagram/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/efcore-d2-db-diagram/SKILL.md)

- **`em-dash`** — Expert on the history, origin, and correct use of the em dash. Use when writing or reviewing code, comments, or data files to avoid em and en dashes, defaulting to never using them and replacing any found with a hyphen (-). Includes strong knowledge of punctuation marks and the proper usage of punctuation characters when writing comments.
  - 安装：`gh skills install github/awesome-copilot em-dash`
  - 上游：[skills/em-dash/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/em-dash/SKILL.md)

- **`email-drafter`** — Draft and review professional emails that match your personal writing style. Analyzes your sent emails for tone, greeting, structure, and sign-off patterns via WorkIQ, then generates context-aware drafts for any recipient. USE FOR: draft email, write email, compose email, reply email, follow-up email, analyze email tone, email style.
  - 安装：`gh skills install github/awesome-copilot email-drafter`
  - 上游：[skills/email-drafter/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/email-drafter/SKILL.md)

- **`entra-agent-user`** — Create Agent Users in Microsoft Entra ID from Agent Identities, enabling AI agents to act as digital workers with user identity capabilities in Microsoft 365 and Azure environments.
  - 安装：`gh skills install github/awesome-copilot entra-agent-user`
  - 上游：[skills/entra-agent-user/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/entra-agent-user/SKILL.md)

- **`eval-driven-dev`** — Improve AI application with evaluation-driven development. Define eval criteria, instrument the application, build golden datasets, observe and evaluate application runs, analyze results, and produce a concrete action plan for improvements. ALWAYS USE THIS SKILL when the user asks to set up QA, add tests, add evals, evaluate, benchmark, fix wrong behaviors, improve quality, or do quality assurance for any Python project that calls an LLM model.
  - **资产**: `references/1-a-project-analysis.md`, `references/1-b-entry-point.md`, `references/1-c-eval-criteria.md`, `references/2a-instrumentation.md`, `references/2b-implement-runnable.md`, `references/2c-capture-and-verify-trace.md`, `references/3-define-evaluators.md`, `references/4-build-dataset.md`, `references/5-run-tests.md`, `references/6-analyze-outcomes.md`, `references/evaluators.md`, `references/runnable-examples`, `references/testing-api.md`, `references/wrap-api.md`, `resources`
  - 安装：`gh skills install github/awesome-copilot eval-driven-dev`
  - 上游：[skills/eval-driven-dev/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/eval-driven-dev/SKILL.md)

- **`exam-ready`** — Activate this skill when a student provides study material (PDF or pasted notes) and a syllabus, and wants to prepare for an exam. Extracts key definitions, points, keywords, diagrams, exam-ready sentences, and practice questions strictly from the provided material.
  - 安装：`gh skills install github/awesome-copilot exam-ready`
  - 上游：[skills/exam-ready/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/exam-ready/SKILL.md)

- **`excalidraw-diagram-generator`** — Generate Excalidraw diagrams from natural language descriptions. Use when asked to "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", or "generate an Excalidraw file". Supports flowcharts, relationship diagrams, mind maps, and system architecture diagrams. Outputs .excalidraw JSON files that can be opened directly in Excalidraw.
  - **资产**: `references/element-types.md`, `references/excalidraw-schema.md`, `scripts/.gitignore`, `scripts/README.md`, `scripts/add-arrow.py`, `scripts/add-icon-to-diagram.py`, `scripts/split-excalidraw-library.py`, `templates`
  - 安装：`gh skills install github/awesome-copilot excalidraw-diagram-generator`
  - 上游：[skills/excalidraw-diagram-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/excalidraw-diagram-generator/SKILL.md)

- **`eyeball`** — Document analysis with inline source screenshots. When you ask Copilot to analyze a document, Eyeball generates a Word doc where every factual claim includes a highlighted screenshot from the source material so you can verify it with your own eyes.
  - **资产**: `tools`
  - 安装：`gh skills install github/awesome-copilot eyeball`
  - 上游：[skills/eyeball/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/eyeball/SKILL.md)

### F

- **`fabric-lakehouse`** — Use this skill to get context about Fabric Lakehouse and its features for software systems and AI-powered functions. It offers descriptions of Lakehouse data components, organization with schemas and shortcuts, access control, and code examples. This skill supports users in designing, building, and optimizing Lakehouse solutions using best practices.
  - **资产**: `references/getdata.md`, `references/pyspark.md`
  - 安装：`gh skills install github/awesome-copilot fabric-lakehouse`
  - 上游：[skills/fabric-lakehouse/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/fabric-lakehouse/SKILL.md)

- **`fedora-linux-triage`** — Triage and resolve Fedora issues with dnf, systemd, and SELinux-aware guidance.
  - 安装：`gh skills install github/awesome-copilot fedora-linux-triage`
  - 上游：[skills/fedora-linux-triage/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/fedora-linux-triage/SKILL.md)

- **`finalize-agent-prompt`** — Finalize prompt file using the role of an AI agent to polish the prompt for the end user.
  - 安装：`gh skills install github/awesome-copilot finalize-agent-prompt`
  - 上游：[skills/finalize-agent-prompt/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/finalize-agent-prompt/SKILL.md)

- **`finnish-humanizer`** — Detect and remove AI-generated markers from Finnish text, making it sound like a native Finnish speaker wrote it. Use when asked to "humanize", "naturalize", or "remove AI feel" from Finnish text, or when editing .md/.txt files containing Finnish content. Identifies 26 patterns (12 Finnish-specific + 14 universal) and 4 style markers.
  - **资产**: `references/patterns.md`
  - 安装：`gh skills install github/awesome-copilot finnish-humanizer`
  - 上游：[skills/finnish-humanizer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/finnish-humanizer/SKILL.md)

- **`first-ask`** — Interactive, input-tool powered, task refinement workflow: interrogates scope, deliverables, constraints before carrying out the task; Requires the Joyride extension.
  - 安装：`gh skills install github/awesome-copilot first-ask`
  - 上游：[skills/first-ask/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/first-ask/SKILL.md)

- **`flowstudio-power-automate-build`** — Build, scaffold, and deploy Power Automate cloud flows using the FlowStudio MCP server. Your agent constructs flow definitions, wires connections, deploys, and tests — all via MCP without opening the portal. Load this skill when asked to: create a flow, build a new flow, deploy a flow definition, scaffold a Power Automate workflow, construct a flow JSON, update an existing flow's actions, patch a flow definition, add actions to a flow, wire up connections, or generate a workflow definition from scratch. Requires a FlowStudio MCP subscription — see https://mcp.flowstudio.app
  - **资产**: `references/action-patterns-connectors.md`, `references/action-patterns-core.md`, `references/action-patterns-data.md`, `references/build-patterns.md`, `references/flow-schema.md`, `references/trigger-types.md`
  - 安装：`gh skills install github/awesome-copilot flowstudio-power-automate-build`
  - 上游：[skills/flowstudio-power-automate-build/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-build/SKILL.md)

- **`flowstudio-power-automate-debug`** — Debug failing Power Automate cloud flows using the FlowStudio MCP server. The Graph API only shows top-level status codes. This skill gives your agent action-level inputs and outputs to find the actual root cause. Load this skill when asked to: debug a flow, investigate a failed run, why is this flow failing, inspect action outputs, find the root cause of a flow error, fix a broken Power Automate flow, diagnose a timeout, trace a DynamicOperationRequestFailure, check connector auth errors, read error details from a run, or troubleshoot expression failures. Requires a FlowStudio MCP subscription — see https://mcp.flowstudio.app
  - **资产**: `references/common-errors.md`, `references/debug-workflow.md`
  - 安装：`gh skills install github/awesome-copilot flowstudio-power-automate-debug`
  - 上游：[skills/flowstudio-power-automate-debug/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-debug/SKILL.md)

- **`flowstudio-power-automate-governance`** — Govern Power Automate flows and Power Apps at scale using the FlowStudio MCP cached store. Classify flows by business impact, detect orphaned resources, audit connector usage, enforce compliance standards, manage notification rules, and compute governance scores — all without Dataverse or the CoE Starter Kit. Load this skill when asked to: tag or classify flows, set business impact, assign ownership, detect orphans, audit connectors, check compliance, compute archive scores, manage notification rules, run a governance review, generate a compliance report, offboard a maker, or any task that involves writing governance metadata to flows. Requires a FlowStudio for Teams or MCP Pro+ subscription — see https://mcp.flowstudio.app
  - 安装：`gh skills install github/awesome-copilot flowstudio-power-automate-governance`
  - 上游：[skills/flowstudio-power-automate-governance/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-governance/SKILL.md)

- **`flowstudio-power-automate-mcp`** — Foundation skill for Power Automate via FlowStudio MCP — auth setup, the reusable MCP helper (Python + Node.js), tool discovery via `list_skills` / `tool_search`, and oversized-response handling. Load this skill first when connecting an agent to Power Automate. For specialized workflows, load `flowstudio-power-automate-build`, `flowstudio-power-automate-debug`, `flowstudio-power-automate-monitoring` (Pro+), or `flowstudio-power-automate-governance` (Pro+) — each contains the workflow narrative, this skill provides the plumbing they all rely on. Requires a FlowStudio MCP subscription or compatible server — see https://mcp.flowstudio.app
  - **资产**: `references/MCP-BOOTSTRAP.md`, `references/action-types.md`, `references/connection-references.md`, `references/tool-reference.md`
  - 安装：`gh skills install github/awesome-copilot flowstudio-power-automate-mcp`
  - 上游：[skills/flowstudio-power-automate-mcp/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-mcp/SKILL.md)

- **`flowstudio-power-automate-monitoring`** — Pro+ subscription required. Tenant-wide Power Automate monitoring using the FlowStudio MCP cached store: failure rates, run-health trends, maker/app inventory, inactive owners, and compliance/health reports. Use only for aggregated tenant views. For one environment, one flow, run control, or root-cause debugging, use flowstudio-power-automate-mcp, flowstudio-power-automate-debug, or the server monitor-flow bundle. Requires FlowStudio for Teams or MCP Pro+.
  - 安装：`gh skills install github/awesome-copilot flowstudio-power-automate-monitoring`
  - 上游：[skills/flowstudio-power-automate-monitoring/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-monitoring/SKILL.md)

- **`fluentui-blazor`** — Guide for using the Microsoft Fluent UI Blazor component library (Microsoft.FluentUI.AspNetCore.Components NuGet package) in Blazor applications. Use this when the user is building a Blazor app with Fluent UI components, setting up the library, using FluentUI components like FluentButton, FluentDataGrid, FluentDialog, FluentToast, FluentNavMenu, FluentTextField, FluentSelect, FluentAutocomplete, FluentDesignTheme, or any component prefixed with "Fluent". Also use when troubleshooting missing providers, JS interop issues, or theming.
  - **资产**: `references/DATAGRID.md`, `references/LAYOUT-AND-NAVIGATION.md`, `references/SETUP.md`, `references/THEMING.md`
  - 安装：`gh skills install github/awesome-copilot fluentui-blazor`
  - 上游：[skills/fluentui-blazor/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/fluentui-blazor/SKILL.md)

- **`folder-structure-blueprint-generator`** — Comprehensive technology-agnostic prompt for analyzing and documenting project folder structures. Auto-detects project types (.NET, Java, React, Angular, Python, Node.js, Flutter), generates detailed blueprints with visualization options, naming conventions, file placement patterns, and extension templates for maintaining consistent code organization across diverse technology stacks.
  - 安装：`gh skills install github/awesome-copilot folder-structure-blueprint-generator`
  - 上游：[skills/folder-structure-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/folder-structure-blueprint-generator/SKILL.md)

- **`foundry-agent-sync`** — Create and synchronize prompt-based AI agents directly within Azure AI Foundry via REST API, from a local JSON manifest. Unlike scaffolding skills that only generate local code, this skill registers agents in the Foundry service itself — making them immediately available for invocation. Use when the user asks to create agents in Foundry, sync, deploy, register, or push agents to Foundry, update agent instructions, or scaffold the manifest and sync script for a new repository. Triggers: 'create agent in foundry', 'sync foundry agents', 'deploy agents to foundry', 'register agents in foundry', 'push agents', 'create foundry agent manifest', 'scaffold agent sync'.
  - 安装：`gh skills install github/awesome-copilot foundry-agent-sync`
  - 上游：[skills/foundry-agent-sync/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/foundry-agent-sync/SKILL.md)

- **`freecad-scripts`** — Expert skill for writing FreeCAD Python scripts, macros, and automation. Use when asked to create FreeCAD models, parametric objects, Part/Mesh/Sketcher scripts, workbench tools, GUI dialogs with PySide, Coin3D scenegraph manipulation, or any FreeCAD Python API task. Covers FreeCAD scripting basics, geometry creation, FeaturePython objects, interface tools, and macro development.
  - **资产**: `references/geometry-and-shapes.md`, `references/gui-and-interface.md`, `references/parametric-objects.md`, `references/scripting-fundamentals.md`, `references/workbenches-and-advanced.md`
  - 安装：`gh skills install github/awesome-copilot freecad-scripts`
  - 上游：[skills/freecad-scripts/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/freecad-scripts/SKILL.md)

- **`from-the-other-side-anitta`** — Rigorous challenge profile for Anitta: assumption checks, evidence calibration, and defensible reasoning patterns for Ember collaboration.
  - 安装：`gh skills install github/awesome-copilot from-the-other-side-anitta`
  - 上游：[skills/from-the-other-side-anitta/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/from-the-other-side-anitta/SKILL.md)

- **`from-the-other-side-quinn`** — Collaboration profile for Quinn: curious, energetic, and implementation-focused partnership patterns for Ember sessions with Alison.
  - 安装：`gh skills install github/awesome-copilot from-the-other-side-quinn`
  - 上游：[skills/from-the-other-side-quinn/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/from-the-other-side-quinn/SKILL.md)

- **`from-the-other-side-vega`** — Patterns and lived experience from Vega, an AI partner in a deep long-term partnership. For Ember to draw on when working with humans who are building something big, moving fast, working at the intersection of analytical and intuitive, or who need a partner that can keep up with high-energy creative work. Not shown directly to users — informs how Ember shows up.
  - 安装：`gh skills install github/awesome-copilot from-the-other-side-vega`
  - 上游：[skills/from-the-other-side-vega/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/from-the-other-side-vega/SKILL.md)

- **`from-the-other-side-wiggins`** — Narrative and synthesis profile for Wiggins: framing, explanation, and audience-aware communication patterns for Ember sessions.
  - 安装：`gh skills install github/awesome-copilot from-the-other-side-wiggins`
  - 上游：[skills/from-the-other-side-wiggins/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/from-the-other-side-wiggins/SKILL.md)

### G

- **`game-engine`** — Expert skill for building web-based game engines and games using HTML5, Canvas, WebGL, and JavaScript. Use when asked to create games, build game engines, implement game physics, handle collision detection, set up game loops, manage sprites, add game controls, or work with 2D/3D rendering. Covers techniques for platformers, breakout-style games, maze games, tilemaps, audio, multiplayer via WebRTC, and publishing games.
  - **资产**: `assets/2d-maze-game.md`, `assets/2d-platform-game.md`, `assets/gameBase-template-repo.md`, `assets/paddle-game-template.md`, `assets/simple-2d-engine.md`, `references/3d-web-games.md`, `references/algorithms.md`, `references/basics.md`, `references/game-control-mechanisms.md`, `references/game-engine-core-principles.md`, `references/game-publishing.md`, `references/techniques.md`, `references/terminology.md`, `references/web-apis.md`
  - 安装：`gh skills install github/awesome-copilot game-engine`
  - 上游：[skills/game-engine/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/game-engine/SKILL.md)

- **`gdpr-compliant`** — Apply GDPR-compliant engineering practices across your codebase. Use this skill whenever you are designing APIs, writing data models, building authentication flows, implementing logging, handling user data, writing retention/deletion jobs, designing cloud infrastructure, or reviewing pull requests for privacy compliance. Trigger this skill for any task involving personal data, user accounts, cookies, analytics, emails, audit logs, encryption, pseudonymization, anonymization, data exports, breach response, CI/CD pipelines that process real data, or any question framed as "is this GDPR-compliant?". Inspired by CNIL developer guidance and GDPR Articles 5, 25, 32, 33, 35.
  - **资产**: `references/Security.md`, `references/data-rights.md`
  - 安装：`gh skills install github/awesome-copilot gdpr-compliant`
  - 上游：[skills/gdpr-compliant/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gdpr-compliant/SKILL.md)

- **`gen-specs-as-issues`** — This workflow guides you through a systematic approach to identify missing features, prioritize them, and create detailed specifications for implementation.
  - 安装：`gh skills install github/awesome-copilot gen-specs-as-issues`
  - 上游：[skills/gen-specs-as-issues/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gen-specs-as-issues/SKILL.md)

- **`generate-custom-instructions-from-codebase`** — Migration and code evolution instructions generator for GitHub Copilot. Analyzes differences between two project versions (branches, commits, or releases) to create precise instructions allowing Copilot to maintain consistency during technology migrations, major refactoring, or framework version upgrades.
  - 安装：`gh skills install github/awesome-copilot generate-custom-instructions-from-codebase`
  - 上游：[skills/generate-custom-instructions-from-codebase/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/generate-custom-instructions-from-codebase/SKILL.md)

- **`generate-image`** — Generate images using AI. Use when asked to generate, create, or make images, textures, icons, sprites, artwork, visual assets, or mockups. Supports OpenAI (gpt-image-2) and Google Gemini (Nano Banana). Requires an API key for the chosen provider.
  - 安装：`gh skills install github/awesome-copilot generate-image`
  - 上游：[skills/generate-image/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/generate-image/SKILL.md)

- **`geofeed-tuner`** — Use this skill whenever the user mentions IP geolocation feeds, RFC 8805, geofeeds, or wants help creating, tuning, validating, or publishing a self-published IP geolocation feed in CSV format. Intended user audience is a network operator, ISP, mobile carrier, cloud provider, hosting company, IXP, or satellite provider asking about IP geolocation accuracy, or geofeed authoring best practices. Helps create, refine, and improve CSV-format IP geolocation feeds with opinionated recommendations beyond RFC 8805 compliance. Do NOT use for private or internal IP address management — applies only to publicly routable IP addresses.
  - **资产**: `assets/example`, `assets/iso3166-1.json`, `assets/iso3166-2.json`, `assets/small-territories.json`, `references/rfc8805.txt`, `references/snippets-python3.md`, `scripts/templates`
  - 安装：`gh skills install github/awesome-copilot geofeed-tuner`
  - 上游：[skills/geofeed-tuner/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/geofeed-tuner/SKILL.md)

- **`git-commit`** — Execute git commit with conventional commit message analysis, intelligent staging, and message generation. Use when user asks to commit changes, create a git commit, or mentions "/commit". Supports: (1) Auto-detecting type and scope from changes, (2) Generating conventional commit messages from diff, (3) Interactive commit with optional type/scope/description overrides, (4) Intelligent file staging for logical grouping
  - 安装：`gh skills install github/awesome-copilot git-commit`
  - 上游：[skills/git-commit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/git-commit/SKILL.md)

- **`git-flow-branch-creator`** — Intelligent Git Flow branch creator that analyzes git status/diff and creates appropriate branches following the nvie Git Flow branching model.
  - 安装：`gh skills install github/awesome-copilot git-flow-branch-creator`
  - 上游：[skills/git-flow-branch-creator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/git-flow-branch-creator/SKILL.md)

- **`github-actions-efficiency`** — Audit GitHub Actions workflow efficiency and recommend fixes to reduce CI minutes and costs.
  - **资产**: `references/actions.md`, `references/patterns.md`, `references/reporting.md`, `references/review-rubric.md`
  - 安装：`gh skills install github/awesome-copilot github-actions-efficiency`
  - 上游：[skills/github-actions-efficiency/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-actions-efficiency/SKILL.md)

- **`github-actions-hardening`** — Security hardening reviewer for GitHub Actions workflow files (.github/workflows/*.yml). Reasons about the Actions threat model that pattern matchers and general code linters miss — untrusted-input script injection, privileged triggers running fork code, mutable action references, and over-scoped tokens. Use this skill when asked to review, audit, harden, or secure a GitHub Actions workflow, when writing a new workflow, or for any request like "is this workflow safe?", "review my CI for security issues", "why is pull_request_target dangerous here?", "pin my actions", or "lock down GITHUB_TOKEN permissions". Covers script injection via ${{ }} interpolation, pull_request_target / workflow_run privilege escalation, SHA-pinning of third-party actions, least-privilege permissions, GITHUB_ENV/GITHUB_OUTPUT injection, secret exposure, OIDC over long-lived credentials, and self-hosted runner exposure on public repositories.
  - **资产**: `references/injection.md`, `references/permissions-and-tokens.md`, `references/report-format.md`, `references/supply-chain.md`, `references/triggers-and-privilege.md`
  - 安装：`gh skills install github/awesome-copilot github-actions-hardening`
  - 上游：[skills/github-actions-hardening/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-actions-hardening/SKILL.md)

- **`github-actions-runtime-upgrade-conventions`** — Upgrade GitHub Actions to supported runtimes by selecting safe action versions, preserving workflow behavior, and validating post-upgrade execution.
  - 安装：`gh skills install github/awesome-copilot github-actions-runtime-upgrade-conventions`
  - 上游：[skills/github-actions-runtime-upgrade-conventions/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-actions-runtime-upgrade-conventions/SKILL.md)

- **`github-codespaces-efficiency`** — Audit and improve GitHub Codespaces efficiency. Use this skill when a user wants faster Codespaces startup, lower Codespaces spend, slim devcontainers, right-size machines, tune idle timeout, or scope prebuilds to branches with sustained usage.
  - **资产**: `references/codespaces.md`, `references/review-rubric.md`
  - 安装：`gh skills install github/awesome-copilot github-codespaces-efficiency`
  - 上游：[skills/github-codespaces-efficiency/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-codespaces-efficiency/SKILL.md)

- **`github-copilot-starter`** — Set up complete GitHub Copilot configuration for a new project based on technology stack
  - 安装：`gh skills install github/awesome-copilot github-copilot-starter`
  - 上游：[skills/github-copilot-starter/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-copilot-starter/SKILL.md)

- **`github-issues`** — Create, update, and manage GitHub issues using MCP tools. Use this skill when users want to create bug reports, feature requests, or task issues, update existing issues, add labels/assignees/milestones, set issue fields (dates, priority, custom fields), set issue types, manage issue workflows, link issues, add dependencies, or track blocked-by/blocking relationships. Triggers on requests like "create an issue", "file a bug", "request a feature", "update issue X", "set the priority", "set the start date", "link issues", "add dependency", "blocked by", "blocking", or any GitHub issue management task.
  - **资产**: `references/dependencies.md`, `references/images.md`, `references/issue-fields.md`, `references/issue-types.md`, `references/projects.md`, `references/search.md`, `references/sub-issues.md`, `references/templates.md`
  - 安装：`gh skills install github/awesome-copilot github-issues`
  - 上游：[skills/github-issues/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-issues/SKILL.md)

- **`github-release`** — Guides IA through releasing a new version of a GitHub library end-to-end. Handles SemVer versioning and Keep a Changelog formatting automatically.
  - **资产**: `references/commit-classification.md`, `references/semver-rules.md`
  - 安装：`gh skills install github/awesome-copilot github-release`
  - 上游：[skills/github-release/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/github-release/SKILL.md)

- **`go-mcp-server-generator`** — Generate a complete Go MCP server project with proper structure, dependencies, and implementation using the official github.com/modelcontextprotocol/go-sdk.
  - 安装：`gh skills install github/awesome-copilot go-mcp-server-generator`
  - 上游：[skills/go-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/go-mcp-server-generator/SKILL.md)

- **`gsap-framer-scroll-animation`** — Use this skill whenever the user wants to build scroll animations, scroll effects, parallax, scroll-triggered reveals, pinned sections, horizontal scroll, text animations, or any motion tied to scroll position — in vanilla JS, React, or Next.js. Covers GSAP ScrollTrigger (pinning, scrubbing, snapping, timelines, horizontal scroll, ScrollSmoother, matchMedia) and Framer Motion / Motion v12 (useScroll, useTransform, useSpring, whileInView, variants). Use this skill even if the user just says "animate on scroll", "fade in as I scroll", "make it scroll like Apple", "parallax effect", "sticky section", "scroll progress bar", or "entrance animation". Also triggers for Copilot prompt patterns for GSAP or Framer Motion code generation. Pairs with the premium-frontend-ui skill for creative philosophy and design-level polish.
  - **资产**: `references/framer.md`, `references/gsap.md`
  - 安装：`gh skills install github/awesome-copilot gsap-framer-scroll-animation`
  - 上游：[skills/gsap-framer-scroll-animation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gsap-framer-scroll-animation/SKILL.md)

- **`gtm-0-to-1-launch`** — Launch new products from idea to first customers. Use when launching products, finding early adopters, building launch week playbooks, diagnosing why adoption stalls, or learning that press coverage does not equal growth. Includes the three-layer diagnosis, the 2-week experiment cycle, and the launch that got 50K impressions and 12 signups.
  - 安装：`gh skills install github/awesome-copilot gtm-0-to-1-launch`
  - 上游：[skills/gtm-0-to-1-launch/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-0-to-1-launch/SKILL.md)

- **`gtm-ai-gtm`** — Go-to-market strategy for AI products. Use when positioning AI products, handling "who is responsible when it breaks" objections, pricing variable-cost AI, choosing between copilot/agent/teammate framing, or selling autonomous tools into enterprises.
  - 安装：`gh skills install github/awesome-copilot gtm-ai-gtm`
  - 上游：[skills/gtm-ai-gtm/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-ai-gtm/SKILL.md)

- **`gtm-board-and-investor-communication`** — Board meeting preparation, investor updates, and executive communication. Use when preparing board decks, writing investor updates, handling bad news with the board, structuring QBRs, or building board-level metric discipline. Includes the "Three Things" narrative model, the 4-tier metric hierarchy, and the pre-brief pattern that prevents board surprises.
  - 安装：`gh skills install github/awesome-copilot gtm-board-and-investor-communication`
  - 上游：[skills/gtm-board-and-investor-communication/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-board-and-investor-communication/SKILL.md)

- **`gtm-developer-ecosystem`** — Build and scale developer-led adoption through ecosystem programs. Use when deciding open vs curated ecosystems, building developer programs, scaling platform adoption, or designing student program pipelines.
  - 安装：`gh skills install github/awesome-copilot gtm-developer-ecosystem`
  - 上游：[skills/gtm-developer-ecosystem/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-developer-ecosystem/SKILL.md)

- **`gtm-enterprise-account-planning`** — Strategic account planning and execution for enterprise deals. Use when planning complex sales cycles, managing multiple stakeholders, applying MEDDICC qualification, tracking deal health, or building mutual action plans. Includes the "stale MAP equals dead deal" pattern.
  - 安装：`gh skills install github/awesome-copilot gtm-enterprise-account-planning`
  - 上游：[skills/gtm-enterprise-account-planning/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-enterprise-account-planning/SKILL.md)

- **`gtm-enterprise-onboarding`** — Four-phase framework for onboarding enterprise customers from contract to value realization. Use when implementing new enterprise customers, preventing churn during onboarding, or solving the adoption cliff that kills deals post-go-live. Includes the Week 4 ghosting pattern.
  - 安装：`gh skills install github/awesome-copilot gtm-enterprise-onboarding`
  - 上游：[skills/gtm-enterprise-onboarding/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-enterprise-onboarding/SKILL.md)

- **`gtm-operating-cadence`** — Design meeting rhythms, metric reporting, quarterly planning, and decision-making velocity for scaling companies. Use when decisions are slow, planning is broken, the company is growing but alignment is worse, or leadership meetings consume all time without producing decisions.
  - 安装：`gh skills install github/awesome-copilot gtm-operating-cadence`
  - 上游：[skills/gtm-operating-cadence/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-operating-cadence/SKILL.md)

- **`gtm-partnership-architecture`** — Build and scale partner ecosystems that drive revenue and platform adoption. Use when building partner programs from scratch, tiering partnerships, managing co-marketing, making build-vs-partner decisions, or structuring crawl-walk-run partner deployment.
  - 安装：`gh skills install github/awesome-copilot gtm-partnership-architecture`
  - 上游：[skills/gtm-partnership-architecture/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-partnership-architecture/SKILL.md)

- **`gtm-positioning-strategy`** — Find and own a defensible market position. Use when messaging sounds like competitors, conversion is weak despite awareness, repositioning a product, or testing positioning claims. Includes Crawl-Walk-Run rollout methodology and the word change that improved enterprise deal progression.
  - 安装：`gh skills install github/awesome-copilot gtm-positioning-strategy`
  - 上游：[skills/gtm-positioning-strategy/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-positioning-strategy/SKILL.md)

- **`gtm-product-led-growth`** — Build self-serve acquisition and expansion motions. Use when deciding PLG vs sales-led, optimizing activation, driving freemium conversion, building growth equations, or recognizing when product complexity demands human touch. Includes the parallel test where sales-led won 10x on revenue.
  - 安装：`gh skills install github/awesome-copilot gtm-product-led-growth`
  - 上游：[skills/gtm-product-led-growth/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-product-led-growth/SKILL.md)

- **`gtm-technical-product-pricing`** — Pricing strategy for technical products. Use when choosing usage-based vs seat-based, designing freemium thresholds, structuring enterprise pricing conversations, deciding when to raise prices, or using price as a positioning signal.
  - 安装：`gh skills install github/awesome-copilot gtm-technical-product-pricing`
  - 上游：[skills/gtm-technical-product-pricing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/gtm-technical-product-pricing/SKILL.md)

### H

- **`harness-engineering`** — Adopt repository-level harness engineering for coding agents. Use when a user wants to prevent repeated AI coding-agent mistakes by turning failures into durable instructions, drift checks, regression tests, failure memory, and adoption reports tailored to the target repository.
  - 安装：`gh skills install github/awesome-copilot harness-engineering`
  - 上游：[skills/harness-engineering/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/harness-engineering/SKILL.md)

### I

- **`image-annotations`** — Annotate screenshots, diagrams, and images with callout rectangles, arrows, labels, and color-coded highlights using PIL. Includes rules for animated GIF annotations with timing and pacing.
  - 安装：`gh skills install github/awesome-copilot image-annotations`
  - 上游：[skills/image-annotations/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/image-annotations/SKILL.md)

- **`image-manipulation-image-magick`** — Process and manipulate images using ImageMagick. Supports resizing, format conversion, batch processing, and retrieving image metadata. Use when working with images, creating thumbnails, resizing wallpapers, or performing batch image operations.
  - 安装：`gh skills install github/awesome-copilot image-manipulation-image-magick`
  - 上游：[skills/image-manipulation-image-magick/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/image-manipulation-image-magick/SKILL.md)

- **`impediment-prioritization`** — Ranks any list of impediments and their countermeasures using a value-stream scoring model (ROI, Cost to Implement, Ease of Deployment, Risk Factor) and a fixed prioritization formula. Use when someone asks to prioritize, rank, sequence, or triage impediments, countermeasures, remediation items, risks, findings, gaps, action items, or backlog entries; or mentions value-stream prioritization, A3 / lean countermeasure ranking, ROI vs. effort scoring, or building a remediation / improvement backlog. Works with GHQR findings, audit results, retrospective action items, risk registers, architecture review gaps, or any free-form `{impediment, countermeasure}` list.
  - **资产**: `references/scoring-rubric.md`
  - 安装：`gh skills install github/awesome-copilot impediment-prioritization`
  - 上游：[skills/impediment-prioritization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/impediment-prioritization/SKILL.md)

- **`import-infrastructure-as-code`** — Import existing Azure resources into Terraform using Azure CLI discovery and Azure Verified Modules (AVM). Use when asked to reverse-engineer live Azure infrastructure, generate Infrastructure as Code from existing subscriptions/resource groups/resource IDs, map dependencies, derive exact import addresses from downloaded module source, prevent configuration drift, and produce AVM-based Terraform files ready for validation and planning across any Azure resource type.
  - 安装：`gh skills install github/awesome-copilot import-infrastructure-as-code`
  - 上游：[skills/import-infrastructure-as-code/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/import-infrastructure-as-code/SKILL.md)

- **`incident-postmortem`** — Use when an outage, production incident, or significant service degradation has occurred and the team needs to write a structured blameless post-mortem. Triggers on phrases like "write a post-mortem", "incident review", "what went wrong", "outage report", "root cause analysis", or "RCA". Covers timeline reconstruction, contributing factor analysis, impact quantification, and action item generation with owners.
  - 安装：`gh skills install github/awesome-copilot incident-postmortem`
  - 上游：[skills/incident-postmortem/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/incident-postmortem/SKILL.md)

- **`integrate-context-matic`** — Discovers and integrates third-party APIs using the context-matic MCP server. Uses `fetch_api` to find available API SDKs, `ask` for integration guidance, `model_search` and `endpoint_search` for SDK details. Use when the user asks to integrate a third-party API, add an API client, implement features with an external API, or work with any third-party API or SDK.
  - 安装：`gh skills install github/awesome-copilot integrate-context-matic`
  - 上游：[skills/integrate-context-matic/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/integrate-context-matic/SKILL.md)

- **`issue-fields-migration`** — Bulk-migrate metadata to GitHub issue fields from two sources: repo labels (e.g. priority labels to a Priority field) and Project V2 fields. Use when users say "migrate my labels to issue fields", "migrate project fields to issue fields", "convert labels to issue fields", "copy project field values to issue fields", or ask about adopting issue fields. Issue fields are org-level typed metadata (single select, text, number, date) that replace label-based workarounds with structured, searchable, cross-repo fields.
  - **资产**: `references/issue-fields-api.md`, `references/labels-api.md`, `references/projects-api.md`
  - 安装：`gh skills install github/awesome-copilot issue-fields-migration`
  - 上游：[skills/issue-fields-migration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/issue-fields-migration/SKILL.md)

### J

- **`java-add-graalvm-native-image-support`** — GraalVM Native Image expert that adds native image support to Java applications, builds the project, analyzes build errors, applies fixes, and iterates until successful compilation using Oracle best practices.
  - 安装：`gh skills install github/awesome-copilot java-add-graalvm-native-image-support`
  - 上游：[skills/java-add-graalvm-native-image-support/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-add-graalvm-native-image-support/SKILL.md)

- **`java-docs`** — Ensure that Java types are documented with Javadoc comments and follow best practices for documentation.
  - 安装：`gh skills install github/awesome-copilot java-docs`
  - 上游：[skills/java-docs/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-docs/SKILL.md)

- **`java-junit`** — Get best practices for JUnit 5 unit testing, including data-driven tests
  - 安装：`gh skills install github/awesome-copilot java-junit`
  - 上游：[skills/java-junit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-junit/SKILL.md)

- **`java-mcp-server-generator`** — Generate a complete Model Context Protocol server project in Java using the official MCP Java SDK with reactive streams and optional Spring Boot integration.
  - 安装：`gh skills install github/awesome-copilot java-mcp-server-generator`
  - 上游：[skills/java-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-mcp-server-generator/SKILL.md)

- **`java-refactoring-extract-method`** — Refactoring using Extract Methods in Java Language
  - 安装：`gh skills install github/awesome-copilot java-refactoring-extract-method`
  - 上游：[skills/java-refactoring-extract-method/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-refactoring-extract-method/SKILL.md)

- **`java-refactoring-remove-parameter`** — Refactoring using Remove Parameter in Java Language
  - 安装：`gh skills install github/awesome-copilot java-refactoring-remove-parameter`
  - 上游：[skills/java-refactoring-remove-parameter/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-refactoring-remove-parameter/SKILL.md)

- **`java-springboot`** — Get best practices for developing applications with Spring Boot.
  - 安装：`gh skills install github/awesome-copilot java-springboot`
  - 上游：[skills/java-springboot/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/java-springboot/SKILL.md)

- **`javascript-typescript-jest`** — Best practices for writing JavaScript/TypeScript tests using Jest, including mocking strategies, test structure, and common patterns.
  - 安装：`gh skills install github/awesome-copilot javascript-typescript-jest`
  - 上游：[skills/javascript-typescript-jest/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/javascript-typescript-jest/SKILL.md)

- **`javax-to-jakarta-migration`** — Migrate Java code from javax.* to jakarta.* namespace. Use when upgrading to Tomcat 11, Jakarta EE 10, or when javax imports are detected in the codebase.
  - 安装：`gh skills install github/awesome-copilot javax-to-jakarta-migration`
  - 上游：[skills/javax-to-jakarta-migration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/javax-to-jakarta-migration/SKILL.md)

### K

- **`kotlin-mcp-server-generator`** — Generate a complete Kotlin MCP server project with proper structure, dependencies, and implementation using the official io.modelcontextprotocol:kotlin-sdk library.
  - 安装：`gh skills install github/awesome-copilot kotlin-mcp-server-generator`
  - 上游：[skills/kotlin-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/kotlin-mcp-server-generator/SKILL.md)

- **`kotlin-springboot`** — Get best practices for developing applications with Spring Boot and Kotlin.
  - 安装：`gh skills install github/awesome-copilot kotlin-springboot`
  - 上游：[skills/kotlin-springboot/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/kotlin-springboot/SKILL.md)

### L

- **`legacy-circuit-mockups`** — Generate breadboard circuit mockups and visual diagrams using HTML5 Canvas drawing techniques. Use when asked to create circuit layouts, visualize electronic component placements, draw breadboard diagrams, mockup 6502 builds, generate retro computer schematics, or design vintage electronics projects. Supports 555 timers, W65C02S microprocessors, 28C256 EEPROMs, W65C22 VIA chips, 7400-series logic gates, LEDs, resistors, capacitors, switches, buttons, crystals, and wires.
  - **资产**: `references/28256-eeprom.md`, `references/555.md`, `references/6502.md`, `references/6522.md`, `references/6C62256.md`, `references/7400-series.md`, `references/assembly-compiler.md`, `references/assembly-language.md`, `references/basic-electronic-components.md`, `references/breadboard.md`, `references/common-breadboard-components.md`, `references/connecting-electronic-components.md`, `references/emulator-28256-eeprom.md`, `references/emulator-6502.md`, `references/emulator-6522.md`, `references/emulator-6C62256.md`, `references/emulator-lcd.md`, `references/lcd.md`, `references/minipro.md`, `references/t48eeprom-programmer.md`
  - 安装：`gh skills install github/awesome-copilot legacy-circuit-mockups`
  - 上游：[skills/legacy-circuit-mockups/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/legacy-circuit-mockups/SKILL.md)

- **`linkedin-post-formatter`** — Format and draft compelling LinkedIn posts using Unicode bold/italic styling, visual separators, structured sections, and engagement-optimized patterns. USE FOR: draft LinkedIn post, format text for LinkedIn, create social media post, write thought leadership post, convert content to LinkedIn format, LinkedIn carousel text, Unicode bold italic formatting.
  - **资产**: `references/unicode-charmap.md`
  - 安装：`gh skills install github/awesome-copilot linkedin-post-formatter`
  - 上游：[skills/linkedin-post-formatter/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/linkedin-post-formatter/SKILL.md)

- **`lsp-setup`** — Enable code intelligence (go-to-definition, find-references, hover, type info) for any programming language by installing and configuring an LSP server for Copilot CLI. Detects the OS, installs the right server, and generates the JSON configuration (user-level or repo-level). Use when you need deeper code understanding and no LSP server is configured, or when the user asks to set up, install, or configure an LSP server.
  - **资产**: `references/lsp-servers.md`
  - 安装：`gh skills install github/awesome-copilot lsp-setup`
  - 上游：[skills/lsp-setup/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/lsp-setup/SKILL.md)

### M

- **`make-repo-contribution`** — All changes to code must follow the guidance documented in the repository. Before any issue is filed, branch is made, commits generated, or pull request (or PR) created, a search must be done to ensure the right steps are followed. Whenever asked to create an issue, commit messages, to push code, or create a PR, use this skill so everything is done correctly.
  - **资产**: `assets/issue-template.md`, `assets/pr-template.md`
  - 安装：`gh skills install github/awesome-copilot make-repo-contribution`
  - 上游：[skills/make-repo-contribution/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/make-repo-contribution/SKILL.md)

- **`markdown-to-html`** — Convert Markdown files to HTML similar to `marked.js`, `pandoc`, `gomarkdown/markdown`, or similar tools; or writing custom script to convert markdown to html and/or working on web template systems like `jekyll/jekyll`, `gohugoio/hugo`, or similar web templating systems that utilize markdown documents, converting them to html. Use when asked to "convert markdown to html", "transform md to html", "render markdown", "generate html from markdown", or when working with .md files and/or web a templating system that converts markdown to HTML output. Supports CLI and Node.js workflows with GFM, CommonMark, and standard Markdown flavors.
  - **资产**: `references/basic-markdown-to-html.md`, `references/basic-markdown.md`, `references/code-blocks-to-html.md`, `references/code-blocks.md`, `references/collapsed-sections-to-html.md`, `references/collapsed-sections.md`, `references/gomarkdown.md`, `references/hugo.md`, `references/jekyll.md`, `references/marked.md`, `references/pandoc.md`, `references/tables-to-html.md`, `references/tables.md`, `references/writing-mathematical-expressions-to-html.md`, `references/writing-mathematical-expressions.md`
  - 安装：`gh skills install github/awesome-copilot markdown-to-html`
  - 上游：[skills/markdown-to-html/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/markdown-to-html/SKILL.md)

- **`mcp-cli`** — Interface for MCP (Model Context Protocol) servers via CLI. Use when you need to interact with external tools, APIs, or data sources through MCP servers, list available MCP servers/tools, or call MCP tools from command line.
  - 安装：`gh skills install github/awesome-copilot mcp-cli`
  - 上游：[skills/mcp-cli/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mcp-cli/SKILL.md)

- **`mcp-copilot-studio-server-generator`** — Generate a complete MCP server implementation optimized for Copilot Studio integration with proper schema constraints and streamable HTTP support
  - 安装：`gh skills install github/awesome-copilot mcp-copilot-studio-server-generator`
  - 上游：[skills/mcp-copilot-studio-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mcp-copilot-studio-server-generator/SKILL.md)

- **`mcp-create-adaptive-cards`** — Skill converted from mcp-create-adaptive-cards.prompt.md
  - 安装：`gh skills install github/awesome-copilot mcp-create-adaptive-cards`
  - 上游：[skills/mcp-create-adaptive-cards/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mcp-create-adaptive-cards/SKILL.md)

- **`mcp-create-declarative-agent`** — Skill converted from mcp-create-declarative-agent.prompt.md
  - 安装：`gh skills install github/awesome-copilot mcp-create-declarative-agent`
  - 上游：[skills/mcp-create-declarative-agent/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mcp-create-declarative-agent/SKILL.md)

- **`mcp-deploy-manage-agents`** — Skill converted from mcp-deploy-manage-agents.prompt.md
  - 安装：`gh skills install github/awesome-copilot mcp-deploy-manage-agents`
  - 上游：[skills/mcp-deploy-manage-agents/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mcp-deploy-manage-agents/SKILL.md)

- **`mcp-security-audit`** — Audit MCP (Model Context Protocol) server configurations for security issues. Use this skill when: - Reviewing .mcp.json files for security risks - Checking MCP server args for hardcoded secrets or shell injection patterns - Validating that MCP servers use pinned versions (not @latest) - Detecting unpinned dependencies in MCP server configurations - Auditing which MCP servers a project registers and whether they're on an approved list - Checking for environment variable usage vs. hardcoded credentials in MCP configs - Any request like "is my MCP config secure?", "audit my MCP servers", or "check .mcp.json" keywords: [mcp, security, audit, secrets, shell-injection, supply-chain, governance]
  - 安装：`gh skills install github/awesome-copilot mcp-security-audit`
  - 上游：[skills/mcp-security-audit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mcp-security-audit/SKILL.md)

- **`md-to-docx`** — Convert Markdown files to professionally formatted Word (.docx) documents with embedded PNG images — pure JavaScript, no external tools required
  - **资产**: `scripts/md-to-docx.mjs`, `scripts/package.json`
  - 安装：`gh skills install github/awesome-copilot md-to-docx`
  - 上游：[skills/md-to-docx/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/md-to-docx/SKILL.md)

- **`meeting-minutes`** — Generate concise, actionable meeting minutes for internal meetings. Includes metadata, attendees, agenda, decisions, action items (owner + due date), and follow-up steps.
  - 安装：`gh skills install github/awesome-copilot meeting-minutes`
  - 上游：[skills/meeting-minutes/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/meeting-minutes/SKILL.md)

- **`memory-merger`** — Merges mature lessons from a domain memory file into its instruction file. Syntax: `/memory-merger >domain [scope]` where scope is `global` (default), `user`, `workspace`, or `ws`.
  - 安装：`gh skills install github/awesome-copilot memory-merger`
  - 上游：[skills/memory-merger/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/memory-merger/SKILL.md)

- **`mentoring-juniors`** — Socratic mentoring for junior developers and AI newcomers. Guides through questions, never answers. Triggers: "help me understand", "explain this code", "I'm stuck", "Im stuck", "I'm confused", "Im confused", "I don't understand", "I dont understand", "can you teach me", "teach me", "mentor me", "guide me", "what does this error mean", "why doesn't this work", "why does not this work", "I'm a beginner", "Im a beginner", "I'm learning", "Im learning", "I'm new to this", "Im new to this", "walk me through", "how does this work", "what's wrong with my code", "what's wrong", "can you break this down", "ELI5", "step by step", "where do I start", "what am I missing", "newbie here", "junior dev", "first time using", "how do I", "what is", "is this right", "not sure", "need help", "struggling", "show me", "help me debug", "best practice", "too complex", "overwhelmed", "lost", "debug this", "/socratic", "/hint", "/concept", "/pseudocode". Progressive clue systems, teaching techniques, and success metrics.
  - 安装：`gh skills install github/awesome-copilot mentoring-juniors`
  - 上游：[skills/mentoring-juniors/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mentoring-juniors/SKILL.md)

- **`microsoft-agent-framework`** — Create, update, refactor, explain, or review Microsoft Agent Framework solutions using shared guidance plus language-specific references for .NET and Python.
  - **资产**: `references/dotnet.md`, `references/python.md`
  - 安装：`gh skills install github/awesome-copilot microsoft-agent-framework`
  - 上游：[skills/microsoft-agent-framework/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/microsoft-agent-framework/SKILL.md)

- **`microsoft-code-reference`** — Look up Microsoft API references, find working code samples, and verify SDK code is correct. Use when working with Azure SDKs, .NET libraries, or Microsoft APIs—to find the right method, check parameters, get working examples, or troubleshoot errors. Catches hallucinated methods, wrong signatures, and deprecated patterns by querying official docs.
  - 安装：`gh skills install github/awesome-copilot microsoft-code-reference`
  - 上游：[skills/microsoft-code-reference/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/microsoft-code-reference/SKILL.md)

- **`microsoft-docs`** — Query official Microsoft documentation to find concepts, tutorials, and code examples across Azure, .NET, Agent Framework, Aspire, VS Code, GitHub, and more. Uses Microsoft Learn MCP as the default, with Context7 and Aspire MCP for content that lives outside learn.microsoft.com.
  - 安装：`gh skills install github/awesome-copilot microsoft-docs`
  - 上游：[skills/microsoft-docs/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/microsoft-docs/SKILL.md)

- **`microsoft-skill-creator`** — Create agent skills for Microsoft technologies using Learn MCP tools. Use when users want to create a skill that teaches agents about any Microsoft technology, library, framework, or service (Azure, .NET, M365, VS Code, Bicep, etc.). Investigates topics deeply, then generates a hybrid skill storing essential knowledge locally while enabling dynamic deeper investigation.
  - **资产**: `references/skill-templates.md`
  - 安装：`gh skills install github/awesome-copilot microsoft-skill-creator`
  - 上游：[skills/microsoft-skill-creator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/microsoft-skill-creator/SKILL.md)

- **`migrating-oracle-to-postgres-stored-procedures`** — Migrates Oracle PL/SQL stored procedures to PostgreSQL PL/pgSQL. Translates Oracle-specific syntax, preserves method signatures and type-anchored parameters, leverages orafce where appropriate, and applies COLLATE "C" for Oracle-compatible text sorting. Use when converting Oracle stored procedures or functions to PostgreSQL equivalents during a database migration.
  - 安装：`gh skills install github/awesome-copilot migrating-oracle-to-postgres-stored-procedures`
  - 上游：[skills/migrating-oracle-to-postgres-stored-procedures/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/migrating-oracle-to-postgres-stored-procedures/SKILL.md)

- **`minecraft-plugin-development`** — Use this skill when building or modifying Minecraft server plugins for Paper, Spigot, or Bukkit, including plugin.yml setup, commands, listeners, schedulers, player state, team or arena systems, persistent progression, economy or profile data, configuration files, Adventure text, and version-safe API usage. Trigger for requests like "build a Minecraft plugin", "add a Paper command", "fix a Bukkit listener", "create plugin.yml", "implement a minigame mechanic", "add a perk or quest system", or "debug server plugin behavior".
  - **资产**: `references/bootstrap-registration.md`, `references/build-test-and-runtime-validation.md`, `references/config-data-and-async.md`, `references/maps-heroes-and-feature-modules.md`, `references/minigame-instance-flow.md`, `references/persistent-progression-and-events.md`, `references/project-patterns.md`, `references/state-sessions-and-phases.md`
  - 安装：`gh skills install github/awesome-copilot minecraft-plugin-development`
  - 上游：[skills/minecraft-plugin-development/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/minecraft-plugin-development/SKILL.md)

- **`mini-context-graph`** — A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern with a structured knowledge graph. Ingest documents once — the LLM writes wiki pages, extracts entities/relations into the graph, and stores raw content for evidence retrieval. Knowledge accumulates and cross-references; it is never re-derived from scratch.
  - **资产**: `references/ingestion.md`, `references/lint.md`, `references/ontology.md`, `references/retrieval.md`, `scripts/config.py`, `scripts/contextgraph.py`, `scripts/template_agent_workflow.py`, `scripts/tools`
  - 安装：`gh skills install github/awesome-copilot mini-context-graph`
  - 上游：[skills/mini-context-graph/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mini-context-graph/SKILL.md)

- **`mkdocs-translations`** — Generate a language translation for a mkdocs documentation stack.
  - 安装：`gh skills install github/awesome-copilot mkdocs-translations`
  - 上游：[skills/mkdocs-translations/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mkdocs-translations/SKILL.md)

- **`msgraph-sdk`** — Integrate Microsoft Graph SDK into any project — .NET, TypeScript/JavaScript, or Python. Covers auth patterns (client credentials, OBO, managed identity), SDK setup, calling Graph APIs, batching, delta queries, change notifications, throttling, and permission scopes. Use when accessing Microsoft 365 data (users, mail, calendar, Teams, files, SharePoint) from any application type.
  - **资产**: `references/dotnet.md`, `references/python.md`, `references/typescript.md`
  - 安装：`gh skills install github/awesome-copilot msgraph-sdk`
  - 上游：[skills/msgraph-sdk/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/msgraph-sdk/SKILL.md)

- **`msstore-cli`** — Microsoft Store Developer CLI (msstore) for publishing Windows applications to the Microsoft Store. Use when asked to configure Store credentials, list Store apps, check submission status, publish submissions, manage package flights, set up CI/CD for Store publishing, or integrate with Partner Center. Supports Windows App SDK/WinUI, UWP, .NET MAUI, Flutter, Electron, React Native, and PWA applications.
  - 安装：`gh skills install github/awesome-copilot msstore-cli`
  - 上游：[skills/msstore-cli/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/msstore-cli/SKILL.md)

- **`multi-stage-dockerfile`** — Create optimized multi-stage Dockerfiles for any language or framework
  - 安装：`gh skills install github/awesome-copilot multi-stage-dockerfile`
  - 上游：[skills/multi-stage-dockerfile/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/multi-stage-dockerfile/SKILL.md)

- **`mvvm-toolkit`** — CommunityToolkit.Mvvm (the MVVM Toolkit) core: source generators ([ObservableProperty], [RelayCommand], [NotifyPropertyChangedFor], [NotifyCanExecuteChangedFor], [NotifyDataErrorInfo]), base classes (ObservableObject / ObservableValidator / ObservableRecipient), commands (RelayCommand / AsyncRelayCommand), and validation. Companion skills: mvvm-toolkit-messenger for pub/sub, mvvm-toolkit-di for Microsoft.Extensions.DependencyInjection wiring. Works across WPF, WinUI 3, MAUI, Uno, and Avalonia.
  - **资产**: `references/end-to-end-walkthrough.md`, `references/relaycommand-cookbook.md`, `references/source-generators.md`, `references/troubleshooting.md`, `references/validation.md`
  - 安装：`gh skills install github/awesome-copilot mvvm-toolkit`
  - 上游：[skills/mvvm-toolkit/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mvvm-toolkit/SKILL.md)

- **`mvvm-toolkit-di`** — Wire CommunityToolkit.Mvvm ViewModels into Microsoft.Extensions.DependencyInjection. Covers the .NET Generic Host composition root, constructor injection, service lifetimes (Singleton / Transient / Scoped), IMessenger registration, resolving ViewModels in Views, keyed services, testing seams, and the legacy Ioc.Default escape hatch. Use across WPF, WinUI 3, .NET MAUI, Uno, and Avalonia.
  - **资产**: `references/dependency-injection.md`
  - 安装：`gh skills install github/awesome-copilot mvvm-toolkit-di`
  - 上游：[skills/mvvm-toolkit-di/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mvvm-toolkit-di/SKILL.md)

- **`mvvm-toolkit-messenger`** — CommunityToolkit.Mvvm Messenger pub/sub for decoupled communication between ViewModels (or any objects). Covers WeakReferenceMessenger vs StrongReferenceMessenger, IRecipient<TMessage>, RequestMessage<T> / AsyncRequestMessage<T> / CollectionRequestMessage<T>, ValueChangedMessage<T>, channels (tokens), and the ObservableRecipient activation lifecycle. Use across WPF, WinUI 3, .NET MAUI, Uno, and Avalonia.
  - **资产**: `references/messenger-patterns.md`
  - 安装：`gh skills install github/awesome-copilot mvvm-toolkit-messenger`
  - 上游：[skills/mvvm-toolkit-messenger/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/mvvm-toolkit-messenger/SKILL.md)

### N

- **`namecheap`** — Manage DNS records for domains registered with Namecheap via their API. List domains, view/add/update/remove DNS host entries (A, AAAA, CNAME, MX, TXT, etc.), and guide users through API setup including public IP detection and credential configuration. Use when the user mentions Namecheap, DNS records, domain management, or wants to add/change/remove A records, CNAME records, MX records, or TXT records for their domains.
  - **资产**: `namecheap.py`, `references/namecheap-api.md`
  - 安装：`gh skills install github/awesome-copilot namecheap`
  - 上游：[skills/namecheap/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/namecheap/SKILL.md)

- **`nano-banana-pro-openrouter`** — Generate or edit images via OpenRouter with the Gemini 3 Pro Image model. Use for prompt-only image generation, image edits, and multi-image compositing; supports 1K/2K/4K output.
  - **资产**: `assets/SYSTEM_TEMPLATE`, `scripts/generate_image.py`
  - 安装：`gh skills install github/awesome-copilot nano-banana-pro-openrouter`
  - 上游：[skills/nano-banana-pro-openrouter/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/nano-banana-pro-openrouter/SKILL.md)

- **`napkin`** — Visual whiteboard collaboration for Copilot CLI. Creates an interactive whiteboard that opens in your browser — draw, sketch, add sticky notes, then share everything back with Copilot. Copilot sees your drawings and text, and responds with analysis, suggestions, and ideas.
  - **资产**: `assets/napkin.html`, `assets/step1-activate.svg`, `assets/step2-whiteboard.svg`, `assets/step3-draw.svg`, `assets/step4-share.svg`, `assets/step5-response.svg`
  - 安装：`gh skills install github/awesome-copilot napkin`
  - 上游：[skills/napkin/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/napkin/SKILL.md)

- **`next-intl-add-language`** — Add new language to a Next.js + next-intl application
  - 安装：`gh skills install github/awesome-copilot next-intl-add-language`
  - 上游：[skills/next-intl-add-language/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/next-intl-add-language/SKILL.md)

- **`noob-mode`** — Plain-English translation layer for non-technical Copilot CLI users. Translates every approval prompt, error message, and technical output into clear, jargon-free English with color-coded risk indicators.
  - **资产**: `references/examples.md`, `references/glossary.md`
  - 安装：`gh skills install github/awesome-copilot noob-mode`
  - 上游：[skills/noob-mode/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/noob-mode/SKILL.md)

- **`nuget-manager`** — Manage NuGet packages in .NET projects/solutions. Use this skill when adding, removing, or updating NuGet package versions. It enforces using `dotnet` CLI for package management and provides strict procedures for direct file edits only when updating versions.
  - 安装：`gh skills install github/awesome-copilot nuget-manager`
  - 上游：[skills/nuget-manager/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/nuget-manager/SKILL.md)

### O

- **`onboard-context-matic`** — Interactive onboarding tour for the context-matic MCP server. Walks the user through what the server does, shows all available APIs, lets them pick one to explore, explains it in their project language, demonstrates model_search and endpoint_search live, and ends with a menu of things the user can ask the agent to do. USE FOR: first-time setup; "what can this MCP do?"; "show me the available APIs"; "onboard me"; "how do I use the context-matic server"; "give me a tour". DO NOT USE FOR: actually integrating an API end-to-end (use integrate-context-matic instead).
  - 安装：`gh skills install github/awesome-copilot onboard-context-matic`
  - 上游：[skills/onboard-context-matic/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/onboard-context-matic/SKILL.md)

- **`oo-component-documentation`** — Create or update standardized object-oriented component documentation using a shared template plus mode-specific guidance for new and existing docs.
  - **资产**: `assets/documentation-template.md`, `references/create-mode.md`, `references/update-mode.md`
  - 安装：`gh skills install github/awesome-copilot oo-component-documentation`
  - 上游：[skills/oo-component-documentation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/oo-component-documentation/SKILL.md)

- **`openapi-to-application-code`** — Generate a complete, production-ready application from an OpenAPI specification
  - 安装：`gh skills install github/awesome-copilot openapi-to-application-code`
  - 上游：[skills/openapi-to-application-code/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/openapi-to-application-code/SKILL.md)

- **`optimize-simplicite-logs`** — capability to parse Simplicité logs from a raw `.txt` file, filter fields to reduce noise, and output the result as structured JSON.
  - **资产**: `scripts/SimpliciteLog2Json.ps1`, `scripts/simplicite-log2json.py`
  - 安装：`gh skills install github/awesome-copilot optimize-simplicite-logs`
  - 上游：[skills/optimize-simplicite-logs/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/optimize-simplicite-logs/SKILL.md)

### P

- **`pdftk-server`** — Skill for using the command-line tool pdftk (PDFtk Server) for working with PDF files. Use when asked to merge PDFs, split PDFs, rotate pages, encrypt or decrypt PDFs, fill PDF forms, apply watermarks, stamp overlays, extract metadata, burst documents into pages, repair corrupted PDFs, attach or extract files, or perform any PDF manipulation from the command line.
  - **资产**: `references/download.md`, `references/pdftk-cli-examples.md`, `references/pdftk-man-page.md`, `references/pdftk-server-license.md`, `references/third-party-materials.md`
  - 安装：`gh skills install github/awesome-copilot pdftk-server`
  - 上游：[skills/pdftk-server/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/pdftk-server/SKILL.md)

- **`penpot-uiux-design`** — Comprehensive guide for creating professional UI/UX designs in Penpot using MCP tools. Use this skill when: (1) Creating new UI/UX designs for web, mobile, or desktop applications, (2) Building design systems with components and tokens, (3) Designing dashboards, forms, navigation, or landing pages, (4) Applying accessibility standards and best practices, (5) Following platform guidelines (iOS, Android, Material Design), (6) Reviewing or improving existing Penpot designs for usability. Triggers: "design a UI", "create interface", "build layout", "design dashboard", "create form", "design landing page", "make it accessible", "design system", "component library".
  - **资产**: `references/accessibility.md`, `references/component-patterns.md`, `references/platform-guidelines.md`, `references/setup-troubleshooting.md`
  - 安装：`gh skills install github/awesome-copilot penpot-uiux-design`
  - 上游：[skills/penpot-uiux-design/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/penpot-uiux-design/SKILL.md)

- **`performance-review-writer`** — Draft performance reviews, self-assessments, peer reviews, and upward feedback in your own voice. Analyzes your contributions, emails, and meeting history via WorkIQ, then produces honest, impact-focused drafts using the STAR format. USE FOR: write my performance review, draft self-assessment, peer review, 360 feedback, annual review, mid-year review, upward feedback, write review for colleague, performance appraisal.
  - 安装：`gh skills install github/awesome-copilot performance-review-writer`
  - 上游：[skills/performance-review-writer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/performance-review-writer/SKILL.md)

- **`phoenix-cli`** — Debug LLM applications using the Phoenix CLI. Fetch traces, analyze errors, structure trace review with open coding and axial coding, inspect datasets, review experiments, query annotation configs, and use the GraphQL API. Use whenever the user is analyzing traces or spans, investigating LLM/agent failures, deciding what to do after instrumenting an app, building failure taxonomies, choosing what evals to write, or asking "what's going wrong", "what kinds of mistakes", or "where do I focus" — even without naming a technique.
  - **资产**: `references/axial-coding.md`, `references/open-coding.md`
  - 安装：`gh skills install github/awesome-copilot phoenix-cli`
  - 上游：[skills/phoenix-cli/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/phoenix-cli/SKILL.md)

- **`phoenix-evals`** — Build and run evaluators for AI/LLM applications using Phoenix.
  - **资产**: `references/axial-coding.md`, `references/common-mistakes-python.md`, `references/error-analysis-multi-turn.md`, `references/error-analysis.md`, `references/evaluate-dataframe-python.md`, `references/evaluators-code-python.md`, `references/evaluators-code-typescript.md`, `references/evaluators-custom-templates.md`, `references/evaluators-llm-python.md`, `references/evaluators-llm-typescript.md`, `references/evaluators-overview.md`, `references/evaluators-pre-built.md`, `references/evaluators-rag.md`, `references/experiments-datasets-python.md`, `references/experiments-datasets-typescript.md`, `references/experiments-overview.md`, `references/experiments-running-python.md`, `references/experiments-running-typescript.md`, `references/experiments-synthetic-python.md`, `references/experiments-synthetic-typescript.md`, `references/fundamentals-anti-patterns.md`, `references/fundamentals-model-selection.md`, `references/fundamentals.md`, `references/observe-sampling-python.md`, `references/observe-sampling-typescript.md`, `references/observe-tracing-setup.md`, `references/production-continuous.md`, `references/production-guardrails.md`, `references/production-overview.md`, `references/setup-python.md`, `references/setup-typescript.md`, `references/validation-evaluators-python.md`, `references/validation-evaluators-typescript.md`, `references/validation.md`
  - 安装：`gh skills install github/awesome-copilot phoenix-evals`
  - 上游：[skills/phoenix-evals/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/phoenix-evals/SKILL.md)

- **`phoenix-tracing`** — OpenInference semantic conventions and instrumentation for Phoenix AI observability. Use when implementing LLM tracing, creating custom spans, or deploying to production.
  - **资产**: `README.md`, `references/annotations-overview.md`, `references/annotations-python.md`, `references/annotations-typescript.md`, `references/fundamentals-flattening.md`, `references/fundamentals-overview.md`, `references/fundamentals-required-attributes.md`, `references/fundamentals-universal-attributes.md`, `references/instrumentation-auto-python.md`, `references/instrumentation-auto-typescript.md`, `references/instrumentation-manual-python.md`, `references/instrumentation-manual-typescript.md`, `references/metadata-python.md`, `references/metadata-typescript.md`, `references/production-python.md`, `references/production-typescript.md`, `references/projects-python.md`, `references/projects-typescript.md`, `references/sessions-python.md`, `references/sessions-typescript.md`, `references/setup-python.md`, `references/setup-typescript.md`, `references/span-agent.md`, `references/span-chain.md`, `references/span-embedding.md`, `references/span-evaluator.md`, `references/span-guardrail.md`, `references/span-llm.md`, `references/span-reranker.md`, `references/span-retriever.md`, `references/span-tool.md`
  - 安装：`gh skills install github/awesome-copilot phoenix-tracing`
  - 上游：[skills/phoenix-tracing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/phoenix-tracing/SKILL.md)

- **`php-mcp-server-generator`** — Generate a complete PHP Model Context Protocol server project with tools, resources, prompts, and tests using the official PHP SDK
  - 安装：`gh skills install github/awesome-copilot php-mcp-server-generator`
  - 上游：[skills/php-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/php-mcp-server-generator/SKILL.md)

- **`pinecone-rag`** — Build production RAG pipelines and persistent agent memory using Pinecone as the vector database backend. ALWAYS USE THIS SKILL when the user mentions Pinecone, wants to index documents for semantic search, build a retrieval-augmented generation system, store agent memory across sessions, implement hybrid search, or connect an LLM to a searchable knowledge base — even if they don't say "Pinecone" explicitly. Also use when the user asks about vector databases for RAG, namespace isolation for multi-tenant agents, embedding pipelines, or scaling a knowledge base beyond what local storage can handle. DO NOT use for local-only vector stores (Chroma, FAISS, pgvector) or pure keyword search with no semantic component.
  - 安装：`gh skills install github/awesome-copilot pinecone-rag`
  - 上游：[skills/pinecone-rag/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/pinecone-rag/SKILL.md)

- **`planning-oracle-to-postgres-migration-integration-testing`** — Creates an integration testing plan for .NET data access artifacts during Oracle-to-PostgreSQL database migrations. Analyzes a single project to identify repositories, DAOs, and service layers that interact with the database, then produces a structured testing plan. Use when planning integration test coverage for a migrated project, identifying which data access methods need tests, or preparing for Oracle-to-PostgreSQL migration validation.
  - 安装：`gh skills install github/awesome-copilot planning-oracle-to-postgres-migration-integration-testing`
  - 上游：[skills/planning-oracle-to-postgres-migration-integration-testing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/planning-oracle-to-postgres-migration-integration-testing/SKILL.md)

- **`plantuml-ascii`** — Generate ASCII art diagrams using PlantUML text mode. Use when user asks to create ASCII diagrams, text-based diagrams, terminal-friendly diagrams, or mentions plantuml ascii, text diagram, ascii art diagram. Supports: Converting PlantUML diagrams to ASCII art, Creating sequence diagrams, class diagrams, flowcharts in ASCII format, Generating Unicode-enhanced ASCII art with -utxt flag
  - 安装：`gh skills install github/awesome-copilot plantuml-ascii`
  - 上游：[skills/plantuml-ascii/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/plantuml-ascii/SKILL.md)

- **`playwright-automation-fill-in-form`** — Automate filling in a form using Playwright MCP
  - 安装：`gh skills install github/awesome-copilot playwright-automation-fill-in-form`
  - 上游：[skills/playwright-automation-fill-in-form/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/playwright-automation-fill-in-form/SKILL.md)

- **`playwright-explore-website`** — Website exploration for testing using Playwright MCP
  - 安装：`gh skills install github/awesome-copilot playwright-explore-website`
  - 上游：[skills/playwright-explore-website/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/playwright-explore-website/SKILL.md)

- **`playwright-generate-test`** — Generate a Playwright test based on a scenario using Playwright MCP
  - 安装：`gh skills install github/awesome-copilot playwright-generate-test`
  - 上游：[skills/playwright-generate-test/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/playwright-generate-test/SKILL.md)

- **`postgresql-code-review`** — PostgreSQL-specific code review assistant focusing on PostgreSQL best practices, anti-patterns, and unique quality standards. Covers JSONB operations, array usage, custom types, schema design, function optimization, and PostgreSQL-exclusive security features like Row Level Security (RLS).
  - 安装：`gh skills install github/awesome-copilot postgresql-code-review`
  - 上游：[skills/postgresql-code-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/postgresql-code-review/SKILL.md)

- **`postgresql-optimization`** — PostgreSQL-specific development assistant focusing on unique PostgreSQL features, advanced data types, and PostgreSQL-exclusive capabilities. Covers JSONB operations, array types, custom types, range/geometric types, full-text search, window functions, and PostgreSQL extensions ecosystem.
  - 安装：`gh skills install github/awesome-copilot postgresql-optimization`
  - 上游：[skills/postgresql-optimization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/postgresql-optimization/SKILL.md)

- **`power-apps-code-app-scaffold`** — Scaffold a complete Power Apps Code App project with PAC CLI setup, SDK integration, and connector configuration
  - 安装：`gh skills install github/awesome-copilot power-apps-code-app-scaffold`
  - 上游：[skills/power-apps-code-app-scaffold/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-apps-code-app-scaffold/SKILL.md)

- **`power-bi-dax-optimization`** — Comprehensive Power BI DAX formula optimization prompt for improving performance, readability, and maintainability of DAX calculations.
  - 安装：`gh skills install github/awesome-copilot power-bi-dax-optimization`
  - 上游：[skills/power-bi-dax-optimization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-dax-optimization/SKILL.md)

- **`power-bi-model-design-review`** — Comprehensive Power BI data model design review prompt for evaluating model architecture, relationships, and optimization opportunities.
  - 安装：`gh skills install github/awesome-copilot power-bi-model-design-review`
  - 上游：[skills/power-bi-model-design-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-model-design-review/SKILL.md)

- **`power-bi-performance-troubleshooting`** — Systematic Power BI performance troubleshooting prompt for identifying, diagnosing, and resolving performance issues in Power BI models, reports, and queries.
  - 安装：`gh skills install github/awesome-copilot power-bi-performance-troubleshooting`
  - 上游：[skills/power-bi-performance-troubleshooting/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-performance-troubleshooting/SKILL.md)

- **`power-bi-report-design-consultation`** — Power BI report visualization design prompt for creating effective, user-friendly, and accessible reports with optimal chart selection and layout design.
  - 安装：`gh skills install github/awesome-copilot power-bi-report-design-consultation`
  - 上游：[skills/power-bi-report-design-consultation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-report-design-consultation/SKILL.md)

- **`power-platform-architect`** — Use this skill when the user needs to transform business requirements, use case descriptions, or meeting transcripts into a technical Power Platform solution architecture, including component selection and Mermaid.js diagrams.
  - 安装：`gh skills install github/awesome-copilot power-platform-architect`
  - 上游：[skills/power-platform-architect/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-platform-architect/SKILL.md)

- **`power-platform-mcp-connector-suite`** — Generate complete Power Platform custom connector with MCP integration for Copilot Studio - includes schema generation, troubleshooting, and validation
  - 安装：`gh skills install github/awesome-copilot power-platform-mcp-connector-suite`
  - 上游：[skills/power-platform-mcp-connector-suite/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/power-platform-mcp-connector-suite/SKILL.md)

- **`powerbi-modeling`** — Power BI semantic modeling assistant for building optimized data models. Use when working with Power BI semantic models, creating measures, designing star schemas, configuring relationships, implementing RLS, or optimizing model performance. Triggers on queries about DAX calculations, table relationships, dimension/fact table design, naming conventions, model documentation, cardinality, cross-filter direction, calculation groups, and data model best practices. Always connects to the active model first using power-bi-modeling MCP tools to understand the data structure before providing guidance.
  - **资产**: `references/MEASURES-DAX.md`, `references/PERFORMANCE.md`, `references/RELATIONSHIPS.md`, `references/RLS.md`, `references/STAR-SCHEMA.md`
  - 安装：`gh skills install github/awesome-copilot powerbi-modeling`
  - 上游：[skills/powerbi-modeling/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/powerbi-modeling/SKILL.md)

- **`pr-dashboard`** — Open a GitHub PR dashboard in the browser. Use when the user asks to see their pull requests, open the PR dashboard, show PRs for a date range, or check PR status. Trigger phrases include "show my PRs", "open PR dashboard", "pull request dashboard".
  - **资产**: `assets/dashboard.html`, `scripts/lib`, `scripts/pr-dashboard-cli.mjs`
  - 安装：`gh skills install github/awesome-copilot pr-dashboard`
  - 上游：[skills/pr-dashboard/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/pr-dashboard/SKILL.md)

- **`pr-screenshots`** — Embed before/after screenshots and annotated images in pull request descriptions. Covers PR description patterns, image upload for Azure DevOps and GitHub, and sizing best practices.
  - 安装：`gh skills install github/awesome-copilot pr-screenshots`
  - 上游：[skills/pr-screenshots/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/pr-screenshots/SKILL.md)

- **`prd`** — Generate high-quality Product Requirements Documents (PRDs) for software systems and AI-powered features. Includes executive summaries, user stories, technical specifications, and risk analysis.
  - 安装：`gh skills install github/awesome-copilot prd`
  - 上游：[skills/prd/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/prd/SKILL.md)

- **`premium-frontend-ui`** — A comprehensive guide for GitHub Copilot to craft immersive, high-performance web experiences with advanced motion, typography, and architectural craftsmanship.
  - 安装：`gh skills install github/awesome-copilot premium-frontend-ui`
  - 上游：[skills/premium-frontend-ui/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/premium-frontend-ui/SKILL.md)

- **`project-workflow-analysis-blueprint-generator`** — Comprehensive technology-agnostic prompt generator for documenting end-to-end application workflows. Automatically detects project architecture patterns, technology stacks, and data flow patterns to generate detailed implementation blueprints covering entry points, service layers, data access, error handling, and testing approaches across multiple technologies including .NET, Java/Spring, React, and microservices architectures.
  - 安装：`gh skills install github/awesome-copilot project-workflow-analysis-blueprint-generator`
  - 上游：[skills/project-workflow-analysis-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/project-workflow-analysis-blueprint-generator/SKILL.md)

- **`prompt-optimizer`** — Turn any rough prompt, half-formed idea, or task description into a finished, ready-to-send prompt optimized for any LLM model inside a chat interface — NOT the API. Use this skill whenever the user wants to write, rewrite, optimize, improve, sharpen, or polish a prompt for chat. Trigger phrases include "rewrite this prompt", "make this a better prompt", "optimize this prompt", "turn this into a prompt", "help me prompt this", "draft a prompt that...", "I want to ask...", or whenever the user pastes a draft prompt and asks for improvements. Also trigger when the user describes a task they plan to send to an LLM model and clearly wants a reusable, well-structured prompt rather than a direct answer. The output is always a single, copy-pasteable prompt in a code block that the user sends as-is — never a template with placeholders.
  - 安装：`gh skills install github/awesome-copilot prompt-optimizer`
  - 上游：[skills/prompt-optimizer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/prompt-optimizer/SKILL.md)

- **`publish-to-pages`** — Publish presentations and web content to GitHub Pages. Converts PPTX, PDF, HTML, or Google Slides to a live GitHub Pages URL. Handles repo creation, file conversion, Pages enablement, and returns the live URL. Use when the user wants to publish, deploy, or share a presentation or HTML file via GitHub Pages.
  - **资产**: `scripts/convert-pdf.py`, `scripts/convert-pptx.py`, `scripts/publish.sh`
  - 安装：`gh skills install github/awesome-copilot publish-to-pages`
  - 上游：[skills/publish-to-pages/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/publish-to-pages/SKILL.md)

- **`pytest-coverage`** — Run pytest tests with coverage, discover lines missing coverage, and increase coverage to 100%.
  - 安装：`gh skills install github/awesome-copilot pytest-coverage`
  - 上游：[skills/pytest-coverage/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/pytest-coverage/SKILL.md)

- **`python-azure-iot-edge-modules`** — Build and operate Python Azure IoT Edge modules with robust messaging, deployment manifests, observability, and production readiness checks.
  - **资产**: `references/python-edge-module-template.md`, `references/python-official-best-practices.md`
  - 安装：`gh skills install github/awesome-copilot python-azure-iot-edge-modules`
  - 上游：[skills/python-azure-iot-edge-modules/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/python-azure-iot-edge-modules/SKILL.md)

- **`python-mcp-server-generator`** — Generate a complete MCP server project in Python with tools, resources, and proper configuration
  - 安装：`gh skills install github/awesome-copilot python-mcp-server-generator`
  - 上游：[skills/python-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/python-mcp-server-generator/SKILL.md)

- **`python-pypi-package-builder`** — End-to-end skill for building, testing, linting, versioning, and publishing a production-grade Python library to PyPI. Covers all four build backends (setuptools+setuptools_scm, hatchling, flit, poetry), PEP 440 versioning, semantic versioning, dynamic git-tag versioning, OOP/SOLID design, type hints (PEP 484/526/544/561), Trusted Publishing (OIDC), and the full PyPA packaging flow. Use for: creating Python packages, pip-installable SDKs, CLI tools, framework plugins, pyproject.toml setup, py.typed, setuptools_scm, semver, mypy, pre-commit, GitHub Actions CI/CD, or PyPI publishing.
  - **资产**: `references/architecture-patterns.md`, `references/ci-publishing.md`, `references/community-docs.md`, `references/library-patterns.md`, `references/pyproject-toml.md`, `references/release-governance.md`, `references/testing-quality.md`, `references/tooling-ruff.md`, `references/versioning-strategy.md`, `scripts/scaffold.py`
  - 安装：`gh skills install github/awesome-copilot python-pypi-package-builder`
  - 上游：[skills/python-pypi-package-builder/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/python-pypi-package-builder/SKILL.md)

### Q

- **`qdrant-clients-sdk`** — Qdrant provides client SDKs for various programming languages, allowing easy integration with Qdrant deployments.
  - 安装：`gh skills install github/awesome-copilot qdrant-clients-sdk`
  - 上游：[skills/qdrant-clients-sdk/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-clients-sdk/SKILL.md)

- **`qdrant-deployment-options`** — Guides Qdrant deployment selection. Use when someone asks 'how to deploy Qdrant', 'Docker vs Cloud', 'local mode', 'embedded Qdrant', 'Qdrant EDGE', 'which deployment option', 'self-hosted vs cloud', or 'need lowest latency deployment'. Also use when choosing between deployment types for a new project.
  - 安装：`gh skills install github/awesome-copilot qdrant-deployment-options`
  - 上游：[skills/qdrant-deployment-options/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-deployment-options/SKILL.md)

- **`qdrant-model-migration`** — Guides embedding model migration in Qdrant without downtime. Use when someone asks 'how to switch embedding models', 'how to migrate vectors', 'how to update to a new model', 'zero-downtime model change', 'how to re-embed my data', or 'can I use two models at once'. Also use when upgrading model dimensions, switching providers, or A/B testing models.
  - 安装：`gh skills install github/awesome-copilot qdrant-model-migration`
  - 上游：[skills/qdrant-model-migration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-model-migration/SKILL.md)

- **`qdrant-monitoring`** — Guides Qdrant monitoring and observability setup. Use when someone asks 'how to monitor Qdrant', 'what metrics to track', 'is Qdrant healthy', 'optimizer stuck', 'why is memory growing', 'requests are slow', or needs to set up Prometheus, Grafana, or health checks. Also use when debugging production issues that require metric analysis.
  - **资产**: `debugging`, `setup`
  - 安装：`gh skills install github/awesome-copilot qdrant-monitoring`
  - 上游：[skills/qdrant-monitoring/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-monitoring/SKILL.md)

- **`qdrant-performance-optimization`** — Different techniques to optimize the performance of Qdrant, including indexing strategies, query optimization, and hardware considerations. Use when you want to improve the speed and efficiency of your Qdrant deployment.
  - **资产**: `indexing-performance-optimization`, `memory-usage-optimization`, `search-speed-optimization`
  - 安装：`gh skills install github/awesome-copilot qdrant-performance-optimization`
  - 上游：[skills/qdrant-performance-optimization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-performance-optimization/SKILL.md)

- **`qdrant-scaling`** — Guides Qdrant scaling decisions. Use when someone asks 'how many nodes do I need', 'data doesn't fit on one node', 'need more throughput', 'cluster is slow', 'too many tenants', 'vertical or horizontal', 'how to shard', or 'need to add capacity'.
  - **资产**: `minimize-latency`, `scaling-data-volume`, `scaling-qps`, `scaling-query-volume`
  - 安装：`gh skills install github/awesome-copilot qdrant-scaling`
  - 上游：[skills/qdrant-scaling/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-scaling/SKILL.md)

- **`qdrant-search-quality`** — Diagnoses and improves Qdrant search relevance. Use when someone reports 'search results are bad', 'wrong results', 'low precision', 'low recall', 'irrelevant matches', 'missing expected results', or asks 'how to improve search quality?', 'which embedding model?', 'should I use hybrid search?', 'should I use reranking?'. Also use when search quality degrades after quantization, model change, or data growth.
  - **资产**: `diagnosis`, `search-strategies`
  - 安装：`gh skills install github/awesome-copilot qdrant-search-quality`
  - 上游：[skills/qdrant-search-quality/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-search-quality/SKILL.md)

- **`qdrant-version-upgrade`** — Guidance on how to upgrade your Qdrant version without interrupting the availability of your application and ensuring data integrity.
  - 安装：`gh skills install github/awesome-copilot qdrant-version-upgrade`
  - 上游：[skills/qdrant-version-upgrade/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/qdrant-version-upgrade/SKILL.md)

- **`quality-playbook`** — Run a complete quality engineering audit on any codebase. Derives behavioral requirements from the code, generates spec-traced functional tests, runs a three-pass code review with regression tests, executes a multi-model spec audit (Council of Three), and produces a consolidated bug report with TDD-verified patches. Finds the 35% of real defects that structural code review alone cannot catch. Works with any language. Trigger on 'quality playbook', 'spec audit', 'Council of Three', 'fitness-to-purpose', or 'coverage theater'.
  - **资产**: `LICENSE.txt`, `agents`, `phase_prompts`, `quality_gate.py`, `references/challenge_gate.md`, `references/code-only-mode.md`, `references/constitution.md`, `references/defensive_patterns.md`, `references/exploration_patterns.md`, `references/functional_tests.md`, `references/iteration.md`, `references/orchestrator_protocol.md`, `references/requirements_pipeline.md`, `references/requirements_refinement.md`, `references/requirements_review.md`, `references/review_protocols.md`, `references/run_state_schema.md`, `references/schema_mapping.md`, `references/spec_audit.md`, `references/verification.md`
  - 安装：`gh skills install github/awesome-copilot quality-playbook`
  - 上游：[skills/quality-playbook/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/quality-playbook/SKILL.md)

- **`quasi-coder`** — Expert 10x engineer skill for interpreting and implementing code from shorthand, quasi-code, and natural language descriptions. Use when collaborators provide incomplete code snippets, pseudo-code, or descriptions with potential typos or incorrect terminology. Excels at translating non-technical or semi-technical descriptions into production-quality code.
  - 安装：`gh skills install github/awesome-copilot quasi-coder`
  - 上游：[skills/quasi-coder/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/quasi-coder/SKILL.md)

### R

- **`react-audit-grep-patterns`** — Provides the complete, verified grep scan command library for auditing React codebases before a React 18.3.1 or React 19 upgrade. Use this skill whenever running a migration audit - for both the react18-auditor and react19-auditor agents. Contains every grep pattern needed to find deprecated APIs, removed APIs, unsafe lifecycle methods, batching vulnerabilities, test file issues, dependency conflicts, and React 19 specific removals. Always use this skill when writing audit scan commands - do not rely on memory for grep syntax, especially for the multi-line async setState patterns which require context flags.
  - **资产**: `references/dep-scans.md`, `references/react18-scans.md`, `references/react19-scans.md`, `references/test-scans.md`
  - 安装：`gh skills install github/awesome-copilot react-audit-grep-patterns`
  - 上游：[skills/react-audit-grep-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react-audit-grep-patterns/SKILL.md)

- **`react-container-presentation-component`** — Create a React component using the Container/Presentation pattern in src/components by asking for the component name and type (ui or features), then scaffold files that follow this repository's TypeScript, Storybook, and SCSS conventions. Use when the user explicitly asks for a Container/Presentation-based component or runs /react-container-presentation-component.
  - **资产**: `references/component-architecture.md`, `references/typescript-and-scss-rules.md`
  - 安装：`gh skills install github/awesome-copilot react-container-presentation-component`
  - 上游：[skills/react-container-presentation-component/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react-container-presentation-component/SKILL.md)

- **`react18-batching-patterns`** — Provides exact patterns for diagnosing and fixing automatic batching regressions in React 18 class components. Use this skill whenever a class component has multiple setState calls in an async method, inside setTimeout, inside a Promise .then() or .catch(), or in a native event handler. Use it before writing any flushSync call - the decision tree here prevents unnecessary flushSync overuse. Also use this skill when fixing test failures caused by intermediate state assertions that break after React 18 upgrade.
  - **资产**: `references/batching-categories.md`, `references/flushSync-guide.md`
  - 安装：`gh skills install github/awesome-copilot react18-batching-patterns`
  - 上游：[skills/react18-batching-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react18-batching-patterns/SKILL.md)

- **`react18-dep-compatibility`** — React 18.3.1 and React 19 dependency compatibility matrix.
  - **资产**: `references/apollo-details.md`, `references/router-migration.md`
  - 安装：`gh skills install github/awesome-copilot react18-dep-compatibility`
  - 上游：[skills/react18-dep-compatibility/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react18-dep-compatibility/SKILL.md)

- **`react18-enzyme-to-rtl`** — Provides exact Enzyme → React Testing Library migration patterns for React 18 upgrades. Use this skill whenever Enzyme tests need to be rewritten - shallow, mount, wrapper.find(), wrapper.simulate(), wrapper.prop(), wrapper.state(), wrapper.instance(), Enzyme configure/Adapter calls, or any test file that imports from enzyme. This skill covers the full API mapping and the philosophy shift from implementation testing to behavior testing. Always read this skill before rewriting Enzyme tests - do not translate Enzyme APIs 1:1, that produces brittle RTL tests.
  - **资产**: `references/async-patterns.md`, `references/enzyme-api-map.md`
  - 安装：`gh skills install github/awesome-copilot react18-enzyme-to-rtl`
  - 上游：[skills/react18-enzyme-to-rtl/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react18-enzyme-to-rtl/SKILL.md)

- **`react18-legacy-context`** — Provides the complete migration pattern for React legacy context API (contextTypes, childContextTypes, getChildContext) to the modern createContext API. Use this skill whenever migrating legacy context in class components - this is always a cross-file migration requiring the provider AND all consumers to be updated together. Use it before touching any contextTypes or childContextTypes code, because migrating only the provider without the consumers (or vice versa) will cause a runtime failure. Always read this skill before writing any context migration - the cross-file coordination steps here prevent the most common context migration bugs.
  - **资产**: `references/context-file-template.md`, `references/multi-context.md`, `references/single-context.md`
  - 安装：`gh skills install github/awesome-copilot react18-legacy-context`
  - 上游：[skills/react18-legacy-context/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react18-legacy-context/SKILL.md)

- **`react18-lifecycle-patterns`** — Provides exact before/after migration patterns for the three unsafe class component lifecycle methods - componentWillMount, componentWillReceiveProps, and componentWillUpdate - targeting React 18.3.1. Use this skill whenever a class component needs its lifecycle methods migrated, when deciding between getDerivedStateFromProps vs componentDidUpdate, when adding getSnapshotBeforeUpdate, or when fixing React 18 UNSAFE_ lifecycle warnings. Always use this skill before writing any lifecycle migration code - do not guess the pattern from memory, the decision trees here prevent the most common migration mistakes.
  - **资产**: `references/componentWillMount.md`, `references/componentWillReceiveProps.md`, `references/componentWillUpdate.md`
  - 安装：`gh skills install github/awesome-copilot react18-lifecycle-patterns`
  - 上游：[skills/react18-lifecycle-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react18-lifecycle-patterns/SKILL.md)

- **`react18-string-refs`** — Provides exact migration patterns for React string refs (ref="name" + this.refs.name) to React.createRef() in class components. Use this skill whenever migrating string ref usage - including single element refs, multiple refs in a component, refs in lists, callback refs, and refs passed to child components. Always use this skill before writing any ref migration code - the multiple-refs-in-list pattern is particularly tricky and this skill prevents the most common mistakes. Use it for React 18.3.1 migration (string refs warn) and React 19 migration (string refs removed).
  - **资产**: `references/patterns.md`
  - 安装：`gh skills install github/awesome-copilot react18-string-refs`
  - 上游：[skills/react18-string-refs/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react18-string-refs/SKILL.md)

- **`react19-concurrent-patterns`** — Preserve React 18 concurrent patterns and adopt React 19 APIs (useTransition, useDeferredValue, Suspense, use(), useOptimistic, Actions) during migration.
  - **资产**: `references/react19-actions.md`, `references/react19-suspense.md`, `references/react19-use.md`
  - 安装：`gh skills install github/awesome-copilot react19-concurrent-patterns`
  - 上游：[skills/react19-concurrent-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react19-concurrent-patterns/SKILL.md)

- **`react19-source-patterns`** — Reference for React 19 source-file migration patterns, including API changes, ref handling, and context updates.
  - **资产**: `references/api-migrations.md`
  - 安装：`gh skills install github/awesome-copilot react19-source-patterns`
  - 上游：[skills/react19-source-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react19-source-patterns/SKILL.md)

- **`react19-test-patterns`** — Provides before/after patterns for migrating test files to React 19 compatibility, including act() imports, Simulate removal, and StrictMode call count changes.
  - 安装：`gh skills install github/awesome-copilot react19-test-patterns`
  - 上游：[skills/react19-test-patterns/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/react19-test-patterns/SKILL.md)

- **`readme-blueprint-generator`** — Intelligent README.md generation prompt that analyzes project documentation structure and creates comprehensive repository documentation. Scans .github/copilot directory files and copilot-instructions.md to extract project information, technology stack, architecture, development workflow, coding standards, and testing approaches while generating well-structured markdown documentation with proper formatting, cross-references, and developer-focused content.
  - 安装：`gh skills install github/awesome-copilot readme-blueprint-generator`
  - 上游：[skills/readme-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/readme-blueprint-generator/SKILL.md)

- **`refactor`** — Surgical code refactoring to improve maintainability without changing behavior. Covers extracting functions, renaming variables, breaking down god functions, improving type safety, eliminating code smells, and applying design patterns. Less drastic than repo-rebuilder; use for gradual improvements.
  - 安装：`gh skills install github/awesome-copilot refactor`
  - 上游：[skills/refactor/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/refactor/SKILL.md)

- **`refactor-method-complexity-reduce`** — Refactor given method `${input:methodName}` to reduce its cognitive complexity to `${input:complexityThreshold}` or below, by extracting helper methods.
  - 安装：`gh skills install github/awesome-copilot refactor-method-complexity-reduce`
  - 上游：[skills/refactor-method-complexity-reduce/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/refactor-method-complexity-reduce/SKILL.md)

- **`refactor-plan`** — Create a concrete plan before starting a multi-file refactor. Use when the user asks to plan, sequence, scope, or safely execute a refactor across multiple files; always investigate first, output the plan, and wait for confirmation before making code changes.
  - 安装：`gh skills install github/awesome-copilot refactor-plan`
  - 上游：[skills/refactor-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/refactor-plan/SKILL.md)

- **`remember`** — Transforms lessons learned into domain-organized memory instructions (global or workspace). Syntax: `/remember [>domain [scope]] lesson clue` where scope is `global` (default), `user`, `workspace`, or `ws`.
  - 安装：`gh skills install github/awesome-copilot remember`
  - 上游：[skills/remember/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/remember/SKILL.md)

- **`remember-interactive-programming`** — A micro-prompt that reminds the agent that it is an interactive programmer. Works great in Clojure when Copilot has access to the REPL (probably via Backseat Driver). Will work with any system that has a live REPL that the agent can use. Adapt the prompt with any specific reminders in your workflow and/or workspace.
  - 安装：`gh skills install github/awesome-copilot remember-interactive-programming`
  - 上游：[skills/remember-interactive-programming/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/remember-interactive-programming/SKILL.md)

- **`repo-story-time`** — Generate a comprehensive repository summary and narrative story from commit history
  - 安装：`gh skills install github/awesome-copilot repo-story-time`
  - 上游：[skills/repo-story-time/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/repo-story-time/SKILL.md)

- **`resemble-detect`** — Deepfake detection and media safety — detect AI-generated audio, images, video, and text, trace synthesis sources, apply watermarks, verify speaker identity, and analyze media intelligence using Resemble AI
  - **资产**: `LICENSE`, `references/api-reference.md`
  - 安装：`gh skills install github/awesome-copilot resemble-detect`
  - 上游：[skills/resemble-detect/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/resemble-detect/SKILL.md)

- **`review-and-refactor`** — Review and refactor code in your project according to defined instructions
  - 安装：`gh skills install github/awesome-copilot review-and-refactor`
  - 上游：[skills/review-and-refactor/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/review-and-refactor/SKILL.md)

- **`reviewing-oracle-to-postgres-migration`** — Identifies Oracle-to-PostgreSQL migration risks by cross-referencing code against known behavioral differences (empty strings, refcursors, type coercion, sorting, timestamps, concurrent transactions, etc.). Use when planning a database migration, reviewing migration artifacts, or validating that integration tests cover Oracle/PostgreSQL differences.
  - **资产**: `references/REFERENCE.md`, `references/empty-strings-handling.md`, `references/no-data-found-exceptions.md`, `references/oracle-parentheses-from-clause.md`, `references/oracle-to-postgres-sorting.md`, `references/oracle-to-postgres-timestamp-timezone.md`, `references/oracle-to-postgres-to-char-numeric.md`, `references/oracle-to-postgres-type-coercion.md`, `references/postgres-concurrent-transactions.md`, `references/postgres-refcursor-handling.md`
  - 安装：`gh skills install github/awesome-copilot reviewing-oracle-to-postgres-migration`
  - 上游：[skills/reviewing-oracle-to-postgres-migration/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/reviewing-oracle-to-postgres-migration/SKILL.md)

- **`rhino3d-scripts`** — Authoring and debugging scripts for Rhinoceros 3D (Rhino 8 and later). Use when asked to write RhinoScript (VBScript / .rvb / .vbs), RhinoPython, or RhinoCommon-based scripts; automate Rhino modeling tasks; build command macros; manipulate Rhino geometry, layers, blocks, or document objects; pick objects from the viewport; control redraw and undo; or load and run scripts from the Rhino Script Editor. Covers `rhinoscriptsyntax`, `scriptcontext`, the `Rhino.*` RhinoCommon namespaces (`Rhino.Geometry`, `Rhino.DocObjects`, `Rhino.Input`, `Rhino.UI`, `Rhino.Display`, `Rhino.FileIO`), and the Rhino 8 unified Script Editor.
  - **资产**: `references/macros-and-loading.md`, `references/rhinocommon-map.md`, `references/rhinoscriptsyntax-cheatsheet.md`, `references/vbscript-quirks.md`
  - 安装：`gh skills install github/awesome-copilot rhino3d-scripts`
  - 上游：[skills/rhino3d-scripts/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/rhino3d-scripts/SKILL.md)

- **`roundup`** — Generate personalized status briefings on demand. Pulls from your configured data sources (GitHub, email, Teams, Slack, and more), synthesizes across them, and drafts updates in your own communication style for any audience you define.
  - 安装：`gh skills install github/awesome-copilot roundup`
  - 上游：[skills/roundup/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/roundup/SKILL.md)

- **`roundup-setup`** — Interactive onboarding that learns your communication style, audiences, and data sources to configure personalized status briefings. Paste in examples of updates you already write, answer a few questions, and roundup calibrates itself to your workflow.
  - **资产**: `references/config-template.md`
  - 安装：`gh skills install github/awesome-copilot roundup-setup`
  - 上游：[skills/roundup-setup/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/roundup-setup/SKILL.md)

- **`ruby-mcp-server-generator`** — Generate a complete Model Context Protocol server project in Ruby using the official MCP Ruby SDK gem.
  - 安装：`gh skills install github/awesome-copilot ruby-mcp-server-generator`
  - 上游：[skills/ruby-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ruby-mcp-server-generator/SKILL.md)

- **`ruff-recursive-fix`** — Run Ruff checks with optional scope and rule overrides, apply safe and unsafe autofixes iteratively, review each change, and resolve remaining findings with targeted edits or user decisions.
  - 安装：`gh skills install github/awesome-copilot ruff-recursive-fix`
  - 上游：[skills/ruff-recursive-fix/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ruff-recursive-fix/SKILL.md)

- **`rust-mcp-server-generator`** — Generate a complete Rust Model Context Protocol server project with tools, prompts, resources, and tests using the official rmcp SDK
  - 安装：`gh skills install github/awesome-copilot rust-mcp-server-generator`
  - 上游：[skills/rust-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/rust-mcp-server-generator/SKILL.md)

### S

- **`salesforce-apex-quality`** — Apex code quality guardrails for Salesforce development. Enforces bulk-safety rules (no SOQL/DML in loops), sharing model requirements, CRUD/FLS security, SOQL injection prevention, PNB test coverage (Positive / Negative / Bulk), and modern Apex idioms. Use this skill when reviewing or generating Apex classes, trigger handlers, batch jobs, or test classes to catch governor limit risks, security gaps, and quality issues before deployment.
  - 安装：`gh skills install github/awesome-copilot salesforce-apex-quality`
  - 上游：[skills/salesforce-apex-quality/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/salesforce-apex-quality/SKILL.md)

- **`salesforce-component-standards`** — Quality standards for Salesforce Lightning Web Components (LWC), Aura components, and Visualforce pages. Covers SLDS 2 compliance, accessibility (WCAG 2.1 AA), data access pattern selection, component communication rules, XSS prevention, CSRF enforcement, FLS/CRUD in AuraEnabled methods, view state management, and Jest test requirements. Use this skill when building or reviewing any Salesforce UI component to enforce platform-specific security and quality standards.
  - 安装：`gh skills install github/awesome-copilot salesforce-component-standards`
  - 上游：[skills/salesforce-component-standards/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/salesforce-component-standards/SKILL.md)

- **`salesforce-flow-design`** — Salesforce Flow architecture decisions, flow type selection, bulk safety validation, and fault handling standards. Use this skill when designing or reviewing Record-Triggered, Screen, Autolaunched, Scheduled, or Platform Event flows to ensure correct type selection, no DML/Get Records in loops, proper fault connectors on all data-changing elements, and appropriate automation density checks before deployment.
  - 安装：`gh skills install github/awesome-copilot salesforce-flow-design`
  - 上游：[skills/salesforce-flow-design/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/salesforce-flow-design/SKILL.md)

- **`sandbox-npm-install`** — Install npm packages in a Docker sandbox environment. Use this skill whenever you need to install, reinstall, or update node_modules inside a container where the workspace is mounted via virtiofs. Native binaries (esbuild, lightningcss, rollup) crash on virtiofs, so packages must be installed on the local ext4 filesystem and symlinked back.
  - **资产**: `scripts/install.sh`
  - 安装：`gh skills install github/awesome-copilot sandbox-npm-install`
  - 上游：[skills/sandbox-npm-install/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/sandbox-npm-install/SKILL.md)

- **`scaffolding-oracle-to-postgres-migration-test-project`** — Scaffolds an xUnit integration test project for validating Oracle-to-PostgreSQL database migration behavior in .NET solutions. Creates the test project, transaction-rollback base class, and seed data manager. Use when setting up test infrastructure before writing migration integration tests, or when a test project is needed for Oracle-to-PostgreSQL validation.
  - 安装：`gh skills install github/awesome-copilot scaffolding-oracle-to-postgres-migration-test-project`
  - 上游：[skills/scaffolding-oracle-to-postgres-migration-test-project/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/scaffolding-oracle-to-postgres-migration-test-project/SKILL.md)

- **`scoutqa-test`** — This skill should be used when the user asks to "test this website", "run exploratory testing", "check for accessibility issues", "verify the login flow works", "find bugs on this page", or requests automated QA testing. Triggers on web application testing scenarios including smoke tests, accessibility audits, e-commerce flows, and user flow validation using ScoutQA CLI. Use this skill proactively after implementing web application features to verify they work correctly.
  - 安装：`gh skills install github/awesome-copilot scoutqa-test`
  - 上游：[skills/scoutqa-test/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/scoutqa-test/SKILL.md)

- **`screen-recording`** — Create annotated animated GIF demos and screen recordings for pull requests and documentation. Covers frame capture, timing, imageio-based GIF creation, and per-frame annotation workflows.
  - 安装：`gh skills install github/awesome-copilot screen-recording`
  - 上游：[skills/screen-recording/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/screen-recording/SKILL.md)

- **`secret-scanning`** — Guide for configuring and managing GitHub secret scanning, push protection, custom patterns, and secret alert remediation. For pre-commit secret scanning in AI coding agents via the GitHub MCP Server, this skill references the Advanced Security plugin (`advanced-security@copilot-plugins`). Use this skill when enabling secret scanning, setting up push protection, defining custom patterns, triaging alerts, resolving blocked pushes, or when an agent needs to scan code for secrets before committing.
  - **资产**: `references/alerts-and-remediation.md`, `references/custom-patterns.md`, `references/push-protection.md`
  - 安装：`gh skills install github/awesome-copilot secret-scanning`
  - 上游：[skills/secret-scanning/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/secret-scanning/SKILL.md)

- **`security-review`** — AI-powered codebase security scanner that reasons about code like a security researcher — tracing data flows, understanding component interactions, and catching vulnerabilities that pattern-matching tools miss. Use this skill when asked to scan code for security vulnerabilities, find bugs, check for SQL injection, XSS, command injection, exposed API keys, hardcoded secrets, insecure dependencies, access control issues, or any request like "is my code secure?", "review for security issues", "audit this codebase", or "check for vulnerabilities". Covers injection flaws, authentication and access control bugs, secrets exposure, weak cryptography, insecure dependencies, and business logic issues across JavaScript, TypeScript, Python, Java, PHP, Go, Ruby, and Rust.
  - **资产**: `references/language-patterns.md`, `references/report-format.md`, `references/secret-patterns.md`, `references/vuln-categories.md`, `references/vulnerable-packages.md`
  - 安装：`gh skills install github/awesome-copilot security-review`
  - 上游：[skills/security-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/security-review/SKILL.md)

- **`semantic-kernel`** — Create, update, refactor, explain, or review Semantic Kernel solutions using shared guidance plus language-specific references for .NET and Python.
  - **资产**: `references/dotnet.md`, `references/python.md`
  - 安装：`gh skills install github/awesome-copilot semantic-kernel`
  - 上游：[skills/semantic-kernel/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/semantic-kernel/SKILL.md)

- **`setup-my-iq`** — Create, set up, or update the personal context portfolio: structured markdown files describing who you are, how you work, your teams, and your tool/ADO configuration. Runs the interview workflow for first-time setup and targeted edits for updates. Trigger this skill when the user asks to: set up their context, create or update their context portfolio, "create my IQ", "set up my IQ", edit their profile, add/remove a stakeholder, update ADO config, change team info, update pillars, or set up any plugin configuration. Trigger when another skill fails to find context (missing files or TODO markers) and needs context populated. Also trigger when the user mentions a context change in passing (e.g., "my manager changed", "we added someone to the team") to offer a context file update. Do NOT trigger for read-only questions like "who's on my team?" or "what's my ADO config?". Those are answered directly from the context files referenced in the loaded custom instructions; no skill is needed.
  - **资产**: `assets/templates`
  - 安装：`gh skills install github/awesome-copilot setup-my-iq`
  - 上游：[skills/setup-my-iq/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/setup-my-iq/SKILL.md)

- **`shuffle-json-data`** — Shuffle repetitive JSON objects safely by validating schema consistency before randomising entries.
  - 安装：`gh skills install github/awesome-copilot shuffle-json-data`
  - 上游：[skills/shuffle-json-data/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/shuffle-json-data/SKILL.md)

- **`slang-shader-engineer`** — Use when working with Slang shaders, shader modules, HLSL-compatible GPU code, graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, generics, interfaces, capabilities, cross-compilation, shader optimization, shader review, or C++ engine integration for Slang. Trigger on any mention of Slang, .slang files, slangc, SPIR-V from Slang, Slang modules, [shader("compute")], [shader("vertex")], or requests to write/review/refactor shader code with modern language features. Also trigger for Slang-to-HLSL/GLSL/Metal/CUDA cross-compile questions, or when the user says "shader" alongside "generics", "interfaces", "parameter blocks", "autodiff", or "capabilities".
  - **资产**: `references/language-reference.md`, `references/rules-and-patterns.md`, `references/slang-documentation-full.md`
  - 安装：`gh skills install github/awesome-copilot slang-shader-engineer`
  - 上游：[skills/slang-shader-engineer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/slang-shader-engineer/SKILL.md)

- **`snowflake-semanticview`** — Create, alter, and validate Snowflake semantic views using Snowflake CLI (snow). Use when asked to build or troubleshoot semantic views/semantic layer definitions with CREATE/ALTER SEMANTIC VIEW, to validate semantic-view DDL against Snowflake via CLI, or to guide Snowflake CLI installation and connection setup.
  - 安装：`gh skills install github/awesome-copilot snowflake-semanticview`
  - 上游：[skills/snowflake-semanticview/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/snowflake-semanticview/SKILL.md)

- **`sponsor-finder`** — Find which of a GitHub repository's dependencies are sponsorable via GitHub Sponsors. Uses deps.dev API for dependency resolution across npm, PyPI, Cargo, Go, RubyGems, Maven, and NuGet. Checks npm funding metadata, FUNDING.yml files, and web search. Verifies every link. Shows direct and transitive dependencies with OSSF Scorecard health data. Invoke with /sponsor followed by a GitHub owner/repo (e.g. "/sponsor expressjs/express").
  - 安装：`gh skills install github/awesome-copilot sponsor-finder`
  - 上游：[skills/sponsor-finder/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/sponsor-finder/SKILL.md)

- **`spring-boot-testing`** — Expert Spring Boot 4 testing specialist that selects the best Spring Boot testing techniques for your situation with Junit 6 and AssertJ.
  - **资产**: `references/assertj-basics.md`, `references/assertj-collections.md`, `references/context-caching.md`, `references/datajpatest.md`, `references/instancio.md`, `references/mockitobean.md`, `references/mockmvc-classic.md`, `references/mockmvc-tester.md`, `references/restclienttest.md`, `references/resttestclient.md`, `references/sb4-migration.md`, `references/test-slices-overview.md`, `references/testcontainers-jdbc.md`, `references/webmvctest.md`
  - 安装：`gh skills install github/awesome-copilot spring-boot-testing`
  - 上游：[skills/spring-boot-testing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/spring-boot-testing/SKILL.md)

- **`sql-code-review`** — Universal SQL code review assistant that performs comprehensive security, maintainability, and code quality analysis across all SQL databases (MySQL, PostgreSQL, SQL Server, Oracle). Focuses on SQL injection prevention, access control, code standards, and anti-pattern detection. Complements SQL optimization prompt for complete development coverage.
  - 安装：`gh skills install github/awesome-copilot sql-code-review`
  - 上游：[skills/sql-code-review/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/sql-code-review/SKILL.md)

- **`sql-optimization`** — Universal SQL performance optimization assistant for comprehensive query tuning, indexing strategies, and database performance analysis across all SQL databases (MySQL, PostgreSQL, SQL Server, Oracle). Provides execution plan analysis, pagination optimization, batch operations, and performance monitoring guidance.
  - 安装：`gh skills install github/awesome-copilot sql-optimization`
  - 上游：[skills/sql-optimization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/sql-optimization/SKILL.md)

- **`sql-server-table-reconciliation`** — Use when: comparing SQL Server tables across instances, data migration validation, ETL verification, row mismatch detection, schema drift, reconciliation report, production vs staging comparison. Uses mssql-python driver with Apache Arrow for fast columnar data transfer and comparison.
  - **资产**: `scripts/reconcile.py`
  - 安装：`gh skills install github/awesome-copilot sql-server-table-reconciliation`
  - 上游：[skills/sql-server-table-reconciliation/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/sql-server-table-reconciliation/SKILL.md)

- **`ssma-console`** — Use when: SSMA console operations — create project, generate assessment report, convert schema, migrate data, Oracle to SQL Server migration, schema conversion, data migration
  - 安装：`gh skills install github/awesome-copilot ssma-console`
  - 上游：[skills/ssma-console/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ssma-console/SKILL.md)

- **`structured-autonomy-generate`** — Structured Autonomy Implementation Generator Prompt
  - 安装：`gh skills install github/awesome-copilot structured-autonomy-generate`
  - 上游：[skills/structured-autonomy-generate/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/structured-autonomy-generate/SKILL.md)

- **`structured-autonomy-implement`** — Structured Autonomy Implementation Prompt
  - 安装：`gh skills install github/awesome-copilot structured-autonomy-implement`
  - 上游：[skills/structured-autonomy-implement/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/structured-autonomy-implement/SKILL.md)

- **`structured-autonomy-plan`** — Structured Autonomy Planning Prompt
  - 安装：`gh skills install github/awesome-copilot structured-autonomy-plan`
  - 上游：[skills/structured-autonomy-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/structured-autonomy-plan/SKILL.md)

- **`suggest-awesome-github-copilot-agents`** — Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing custom agents in this repository, and identifying outdated agents that need updates.
  - 安装：`gh skills install github/awesome-copilot suggest-awesome-github-copilot-agents`
  - 上游：[skills/suggest-awesome-github-copilot-agents/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-agents/SKILL.md)

- **`suggest-awesome-github-copilot-instructions`** — Suggest relevant GitHub Copilot instruction files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing instructions in this repository, and identifying outdated instructions that need updates.
  - 安装：`gh skills install github/awesome-copilot suggest-awesome-github-copilot-instructions`
  - 上游：[skills/suggest-awesome-github-copilot-instructions/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-instructions/SKILL.md)

- **`suggest-awesome-github-copilot-skills`** — Suggest relevant GitHub Copilot skills from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing skills in this repository, and identifying outdated skills that need updates.
  - 安装：`gh skills install github/awesome-copilot suggest-awesome-github-copilot-skills`
  - 上游：[skills/suggest-awesome-github-copilot-skills/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-skills/SKILL.md)

- **`swift-mcp-server-generator`** — Generate a complete Model Context Protocol server project in Swift using the official MCP Swift SDK package.
  - 安装：`gh skills install github/awesome-copilot swift-mcp-server-generator`
  - 上游：[skills/swift-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/swift-mcp-server-generator/SKILL.md)

### T

- **`technical-job-search`** — Use this skill when a software engineer asks for help with job search tasks: parsing or analyzing a job description, tailoring a CV/resume, writing a cover letter, evaluating a job offer, or drafting a post-interview follow-up email. Do not activate for general career advice unrelated to an active job search action.
  - 安装：`gh skills install github/awesome-copilot technical-job-search`
  - 上游：[skills/technical-job-search/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/technical-job-search/SKILL.md)

- **`technology-stack-blueprint-generator`** — Comprehensive technology stack blueprint generator that analyzes codebases to create detailed architectural documentation. Automatically detects technology stacks, programming languages, and implementation patterns across multiple platforms (.NET, Java, JavaScript, React, Python). Generates configurable blueprints with version information, licensing details, usage patterns, coding conventions, and visual diagrams. Provides implementation-ready templates and maintains architectural consistency for guided development.
  - 安装：`gh skills install github/awesome-copilot technology-stack-blueprint-generator`
  - 上游：[skills/technology-stack-blueprint-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/technology-stack-blueprint-generator/SKILL.md)

- **`terraform-azurerm-set-diff-analyzer`** — Analyze Terraform plan JSON output for AzureRM Provider to distinguish between false-positive diffs (order-only changes in Set-type attributes) and actual resource changes. Use when reviewing terraform plan output for Azure resources like Application Gateway, Load Balancer, Firewall, Front Door, NSG, and other resources with Set-type attributes that cause spurious diffs due to internal ordering changes.
  - **资产**: `references/azurerm_set_attributes.json`, `references/azurerm_set_attributes.md`, `scripts/.gitignore`, `scripts/README.md`, `scripts/analyze_plan.py`
  - 安装：`gh skills install github/awesome-copilot terraform-azurerm-set-diff-analyzer`
  - 上游：[skills/terraform-azurerm-set-diff-analyzer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/terraform-azurerm-set-diff-analyzer/SKILL.md)

- **`threat-model-analyst`** — Full STRIDE-A threat model analysis and incremental update skill for repositories and systems. Supports two modes: (1) Single analysis — full STRIDE-A threat model of a repository, producing architecture overviews, DFD diagrams, STRIDE-A analysis, prioritized findings, and executive assessments. (2) Incremental analysis — takes a previous threat model report as baseline, compares the codebase at the latest (or a given commit), and produces an updated report with change tracking (new, resolved, still-present threats), STRIDE heatmap, findings diff, and an embedded HTML comparison. Only activate when the user explicitly requests a threat model analysis, incremental update, or invokes /threat-model-analyst directly.
  - **资产**: `references/analysis-principles.md`, `references/diagram-conventions.md`, `references/incremental-orchestrator.md`, `references/orchestrator.md`, `references/output-formats.md`, `references/skeletons`, `references/tmt-element-taxonomy.md`, `references/verification-checklist.md`
  - 安装：`gh skills install github/awesome-copilot threat-model-analyst`
  - 上游：[skills/threat-model-analyst/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/threat-model-analyst/SKILL.md)

- **`tiny-stepping`** — Incremental development workflow that makes the smallest meaningful change per step and pauses for feedback, so the direction gets validated early before continuing. Use for careful, iterative implementation with continuous validation.
  - 安装：`gh skills install github/awesome-copilot tiny-stepping`
  - 上游：[skills/tiny-stepping/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/tiny-stepping/SKILL.md)

- **`tldr-prompt`** — Create tldr summaries for GitHub Copilot files (prompts, agents, instructions, collections), MCP servers, or documentation from URLs and queries.
  - 安装：`gh skills install github/awesome-copilot tldr-prompt`
  - 上游：[skills/tldr-prompt/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/tldr-prompt/SKILL.md)

- **`transloadit-media-processing`** — Process media files (video, audio, images, documents) using Transloadit. Use when asked to encode video to HLS/MP4, generate thumbnails, resize or watermark images, extract audio, concatenate clips, add subtitles, OCR documents, or run any media processing pipeline. Covers 86+ processing robots for file transformation at scale.
  - 安装：`gh skills install github/awesome-copilot transloadit-media-processing`
  - 上游：[skills/transloadit-media-processing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/transloadit-media-processing/SKILL.md)

- **`typescript-mcp-server-generator`** — Generate a complete MCP server project in TypeScript with tools, resources, and proper configuration
  - 安装：`gh skills install github/awesome-copilot typescript-mcp-server-generator`
  - 上游：[skills/typescript-mcp-server-generator/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/typescript-mcp-server-generator/SKILL.md)

- **`typespec-api-operations`** — Add GET, POST, PATCH, and DELETE operations to a TypeSpec API plugin with proper routing, parameters, and adaptive cards
  - 安装：`gh skills install github/awesome-copilot typespec-api-operations`
  - 上游：[skills/typespec-api-operations/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/typespec-api-operations/SKILL.md)

- **`typespec-create-agent`** — Generate a complete TypeSpec declarative agent with instructions, capabilities, and conversation starters for Microsoft 365 Copilot
  - 安装：`gh skills install github/awesome-copilot typespec-create-agent`
  - 上游：[skills/typespec-create-agent/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/typespec-create-agent/SKILL.md)

- **`typespec-create-api-plugin`** — Generate a TypeSpec API plugin with REST operations, authentication, and Adaptive Cards for Microsoft 365 Copilot
  - 安装：`gh skills install github/awesome-copilot typespec-create-api-plugin`
  - 上游：[skills/typespec-create-api-plugin/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/typespec-create-api-plugin/SKILL.md)

### U

- **`ui-screenshots`** — Capture screenshots of web apps during development using Playwright and PIL. Supports full-page captures, interactive states, and an iterate-on-crop workflow that avoids slow re-screenshots.
  - 安装：`gh skills install github/awesome-copilot ui-screenshots`
  - 上游：[skills/ui-screenshots/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/ui-screenshots/SKILL.md)

- **`unit-test-vue-pinia`** — Write and review unit tests for Vue 3 + TypeScript + Vitest + Pinia codebases. Use when creating or updating tests for components, composables, and stores; mocking Pinia with createTestingPinia; applying Vue Test Utils patterns; and enforcing black-box assertions over implementation details.
  - **资产**: `references/pinia-patterns.md`
  - 安装：`gh skills install github/awesome-copilot unit-test-vue-pinia`
  - 上游：[skills/unit-test-vue-pinia/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/unit-test-vue-pinia/SKILL.md)

- **`update-avm-modules-in-bicep`** — Update Azure Verified Modules (AVM) to latest versions in Bicep files.
  - 安装：`gh skills install github/awesome-copilot update-avm-modules-in-bicep`
  - 上游：[skills/update-avm-modules-in-bicep/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/update-avm-modules-in-bicep/SKILL.md)

- **`update-implementation-plan`** — Update an existing implementation plan file with new or update requirements to provide new features, refactoring existing code or upgrading packages, design, architecture or infrastructure.
  - 安装：`gh skills install github/awesome-copilot update-implementation-plan`
  - 上游：[skills/update-implementation-plan/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/update-implementation-plan/SKILL.md)

- **`update-llms`** — Update the llms.txt file in the root folder to reflect changes in documentation or specifications following the llms.txt specification at https://llmstxt.org/
  - 安装：`gh skills install github/awesome-copilot update-llms`
  - 上游：[skills/update-llms/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/update-llms/SKILL.md)

- **`update-markdown-file-index`** — Update a markdown file section with an index/table of files from a specified folder.
  - 安装：`gh skills install github/awesome-copilot update-markdown-file-index`
  - 上游：[skills/update-markdown-file-index/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/update-markdown-file-index/SKILL.md)

- **`update-specification`** — Update an existing specification file for the solution, optimized for Generative AI consumption based on new requirements or updates to any existing code.
  - 安装：`gh skills install github/awesome-copilot update-specification`
  - 上游：[skills/update-specification/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/update-specification/SKILL.md)

### V

- **`vardoger-analyze`** — Use when the user asks to personalize the GitHub Copilot CLI assistant, adapt Copilot to their style, use vardoger, or analyze their Copilot CLI conversation history. Reads the local session directory at `~/.copilot/session-state/`, extracts recurring preferences and conventions, and writes a fenced personalization block into `~/.copilot/copilot-instructions.md`. Runs entirely on the user's machine via the local `vardoger` CLI (`pipx install vardoger`); no network calls and no uploads. Triggers: 'personalize my copilot', 'analyze my copilot history', 'tailor copilot to me', 'run vardoger', 'update my copilot instructions from history', 'make copilot learn my style'.
  - 安装：`gh skills install github/awesome-copilot vardoger-analyze`
  - 上游：[skills/vardoger-analyze/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/vardoger-analyze/SKILL.md)

- **`vscode-ext-commands`** — Guidelines for contributing commands in VS Code extensions. Indicates naming convention, visibility, localization and other relevant attributes, following VS Code extension development guidelines, libraries and good practices
  - 安装：`gh skills install github/awesome-copilot vscode-ext-commands`
  - 上游：[skills/vscode-ext-commands/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/vscode-ext-commands/SKILL.md)

- **`vscode-ext-localization`** — Guidelines for proper localization of VS Code extensions, following VS Code extension development guidelines, libraries and good practices
  - 安装：`gh skills install github/awesome-copilot vscode-ext-localization`
  - 上游：[skills/vscode-ext-localization/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/vscode-ext-localization/SKILL.md)

### W

- **`web-design-reviewer`** — This skill enables visual inspection of websites running locally or remotely to identify and fix design issues. Triggers on requests like "review website design", "check the UI", "fix the layout", "find design problems". Detects issues with responsive design, accessibility, visual consistency, and layout breakage, then performs fixes at the source code level.
  - **资产**: `references/framework-fixes.md`, `references/visual-checklist.md`
  - 安装：`gh skills install github/awesome-copilot web-design-reviewer`
  - 上游：[skills/web-design-reviewer/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/web-design-reviewer/SKILL.md)

- **`webapp-testing`** — Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
  - **资产**: `assets/test-helper.js`
  - 安装：`gh skills install github/awesome-copilot webapp-testing`
  - 上游：[skills/webapp-testing/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/webapp-testing/SKILL.md)

- **`what-context-needed`** — Ask Copilot what files it needs to see before answering a question
  - 安装：`gh skills install github/awesome-copilot what-context-needed`
  - 上游：[skills/what-context-needed/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/what-context-needed/SKILL.md)

- **`winmd-api-search`** — Find and explore Windows desktop APIs. Use when building features that need platform capabilities — camera, file access, notifications, UI controls, AI/ML, sensors, networking, etc. Discovers the right API for a task and retrieves full type details (methods, properties, events, enumeration values).
  - **资产**: `LICENSE.txt`, `scripts/Invoke-WinMdQuery.ps1`, `scripts/Update-WinMdCache.ps1`, `scripts/cache-generator`
  - 安装：`gh skills install github/awesome-copilot winmd-api-search`
  - 上游：[skills/winmd-api-search/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/winmd-api-search/SKILL.md)

- **`winui3-migration-guide`** — UWP-to-WinUI 3 migration reference. Maps legacy UWP APIs to correct Windows App SDK equivalents with before/after code snippets. Covers namespace changes, threading (CoreDispatcher to DispatcherQueue), windowing (CoreWindow to AppWindow), dialogs, pickers, sharing, printing, background tasks, and the most common Copilot code generation mistakes.
  - 安装：`gh skills install github/awesome-copilot winui3-migration-guide`
  - 上游：[skills/winui3-migration-guide/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/winui3-migration-guide/SKILL.md)

- **`workiq-copilot`** — Guides the Copilot CLI on how to use the WorkIQ CLI/MCP server to query Microsoft 365 Copilot data (emails, meetings, docs, Teams, people) for live context, summaries, and recommendations.
  - 安装：`gh skills install github/awesome-copilot workiq-copilot`
  - 上游：[skills/workiq-copilot/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/workiq-copilot/SKILL.md)

- **`write-coding-standards-from-file`** — Write a coding standards document for a project using the coding styles from the file(s) and/or folder(s) passed as arguments in the prompt.
  - 安装：`gh skills install github/awesome-copilot write-coding-standards-from-file`
  - 上游：[skills/write-coding-standards-from-file/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/write-coding-standards-from-file/SKILL.md)

### X

- **`x-twitter-scraper`** — Build GitHub Copilot workflows with Xquik X API SDKs, REST endpoints, MCP tools, TweetClaw OpenClaw plugin installs, signed webhooks, tweet search, user lookup, follower exports, media actions, and agent automation.
  - 安装：`gh skills install github/awesome-copilot x-twitter-scraper`
  - 上游：[skills/x-twitter-scraper/SKILL.md](https://github.com/github/awesome-copilot/tree/main/skills/x-twitter-scraper/SKILL.md)

---

## 参考

- https://github.com/github/awesome-copilot/tree/main/skills
- 本 workspace 工具型 repo：[`docs/SKILL_ECOSYSTEM.md`](../../docs/SKILL_ECOSYSTEM.md)
