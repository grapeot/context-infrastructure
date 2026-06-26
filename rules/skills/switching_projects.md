## 元数据

- **类型**: Workflow
- **分类**: Cursor-Native
- **适用场景**: Switch the current Cursor workspace to a different project directory using the cursor-app-control MCP. Use when the user asks to switch projects, open another repo, jump to a different codebase, or move to a worktree.
- **上游来源**: [switching-projects](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/switching-projects)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Switch Project

Use this skill when the user wants to switch to a different project, open another codebase, or move the current conversation to a different workspace root.

## How It Works

Cursor has a built-in MCP server called `cursor-app-control` with a tool called `move_agent_to_root` that changes the agent's active workspace directory. This lets you switch projects mid-conversation without opening a new window.

## Steps

1. **Ask or infer the target project** — if the user says "switch to my-app", search for it. Common project locations:
   - `~/Documents/development/`
   - `~/projects/`
   - `~/code/`
   - `~/repos/`

   List directories in the likely parent folder to find the project:

   ```bash
   ls ~/Documents/development/
   ```

   If ambiguous, ask the user which project they mean.

2. **Switch the workspace** — call the `cursor-app-control` MCP tool:

   ```
   Tool: move_agent_to_root
   Arguments: { "rootPath": "/Users/<username>/Documents/development/<project-name>" }
   ```

   This updates the visible workspace, file tree, and default working directory for all subsequent commands.

3. **Orient in the new project** — after switching, briefly describe what you see:
   - Read the project's `package.json`, `README.md`, or equivalent to understand the stack.
   - Run `git status` to show the current branch and state.
   - List the top-level directory structure.

## Creating a New Project

If the user wants to start a new project and switch to it:

1. Call `create_project` with the desired path — this creates the directory and initializes a git repo.
2. Call `move_agent_to_root` to switch into it.
3. Begin scaffolding.

## Notes

- This only works if the `cursor-app-control` MCP server is enabled.
- The switch happens in the current conversation — no new window is opened.
- All file paths in subsequent tool calls will resolve relative to the new root.
- You can switch back to the original project the same way.
