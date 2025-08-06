# Git Commit Guide

## Overview

Effective commits are essential for collaboration, code clarity, and project tracking. Good commit practices improve the understanding of a project’s history and make it easier to review, debug, and revert code when needed.

This document covers:

- [Why commit practices matter](#why-commit-practices-matter)
- [Writing good commit messages](#writing-good-commit-messages)
- [Commit message conventions](#commit-message-conventions)
- [Commit frequency and scope](#commit-frequency-and-scope)
- [Summary](#summary)

## Why commit practices matter:

- Helps others (and your future self) understand why changes were made
- Makes code review and debugging easier
- Enables better project automation (e.g., changelogs, semantic versioning)
- Maintains clean project history

## Writing Good Commit Messages

A good commit message should be:

- **Concise**: Focused and to the point
- **Descriptive**: Explains the _why_, not just the _what_
- **Formatted** properly:

```
type(scope): short summary

optional longer description
```

### Example:

```
feat(auth): add JWT-based login system

Implements secure login using JWT and updates login endpoint to support token response.
```

## Commit Message Conventions

### Conventional Commits

A standardized format for writing commit messages. Structure:

```
type(scope?): description
```

#### Common `type` values:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Maintenance tasks

### Scopes

Scope is optional but helpful to narrow down the affected part of the code (e.g., `auth`, `ui`, `api`, `db`).

## Commit Frequency and Scope

- Commit **early and often** during development
- Each commit should represent a single logical change
- Avoid large, unrelated changes in one commit
- Squash trivial commits before merging (if needed)

## Summary

Clear, consistent commit messages help everyone. Adopt conventions like Conventional Commits, commit frequently with meaningful messages, and leverage tools to automate checks and releases.
