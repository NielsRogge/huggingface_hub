<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# HfApi Client

Below is the documentation for the `HfApi` class, which serves as a Python wrapper for the Hugging Face Hub's API.

All methods from the `HfApi` are also accessible from the package's root directly. Both approaches are detailed below.

Using the root method is more straightforward but the [`HfApi`] class gives you more flexibility.
In particular, you can pass a token that will be reused in all HTTP calls. This is different
than `huggingface-cli login` or [`login`] as the token is not persisted on the machine.
It is also possible to provide a different endpoint or configure a custom user-agent.

```python
from huggingface_hub import HfApi, list_models

# Use root method
models = list_models()

# Or configure a HfApi client
hf_api = HfApi(
    endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token="hf_xxx", # Token is not persisted on the machine.
)
models = hf_api.list_models()
```

## HfApi

### HfApi

```python
Client to interact with the Hugging Face Hub via HTTP.

The client is initialized with some high-level settings used in all requests
made to the Hub (HF endpoint, authentication, user agents...). Using the `HfApi`
client is preferred but not mandatory as all of its public methods are exposed
directly at the root of `huggingface_hub`.

Args:
    endpoint (`str`, *optional*):
        Endpoint of the Hub. Defaults to <https://huggingface.co>.
    token (Union[bool, str, None], optional):
        A valid user access token (string). Defaults to the locally saved
        token, which is the recommended method for authentication (see
        https://huggingface.co/docs/huggingface_hub/quick-start#authentication).
        To disable authentication, pass `False`.
    library_name (`str`, *optional*):
        The name of the library that is making the HTTP request. Will be added to
        the user-agent header. Example: `"transformers"`.
    library_version (`str`, *optional*):
        The version of the library that is making the HTTP request. Will be added
        to the user-agent header. Example: `"4.24.0"`.
    user_agent (`str`, `dict`, *optional*):
        The user agent info in the form of a dictionary or a single string. It will
        be completed with information about the installed packages.
    headers (`dict`, *optional*):
        Additional headers to be sent with each request. Example: `{"X-My-Header": "value"}`.
        Headers passed here are taking precedence over the default headers.
```


## API Dataclasses

### AccessRequest

### huggingface_hub.hf_api.AccessRequest

```python
Data structure containing information about a user access request.

Attributes:
    username (`str`):
        Username of the user who requested access.
    fullname (`str`):
        Fullname of the user who requested access.
    email (`Optional[str]`):
        Email of the user who requested access.
        Can only be `None` in the /accepted list if the user was granted access manually.
    timestamp (`datetime`):
        Timestamp of the request.
    status (`Literal["pending", "accepted", "rejected"]`):
        Status of the request. Can be one of `["pending", "accepted", "rejected"]`.
    fields (`Dict[str, Any]`, *optional*):
        Additional fields filled by the user in the gate form.
```


### CommitInfo

### huggingface_hub.hf_api.CommitInfo

```python
Data structure containing information about a newly created commit.

Returned by any method that creates a commit on the Hub: [`create_commit`], [`upload_file`], [`upload_folder`],
[`delete_file`], [`delete_folder`]. It inherits from `str` for backward compatibility but using methods specific
to `str` is deprecated.

Attributes:
    commit_url (`str`):
        Url where to find the commit.

    commit_message (`str`):
        The summary (first line) of the commit that has been created.

    commit_description (`str`):
        Description of the commit that has been created. Can be empty.

    oid (`str`):
        Commit hash id. Example: `"91c54ad1727ee830252e457677f467be0bfd8a57"`.

    pr_url (`str`, *optional*):
        Url to the PR that has been created, if any. Populated when `create_pr=True`
        is passed.

    pr_revision (`str`, *optional*):
        Revision of the PR that has been created, if any. Populated when
        `create_pr=True` is passed. Example: `"refs/pr/1"`.

    pr_num (`int`, *optional*):
        Number of the PR discussion that has been created, if any. Populated when
        `create_pr=True` is passed. Can be passed as `discussion_num` in
        [`get_discussion_details`]. Example: `1`.

    repo_url (`RepoUrl`):
        Repo URL of the commit containing info like repo_id, repo_type, etc.

    _url (`str`, *optional*):
        Legacy url for `str` compatibility. Can be the url to the uploaded file on the Hub (if returned by
        [`upload_file`]), to the uploaded folder on the Hub (if returned by [`upload_folder`]) or to the commit on
        the Hub (if returned by [`create_commit`]). Defaults to `commit_url`. It is deprecated to use this
        attribute. Please use `commit_url` instead.
```


