<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Inference

Inference is the process of using a trained model to make predictions on new data. As this process can be compute-intensive,
running on a dedicated server can be an interesting option. The `huggingface_hub` library provides an easy way to call a
service that runs inference for hosted models. There are several services you can connect to:
- [Inference API](https://huggingface.co/docs/api-inference/index): a service that allows you to run accelerated inference
on Hugging Face's infrastructure for free. This service is a fast way to get started, test different models, and
prototype AI products.
- [Inference Endpoints](https://huggingface.co/inference-endpoints): a product to easily deploy models to production.
Inference is run by Hugging Face in a dedicated, fully managed infrastructure on a cloud provider of your choice.

These services can be called with the [`InferenceClient`] object. Please refer to [this guide](../guides/inference)
for more information on how to use it.

## Inference Client

### InferenceClient

```python
Initialize a new Inference Client.

[`InferenceClient`] aims to provide a unified experience to perform inference. The client can be used
seamlessly with either the (free) Inference API or self-hosted Inference Endpoints.

Args:
    model (`str`, `optional`):
        The model to run inference with. Can be a model id hosted on the Hugging Face Hub, e.g. `meta-llama/Meta-Llama-3-8B-Instruct`
        or a URL to a deployed Inference Endpoint. Defaults to None, in which case a recommended model is
        automatically selected for the task.
        Note: for better compatibility with OpenAI's client, `model` has been aliased as `base_url`. Those 2
        arguments are mutually exclusive. If using `base_url` for chat completion, the `/chat/completions` suffix
        path will be appended to the base URL (see the [TGI Messages API](https://huggingface.co/docs/text-generation-inference/en/messages_api)
        documentation for details). When passing a URL as `model`, the client will not append any suffix path to it.
    token (`str` or `bool`, *optional*):
        Hugging Face token. Will default to the locally saved token if not provided.
        Pass `token=False` if you don't want to send your token to the server.
        Note: for better compatibility with OpenAI's client, `token` has been aliased as `api_key`. Those 2
        arguments are mutually exclusive and have the exact same behavior.
    timeout (`float`, `optional`):
        The maximum number of seconds to wait for a response from the server. Loading a new model in Inference
        API can take up to several minutes. Defaults to None, meaning it will loop until the server is available.
    headers (`Dict[str, str]`, `optional`):
        Additional headers to send to the server. By default only the authorization and user-agent headers are sent.
        Values in this dictionary will override the default values.
    cookies (`Dict[str, str]`, `optional`):
        Additional cookies to send to the server.
    proxies (`Any`, `optional`):
        Proxies to use for the request.
    base_url (`str`, `optional`):
        Base URL to run inference. This is a duplicated argument from `model` to make [`InferenceClient`]
        follow the same pattern as `openai.OpenAI` client. Cannot be used if `model` is set. Defaults to None.
    api_key (`str`, `optional`):
        Token to use for authentication. This is a duplicated argument from `token` to make [`InferenceClient`]
        follow the same pattern as `openai.OpenAI` client. Cannot be used if `token` is set. Defaults to None.
```


## Async Inference Client

An async version of the client is also provided, based on `asyncio` and `aiohttp`.
To use it, you can either install `aiohttp` directly or use the `[inference]` extra:

```sh
pip install --upgrade huggingface_hub[inference]
# or
# pip install aiohttp
```

### AsyncInferenceClient

```python
Initialize a new Inference Client.

[`InferenceClient`] aims to provide a unified experience to perform inference. The client can be used
seamlessly with either the (free) Inference API or self-hosted Inference Endpoints.

Args:
    model (`str`, `optional`):
        The model to run inference with. Can be a model id hosted on the Hugging Face Hub, e.g. `meta-llama/Meta-Llama-3-8B-Instruct`
        or a URL to a deployed Inference Endpoint. Defaults to None, in which case a recommended model is
        automatically selected for the task.
        Note: for better compatibility with OpenAI's client, `model` has been aliased as `base_url`. Those 2
        arguments are mutually exclusive. If using `base_url` for chat completion, the `/chat/completions` suffix
        path will be appended to the base URL (see the [TGI Messages API](https://huggingface.co/docs/text-generation-inference/en/messages_api)
        documentation for details). When passing a URL as `model`, the client will not append any suffix path to it.
    token (`str` or `bool`, *optional*):
        Hugging Face token. Will default to the locally saved token if not provided.
        Pass `token=False` if you don't want to send your token to the server.
        Note: for better compatibility with OpenAI's client, `token` has been aliased as `api_key`. Those 2
        arguments are mutually exclusive and have the exact same behavior.
    timeout (`float`, `optional`):
        The maximum number of seconds to wait for a response from the server. Loading a new model in Inference
        API can take up to several minutes. Defaults to None, meaning it will loop until the server is available.
    headers (`Dict[str, str]`, `optional`):
        Additional headers to send to the server. By default only the authorization and user-agent headers are sent.
        Values in this dictionary will override the default values.
    cookies (`Dict[str, str]`, `optional`):
        Additional cookies to send to the server.
    trust_env ('bool', 'optional'):
        Trust environment settings for proxy configuration if the parameter is `True` (`False` by default).
    proxies (`Any`, `optional`):
        Proxies to use for the request.
    base_url (`str`, `optional`):
        Base URL to run inference. This is a duplicated argument from `model` to make [`InferenceClient`]
        follow the same pattern as `openai.OpenAI` client. Cannot be used if `model` is set. Defaults to None.
    api_key (`str`, `optional`):
        Token to use for authentication. This is a duplicated argument from `token` to make [`InferenceClient`]
        follow the same pattern as `openai.OpenAI` client. Cannot be used if `token` is set. Defaults to None.
```


## InferenceTimeoutError

### InferenceTimeoutError

```python
Error raised when a model is unavailable or the request times out.
```


### ModelStatus

### huggingface_hub.inference._common.ModelStatus

```python
This Dataclass represents the model status in the Hugging Face Inference API.

Args:
    loaded (`bool`):
        If the model is currently loaded into Hugging Face's InferenceAPI. Models
        are loaded on-demand, leading to the user's first request taking longer.
        If a model is loaded, you can be assured that it is in a healthy state.
    state (`str`):
        The current state of the model. This can be 'Loaded', 'Loadable', 'TooBig'.
        If a model's state is 'Loadable', it's not too big and has a supported
        backend. Loadable models are automatically loaded when the user first
        requests inference on the endpoint. This means it is transparent for the
        user to load a model, except that the first call takes longer to complete.
    compute_type (`Dict`):
        Information about the compute resource the model is using or will use, such as 'gpu' type and number of
        replicas.
    framework (`str`):
        The name of the framework that the model was built with, such as 'transformers'
        or 'text-generation-inference'.
```


## InferenceAPI

[`InferenceAPI`] is the legacy way to call the Inference API. The interface is more simplistic and requires knowing
the input parameters and output format for each task. It also lacks the ability to connect to other services like
Inference Endpoints or AWS SageMaker. [`InferenceAPI`] will soon be deprecated so we recommend using [`InferenceClient`]
whenever possible. Check out [this guide](../guides/inference#legacy-inferenceapi-client) to learn how to switch from
[`InferenceAPI`] to [`InferenceClient`] in your scripts.

### InferenceApi

```python
Client to configure requests and make calls to the HuggingFace Inference API.

Example:

```python
>>> from huggingface_hub.inference_api import InferenceApi

>>> # Mask-fill example
>>> inference = InferenceApi("bert-base-uncased")
>>> inference(inputs="The goal of life is [MASK].")
[{'sequence': 'the goal of life is life.', 'score': 0.10933292657136917, 'token': 2166, 'token_str': 'life'}]

>>> # Question Answering example
>>> inference = InferenceApi("deepset/roberta-base-squad2")
>>> inputs = {
...     "question": "What's my name?",
...     "context": "My name is Clara and I live in Berkeley.",
... }
>>> inference(inputs)
{'score': 0.9326569437980652, 'start': 11, 'end': 16, 'answer': 'Clara'}

>>> # Zero-shot example
>>> inference = InferenceApi("typeform/distilbert-base-uncased-mnli")
>>> inputs = "Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!"
>>> params = {"candidate_labels": ["refund", "legal", "faq"]}
>>> inference(inputs, params)
{'sequence': 'Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!', 'labels': ['refund', 'faq', 'legal'], 'scores': [0.9378499388694763, 0.04914155602455139, 0.013008488342165947]}

>>> # Overriding configured task
>>> inference = InferenceApi("bert-base-uncased", task="feature-extraction")

>>> # Text-to-image
>>> inference = InferenceApi("stabilityai/stable-diffusion-2-1")
>>> inference("cat")
<PIL.PngImagePlugin.PngImageFile image (...)>

>>> # Return as raw response to parse the output yourself
>>> inference = InferenceApi("mio/amadeus")
>>> response = inference("hello world", raw_response=True)
>>> response.headers
{"Content-Type": "audio/flac", ...}
>>> response.content # raw bytes from server
b'(...)'
```
```

    - __init__
    - __call__
    - all
