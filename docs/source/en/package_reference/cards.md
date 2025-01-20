<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Repository Cards

The huggingface_hub library provides a Python interface to create, share, and update Model/Dataset Cards.
Visit the [dedicated documentation page](https://huggingface.co/docs/hub/models-cards) for a deeper view of what
Model Cards on the Hub are, and how they work under the hood. You can also check out our [Model Cards guide](../how-to-model-cards) to
get a feel for how you would use these utilities in your own projects.

## Repo Card

The `RepoCard` object is the parent class of [`ModelCard`], [`DatasetCard`] and `SpaceCard`.

### huggingface_hub.repocard.RepoCard

No docstring found for huggingface_hub.repocard.RepoCard

    - __init__
    - all

## Card Data

The [`CardData`] object is the parent class of [`ModelCardData`] and [`DatasetCardData`].

### huggingface_hub.repocard_data.CardData

```python
Structure containing metadata from a RepoCard.

[`CardData`] is the parent class of [`ModelCardData`] and [`DatasetCardData`].

Metadata can be exported as a dictionary or YAML. Export can be customized to alter the representation of the data
(example: flatten evaluation results). `CardData` behaves as a dictionary (can get, pop, set values) but do not
inherit from `dict` to allow this export step.
```


## Model Cards

### ModelCard

### ModelCard

No docstring found for huggingface_hub.ModelCard


### ModelCardData

### ModelCardData

```python
Model Card Metadata that is used by Hugging Face Hub when included at the top of your README.md

Args:
    base_model (`str` or `List[str]`, *optional*):
        The identifier of the base model from which the model derives. This is applicable for example if your model is a
        fine-tune or adapter of an existing model. The value must be the ID of a model on the Hub (or a list of IDs
        if your model derives from multiple models). Defaults to None.
    datasets (`Union[str, List[str]]`, *optional*):
        Dataset or list of datasets that were used to train this model. Should be a dataset ID
        found on https://hf.co/datasets. Defaults to None.
    eval_results (`Union[List[EvalResult], EvalResult]`, *optional*):
        List of `huggingface_hub.EvalResult` that define evaluation results of the model. If provided,
        `model_name` is used to as a name on PapersWithCode's leaderboards. Defaults to `None`.
    language (`Union[str, List[str]]`, *optional*):
        Language of model's training data or metadata. It must be an ISO 639-1, 639-2 or
        639-3 code (two/three letters), or a special value like "code", "multilingual". Defaults to `None`.
    library_name (`str`, *optional*):
        Name of library used by this model. Example: keras or any library from
        https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/model-libraries.ts.
        Defaults to None.
    license (`str`, *optional*):
        License of this model. Example: apache-2.0 or any license from
        https://huggingface.co/docs/hub/repositories-licenses. Defaults to None.
    license_name (`str`, *optional*):
        Name of the license of this model. Defaults to None. To be used in conjunction with `license_link`.
        Common licenses (Apache-2.0, MIT, CC-BY-SA-4.0) do not need a name. In that case, use `license` instead.
    license_link (`str`, *optional*):
        Link to the license of this model. Defaults to None. To be used in conjunction with `license_name`.
        Common licenses (Apache-2.0, MIT, CC-BY-SA-4.0) do not need a link. In that case, use `license` instead.
    metrics (`List[str]`, *optional*):
        List of metrics used to evaluate this model. Should be a metric name that can be found
        at https://hf.co/metrics. Example: 'accuracy'. Defaults to None.
    model_name (`str`, *optional*):
        A name for this model. It is used along with
        `eval_results` to construct the `model-index` within the card's metadata. The name
        you supply here is what will be used on PapersWithCode's leaderboards. If None is provided
        then the repo name is used as a default. Defaults to None.
    pipeline_tag (`str`, *optional*):
        The pipeline tag associated with the model. Example: "text-classification".
    tags (`List[str]`, *optional*):
        List of tags to add to your model that can be used when filtering on the Hugging
        Face Hub. Defaults to None.
    ignore_metadata_errors (`str`):
        If True, errors while parsing the metadata section will be ignored. Some information might be lost during
        the process. Use it at your own risk.
    kwargs (`dict`, *optional*):
        Additional metadata that will be added to the model card. Defaults to None.

Example:
    ```python
    >>> from huggingface_hub import ModelCardData
    >>> card_data = ModelCardData(
    ...     language="en",
    ...     license="mit",
    ...     library_name="timm",
    ...     tags=['image-classification', 'resnet'],
    ... )
    >>> card_data.to_dict()
    {'language': 'en', 'license': 'mit', 'library_name': 'timm', 'tags': ['image-classification', 'resnet']}

    ```
```


## Dataset Cards

Dataset cards are also known as Data Cards in the ML Community.

### DatasetCard

### DatasetCard

No docstring found for huggingface_hub.DatasetCard


### DatasetCardData

### DatasetCardData

```python
Dataset Card Metadata that is used by Hugging Face Hub when included at the top of your README.md

Args:
    language (`List[str]`, *optional*):
        Language of dataset's data or metadata. It must be an ISO 639-1, 639-2 or
        639-3 code (two/three letters), or a special value like "code", "multilingual".
    license (`Union[str, List[str]]`, *optional*):
        License(s) of this dataset. Example: apache-2.0 or any license from
        https://huggingface.co/docs/hub/repositories-licenses.
    annotations_creators (`Union[str, List[str]]`, *optional*):
        How the annotations for the dataset were created.
        Options are: 'found', 'crowdsourced', 'expert-generated', 'machine-generated', 'no-annotation', 'other'.
    language_creators (`Union[str, List[str]]`, *optional*):
        How the text-based data in the dataset was created.
        Options are: 'found', 'crowdsourced', 'expert-generated', 'machine-generated', 'other'
    multilinguality (`Union[str, List[str]]`, *optional*):
        Whether the dataset is multilingual.
        Options are: 'monolingual', 'multilingual', 'translation', 'other'.
    size_categories (`Union[str, List[str]]`, *optional*):
        The number of examples in the dataset. Options are: 'n<1K', '1K<n<10K', '10K<n<100K',
        '100K<n<1M', '1M<n<10M', '10M<n<100M', '100M<n<1B', '1B<n<10B', '10B<n<100B', '100B<n<1T', 'n>1T', and 'other'.
    source_datasets (`List[str]]`, *optional*):
        Indicates whether the dataset is an original dataset or extended from another existing dataset.
        Options are: 'original' and 'extended'.
    task_categories (`Union[str, List[str]]`, *optional*):
        What categories of task does the dataset support?
    task_ids (`Union[str, List[str]]`, *optional*):
        What specific tasks does the dataset support?
    paperswithcode_id (`str`, *optional*):
        ID of the dataset on PapersWithCode.
    pretty_name (`str`, *optional*):
        A more human-readable name for the dataset. (ex. "Cats vs. Dogs")
    train_eval_index (`Dict`, *optional*):
        A dictionary that describes the necessary spec for doing evaluation on the Hub.
        If not provided, it will be gathered from the 'train-eval-index' key of the kwargs.
    config_names (`Union[str, List[str]]`, *optional*):
        A list of the available dataset configs for the dataset.
```