### DatasetInfo

### huggingface_hub.hf_api.DatasetInfo

```python
Contains information about a dataset on the Hub.

<Tip>

Most attributes of this class are optional. This is because the data returned by the Hub depends on the query made.
In general, the more specific the query, the more information is returned. On the contrary, when listing datasets
using [`list_datasets`] only a subset of the attributes are returned.

</Tip>

Attributes:
    id (`str`):
        ID of dataset.
    author (`str`):
        Author of the dataset.
    sha (`str`):
        Repo SHA at this particular revision.
    created_at (`datetime`, *optional*):
        Date of creation of the repo on the Hub. Note that the lowest value is `2022-03-02T23:29:04.000Z`,
        corresponding to the date when we began to store creation dates.
    last_modified (`datetime`, *optional*):
        Date of last commit to the repo.
    private (`bool`):
        Is the repo private.
    disabled (`bool`, *optional*):
        Is the repo disabled.
    gated (`Literal["auto", "manual", False]`, *optional*):
        Is the repo gated.
        If so, whether there is manual or automatic approval.
    downloads (`int`):
        Number of downloads of the dataset over the last 30 days.
    downloads_all_time (`int`):
        Cumulated number of downloads of the model since its creation.
    likes (`int`):
        Number of likes of the dataset.
    tags (`List[str]`):
        List of tags of the dataset.
    card_data (`DatasetCardData`, *optional*):
        Model Card Metadata  as a [`huggingface_hub.repocard_data.DatasetCardData`] object.
    siblings (`List[RepoSibling]`):
        List of [`huggingface_hub.hf_api.RepoSibling`] objects that constitute the dataset.
    paperswithcode_id (`str`, *optional*):
        Papers with code ID of the dataset.
    trending_score (`int`, *optional*):
        Trending score of the dataset.
```


### GitRefInfo

### huggingface_hub.hf_api.GitRefInfo

```python
Contains information about a git reference for a repo on the Hub.

Attributes:
    name (`str`):
        Name of the reference (e.g. tag name or branch name).
    ref (`str`):
        Full git ref on the Hub (e.g. `"refs/heads/main"` or `"refs/tags/v1.0"`).
    target_commit (`str`):
        OID of the target commit for the ref (e.g. `"e7da7f221d5bf496a48136c0cd264e630fe9fcc8"`)
```


### GitCommitInfo

### huggingface_hub.hf_api.GitCommitInfo

```python
Contains information about a git commit for a repo on the Hub. Check out [`list_repo_commits`] for more details.

Attributes:
    commit_id (`str`):
        OID of the commit (e.g. `"e7da7f221d5bf496a48136c0cd264e630fe9fcc8"`)
    authors (`List[str]`):
        List of authors of the commit.
    created_at (`datetime`):
        Datetime when the commit was created.
    title (`str`):
        Title of the commit. This is a free-text value entered by the authors.
    message (`str`):
        Description of the commit. This is a free-text value entered by the authors.
    formatted_title (`str`):
        Title of the commit formatted as HTML. Only returned if `formatted=True` is set.
    formatted_message (`str`):
        Description of the commit formatted as HTML. Only returned if `formatted=True` is set.
```


### GitRefs

### huggingface_hub.hf_api.GitRefs

