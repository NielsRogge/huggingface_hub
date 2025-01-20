# 추론 엔드포인트 [[inference-endpoints]]

Hugging Face가 관리하는 추론 엔드포인트는 우리가 모델을 쉽고 안전하게 배포할 수 있게 해주는 도구입니다. 이러한 추론 엔드포인트는 [Hub](https://huggingface.co/models)에 있는 모델을 기반으로 설계되었습니다. 이 문서는 `huggingface_hub`와 추론 엔드포인트 통합에 관한 참조 페이지이며, 더욱 자세한 정보는 [공식 문서](https://huggingface.co/docs/inference-endpoints/index)를 통해 확인할 수 있습니다.

<Tip>

'huggingface_hub'를 사용하여 추론 엔드포인트를 프로그래밍 방식으로 관리하는 방법을 알고 싶다면, [관련 가이드](../guides/inference_endpoints)를 확인해 보세요.

</Tip>

추론 엔드포인트는 API로 쉽게 접근할 수 있습니다. 이 엔드포인트들은 [Swagger](https://api.endpoints.huggingface.cloud/)를 통해 문서화되어 있고, [`InferenceEndpoint`] 클래스는 이 API를 사용해 만든 간단한 래퍼입니다.

## 매소드 [[methods]]

다음과 같은 추론 엔드포인트의 기능이 [`HfApi`]안에 구현되어 있습니다:

- [`get_inference_endpoint`]와 [`list_inference_endpoints`]를 사용해 엔드포인트 정보를 조회할 수 있습니다.
- [`create_inference_endpoint`], [`update_inference_endpoint`], [`delete_inference_endpoint`]로 엔드포인트를 배포하고 관리할 수 있습니다.
- [`pause_inference_endpoint`]와 [`resume_inference_endpoint`]로 엔드포인트를 잠시 멈추거나 다시 시작할 수 있습니다.
- [`scale_to_zero_inference_endpoint`]로 엔드포인트의 복제본을 0개로 설정할 수 있습니다.

## InferenceEndpoint [[huggingface_hub.InferenceEndpoint]]

기본 데이터 클래스는 [`InferenceEndpoint`]입니다. 여기에는 구성 및 현재 상태를 가지고 있는 배포된 `InferenceEndpoint`에 대한 정보가 포함되어 있습니다. 배포 후에는 [`InferenceEndpoint.client`]와 [`InferenceEndpoint.async_client`]를 사용해 엔드포인트에서 추론 작업을 할 수 있고, 이때 [`InferenceClient`]와 [`AsyncInferenceClient`] 객체를 반환합니다.

### InferenceEndpoint

```python
Contains information about a deployed Inference Endpoint.

Args:
    name (`str`):
        The unique name of the Inference Endpoint.
    namespace (`str`):
        The namespace where the Inference Endpoint is located.
    repository (`str`):
        The name of the model repository deployed on this Inference Endpoint.
    status ([`InferenceEndpointStatus`]):
        The current status of the Inference Endpoint.
    url (`str`, *optional*):
        The URL of the Inference Endpoint, if available. Only a deployed Inference Endpoint will have a URL.
    framework (`str`):
        The machine learning framework used for the model.
    revision (`str`):
        The specific model revision deployed on the Inference Endpoint.
    task (`str`):
        The task associated with the deployed model.
    created_at (`datetime.datetime`):
        The timestamp when the Inference Endpoint was created.
    updated_at (`datetime.datetime`):
        The timestamp of the last update of the Inference Endpoint.
    type ([`InferenceEndpointType`]):
        The type of the Inference Endpoint (public, protected, private).
    raw (`Dict`):
        The raw dictionary data returned from the API.
    token (`str` or `bool`, *optional*):
        Authentication token for the Inference Endpoint, if set when requesting the API. Will default to the
        locally saved token if not provided. Pass `token=False` if you don't want to send your token to the server.

Example:
    ```python
    >>> from huggingface_hub import get_inference_endpoint
    >>> endpoint = get_inference_endpoint("my-text-to-image")
    >>> endpoint
    InferenceEndpoint(name='my-text-to-image', ...)

    # Get status
    >>> endpoint.status
    'running'
    >>> endpoint.url
    'https://my-text-to-image.region.vendor.endpoints.huggingface.cloud'

    # Run inference
    >>> endpoint.client.text_to_image(...)

    # Pause endpoint to save $$$
    >>> endpoint.pause()

    # ...
    # Resume and wait for deployment
    >>> endpoint.resume()
    >>> endpoint.wait()
    >>> endpoint.client.text_to_image(...)
    ```
```

  - from_raw
  - client
  - async_client
  - all

## InferenceEndpointStatus [[huggingface_hub.InferenceEndpointStatus]]

### InferenceEndpointStatus

```python
An enumeration.
```


## InferenceEndpointType [[huggingface_hub.InferenceEndpointType]]

### InferenceEndpointType

```python
An enumeration.
```


## InferenceEndpointError [[huggingface_hub.InferenceEndpointError]]

### InferenceEndpointError

```python
Generic exception when dealing with Inference Endpoints.
```

