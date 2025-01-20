<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Utilities

## Configure logging

The `huggingface_hub` package exposes a `logging` utility to control the logging level of the package itself.
You can import it as such:

```py
from huggingface_hub import logging
```

Then, you may define the verbosity in order to update the amount of logs you'll see:

```python
from huggingface_hub import logging

logging.set_verbosity_error()
logging.set_verbosity_warning()
logging.set_verbosity_info()
logging.set_verbosity_debug()

logging.set_verbosity(...)
```

The levels should be understood as follows:

- `error`: only show critical logs about usage which may result in an error or unexpected behavior.
- `warning`: show logs that aren't critical but usage may result in unintended behavior.
  Additionally, important informative logs may be shown.
- `info`: show most logs, including some verbose logging regarding what is happening under the hood.
  If something is behaving in an unexpected manner, we recommend switching the verbosity level to this in order
  to get more information.
- `debug`: show all logs, including some internal logs which may be used to track exactly what's happening
  under the hood.

### logging.get_verbosity

Error fetching docstring for logging.get_verbosity: module 'logging' has no attribute 'get_verbosity'

### logging.set_verbosity

Error fetching docstring for logging.set_verbosity: module 'logging' has no attribute 'set_verbosity'

### logging.set_verbosity_info

Error fetching docstring for logging.set_verbosity_info: module 'logging' has no attribute 'set_verbosity_info'

### logging.set_verbosity_debug

Error fetching docstring for logging.set_verbosity_debug: module 'logging' has no attribute 'set_verbosity_debug'

### logging.set_verbosity_warning

Error fetching docstring for logging.set_verbosity_warning: module 'logging' has no attribute 'set_verbosity_warning'

### logging.set_verbosity_error

Error fetching docstring for logging.set_verbosity_error: module 'logging' has no attribute 'set_verbosity_error'

### logging.disable_propagation

Error fetching docstring for logging.disable_propagation: module 'logging' has no attribute 'disable_propagation'

### logging.enable_propagation

Error fetching docstring for logging.enable_propagation: module 'logging' has no attribute 'enable_propagation'


### Repo-specific helper methods

The methods exposed below are relevant when modifying modules from the `huggingface_hub` library itself.
Using these shouldn't be necessary if you use `huggingface_hub` and you don't modify them.

### logging.get_logger

Error fetching docstring for logging.get_logger: module 'logging' has no attribute 'get_logger'


## Configure progress bars

Progress bars are a useful tool to display information to the user while a long-running task is being executed (e.g.
when downloading or uploading files). `huggingface_hub` exposes a [`~utils.tqdm`] wrapper to display progress bars in a
consistent way across the library.

By default, progress bars are enabled. You can disable them globally by setting `HF_HUB_DISABLE_PROGRESS_BARS`
environment variable. You can also enable/disable them using [`~utils.enable_progress_bars`] and
[`~utils.disable_progress_bars`]. If set, the environment variable has priority on the helpers.

```py
>>> from huggingface_hub import snapshot_download
>>> from huggingface_hub.utils import are_progress_bars_disabled, disable_progress_bars, enable_progress_bars

>>> # Disable progress bars globally
>>> disable_progress_bars()

>>> # Progress bar will not be shown !
>>> snapshot_download("gpt2")

>>> are_progress_bars_disabled()
True

>>> # Re-enable progress bars globally
>>> enable_progress_bars()
```

### Group-specific control of progress bars

You can also enable or disable progress bars for specific groups. This allows you to manage progress bar visibility more granularly within different parts of your application or library. When a progress bar is disabled for a group, all subgroups under it are also affected unless explicitly overridden.

