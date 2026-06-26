## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Detect EADDRINUSE and port conflicts, find what's using the port, and resolve it by killing the process or suggesting an alternative port.
- **上游来源**: [detecting-port-conflicts](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/detecting-port-conflicts)
- **user-invocable**: true
- **导入日期**: 2026-06-26

---

# Detecting Port Conflicts

When a dev server fails to start because a port is already in use, diagnose and resolve it.

## Detection

Scan terminal output for these patterns:
- `EADDRINUSE`
- `address already in use`
- `Port XXXX is already in use`
- `bind: address already in use`
- `OSError: [Errno 98] Address already in use`

Extract the port number from the error message.

## Diagnosis

Find what's using the port:

```bash
lsof -i :<PORT> -P -n
```

This shows the PID, process name, and user. Common culprits:
- A previous dev server that didn't shut down cleanly
- Another project's dev server
- A Docker container
- A system service

## Resolution Options

### Option 1: Kill the blocking process

```bash
kill <PID>
# If it doesn't stop:
kill -9 <PID>
```

Then restart the original server.

### Option 2: Use a different port

Suggest the next available port:

```bash
# Check if port+1 is free
lsof -i :<PORT+1> -P -n
```

Update the dev server config or start command:
- Next.js: `next dev -p <PORT>`
- Vite: `vite --port <PORT>`
- Express: set `PORT` env var
- Django: `python manage.py runserver <PORT>`

### Option 3: Kill all node processes (nuclear option)

```bash
killall node
```

Only suggest this if the user confirms — it kills everything.

## Tips

- On macOS, ports below 1024 require root
- Docker containers bind ports that persist even if the container is stopped — check `docker ps`
- If `lsof` shows nothing, the port may be in TIME_WAIT state — just wait 30 seconds or use a different port
