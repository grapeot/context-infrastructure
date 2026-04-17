# Skill: Typefully 发帖 CLI

通过 Typefully v2 API 创建草稿、排期发布、立即发布 tweet 和 thread。

## When to Use

用户说出以下意图时触发：
- 发个推文
- 发 Twitter / 发 X
- 把这篇发到 Twitter
- 排期发推
- share 报告发布后同步发 Twitter

## Prerequisites

- 根目录 `.env` 包含：
  - `TYPEFULLY_API_KEY`：Typefully API key
  - `TYPEFULLY_SOCIAL_SET_ID`：目标账号对应的 social set ID
- Python venv 已激活
- 依赖已安装：`pip install -r tools/requirements.txt`

Typefully 的 API key 可在 Settings → API 中生成。Social set ID 需要从你自己的 Typefully 账号配置中获取。

## 五条发布规则

1. **默认单条，不默认 thread**：只有在内容天然需要拆成 2-4 条，或者用户明确要求 thread 时再发 thread。
2. **带 URL 时优先排期**：这套 workflow 默认把带 URL 的 tweet 排到 1-2 分钟后，不直接 `now`。这样更稳，也方便最后再检查一次文案和链接。
3. **URL 带 UTM**：链接建议使用 tracked URL，例如 `https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post`。
4. **长度按 weighted count 校验**：发布前先跑 `count`，不要凭肉眼估 280 字符。URL 按 23 计，CJK 字符通常按 2 计。
5. **Long post 显式开启**：超过标准 tweet 长度时，用 `--long-post`。long post 和 thread 是两种不同格式，不混用。

## Usage

所有命令从 repo 根目录运行。

### 单条 tweet

```bash
python tools/typefully_post.py draft --text "Hello from the API!"
python tools/typefully_post.py post --text "Going live now!" --publish-at now
python tools/typefully_post.py post --text "Tomorrow morning" --publish-at "2026-04-20T16:00:00Z"
python tools/typefully_post.py count --text "Draft tweet with URL https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post"
```

### Long post

```bash
python tools/typefully_post.py post --text "$(cat long_post.md)" --publish-at "2026-04-20T16:00:00Z" --long-post
```

### Thread

Thread 文件格式：每条 tweet 之间用 `---` 分隔。

```bash
python tools/typefully_post.py post --thread-file my_thread.md
python tools/typefully_post.py schedule 12345 --at "2026-04-20T16:00:00Z"
printf "First tweet\n---\nSecond tweet" | python tools/typefully_post.py post --thread-stdin
```

### 草稿管理

```bash
python tools/typefully_post.py list --status published --limit 10
python tools/typefully_post.py list --status draft
python tools/typefully_post.py get 12345
python tools/typefully_post.py publish 12345
python tools/typefully_post.py schedule 12345 --at "2026-04-20T16:00:00Z"
python tools/typefully_post.py schedule 12345 --next-free-slot
python tools/typefully_post.py delete 12345
python tools/typefully_post.py draft --text "tweet content" --draft-title "Launch post"
```

## 发前检查

先用本地 CLI 做 weighted count：

```bash
python tools/typefully_post.py count --text "你的文案 https://example.com/article?utm_source=twitter&utm_medium=social&utm_campaign=launch-post"
python tools/typefully_post.py count --thread-file my_thread.md
```

输出会显示每条 tweet 的 `weighted_length/280`，超限时标为 `TOO_LONG`。

## 写作习惯

- Observation first：先说一个会改变读者判断的观察、数字或选择，再给结论
- 一条 tweet 只承载一个主判断，把链接当延伸阅读
- 默认只放一个 URL。单条放末尾，thread 放最后一条
- 文风偏工程师。少写摘要腔，多写判断和观察

## Optional workflow

如果你已经有自己的分享工作流，可以把这条 skill 接在后面：

1. 先发布文章或报告，拿到公开 URL
2. 在 URL 上加 UTM 参数
3. 写 tweet 文案，先跑 `count`
4. 最后用 `post` 或 `draft + schedule` 发出

## Notes

- `--publish-at` 支持 `now`、`next-free-slot` 或 ISO 时间
- `post --thread-file` 适合先创建 thread 草稿；如果你要精确控制时间，`draft` 后再 `schedule` 更直接
- `TYPEFULLY_API_KEY` 和 `TYPEFULLY_SOCIAL_SET_ID` 都应由用户自己提供，不要写进仓库
