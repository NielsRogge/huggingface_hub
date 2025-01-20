<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Managing local and online repositories

The `Repository` class is a helper class that wraps `git` and `git-lfs` commands. It provides tooling adapted
for managing repositories which can be very large.

It is the recommended tool as soon as any `git` operation is involved, or when collaboration will be a point
of focus with the repository itself.

## The Repository class

### Repository

```python
Helper class to wrap the git and git-lfs commands.

The aim is to facilitate interacting with huggingface.co hosted model or
dataset repos, though not a lot here (if any) is actually specific to
huggingface.co.

<Tip warning={true}>

[`Repository`] is deprecated in favor of the http-based alternatives implemented in
[`HfApi`]. Given its large adoption in legacy code, the complete removal of
[`Repository`] will only happen in release `v1.0`. For more details, please read
https://huggingface.co/docs/huggingface_hub/concepts/git_vs_http.

</Tip>
```

    - __init__
    - current_branch
    - all

## Helper methods

### huggingface_hub.repository.is_git_repo

```python
Check if the folder is the root or part of a git repository

Args:
    folder (`str`):
        The folder in which to run the command.

Returns:
    `bool`: `True` if the repository is part of a repository, `False`
    otherwise.
```


### huggingface_hub.repository.is_local_clone

```python
Check if the folder is a local clone of the remote_url

Args:
    folder (`str` or `Path`):
        The folder in which to run the command.
    remote_url (`str`):
        The url of a git repository.

Returns:
    `bool`: `True` if the repository is a local clone of the remote
    repository specified, `False` otherwise.
```


### huggingface_hub.repository.is_tracked_with_lfs

```python
Check if the file passed is tracked with git-lfs.

Args:
    filename (`str` or `Path`):
        The filename to check.

Returns:
    `bool`: `True` if the file passed is tracked with git-lfs, `False`
    otherwise.
```


### huggingface_hub.repository.is_git_ignored

```python
Check if file is git-ignored. Supports nested .gitignore files.

Args:
    filename (`str` or `Path`):
        The filename to check.

Returns:
    `bool`: `True` if the file passed is ignored by `git`, `False`
    otherwise.
```


### huggingface_hub.repository.files_to_be_staged

```python
Returns a list of filenames that are to be staged.

Args:
    pattern (`str` or `Path`):
        The pattern of filenames to check. Put `.` to get all files.
    folder (`str` or `Path`):
        The folder in which to run the command.

Returns:
    `List[str]`: List of files that are to be staged.
```


### huggingface_hub.repository.is_tracked_upstream

```python
Check if the current checked-out branch is tracked upstream.

Args:
    folder (`str` or `Path`):
        The folder in which to run the command.

Returns:
    `bool`: `True` if the current checked-out branch is tracked upstream,
    `False` otherwise.
```


### huggingface_hub.repository.commits_to_push

```python
    Check the number of commits that would be pushed upstream

    Args:
        folder (`str` or `Path`):
            The folder in which to run the command.
        upstream (`str`, *optional*):
The name of the upstream repository with which the comparison should be
made.

    Returns:
        `int`: Number of commits that would be pushed upstream were a `git
        push` to proceed.
```


## Following asynchronous commands

The `Repository` utility offers several methods which can be launched asynchronously:
- `git_push`
- `git_pull`
- `push_to_hub`
- The `commit` context manager

See below for utilities to manage such asynchronous methods.

### Repository

```python
Helper class to wrap the git and git-lfs commands.

The aim is to facilitate interacting with huggingface.co hosted model or
dataset repos, though not a lot here (if any) is actually specific to
huggingface.co.

<Tip warning={true}>

[`Repository`] is deprecated in favor of the http-based alternatives implemented in
[`HfApi`]. Given its large adoption in legacy code, the complete removal of
[`Repository`] will only happen in release `v1.0`. For more details, please read
https://huggingface.co/docs/huggingface_hub/concepts/git_vs_http.

</Tip>
```

    - commands_failed
    - commands_in_progress
    - wait_for_commands

### huggingface_hub.repository.CommandInProgress

```python
Utility to follow commands launched asynchronously.
```