## Space Cards

### SpaceCard

### SpaceCard

No docstring found for huggingface_hub.SpaceCard


### SpaceCardData

### SpaceCardData

```python
Space Card Metadata that is used by Hugging Face Hub when included at the top of your README.md

To get an exhaustive reference of Spaces configuration, please visit https://huggingface.co/docs/hub/spaces-config-reference#spaces-configuration-reference.

Args:
    title (`str`, *optional*)
        Title of the Space.
    sdk (`str`, *optional*)
        SDK of the Space (one of `gradio`, `streamlit`, `docker`, or `static`).
    sdk_version (`str`, *optional*)
        Version of the used SDK (if Gradio/Streamlit sdk).
    python_version (`str`, *optional*)
        Python version used in the Space (if Gradio/Streamlit sdk).
    app_file (`str`, *optional*)
        Path to your main application file (which contains either gradio or streamlit Python code, or static html code).
        Path is relative to the root of the repository.
    app_port (`str`, *optional*)
        Port on which your application is running. Used only if sdk is `docker`.
    license (`str`, *optional*)
        License of this model. Example: apache-2.0 or any license from
        https://huggingface.co/docs/hub/repositories-licenses.
    duplicated_from (`str`, *optional*)
        ID of the original Space if this is a duplicated Space.
    models (List[`str`], *optional*)
        List of models related to this Space. Should be a dataset ID found on https://hf.co/models.
    datasets (`List[str]`, *optional*)
        List of datasets related to this Space. Should be a dataset ID found on https://hf.co/datasets.
    tags (`List[str]`, *optional*)
        List of tags to add to your Space that can be used when filtering on the Hub.
    ignore_metadata_errors (`str`):
        If True, errors while parsing the metadata section will be ignored. Some information might be lost during
        the process. Use it at your own risk.
    kwargs (`dict`, *optional*):
        Additional metadata that will be added to the space card.

Example:
    ```python
    >>> from huggingface_hub import SpaceCardData
    >>> card_data = SpaceCardData(
    ...     title="Dreambooth Training",
    ...     license="mit",
    ...     sdk="gradio",
    ...     duplicated_from="multimodalart/dreambooth-training"
    ... )
    >>> card_data.to_dict()
    {'title': 'Dreambooth Training', 'sdk': 'gradio', 'license': 'mit', 'duplicated_from': 'multimodalart/dreambooth-training'}
    ```
```


