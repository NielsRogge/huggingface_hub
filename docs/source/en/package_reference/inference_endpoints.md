# Inference Endpoints

Inference Endpoints provides a secure production solution to easily deploy models on a dedicated and autoscaling infrastructure managed by Hugging Face. An Inference Endpoint is built from a model from the [Hub](https://huggingface.co/models). This page is a reference for `huggingface_hub`'s integration with Inference Endpoints. For more information about the Inference Endpoints product, check out its [official documentation](https://huggingface.co/docs/inference-endpoints/index).

<Tip>

Check out the [related guide](../guides/inference_endpoints) to learn how to use `huggingface_hub` to manage your Inference Endpoints programmatically.

</Tip>

Inference Endpoints can be fully managed via API. The endpoints are documented with [Swagger](https://api.endpoints.huggingface.cloud/). The [`InferenceEndpoint`] class is a simple wrapper built on top on this API.

## Methods

A subset of the Inference Endpoint features are implemented in [`HfApi`]:

- [`get_inference_endpoint`] and [`list_inference_endpoints`] to get information about your Inference Endpoints
- [`create_inference_endpoint`], [`update_inference_endpoint`] and [`delete_inference_endpoint`] to deploy and manage Inference Endpoints
- [`pause_inference_endpoint`] and [`resume_inference_endpoint`] to pause and resume an Inference Endpoint
- [`scale_to_zero_inference_endpoint`] to manually scale an Endpoint to 0 replicas

## InferenceEndpoint

The main dataclass is [`InferenceEndpoint`]. It contains information about a deployed `InferenceEndpoint`, including its configuration and current state. Once deployed, you can run inference on the Endpoint using the  [`InferenceEndpoint.client`] and [`InferenceEndpoint.async_client`] properties that respectively return an [`InferenceClient`] and an [`AsyncInferenceClient`] object.

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

## InferenceEndpointStatus

### InferenceEndpointStatus

```python
An enumeration.
```


## InferenceEndpointType

### InferenceEndpointType

```python
An enumeration.
```


## InferenceEndpointError

### InferenceEndpointError

```python
Generic exception when dealing with Inference Endpoints.
```

