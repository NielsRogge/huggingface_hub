<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# TensorBoard 로거[[tensorboard-logger]]

TensorBoard는 기계학습 실험을 위한 시각화 도구입니다. 주로 손실 및 정확도와 같은 지표를 추적 및 시각화하고, 모델 그래프와 
히스토그램을 보여주고, 이미지를 표시하는 등 다양한 기능을 제공합니다. 또한 TensorBoard는 Hugging Face Hub와 잘 통합되어 있습니다. 
`tfevents` 같은 TensorBoard 추적을 Hub에 푸시하면 Hub는 이를 자동으로 감지하여 시각화 인스턴스를 시작합니다.
TensorBoard와 Hub의 통합에 대한 자세한 정보는 [가이드](https://huggingface.co/docs/hub/tensorboard)를 확인하세요.

이 통합을 위해, `huggingface_hub`는 로그를 Hub로 푸시하기 위한 사용자 정의 로거를 제공합니다. 
이 로거는 추가적인 코드 없이 [SummaryWriter](https://tensorboardx.readthedocs.io/en/latest/tensorboard.html)의 대체제로 사용될 수 있습니다. 
추적은 계속해서 로컬에 저장되며 백그라운드 작업이 일정한 시간마다 Hub에 푸시하는 형태로 동작합니다.

## HFSummaryWriter[[huggingface_hub.HFSummaryWriter]]

### HFSummaryWriter

```python
Wrapper around the tensorboard's `SummaryWriter` to push training logs to the Hub.

Data is logged locally and then pushed to the Hub asynchronously. Pushing data to the Hub is done in a separate
thread to avoid blocking the training script. In particular, if the upload fails for any reason (e.g. a connection
issue), the main script will not be interrupted. Data is automatically pushed to the Hub every `commit_every`
minutes (default to every 5 minutes).

<Tip warning={true}>

`HFSummaryWriter` is experimental. Its API is subject to change in the future without prior notice.

</Tip>

Args:
    repo_id (`str`):
        The id of the repo to which the logs will be pushed.
    logdir (`str`, *optional*):
        The directory where the logs will be written. If not specified, a local directory will be created by the
        underlying `SummaryWriter` object.
    commit_every (`int` or `float`, *optional*):
        The frequency (in minutes) at which the logs will be pushed to the Hub. Defaults to 5 minutes.
    squash_history (`bool`, *optional*):
        Whether to squash the history of the repo after each commit. Defaults to `False`. Squashing commits is
        useful to avoid degraded performances on the repo when it grows too large.
    repo_type (`str`, *optional*):
        The type of the repo to which the logs will be pushed. Defaults to "model".
    repo_revision (`str`, *optional*):
        The revision of the repo to which the logs will be pushed. Defaults to "main".
    repo_private (`bool`, *optional*):
        Whether to make the repo private. If `None` (default), the repo will be public unless the organization's default is private. This value is ignored if the repo already exists.
    path_in_repo (`str`, *optional*):
        The path to the folder in the repo where the logs will be pushed. Defaults to "tensorboard/".
    repo_allow_patterns (`List[str]` or `str`, *optional*):
        A list of patterns to include in the upload. Defaults to `"*.tfevents.*"`. Check out the
        [upload guide](https://huggingface.co/docs/huggingface_hub/guides/upload#upload-a-folder) for more details.
    repo_ignore_patterns (`List[str]` or `str`, *optional*):
        A list of patterns to exclude in the upload. Check out the
        [upload guide](https://huggingface.co/docs/huggingface_hub/guides/upload#upload-a-folder) for more details.
    token (`str`, *optional*):
        Authentication token. Will default to the stored token. See https://huggingface.co/settings/token for more
        details
    kwargs:
        Additional keyword arguments passed to `SummaryWriter`.

Examples:
```diff
# Taken from https://pytorch.org/docs/stable/tensorboard.html
- from torch.utils.tensorboard import SummaryWriter
+ from huggingface_hub import HFSummaryWriter

import numpy as np

- writer = SummaryWriter()
+ writer = HFSummaryWriter(repo_id="username/my-trained-model")

for n_iter in range(100):
    writer.add_scalar('Loss/train', np.random.random(), n_iter)
    writer.add_scalar('Loss/test', np.random.random(), n_iter)
    writer.add_scalar('Accuracy/train', np.random.random(), n_iter)
    writer.add_scalar('Accuracy/test', np.random.random(), n_iter)
```

```py
>>> from huggingface_hub import HFSummaryWriter

# Logs are automatically pushed every 15 minutes (5 by default) + when exiting the context manager
>>> with HFSummaryWriter(repo_id="test_hf_logger", commit_every=15) as logger:
...     logger.add_scalar("a", 1)
...     logger.add_scalar("b", 2)
```
```

