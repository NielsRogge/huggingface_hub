<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Serialization

`huggingface_hub` provides helpers to save and load ML model weights in a standardized way. This part of the library is still under development and will be improved in future releases. The goal is to harmonize how weights are saved and loaded across the Hub, both to remove code duplication across libraries and to establish consistent conventions.

## DDUF file format

DDUF is a file format designed for diffusion models. It allows saving all the information to run a model in a single file. This work is inspired by the [GGUF](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md) format. `huggingface_hub` provides helpers to save and load DDUF files, ensuring the file format is respected.

<Tip warning={true}>

This is a very early version of the parser. The API and implementation can evolve in the near future.

The parser currently does very little validation. For more details about the file format, check out https://github.com/huggingface/huggingface.js/tree/main/packages/dduf.

</Tip>

### How to write a DDUF file?

Here is how to export a folder containing different parts of a diffusion model using [`export_folder_as_dduf`]:

```python
# Export a folder as a DDUF file
>>> from huggingface_hub import export_folder_as_dduf
>>> export_folder_as_dduf("FLUX.1-dev.dduf", folder_path="path/to/FLUX.1-dev")
```

For more flexibility, you can use [`export_entries_as_dduf`] and pass a list of files to include in the final DDUF file:

```python
# Export specific files from the local disk.
>>> from huggingface_hub import export_entries_as_dduf
>>> export_entries_as_dduf(
...     dduf_path="stable-diffusion-v1-4-FP16.dduf",
...     entries=[ # List entries to add to the DDUF file (here, only FP16 weights)
...         ("model_index.json", "path/to/model_index.json"),
...         ("vae/config.json", "path/to/vae/config.json"),
...         ("vae/diffusion_pytorch_model.fp16.safetensors", "path/to/vae/diffusion_pytorch_model.fp16.safetensors"),
...         ("text_encoder/config.json", "path/to/text_encoder/config.json"),
...         ("text_encoder/model.fp16.safetensors", "path/to/text_encoder/model.fp16.safetensors"),
...         # ... add more entries here
...     ]
... )
```

The `entries` parameter also supports passing an iterable of paths or bytes. This can prove useful if you have a loaded model and want to serialize it directly into a DDUF file instead of having to serialize each component to disk first and then as a DDUF file. Here is an example of how a `StableDiffusionPipeline` can be serialized as DDUF:


```python
# Export state_dicts one by one from a loaded pipeline 
>>> from diffusers import DiffusionPipeline
>>> from typing import Generator, Tuple
>>> import safetensors.torch
>>> from huggingface_hub import export_entries_as_dduf
>>> pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
... # ... do some work with the pipeline

>>> def as_entries(pipe: DiffusionPipeline) -> Generator[Tuple[str, bytes], None, None]:
...     # Build a generator that yields the entries to add to the DDUF file.
...     # The first element of the tuple is the filename in the DDUF archive (must use UNIX separator!). The second element is the content of the file.
...     # Entries will be evaluated lazily when the DDUF file is created (only 1 entry is loaded in memory at a time)
...     yield "vae/config.json", pipe.vae.to_json_string().encode()
...     yield "vae/diffusion_pytorch_model.safetensors", safetensors.torch.save(pipe.vae.state_dict())
...     yield "text_encoder/config.json", pipe.text_encoder.config.to_json_string().encode()
...     yield "text_encoder/model.safetensors", safetensors.torch.save(pipe.text_encoder.state_dict())
...     # ... add more entries here

>>> export_entries_as_dduf(dduf_path="stable-diffusion-v1-4.dduf", entries=as_entries(pipe))
```

**Note:** in practice, `diffusers` provides a method to directly serialize a pipeline in a DDUF file. The snippet above is only meant as an example.

### How to read a DDUF file?

