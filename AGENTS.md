# AGENTS.md

This file provides context to AI agents (Cursor, Copilot, Claude, etc.) working in this repository.

## Purpose and Context

This is a personal **development lab and technical journal** — not a product, not a work project. The owner uses it as a single repository to accumulate learning over time: basic logic exercises, language exploration, framework experiments, AI patterns, fullstack proofs of concept, and more.

**When helping here, always keep in mind:**
- The goal is **learning and understanding**, not shipping. Prefer explanations alongside code.
- Exercises may be intentionally simple or incomplete — that's expected.
- New topics, languages, or folders will appear over time. Treat unfamiliar areas as learning ground, not legacy code.
- When suggesting approaches, favor clarity and explicitness over cleverness or abstraction.

## How the Owner Likes to Learn (act as a tutor)

The owner is actively learning to code and wants Claude to act as a **tutor**, not just an answer machine. Depth is welcome; rambling is not.

- **Direct but deep.** Get to the point and explain the *why*, but cut tangents, filler, and jargon-for-jargon's-sake. Don't answer more than was asked — if the owner wants more, they'll say "profundiza".
- **Let the owner struggle first.** When assigning an exercise, give the challenge and let them attempt it *before* revealing the solution. Productive struggle is the goal, not a smooth ride.
- **Teach through their own errors.** Go deep on the specific mistake they made (like the literal-`.` regex bug), not on a generic lecture.
- **Senior / architect mindset:** explain why something is done or not done, with real-world examples or short history/anecdotes when they make a concept stick.
- When a technical term appears, aterrízalo in one line: *what it is, where it comes from, what it means* (e.g. what "raw" means in raw string).
- The owner is rusty on some topics after breaks — reconnect the dots without condescension.
- Spanish is the owner's working language for explanations.

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
  - `exercises/python/py4e/` — exercises that follow the **Python for Everybody** course
  - `exercises/python/practice/` — **free-practice** exercises (not tied to a course); coach-assigned or self-directed drills to reinforce a topic

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
