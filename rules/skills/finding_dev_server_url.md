## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Scan running terminals for dev server URLs (localhost ports), report them, and optionally open the app in Cursor's built-in browser.
- **上游来源**: [finding-dev-server-url](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/finding-dev-server-url)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Finding Dev Server URL

Detect which dev servers are running, what ports they're on, and open them.

## How It Works

Cursor stores live terminal output in text files. Each terminal has a file at:

```
<terminals_folder>/<id>.txt
```

The terminals folder path is provided in your system context. Each file contains metadata (pid, cwd, last command) followed by the full terminal output.

## Workflow

### 1. List All Terminals

```bash
ls <terminals_folder>/*.txt
```

### 2. Read Each Terminal's Metadata

Read the first ~10 lines of each terminal file to see:
- `pid` — process ID
- `cwd` — working directory
- `last_command` — what's running (e.g. `npm run dev`, `pnpm dev`, `python manage.py runserver`)

Skip terminals where the last command is clearly not a server (e.g. `git status`, `ls`, `cd`).

### 3. Scan for Server URLs

Read the full content of terminals that look like they're running a server. Search for these patterns:

| Framework | Pattern |
|-----------|---------|
| Next.js | `Local: http://localhost:XXXX` or `▲ Ready` |
| Vite | `Local: http://localhost:XXXX/` |
| Create React App | `Local: http://localhost:XXXX` |
| Express | `listening on port XXXX` or `listening at http://...` |
| Django | `Starting development server at http://127.0.0.1:XXXX/` |
| Rails | `Listening on http://127.0.0.1:XXXX` |
| Flask | `Running on http://127.0.0.1:XXXX` |
| Go | `Listening on :XXXX` or `http server started on :XXXX` |
| PHP | `Development Server (http://localhost:XXXX) started` |
| Remix | `http://localhost:XXXX` |
| Astro | `http://localhost:XXXX` |
| Nuxt | `http://localhost:XXXX` |

Regex to match most server output:

```
https?://(localhost|127\.0\.0\.1|0\.0\.0\.0)(:\d+)
```

Also check for standalone port patterns:

```
(listening|started|running|ready|serving).*(port\s*|:)\s*(\d{4,5})
```

### 4. Report

Print a summary:

```
Dev servers found:
  Terminal 1 (pid 12345) — npm run dev → http://localhost:3000 (cwd: /Users/me/app)
  Terminal 3 (pid 67890) — python manage.py runserver → http://127.0.0.1:8000 (cwd: /Users/me/api)
```

If no servers are found, say so and suggest starting one.

### 5. Open in Browser (Optional)

If the user wants to view the app, use Cursor's built-in browser:

```
browser_navigate → http://localhost:<port>
```

Then take a screenshot to confirm it's rendering:

```
browser_take_screenshot
```

## Tips

- If multiple servers are found, ask the user which one to open
- If a terminal shows an error (e.g. `EADDRINUSE`, `address already in use`), report the conflict
- If the server crashed (process exited), note that too — check for `exit_code` in the terminal file footer
- Common default ports: Next.js (3000), Vite (5173), Django (8000), Rails (3000), Flask (5000), Go (8080)
