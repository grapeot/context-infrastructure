# Playwright Ajax Capture Skill

## 元数据

- **类型**: Workflow
- **适用场景**: 需要逆向一个已登录的 web app 的 internal API，抓取其 ajax/XHR 调用的 URL、method、headers、payload 和 response，用于后续用 plain HTTP 复现调用、绕过 Admin API 限制或做 E2E 自动化
- **创建日期**: 2026-08-06
- **实战验证**: 已用于逆向 Circle 社区的 9 个 internal API endpoint（通知、帖子 CRUD、评论、聊天、图片上传），全部用 plain requests + cookie + CSRF 复现成功

## 目标

让 AI agent 在一个已登录的 Playwright/CDP 浏览器 session 里，拦截并记录前端发出的所有 fetch/XHR 调用，逆向出 internal API 的完整 contract（endpoint、method、params、body、auth headers），从而用 plain `requests` 复现同样的调用——不需要 Admin API key、不需要现场写 raw JS。

## 何时使用

- 用户想用普通成员权限调用某个 web app 的 internal API，但没有官方 API 文档
- Admin API key 太危险或不可用，想走 browser session 鉴权（cookie + CSRF）替代
- 需要把一个 web UI 操作（列帖、发帖、删帖）逆向成可复现的 HTTP 调用

## 何时不用

- 目标 app 有公开 REST API 文档——直接读文档更快
- 只需要读公开页面、不需要鉴权——直接 webfetch
- 操作是纯前端计算、不发 ajax——抓 ajax 没意义

## 可用资源

- **`pw-test` CLI**：位于 `/Users/grapeot/co/knowledge_working/adhoc_jobs/playwright_test_skill/.venv/bin/pw-test`，提供 `goto`/`click`/`eval`/`snapshot`/`storage` 等 CDP 原语（详见 `rules/skills/playwright_e2e.md`）
- **CDP Chrome**：`--remote-debugging-port=9222 --user-data-dir=/tmp/pw_<purpose>_profile`，用户手动登录后 session 即可用
- **Playwright Python**：同 venv 下可直接 `from playwright.async_api import async_playwright`，用于走 CDP 拿 HttpOnly cookie（`document.cookie` 看不到的）和持久网络监听

## 方法论

### 1. 启动 CDP Chrome 并让用户登录

```bash
rm -rf /tmp/pw_<purpose>_profile
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 --user-data-dir=/tmp/pw_<purpose>_profile \
  --no-first-run --no-default-browser-check > /dev/null 2>&1 &
```

导航到目标站，让用户手动登录。SSO/OTP 流程对 agent 是黑盒，不要尝试自动化登录。

### 2. 持久网络监听（优先方案）

**不要用 `window.fetch` monkey-patch**——页面刷新会重置 `window.__captured`，丢失拦截记录。改用 Playwright Python 的 `page.on("request")` / `page.on("response")`，这个走 CDP 协议层，不受页面刷新影响：

```python
import asyncio, json
from playwright.async_api import async_playwright

NOISE = ("segment", "sentry", "amplitude", "google-analytics", "googletagmanager",
         "pendo", "vwo", "stripe", "facebook", "doubleclick", "hotjar", "cookieyes",
         "bugsnag", "packs/", "analytics/track", "active_storage", "assets-v2")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        page = ctx.pages[0]

        captured = []

        def on_request(req):
            if any(n in req.url for n in NOISE):
                return
            entry = {"url": req.url, "method": req.method}
            try:
                pd = req.post_data
                entry["reqBody"] = pd[:5000] if pd else None
            except Exception:
                entry["reqBody"] = "[binary]"
            captured.append(entry)

        def on_response(resp):
            for entry in reversed(captured):
                if entry["url"] == resp.url and entry["method"] == resp.request.method and "status" not in entry:
                    entry["status"] = resp.status
                    break

        page.on("request", on_request)
        page.on("response", on_response)

        # ... perform UI actions: page.goto(), page.click(), page.fill(), etc.
        await page.goto("https://target-domain.com/feed", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        await page.click("button:has-text('New post')")
        # ... fill and submit

        print(json.dumps(captured, indent=2, ensure_ascii=False))

asyncio.run(main())
```

