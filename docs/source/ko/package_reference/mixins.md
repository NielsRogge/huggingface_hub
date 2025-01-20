<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 믹스인 & 직렬화 메소드[[mixins--serialization-methods]]

## 믹스인[[mixins]]

`huggingface_hub` 라이브러리는 객체에 함수들의 업로드 및 다운로드 기능을 손쉽게 제공하기 위해서, 부모 클래스로 사용될 수 있는 다양한 믹스인을 제공합니다.
ML 프레임워크를 Hub와 통합하는 방법은 [통합 가이드](../guides/integrations)를 통해 배울 수 있습니다.

### 제네릭[[huggingface_hub.ModelHubMixin]]

### ModelHubMixin

```python
A generic mixin to integrate ANY machine learning framework with the Hub.

To integrate your framework, your model class must inherit from this class. Custom logic for saving/loading models
have to be overwritten in  [`_from_pretrained`] and [`_save_pretrained`]. [`PyTorchModelHubMixin`] is a good example
of mixin integration with the Hub. Check out our [integration guide](../guides/integrations) for more instructions.

When inheriting from [`ModelHubMixin`], you can define class-level attributes. These attributes are not passed to
`__init__` but to the class definition itself. This is useful to define metadata about the library integrating
[`ModelHubMixin`].

For more details on how to integrate the mixin with your library, checkout the [integration guide](../guides/integrations).

Args:
    repo_url (`str`, *optional*):
        URL of the library repository. Used to generate model card.
    docs_url (`str`, *optional*):
        URL of the library documentation. Used to generate model card.
    model_card_template (`str`, *optional*):
        Template of the model card. Used to generate model card. Defaults to a generic template.
    language (`str` or `List[str]`, *optional*):
        Language supported by the library. Used to generate model card.
    library_name (`str`, *optional*):
        Name of the library integrating ModelHubMixin. Used to generate model card.
    license (`str`, *optional*):
        License of the library integrating ModelHubMixin. Used to generate model card.
        E.g: "apache-2.0"
    license_name (`str`, *optional*):
        Name of the library integrating ModelHubMixin. Used to generate model card.
        Only used if `license` is set to `other`.
        E.g: "coqui-public-model-license".
    license_link (`str`, *optional*):
        URL to the license of the library integrating ModelHubMixin. Used to generate model card.
        Only used if `license` is set to `other` and `license_name` is set.
        E.g: "https://coqui.ai/cpml".
    pipeline_tag (`str`, *optional*):
        Tag of the pipeline. Used to generate model card. E.g. "text-classification".
    tags (`List[str]`, *optional*):
        Tags to be added to the model card. Used to generate model card. E.g. ["x-custom-tag", "arxiv:2304.12244"]
    coders (`Dict[Type, Tuple[Callable, Callable]]`, *optional*):
        Dictionary of custom types and their encoders/decoders. Used to encode/decode arguments that are not
        jsonable by default. E.g dataclasses, argparse.Namespace, OmegaConf, etc.

Example:

```python
>>> from huggingface_hub import ModelHubMixin

# Inherit from ModelHubMixin
>>> class MyCustomModel(
...         ModelHubMixin,
...         library_name="my-library",
...         tags=["x-custom-tag", "arxiv:2304.12244"],
...         repo_url="https://github.com/huggingface/my-cool-library",
...         docs_url="https://huggingface.co/docs/my-cool-library",
...         # ^ optional metadata to generate model card
...     ):
...     def __init__(self, size: int = 512, device: str = "cpu"):
...         # define how to initialize your model
...         super().__init__()
...         ...
...
...     def _save_pretrained(self, save_directory: Path) -> None:
...         # define how to serialize your model
...         ...
...
...     @classmethod
...     def from_pretrained(
...         cls: Type[T],
...         pretrained_model_name_or_path: Union[str, Path],
...         *,
...         force_download: bool = False,
...         resume_download: Optional[bool] = None,
...         proxies: Optional[Dict] = None,
...         token: Optional[Union[str, bool]] = None,
...         cache_dir: Optional[Union[str, Path]] = None,
...         local_files_only: bool = False,
...         revision: Optional[str] = None,
...         **model_kwargs,
...     ) -> T:
...         # define how to deserialize your model
...         ...