## Utilities

### EvalResult

### EvalResult

```python
Flattened representation of individual evaluation results found in model-index of Model Cards.

For more information on the model-index spec, see https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1.

Args:
    task_type (`str`):
        The task identifier. Example: "image-classification".
    dataset_type (`str`):
        The dataset identifier. Example: "common_voice". Use dataset id from https://hf.co/datasets.
    dataset_name (`str`):
        A pretty name for the dataset. Example: "Common Voice (French)".
    metric_type (`str`):
        The metric identifier. Example: "wer". Use metric id from https://hf.co/metrics.
    metric_value (`Any`):
        The metric value. Example: 0.9 or "20.0 ± 1.2".
    task_name (`str`, *optional*):
        A pretty name for the task. Example: "Speech Recognition".
    dataset_config (`str`, *optional*):
        The name of the dataset configuration used in `load_dataset()`.
        Example: fr in `load_dataset("common_voice", "fr")`. See the `datasets` docs for more info:
        https://hf.co/docs/datasets/package_reference/loading_methods#datasets.load_dataset.name
    dataset_split (`str`, *optional*):
        The split used in `load_dataset()`. Example: "test".
    dataset_revision (`str`, *optional*):
        The revision (AKA Git Sha) of the dataset used in `load_dataset()`.
        Example: 5503434ddd753f426f4b38109466949a1217c2bb
    dataset_args (`Dict[str, Any]`, *optional*):
        The arguments passed during `Metric.compute()`. Example for `bleu`: `{"max_order": 4}`
    metric_name (`str`, *optional*):
        A pretty name for the metric. Example: "Test WER".
    metric_config (`str`, *optional*):
        The name of the metric configuration used in `load_metric()`.
        Example: bleurt-large-512 in `load_metric("bleurt", "bleurt-large-512")`.
        See the `datasets` docs for more info: https://huggingface.co/docs/datasets/v2.1.0/en/loading#load-configurations
    metric_args (`Dict[str, Any]`, *optional*):
        The arguments passed during `Metric.compute()`. Example for `bleu`: max_order: 4
    verified (`bool`, *optional*):
        Indicates whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not. Automatically computed by Hugging Face, do not set.
    verify_token (`str`, *optional*):
        A JSON Web Token that is used to verify whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not.
    source_name (`str`, *optional*):
        The name of the source of the evaluation result. Example: "Open LLM Leaderboard".
    source_url (`str`, *optional*):
        The URL of the source of the evaluation result. Example: "https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard".
```


### model_index_to_eval_results

### huggingface_hub.repocard_data.model_index_to_eval_results