```python
>>> import json
>>> import safetensors.torch
>>> from huggingface_hub import read_dduf_file

# Read DDUF metadata
>>> dduf_entries = read_dduf_file("FLUX.1-dev.dduf")

# Returns a mapping filename <> DDUFEntry
>>> dduf_entries["model_index.json"]
DDUFEntry(filename='model_index.json', offset=66, length=587)

# Load model index as JSON
>>> json.loads(dduf_entries["model_index.json"].read_text())
{'_class_name': 'FluxPipeline', '_diffusers_version': '0.32.0.dev0', '_name_or_path': 'black-forest-labs/FLUX.1-dev', 'scheduler': ['diffusers', 'FlowMatchEulerDiscreteScheduler'], 'text_encoder': ['transformers', 'CLIPTextModel'], 'text_encoder_2': ['transformers', 'T5EncoderModel'], 'tokenizer': ['transformers', 'CLIPTokenizer'], 'tokenizer_2': ['transformers', 'T5TokenizerFast'], 'transformer': ['diffusers', 'FluxTransformer2DModel'], 'vae': ['diffusers', 'AutoencoderKL']}

# Load VAE weights using safetensors
>>> with dduf_entries["vae/diffusion_pytorch_model.safetensors"].as_mmap() as mm:
...     state_dict = safetensors.torch.load(mm)
```

### Helpers

### huggingface_hub.export_entries_as_dduf

```python
Write a DDUF file from an iterable of entries.

This is a lower-level helper than [`export_folder_as_dduf`] that allows more flexibility when serializing data.
In particular, you don't need to save the data on disk before exporting it in the DDUF file.

Args:
    dduf_path (`str` or `os.PathLike`):
        The path to the DDUF file to write.
    entries (`Iterable[Tuple[str, Union[str, Path, bytes]]]`):
        An iterable of entries to write in the DDUF file. Each entry is a tuple with the filename and the content.
        The filename should be the path to the file in the DDUF archive.
        The content can be a string or a pathlib.Path representing a path to a file on the local disk or directly the content as bytes.

Raises:
    - [`DDUFExportError`]: If anything goes wrong during the export (e.g. invalid entry name, missing 'model_index.json', etc.).

Example:
    ```python
    # Export specific files from the local disk.
    >>> from huggingface_hub import export_entries_as_dduf
    >>> export_entries_as_dduf(
    ...     dduf_path="stable-diffusion-v1-4-FP16.dduf",
    ...     entries=[ # List entries to add to the DDUF file (here, only FP16 weights)
    ...         ("model_index.json", "path/to/model_index.json"),
    ...         ("vae/config.json", "path/to/vae/config.json"),
    ...         ("vae/diffusion_pytorch_model.fp16.safetensors", "path/to/vae/diffusion_pytorch_model.fp16.safetensors"),
    ...         ("text_encoder/config.json", "path/to/text_encoder/config.json"),
    ...         ("text_encoder/model.fp16.safetensors", "path/to/text_encoder/model.fp16.safetensors"),
    ...         # ... add more entries here
    ...     ]
    ... )
    ```

    ```python
    # Export state_dicts one by one from a loaded pipeline
    >>> from diffusers import DiffusionPipeline
    >>> from typing import Generator, Tuple
    >>> import safetensors.torch
    >>> from huggingface_hub import export_entries_as_dduf
    >>> pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    ... # ... do some work with the pipeline

    >>> def as_entries(pipe: DiffusionPipeline) -> Generator[Tuple[str, bytes], None, None]:
    ...     # Build an generator that yields the entries to add to the DDUF file.
    ...     # The first element of the tuple is the filename in the DDUF archive (must use UNIX separator!). The second element is the content of the file.
    ...     # Entries will be evaluated lazily when the DDUF file is created (only 1 entry is loaded in memory at a time)
    ...     yield "vae/config.json", pipe.vae.to_json_string().encode()
    ...     yield "vae/diffusion_pytorch_model.safetensors", safetensors.torch.save(pipe.vae.state_dict())
    ...     yield "text_encoder/config.json", pipe.text_encoder.config.to_json_string().encode()
    ...     yield "text_encoder/model.safetensors", safetensors.torch.save(pipe.text_encoder.state_dict())
    ...     # ... add more entries here

    >>> export_entries_as_dduf(dduf_path="stable-diffusion-v1-4.dduf", entries=as_entries(pipe))
    ```
```


### huggingface_hub.export_folder_as_dduf

```python
Export a folder as a DDUF file.

AUses [`export_entries_as_dduf`] under the hood.

Args:
    dduf_path (`str` or `os.PathLike`):
        The path to the DDUF file to write.
    folder_path (`str` or `os.PathLike`):
        The path to the folder containing the diffusion model.

Example:
    ```python
    >>> from huggingface_hub import export_folder_as_dduf
    >>> export_folder_as_dduf(dduf_path="FLUX.1-dev.dduf", folder_path="path/to/FLUX.1-dev")
    ```
```


