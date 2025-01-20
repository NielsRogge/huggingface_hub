<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 유틸리티[[utilities]]

## 로깅 구성[[huggingface_hub.utils.logging.get_verbosity]]

`huggingface_hub` 패키지는 패키지 로그 레벨을 제어하기 위한 `logging` 유틸리티를 제공합니다. 
다음과 같이 가져올 수 있습니다:

```py
from huggingface_hub import logging
```

그런 다음, 로그의 출력 수를 업데이트하기 위해 로그 레벨을 정의할 수 있습니다:

```python
from huggingface_hub import logging

logging.set_verbosity_error()
logging.set_verbosity_warning()
logging.set_verbosity_info()
logging.set_verbosity_debug()

logging.set_verbosity(...)
```

로그 레벨은 다음과 같이 이해하면 됩니다:

- `error`: 오류 또는 예기치 않은 동작으로 이어질 수 있는 결정적인 로그만 표시합니다.
- `warning`:  결정적이진 않지만 의도치 않은 동작을 초래할 수 있는 로그를 표시합니다. 또한 중요한 정보를 포함한 로그도 표시될 수 있습니다.
- `info`: 하부에서 무슨 일이 일어나고 있는지에 대한 자세한 로그를 포함하여 대부분의 로그를 표시합니다. 무언가 예상치 못한 방식으로 동작하는 경우, 더 많은 정보를 얻기 위해 verbosity 단계로 전환하는 것이 좋습니다.
- `debug`: 하부에서 정확히 무슨 일이 일어나고 있는지를 추적하는 데 사용될 수 있는 일부 내부 로그를 포함하여 모든 로그를 표시합니다.

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


### 리포지토리별 도우미 메소드[[huggingface_hub.utils.logging.get_logger]]

아래 제공된 메소드들은 `huggingface_hub` 라이브러리 모듈을 수정할 때 관련이 있습니다. `huggingface_hub`를 사용하고 해당 모듈을 수정하지 않는 경우에는 사용할 필요가 없습니다.

### logging.get_logger

Error fetching docstring for logging.get_logger: module 'logging' has no attribute 'get_logger'


## 프로그레스 바 구성하기[[configure-progress-bars]]

프로그레스 바는 긴 시간이 걸리는 작업을 실행하는 동안 정보를 표시하는 유용한 도구입니다(예시로 파일을 다운로드하거나 업로드하는 등). `huggingface_hub`는 라이브러리 전체에서 일관된 방식으로 프로그레스 바를 표시하기 위한 [`~utils.tqdm`] 래퍼를 제공합니다.

기본적으로 프로그레스 바가 활성화되어 있습니다. `HF_HUB_DISABLE_PROGRESS_BARS` 환경 변수를 설정하여 전역적으로 비활성화할 수 있습니다. 또한 [`~utils.enable_progress_bars`]와 [`~utils.disable_progress_bars`]를 사용하여 프로그레스 바를 개별적으로 활성화 또는 비활성화할 수도 있습니다. 만약 환경 변수가 설정되어 있다면, 환경 변수가 도우미에서 우선 순위를 가집니다.


```py
>>> from huggingface_hub import snapshot_download
>>> from huggingface_hub.utils import are_progress_bars_disabled, disable_progress_bars, enable_progress_bars

>>> # 전역적으로 프로그레스 바를 비활성화합니다.
>>> disable_progress_bars()

>>> # 프로그레스 바가 표시되지 않습니다!
>>> snapshot_download("gpt2")

>>> are_progress_bars_disabled()
True

>>> # 다시 프로그레스 바가 활성화됩니다
>>> enable_progress_bars()
```

### are_progress_bars_disabled[[huggingface_hub.utils.are_progress_bars_disabled]]

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


### disable_progress_bars[[huggingface_hub.utils.disable_progress_bars]]

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


### enable_progress_bars[huggingface_hub.utils.enable_progress_bars]]

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


## HTTP 백엔드 구성[[huggingface_hub.configure_http_backend]]