```python
Contains information about all git references for a repo on the Hub.

Object is returned by [`list_repo_refs`].

Attributes:
    branches (`List[GitRefInfo]`):
        A list of [`GitRefInfo`] containing information about branches on the repo.
    converts (`List[GitRefInfo]`):
        A list of [`GitRefInfo`] containing information about "convert" refs on the repo.
        Converts are refs used (internally) to push preprocessed data in Dataset repos.
    tags (`List[GitRefInfo]`):
        A list of [`GitRefInfo`] containing information about tags on the repo.
    pull_requests (`List[GitRefInfo]`, *optional*):
        A list of [`GitRefInfo`] containing information about pull requests on the repo.
        Only returned if `include_prs=True` is set.
```


### ModelInfo

### huggingface_hub.hf_api.ModelInfo

```python
Contains information about a model on the Hub.

<Tip>

Most attributes of this class are optional. This is because the data returned by the Hub depends on the query made.
In general, the more specific the query, the more information is returned. On the contrary, when listing models
using [`list_models`] only a subset of the attributes are returned.

</Tip>

Attributes:
    id (`str`):
        ID of model.
    author (`str`, *optional*):
        Author of the model.
    sha (`str`, *optional*):
        Repo SHA at this particular revision.
    created_at (`datetime`, *optional*):
        Date of creation of the repo on the Hub. Note that the lowest value is `2022-03-02T23:29:04.000Z`,
        corresponding to the date when we began to store creation dates.
    last_modified (`datetime`, *optional*):
        Date of last commit to the repo.
    private (`bool`):
        Is the repo private.
    disabled (`bool`, *optional*):
        Is the repo disabled.
    downloads (`int`):
        Number of downloads of the model over the last 30 days.
    downloads_all_time (`int`):
        Cumulated number of downloads of the model since its creation.
    gated (`Literal["auto", "manual", False]`, *optional*):
        Is the repo gated.
        If so, whether there is manual or automatic approval.
    gguf (`Dict`, *optional*):
        GGUF information of the model.
    inference (`Literal["cold", "frozen", "warm"]`, *optional*):
        Status of the model on the inference API.
        Warm models are available for immediate use. Cold models will be loaded on first inference call.
        Frozen models are not available in Inference API.
    likes (`int`):
        Number of likes of the model.
    library_name (`str`, *optional*):
        Library associated with the model.
    tags (`List[str]`):
        List of tags of the model. Compared to `card_data.tags`, contains extra tags computed by the Hub
        (e.g. supported libraries, model's arXiv).
    pipeline_tag (`str`, *optional*):
        Pipeline tag associated with the model.
    mask_token (`str`, *optional*):
        Mask token used by the model.
    widget_data (`Any`, *optional*):
        Widget data associated with the model.
    model_index (`Dict`, *optional*):
        Model index for evaluation.
    config (`Dict`, *optional*):
        Model configuration.
    transformers_info (`TransformersInfo`, *optional*):
        Transformers-specific info (auto class, processor, etc.) associated with the model.
    trending_score (`int`, *optional*):
        Trending score of the model.
    card_data (`ModelCardData`, *optional*):
        Model Card Metadata  as a [`huggingface_hub.repocard_data.ModelCardData`] object.
    siblings (`List[RepoSibling]`):
        List of [`huggingface_hub.hf_api.RepoSibling`] objects that constitute the model.
    spaces (`List[str]`, *optional*):
        List of spaces using the model.
    safetensors (`SafeTensorsInfo`, *optional*):
        Model's safetensors information.
    security_repo_status (`Dict`, *optional*):
        Model's security scan status.
```


### RepoSibling

### huggingface_hub.hf_api.RepoSibling

