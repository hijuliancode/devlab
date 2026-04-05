# devlab

A personal monorepo that works as a technical journal and development lab. The idea is to have a single place to accumulate exercises, experiments, and proofs of concept over time — from basic logic scripts in Python to advanced AI patterns, fullstack apps, architectures, and whatever comes up along the way.

This is not a product project or meant for publication. It's a space for learning, remembering, and keeping evidence of what has been explored.

## Structure

```
apps/          → applications (Next.js, etc.)
packages/      → shared packages (ui, ai-client, configs)
exercises/
  javascript/  → JS/Node.js scripts and exercises
  python/      → Python scripts and exercises
```

## Stack

- **pnpm** as package manager
- **Turborepo** for task orchestration across the monorepo
- **TypeScript** for all JS/Node work
- **Next.js** for fullstack experiments

## Commands

```sh
pnpm install                          # install all dependencies
pnpm dev                              # start all dev servers
pnpm build                            # build all packages and apps
pnpm lint                             # lint everything
pnpm check-types                      # type-check everything
pnpm turbo dev --filter=web           # dev a specific package only
```

Standalone exercises run directly:

```sh
node exercises/javascript/llm-api/openai-test.js
python exercises/python/py4e/00-hello-world.py
```
