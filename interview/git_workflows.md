# Git Workflows — Rebasing vs Merging

Purpose: Practical guidance for choosing between merge commits and rebasing, plus common commands.

## Merge

- Behavior: merges feature branch into target with a merge commit, preserving original commits and branching history.
- Pros: preserves context, easy to trace when branches merged, safe for shared branches.
- Cons: history can be noisy with many merge commits.

Common command:

- git checkout main
- git pull
- git merge --no-ff feature/xyz
- git push

## Rebase

- Behavior: replays commits from feature branch onto tip of main to create linear history.
- Pros: clean, linear history; easier bisecting.
- Cons: rewrites commit hashes — never rebase public/shared branch unless team agrees.
- Good practice: rebase locally before opening PR to keep history tidy.

Common command:

- git checkout feature/xyz
- git fetch origin
- git rebase origin/main
- Resolve conflicts, git rebase --continue
- git push --force-with-lease

## Conflict handling and policies

- Use --force-with-lease to avoid overwriting others' work.
- For long-running branches, prefer merges to preserve integration points.
- Team policy examples:
  - Keep main linear via squash merges or rebased PRs.
  - Use merge commits for release branches to track integrations.

## Recommended workflows

- GitHub Flow: short-lived feature branches, PRs, merge to main when green.
- GitFlow: broader branch model for releases, hotfixes — more structure for large teams.

## Interview prompts

- When would you choose rebase over merge in a team environment?
- Explain force push risks and how --force-with-lease helps.

Quick tips:

- Use graphical history tools (gitk, git log --graph --oneline).
- Protect main branch with required status checks and branch protection rules.
