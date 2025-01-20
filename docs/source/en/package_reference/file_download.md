<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Downloading files

## Download a single file

### hf_hub_download

### huggingface_hub.hf_hub_download

```python
Download a given file if it's not already present in the local cache.

The new cache file layout looks like this:
- The cache directory contains one subfolder per repo_id (namespaced by repo type)
- inside each repo folder:
    - refs is a list of the latest known revision => commit_hash pairs
    - blobs contains the actual file blobs (identified by their git-sha or sha256, depending on
      whether they're LFS files or not)
    - snapshots contains one subfolder per commit, each "commit" contains the subset of the files
      that have been resolved at that particular commit. Each filename is a symlink to the blob
      at that particular commit.

```
[  96]  .
└── [ 160]  models--julien-c--EsperBERTo-small
    ├── [ 160]  blobs
    │   ├── [321M]  403450e234d65943a7dcf7e05a771ce3c92faa84dd07db4ac20f592037a1e4bd
    │   ├── [ 398]  7cb18dc9bafbfcf74629a4b760af1b160957a83e
    │   └── [1.4K]  d7edf6bd2a681fb0175f7735299831ee1b22b812
    ├── [  96]  refs
    │   └── [  40]  main
    └── [ 128]  snapshots
        ├── [ 128]  2439f60ef33a0d46d85da5001d52aeda5b00ce9f
        │   ├── [  52]  README.md -> ../../blobs/d7edf6bd2a681fb0175f7735299831ee1b22b812
        │   └── [  76]  pytorch_model.bin -> ../../blobs/403450e234d65943a7dcf7e05a771ce3c92faa84dd07db4ac20f592037a1e4bd
        └── [ 128]  bbc77c8132af1cc5cf678da3f1ddf2de43606d48
            ├── [  52]  README.md -> ../../blobs/7cb18dc9bafbfcf74629a4b760af1b160957a83e
            └── [  76]  pytorch_model.bin -> ../../blobs/403450e234d65943a7dcf7e05a771ce3c92faa84dd07db4ac20f592037a1e4bd
```

If `local_dir` is provided, the file structure from the repo will be replicated in this location. When using this
option, the `cache_dir` will not be used and a `.cache/huggingface/` folder will be created at the root of `local_dir`
to store some metadata related to the downloaded files. While this mechanism is not as robust as the main
cache-system, it's optimized for regularly pulling the latest version of a repository.

Args:
    repo_id (`str`):
        A user or an organization name and a repo name separated by a `/`.
    filename (`str`):
        The name of the file in the repo.
    subfolder (`str`, *optional*):
        An optional value corresponding to a folder inside the model repo.
    repo_type (`str`, *optional*):
        Set to `"dataset"` or `"space"` if downloading from a dataset or space,
        `None` or `"model"` if downloading from a model. Default is `None`.
    revision (`str`, *optional*):
        An optional Git revision id which can be a branch name, a tag, or a
        commit hash.
    library_name (`str`, *optional*):
        The name of the library to which the object corresponds.
    library_version (`str`, *optional*):
        The version of the library.
    cache_dir (`str`, `Path`, *optional*):
        Path to the folder where cached files are stored.
    local_dir (`str` or `Path`, *optional*):
        If provided, the downloaded file will be placed under this directory.
    user_agent (`dict`, `str`, *optional*):
        The user-agent info in the form of a dictionary or a string.
    force_download (`bool`, *optional*, defaults to `False`):
        Whether the file should be downloaded even if it already exists in
        the local cache.
    proxies (`dict`, *optional*):
        Dictionary mapping protocol to the URL of the proxy passed to
        `requests.request`.
    etag_timeout (`float`, *optional*, defaults to `10`):
        When fetching ETag, how many seconds to wait for the server to send
        data before giving up which is passed to `requests.request`.
    token (`str`, `bool`, *optional*):
        A token to be used for the download.
            - If `True`, the token is read from the HuggingFace config
              folder.
            - If a string, it's used as the authentication token.
    local_files_only (`bool`, *optional*, defaults to `False`):
        If `True`, avoid downloading the file and return the path to the
        local cached file if it exists.
    headers (`dict`, *optional*):
        Additional headers to be sent with the request.

Returns:
    `str`: Local path of file or if networking is off, last version of file cached on disk.

Raises:
    [`~utils.RepositoryNotFoundError`]
        If the repository to download from cannot be found. This may be because it doesn't exist,
        or because it is set to `private` and you do not have access.
    [`~utils.RevisionNotFoundError`]
        If the revision to download from cannot be found.
    [`~utils.EntryNotFoundError`]
        If the file to download cannot be found.
    [`~utils.LocalEntryNotFoundError`]
        If network is disabled or unavailable and file is not found in cache.
    [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
        If `token=True` but the token cannot be found.
    [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError)
        If ETag cannot be determined.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If some parameter value is invalid.
```