>>> model = MyCustomModel(size=256, device="gpu")

# Save model weights to local directory
>>> model.save_pretrained("my-awesome-model")

# Push model weights to the Hub
>>> model.push_to_hub("my-awesome-model")

# Download and initialize weights from the Hub
>>> reloaded_model = MyCustomModel.from_pretrained("username/my-awesome-model")
>>> reloaded_model.size
256

# Model card has been correctly populated
>>> from huggingface_hub import ModelCard
>>> card = ModelCard.load("username/my-awesome-model")
>>> card.data.tags
["x-custom-tag", "pytorch_model_hub_mixin", "model_hub_mixin"]
>>> card.data.library_name
"my-library"
```
```

    - all
    - _save_pretrained
    - _from_pretrained

### PyTorch[[huggingface_hub.PyTorchModelHubMixin]]

### PyTorchModelHubMixin

```python
Implementation of [`ModelHubMixin`] to provide model Hub upload/download capabilities to PyTorch models. The model
is set in evaluation mode by default using `model.eval()` (dropout modules are deactivated). To train the model,
you should first set it back in training mode with `model.train()`.

See [`ModelHubMixin`] for more details on how to use the mixin.

Example:

```python
>>> import torch
>>> import torch.nn as nn
>>> from huggingface_hub import PyTorchModelHubMixin

>>> class MyModel(
...         nn.Module,
...         PyTorchModelHubMixin,
...         library_name="keras-nlp",
...         repo_url="https://github.com/keras-team/keras-nlp",
...         docs_url="https://keras.io/keras_nlp/",
...         # ^ optional metadata to generate model card
...     ):
...     def __init__(self, hidden_size: int = 512, vocab_size: int = 30000, output_size: int = 4):
...         super().__init__()
...         self.param = nn.Parameter(torch.rand(hidden_size, vocab_size))
...         self.linear = nn.Linear(output_size, vocab_size)

...     def forward(self, x):
...         return self.linear(x + self.param)
>>> model = MyModel(hidden_size=256)

# Save model weights to local directory
>>> model.save_pretrained("my-awesome-model")

# Push model weights to the Hub
>>> model.push_to_hub("my-awesome-model")

# Download and initialize weights from the Hub
>>> model = MyModel.from_pretrained("username/my-awesome-model")
>>> model.hidden_size
256
```
```


### Keras[[huggingface_hub.KerasModelHubMixin]]

### KerasModelHubMixin

```python
Implementation of [`ModelHubMixin`] to provide model Hub upload/download
capabilities to Keras models.


```python
>>> import tensorflow as tf
>>> from huggingface_hub import KerasModelHubMixin


>>> class MyModel(tf.keras.Model, KerasModelHubMixin):
...     def __init__(self, **kwargs):
...         super().__init__()
...         self.config = kwargs.pop("config", None)
...         self.dummy_inputs = ...
...         self.layer = ...

...     def call(self, *args):
...         return ...


>>> # Initialize and compile the model as you normally would
>>> model = MyModel()
>>> model.compile(...)
>>> # Build the graph by training it or passing dummy inputs
>>> _ = model(model.dummy_inputs)
>>> # Save model weights to local directory
>>> model.save_pretrained("my-awesome-model")
>>> # Push model weights to the Hub
>>> model.push_to_hub("my-awesome-model")
>>> # Download and initialize weights from the Hub
>>> model = MyModel.from_pretrained("username/super-cool-model")
```
```


### from_pretrained_keras

