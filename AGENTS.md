# AGENTS.md

This file provides context to AI agents (Cursor, Copilot, Claude, etc.) working in this repository.

## Purpose and Context

This is a personal **development lab and technical journal** — not a product, not a work project. The owner uses it as a single repository to accumulate learning over time: basic logic exercises, language exploration, framework experiments, AI patterns, fullstack proofs of concept, and more.

**When helping here, always keep in mind:**
- The goal is **learning and understanding**, not shipping. Prefer explanations alongside code.
- Exercises may be intentionally simple or incomplete — that's expected.
- New topics, languages, or folders will appear over time. Treat unfamiliar areas as learning ground, not legacy code.
- When suggesting approaches, favor clarity and explicitness over cleverness or abstraction.

## Monorepo Structure

This is a **pnpm + Turborepo** monorepo. Workspaces are defined in `pnpm-workspace.yaml`:

- `apps/web` — Next.js app (port 3000)
- `apps/docs` — Next.js app (port 3001)
- `packages/ui` — Shared React component library (`@repo/ui`), imported as `@repo/ui/*`
- `packages/ai-client` — LLM client wrapper (`@devlab/ai-client`), wraps OpenAI SDK with a `createClient(provider, options)` factory
- `packages/eslint-config` — Shared ESLint config (`@repo/eslint-config`)
- `packages/typescript-config` — Shared `tsconfig.json` bases (`@repo/typescript-config`)
- `exercises/javascript/*` — JS/Node.js standalone exercises (each is its own workspace package)
- `exercises/python/` — Python exercises (not part of the pnpm workspace; run with `python` directly)

## Commands

All commands run from the repo root unless otherwise noted.

```sh
pnpm install          # install all dependencies
pnpm build            # build all packages/apps via Turborepo
pnpm dev              # start all dev servers
pnpm lint             # lint all packages
pnpm check-types      # type-check all packages
pnpm format           # prettier format all TS/TSX/MD files
```

Filter to a specific package with Turborepo's `--filter` flag:

```sh
pnpm turbo dev --filter=web
pnpm turbo build --filter=@devlab/ai-client
pnpm turbo lint --filter=docs
```

Run a JS exercise directly (they use ESM):

```sh
cd exercises/javascript/llm-api
node openai-test.js
```

Run a Python exercise:

```sh
python exercises/python/py4e/00-hello-world.py
```

## Key Architectural Notes

### `@devlab/ai-client`

Located in `packages/ai-client/`. Exports a single `createClient(provider, options)` function that returns a provider-specific SDK instance. Currently only supports `"openai"`, returning a raw `OpenAI` instance. Compiled to `dist/` via `tsc`.

Consumer code (e.g., `exercises/javascript/llm-api/openai-test.js`) loads API keys from `.env.local` at the repo root using `dotenv`.

### Shared UI (`@repo/ui`)

Exports React components directly from source (`"exports": { "./*": "./src/*.tsx" }`), so no build step is needed. Add new components as individual `.tsx` files in `packages/ui/src/`. Generate a component scaffold with:

```sh
cd packages/ui && pnpm generate:component
```

### Environment Variables

The repo root `.env.local` is the expected location for secrets (e.g., `OPENAI_API_KEY`). This file is not committed.