### hf_hub_url

### huggingface_hub.hf_hub_url

```python
Construct the URL of a file from the given information.

The resolved address can either be a huggingface.co-hosted url, or a link to
Cloudfront (a Content Delivery Network, or CDN) for large files which are
more than a few MBs.

Args:
    repo_id (`str`):
        A namespace (user or an organization) name and a repo name separated
        by a `/`.
    filename (`str`):
        The name of the file in the repo.
    subfolder (`str`, *optional*):
        An optional value corresponding to a folder inside the repo.
    repo_type (`str`, *optional*):
        Set to `"dataset"` or `"space"` if downloading from a dataset or space,
        `None` or `"model"` if downloading from a model. Default is `None`.
    revision (`str`, *optional*):
        An optional Git revision id which can be a branch name, a tag, or a
        commit hash.

Example:

```python
>>> from huggingface_hub import hf_hub_url

>>> hf_hub_url(
...     repo_id="julien-c/EsperBERTo-small", filename="pytorch_model.bin"
... )
'https://huggingface.co/julien-c/EsperBERTo-small/resolve/main/pytorch_model.bin'
```

<Tip>

Notes:

    Cloudfront is replicated over the globe so downloads are way faster for
    the end user (and it also lowers our bandwidth costs).

    Cloudfront aggressively caches files by default (default TTL is 24
    hours), however this is not an issue here because we implement a
    git-based versioning system on huggingface.co, which means that we store
    the files on S3/Cloudfront in a content-addressable way (i.e., the file
    name is its hash). Using content-addressable filenames means cache can't
    ever be stale.

    In terms of client-side caching from this library, we base our caching
    on the objects' entity tag (`ETag`), which is an identifier of a
    specific version of a resource [1]_. An object's ETag is: its git-sha1
    if stored in git, or its sha256 if stored in git-lfs.

</Tip>

References:

-  [1] https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag
```


## Download a snapshot of the repo

### huggingface_hub.snapshot_download

