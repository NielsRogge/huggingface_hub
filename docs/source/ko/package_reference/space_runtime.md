<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Space 런타임 관리[[managing-your-space-runtime]]

Hub의 Space를 관리하는 메소드에 대한 자세한 설명은 [`HfApi`]페이지를 확인하세요.

- Space 복제: [`duplicate_space`]
- 현재 런타임 가져오기: [`get_space_runtime`]
- 보안 관리: [`add_space_secret`] 및 [`delete_space_secret`]
- 하드웨어 관리: [`request_space_hardware`]
- 상태 관리: [`pause_space`], [`restart_space`], [`set_space_sleep_time`]

## 데이터 구조[[data-structures]]

### SpaceRuntime[[huggingface_hub.SpaceRuntime]]

### SpaceRuntime

```python
Contains information about the current runtime of a Space.

Args:
    stage (`str`):
        Current stage of the space. Example: RUNNING.
    hardware (`str` or `None`):
        Current hardware of the space. Example: "cpu-basic". Can be `None` if Space
        is `BUILDING` for the first time.
    requested_hardware (`str` or `None`):
        Requested hardware. Can be different than `hardware` especially if the request
        has just been made. Example: "t4-medium". Can be `None` if no hardware has
        been requested yet.
    sleep_time (`int` or `None`):
        Number of seconds the Space will be kept alive after the last request. By default (if value is `None`), the
        Space will never go to sleep if it's running on an upgraded hardware, while it will go to sleep after 48
        hours on a free 'cpu-basic' hardware. For more details, see https://huggingface.co/docs/hub/spaces-gpus#sleep-time.
    raw (`dict`):
        Raw response from the server. Contains more information about the Space
        runtime like number of replicas, number of cpu, memory size,...
```


### SpaceHardware[[huggingface_hub.SpaceHardware]]

### SpaceHardware

```python
Enumeration of hardwares available to run your Space on the Hub.

Value can be compared to a string:
```py
assert SpaceHardware.CPU_BASIC == "cpu-basic"
```

Taken from https://github.com/huggingface/moon-landing/blob/main/server/repo_types/SpaceInfo.ts#L73 (private url).
```


### SpaceStage[[huggingface_hub.SpaceStage]]

### SpaceStage

```python
Enumeration of possible stage of a Space on the Hub.

Value can be compared to a string:
```py
assert SpaceStage.BUILDING == "BUILDING"
```

Taken from https://github.com/huggingface/moon-landing/blob/main/server/repo_types/SpaceInfo.ts#L61 (private url).
```


### SpaceStorage[[huggingface_hub.SpaceStorage]]

### SpaceStorage

```python
Enumeration of persistent storage available for your Space on the Hub.

Value can be compared to a string:
```py
assert SpaceStorage.SMALL == "small"
```

Taken from https://github.com/huggingface/moon-landing/blob/main/server/repo_types/SpaceHardwareFlavor.ts#L24 (private url).
```


### SpaceVariable[[huggingface_hub.SpaceVariable]]

### SpaceVariable

```python
Contains information about the current variables of a Space.

Args:
    key (`str`):
        Variable key. Example: `"MODEL_REPO_ID"`
    value (`str`):
        Variable value. Example: `"the_model_repo_id"`.
    description (`str` or None):
        Description of the variable. Example: `"Model Repo ID of the implemented model"`.
    updatedAt (`datetime` or None):
        datetime of the last update of the variable (if the variable has been updated at least once).
```