```py
# Disable progress bars for a specific group
>>> disable_progress_bars("peft.foo")
>>> assert not are_progress_bars_disabled("peft")
>>> assert not are_progress_bars_disabled("peft.something")
>>> assert are_progress_bars_disabled("peft.foo")
>>> assert are_progress_bars_disabled("peft.foo.bar")

# Re-enable progress bars for a subgroup
>>> enable_progress_bars("peft.foo.bar")
>>> assert are_progress_bars_disabled("peft.foo")
>>> assert not are_progress_bars_disabled("peft.foo.bar")

# Use groups with tqdm
# No progress bar for `name="peft.foo"`
>>> for _ in tqdm(range(5), name="peft.foo"):
...     pass

# Progress bar will be shown for `name="peft.foo.bar"`
>>> for _ in tqdm(range(5), name="peft.foo.bar"):
...     pass
100%|███████████████████████████████████████| 5/5 [00:00<00:00, 117817.53it/s]
```

### are_progress_bars_disabled

### huggingface_hub.utils.are_progress_bars_disabled

```python
Check if progress bars are disabled globally or for a specific group.

This function returns whether progress bars are disabled for a given group or globally.
It checks the `HF_HUB_DISABLE_PROGRESS_BARS` environment variable first, then the programmatic
settings.

Args:
    name (`str`, *optional*):
        The group name to check; if None, checks the global setting.

Returns:
    `bool`: True if progress bars are disabled, False otherwise.
```


### disable_progress_bars

### huggingface_hub.utils.disable_progress_bars

```python
Disable progress bars either globally or for a specified group.

This function updates the state of progress bars based on a group name.
If no group name is provided, all progress bars are disabled. The operation
respects the `HF_HUB_DISABLE_PROGRESS_BARS` environment variable's setting.

Args:
    name (`str`, *optional*):
        The name of the group for which to disable the progress bars. If None,
        progress bars are disabled globally.

Raises:
    Warning: If the environment variable precludes changes.
```


### enable_progress_bars

### huggingface_hub.utils.enable_progress_bars

```python
Enable progress bars either globally or for a specified group.

This function sets the progress bars to enabled for the specified group or globally
if no group is specified. The operation is subject to the `HF_HUB_DISABLE_PROGRESS_BARS`
environment setting.

Args:
    name (`str`, *optional*):
        The name of the group for which to enable the progress bars. If None,
        progress bars are enabled globally.

Raises:
    Warning: If the environment variable precludes changes.
```


## Configure HTTP backend

