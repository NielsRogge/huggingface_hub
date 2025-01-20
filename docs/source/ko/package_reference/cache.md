<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 캐시 시스템 참조[[cache-system-reference]]

버전 0.8.0에서의 업데이트로, 캐시 시스템은 Hub에 의존하는 라이브러리 전체에서 공유되는 중앙 캐시 시스템으로 발전하였습니다. Hugging Face 캐싱에 대한 자세한 설명은 [캐시 시스템 가이드](../guides/manage-cache)를 참조하세요.

## 도우미 함수[[helpers]]

### try_to_load_from_cache[[huggingface_hub.try_to_load_from_cache]]

### huggingface_hub.try_to_load_from_cache

```python
Explores the cache to return the latest cached file for a given revision if found.

This function will not raise any exception if the file in not cached.

Args:
    cache_dir (`str` or `os.PathLike`):
        The folder where the cached files lie.
    repo_id (`str`):
        The ID of the repo on huggingface.co.
    filename (`str`):
        The filename to look for inside `repo_id`.
    revision (`str`, *optional*):
        The specific model version to use. Will default to `"main"` if it's not provided and no `commit_hash` is
        provided either.
    repo_type (`str`, *optional*):
        The type of the repository. Will default to `"model"`.

Returns:
    `Optional[str]` or `_CACHED_NO_EXIST`:
        Will return `None` if the file was not cached. Otherwise:
        - The exact path to the cached file if it's found in the cache
        - A special value `_CACHED_NO_EXIST` if the file does not exist at the given commit hash and this fact was
          cached.

Example:

```python
from huggingface_hub import try_to_load_from_cache, _CACHED_NO_EXIST

filepath = try_to_load_from_cache()
if isinstance(filepath, str):
    # file exists and is cached
    ...
elif filepath is _CACHED_NO_EXIST:
    # non-existence of file is cached
    ...
else:
    # file is not cached
    ...
```
```


### cached_assets_path[[huggingface_hub.cached_assets_path]]

### huggingface_hub.cached_assets_path

```python
Return a folder path to cache arbitrary files.

`huggingface_hub` provides a canonical folder path to store assets. This is the
recommended way to integrate cache in a downstream library as it will benefit from
the builtins tools to scan and delete the cache properly.

The distinction is made between files cached from the Hub and assets. Files from the
Hub are cached in a git-aware manner and entirely managed by `huggingface_hub`. See
[related documentation](https://huggingface.co/docs/huggingface_hub/how-to-cache).
All other files that a downstream library caches are considered to be "assets"
(files downloaded from external sources, extracted from a .tar archive, preprocessed
for training,...).

Once the folder path is generated, it is guaranteed to exist and to be a directory.
The path is based on 3 levels of depth: the library name, a namespace and a
subfolder. Those 3 levels grants flexibility while allowing `huggingface_hub` to
expect folders when scanning/deleting parts of the assets cache. Within a library,
it is expected that all namespaces share the same subset of subfolder names but this
is not a mandatory rule. The downstream library has then full control on which file
structure to adopt within its cache. Namespace and subfolder are optional (would
default to a `"default/"` subfolder) but library name is mandatory as we want every
downstream library to manage its own cache.

Expected tree:
```text
    assets/
    └── datasets/
    │   ├── SQuAD/
    │   │   ├── downloaded/
    │   │   ├── extracted/
    │   │   └── processed/
    │   ├── Helsinki-NLP--tatoeba_mt/
    │       ├── downloaded/
    │       ├── extracted/
    │       └── processed/
    └── transformers/
        ├── default/
        │   ├── something/
        ├── bert-base-cased/
        │   ├── default/
        │   └── training/
    hub/
    └── models--julien-c--EsperBERTo-small/
        ├── blobs/
        │   ├── (...)
        │   ├── (...)
        ├── refs/
        │   └── (...)
        └── [ 128]  snapshots/
            ├── 2439f60ef33a0d46d85da5001d52aeda5b00ce9f/
            │   ├── (...)
            └── bbc77c8132af1cc5cf678da3f1ddf2de43606d48/
                └── (...)
```


Args:
    library_name (`str`):
        Name of the library that will manage the cache folder. Example: `"dataset"`.
    namespace (`str`, *optional*, defaults to "default"):
        Namespace to which the data belongs. Example: `"SQuAD"`.
    subfolder (`str`, *optional*, defaults to "default"):
        Subfolder in which the data will be stored. Example: `extracted`.
    assets_dir (`str`, `Path`, *optional*):
        Path to the folder where assets are cached. This must not be the same folder
        where Hub files are cached. Defaults to `HF_HOME / "assets"` if not provided.
        Can also be set with `HF_ASSETS_CACHE` environment variable.

Returns:
    Path to the cache folder (`Path`).

Example:
```py
>>> from huggingface_hub import cached_assets_path

>>> cached_assets_path(library_name="datasets", namespace="SQuAD", subfolder="download")
PosixPath('/home/wauplin/.cache/huggingface/extra/datasets/SQuAD/download')

