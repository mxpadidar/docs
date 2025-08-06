# git rebase --onto: common scenarios and how to use them

the `git rebase --onto` command is a powerful tool to transplant commits from one base to another. it lets you precisely control which commits to replay and where.

this document summarizes common scenarios where `git rebase --onto` is useful, with commands and visual summaries.

---

## 1. rebase commits from one base to another (standard use case)

**use case:**  
you branched off an old commit, but want to replay your commits on top of a new base branch (e.g., `main` has moved forward).

```bash
git rebase --onto <new-base> <old-base> <branch>
```

- `<old-base>`: the commit before your branch's first commit.
- `<new-base>`: the commit you want to rebase onto.
- `<branch>`: the branch you want to rebase.

**example:**

```bash
git rebase --onto main a feature
```

**visual summary:**

before rebase:

```
main:     a --- b --- c
                   \
feature:            d --- e
```

after rebase:

```
main:     a --- b --- c
                          \
feature:                   d' --- e'
```

---

## 2. cherry-pick a subset of commits (partial rebase)

**use case:**
you want to rebase only a subset of commits from your branch, not the entire history.

```bash
git rebase --onto <new-base> <up-to-commit> <branch>
```

- commits after `<up-to-commit>` up to the tip of `<branch>` will be replayed.

**example:**

```bash
git rebase --onto main c1 feature
```

where commits on `feature` are `c1, c2, c3, c4` and you want to rebase only `c2, c3, c4`.

**visual summary:**

before rebase:

```
main:     a --- b --- c1
                       \
feature:                 c2 --- c3 --- c4
```

after rebase:

```
main:     a --- b --- c1 --- c2' --- c3' --- c4'
```

---

## 3. moving commits off a branch that's being deleted or replaced

**use case:**
you want to move commits from a branch that will be deleted onto another branch.

```bash
git rebase --onto <new-branch> <old-branch-base> <old-branch>
```

**example:**

```bash
git rebase --onto develop feature-base feature
```

**visual summary:**

before rebase:

```
develop:      a --- b --- c
                         \
feature-base:              d
                            \
feature:                    e --- f
```

after rebase:

```
develop:      a --- b --- c --- e' --- f'
feature-base:              d (deleted)
feature:                    (moved commits e, f onto develop)
```

---

## 4. interactive rebase with `--onto`

**use case:**
you want to rebase starting from a certain commit, with the ability to reorder, squash, or edit commits.

```bash
git rebase -i --onto <new-base> <up-to-commit> <branch>
```

**example:**

```bash
git rebase -i --onto main c feature
```

you can then edit the todo list to squash or reorder commits.

**visual summary:**

before:

```
main:     a --- b --- c
                   \
feature:            d --- e --- f
```

during interactive rebase, you choose how to replay `d, e, f`.

after:

```
main:     a --- b --- c
                          \
feature:                   d* --- e* --- f*
```

(\* possibly reordered or squashed)

---

## 5. fixing history after upstream rebases or force pushes

**use case:**
the upstream branch you branched from was force-pushed or rebased, so your branch is based on commits that no longer exist.

```bash
git rebase --onto <new-upstream> <old-upstream-base> <feature-branch>
```

**example:**

```bash
git rebase --onto main old-main-base feature
```

**visual summary:**

before:

```
old-main: a --- b --- c
                   \
feature:            d --- e
```

upstream rebased `main`:

```
main:     a --- b' --- c'
```

after rebase:

```
main:     a --- b' --- c'
                          \
feature:                   d' --- e'
```

---

## 6. reparenting commits onto an unrelated branch

**use case:**
you want to move commits from one branch to a completely different branch, which might not share recent history.

```bash
git rebase --onto <target-branch> <common-ancestor> <source-branch>
```

**example:**

```bash
git rebase --onto experimental main feature
```

**visual summary:**

before:

```
main:        a --- b --- c
feature:              \
                        d --- e
experimental: x --- y --- z
```

after:

```
experimental: x --- y --- z --- d' --- e'
main:        a --- b --- c
```

---

# summary table

| scenario                                        | command template                                               | description                                          |
| ----------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------- |
| move feature commits to new base                | `git rebase --onto new-base old-base feature`                  | rebase feature commits onto new base                 |
| cherry-pick subset of commits                   | `git rebase --onto new-base commit-before-subset branch`       | only rebase selected commits                         |
| move commits off branch being deleted           | `git rebase --onto new-branch old-branch-base old-branch`      | rebase commits onto a different branch               |
| interactive rebase with commit selection        | `git rebase -i --onto new-base old-base branch`                | edit, squash, reorder commits starting from old-base |
| fix history after upstream force-push or rebase | `git rebase --onto new-upstream old-upstream-base feature`     | rebase after upstream history rewrite                |
| reparent commits onto unrelated branch          | `git rebase --onto target-branch common-ancestor experimental` | move commits between unrelated branches              |

---

# notes

- `<old-base>` is the commit _before_ your first commit to rebase.
- if `<branch>` is omitted, git rebases the current branch.
- `git rebase --onto` gives fine-grained control beyond `git rebase <branch>`.
- always resolve conflicts as they appear and use `git rebase --continue`.
- after rebasing published branches, force push with `git push --force-with-lease`.