In some environments, you might want to configure how HTTP calls are made, for example if you are using a proxy.
`huggingface_hub` let you configure this globally using [`configure_http_backend`]. All requests made to the Hub will
then use your settings. Under the hood, `huggingface_hub` uses `requests.Session` so you might want to refer to the
[`requests` documentation](https://requests.readthedocs.io/en/latest/user/advanced) to learn more about the available
parameters.

Since `requests.Session` is not guaranteed to be thread-safe, `huggingface_hub` creates one session instance per thread.
Using sessions allows us to keep the connection open between HTTP calls and ultimately save time. If you are
integrating `huggingface_hub` in a third-party library and wants to make a custom call to the Hub, use [`get_session`]
to get a Session configured by your users (i.e. replace any `requests.get(...)` call by `get_session().get(...)`).

### configure_http_backend

```python
Configure the HTTP backend by providing a `backend_factory`. Any HTTP calls made by `huggingface_hub` will use a
Session object instantiated by this factory. This can be useful if you are running your scripts in a specific
environment requiring custom configuration (e.g. custom proxy or certifications).

Use [`get_session`] to get a configured Session. Since `requests.Session` is not guaranteed to be thread-safe,
`huggingface_hub` creates 1 Session instance per thread. They are all instantiated using the same `backend_factory`
set in [`configure_http_backend`]. A LRU cache is used to cache the created sessions (and connections) between
calls. Max size is 128 to avoid memory leaks if thousands of threads are spawned.

See [this issue](https://github.com/psf/requests/issues/2766) to know more about thread-safety in `requests`.

Example:
```py
import requests
from huggingface_hub import configure_http_backend, get_session

# Create a factory function that returns a Session with configured proxies
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.proxies = {"http": "http://10.10.1.10:3128", "https": "https://10.10.1.11:1080"}
    return session

# Set it as the default session factory
configure_http_backend(backend_factory=backend_factory)

# In practice, this is mostly done internally in `huggingface_hub`
session = get_session()
```
```


### get_session

```python
Get a `requests.Session` object, using the session factory from the user.

Use [`get_session`] to get a configured Session. Since `requests.Session` is not guaranteed to be thread-safe,
`huggingface_hub` creates 1 Session instance per thread. They are all instantiated using the same `backend_factory`
set in [`configure_http_backend`]. A LRU cache is used to cache the created sessions (and connections) between
calls. Max size is 128 to avoid memory leaks if thousands of threads are spawned.

See [this issue](https://github.com/psf/requests/issues/2766) to know more about thread-safety in `requests`.

Example:
```py
import requests
from huggingface_hub import configure_http_backend, get_session

# Create a factory function that returns a Session with configured proxies
def backend_factory() -> requests.Session:
    session = requests.Session()
    session.proxies = {"http": "http://10.10.1.10:3128", "https": "https://10.10.1.11:1080"}
    return session

# Set it as the default session factory
configure_http_backend(backend_factory=backend_factory)

# In practice, this is mostly done internally in `huggingface_hub`
session = get_session()
```
```



## Handle HTTP errors

`huggingface_hub` defines its own HTTP errors to refine the `HTTPError` raised by
`requests` with additional information sent back by the server.

### Raise for status

[`~utils.hf_raise_for_status`] is meant to be the central method to "raise for status" from any
request made to the Hub. It wraps the base `requests.raise_for_status` to provide
additional information. Any `HTTPError` thrown is converted into a `HfHubHTTPError`.

```py
import requests
from huggingface_hub.utils import hf_raise_for_status, HfHubHTTPError

response = requests.post(...)
try:
    hf_raise_for_status(response)
except HfHubHTTPError as e:
    print(str(e)) # formatted message
    e.request_id, e.server_message # details returned by server

    # Complete the error message with additional information once it's raised
    e.append_to_message("\n`create_commit` expects the repository to exist.")
    raise
```

### huggingface_hub.utils.hf_raise_for_status

```python
    Internal version of `response.raise_for_status()` that will refine a
    potential HTTPError. Raised exception will be an instance of `HfHubHTTPError`.

    This helper is meant to be the unique method to raise_for_status when making a call
    to the Hugging Face Hub.


    Example:
    ```py
        import requests
        from huggingface_hub.utils import get_session, hf_raise_for_status, HfHubHTTPError

        response = get_session().post(...)
        try:
            hf_raise_for_status(response)
        except HfHubHTTPError as e:
            print(str(e)) # formatted message
            e.request_id, e.server_message # details returned by server

            # Complete the error message with additional information once it's raised
            e.append_to_message("
`create_commit` expects the repository to exist.")
            raise
    ```

    Args:
        response (`Response`):
            Response from the server.
        endpoint_name (`str`, *optional*):
            Name of the endpoint that has been called. If provided, the error message
            will be more complete.

    <Tip warning={true}>

    Raises when the request has failed:

        - [`~utils.RepositoryNotFoundError`]
            If the repository to download from cannot be found. This may be because it
            doesn't exist, because `repo_type` is not set correctly, or because the repo
            is `private` and you do not have access.
        - [`~utils.GatedRepoError`]
            If the repository exists but is gated and the user is not on the authorized
            list.
        - [`~utils.RevisionNotFoundError`]
            If the repository exists but the revision couldn't be find.
        - [`~utils.EntryNotFoundError`]
            If the repository exists but the entry (e.g. the requested file) couldn't be
            find.
        - [`~utils.BadRequestError`]
            If request failed with a HTTP 400 BadRequest error.
        - [`~utils.HfHubHTTPError`]
            If request failed for a reason not listed above.

    </Tip>
    
```


### HTTP errors

Here is a list of HTTP errors thrown in `huggingface_hub`.

#### HfHubHTTPError

`HfHubHTTPError` is the parent class for any HF Hub HTTP error. It takes care of parsing
the server response and format the error message to provide as much information to the
user as possible.

### huggingface_hub.utils.HfHubHTTPError

```python
    HTTPError to inherit from for any custom HTTP Error raised in HF Hub.

    Any HTTPError is converted at least into a `HfHubHTTPError`. If some information is
    sent back by the server, it will be added to the error message.

    Added details:
    - Request id from "X-Request-Id" header if exists. If not, fallback to "X-Amzn-Trace-Id" header if exists.
    - Server error message from the header "X-Error-Message".
    - Server error message if we can found one in the response body.

    Example:
    ```py
        import requests
        from huggingface_hub.utils import get_session, hf_raise_for_status, HfHubHTTPError

        response = get_session().post(...)
        try:
            hf_raise_for_status(response)
        except HfHubHTTPError as e:
            print(str(e)) # formatted message
            e.request_id, e.server_message # details returned by server

            # Complete the error message with additional information once it's raised
            e.append_to_message("
`create_commit` expects the repository to exist.")
            raise
    ```
    
```


#### RepositoryNotFoundError

### huggingface_hub.utils.RepositoryNotFoundError

```python
Raised when trying to access a hf.co URL with an invalid repository name, or
with a private repo name the user does not have access to.

Example:

```py
>>> from huggingface_hub import model_info
>>> model_info("<non_existent_repository>")
(...)
huggingface_hub.utils._errors.RepositoryNotFoundError: 401 Client Error. (Request ID: PvMw_VjBMjVdMz53WKIzP)

Repository Not Found for url: https://huggingface.co/api/models/%3Cnon_existent_repository%3E.
Please make sure you specified the correct `repo_id` and `repo_type`.
If the repo is private, make sure you are authenticated.
Invalid username or password.
```
```


#### GatedRepoError

### huggingface_hub.utils.GatedRepoError

```python
Raised when trying to access a gated repository for which the user is not on the
authorized list.

Note: derives from `RepositoryNotFoundError` to ensure backward compatibility.

Example:

```py
>>> from huggingface_hub import model_info
>>> model_info("<gated_repository>")
(...)
huggingface_hub.utils._errors.GatedRepoError: 403 Client Error. (Request ID: ViT1Bf7O_026LGSQuVqfa)

Cannot access gated repo for url https://huggingface.co/api/models/ardent-figment/gated-model.
Access to model ardent-figment/gated-model is restricted and you are not in the authorized list.
Visit https://huggingface.co/ardent-figment/gated-model to ask for access.
```
```


#### RevisionNotFoundError

### huggingface_hub.utils.RevisionNotFoundError

```python
Raised when trying to access a hf.co URL with a valid repository but an invalid
revision.

Example:

```py
>>> from huggingface_hub import hf_hub_download
>>> hf_hub_download('bert-base-cased', 'config.json', revision='<non-existent-revision>')
(...)
huggingface_hub.utils._errors.RevisionNotFoundError: 404 Client Error. (Request ID: Mwhe_c3Kt650GcdKEFomX)

Revision Not Found for url: https://huggingface.co/bert-base-cased/resolve/%3Cnon-existent-revision%3E/config.json.
```
```


#### EntryNotFoundError

### huggingface_hub.utils.EntryNotFoundError

```python
Raised when trying to access a hf.co URL with a valid repository and revision
but an invalid filename.

Example:

```py
>>> from huggingface_hub import hf_hub_download
>>> hf_hub_download('bert-base-cased', '<non-existent-file>')
(...)
huggingface_hub.utils._errors.EntryNotFoundError: 404 Client Error. (Request ID: 53pNl6M0MxsnG5Sw8JA6x)

Entry Not Found for url: https://huggingface.co/bert-base-cased/resolve/main/%3Cnon-existent-file%3E.
```
```


#### BadRequestError

### huggingface_hub.utils.BadRequestError

```python
Raised by `hf_raise_for_status` when the server returns a HTTP 400 error.

Example:

```py
>>> resp = requests.post("hf.co/api/check", ...)
>>> hf_raise_for_status(resp, endpoint_name="check")
huggingface_hub.utils._errors.BadRequestError: Bad request for check endpoint: {details} (Request ID: XXX)
```
```


#### LocalEntryNotFoundError

### huggingface_hub.utils.LocalEntryNotFoundError

```python
Raised when trying to access a file or snapshot that is not on the disk when network is
disabled or unavailable (connection issue). The entry may exist on the Hub.

Note: `ValueError` type is to ensure backward compatibility.
Note: `LocalEntryNotFoundError` derives from `HTTPError` because of `EntryNotFoundError`
      even when it is not a network issue.

Example:

```py
>>> from huggingface_hub import hf_hub_download
>>> hf_hub_download('bert-base-cased', '<non-cached-file>',  local_files_only=True)
(...)
huggingface_hub.utils._errors.LocalEntryNotFoundError: Cannot find the requested files in the disk cache and outgoing traffic has been disabled. To enable hf.co look-ups and downloads online, set 'local_files_only' to False.
```
```


#### OfflineModeIsEnabled

### huggingface_hub.utils.OfflineModeIsEnabled

```python
Raised when a request is made but `HF_HUB_OFFLINE=1` is set as environment variable.
```


## Telemetry

`huggingface_hub` includes an helper to send telemetry data. This information helps us debug issues and prioritize new features.
Users can disable telemetry collection at any time by setting the `HF_HUB_DISABLE_TELEMETRY=1` environment variable.
Telemetry is also disabled in offline mode (i.e. when setting HF_HUB_OFFLINE=1).

If you are maintainer of a third-party library, sending telemetry data is as simple as making a call to [`send_telemetry`].
Data is sent in a separate thread to reduce as much as possible the impact for users.

### utils.send_telemetry

Error fetching docstring for utils.send_telemetry: module 'utils' has no attribute 'send_telemetry'



## Validators

`huggingface_hub` includes custom validators to validate method arguments automatically.
Validation is inspired by the work done in [Pydantic](https://pydantic-docs.helpmanual.io/)
to validate type hints but with more limited features.

### Generic decorator

[`~utils.validate_hf_hub_args`] is a generic decorator to encapsulate
methods that have arguments following `huggingface_hub`'s naming. By default, all
arguments that has a validator implemented will be validated.

If an input is not valid, a [`~utils.HFValidationError`] is thrown. Only
the first non-valid value throws an error and stops the validation process.

Usage:

```py
>>> from huggingface_hub.utils import validate_hf_hub_args

>>> @validate_hf_hub_args
... def my_cool_method(repo_id: str):
...     print(repo_id)

>>> my_cool_method(repo_id="valid_repo_id")
valid_repo_id

>>> my_cool_method("other..repo..id")
huggingface_hub.utils._validators.HFValidationError: Cannot have -- or .. in repo_id: 'other..repo..id'.

>>> my_cool_method(repo_id="other..repo..id")
huggingface_hub.utils._validators.HFValidationError: Cannot have -- or .. in repo_id: 'other..repo..id'.

>>> @validate_hf_hub_args
... def my_cool_auth_method(token: str):
...     print(token)

>>> my_cool_auth_method(token="a token")
"a token"

>>> my_cool_auth_method(use_auth_token="a use_auth_token")
"a use_auth_token"

>>> my_cool_auth_method(token="a token", use_auth_token="a use_auth_token")
UserWarning: Both `token` and `use_auth_token` are passed (...). `use_auth_token` value will be ignored.
"a token"
```

#### validate_hf_hub_args

### utils.validate_hf_hub_args

Error fetching docstring for utils.validate_hf_hub_args: module 'utils' has no attribute 'validate_hf_hub_args'


#### HFValidationError

### utils.HFValidationError

Error fetching docstring for utils.HFValidationError: module 'utils' has no attribute 'HFValidationError'


### Argument validators

Validators can also be used individually. Here is a list of all arguments that can be
validated.

#### repo_id

### utils.validate_repo_id

Error fetching docstring for utils.validate_repo_id: module 'utils' has no attribute 'validate_repo_id'


#### smoothly_deprecate_use_auth_token

Not exactly a validator, but ran as well.

### utils.smoothly_deprecate_use_auth_token

Error fetching docstring for utils.smoothly_deprecate_use_auth_token: module 'utils' has no attribute 'smoothly_deprecate_use_auth_token'