일부 환경에서는 HTTP 호출이 이루어지는 방식을 구성할 수 있습니다. 예를 들어, 프록시를 사용하는 경우가 그렇습니다. `huggingface_hub`는 [`configure_http_backend`]를 사용하여 전역적으로 이를 구성할 수 있게 합니다. 그러면 Hub로의 모든 요청이 사용자가 설정한 설정을 사용합니다. 내부적으로 `huggingface_hub`는 `requests.Session`을 사용하므로 사용 가능한 매개변수에 대해 자세히 알아보려면 [requests 문서](https://requests.readthedocs.io/en/latest/user/advanced)를 참조하는 것이 좋습니다.

`requests.Session`이 스레드 안전을 보장하지 않기 때문에 `huggingface_hub`는 스레드당 하나의 세션 인스턴스를 생성합니다. 세션을 사용하면 HTTP 호출 사이에 연결을 유지하고 최종적으로 시간을 절약할 수 있습니다. `huggingface_hub`를 서드 파티 라이브러리에 통합하고 사용자 지정 호출을 Hub로 만들려는 경우, [`get_session`]을 사용하여 사용자가 구성한 세션을 가져옵니다 (즉, 모든 `requests.get(...)` 호출을 `get_session().get(...)`으로 대체합니다).

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



## HTTP 오류 다루기[[handle-http-errors]]

`huggingface_hub`는 서버에서 반환된 추가 정보로 `requests`에서 발생한 `HTTPError`를 세분화하기 위해 자체 HTTP 오류를 정의합니다.

### 예외 발생[[huggingface_hub.utils.hf_raise_for_status]]

[`~utils.hf_raise_for_status`]는 Hub에 대한 모든 요청에서 "상태를 확인하고 예외를 발생시키는" 중앙 메소드로 사용됩니다. 이 메서드는 기본 `requests.raise_for_status`를 감싸서 추가 정보를 제공합니다. 발생된 모든 `HTTPError`는 `HfHubHTTPError`로 변환됩니다.

```py
import requests
from huggingface_hub.utils import hf_raise_for_status, HfHubHTTPError

response = requests.post(...)
try:
    hf_raise_for_status(response)
except HfHubHTTPError as e:
    print(str(e)) # 형식화된 메시지
    e.request_id, e.server_message # 서버에서 반환된 세부 정보

    # 오류 메시지를 발생시킬 때 추가 정보를 포함하여 완성합니다
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


### HTTP 오류[[http-errors]]

여기에는 `huggingface_hub`에서 발생하는 HTTP 오류 목록이 있습니다.

#### HfHubHTTPError[[huggingface_hub.utils.HfHubHTTPError]]

`HfHubHTTPError`는 HF Hub HTTP 오류에 대한 부모 클래스입니다. 이 클래스는 서버 응답을 구문 분석하고 오류 메시지를 형식화하여 사용자에게 가능한 많은 정보를 제공합니다.

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


#### RepositoryNotFoundError[[huggingface_hub.utils.RepositoryNotFoundError]]

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


#### GatedRepoError[[huggingface_hub.utils.GatedRepoError]]

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


#### RevisionNotFoundError[[huggingface_hub.utils.RevisionNotFoundError]]

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


#### EntryNotFoundError[[huggingface_hub.utils.EntryNotFoundError]]

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


#### BadRequestError[[huggingface_hub.utils.BadRequestError]]

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


#### LocalEntryNotFoundError[[huggingface_hub.utils.LocalEntryNotFoundError]]

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


#### OfflineModeIsEnabledd[[huggingface_hub.utils.OfflineModeIsEnabled]]

### huggingface_hub.utils.OfflineModeIsEnabled

```python
Raised when a request is made but `HF_HUB_OFFLINE=1` is set as environment variable.
```


## 원격 측정[[huggingface_hub.utils.send_telemetry]]

`huggingface_hub`는 원격 측정 데이터를 보내는 도우미가 포함되어 있습니다. 이 정보는 문제를 디버깅하고 새로운 기능을 우선적으로 처리하는 데 도움이 됩니다. 사용자는 `HF_HUB_DISABLE_TELEMETRY=1` 환경 변수를 설정하여 언제든지 원격 측정 수집을 비활성화할 수 있습니다. 또한 오프라인 모드에서도 (즉, HF_HUB_OFFLINE=1로 설정된 경우) 원격 측정이 비활성화됩니다.

서드 파티 라이브러리의 유지 관리자인 경우, 원격 측정 데이터를 보내는 것은 [`send_telemetry`]를 호출하는 것만큼 간단합니다. 사용자에게 가능한 영향을 최소화하기 위해 데이터는 별도의 스레드에서 전송됩니다.

### utils.send_telemetry

Error fetching docstring for utils.send_telemetry: module 'utils' has no attribute 'send_telemetry'



## 검증기[[validators]]

`huggingface_hub`에는 메소드 인수를 자동으로 유효성 검사하는 사용자 정의 검증기가 포함되어 있습니다. 이 유효성 검사는 타입 힌트를 검증하는 데 [Pydantic](https://pydantic-docs.helpmanual.io/)의 작업을 참고하여 구현되었지만, 기능은 더 제한적입니다.

### 일반 데코레이터[[generic-decorator]]

[`~utils.validate_hf_hub_args`]는 `huggingface_hub`의 네이밍을 따르는 인수를 갖는 메소드를 캡슐화하는 일반적인 데코레이터입니다. 기본적으로 구현된 검증기가 있는 모든 인수가 유효성 검사됩니다.

입력이 유효하지 않은 경우 [`~utils.HFValidationError`]이 발생합니다. 첫 번째 유효하지 않은 값만 오류를 발생시키고 유효성 검사 프로세스를 중지합니다.

사용법:

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

#### validate_hf_hub_args[[huggingface_hub.utils.validate_hf_hub_args]]

### utils.validate_hf_hub_args

Error fetching docstring for utils.validate_hf_hub_args: module 'utils' has no attribute 'validate_hf_hub_args'


#### HFValidationError[[huggingface_hub.utils.HFValidationError]]

### utils.HFValidationError

Error fetching docstring for utils.HFValidationError: module 'utils' has no attribute 'HFValidationError'


### Argument validators[[argument-validators]]

검증기는 개별적으로도 사용할 수 있습니다. 다음은 검증할 수 있는 모든 인수 목록입니다.

#### repo_id[[huggingface_hub.utils.validate_repo_id]]

### utils.validate_repo_id

Error fetching docstring for utils.validate_repo_id: module 'utils' has no attribute 'validate_repo_id'


#### smoothly_deprecate_use_auth_token[[huggingface_hub.utils.smoothly_deprecate_use_auth_token]]

정확히 검증기는 아니지만, 잘 실행됩니다.

### utils.smoothly_deprecate_use_auth_token

Error fetching docstring for utils.smoothly_deprecate_use_auth_token: module 'utils' has no attribute 'smoothly_deprecate_use_auth_token'