```python
Download repo files.

Download a whole snapshot of a repo's files at the specified revision. This is useful when you want all files from
a repo, because you don't know which ones you will need a priori. All files are nested inside a folder in order
to keep their actual filename relative to that folder. You can also filter which files to download using
`allow_patterns` and `ignore_patterns`.

If `local_dir` is provided, the file structure from the repo will be replicated in this location. When using this
option, the `cache_dir` will not be used and a `.cache/huggingface/` folder will be created at the root of `local_dir`
to store some metadata related to the downloaded files. While this mechanism is not as robust as the main
cache-system, it's optimized for regularly pulling the latest version of a repository.

An alternative would be to clone the repo but this requires git and git-lfs to be installed and properly
configured. It is also not possible to filter which files to download when cloning a repository using git.

Args:
    repo_id (`str`):
        A user or an organization name and a repo name separated by a `/`.
    repo_type (`str`, *optional*):
        Set to `"dataset"` or `"space"` if downloading from a dataset or space,
        `None` or `"model"` if downloading from a model. Default is `None`.
    revision (`str`, *optional*):
        An optional Git revision id which can be a branch name, a tag, or a
        commit hash.
    cache_dir (`str`, `Path`, *optional*):
        Path to the folder where cached files are stored.
    local_dir (`str` or `Path`, *optional*):
        If provided, the downloaded files will be placed under this directory.
    library_name (`str`, *optional*):
        The name of the library to which the object corresponds.
    library_version (`str`, *optional*):
        The version of the library.
    user_agent (`str`, `dict`, *optional*):
        The user-agent info in the form of a dictionary or a string.
    proxies (`dict`, *optional*):
        Dictionary mapping protocol to the URL of the proxy passed to
        `requests.request`.
    etag_timeout (`float`, *optional*, defaults to `10`):
        When fetching ETag, how many seconds to wait for the server to send
        data before giving up which is passed to `requests.request`.
    force_download (`bool`, *optional*, defaults to `False`):
        Whether the file should be downloaded even if it already exists in the local cache.
    token (`str`, `bool`, *optional*):
        A token to be used for the download.
            - If `True`, the token is read from the HuggingFace config
              folder.
            - If a string, it's used as the authentication token.
    headers (`dict`, *optional*):
        Additional headers to include in the request. Those headers take precedence over the others.
    local_files_only (`bool`, *optional*, defaults to `False`):
        If `True`, avoid downloading the file and return the path to the
        local cached file if it exists.
    allow_patterns (`List[str]` or `str`, *optional*):
        If provided, only files matching at least one pattern are downloaded.
    ignore_patterns (`List[str]` or `str`, *optional*):
        If provided, files matching any of the patterns are not downloaded.
    max_workers (`int`, *optional*):
        Number of concurrent threads to download files (1 thread = 1 file download).
        Defaults to 8.
    tqdm_class (`tqdm`, *optional*):
        If provided, overwrites the default behavior for the progress bar. Passed
        argument must inherit from `tqdm.auto.tqdm` or at least mimic its behavior.
        Note that the `tqdm_class` is not passed to each individual download.
        Defaults to the custom HF progress bar that can be disabled by setting
        `HF_HUB_DISABLE_PROGRESS_BARS` environment variable.

Returns:
    `str`: folder path of the repo snapshot.

Raises:
    [`~utils.RepositoryNotFoundError`]
        If the repository to download from cannot be found. This may be because it doesn't exist,
        or because it is set to `private` and you do not have access.
    [`~utils.RevisionNotFoundError`]
        If the revision to download from cannot be found.
    [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
        If `token=True` and the token cannot be found.
    [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError) if
        ETag cannot be determined.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        if some parameter value is invalid.
```


## Get metadata about a file

### get_hf_file_metadata

### huggingface_hub.get_hf_file_metadata

```python
Fetch metadata of a file versioned on the Hub for a given url.

Args:
    url (`str`):
        File url, for example returned by [`hf_hub_url`].
    token (`str` or `bool`, *optional*):
        A token to be used for the download.
            - If `True`, the token is read from the HuggingFace config
              folder.
            - If `False` or `None`, no token is provided.
            - If a string, it's used as the authentication token.
    proxies (`dict`, *optional*):
        Dictionary mapping protocol to the URL of the proxy passed to
        `requests.request`.
    timeout (`float`, *optional*, defaults to 10):
        How many seconds to wait for the server to send metadata before giving up.
    library_name (`str`, *optional*):
        The name of the library to which the object corresponds.
    library_version (`str`, *optional*):
        The version of the library.
    user_agent (`dict`, `str`, *optional*):
        The user-agent info in the form of a dictionary or a string.
    headers (`dict`, *optional*):
        Additional headers to be sent with the request.

Returns:
    A [`HfFileMetadata`] object containing metadata such as location, etag, size and
    commit_hash.
```


### HfFileMetadata

### huggingface_hub.HfFileMetadata

```python
Data structure containing information about a file versioned on the Hub.

Returned by [`get_hf_file_metadata`] based on a URL.

Args:
    commit_hash (`str`, *optional*):
        The commit_hash related to the file.
    etag (`str`, *optional*):
        Etag of the file on the server.
    location (`str`):
        Location where to download the file. Can be a Hub url or not (CDN).
    size (`size`):
        Size of the file. In case of an LFS file, contains the size of the actual
        LFS file, not the pointer.
```


## Caching

The methods displayed above are designed to work with a caching system that prevents
re-downloading files. The caching system was updated in v0.8.0 to become the central
cache-system shared across libraries that depend on the Hub.

Read the [cache-system guide](../guides/manage-cache) for a detailed presentation of caching at
at HF.