```python
Contains basic information about a repo file inside a repo on the Hub.

<Tip>

All attributes of this class are optional except `rfilename`. This is because only the file names are returned when
listing repositories on the Hub (with [`list_models`], [`list_datasets`] or [`list_spaces`]). If you need more
information like file size, blob id or lfs details, you must request them specifically from one repo at a time
(using [`model_info`], [`dataset_info`] or [`space_info`]) as it adds more constraints on the backend server to
retrieve these.

</Tip>

Attributes:
    rfilename (str):
        file name, relative to the repo root.
    size (`int`, *optional*):
        The file's size, in bytes. This attribute is defined when `files_metadata` argument of [`repo_info`] is set
        to `True`. It's `None` otherwise.
    blob_id (`str`, *optional*):
        The file's git OID. This attribute is defined when `files_metadata` argument of [`repo_info`] is set to
        `True`. It's `None` otherwise.
    lfs (`BlobLfsInfo`, *optional*):
        The file's LFS metadata. This attribute is defined when`files_metadata` argument of [`repo_info`] is set to
        `True` and the file is stored with Git LFS. It's `None` otherwise.
```


### RepoFile

### huggingface_hub.hf_api.RepoFile

```python
Contains information about a file on the Hub.

Attributes:
    path (str):
        file path relative to the repo root.
    size (`int`):
        The file's size, in bytes.
    blob_id (`str`):
        The file's git OID.
    lfs (`BlobLfsInfo`):
        The file's LFS metadata.
    last_commit (`LastCommitInfo`, *optional*):
        The file's last commit metadata. Only defined if [`list_repo_tree`] and [`get_paths_info`]
        are called with `expand=True`.
    security (`BlobSecurityInfo`, *optional*):
        The file's security scan metadata. Only defined if [`list_repo_tree`] and [`get_paths_info`]
        are called with `expand=True`.
```


### RepoUrl

### huggingface_hub.hf_api.RepoUrl

```python
Subclass of `str` describing a repo URL on the Hub.

`RepoUrl` is returned by `HfApi.create_repo`. It inherits from `str` for backward
compatibility. At initialization, the URL is parsed to populate properties:
- endpoint (`str`)
- namespace (`Optional[str]`)
- repo_name (`str`)
- repo_id (`str`)
- repo_type (`Literal["model", "dataset", "space"]`)
- url (`str`)

Args:
    url (`Any`):
        String value of the repo url.
    endpoint (`str`, *optional*):
        Endpoint of the Hub. Defaults to <https://huggingface.co>.

Example:
```py
>>> RepoUrl('https://huggingface.co/gpt2')
RepoUrl('https://huggingface.co/gpt2', endpoint='https://huggingface.co', repo_type='model', repo_id='gpt2')

>>> RepoUrl('https://hub-ci.huggingface.co/datasets/dummy_user/dummy_dataset', endpoint='https://hub-ci.huggingface.co')
RepoUrl('https://hub-ci.huggingface.co/datasets/dummy_user/dummy_dataset', endpoint='https://hub-ci.huggingface.co', repo_type='dataset', repo_id='dummy_user/dummy_dataset')

>>> RepoUrl('hf://datasets/my-user/my-dataset')
RepoUrl('hf://datasets/my-user/my-dataset', endpoint='https://huggingface.co', repo_type='dataset', repo_id='user/dataset')

>>> HfApi.create_repo("dummy_model")
RepoUrl('https://huggingface.co/Wauplin/dummy_model', endpoint='https://huggingface.co', repo_type='model', repo_id='Wauplin/dummy_model')
```

Raises:
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If URL cannot be parsed.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If `repo_type` is unknown.
```


### SafetensorsRepoMetadata

### huggingface_hub.utils.SafetensorsRepoMetadata

```python
Metadata for a Safetensors repo.

A repo is considered to be a Safetensors repo if it contains either a 'model.safetensors' weight file (non-shared
model) or a 'model.safetensors.index.json' index file (sharded model) at its root.

This class is returned by [`get_safetensors_metadata`].

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

Attributes:
    metadata (`Dict`, *optional*):
        The metadata contained in the 'model.safetensors.index.json' file, if it exists. Only populated for sharded
        models.
    sharded (`bool`):
        Whether the repo contains a sharded model or not.
    weight_map (`Dict[str, str]`):
        A map of all weights. Keys are tensor names and values are filenames of the files containing the tensors.
    files_metadata (`Dict[str, SafetensorsFileMetadata]`):
        A map of all files metadata. Keys are filenames and values are the metadata of the corresponding file, as
        a [`SafetensorsFileMetadata`] object.
    parameter_count (`Dict[str, int]`):
        A map of the number of parameters per data type. Keys are data types and values are the number of parameters
        of that data type.
```


