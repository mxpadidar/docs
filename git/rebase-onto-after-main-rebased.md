# rebasing a feature branch after `main` has been rebased

you created a feature branch (e.g., `feat/xyz`) from `main`.  
later, `main` was **rebased** (e.g., to clean up history or squash fixups), which changed the commit hashes.

now, your feature branch is based on outdated commits that no longer exist in `main`.

you want to rebase your feature branch onto the **new** `main` branch.

## checkout your feature branch

```bash
git checkout feat/xyz
```

## find the last common commit between the old `main` and your feature branch

```bash
git merge-base feat/xyz main
```

this will return a commit hash (e.g., `abc1234`).

## rebase your feature branch onto the updated `main`

```bash
git rebase --onto main abc1234
```

**explanation**:
this tells git:

> “take all commits in `feat/xyz` that came after `abc1234`, and replay them on top of the current `main`.”

## resolve any conflicts

if there are conflicts, git will pause and allow you to resolve them.
after resolving, continue the rebase:

```bash
git rebase --continue
```

to abort the rebase if needed:

```bash
git rebase --abort
```

## force-push the updated branch

since the commit history has changed, you need to force-push:

```bash
git push --force-with-lease origin feat/xyz
```

## visual summary

before rebase:

```
main:     a --- b --- c
                       \
feat/xyz:               d --- e
```

after `main` is rebased:

```
main:     a --- b' --- c'
```

to rebase `feat/xyz` onto the new `main`:

```bash
git rebase --onto main c
```

resulting history:

```
main:     a --- b' --- c'
                        \
feat/xyz:                d' --- e'
```

## notes

- use this pattern whenever your base branch (e.g., `main`) has been rebased.
- avoid rebasing shared branches unless your team agrees on it.
- you can use `--interactive` (`-i`) and `--autosquash` to clean up your commits while rebasing.
