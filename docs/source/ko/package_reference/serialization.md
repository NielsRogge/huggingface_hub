<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 직렬화[[serialization]]

`huggingface_hub`에는 ML 라이브러리가 모델 가중치를 표준화된 방식으로 직렬화 할 수 있도록 돕는 헬퍼를 포함하고 있습니다. 라이브러리의 이 부분은 아직 개발 중이며 향후 버전에서 개선될 예정입니다. 개선 목표는 Hub에서 가중치의 직렬화 방식을 통일하고, 라이브러리 간 코드 중복을 줄이며, Hub에서의 규약을 촉진하는 것입니다.

## 상태 사전을 샤드로 나누기[[split-state-dict-into-shards]]

현재 이 모듈은 상태 딕셔너리(예: 레이어 이름과 관련 텐서 간의 매핑)를 받아 여러 샤드로 나누고, 이 과정에서 적절한 인덱스를 생성하는 단일 헬퍼를 포함하고 있습니다. 이 헬퍼는 `torch`, `tensorflow`, `numpy` 텐서에 사용 가능하며, 다른 ML 프레임워크로 쉽게 확장될 수 있도록 설계되었습니다.

### split_tf_state_dict_into_shards[[huggingface_hub.split_tf_state_dict_into_shards]]

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


### split_torch_state_dict_into_shards[[huggingface_hub.split_torch_state_dict_into_shards]]

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


### split_state_dict_into_shards_factory[[huggingface_hub.split_state_dict_into_shards_factory]]

이것은 각 프레임워크별 헬퍼가 파생되는 기본 틀입니다. 실제로는 아직 지원되지 않는 프레임워크에 맞게 조정할 필요가 있는 경우가 아니면 이 틀을 직접 사용할 것으로 예상되지 않습니다. 그런 경우가 있다면, `huggingface_hub` 리포지토리에 [새로운 이슈를 개설](https://github.com/huggingface/huggingface_hub/issues/new) 하여 알려주세요.

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


## 도우미

### get_torch_storage_id[[huggingface_hub.get_torch_storage_id]]

### huggingface_hub.get_torch_storage_id

```python
Return unique identifier to a tensor storage.

Multiple different tensors can share the same underlying storage. This identifier is
guaranteed to be unique and constant for this tensor's storage during its lifetime. Two tensor storages with
non-overlapping lifetimes may have the same id.
In the case of meta tensors, we return None since we can't tell if they share the same storage.

Taken from https://github.com/huggingface/transformers/blob/1ecf5f7c982d761b4daaa96719d162c324187c64/src/transformers/pytorch_utils.py#L278.
```
