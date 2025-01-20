<!--⚠️ Note that this file is in Markdown but contains specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.
-->

# Webhooks Server

Webhooks are a foundation for MLOps-related features. They allow you to listen for new changes on specific repos or to
all repos belonging to particular users/organizations you're interested in following. To learn
more about webhooks on the Huggingface Hub, you can read the Webhooks [guide](https://huggingface.co/docs/hub/webhooks).

<Tip>

Check out this [guide](../guides/webhooks_server) for a step-by-step tutorial on how to setup your webhooks server and
deploy it as a Space.

</Tip>

<Tip warning={true}>

This is an experimental feature. This means that we are still working on improving the API. Breaking changes might be
introduced in the future without prior notice. Make sure to pin the version of `huggingface_hub` in your requirements.
A warning is triggered when you use an experimental feature. You can disable it by setting `HF_HUB_DISABLE_EXPERIMENTAL_WARNING=1` as an environment variable.

</Tip>

## Server

The server is a [Gradio](https://gradio.app/) app. It has a UI to display instructions for you or your users and an API
to listen to webhooks. Implementing a webhook endpoint is as simple as decorating a function. You can then debug it
by redirecting the Webhooks to your machine (using a Gradio tunnel) before deploying it to a Space.

### WebhooksServer

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


### @webhook_endpoint

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


## Payload

[`WebhookPayload`] is the main data structure that contains the payload from Webhooks. This is
a `pydantic` class which makes it very easy to use with FastAPI. If you pass it as a parameter to a webhook endpoint, it
will be automatically validated and parsed as a Python object.

For more information about webhooks payload, you can refer to the Webhooks Payload [guide](https://huggingface.co/docs/hub/webhooks#webhook-payloads).

### huggingface_hub.WebhookPayload

No docstring found for huggingface_hub.WebhookPayload


### WebhookPayload

### huggingface_hub.WebhookPayload

No docstring found for huggingface_hub.WebhookPayload


### WebhookPayloadComment

### huggingface_hub.WebhookPayloadComment

No docstring found for huggingface_hub.WebhookPayloadComment


### WebhookPayloadDiscussion

### huggingface_hub.WebhookPayloadDiscussion

No docstring found for huggingface_hub.WebhookPayloadDiscussion


### WebhookPayloadDiscussionChanges

### huggingface_hub.WebhookPayloadDiscussionChanges

No docstring found for huggingface_hub.WebhookPayloadDiscussionChanges


### WebhookPayloadEvent

### huggingface_hub.WebhookPayloadEvent

No docstring found for huggingface_hub.WebhookPayloadEvent


### WebhookPayloadMovedTo

### huggingface_hub.WebhookPayloadMovedTo

No docstring found for huggingface_hub.WebhookPayloadMovedTo


### WebhookPayloadRepo

### huggingface_hub.WebhookPayloadRepo

No docstring found for huggingface_hub.WebhookPayloadRepo


### WebhookPayloadUrl

### huggingface_hub.WebhookPayloadUrl

No docstring found for huggingface_hub.WebhookPayloadUrl


### WebhookPayloadWebhook

### huggingface_hub.WebhookPayloadWebhook

No docstring found for huggingface_hub.WebhookPayloadWebhook