>>> cached_assets_path(library_name="datasets", namespace="SQuAD", subfolder="extracted")
PosixPath('/home/wauplin/.cache/huggingface/extra/datasets/SQuAD/extracted')

>>> cached_assets_path(library_name="datasets", namespace="Helsinki-NLP/tatoeba_mt")
PosixPath('/home/wauplin/.cache/huggingface/extra/datasets/Helsinki-NLP--tatoeba_mt/default')

>>> cached_assets_path(library_name="datasets", assets_dir="/tmp/tmp123456")
PosixPath('/tmp/tmp123456/datasets/default/default')
```
```


### scan_cache_dir[[huggingface_hub.scan_cache_dir]]

### huggingface_hub.scan_cache_dir

```python
Scan the entire HF cache-system and return a [`~HFCacheInfo`] structure.

Use `scan_cache_dir` in order to programmatically scan your cache-system. The cache
will be scanned repo by repo. If a repo is corrupted, a [`~CorruptedCacheException`]
will be thrown internally but captured and returned in the [`~HFCacheInfo`]
structure. Only valid repos get a proper report.

```py
>>> from huggingface_hub import scan_cache_dir

>>> hf_cache_info = scan_cache_dir()
HFCacheInfo(
    size_on_disk=3398085269,
    repos=frozenset({
        CachedRepoInfo(
            repo_id='t5-small',
            repo_type='model',
            repo_path=PosixPath(...),
            size_on_disk=970726914,
            nb_files=11,
            revisions=frozenset({
                CachedRevisionInfo(
                    commit_hash='d78aea13fa7ecd06c29e3e46195d6341255065d5',
                    size_on_disk=970726339,
                    snapshot_path=PosixPath(...),
                    files=frozenset({
                        CachedFileInfo(
                            file_name='config.json',
                            size_on_disk=1197
                            file_path=PosixPath(...),
                            blob_path=PosixPath(...),
                        ),
                        CachedFileInfo(...),
                        ...
                    }),
                ),
                CachedRevisionInfo(...),
                ...
            }),
        ),
        CachedRepoInfo(...),
        ...
    }),
    warnings=[
        CorruptedCacheException("Snapshots dir doesn't exist in cached repo: ..."),
        CorruptedCacheException(...),
        ...
    ],
)
```

You can also print a detailed report directly from the `huggingface-cli` using:
```text
> huggingface-cli scan-cache
REPO ID                     REPO TYPE SIZE ON DISK NB FILES REFS                LOCAL PATH
--------------------------- --------- ------------ -------- ------------------- -------------------------------------------------------------------------
glue                        dataset         116.3K       15 1.17.0, main, 2.4.0 /Users/lucain/.cache/huggingface/hub/datasets--glue
google/fleurs               dataset          64.9M        6 main, refs/pr/1     /Users/lucain/.cache/huggingface/hub/datasets--google--fleurs
Jean-Baptiste/camembert-ner model           441.0M        7 main                /Users/lucain/.cache/huggingface/hub/models--Jean-Baptiste--camembert-ner
bert-base-cased             model             1.9G       13 main                /Users/lucain/.cache/huggingface/hub/models--bert-base-cased
t5-base                     model            10.1K        3 main                /Users/lucain/.cache/huggingface/hub/models--t5-base
t5-small                    model           970.7M       11 refs/pr/1, main     /Users/lucain/.cache/huggingface/hub/models--t5-small

Done in 0.0s. Scanned 6 repo(s) for a total of 3.4G.
Got 1 warning(s) while scanning. Use -vvv to print details.
```

Args:
    cache_dir (`str` or `Path`, `optional`):
        Cache directory to cache. Defaults to the default HF cache directory.

<Tip warning={true}>

Raises:

    `CacheNotFound`
      If the cache directory does not exist.

    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
      If the cache directory is a file, instead of a directory.

</Tip>

Returns: a [`~HFCacheInfo`] object.
```


## 데이터 구조[[data-structures]]

모든 구조체는 [`scan_cache_dir`]에 의해 생성되고 반환되며, 불변(immutable)입니다.

### HFCacheInfo[[huggingface_hub.HFCacheInfo]]

### huggingface_hub.HFCacheInfo

```python
Frozen data structure holding information about the entire cache-system.

This data structure is returned by [`scan_cache_dir`] and is immutable.

Args:
    size_on_disk (`int`):
        Sum of all valid repo sizes in the cache-system.
    repos (`FrozenSet[CachedRepoInfo]`):
        Set of [`~CachedRepoInfo`] describing all valid cached repos found on the
        cache-system while scanning.
    warnings (`List[CorruptedCacheException]`):
        List of [`~CorruptedCacheException`] that occurred while scanning the cache.
        Those exceptions are captured so that the scan can continue. Corrupted repos
        are skipped from the scan.

<Tip warning={true}>

Here `size_on_disk` is equal to the sum of all repo sizes (only blobs). However if
some cached repos are corrupted, their sizes are not taken into account.

</Tip>
```


### CachedRepoInfo[[huggingface_hub.CachedRepoInfo]]

