---
url: "https://docs.keywordsai.co/get-started/quickstart/logging"
title: "Logging via API - Docs"
---

[Skip to main content](https://docs.keywordsai.co/get-started/quickstart/logging#content-area)

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

Logging via API

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

Quickstart

# Logging via API

Copy page

Send your LLM logs to Keywords AI and monitor them in real-time

Copy page

## [​](https://docs.keywordsai.co/get-started/quickstart/logging\#what-is-logging)  What is logging?

1. Send a `POST` request to log your AI conversations
2. See them appear instantly on your Keywords AI platform

![](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/observability/overview/logs.jpg)

## [​](https://docs.keywordsai.co/get-started/quickstart/logging\#use-logging-api)  Use logging API

### [​](https://docs.keywordsai.co/get-started/quickstart/logging\#1-get-your-keywords-ai-api-key)  1\. Get your Keywords AI API key

After you create an account on [Keywords AI](https://platform.keywordsai.co/), you can get your API key from the [API keys page](https://platform.keywordsai.co/platform/api/api-keys).

![Create API key placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/api-keys.png)

### [​](https://docs.keywordsai.co/get-started/quickstart/logging\#2-integrate-async-logging-into-your-codebase)  2\. Integrate Async Logging into your codebase

Python

TypeScript

cURL

Copy

```
import requests
import json

url = "https://api.keywordsai.co/api/request-logs/create/"
payload = {
    "model": "gpt-4o",
    "log_type": "chat",
    "input": json.dumps([\
        {\
            "role": "user",\
            "content": "How can I help a customer with a billing issue?"\
        }\
    ]),
    "output": json.dumps({
        "role": "assistant",
        "content": "I'd be happy to help with billing issues. First, let me check your account details..."
    }),
    "customer_identifier": "support_agent_001"
}

headers = {
    "Authorization": "Bearer YOUR_KEYWORDS_AI_API_KEY",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)
```

### [​](https://docs.keywordsai.co/get-started/quickstart/logging\#3-check-your-logs-on-the-platform)  3\. Check your logs on the platform

After you integrate the async logging into your codebase and send the request successfully, you can check your logs on the [Logs page](https://platform.keywordsai.co/platform/requests).

![Logs page placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/documentation/get-started/logging_showlog.png)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/keywords-ai/keywords-ai-docs/edit/main/get-started/quickstart/logging.mdx) [Raise issue](https://github.com/keywords-ai/keywords-ai-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/get-started/quickstart/logging)

[Previous](https://docs.keywordsai.co/get-started/overview) [Agent tracingYou can use Keywords AI Traces to trace your LLM requests and responses.\\
\\
Next](https://docs.keywordsai.co/get-started/quickstart/tracing)

Ctrl+I

[linkedin](https://www.linkedin.com/company/keywordsai/) [github](https://github.com/keywordsai) [discord](https://discord.com/invite/KEanfAafQQ)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=keywordsai)

On this page

- [What is logging?](https://docs.keywordsai.co/get-started/quickstart/logging#what-is-logging)
- [Use logging API](https://docs.keywordsai.co/get-started/quickstart/logging#use-logging-api)
- [1\. Get your Keywords AI API key](https://docs.keywordsai.co/get-started/quickstart/logging#1-get-your-keywords-ai-api-key)
- [2\. Integrate Async Logging into your codebase](https://docs.keywordsai.co/get-started/quickstart/logging#2-integrate-async-logging-into-your-codebase)
- [3\. Check your logs on the platform](https://docs.keywordsai.co/get-started/quickstart/logging#3-check-your-logs-on-the-platform)

Assistant

Responses are generated using AI and may contain mistakes.

![](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/observability/overview/logs.jpg)

![Create API key placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/api-keys.png)

![Logs page placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/documentation/get-started/logging_showlog.png)