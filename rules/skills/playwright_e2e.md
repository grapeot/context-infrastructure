# Playwright E2E 测试方法论

## 元数据

- **类型**: Workflow
- **适用场景**: 需要对带前端 UI 的系统做端到端测试，尤其是涉及第三方 SSO（Logto/Auth0 等）、多步骤注册/登录流程、邮件验证码等复杂交互的场景
- **创建日期**: 2026-06-27

## 这个文件是干什么的

教 AI agent 如何高效地用 Playwright 建立可靠的 E2E 测试。核心方法论是"先手动跑通，再自动化"——不要一上来就写自动化脚本死磕，而是先用 CDP 模式逐步观察页面行为，摸清完整流程后再用程序 reproduce。

## 核心方法论：先手动，再自动化

### 为什么不能直接写自动化脚本

E2E 测试最大的坑不是写代码，而是不知道页面接下来会发生什么。第三方 SSO 登录流程尤其如此：弹窗、modal、多步表单、redirect 链路、SDK 内部状态——这些在文档里往往说不清楚，只有实际跑一遍才能看到全貌。

直接写自动化脚本的问题在于：当脚本在某一步卡住时，你不知道是 selector 不对、是页面还没加载、是流程变了、还是本来就有这一步但脚本没处理。你会反复改 selector、加 wait、猜页面状态，效率极低。

### CDP 手动调试法

Chrome DevTools Protocol (CDP) 让 Playwright 连接到一个已经打开的 Chrome 实例。你可以分步操作页面（goto、click、fill），每步后用 snapshot 查看完整 DOM 状态（URL、body text、所有 input、所有 button、所有 link）。这比 headless 脚本高效得多，因为你能看到页面在每一步的实际状态。

**启动 CDP Chrome：**

```bash
pkill -f "remote-debugging-port=9222" 2>/dev/null; sleep 1
nohup "<chromium_path>" --remote-debugging-port=9222 --disable-extensions \
  --user-data-dir=/tmp/playwright_debug_profile about:blank > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:9222/json/version | head -3  # 验证 CDP 就绪
```

Chromium 路径在 macOS 上通常是 `~/Library/Caches/ms-playwright/chromium-XXXX/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing`。

**分步操作辅助脚本：**

写一个单文件 Python 脚本（如 `/tmp/pw_step.py`），支持 `goto`、`click`、`fill`、`snapshot`、`wait`、`reload`、`storage`、`eval` 等子命令。每次调用连接 CDP、执行一个操作、打印结果、断开连接。这样你可以像在终端里逐行操作浏览器一样调试。

**snapshot 子命令**是核心——它打印当前页面的 URL、title、body text（前 1500 字符）、所有 input（name/type/visible/value）、所有 button（text/visible）、所有 link（text/href/visible）。这让你完整看到页面状态，不需要截图。

### 从手动到自动化的流程

1. **启动 CDP Chrome**，用辅助脚本逐步走完整个流程
2. **每步记录**：URL 变化、需要交互的元素 selector、页面跳转条件
3. **摸清所有分支**：新用户 vs 已有用户、首次登录 vs 后续登录、不同 SSO app 的 register vs sign-in 流程
4. **用程序 reproduce**：把手动步骤翻译成 Playwright 脚本，用 `wait_for` + selector 替代固定 `wait_for_timeout`
5. **跑通后更新本 skill**：把新发现的坑记录到"已知陷阱"部分

## 验收标准

- E2E 测试能在本地完整跑通，不卡在任何中间步骤
- 测试覆盖完整用户旅程（所有角色的登录 + 核心操作）
- 每一步的等待基于元素状态（`wait_for` selector），不依赖固定 timeout
- 已知限制（如第三方 onboarding 页面不可控）有明确记录
- 测试失败时保留现场（不执行 cleanup），测试通过时自动清理

## 可用资源

- Playwright Python（`pip install playwright && python -m playwright install chromium`）
- CDP 模式：`playwright.chromium.connect_over_cdp("http://localhost:9222")`
- unified_email（如果需要从邮件中提取验证码）
- Logto Management API（如果需要创建/删除测试用户、分配 role）

## 已知陷阱

### 1. SSO SDK callback 不自动处理

**表现：** SSO 登录完成后 redirect 回前端 callback URL（如 `/callback?code=...`），但页面显示未登录状态，SDK 没有处理 token exchange。

**根因：** 很多 SSO SDK（如 `@logto/react`）需要显式调用 callback 处理 hook（如 `useHandleSignInCallback`）。SDK 不会自动检测 callback URL 并处理。

**应对：** 在前端根组件中调用 SDK 提供的 callback hook。对于 SPA（没有路由），callback 和首页是同一个组件，hook 会在 URL 匹配时自动处理。