### 3. fetch monkey-patch（备用方案，仅用于 SPA 内部导航）

如果只需要抓 SPA 内部导航（不触发页面刷新）的 ajax，可以用 `pw-test eval` 注入 fetch hook：

```javascript
(function(){
  window.__captured = window.__captured || [];
  if (window.__fetchHooked) return "already hooked";
  window.__fetchHooked = true;
  const orig = window.fetch;
  window.fetch = function(...args){
    const url = typeof args[0]==="string" ? args[0] : (args[0] && args[0].url);
    const init = args[1] || {};
    let bodyDesc = null;
    if (init.body) {
      if (typeof init.body === "string") bodyDesc = {type:"string", value: init.body.slice(0,2000)};
      else if (init.body instanceof FormData) {
        bodyDesc = {type:"FormData", entries: {}};
        for (const [k,v] of init.body.entries()) {
          if (v instanceof File) bodyDesc.entries[k] = {type:"File", name:v.name, size:v.size, mime:v.type};
          else bodyDesc.entries[k] = String(v).slice(0,500);
        }
      } else bodyDesc = {type: init.body.constructor.name};
    }
    const rec = {url, method: init.method||"GET", reqBody: bodyDesc, t: Date.now()};
    window.__captured.push(rec);
    return orig.apply(this, args).then(async resp=>{
      try { const c = resp.clone(); if ((resp.headers.get("content-type")||"").includes("json")) rec.resBody = (await c.text()).slice(0,1000); } catch(e){}
      rec.status = resp.status;
      return resp;
    });
  };
  return "hooked";
})()
```

**但注意**：如果操作触发页面刷新（如 form submit），`window.__captured` 会丢失。实测 update post 的 Save 按钮在某些 SPA 中会触发全页刷新。遇到这种情况立即切换到方案 2（CDP `page.on`）。

### 4. 导出 HttpOnly cookie 用于 plain HTTP 复现

`document.cookie` 拿不到 HttpOnly cookie（如 `remember_user_token`、`_circle_session`）。用 Playwright Python 走 CDP `context.cookies()` 导出完整 cookie header：

```python
import asyncio, json
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        cookies = await ctx.cookies()
        relevant = [c for c in cookies if "target-domain.com" in c.get("domain","")]
        cookie_header = "; ".join(f'{c["name"]}={c["value"]}' for c in relevant)
        csrf = next((c for c in relevant if c["name"]=="csrf_token"), None)
        print(json.dumps({"cookie_header": cookie_header, "csrf_token": csrf["value"] if csrf else None}))

asyncio.run(main())
```

### 5. 鉴权机制判断

internal API 常见的鉴权组合：

- **Cookie + CSRF**：最常见。GET 请求只要带 cookie；POST/PUT/DELETE 还要带 `X-CSRF-Token` header（值通常来自名为 `csrf_token` 的 cookie 或 `<meta name="csrf-token">`）。验证方法：用 fetch + `credentials:"include"` 不显式带 Authorization header 发一个 GET，如果 200 说明 cookie-only 就够。
- **Bearer JWT**：`Authorization: Bearer <jwt>` header。JWT 通常存在 localStorage 或由前端从 cookie 换取。如果 cookie-only GET 失败、需要 Authorization，从 `pw-test storage` 或拦截的 request headers 里找 JWT。
- **两者都要**：cookie 做 session、JWT 做 API auth。少见但存在。实测 Circle 的 GET 只靠 cookie 就 200，JWT 是冗余的。

先验证最低权限组合：cookie-only GET 能过就不加 JWT；mutation 失败再加 CSRF；还不行才查 Authorization。

### 6. 用 plain requests 验证

拿到 cookie + csrf 后，用 requests 复现一次调用，确认脱离浏览器也能跑：

```python
import requests
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cookie": cookie_header,
    "X-CSRF-Token": csrf_token,  # mutation 才需要
    "Referer": "https://target-domain.com/",
    "User-Agent": "Mozilla/5.0 ...",
}
r = requests.get("https://target-domain.com/internal_api/...", headers=headers)
```

