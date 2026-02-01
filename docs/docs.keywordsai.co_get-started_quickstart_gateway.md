---
url: "https://docs.keywordsai.co/get-started/quickstart/gateway"
title: "AI gateway"
---

[Skip to main content](https://docs.keywordsai.co/get-started/quickstart/gateway#content-area)

[Docs home page![light logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/light.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=7a97b614ddd4af346e9de4ba118e1fd7)![dark logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/dark.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=b4d210c0b5c294be66b448eab084f3e5)](https://www.keywordsai.co/)

Search...

Ctrl K

##### Get started

- [Overview](https://docs.keywordsai.co/get-started/overview)
- Quickstart

  - [Logging via API](https://docs.keywordsai.co/get-started/quickstart/logging)
  - [Agent tracing](https://docs.keywordsai.co/get-started/quickstart/tracing)
  - [AI gateway](https://docs.keywordsai.co/get-started/quickstart/gateway)
  - [Create a prompt](https://docs.keywordsai.co/get-started/quickstart/prompt_management)
  - [Evaluations](https://docs.keywordsai.co/get-started/quickstart/evaluation)
- [Observability data model](https://docs.keywordsai.co/get-started/observability_data_model)

##### Features

- Observability

- Prompt management

- Evals

- LLM Gateway

  - [AI gateway](https://docs.keywordsai.co/get-started/quickstart/gateway)
  - [Supported models](https://docs.keywordsai.co/documentation/products/gateway/configuration/models)
  - [Load balancing](https://docs.keywordsai.co/documentation/products/gateway/traffic_management/load-balancing)
  - [Retries](https://docs.keywordsai.co/documentation/products/gateway/traffic_management/retries)
  - [Fallback models](https://docs.keywordsai.co/documentation/products/gateway/traffic_management/fallbacks)
  - [Rate limit](https://docs.keywordsai.co/documentation/products/gateway/traffic_management/rate_limit)
  - Caches

  - [Function calling](https://docs.keywordsai.co/documentation/products/gateway/advanced_features/function_calling)
  - [Enable thinking](https://docs.keywordsai.co/documentation/products/gateway/advanced_features/thinking)
  - [Upload PDF](https://docs.keywordsai.co/documentation/products/gateway/advanced_features/upload_pdf)
  - [Upload image](https://docs.keywordsai.co/documentation/products/gateway/advanced_features/upload_image)
  - [Disable logging](https://docs.keywordsai.co/documentation/products/gateway/monitoring_analysis/disable_logging)
- Notifications

- Automations (Beta)


##### Admin

- [Keywords API keys](https://docs.keywordsai.co/documentation/admin/keywords_api_keys)
- [LLM provider keys](https://docs.keywordsai.co/documentation/admin/llm_provider_keys)
- Team management


##### Security

- [Trust center](https://docs.keywordsai.co/documentation/security/trust_center)
- [SOC II](https://docs.keywordsai.co/documentation/security/socii)
- [HIPAA Compliance](https://docs.keywordsai.co/documentation/security/hipaa)
- [GDPR](https://docs.keywordsai.co/documentation/security/gdpr)
- [Architecture review](https://docs.keywordsai.co/documentation/security/architecture_review)
- [Security FAQ](https://docs.keywordsai.co/documentation/security/security-qa)

##### Resources

- [Model Context Protocol (MCP)](https://docs.keywordsai.co/documentation/resources/mcp)
- [What is LLM monitoring?](https://docs.keywordsai.co/documentation/resources/what-is-llm-observability-and-monitoring)
- [Automatic retries](https://docs.keywordsai.co/documentation/resources/automatic-retries)
- [How streaming works](https://docs.keywordsai.co/documentation/resources/streaming)
- [Error handling](https://docs.keywordsai.co/documentation/resources/error-handling)
- [API rate limits](https://docs.keywordsai.co/documentation/resources/api-rate-limits)

##### Help & Community

- [Support](https://docs.keywordsai.co/documentation/support/support)
- [Feedback](https://docs.keywordsai.co/documentation/support/feedback)
- [Status](https://docs.keywordsai.co/documentation/support/status)

- [Discord](https://discord.com/invite/KEanfAafQQ)
- [platform](https://platform.keywordsai.co/)

[Docs home page![light logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/light.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=7a97b614ddd4af346e9de4ba118e1fd7)![dark logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/dark.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=b4d210c0b5c294be66b448eab084f3e5)](https://www.keywordsai.co/)

Search...

Ctrl K

- [Discord](https://discord.com/invite/KEanfAafQQ)
- [platform](https://platform.keywordsai.co/)
- [platform](https://platform.keywordsai.co/)

Search...

Navigation

Quickstart

AI gateway

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

Quickstart

# AI gateway

Copy page

Keywords AI AI gateway supports you call 250+ LLMs using the same input/output format.

Copy page

* * *

## [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#what-is-ai-gateway)  What is AI gateway?

Keywords AI’s AI Gateway is a gateway that lets you interface with 250+ large language models (LLMs) via one unified API.

Input

LLM gateway

250+ LLMs

Model fallback

Load balancing

Prompt caching

Optimized LLM Output

### [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#considerations:)  Considerations:

- May not be suitable for products with strict latency requirements ( **50 - 150ms** added).
- May not be ideal for those who do not want to integrate a third-party service into the core of their application.

## [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#use-ai-gateway)  Use AI gateway

### [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#1-get-your-keywords-ai-api-key)  1\. Get your Keywords AI API key

After you create an account on [Keywords AI](https://platform.keywordsai.co/), you can get your API key from the [API keys page](https://platform.keywordsai.co/platform/api/api-keys).

![Create API key placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/api-keys.png)

### [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#2-set-up-llm-provider-api-key)  2\. Set up LLM provider API key

**Environment Management**: To separate test and production environments, create separate API keys for each environment instead of using an `env` parameter. This approach provides better security and clearer separation between your development and production workflows.

For all AI gateway users, you have to add your own credentials to activate AI gateway. We will use your credentials to call LLMs on your behalf.

For example, if you want to use OpenAI, you have to add your OpenAI API key to activate AI gateway.
We won’t use your credentials for any other purposes.

- [Set up LLM provider API key](https://platform.keywordsai.co/platform/api/providers)

### [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#3-call-a-llm)  3\. Call a LLM

You can use the standard API call to connect 250+ LLMs.

Python

TypeScript

Bash

PHP

Go

Copy

```
import requests
def demo_call(input,
              model="gpt-4o-mini",
              token="YOUR_KEYWORDS_AI_API_KEY"
              ):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': input}],
    }

    response = requests.post('https://api.keywordsai.co/api/chat/completions', headers=headers, json=data)
    return response

messages = "Say 'Hello World'"
print(demo_call(messages).json())
```

### [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#4-parameters)  4\. Parameters

OpenAI Parameters

We support all OpenAI parameters, which is the standard format for LLMs. You can check out important [OpenAI parameters in this page](https://docs.keywordsai.co/api-endpoints/develop/gateway/chat-completions#openai-compatible-parameters). You can also learn more about OpenAI parameters [here](https://platform.openai.com/docs/api-reference/chat).

Keywords AI Parameters

Use these when you want to achieve specific goals. For example, you can use `fallback_models` to specify fallback models when the primary model is down. You can check out all [Keywords AI parameters in this page](https://docs.keywordsai.co/api-endpoints/develop/gateway/chat-completions#keywords-ai-parameters).

## [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#integrate-with-your-existing-ai-framework)  Integrate with your existing AI framework

Keywords AI offers various integration options, including all mainstream LLM frameworks and REST APIs.

### [​](https://docs.keywordsai.co/get-started/quickstart/gateway\#supported-frameworks)  Supported frameworks

[![OpenAI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/openai_sdk_v0.png)![OpenAI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/openai_sdk_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/llm_framework/openai/openai-sdk)[![LangChain SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/langchain_v0.png)![LangChain SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/langchain_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/llm_framework/langchain)[![Vercel AI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/vercelai_sdk_v0.png)![Vercel AI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/vercelai_sdk_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/llm_framework/vercel)[![LlamaIndex SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/llamaindex_v0.png)![LlamaIndex SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/llamaindex_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/llm_framework/llama-index)[![Google GenAI](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/genai_v0.png)![Google GenAI](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/genai_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/llm_framework/google_genai)[![Anthropic](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/anthropic_v0.png)![Anthropic](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/anthropic_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/llm_framework/anthropic)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/keywords-ai/keywords-ai-docs/edit/main/get-started/quickstart/gateway.mdx) [Raise issue](https://github.com/keywords-ai/keywords-ai-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/get-started/quickstart/gateway)

[Previous](https://docs.keywordsai.co/get-started/quickstart/tracing) [Create a promptA complete guide to create, deploy, and use prompts in your codebase.\\
\\
Next](https://docs.keywordsai.co/get-started/quickstart/prompt_management)

Ctrl+I

[linkedin](https://www.linkedin.com/company/keywordsai/) [github](https://github.com/keywordsai) [discord](https://discord.com/invite/KEanfAafQQ)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=keywordsai)

On this page

- [What is AI gateway?](https://docs.keywordsai.co/get-started/quickstart/gateway#what-is-ai-gateway)
- [Considerations:](https://docs.keywordsai.co/get-started/quickstart/gateway#considerations%3A)
- [Use AI gateway](https://docs.keywordsai.co/get-started/quickstart/gateway#use-ai-gateway)
- [1\. Get your Keywords AI API key](https://docs.keywordsai.co/get-started/quickstart/gateway#1-get-your-keywords-ai-api-key)
- [2\. Set up LLM provider API key](https://docs.keywordsai.co/get-started/quickstart/gateway#2-set-up-llm-provider-api-key)
- [3\. Call a LLM](https://docs.keywordsai.co/get-started/quickstart/gateway#3-call-a-llm)
- [4\. Parameters](https://docs.keywordsai.co/get-started/quickstart/gateway#4-parameters)
- [Integrate with your existing AI framework](https://docs.keywordsai.co/get-started/quickstart/gateway#integrate-with-your-existing-ai-framework)
- [Supported frameworks](https://docs.keywordsai.co/get-started/quickstart/gateway#supported-frameworks)

Assistant

Responses are generated using AI and may contain mistakes.

![Create API key placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/api-keys.png)

![OpenAI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/openai_sdk_v0.png)

![OpenAI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/openai_sdk_v0_black.png)

![LangChain SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/langchain_v0.png)

![LangChain SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/langchain_v0_black.png)

![Vercel AI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/vercelai_sdk_v0.png)

![Vercel AI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/vercelai_sdk_v0_black.png)

![LlamaIndex SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/llamaindex_v0.png)

![LlamaIndex SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/llamaindex_v0_black.png)

![Google GenAI](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/genai_v0.png)

![Google GenAI](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/genai_v0_black.png)

![Anthropic](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/anthropic_v0.png)

![Anthropic](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/anthropic_v0_black.png)