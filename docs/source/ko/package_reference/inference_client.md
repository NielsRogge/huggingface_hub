<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 추론[[inference]]

추론은 학습된 모델을 사용하여 새로운 데이터를 예측하는 과정입니다. 이 과정은 계산량이 많을 수 있기 때문에, 전용 서버에서 실행하는 것이 흥미로운 옵션이 될 수 있습니다. `huggingface_hub` 라이브러리는 호스팅된 모델에 대한 추론을 실행하는 간단한 방법을 제공합니다. 연결할 수 있는 서비스는 여러가지가 있습니다:

- [추론 API](https://huggingface.co/docs/api-inference/index): Hugging Face의 인프라에서 가속화된 추론을 무료로 실행할 수 있는 서비스입니다. 이 서비스는 시작하기 위한 빠른 방법이며, 다양한 모델을 테스트하고 AI 제품을 프로토타입화하는 데에도 유용합니다.
- [추론 엔드포인트](https://huggingface.co/inference-endpoints): 모델을 쉽게 운영 환경으로 배포할 수 있는 제품입니다. 추론은 여러분이 선택한 클라우드 제공업체의 전용 및 완전히 관리되는 인프라에서 Hugging Face에 의해 실행됩니다.

이러한 서비스는 [`InferenceClient`] 객체를 사용하여 호출할 수 있습니다. 자세한 사용 방법에 대해서는 [이 가이드](../guides/inference)를 참조해주세요.

## 추론 클라이언트[[huggingface_hub.InferenceClient]]

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


## 비동기 추론 클라이언트[[huggingface_hub.AsyncInferenceClient]]

비동기 버전의 클라이언트도 제공되며, 이는 `asyncio`와 `aiohttp`를 기반으로 작동합니다. 
이를 사용하려면 `aiohttp`를 직접 설치하거나 `[inference]` 추가 기능을 사용할 수 있습니다:

```sh
pip install --upgrade huggingface_hub[inference]
# 또는
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


## 추론 시간 초과 오류[[huggingface_hub.InferenceTimeoutError]]

### InferenceTimeoutError

```python
Error raised when a model is unavailable or the request times out.
```


## 반환 유형[[return-types]]

대부분의 작업에 대해, 반환 값은 내장된 유형(string, list, image...)을 갖습니다. 보다 복잡한 유형을 위한 목록은 다음과 같습니다.

### 모델 상태[[huggingface_hub.inference._common.ModelStatus]]

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


## 추론 API[[huggingface_hub.InferenceApi]]

[`InferenceAPI`]는 추론 API를 호출하는 레거시 방식입니다. 이 인터페이스는 더 간단하며 각 작업의 입력 매개변수와 출력 형식을 알아야 합니다. 또한 추론 엔드포인트나 AWS SageMaker와 같은 다른 서비스에 연결할 수 있는 기능이 없습니다. [`InferenceAPI`]는 곧 폐지될 예정이므로 가능한 경우 [`InferenceClient`]를 사용하는 것을 권장합니다. 스크립트에서 [`InferenceAPI`]를 [`InferenceClient`]로 전환하는 방법에 대해 알아보려면 [이 가이드](../guides/inference#legacy-inferenceapi-client)를 참조하세요.

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