```python
Instantiate a pretrained Keras model from a pre-trained model from the Hub.
The model is expected to be in `SavedModel` format.

Args:
    pretrained_model_name_or_path (`str` or `os.PathLike`):
        Can be either:
            - A string, the `model id` of a pretrained model hosted inside a
              model repo on huggingface.co. Valid model ids can be located
              at the root-level, like `bert-base-uncased`, or namespaced
              under a user or organization name, like
              `dbmdz/bert-base-german-cased`.
            - You can add `revision` by appending `@` at the end of model_id
              simply like this: `dbmdz/bert-base-german-cased@main` Revision
              is the specific model version to use. It can be a branch name,
              a tag name, or a commit id, since we use a git-based system
              for storing models and other artifacts on huggingface.co, so
              `revision` can be any identifier allowed by git.
            - A path to a `directory` containing model weights saved using
              [`~transformers.PreTrainedModel.save_pretrained`], e.g.,
              `./my_model_directory/`.
            - `None` if you are both providing the configuration and state
              dictionary (resp. with keyword arguments `config` and
              `state_dict`).
    force_download (`bool`, *optional*, defaults to `False`):
        Whether to force the (re-)download of the model weights and
        configuration files, overriding the cached versions if they exist.
    proxies (`Dict[str, str]`, *optional*):
        A dictionary of proxy servers to use by protocol or endpoint, e.g.,
        `{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}`. The
        proxies are used on each request.
    token (`str` or `bool`, *optional*):
        The token to use as HTTP bearer authorization for remote files. If
        `True`, will use the token generated when running `transformers-cli
        login` (stored in `~/.huggingface`).
    cache_dir (`Union[str, os.PathLike]`, *optional*):
        Path to a directory in which a downloaded pretrained model
        configuration should be cached if the standard cache should not be
        used.
    local_files_only(`bool`, *optional*, defaults to `False`):
        Whether to only look at local files (i.e., do not try to download
        the model).
    model_kwargs (`Dict`, *optional*):
        model_kwargs will be passed to the model during initialization

<Tip>

Passing `token=True` is required when you want to use a private
model.

</Tip>
```


### push_to_hub_keras

