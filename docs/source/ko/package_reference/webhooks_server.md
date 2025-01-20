<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# 웹훅 서버[[webhooks-server]]

웹훅은 MLOps 관련 기능의 기반이 됩니다. 이를 통해 특정 저장소의 새로운 변경 사항을 수신하거나, 관심 있는 특정 사용자/조직에 속한 모든 저장소의 변경 사항을 받아볼 수 있습니다.
Huggingface Hub의 웹훅에 대해 더 자세히 알아보려면 이 [가이드](https://huggingface.co/docs/hub/webhooks)를 읽어보세요.

<Tip>

웹훅 서버를 설정하고 Space로 배포하는 방법은 이 단계별 [가이드](../guides/webhooks_server)를 확인하세요.

</Tip>

<Tip warning={true}>

이 기능은 실험적인 기능입니다. 본 API는 현재 개선 작업 중이며, 향후 사전 통지 없이 주요 변경 사항이 도입될 수 있음을 의미합니다. `requirements`에서 `huggingface_hub`의 버전을 고정하는 것을 권장합니다. 참고로 실험적 기능을 사용하면 경고가 트리거 됩니다. 이 경고 트리거를 비활성화 시키길 원한다면 환경변수 `HF_HUB_DISABLE_EXPERIMENTAL_WARNING=1`를 설정하세요.

</Tip>

## 서버[[server]]
여기서 서버는 하나의 [Gradio](https://gradio.app/) 앱을 의미합니다. Gradio에는 사용자 또는 사용자에게 지침을 표시하는 UI와 웹훅을 수신하기 위한 API가 있습니다. 웹훅 엔드포인트를 구현하는 것은 함수에 데코레이터를 추가하는 것만큼 간단합니다. 서버를 Space에 배포하기 전에 Gradio 터널을 사용하여 웹훅을 머신으로 리디렉션하여 디버깅할 수 있습니다.

### WebhooksServer[[huggingface_hub.WebhooksServer]]

### huggingface_hub.WebhooksServer

```python
The [`WebhooksServer`] class lets you create an instance of a Gradio app that can receive Huggingface webhooks.
These webhooks can be registered using the [`~WebhooksServer.add_webhook`] decorator. Webhook endpoints are added to
the app as a POST endpoint to the FastAPI router. Once all the webhooks are registered, the `launch` method has to be
called to start the app.

It is recommended to accept [`WebhookPayload`] as the first argument of the webhook function. It is a Pydantic
model that contains all the information about the webhook event. The data will be parsed automatically for you.

Check out the [webhooks guide](../guides/webhooks_server) for a step-by-step tutorial on how to setup your
WebhooksServer and deploy it on a Space.

<Tip warning={true}>

`WebhooksServer` is experimental. Its API is subject to change in the future.

</Tip>

<Tip warning={true}>

You must have `gradio` installed to use `WebhooksServer` (`pip install --upgrade gradio`).

</Tip>

Args:
    ui (`gradio.Blocks`, optional):
        A Gradio UI instance to be used as the Space landing page. If `None`, a UI displaying instructions
        about the configured webhooks is created.
    webhook_secret (`str`, optional):
        A secret key to verify incoming webhook requests. You can set this value to any secret you want as long as
        you also configure it in your [webhooks settings panel](https://huggingface.co/settings/webhooks). You
        can also set this value as the `WEBHOOK_SECRET` environment variable. If no secret is provided, the
        webhook endpoints are opened without any security.

Example:

    ```python
    import gradio as gr
    from huggingface_hub import WebhooksServer, WebhookPayload

    with gr.Blocks() as ui:
        ...

    app = WebhooksServer(ui=ui, webhook_secret="my_secret_key")

    @app.add_webhook("/say_hello")
    async def hello(payload: WebhookPayload):
        return {"message": "hello"}

    app.launch()
    ```
```


### @webhook_endpoint[[huggingface_hub.webhook_endpoint]]

### huggingface_hub.webhook_endpoint

```python
Decorator to start a [`WebhooksServer`] and register the decorated function as a webhook endpoint.

This is a helper to get started quickly. If you need more flexibility (custom landing page or webhook secret),
you can use [`WebhooksServer`] directly. You can register multiple webhook endpoints (to the same server) by using
this decorator multiple times.

Check out the [webhooks guide](../guides/webhooks_server) for a step-by-step tutorial on how to setup your
server and deploy it on a Space.

<Tip warning={true}>

`webhook_endpoint` is experimental. Its API is subject to change in the future.

</Tip>

<Tip warning={true}>

You must have `gradio` installed to use `webhook_endpoint` (`pip install --upgrade gradio`).

</Tip>

Args:
    path (`str`, optional):
        The URL path to register the webhook function. If not provided, the function name will be used as the path.
        In any case, all webhooks are registered under `/webhooks`.

Examples:
    The default usage is to register a function as a webhook endpoint. The function name will be used as the path.
    The server will be started automatically at exit (i.e. at the end of the script).

    ```python
    from huggingface_hub import webhook_endpoint, WebhookPayload

    @webhook_endpoint
    async def trigger_training(payload: WebhookPayload):
        if payload.repo.type == "dataset" and payload.event.action == "update":
            # Trigger a training job if a dataset is updated
            ...

    # Server is automatically started at the end of the script.
    ```

    Advanced usage: register a function as a webhook endpoint and start the server manually. This is useful if you
    are running it in a notebook.

    ```python
    from huggingface_hub import webhook_endpoint, WebhookPayload

    @webhook_endpoint
    async def trigger_training(payload: WebhookPayload):
        if payload.repo.type == "dataset" and payload.event.action == "update":
            # Trigger a training job if a dataset is updated
            ...

    # Start the server manually
    trigger_training.launch()
    ```
```


## 페이로드[[huggingface_hub.WebhookPayload]]

[`WebhookPayload`]는 웹훅의 페이로드를 포함하는 기본 데이터 구조입니다. 이것은 `pydantic` 클래스로서 FastAPI에서 매우 쉽게 사용할 수 있습니다. 즉 WebhookPayload를 웹후크 엔드포인트에 매개변수로 전달하면 자동으로 유효성이 검사되고 파이썬 객체로 파싱됩니다.

웹훅 페이로드에 대한 자세한 사항은 이 [가이드](https://huggingface.co/docs/hub/webhooks#webhook-payloads)를 참고하세요.

### huggingface_hub.WebhookPayload

No docstring found for huggingface_hub.WebhookPayload


### WebhookPayload[[huggingface_hub.WebhookPayload]]

### huggingface_hub.WebhookPayload

No docstring found for huggingface_hub.WebhookPayload


### WebhookPayloadComment[[huggingface_hub.WebhookPayloadComment]]

### huggingface_hub.WebhookPayloadComment

No docstring found for huggingface_hub.WebhookPayloadComment


### WebhookPayloadDiscussion[[huggingface_hub.WebhookPayloadDiscussion]]

### huggingface_hub.WebhookPayloadDiscussion

No docstring found for huggingface_hub.WebhookPayloadDiscussion


### WebhookPayloadDiscussionChanges[[huggingface_hub.WebhookPayloadDiscussionChanges]]

### huggingface_hub.WebhookPayloadDiscussionChanges

No docstring found for huggingface_hub.WebhookPayloadDiscussionChanges


### WebhookPayloadEvent[[huggingface_hub.WebhookPayloadEvent]]

### huggingface_hub.WebhookPayloadEvent

No docstring found for huggingface_hub.WebhookPayloadEvent


### WebhookPayloadMovedTo[[huggingface_hub.WebhookPayloadMovedTo]]

### huggingface_hub.WebhookPayloadMovedTo

No docstring found for huggingface_hub.WebhookPayloadMovedTo


### WebhookPayloadRepo[[huggingface_hub.WebhookPayloadRepo]]

### huggingface_hub.WebhookPayloadRepo

No docstring found for huggingface_hub.WebhookPayloadRepo


### WebhookPayloadUrl[[huggingface_hub.WebhookPayloadUrl]]

### huggingface_hub.WebhookPayloadUrl

No docstring found for huggingface_hub.WebhookPayloadUrl


### WebhookPayloadWebhook[[huggingface_hub.WebhookPayloadWebhook]]

### huggingface_hub.WebhookPayloadWebhook

No docstring found for huggingface_hub.WebhookPayloadWebhook