```python
Takes in a model index and returns the model name and a list of `huggingface_hub.EvalResult` objects.

A detailed spec of the model index can be found here:
https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1

Args:
    model_index (`List[Dict[str, Any]]`):
        A model index data structure, likely coming from a README.md file on the
        Hugging Face Hub.

Returns:
    model_name (`str`):
        The name of the model as found in the model index. This is used as the
        identifier for the model on leaderboards like PapersWithCode.
    eval_results (`List[EvalResult]`):
        A list of `huggingface_hub.EvalResult` objects containing the metrics
        reported in the provided model_index.

Example:
    ```python
    >>> from huggingface_hub.repocard_data import model_index_to_eval_results
    >>> # Define a minimal model index
    >>> model_index = [
    ...     {
    ...         "name": "my-cool-model",
    ...         "results": [
    ...             {
    ...                 "task": {
    ...                     "type": "image-classification"
    ...                 },
    ...                 "dataset": {
    ...                     "type": "beans",
    ...                     "name": "Beans"
    ...                 },
    ...                 "metrics": [
    ...                     {
    ...                         "type": "accuracy",
    ...                         "value": 0.9
    ...                     }
    ...                 ]
    ...             }
    ...         ]
    ...     }
    ... ]
    >>> model_name, eval_results = model_index_to_eval_results(model_index)
    >>> model_name
    'my-cool-model'
    >>> eval_results[0].task_type
    'image-classification'
    >>> eval_results[0].metric_type
    'accuracy'

    ```
```


### eval_results_to_model_index

### huggingface_hub.repocard_data.eval_results_to_model_index

```python
Takes in given model name and list of `huggingface_hub.EvalResult` and returns a
valid model-index that will be compatible with the format expected by the
Hugging Face Hub.

Args:
    model_name (`str`):
        Name of the model (ex. "my-cool-model"). This is used as the identifier
        for the model on leaderboards like PapersWithCode.
    eval_results (`List[EvalResult]`):
        List of `huggingface_hub.EvalResult` objects containing the metrics to be
        reported in the model-index.

Returns:
    model_index (`List[Dict[str, Any]]`): The eval_results converted to a model-index.

Example:
    ```python
    >>> from huggingface_hub.repocard_data import eval_results_to_model_index, EvalResult
    >>> # Define minimal eval_results
    >>> eval_results = [
    ...     EvalResult(
    ...         task_type="image-classification",  # Required
    ...         dataset_type="beans",  # Required
    ...         dataset_name="Beans",  # Required
    ...         metric_type="accuracy",  # Required
    ...         metric_value=0.9,  # Required
    ...     )
    ... ]
    >>> eval_results_to_model_index("my-cool-model", eval_results)
    [{'name': 'my-cool-model', 'results': [{'task': {'type': 'image-classification'}, 'dataset': {'name': 'Beans', 'type': 'beans'}, 'metrics': [{'type': 'accuracy', 'value': 0.9}]}]}]

    ```
```


### metadata_eval_result

### huggingface_hub.repocard.metadata_eval_result