只有 requests 验证通过，才能放心写进 CLI。建议写一个端到端验证脚本，覆盖所有逆向出的 endpoint（create → update → reply → list → delete），一次跑通全部。

## 已知陷阱

### 1. 页面刷新重置 window.__captured

**症状**：注入了 fetch hook，点了 Save 按钮，但 `__captured` 为空。

**原因**：Save 触发了全页刷新（form submit），JS 上下文重置，`window.__captured` 和 `window.__fetchHooked` 都丢了。

**应对**：不要依赖 `window.__captured`。改用 Playwright Python 的 `page.on("request")` / `page.on("response")`，这个走 CDP 协议层，不受页面刷新影响。

### 2. SSO 登录页直接拼 URL 会 403

**症状**：直接 `pw-test goto "https://app/.../space/123"` 返回 "We were unable to process your request"。

**原因**：SSO 校验 referer/origin，直接跳深链被拦。

**应对**：先 `goto` 到 feed/首页，再从 UI 链接点击导航进目标 space，让 referer 链自然建立。

### 3. document.cookie 拿不到 HttpOnly cookie

**症状**：`pw-test eval 'document.cookie'` 看到的 cookie 不全，缺少 `remember_user_token`、`_circle_session` 等关键 session cookie。

**原因**：HttpOnly cookie 设计上对 JS 不可见。

**应对**：用 Playwright Python `context.cookies()`（走 CDP 协议层，能拿 HttpOnly），不要用 `document.cookie`。

### 4. set_key 重复写入导致 .env 出现重复 key

**症状**：`.env` 里同一个 key 出现多行（如两行 `CIRCLE_CLIENT_COOKIE=`）。

**原因**：python-dotenv 的 `set_key` 在某些模式下追加而非覆盖。

**应对**：更新 `.env` 前先 dedup by key（保留最后一次出现），或在写入前清空目标 key 再 set。

### 5. analytics 噪音淹没业务 API

**症状**：captured 里 90% 是 segment/pendo/google-analytics/sentry/googletagmanager 请求。

**应对**：过滤时硬编码排除清单：`segment`、`sentry`、`amplitude`、`google-analytics`、`googletagmanager`、`pendo`、`hotjar`、`vwo`、`doubleclick`、`facebook.com`、`stripe.com`（除非业务就是支付）、`bugsnag`、`packs/js`、`analytics/track`、`active_storage`、`assets-v2`。

### 6. TipTap/ProseMirror 编辑器：innerHTML 不触发 React 状态更新

**症状**：用 `el.innerHTML = '<p>content</p>'` 设置 TipTap 编辑器内容，Post 按钮点击后没有任何网络请求。

**原因**：TipTap/ProseMirror 用 React 状态管理编辑器内容。直接设 `innerHTML` 不会触发 React 的 `onChange`/`input` 状态更新，React 认为 editor 是空的，submit 按钮不发出请求。

**应对**：用 `page.keyboard.type(text, delay=30)` 真正通过键盘输入触发 React 状态。先用 `page.click(editor)` focus，再 `keyboard.type`。如果编辑器有旧内容，先 `keyboard.press("Meta+A")` + `keyboard.press("Backspace")` 清空。

### 7. POST 返回的 response 可能没有 id 字段

**症状**：用 POST 创建资源后，response 里没有 `id` 字段，只有 `creation_uuid` 或类似字段。如果接着用这个不存在的 `id` 作为后续请求的参数（如 `parent_message_id`），参数变成 None，请求行为不符合预期（如 thread reply 变成独立消息）。

**原因**：部分 internal API 的 POST 返回的是异步处理凭证（`creation_uuid`），不是资源 ID。资源 ID 在服务器处理完成后才生成。

**应对**：POST 后不要直接用 response 里的 id。如果需要新资源的 ID，POST 后再发一次 GET（fetch list）找到刚创建的资源。或者参考已有项目（如 translation bot）的做法：发完消息后立即 fetch messages，通过内容匹配找到新消息的数字 ID。

### 8. CSRF token 在页面刷新后变化

**症状**：`.env` 里保存的 CSRF token 突然失效，mutation 请求返回 403。