### SafetensorsFileMetadata

### huggingface_hub.utils.SafetensorsFileMetadata

```python
Metadata for a Safetensors file hosted on the Hub.

This class is returned by [`parse_safetensors_file_metadata`].

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

Attributes:
    metadata (`Dict`):
        The metadata contained in the file.
    tensors (`Dict[str, TensorInfo]`):
        A map of all tensors. Keys are tensor names and values are information about the corresponding tensor, as a
        [`TensorInfo`] object.
    parameter_count (`Dict[str, int]`):
        A map of the number of parameters per data type. Keys are data types and values are the number of parameters
        of that data type.
```


### SpaceInfo

### huggingface_hub.hf_api.SpaceInfo

```python
Contains information about a Space on the Hub.

<Tip>

Most attributes of this class are optional. This is because the data returned by the Hub depends on the query made.
In general, the more specific the query, the more information is returned. On the contrary, when listing spaces
using [`list_spaces`] only a subset of the attributes are returned.

</Tip>

Attributes:
    id (`str`):
        ID of the Space.
    author (`str`, *optional*):
        Author of the Space.
    sha (`str`, *optional*):
        Repo SHA at this particular revision.
    created_at (`datetime`, *optional*):
        Date of creation of the repo on the Hub. Note that the lowest value is `2022-03-02T23:29:04.000Z`,
        corresponding to the date when we began to store creation dates.
    last_modified (`datetime`, *optional*):
        Date of last commit to the repo.
    private (`bool`):
        Is the repo private.
    gated (`Literal["auto", "manual", False]`, *optional*):
        Is the repo gated.
        If so, whether there is manual or automatic approval.
    disabled (`bool`, *optional*):
        Is the Space disabled.
    host (`str`, *optional*):
        Host URL of the Space.
    subdomain (`str`, *optional*):
        Subdomain of the Space.
    likes (`int`):
        Number of likes of the Space.
    tags (`List[str]`):
        List of tags of the Space.
    siblings (`List[RepoSibling]`):
        List of [`huggingface_hub.hf_api.RepoSibling`] objects that constitute the Space.
    card_data (`SpaceCardData`, *optional*):
        Space Card Metadata  as a [`huggingface_hub.repocard_data.SpaceCardData`] object.
    runtime (`SpaceRuntime`, *optional*):
        Space runtime information as a [`huggingface_hub.hf_api.SpaceRuntime`] object.
    sdk (`str`, *optional*):
        SDK used by the Space.
    models (`List[str]`, *optional*):
        List of models used by the Space.
    datasets (`List[str]`, *optional*):
        List of datasets used by the Space.
    trending_score (`int`, *optional*):
        Trending score of the Space.
```


### TensorInfo

### huggingface_hub.utils.TensorInfo

```python
Information about a tensor.

For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

Attributes:
    dtype (`str`):
        The data type of the tensor ("F64", "F32", "F16", "BF16", "I64", "I32", "I16", "I8", "U8", "BOOL").
    shape (`List[int]`):
        The shape of the tensor.
    data_offsets (`Tuple[int, int]`):
        The offsets of the data in the file as a tuple `[BEGIN, END]`.
    parameter_count (`int`):
        The number of parameters in the tensor.
```


### User

### huggingface_hub.hf_api.User