```python
Creates a metadata dict with the result from a model evaluated on a dataset.

Args:
    model_pretty_name (`str`):
        The name of the model in natural language.
    task_pretty_name (`str`):
        The name of a task in natural language.
    task_id (`str`):
        Example: automatic-speech-recognition. A task id.
    metrics_pretty_name (`str`):
        A name for the metric in natural language. Example: Test WER.
    metrics_id (`str`):
        Example: wer. A metric id from https://hf.co/metrics.
    metrics_value (`Any`):
        The value from the metric. Example: 20.0 or "20.0 ± 1.2".
    dataset_pretty_name (`str`):
        The name of the dataset in natural language.
    dataset_id (`str`):
        Example: common_voice. A dataset id from https://hf.co/datasets.
    metrics_config (`str`, *optional*):
        The name of the metric configuration used in `load_metric()`.
        Example: bleurt-large-512 in `load_metric("bleurt", "bleurt-large-512")`.
    metrics_verified (`bool`, *optional*, defaults to `False`):
        Indicates whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not. Automatically computed by Hugging Face, do not set.
    dataset_config (`str`, *optional*):
        Example: fr. The name of the dataset configuration used in `load_dataset()`.
    dataset_split (`str`, *optional*):
        Example: test. The name of the dataset split used in `load_dataset()`.
    dataset_revision (`str`, *optional*):
        Example: 5503434ddd753f426f4b38109466949a1217c2bb. The name of the dataset dataset revision
        used in `load_dataset()`.
    metrics_verification_token (`bool`, *optional*):
        A JSON Web Token that is used to verify whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not.

Returns:
    `dict`: a metadata dict with the result from a model evaluated on a dataset.

Example:
    ```python
    >>> from huggingface_hub import metadata_eval_result
    >>> results = metadata_eval_result(
    ...         model_pretty_name="RoBERTa fine-tuned on ReactionGIF",
    ...         task_pretty_name="Text Classification",
    ...         task_id="text-classification",
    ...         metrics_pretty_name="Accuracy",
    ...         metrics_id="accuracy",
    ...         metrics_value=0.2662102282047272,
    ...         dataset_pretty_name="ReactionJPEG",
    ...         dataset_id="julien-c/reactionjpeg",
    ...         dataset_config="default",
    ...         dataset_split="test",
    ... )
    >>> results == {
    ...     'model-index': [
    ...         {
    ...             'name': 'RoBERTa fine-tuned on ReactionGIF',
    ...             'results': [
    ...                 {
    ...                     'task': {
    ...                         'type': 'text-classification',
    ...                         'name': 'Text Classification'
    ...                     },
    ...                     'dataset': {
    ...                         'name': 'ReactionJPEG',
    ...                         'type': 'julien-c/reactionjpeg',
    ...                         'config': 'default',
    ...                         'split': 'test'
    ...                     },
    ...                     'metrics': [
    ...                         {
    ...                             'type': 'accuracy',
    ...                             'value': 0.2662102282047272,
    ...                             'name': 'Accuracy',
    ...                             'verified': False
    ...                         }
    ...                     ]
    ...                 }
    ...             ]
    ...         }
    ...     ]
    ... }
    True

    ```
```


### metadata_update

### huggingface_hub.repocard.metadata_update

```python
Updates the metadata in the README.md of a repository on the Hugging Face Hub.
If the README.md file doesn't exist yet, a new one is created with metadata and an
the default ModelCard or DatasetCard template. For `space` repo, an error is thrown
as a Space cannot exist without a `README.md` file.

Args:
    repo_id (`str`):
        The name of the repository.
    metadata (`dict`):
        A dictionary containing the metadata to be updated.
    repo_type (`str`, *optional*):
        Set to `"dataset"` or `"space"` if updating to a dataset or space,
        `None` or `"model"` if updating to a model. Default is `None`.
    overwrite (`bool`, *optional*, defaults to `False`):
        If set to `True` an existing field can be overwritten, otherwise
        attempting to overwrite an existing field will cause an error.
    token (`str`, *optional*):
        The Hugging Face authentication token.
    commit_message (`str`, *optional*):
        The summary / title / first line of the generated commit. Defaults to
        `f"Update metadata with huggingface_hub"`
    commit_description (`str` *optional*)
        The description of the generated commit
    revision (`str`, *optional*):
        The git revision to commit from. Defaults to the head of the
        `"main"` branch.
    create_pr (`boolean`, *optional*):
        Whether or not to create a Pull Request from `revision` with that commit.
        Defaults to `False`.
    parent_commit (`str`, *optional*):
        The OID / SHA of the parent commit, as a hexadecimal string. Shorthands (7 first characters) are also supported.
        If specified and `create_pr` is `False`, the commit will fail if `revision` does not point to `parent_commit`.
        If specified and `create_pr` is `True`, the pull request will be created from `parent_commit`.
        Specifying `parent_commit` ensures the repo has not changed before committing the changes, and can be
        especially useful if the repo is updated / committed to concurrently.
Returns:
    `str`: URL of the commit which updated the card metadata.

Example:
    ```python
    >>> from huggingface_hub import metadata_update
    >>> metadata = {'model-index': [{'name': 'RoBERTa fine-tuned on ReactionGIF',
    ...             'results': [{'dataset': {'name': 'ReactionGIF',
    ...                                      'type': 'julien-c/reactiongif'},
    ...                           'metrics': [{'name': 'Recall',
    ...                                        'type': 'recall',
    ...                                        'value': 0.7762102282047272}],
    ...                          'task': {'name': 'Text Classification',
    ...                                   'type': 'text-classification'}}]}]}
    >>> url = metadata_update("hf-internal-testing/reactiongif-roberta-card", metadata)

    ```
```

