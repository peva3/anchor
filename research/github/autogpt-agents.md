# AutoGPT Platform Contribution Guide

This guide provides context for coding agents when updating the **autogpt_platform** folder.

## Directory Overview

- `autogpt_platform/backend` - FastAPI based backend service
- `autogpt_platform/autogpt_libs` - Shared Python libraries
- `autogpt_platform/frontend` - Next.js + Typescript frontend
- `autogpt_platform/docker-compose.yml` - development stack

## Code Style

- Format Python code with `poetry run format`
- Format frontend code using `pnpm format`

## Frontend Guidelines

1. **Pages**: Create in `src/app/(platform)/feature-name/page.tsx`
2. **Components**: Structure as `ComponentName/ComponentName.tsx` + `useComponentName.ts` + `helpers.ts`
3. **Data fetching**: Use generated API hooks from `@/app/api/__generated__/endpoints/`
4. **Styling**: Tailwind CSS only, use design tokens, Phosphor Icons only
5. **Testing**: Integration tests (Vitest + RTL + MSW) ~90%, Playwright for E2E
6. **Code conventions**: Function declarations for components/handlers

## Backend

- Uses FastAPI
- Testing: `poetry run test` (pytest with docker based postgres + prisma)

## Pull Requests

- Use the template in `.github/PULL_REQUEST_TEMPLATE.md`
- Follow conventional commit messages
- Fill out **Changes** section and checklist
- Keep out-of-scope changes under 20% of the PR

---

Source: https://github.com/Significant-Gravitas/AutoGPT