**原因**：页面刷新后 `csrf_token` cookie 可能重新生成。

**应对**：`.env` 里的 CSRF 值需要定期更新。如果 mutation 失败且 status 403，先用 CDP 重新导出 cookie + CSRF。

### 9. 搞错 parent message ID 导致 thread reply 不可见

**症状**：API 返回 202 且 `parent_message_id` 正确回显，`fetch_replies` 也能查到回复，但浏览器 UI 的 thread 面板里看不到回复。

**原因**：给错误的 parent message ID 发了 thread reply。API 层面成功了（reply 确实关联到那个 parent），但你在 UI 里打开的是另一条消息的 thread 面板。

**应对**：发 thread reply 前，先通过 API 查询确认 parent message 的真实 ID。不要用 POST 返回的 `creation_uuid` 推断 ID。在 UI 里验证前，确保你打开的 thread 面板对应的是你发 reply 的那条消息。

### 10. 猜测 SPA URL 模式导致 404，污染浏览器 session

**症状**：为了用 Playwright 捕获单个 post 的 ajax 调用，直接拼接 URL `https://community.circle.so/s/<space-slug>/p/<post-slug>` 导航过去，页面返回 "We were unable to process your request"（404 错误页），并且后续从这个 session 页面导航到 `/s/<space-slug>` 也持续 404。

**原因**：Circle 的 SPA 路由不使用 `/s/<space>/p/<post>` 模式。猜测的 URL 结构与实际路由不匹配，导航到一个不存在的路由后，SPA 的前端路由状态可能进入异常分支，导致后续从同一 page 导航到合法路由也持续失败。CDP `page.on("request"/"response")` 捕获到的只有 404 的 HTML 文档请求，没有任何 `internal_api` 调用——因为 SPA 在路由匹配阶段就失败了，根本没走到数据加载阶段。

**应对**：不要猜测 SPA 的深链 URL 模式。正确做法：
1. 先导航到已知合法的入口页（如社区首页 `/` 或 feed 页），等 `networkidle`
2. 用 `page.locator("a[href*='keyword']")` 找到目标链接的 `<a>` 标签，用 `.click()` 走 SPA 内部路由跳转
3. 如果 list endpoint（如 `list-posts`）已经返回了完整 record（含 body），直接用 plain HTTP 复现那个 endpoint，不需要 Playwright 捕获
4. 如果不确定 URL 结构，先在浏览器里手动导航到目标页面，从地址栏复制真实 URL，再喂给 Playwright

这个教训也说明：在 `list-posts` 已经能返回完整数据的情况下，不应该用 Playwright 去捕获"看一个 post"的 ajax——直接调用已有的 list endpoint 或给 CLI 加 `get-post` 命令即可。Playwright Ajax Capture 是"没有 API 文档时的逆向工具"，不是"已有 API 时的首选方案"。

## 验收标准

- [ ] CDP Chrome 启动且用户已登录目标站（`pw-test url` 返回已登录态 URL，不是 login 页）
- [ ] 使用 CDP `page.on("request"/"response")` 持久监听网络（不依赖 `window.__captured`）
- [ ] 触发目标操作后 captured 里能找到业务 API 调用（非 analytics 噪音）
- [ ] 提取出 endpoint URL、method、关键 params、request body schema、response schema 要点
- [ ] HttpOnly cookie 通过 Playwright Python CDP 导出
- [ ] plain `requests` 复现调用成功（status 200/201/202，response body 结构与浏览器一致）
- [ ] 如果需要新创建资源的 ID，POST 后再 GET 确认 ID（不要用 `creation_uuid` 当 ID）
- [ ] 凭证更新到 `.env`（如适用），requests 模式跑通

## 与现有 skill 的关系

- **`playwright_e2e.md`**：本 skill 是其特化版——E2E skill 关注"复现一个 UI flow 写成测试"，本 skill 关注"逆向 ajax contract 用 plain HTTP 复现"。共享 CDP Chrome 启动、pw-test CLI、避免 stale profile 等 pitfall。
- **`bestpractice_gui_automation.md`**：通用 GUI 自动化方法论，本 skill 是其"把无 API 的界面转化为可编程接口"原则的具体落地。