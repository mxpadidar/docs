# Git Branching Guide

## Overview

Branching allows you to diverge from the main line of development and continue to do work without messing with that main line. By following a consistent strategy and using clear conventions, you can manage even the most complex projects with ease.

A Git branch is essentially a lightweight movable pointer to a commit. The default branch in Git is usually called `main` or `master`. When you create a new branch, you're creating a new pointer you can move around while isolating your changes.

Branches allow for:

- Parallel development
- Feature isolation
- Safer experimentation

This document covers:

- [Types of branches](#types-of-branches)
- [Branching workflows](#branching-workflows)
- [Feature branch workflow](#feature-branch-workflow)
- [Best practices](#best-practices)

## Types of Branches

### Main Branches

- `main` (or `master`): The production-ready branch.
- `develop`: Often used in Git Flow as the integration branch for features.

### Supporting Branches

- `feature/*`: Used to develop new features (e.g., `feature/login-page`)
- `bugfix/*`: Used to fix non-critical bugs
- `hotfix/*`: Urgent fixes to `main`
- `release/*`: For final polishing before merging to `main`

## Branching Workflows

### Git Flow

A strict branching model with the following:

- `main`: production
- `develop`: integration
- `feature/`, `release/`, `hotfix/` branches for tasks

**Pros:** Clear structure, good for large teams.

**Cons:** Heavyweight for small teams or solo devs.

### GitHub Flow

A lightweight workflow:

- `main` as the only permanent branch
- New branches from `main`
- Use Pull Requests to merge

**Pros:** Simple, fast, ideal for CI/CD

**Cons:** Less structured, can get messy without discipline

### Trunk-Based Development

- Only one long-lived branch: `main`
- Short-lived branches merged back daily

**Pros:** Encourages CI, rapid integration

**Cons:** Requires strict testing and discipline

## Feature Branch Workflow

The **Feature Branch Workflow** is a common Git branching strategy where each new feature is developed in its own dedicated branch, separate from the `main` or `develop` branches.

### Why Use Feature Branches?

- Isolate work from other features
- Improve collaboration by avoiding conflicts
- Enable code reviews via pull requests
- Maintain a clean and stable `main` branch

### Naming Convention

Use consistent and descriptive branch names:

```
feature/<feature-name>
```

Examples:

- `feature/login-page`
- `feature/payment-integration`
- `feature/user-profile-edit`

### Workflow Steps

#### 1. Create the Feature Branch

Branch off from `develop` or `main`:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-new-feature
```

#### 2. Work on the Feature

Make changes and commit regularly:

```bash
git add .
git commit -m "Add basic layout for login page"
```

#### 3. Keep Branch Up-to-Date

Rebase with the target branch to avoid merge conflicts later:

```bash
git fetch origin
git rebase origin/develop
```

Or merge (less clean history):

```bash
git merge origin/develop
```

#### 4. Push to Remote

Push your branch and track it:

```bash
git push --set-upstream origin feature/my-new-feature
```

#### 5. Open a Pull Request

Open a PR (Pull Request) on GitHub, GitLab, etc., targeting the correct base branch (`main` or `develop`).

Request reviews and wait for approvals.

#### 6. Squash and Merge

If your team prefers a clean history, squash commits:

```bash
git rebase -i origin/develop
```

Then merge via the platform or command line:

```bash
git checkout develop
git merge feature/my-new-feature
```

#### 7. Clean Up

After merging:

```bash
git branch -d feature/my-new-feature
git push origin --delete feature/my-new-feature
```

### Tips

- Always pull the latest changes before branching.
- Keep feature branches focused and small.
- Use draft PRs to get early feedback.
- Add meaningful commit messages and descriptions.

---

## Best Practices

- Use clear, consistent naming (e.g., `feature/user-auth`)
- Branch from the correct base (`develop` or `main`)
- Keep branches short-lived and small
- Rebase before merging (unless using merge commits intentionally)
- Delete merged branches
- Use protected branches for `main`