```python
Upload model checkpoint to the Hub.

Use `allow_patterns` and `ignore_patterns` to precisely filter which files should be pushed to the hub. Use
`delete_patterns` to delete existing remote files in the same commit. See [`upload_folder`] reference for more
details.

Args:
    model (`Keras.Model`):
        The [Keras model](`https://www.tensorflow.org/api_docs/python/tf/keras/Model`) you'd like to push to the
        Hub. The model must be compiled and built.
    repo_id (`str`):
            ID of the repository to push to (example: `"username/my-model"`).
    commit_message (`str`, *optional*, defaults to "Add Keras model"):
        Message to commit while pushing.
    private (`bool`, *optional*):
        Whether the repository created should be private.
        If `None` (default), the repo will be public unless the organization's default is private.
    api_endpoint (`str`, *optional*):
        The API endpoint to use when pushing the model to the hub.
    token (`str`, *optional*):
        The token to use as HTTP bearer authorization for remote files. If
        not set, will use the token set when logging in with
        `huggingface-cli login` (stored in `~/.huggingface`).
    branch (`str`, *optional*):
        The git branch on which to push the model. This defaults to
        the default branch as specified in your repository, which
        defaults to `"main"`.
    create_pr (`boolean`, *optional*):
        Whether or not to create a Pull Request from `branch` with that commit.
        Defaults to `False`.
    config (`dict`, *optional*):
        Configuration object to be saved alongside the model weights.
    allow_patterns (`List[str]` or `str`, *optional*):
        If provided, only files matching at least one pattern are pushed.
    ignore_patterns (`List[str]` or `str`, *optional*):
        If provided, files matching any of the patterns are not pushed.
    delete_patterns (`List[str]` or `str`, *optional*):
        If provided, remote files matching any of the patterns will be deleted from the repo.
    log_dir (`str`, *optional*):
        TensorBoard logging directory to be pushed. The Hub automatically
        hosts and displays a TensorBoard instance if log files are included
        in the repository.
    include_optimizer (`bool`, *optional*, defaults to `False`):
        Whether or not to include optimizer during serialization.
    tags (Union[`list`, `str`], *optional*):
        List of tags that are related to model or string of a single tag. See example tags
        [here](https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1).
    plot_model (`bool`, *optional*, defaults to `True`):
        Setting this to `True` will plot the model and put it in the model
        card. Requires graphviz and pydot to be installed.
    model_save_kwargs(`dict`, *optional*):
        model_save_kwargs will be passed to
        [`tf.keras.models.save_model()`](https://www.tensorflow.org/api_docs/python/tf/keras/models/save_model).

Returns:
    The url of the commit of your model in the given repository.
```


### save_pretrained_keras

```python
Saves a Keras model to save_directory in SavedModel format. Use this if
you're using the Functional or Sequential APIs.

Args:
    model (`Keras.Model`):
        The [Keras
        model](https://www.tensorflow.org/api_docs/python/tf/keras/Model)
        you'd like to save. The model must be compiled and built.
    save_directory (`str` or `Path`):
        Specify directory in which you want to save the Keras model.
    config (`dict`, *optional*):
        Configuration object to be saved alongside the model weights.
    include_optimizer(`bool`, *optional*, defaults to `False`):
        Whether or not to include optimizer in serialization.
    plot_model (`bool`, *optional*, defaults to `True`):
        Setting this to `True` will plot the model and put it in the model
        card. Requires graphviz and pydot to be installed.
    tags (Union[`str`,`list`], *optional*):
        List of tags that are related to model or string of a single tag. See example tags
        [here](https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1).
    model_save_kwargs(`dict`, *optional*):
        model_save_kwargs will be passed to
        [`tf.keras.models.save_model()`](https://www.tensorflow.org/api_docs/python/tf/keras/models/save_model).
```


### Fastai[[huggingface_hub.from_pretrained_fastai]]

### from_pretrained_fastai

```python
Load pretrained fastai model from the Hub or from a local directory.

Args:
    repo_id (`str`):
        The location where the pickled fastai.Learner is. It can be either of the two:
            - Hosted on the Hugging Face Hub. E.g.: 'espejelomar/fatai-pet-breeds-classification' or 'distilgpt2'.
              You can add a `revision` by appending `@` at the end of `repo_id`. E.g.: `dbmdz/bert-base-german-cased@main`.
              Revision is the specific model version to use. Since we use a git-based system for storing models and other
              artifacts on the Hugging Face Hub, it can be a branch name, a tag name, or a commit id.
            - Hosted locally. `repo_id` would be a directory containing the pickle and a pyproject.toml
              indicating the fastai and fastcore versions used to build the `fastai.Learner`. E.g.: `./my_model_directory/`.
    revision (`str`, *optional*):
        Revision at which the repo's files are downloaded. See documentation of `snapshot_download`.

Returns:
    The `fastai.Learner` model in the `repo_id` repo.
```


### push_to_hub_fastai

```python
Upload learner checkpoint files to the Hub.

Use `allow_patterns` and `ignore_patterns` to precisely filter which files should be pushed to the hub. Use
`delete_patterns` to delete existing remote files in the same commit. See [`upload_folder`] reference for more
details.

Args:
    learner (`Learner`):
        The `fastai.Learner' you'd like to push to the Hub.
    repo_id (`str`):
        The repository id for your model in Hub in the format of "namespace/repo_name". The namespace can be your individual account or an organization to which you have write access (for example, 'stanfordnlp/stanza-de').
    commit_message (`str`, *optional*):
        Message to commit while pushing. Will default to :obj:`"add model"`.
    private (`bool`, *optional*):
        Whether or not the repository created should be private.
        If `None` (default), will default to been public except if the organization's default is private.
    token (`str`, *optional*):
        The Hugging Face account token to use as HTTP bearer authorization for remote files. If :obj:`None`, the token will be asked by a prompt.
    config (`dict`, *optional*):
        Configuration object to be saved alongside the model weights.
    branch (`str`, *optional*):
        The git branch on which to push the model. This defaults to
        the default branch as specified in your repository, which
        defaults to `"main"`.
    create_pr (`boolean`, *optional*):
        Whether or not to create a Pull Request from `branch` with that commit.
        Defaults to `False`.
    api_endpoint (`str`, *optional*):
        The API endpoint to use when pushing the model to the hub.
    allow_patterns (`List[str]` or `str`, *optional*):
        If provided, only files matching at least one pattern are pushed.
    ignore_patterns (`List[str]` or `str`, *optional*):
        If provided, files matching any of the patterns are not pushed.
    delete_patterns (`List[str]` or `str`, *optional*):
        If provided, remote files matching any of the patterns will be deleted from the repo.

Returns:
    The url of the commit of your model in the given repository.

<Tip>

Raises the following error:

    - [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
      if the user is not log on to the Hugging Face Hub.

</Tip>
```