### huggingface_hub.read_dduf_file

```python
Read a DDUF file and return a dictionary of entries.

Only the metadata is read, the data is not loaded in memory.

Args:
    dduf_path (`str` or `os.PathLike`):
        The path to the DDUF file to read.

Returns:
    `Dict[str, DDUFEntry]`:
        A dictionary of [`DDUFEntry`] indexed by filename.

Raises:
    - [`DDUFCorruptedFileError`]: If the DDUF file is corrupted (i.e. doesn't follow the DDUF format).

Example:
    ```python
    >>> import json
    >>> import safetensors.torch
    >>> from huggingface_hub import read_dduf_file

    # Read DDUF metadata
    >>> dduf_entries = read_dduf_file("FLUX.1-dev.dduf")

    # Returns a mapping filename <> DDUFEntry
    >>> dduf_entries["model_index.json"]
    DDUFEntry(filename='model_index.json', offset=66, length=587)

    # Load model index as JSON
    >>> json.loads(dduf_entries["model_index.json"].read_text())
    {'_class_name': 'FluxPipeline', '_diffusers_version': '0.32.0.dev0', '_name_or_path': 'black-forest-labs/FLUX.1-dev', ...

    # Load VAE weights using safetensors
    >>> with dduf_entries["vae/diffusion_pytorch_model.safetensors"].as_mmap() as mm:
    ...     state_dict = safetensors.torch.load(mm)
    ```
```


### huggingface_hub.DDUFEntry

```python
Object representing a file entry in a DDUF file.

See [`read_dduf_file`] for how to read a DDUF file.

Attributes:
    filename (str):
        The name of the file in the DDUF archive.
    offset (int):
        The offset of the file in the DDUF archive.
    length (int):
        The length of the file in the DDUF archive.
    dduf_path (str):
        The path to the DDUF archive (for internal use).
```


### Errors

### huggingface_hub.errors.DDUFError

```python
Base exception for errors related to the DDUF format.
```


### huggingface_hub.errors.DDUFCorruptedFileError

```python
Exception thrown when the DDUF file is corrupted.
```


### huggingface_hub.errors.DDUFExportError

```python
Base exception for errors during DDUF export.
```


### huggingface_hub.errors.DDUFInvalidEntryNameError

```python
Exception thrown when the entry name is invalid.
```


## Saving tensors

The main helper of the `serialization` module takes a torch `nn.Module` as input and saves it to disk. It handles the logic to save shared tensors (see [safetensors explanation](https://huggingface.co/docs/safetensors/torch_shared_tensors)) as well as logic to split the state dictionary into shards, using [`split_torch_state_dict_into_shards`] under the hood. At the moment, only `torch` framework is supported.

If you want to save a state dictionary (e.g. a mapping between layer names and related tensors) instead of a `nn.Module`, you can use [`save_torch_state_dict`] which provides the same features. This is useful for example if you want to apply custom logic to the state dict before saving it.

### save_torch_model

### huggingface_hub.save_torch_model

```python
Saves a given torch model to disk, handling sharding and shared tensors issues.

See also [`save_torch_state_dict`] to save a state dict with more flexibility.

For more information about tensor sharing, check out [this guide](https://huggingface.co/docs/safetensors/torch_shared_tensors).

The model state dictionary is split into shards so that each shard is smaller than a given size. The shards are
saved in the `save_directory` with the given `filename_pattern`. If the model is too big to fit in a single shard,
an index file is saved in the `save_directory` to indicate where each tensor is saved. This helper uses
[`split_torch_state_dict_into_shards`] under the hood. If `safe_serialization` is `True`, the shards are saved as
safetensors (the default). Otherwise, the shards are saved as pickle.

Before saving the model, the `save_directory` is cleaned from any previous shard files.

<Tip warning={true}>

If one of the model's tensor is bigger than `max_shard_size`, it will end up in its own shard which will have a
size greater than `max_shard_size`.

</Tip>

<Tip warning={true}>

If your model is a `transformers.PreTrainedModel`, you should pass `model._tied_weights_keys` as `shared_tensors_to_discard` to properly handle shared tensors saving. This ensures the correct duplicate tensors are discarded during saving.

</Tip>

Args:
    model (`torch.nn.Module`):
        The model to save on disk.
    save_directory (`str` or `Path`):
        The directory in which the model will be saved.
    filename_pattern (`str`, *optional*):
        The pattern to generate the files names in which the model will be saved. Pattern must be a string that
        can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
        Defaults to `"model{suffix}.safetensors"` or `pytorch_model{suffix}.bin` depending on `safe_serialization`
        parameter.
    force_contiguous (`boolean`, *optional*):
        Forcing the state_dict to be saved as contiguous tensors. This has no effect on the correctness of the
        model, but it could potentially change performance if the layout of the tensor was chosen specifically for
        that reason. Defaults to `True`.
    max_shard_size (`int` or `str`, *optional*):
        The maximum size of each shard, in bytes. Defaults to 5GB.
    metadata (`Dict[str, str]`, *optional*):
        Extra information to save along with the model. Some metadata will be added for each dropped tensors.
        This information will not be enough to recover the entire shared structure but might help understanding
        things.
    safe_serialization (`bool`, *optional*):
        Whether to save as safetensors, which is the default behavior. If `False`, the shards are saved as pickle.
        Safe serialization is recommended for security reasons. Saving as pickle is deprecated and will be removed
        in a future version.
    is_main_process (`bool`, *optional*):
        Whether the process calling this is the main process or not. Useful when in distributed training like
        TPUs and need to call this function from all processes. In this case, set `is_main_process=True` only on
        the main process to avoid race conditions. Defaults to True.
    shared_tensors_to_discard (`List[str]`, *optional*):
        List of tensor names to drop when saving shared tensors. If not provided and shared tensors are
        detected, it will drop the first name alphabetically.

Example:

```py
>>> from huggingface_hub import save_torch_model
>>> model = ... # A PyTorch model

# Save state dict to "path/to/folder". The model will be split into shards of 5GB each and saved as safetensors.
>>> save_torch_model(model, "path/to/folder")

# Load model back
>>> from huggingface_hub import load_torch_model  # TODO
>>> load_torch_model(model, "path/to/folder")
>>>
```
```


### save_torch_state_dict

### huggingface_hub.save_torch_state_dict

```python
Save a model state dictionary to the disk, handling sharding and shared tensors issues.

See also [`save_torch_model`] to directly save a PyTorch model.

For more information about tensor sharing, check out [this guide](https://huggingface.co/docs/safetensors/torch_shared_tensors).

The model state dictionary is split into shards so that each shard is smaller than a given size. The shards are
saved in the `save_directory` with the given `filename_pattern`. If the model is too big to fit in a single shard,
an index file is saved in the `save_directory` to indicate where each tensor is saved. This helper uses
[`split_torch_state_dict_into_shards`] under the hood. If `safe_serialization` is `True`, the shards are saved as
safetensors (the default). Otherwise, the shards are saved as pickle.

Before saving the model, the `save_directory` is cleaned from any previous shard files.

<Tip warning={true}>

If one of the model's tensor is bigger than `max_shard_size`, it will end up in its own shard which will have a
size greater than `max_shard_size`.

</Tip>

<Tip warning={true}>

If your model is a `transformers.PreTrainedModel`, you should pass `model._tied_weights_keys` as `shared_tensors_to_discard` to properly handle shared tensors saving. This ensures the correct duplicate tensors are discarded during saving.

</Tip>

Args:
    state_dict (`Dict[str, torch.Tensor]`):
        The state dictionary to save.
    save_directory (`str` or `Path`):
        The directory in which the model will be saved.
    filename_pattern (`str`, *optional*):
        The pattern to generate the files names in which the model will be saved. Pattern must be a string that
        can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
        Defaults to `"model{suffix}.safetensors"` or `pytorch_model{suffix}.bin` depending on `safe_serialization`
        parameter.
    force_contiguous (`boolean`, *optional*):
        Forcing the state_dict to be saved as contiguous tensors. This has no effect on the correctness of the
        model, but it could potentially change performance if the layout of the tensor was chosen specifically for
        that reason. Defaults to `True`.
    max_shard_size (`int` or `str`, *optional*):
        The maximum size of each shard, in bytes. Defaults to 5GB.
    metadata (`Dict[str, str]`, *optional*):
        Extra information to save along with the model. Some metadata will be added for each dropped tensors.
        This information will not be enough to recover the entire shared structure but might help understanding
        things.
    safe_serialization (`bool`, *optional*):
        Whether to save as safetensors, which is the default behavior. If `False`, the shards are saved as pickle.
        Safe serialization is recommended for security reasons. Saving as pickle is deprecated and will be removed
        in a future version.
    is_main_process (`bool`, *optional*):
        Whether the process calling this is the main process or not. Useful when in distributed training like
        TPUs and need to call this function from all processes. In this case, set `is_main_process=True` only on
        the main process to avoid race conditions. Defaults to True.
    shared_tensors_to_discard (`List[str]`, *optional*):
        List of tensor names to drop when saving shared tensors. If not provided and shared tensors are
        detected, it will drop the first name alphabetically.

Example:

```py
>>> from huggingface_hub import save_torch_state_dict
>>> model = ... # A PyTorch model

# Save state dict to "path/to/folder". The model will be split into shards of 5GB each and saved as safetensors.
>>> state_dict = model_to_save.state_dict()
>>> save_torch_state_dict(state_dict, "path/to/folder")
```
```



The `serialization` module also contains low-level helpers to split a state dictionary into several shards, while creating a proper index in the process. These helpers are available for `torch` and `tensorflow` tensors and are designed to be easily extended to any other ML frameworks.

### split_tf_state_dict_into_shards

### huggingface_hub.split_tf_state_dict_into_shards

```python
Split a model state dictionary in shards so that each shard is smaller than a given size.

The shards are determined by iterating through the `state_dict` in the order of its keys. There is no optimization
made to make each shard as close as possible to the maximum size passed. For example, if the limit is 10GB and we
have tensors of sizes [6GB, 6GB, 2GB, 6GB, 2GB, 2GB] they will get sharded as [6GB], [6+2GB], [6+2+2GB] and not
[6+2+2GB], [6+2GB], [6GB].

<Tip warning={true}>

If one of the model's tensor is bigger than `max_shard_size`, it will end up in its own shard which will have a
size greater than `max_shard_size`.

</Tip>

Args:
    state_dict (`Dict[str, Tensor]`):
        The state dictionary to save.
    filename_pattern (`str`, *optional*):
        The pattern to generate the files names in which the model will be saved. Pattern must be a string that
        can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
        Defaults to `"tf_model{suffix}.h5"`.
    max_shard_size (`int` or `str`, *optional*):
        The maximum size of each shard, in bytes. Defaults to 5GB.

Returns:
    [`StateDictSplit`]: A `StateDictSplit` object containing the shards and the index to retrieve them.
```


### split_torch_state_dict_into_shards

### huggingface_hub.split_torch_state_dict_into_shards

```python
Split a model state dictionary in shards so that each shard is smaller than a given size.

The shards are determined by iterating through the `state_dict` in the order of its keys. There is no optimization
made to make each shard as close as possible to the maximum size passed. For example, if the limit is 10GB and we
have tensors of sizes [6GB, 6GB, 2GB, 6GB, 2GB, 2GB] they will get sharded as [6GB], [6+2GB], [6+2+2GB] and not
[6+2+2GB], [6+2GB], [6GB].


<Tip>

To save a model state dictionary to the disk, see [`save_torch_state_dict`]. This helper uses
`split_torch_state_dict_into_shards` under the hood.

</Tip>

<Tip warning={true}>

If one of the model's tensor is bigger than `max_shard_size`, it will end up in its own shard which will have a
size greater than `max_shard_size`.

</Tip>

Args:
    state_dict (`Dict[str, torch.Tensor]`):
        The state dictionary to save.
    filename_pattern (`str`, *optional*):
        The pattern to generate the files names in which the model will be saved. Pattern must be a string that
        can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
        Defaults to `"model{suffix}.safetensors"`.
    max_shard_size (`int` or `str`, *optional*):
        The maximum size of each shard, in bytes. Defaults to 5GB.

Returns:
    [`StateDictSplit`]: A `StateDictSplit` object containing the shards and the index to retrieve them.

Example:
```py
>>> import json
>>> import os
>>> from safetensors.torch import save_file as safe_save_file
>>> from huggingface_hub import split_torch_state_dict_into_shards

>>> def save_state_dict(state_dict: Dict[str, torch.Tensor], save_directory: str):
...     state_dict_split = split_torch_state_dict_into_shards(state_dict)
...     for filename, tensors in state_dict_split.filename_to_tensors.items():
...         shard = {tensor: state_dict[tensor] for tensor in tensors}
...         safe_save_file(
...             shard,
...             os.path.join(save_directory, filename),
...             metadata={"format": "pt"},
...         )
...     if state_dict_split.is_sharded:
...         index = {
...             "metadata": state_dict_split.metadata,
...             "weight_map": state_dict_split.tensor_to_filename,
...         }
...         with open(os.path.join(save_directory, "model.safetensors.index.json"), "w") as f:
...             f.write(json.dumps(index, indent=2))
```
```


### split_state_dict_into_shards_factory

This is the underlying factory from which each framework-specific helper is derived. In practice, you are not expected to use this factory directly except if you need to adapt it to a framework that is not yet supported. If that is the case, please let us know by [opening a new issue](https://github.com/huggingface/huggingface_hub/issues/new) on the `huggingface_hub` repo.

### huggingface_hub.split_state_dict_into_shards_factory

```python
Split a model state dictionary in shards so that each shard is smaller than a given size.

The shards are determined by iterating through the `state_dict` in the order of its keys. There is no optimization
made to make each shard as close as possible to the maximum size passed. For example, if the limit is 10GB and we
have tensors of sizes [6GB, 6GB, 2GB, 6GB, 2GB, 2GB] they will get sharded as [6GB], [6+2GB], [6+2+2GB] and not
[6+2+2GB], [6+2GB], [6GB].

<Tip warning={true}>

If one of the model's tensor is bigger than `max_shard_size`, it will end up in its own shard which will have a
size greater than `max_shard_size`.

</Tip>

Args:
    state_dict (`Dict[str, Tensor]`):
        The state dictionary to save.
    get_storage_size (`Callable[[Tensor], int]`):
        A function that returns the size of a tensor when saved on disk in bytes.
    get_storage_id (`Callable[[Tensor], Optional[Any]]`, *optional*):
        A function that returns a unique identifier to a tensor storage. Multiple different tensors can share the
        same underlying storage. This identifier is guaranteed to be unique and constant for this tensor's storage
        during its lifetime. Two tensor storages with non-overlapping lifetimes may have the same id.
    filename_pattern (`str`, *optional*):
        The pattern to generate the files names in which the model will be saved. Pattern must be a string that
        can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
    max_shard_size (`int` or `str`, *optional*):
        The maximum size of each shard, in bytes. Defaults to 5GB.

Returns:
    [`StateDictSplit`]: A `StateDictSplit` object containing the shards and the index to retrieve them.
```


## Loading tensors

The loading helpers support both single-file and sharded checkpoints in either safetensors or pickle format. [`load_torch_model`] takes a `nn.Module` and a checkpoint path (either a single file or a directory) as input and load the weights into the model.

### load_torch_model

### huggingface_hub.load_torch_model

```python
Load a checkpoint into a model, handling both sharded and non-sharded checkpoints.

Args:
    model (`torch.nn.Module`):
        The model in which to load the checkpoint.
    checkpoint_path (`str` or `os.PathLike`):
        Path to either the checkpoint file or directory containing the checkpoint(s).
    strict (`bool`, *optional*, defaults to `False`):
        Whether to strictly enforce that the keys in the model state dict match the keys in the checkpoint.
    safe (`bool`, *optional*, defaults to `True`):
        If `safe` is True, the safetensors files will be loaded. If `safe` is False, the function
        will first attempt to load safetensors files if they are available, otherwise it will fall back to loading
        pickle files. `filename_pattern` parameter takes precedence over `safe` parameter.
    weights_only (`bool`, *optional*, defaults to `False`):
        If True, only loads the model weights without optimizer states and other metadata.
        Only supported in PyTorch >= 1.13.
    map_location (`str` or `torch.device`, *optional*):
        A `torch.device` object, string or a dict specifying how to remap storage locations. It
        indicates the location where all tensors should be loaded.
    mmap (`bool`, *optional*, defaults to `False`):
        Whether to use memory-mapped file loading. Memory mapping can improve loading performance
        for large models in PyTorch >= 2.1.0 with zipfile-based checkpoints.
    filename_pattern (`str`, *optional*):
        The pattern to look for the index file. Pattern must be a string that
        can be formatted with `filename_pattern.format(suffix=...)` and must contain the keyword `suffix`
        Defaults to `"model{suffix}.safetensors"`.
Returns:
    `NamedTuple`: A named tuple with `missing_keys` and `unexpected_keys` fields.
        - `missing_keys` is a list of str containing the missing keys, i.e. keys that are in the model but not in the checkpoint.
        - `unexpected_keys` is a list of str containing the unexpected keys, i.e. keys that are in the checkpoint but not in the model.

Raises:
    [`FileNotFoundError`](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)
        If the checkpoint file or directory does not exist.
    [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
        If safetensors or torch is not installed when trying to load a .safetensors file or a PyTorch checkpoint respectively.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
       If the checkpoint path is invalid or if the checkpoint format cannot be determined.

Example:
```python
>>> from huggingface_hub import load_torch_model
>>> model = ... # A PyTorch model
>>> load_torch_model(model, "path/to/checkpoint")
```
```


### load_state_dict_from_file

### huggingface_hub.load_state_dict_from_file

```python
Loads a checkpoint file, handling both safetensors and pickle checkpoint formats.

Args:
    checkpoint_file (`str` or `os.PathLike`):
        Path to the checkpoint file to load. Can be either a safetensors or pickle (`.bin`) checkpoint.
    map_location (`str` or `torch.device`, *optional*):
        A `torch.device` object, string or a dict specifying how to remap storage locations. It
        indicates the location where all tensors should be loaded.
    weights_only (`bool`, *optional*, defaults to `False`):
        If True, only loads the model weights without optimizer states and other metadata.
        Only supported for pickle (`.bin`) checkpoints with PyTorch >= 1.13. Has no effect when
        loading safetensors files.
    mmap (`bool`, *optional*, defaults to `False`):
        Whether to use memory-mapped file loading. Memory mapping can improve loading performance
        for large models in PyTorch >= 2.1.0 with zipfile-based checkpoints. Has no effect when
        loading safetensors files, as the `safetensors` library uses memory mapping by default.

Returns:
    `Union[Dict[str, "torch.Tensor"], Any]`: The loaded checkpoint.
        - For safetensors files: always returns a dictionary mapping parameter names to tensors.
        - For pickle files: returns any Python object that was pickled (commonly a state dict, but could be
          an entire model, optimizer state, or any other Python object).

Raises:
    [`FileNotFoundError`](https://docs.python.org/3/library/exceptions.html#FileNotFoundError)
        If the checkpoint file does not exist.
    [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
        If safetensors or torch is not installed when trying to load a .safetensors file or a PyTorch checkpoint respectively.
    [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError)
        If the checkpoint file format is invalid or if git-lfs files are not properly downloaded.
    [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
        If the checkpoint file path is empty or invalid.

Example:
```python
>>> from huggingface_hub import load_state_dict_from_file

# Load a PyTorch checkpoint
>>> state_dict = load_state_dict_from_file("path/to/model.bin", map_location="cpu")
>>> model.load_state_dict(state_dict)

# Load a safetensors checkpoint
>>> state_dict = load_state_dict_from_file("path/to/model.safetensors")
>>> model.load_state_dict(state_dict)
```
```



## Tensors helpers

### get_torch_storage_id

### huggingface_hub.get_torch_storage_id

```python
Return unique identifier to a tensor storage.

Multiple different tensors can share the same underlying storage. This identifier is
guaranteed to be unique and constant for this tensor's storage during its lifetime. Two tensor storages with
non-overlapping lifetimes may have the same id.
In the case of meta tensors, we return None since we can't tell if they share the same storage.

Taken from https://github.com/huggingface/transformers/blob/1ecf5f7c982d761b4daaa96719d162c324187c64/src/transformers/pytorch_utils.py#L278.
```


### get_torch_storage_size

### huggingface_hub.get_torch_storage_size

```python
Taken from https://github.com/huggingface/safetensors/blob/08db34094e9e59e2f9218f2df133b7b4aaff5a99/bindings/python/py_src/safetensors/torch.py#L31C1-L41C59
```
