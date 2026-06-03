# AutoGPT AGENTS.md Content

## Source
- **Repository**: https://github.com/Significant-Gravitas/AutoGPT
- **File**: AGENTS.md
- **Stars**: 185k

## Content Summary

### Purpose
This is a contribution guide for coding agents when updating the autogpt_platform folder.

### Directory Structure
```
autogpt_platform/
├── backend     - FastAPI based backend service
├── autogpt_libs - Shared Python libraries
├── frontend    - Next.js + Typescript frontend
├── docker-compose.yml - development stack
```

### Code Style Guidelines

#### Python Code
- Format with: `poetry run format`

#### Frontend Code
- Format with: `pnpm format`

### Frontend Guidelines

1. **Page Structure**: Create in `src/app/(platform)/feature-name/page.tsx`
   - Add `usePageName.ts` hook for logic
   - Put sub-components in local `components/` folder

2. **Component Structure**: ComponentName/ComponentName.tsx + useComponentName.ts + helpers.ts
   - Use design system components from `src/components/` (atoms, molecules, organisms)
   - Never use `src/components/__legacy__/*`

3. **Data Fetching**: Use generated API hooks from `@/app/api/__generated__/endpoints/`
   - Regenerate with `pnpm generate:api`
   - Pattern: `use{Method}{Version}{OperationName}`

4. **Styling**: Tailwind CSS only, use design tokens, Phosphor Icons only

5. **Testing Strategy**:
   - Integration tests (Vitest + RTL + MSW) ~90%, page-level - DEFAULT
   - Playwright for E2E critical flows
   - Storybook for design system components
   - See `autogpt_platform/frontend/TESTING.md`

6. **Code Conventions**:
   - Function declarations (not arrow functions) for components/handlers
   - Component props should be `interface Props { ... }` (not exported) unless needed outside component
   - Separate render logic from business logic
   - Colocate state when possible; avoid large components
   - Use local `/components` folder next to parent component
   - Avoid large hooks; abstract logic into `helpers.ts` when sensible
   - No barrel files or `index.ts` re-exports
   - Avoid comments unless code is very complex
   - Do not use `useCallback` or `useMemo` unless asked to optimize
   - Never type with `any`; use `unknown` if needed

### Testing Commands

- **Backend**: `poetry run test` (runs pytest with docker based postgres + prisma)
- **Frontend unit tests**: `pnpm test:unit` (Vitest + RTL + MSW)
- **Frontend E2E tests**: `pnpm test` or `pnpm test-ui` (Playwright)

### Pull Request Guidelines

- Use template in `.github/PULL_REQUEST_TEMPLATE.md`
- Rely on pre-commit checks for linting and formatting
- Fill out **Changes** section and checklist
- Use conventional commit titles with scope (e.g., `feat(frontend): add feature`)
- Keep out-of-scope changes under 20% of PR
- Ensure PR descriptions are complete
- For changes touching `data/*.py`, validate user ID checks
- If adding protected frontend routes, update `frontend/lib/supabase/middleware.ts`
- Use linear ticket branch structure if given

### Commit Types
- feat, fix, refactor, ci, dx (developer experience)

### Scopes
- platform, platform/library, platform/marketplace, backend, backend/executor, frontend, frontend/library, frontend/marketplace, blocks

## Best Practices Extracted

1. **Clear directory organization** - separate concerns by functionality
2. **Component naming conventions** - consistent file naming
3. **Hook-based logic extraction** - separate business logic from UI
4. **Generated API clients** - type-safe API access
5. **Testing分层** - integration vs E2E
6. **Code formatting enforcement** - automated style checks
7. **Conventional commits** - standardized commit messages

---
*Extracted from AutoGPT AGENTS.md*