### huggingface_hub.CachedRepoInfo

```python
Frozen data structure holding information about a cached repository.

Args:
    repo_id (`str`):
        Repo id of the repo on the Hub. Example: `"google/fleurs"`.
    repo_type (`Literal["dataset", "model", "space"]`):
        Type of the cached repo.
    repo_path (`Path`):
        Local path to the cached repo.
    size_on_disk (`int`):
        Sum of the blob file sizes in the cached repo.
    nb_files (`int`):
        Total number of blob files in the cached repo.
    revisions (`FrozenSet[CachedRevisionInfo]`):
        Set of [`~CachedRevisionInfo`] describing all revisions cached in the repo.
    last_accessed (`float`):
        Timestamp of the last time a blob file of the repo has been accessed.
    last_modified (`float`):
        Timestamp of the last time a blob file of the repo has been modified/created.

<Tip warning={true}>

`size_on_disk` is not necessarily the sum of all revisions sizes because of
duplicated files. Besides, only blobs are taken into account, not the (negligible)
size of folders and symlinks.

</Tip>

<Tip warning={true}>

`last_accessed` and `last_modified` reliability can depend on the OS you are using.
See [python documentation](https://docs.python.org/3/library/os.html#os.stat_result)
for more details.

</Tip>
```

    - size_on_disk_str
    - refs

### CachedRevisionInfo[[huggingface_hub.CachedRevisionInfo]]

### huggingface_hub.CachedRevisionInfo

```python
Frozen data structure holding information about a revision.

A revision correspond to a folder in the `snapshots` folder and is populated with
the exact tree structure as the repo on the Hub but contains only symlinks. A
revision can be either referenced by 1 or more `refs` or be "detached" (no refs).

Args:
    commit_hash (`str`):
        Hash of the revision (unique).
        Example: `"9338f7b671827df886678df2bdd7cc7b4f36dffd"`.
    snapshot_path (`Path`):
        Path to the revision directory in the `snapshots` folder. It contains the
        exact tree structure as the repo on the Hub.
    files: (`FrozenSet[CachedFileInfo]`):
        Set of [`~CachedFileInfo`] describing all files contained in the snapshot.
    refs (`FrozenSet[str]`):
        Set of `refs` pointing to this revision. If the revision has no `refs`, it
        is considered detached.
        Example: `{"main", "2.4.0"}` or `{"refs/pr/1"}`.
    size_on_disk (`int`):
        Sum of the blob file sizes that are symlink-ed by the revision.
    last_modified (`float`):
        Timestamp of the last time the revision has been created/modified.

<Tip warning={true}>

`last_accessed` cannot be determined correctly on a single revision as blob files
are shared across revisions.

</Tip>

<Tip warning={true}>

`size_on_disk` is not necessarily the sum of all file sizes because of possible
duplicated files. Besides, only blobs are taken into account, not the (negligible)
size of folders and symlinks.

</Tip>
```

    - size_on_disk_str
    - nb_files

### CachedFileInfo[[huggingface_hub.CachedFileInfo]]

### huggingface_hub.CachedFileInfo

```python
Frozen data structure holding information about a single cached file.

Args:
    file_name (`str`):
        Name of the file. Example: `config.json`.
    file_path (`Path`):
        Path of the file in the `snapshots` directory. The file path is a symlink
        referring to a blob in the `blobs` folder.
    blob_path (`Path`):
        Path of the blob file. This is equivalent to `file_path.resolve()`.
    size_on_disk (`int`):
        Size of the blob file in bytes.
    blob_last_accessed (`float`):
        Timestamp of the last time the blob file has been accessed (from any
        revision).
    blob_last_modified (`float`):
        Timestamp of the last time the blob file has been modified/created.

<Tip warning={true}>

`blob_last_accessed` and `blob_last_modified` reliability can depend on the OS you
are using. See [python documentation](https://docs.python.org/3/library/os.html#os.stat_result)
for more details.

</Tip>
```

    - size_on_disk_str

### DeleteCacheStrategy[[huggingface_hub.DeleteCacheStrategy]]

### huggingface_hub.DeleteCacheStrategy

```python
Frozen data structure holding the strategy to delete cached revisions.

This object is not meant to be instantiated programmatically but to be returned by
[`~utils.HFCacheInfo.delete_revisions`]. See documentation for usage example.

Args:
    expected_freed_size (`float`):
        Expected freed size once strategy is executed.
    blobs (`FrozenSet[Path]`):
        Set of blob file paths to be deleted.
    refs (`FrozenSet[Path]`):
        Set of reference file paths to be deleted.
    repos (`FrozenSet[Path]`):
        Set of entire repo paths to be deleted.
    snapshots (`FrozenSet[Path]`):
        Set of snapshots to be deleted (directory of symlinks).
```

    - expected_freed_size_str

## 예외[[exceptions]]

### CorruptedCacheException[[huggingface_hub.CorruptedCacheException]]

### huggingface_hub.CorruptedCacheException

```python
Exception for any unexpected structure in the Huggingface cache-system.
```

