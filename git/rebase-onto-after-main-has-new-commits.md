# rebasing a feature branch after `main` has new commits

you created a feature branch (e.g., `feat/xyz`) from `main`. later, the `main`
branch received new commits (possibly via rebase, merge, or direct changes),
so now your `feat/xyz` branch is based on an outdated version of `main`. you
want to move your feature branch commits on top of the latest commits in `main`.

## checkout your feature branch

```bash
git checkout feat/xyz
```

## find the last common commit between your feature branch and the old `main`

```bash
git merge-base feat/xyz main
```

this will return a commit hash (e.g., `abc1234`).

## rebase your feature branch onto the new `main`

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

before `main` received new commits:

```
main:     a --- b --- c
                       \
feat/xyz:               d --- e
```

after `main` is updated (e.g., rebase or new commits):

```
main:     a --- b --- c --- f --- g
```

to rebase `feat/xyz` onto the new `main`:

```bash
git rebase --onto main c
```

resulting history:

```
main:     a --- b --- c --- f --- g
                                   \
feat/xyz:                           d' --- e'
```

## notes

- this method is useful when `main` has changed independently of your feature branch.
- if your branch is public or shared with others, coordinate before force-pushing.
- use `git log --oneline --graph` to visualize your rebase before and after.
