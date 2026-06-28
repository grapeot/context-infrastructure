# Cocoon Architecture Diagram — 暗色 HTML 架构图

## 元数据

- **类型**: Workflow
- **适用场景**: 生成暗色主题、自包含 HTML+SVG 系统/云/基础设施架构图；浏览器内 Copy/PNG/PDF 导出
- **上游来源**: [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)（MIT）
- **创建日期**: 2026-06-27
- **user-invocable**: true

---

## 何时触发

系统架构图、云拓扑、微服务/AWS/K8s 部署图，且需要**单 HTML 文件 + 浏览器导出**。

**路由**：多风格 SVG+PNG → `generating_tech_diagrams.md`；survey 可编辑 → Excalidraw；Markdown 示意 → Mermaid。

## 安装

```bash
curl -L -o /tmp/architecture-diagram.zip \
  https://github.com/Cocoon-AI/architecture-diagram-generator/raw/main/architecture-diagram.zip
unzip /tmp/architecture-diagram.zip -d ~/.cursor/skills/
```

生成前读 `architecture-diagram/SKILL.md` 与 `resources/template.html`。

## 工作流

1. 收集组件与连接 → 2. 基于 template 定制 → 3. 保留 export toolbar → 4. 输出 `.html`

默认输出：`tools/<name>_architecture.html` 或 `tmp/diagrams/`。

## 设计系统速查

| 类型 | Stroke |
|------|--------|
| Frontend | `#22d3ee` |
| Backend | `#34d399` |
| Database | `#a78bfa` |
| Cloud/AWS | `#fbbf24` |
| Security | `#fb7185` |

背景 `#020617` + 40px 网格；字体 JetBrains Mono；箭头先画、组件盒用 opaque underlay 遮罩。

## 参考

- https://github.com/Cocoon-AI/architecture-diagram-generator
