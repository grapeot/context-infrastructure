## 元数据

- **类型**: Workflow
- **分类**: Infrastructure & DevOps
- **适用场景**: Dockerize an application with a production-ready Dockerfile, docker-compose setup, and .dockerignore.
- **上游来源**: [adding-docker](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-docker)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add Docker

Use this skill when the user asks to dockerize, containerize, or add Docker support to an application.

## Steps

1. **Detect the runtime** — inspect `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, etc. to determine the language and runtime.

2. **Create a multi-stage `Dockerfile`**

   For Node.js (example):

   ```dockerfile
   FROM node:20-alpine AS base

   FROM base AS deps
   WORKDIR /app
   COPY package.json package-lock.json ./
   RUN npm ci --omit=dev

   FROM base AS build
   WORKDIR /app
   COPY package.json package-lock.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   FROM base AS runner
   WORKDIR /app
   ENV NODE_ENV=production
   COPY --from=deps /app/node_modules ./node_modules
   COPY --from=build /app/.next ./.next
   COPY --from=build /app/public ./public
   COPY --from=build /app/package.json ./
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

   Adapt for the detected framework — adjust the build output directory, entry command, and base image.

3. **Create `.dockerignore`**

   ```
   node_modules
   .next
   .git
   .env*
   *.md
   ```

4. **Create `docker-compose.yml`** (if the app has dependencies like a database or Redis):

   ```yaml
   services:
     app:
       build: .
       ports:
         - "3000:3000"
       env_file: .env
       depends_on:
         - db
     db:
       image: postgres:16-alpine
       environment:
         POSTGRES_DB: app
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: postgres
       volumes:
         - pgdata:/var/lib/postgresql/data
   volumes:
     pgdata:
   ```

5. **Add npm scripts** (optional)

   ```json
   {
     "docker:build": "docker build -t myapp .",
     "docker:run": "docker compose up"
   }
   ```

## Notes

- Use Alpine-based images to minimize image size.
- Never copy `.env` files into the image — use `env_file` or runtime injection.
- For monorepos, use a `.dockerignore` that excludes sibling packages not needed by the target app.
- Add a `HEALTHCHECK` instruction for production deployments.
