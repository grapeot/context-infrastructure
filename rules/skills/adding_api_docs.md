## 元数据

- **类型**: Workflow
- **分类**: Documentation
- **适用场景**: Generate OpenAPI/Swagger documentation for an API, including endpoint schemas, request/response types, and interactive docs UI.
- **上游来源**: [adding-api-docs](https://github.com/spencerpauly/awesome-cursor-skills/tree/main/resources/adding-api-docs)
- **user-invocable**: —
- **导入日期**: 2026-06-26

---

# Add API Documentation (OpenAPI)

Use this skill when the user asks to add API docs, Swagger, OpenAPI spec, or generate endpoint documentation.

## Steps

1. **Detect the API framework** — check for Express, Fastify, Next.js API routes, Hono, Django REST Framework, FastAPI, etc.

2. **For Node.js/Express** — install `swagger-jsdoc` and `swagger-ui-express`:

   ```bash
   npm install swagger-jsdoc swagger-ui-express
   npm install -D @types/swagger-jsdoc @types/swagger-ui-express
   ```

   Create the OpenAPI spec from JSDoc annotations on route handlers:

   ```ts
   /**
    * @openapi
    * /api/users:
    *   get:
    *     summary: List all users
    *     responses:
    *       200:
    *         description: A list of users
    */
   ```

3. **For Next.js API routes** — create an `openapi.json` file manually or use `next-swagger-doc` to generate from route handlers. Serve the spec at `/api/docs`.

4. **For FastAPI (Python)** — docs are built-in at `/docs` (Swagger UI) and `/redoc`. Ensure Pydantic models are used for request/response types so schemas are auto-generated.

5. **Add interactive docs UI** — serve Swagger UI at a `/docs` route, or use Scalar/Redoc for a modern alternative:

   ```bash
   npm install @scalar/express-api-reference
   ```

6. **Define schemas** — create Zod schemas (or JSON Schema) for request bodies and responses, then reference them in the OpenAPI spec. For TypeScript projects, use `zod-to-openapi` to generate schemas from existing Zod validators.

7. **Add authentication documentation** — document the auth scheme (Bearer token, API key, OAuth2) in the OpenAPI `securitySchemes` section.

## Notes

- Keep the spec in sync with the actual API — generate from code when possible rather than maintaining a separate YAML file.
- Add example values to schemas for better developer experience.
- Version the API docs alongside the code.
