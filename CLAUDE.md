# CLAUDE.md

This file provides guidance for AI assistants (Claude and others) working in this repository.

## Project Overview

**criativos-growth** is a repository for creatives (content, assets, campaigns) targeting the Growth vertical clients.

- **Language/Description**: "Criativos para clientes da vertical de Growth" (Creatives for Growth vertical clients)
- **Status**: Early-stage — repository initialized, no tech stack configured yet

## Repository State

As of the latest analysis, this is a newly initialized repository containing:

```
criativos-growth/
└── README.md
```

No language, framework, database, or tooling has been configured yet. When the stack is defined, update this file accordingly.

## Git Workflow

### Branches

- `master` — main/stable branch
- Feature and AI-assisted work branches use the pattern `claude/<descriptor>-<session-id>`

### Commit Conventions

Use clear, descriptive commit messages in imperative form:

```
Add user authentication flow
Fix broken image asset pipeline
Update campaign template for Q2
```

Avoid vague messages like "fix stuff" or "updates".

### Push Instructions

Always push with upstream tracking:

```bash
git push -u origin <branch-name>
```

Branch names for AI-assisted work must start with `claude/` and end with the session ID.

## Development Setup

> **Note**: No tech stack is defined yet. Update this section once the stack is chosen and initialized.

Likely steps once configured:

1. Install dependencies (e.g., `npm install`, `pip install -r requirements.txt`)
2. Copy environment variables: `cp .env.example .env`
3. Configure any required API keys or credentials
4. Run the development server

## Available Commands

> **Note**: No scripts are defined yet. Populate this section once a `package.json`, `Makefile`, or equivalent is added.

Expected commands to document here:
- Build / compile
- Dev server / watch mode
- Lint and format
- Run tests

## Testing

> **Note**: No testing framework is configured. When added, document:
> - Test runner and command
> - Where tests live (`tests/`, `__tests__/`, `spec/`, etc.)
> - How to run a single test vs. the full suite
> - Coverage reporting

## Code Conventions

Since no code exists yet, these are recommended conventions to adopt:

- Keep related assets and code co-located by feature or campaign
- Use consistent naming: `kebab-case` for files, descriptive folder names
- Avoid committing generated files, secrets, or large binaries — add them to `.gitignore`
- Prefer small, focused commits over large omnibus changes

## Environment Variables

> No `.env` or `.env.example` exists yet. When environment variables are needed:
> - Create `.env.example` with all required keys (no real values)
> - Add `.env` to `.gitignore`
> - Document each variable's purpose here

## For AI Assistants

- This repo has minimal existing code — do not assume any framework or language is in use until verified
- Before writing code, check whether relevant files exist using Glob or Read tools
- Commit and push changes to the designated `claude/` branch — never push to `master` without explicit permission
- When adding new tooling or dependencies, document them in this file
- Keep changes minimal and focused on the task at hand — avoid over-engineering
