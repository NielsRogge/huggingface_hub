<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 파일 시스템 API[[filesystem-api]]

[`HfFileSystem`] 클래스는 [`fsspec`](https://filesystem-spec.readthedocs.io/en/latest/)을 기반으로 Hugging Face Hub에 Python 파일 인터페이스를 제공합니다.

## [HfFileSystem](Hf파일시스템)

[`HfFileSystem`]은 [`fsspec`](https://filesystem-spec.readthedocs.io/en/latest/)을 기반으로 하므로 제공되는 대부분의 API와 호환됩니다. 자세한 내용은 [가이드](../guides/hf_file_system) 및 fsspec의 [API 레퍼런스](https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.spec.AbstractFileSystem)를 확인하세요.

### HfFileSystem

```python
Access a remote Hugging Face Hub repository as if were a local file system.

<Tip warning={true}>

    [`HfFileSystem`] provides fsspec compatibility, which is useful for libraries that require it (e.g., reading
    Hugging Face datasets directly with `pandas`). However, it introduces additional overhead due to this compatibility
    layer. For better performance and reliability, it's recommended to use `HfApi` methods when possible.

</Tip>

Args:
    token (`str` or `bool`, *optional*):
        A valid user access token (string). Defaults to the locally saved
        token, which is the recommended method for authentication (see
        https://huggingface.co/docs/huggingface_hub/quick-start#authentication).
        To disable authentication, pass `False`.
    endpoint (`str`, *optional*):
        Endpoint of the Hub. Defaults to <https://huggingface.co>.
Usage:

```python
>>> from huggingface_hub import HfFileSystem

>>> fs = HfFileSystem()

>>> # List files
>>> fs.glob("my-username/my-model/*.bin")
['my-username/my-model/pytorch_model.bin']
>>> fs.ls("datasets/my-username/my-dataset", detail=False)
['datasets/my-username/my-dataset/.gitattributes', 'datasets/my-username/my-dataset/README.md', 'datasets/my-username/my-dataset/data.json']

>>> # Read/write files
>>> with fs.open("my-username/my-model/pytorch_model.bin") as f:
...     data = f.read()
>>> with fs.open("my-username/my-model/pytorch_model.bin", "wb") as f:
...     f.write(data)
```
```

    - __init__
    - resolve_path
    - ls