```python
Contains information about a user on the Hub.

Attributes:
    username (`str`):
        Name of the user on the Hub (unique).
    fullname (`str`):
        User's full name.
    avatar_url (`str`):
        URL of the user's avatar.
    details (`str`, *optional*):
        User's details.
    is_following (`bool`, *optional*):
        Whether the authenticated user is following this user.
    is_pro (`bool`, *optional*):
        Whether the user is a pro user.
    num_models (`int`, *optional*):
        Number of models created by the user.
    num_datasets (`int`, *optional*):
        Number of datasets created by the user.
    num_spaces (`int`, *optional*):
        Number of spaces created by the user.
    num_discussions (`int`, *optional*):
        Number of discussions initiated by the user.
    num_papers (`int`, *optional*):
        Number of papers authored by the user.
    num_upvotes (`int`, *optional*):
        Number of upvotes received by the user.
    num_likes (`int`, *optional*):
        Number of likes given by the user.
    num_following (`int`, *optional*):
        Number of users this user is following.
    num_followers (`int`, *optional*):
        Number of users following this user.
    orgs (list of [`Organization`]):
        List of organizations the user is part of.
```


### UserLikes

### huggingface_hub.hf_api.UserLikes

```python
Contains information about a user likes on the Hub.

Attributes:
    user (`str`):
        Name of the user for which we fetched the likes.
    total (`int`):
        Total number of likes.
    datasets (`List[str]`):
        List of datasets liked by the user (as repo_ids).
    models (`List[str]`):
        List of models liked by the user (as repo_ids).
    spaces (`List[str]`):
        List of spaces liked by the user (as repo_ids).
```


### WebhookInfo

### huggingface_hub.hf_api.WebhookInfo

```python
Data structure containing information about a webhook.

Attributes:
    id (`str`):
        ID of the webhook.
    url (`str`):
        URL of the webhook.
    watched (`List[WebhookWatchedItem]`):
        List of items watched by the webhook, see [`WebhookWatchedItem`].
    domains (`List[WEBHOOK_DOMAIN_T]`):
        List of domains the webhook is watching. Can be one of `["repo", "discussions"]`.
    secret (`str`, *optional*):
        Secret of the webhook.
    disabled (`bool`):
        Whether the webhook is disabled or not.
```


### WebhookWatchedItem

### huggingface_hub.hf_api.WebhookWatchedItem

```python
Data structure containing information about the items watched by a webhook.

Attributes:
    type (`Literal["dataset", "model", "org", "space", "user"]`):
        Type of the item to be watched. Can be one of `["dataset", "model", "org", "space", "user"]`.
    name (`str`):
        Name of the item to be watched. Can be the username, organization name, model name, dataset name or space name.
```


## CommitOperation

Below are the supported values for [`CommitOperation`]:

### CommitOperationAdd

```python
Data structure holding necessary info to upload a file to a repository on the Hub.

Args:
    path_in_repo (`str`):
        Relative filepath in the repo, for example: `"checkpoints/1fec34a/weights.bin"`
    path_or_fileobj (`str`, `Path`, `bytes`, or `BinaryIO`):
        Either:
        - a path to a local file (as `str` or `pathlib.Path`) to upload
        - a buffer of bytes (`bytes`) holding the content of the file to upload
        - a "file object" (subclass of `io.BufferedIOBase`), typically obtained
            with `open(path, "rb")`. It must support `seek()` and `tell()` methods.

Raises:
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If `path_or_fileobj` is not one of `str`, `Path`, `bytes` or `io.BufferedIOBase`.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If `path_or_fileobj` is a `str` or `Path` but not a path to an existing file.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If `path_or_fileobj` is a `io.BufferedIOBase` but it doesn't support both
        `seek()` and `tell()`.
```


### CommitOperationDelete

```python
Data structure holding necessary info to delete a file or a folder from a repository
on the Hub.

Args:
    path_in_repo (`str`):
        Relative filepath in the repo, for example: `"checkpoints/1fec34a/weights.bin"`
        for a file or `"checkpoints/1fec34a/"` for a folder.
    is_folder (`bool` or `Literal["auto"]`, *optional*)
        Whether the Delete Operation applies to a folder or not. If "auto", the path
        type (file or folder) is guessed automatically by looking if path ends with
        a "/" (folder) or not (file). To explicitly set the path type, you can set
        `is_folder=True` or `is_folder=False`.
```