### 2. JWT algorithm 不匹配

**表现：** 前端拿到 SSO token 后调 API，后端返回 401 "Invalid token"。

**根因：** SSO provider 可能使用非标准 algorithm（如 Logto 用 ES384），但后端 JWT 验证只配置了常见的 RS256/ES256。

**应对：** 解码 token header 检查 `alg` 字段，确保后端 `jwt.decode` 的 `algorithms` 参数包含它。

### 3. JWT issuer 带后缀

**表现：** JWT 验证报 `InvalidIssuerError`。

**根因：** SSO provider 的 OIDC discovery endpoint 返回的 `issuer` 可能带 `/oidc` 后缀（如 `https://auth.example.com/oidc`），但配置中的 `issuer` 不带后缀（如 `https://auth.example.com`）。

**应对：** 在后端 JWT 验证时拼接 `f"{settings.issuer}/oidc"`，或者直接从 OIDC discovery endpoint 读取 issuer 值。

### 4. Resource access token 不含 email/roles

**表现：** 后端 JWT 验证通过，但 token claims 里没有 email 或 roles，后端无法识别用户身份。

**根因：** SSO 的 resource access token（audience = API URL）只包含 `sub`、`iss`、`aud`、`exp` 等标准 JWT claims，不包含 OIDC scope claims（email、profile）。OIDC userinfo endpoint 也不接受 resource token。

**应对：** 用 Management API 通过 `sub` 查用户信息。`GET /api/users/{sub}` 获取 email/name，`GET /api/users/{sub}/roles` 获取 roles。需要 M2M 凭证（app_id + app_secret）。

### 5. 新用户登录有多步 modal

**表现：** 验证码提交后页面没跳转，看起来卡住了。

**根因：** 新用户首次登录时 SSO 会弹出多个 modal：
1. "No account found, Create new one?" → 需要点 Continue
2. "Agree to Terms of Use and Privacy Policy" → 需要点 Agree
3. Set password 页面 → 需要填密码并 Save
4. Extra-profile 页面（"Tell us about yourself"）→ 需要填 Name 并 Continue

**应对：** 验证码提交后，依次检查并处理每个 modal/页面。用 `div.ReactModalPortal` 检测 modal，用 modal 内的按钮 selector 点击。Management API 创建的用户也会走 Set password（因为没预设密码），但不弹 "No account found" modal。

### 6. Register vs Sign-in 流程不同

**表现：** Guest 通过 signup URL 注册时，验证码提交后页面行为与 sponsor/admin 登录不同。

**根因：** Sign-in 流程验证码提交后可能弹 "No account found" modal（如果用户不存在）。Register 流程不会弹这个 modal（因为本来就是创建新账户），验证码提交后直接跳 Set password。

**应对：** 对 register 和 sign-in 用不同的处理逻辑。Register 流程不需要检查 "No account found" modal，直接检查 Set password 页面。

### 7. 第三方 onboarding 页面不可控

**表现：** SSO 注册完成后 redirect 到第三方社区平台（如 Circle.so）的 profile onboarding 页面，form 提交失败。

**根因：** 第三方平台的 onboarding form 是 Rails form（或类似），需要 CSRF token + POST 提交，用 JS `form.submit()` 会变成 GET 请求导致失败。

**应对：** 如果核心功能（账户创建、access group 授权）已验证通过，onboarding form 不是 E2E 的范围。到达该页面即认为注册完成，不尝试提交第三方 form。

### 8. 固定 timeout 不够

**表现：** 自动化脚本在某一步等待 3 秒后检查元素，但页面还没加载完，报 "not found"。

**根因：** SSO 登录后的 API 调用可能需要经过 Management API（查用户信息），耗时不确定。固定 3 秒在某些网络条件下不够。

**应对：** 用 `locator.wait_for(timeout=30000)` 等待目标元素出现，而不是固定 `wait_for_timeout(3000)` 然后检查。对 "loading" 状态元素用 `wait_for(state="detached")` 等待消失。

### 9. JWT 模式下不能用 test headers 做后端验证

**表现：** E2E 测试后端验证步骤调 API 返回 401。

**根因：** 后端运行在 JWT auth mode 时，只接受真实 JWT token，不认 test headers（`X-Test-User-Email` 等）。

**应对：** 后端验证步骤直接读数据库或调用 Service 层，不通过 HTTP API。或者在前端 Playwright session 中提取 token 后用真实 token 调 API。

## 与现有 skill 的关系

- `bestpractice_gui_automation.md` — GUI 自动化的通用方法论
- `bestpractice_staged_approach.md` — 分阶段工作法，E2E 调试天然适合"先隔离再处理"
- `workflow_parallel_subagents.md` — 如果需要同时测多个角色旅程，可以用并行 subagent