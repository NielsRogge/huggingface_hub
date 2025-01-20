<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Authentication

The `huggingface_hub` library allows users to programmatically manage authentication to the Hub. This includes logging in, logging out, switching between tokens, and listing available tokens.

For more details about authentication, check out [this section](../quick-start#authentication).

## login

### login

```python
Login the machine to access the Hub.

The `token` is persisted in cache and set as a git credential. Once done, the machine
is logged in and the access token will be available across all `huggingface_hub`
components. If `token` is not provided, it will be prompted to the user either with
a widget (in a notebook) or via the terminal.

To log in from outside of a script, one can also use `huggingface-cli login` which is
a cli command that wraps [`login`].

<Tip>

[`login`] is a drop-in replacement method for [`notebook_login`] as it wraps and
extends its capabilities.

</Tip>

<Tip>

When the token is not passed, [`login`] will automatically detect if the script runs
in a notebook or not. However, this detection might not be accurate due to the
variety of notebooks that exists nowadays. If that is the case, you can always force
the UI by using [`notebook_login`] or [`interpreter_login`].

</Tip>

Args:
    token (`str`, *optional*):
        User access token to generate from https://huggingface.co/settings/token.
    add_to_git_credential (`bool`, defaults to `False`):
        If `True`, token will be set as git credential. If no git credential helper
        is configured, a warning will be displayed to the user. If `token` is `None`,
        the value of `add_to_git_credential` is ignored and will be prompted again
        to the end user.
    new_session (`bool`, defaults to `True`):
        If `True`, will request a token even if one is already saved on the machine.
    write_permission (`bool`):
        Ignored and deprecated argument.
Raises:
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If an organization token is passed. Only personal account tokens are valid
        to log in.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If token is invalid.
    [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
        If running in a notebook but `ipywidgets` is not installed.
```


## interpreter_login

### interpreter_login

```python
Displays a prompt to log in to the HF website and store the token.

This is equivalent to [`login`] without passing a token when not run in a notebook.
[`interpreter_login`] is useful if you want to force the use of the terminal prompt
instead of a notebook widget.

For more details, see [`login`].

Args:
    new_session (`bool`, defaults to `True`):
        If `True`, will request a token even if one is already saved on the machine.
    write_permission (`bool`):
        Ignored and deprecated argument.
```


## notebook_login

### notebook_login

```python
Displays a widget to log in to the HF website and store the token.

This is equivalent to [`login`] without passing a token when run in a notebook.
[`notebook_login`] is useful if you want to force the use of the notebook widget
instead of a prompt in the terminal.

For more details, see [`login`].

Args:
    new_session (`bool`, defaults to `True`):
        If `True`, will request a token even if one is already saved on the machine.
    write_permission (`bool`):
        Ignored and deprecated argument.
```


## logout

### logout

```python
Logout the machine from the Hub.

Token is deleted from the machine and removed from git credential.

Args:
    token_name (`str`, *optional*):
        Name of the access token to logout from. If `None`, will logout from all saved access tokens.
Raises:
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError):
        If the access token name is not found.
```


## auth_switch

### auth_switch

```python
Switch to a different access token.

Args:
    token_name (`str`):
        Name of the access token to switch to.
    add_to_git_credential (`bool`, defaults to `False`):
        If `True`, token will be set as git credential. If no git credential helper
        is configured, a warning will be displayed to the user. If `token` is `None`,
        the value of `add_to_git_credential` is ignored and will be prompted again
        to the end user.

Raises:
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError):
        If the access token name is not found.
```


## auth_list

### auth_list

```python
List all stored access tokens.
```