### CommitOperationCopy

```python
Data structure holding necessary info to copy a file in a repository on the Hub.

Limitations:
  - Only LFS files can be copied. To copy a regular file, you need to download it locally and re-upload it
  - Cross-repository copies are not supported.

Note: you can combine a [`CommitOperationCopy`] and a [`CommitOperationDelete`] to rename an LFS file on the Hub.

Args:
    src_path_in_repo (`str`):
        Relative filepath in the repo of the file to be copied, e.g. `"checkpoints/1fec34a/weights.bin"`.
    path_in_repo (`str`):
        Relative filepath in the repo where to copy the file, e.g. `"checkpoints/1fec34a/weights_copy.bin"`.
    src_revision (`str`, *optional*):
        The git revision of the file to be copied. Can be any valid git revision.
        Default to the target commit revision.
```


## CommitScheduler

### CommitScheduler

```python
Scheduler to upload a local folder to the Hub at regular intervals (e.g. push to hub every 5 minutes).

The recommended way to use the scheduler is to use it as a context manager. This ensures that the scheduler is
properly stopped and the last commit is triggered when the script ends. The scheduler can also be stopped manually
with the `stop` method. Checkout the [upload guide](https://huggingface.co/docs/huggingface_hub/guides/upload#scheduled-uploads)
to learn more about how to use it.

Args:
    repo_id (`str`):
        The id of the repo to commit to.
    folder_path (`str` or `Path`):
        Path to the local folder to upload regularly.
    every (`int` or `float`, *optional*):
        The number of minutes between each commit. Defaults to 5 minutes.
    path_in_repo (`str`, *optional*):
        Relative path of the directory in the repo, for example: `"checkpoints/"`. Defaults to the root folder
        of the repository.
    repo_type (`str`, *optional*):
        The type of the repo to commit to. Defaults to `model`.
    revision (`str`, *optional*):
        The revision of the repo to commit to. Defaults to `main`.
    private (`bool`, *optional*):
        Whether to make the repo private. If `None` (default), the repo will be public unless the organization's default is private. This value is ignored if the repo already exists.
    token (`str`, *optional*):
        The token to use to commit to the repo. Defaults to the token saved on the machine.
    allow_patterns (`List[str]` or `str`, *optional*):
        If provided, only files matching at least one pattern are uploaded.
    ignore_patterns (`List[str]` or `str`, *optional*):
        If provided, files matching any of the patterns are not uploaded.
    squash_history (`bool`, *optional*):
        Whether to squash the history of the repo after each commit. Defaults to `False`. Squashing commits is
        useful to avoid degraded performances on the repo when it grows too large.
    hf_api (`HfApi`, *optional*):
        The [`HfApi`] client to use to commit to the Hub. Can be set with custom settings (user agent, token,...).

Example:
```py
>>> from pathlib import Path
>>> from huggingface_hub import CommitScheduler

# Scheduler uploads every 10 minutes
>>> csv_path = Path("watched_folder/data.csv")
>>> CommitScheduler(repo_id="test_scheduler", repo_type="dataset", folder_path=csv_path.parent, every=10)

>>> with csv_path.open("a") as f:
...     f.write("first line")

# Some time later (...)
>>> with csv_path.open("a") as f:
...     f.write("second line")
```

Example using a context manager:
```py
>>> from pathlib import Path
>>> from huggingface_hub import CommitScheduler

>>> with CommitScheduler(repo_id="test_scheduler", repo_type="dataset", folder_path="watched_folder", every=10) as scheduler:
...     csv_path = Path("watched_folder/data.csv")
...     with csv_path.open("a") as f:
...         f.write("first line")
...     (...)
...     with csv_path.open("a") as f:
...         f.write("second line")

# Scheduler is now stopped and last commit have been triggered
```
```

