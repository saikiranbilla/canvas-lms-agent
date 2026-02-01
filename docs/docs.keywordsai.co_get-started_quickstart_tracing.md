---
url: "https://docs.keywordsai.co/get-started/quickstart/tracing"
title: "LLM tracing"
---

[Skip to main content](https://docs.keywordsai.co/get-started/quickstart/tracing#content-area)

[Docs home page![light logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/light.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=7a97b614ddd4af346e9de4ba118e1fd7)![dark logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/dark.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=b4d210c0b5c294be66b448eab084f3e5)](https://www.keywordsai.co/)

Search...

⌘K

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

⌘K

- [Discord](https://discord.com/invite/KEanfAafQQ)
- [platform](https://platform.keywordsai.co/)
- [platform](https://platform.keywordsai.co/)

Search...

Navigation

Quickstart

Agent tracing

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

Quickstart

# Agent tracing

Copy page

You can use Keywords AI Traces to trace your LLM requests and responses.

Copy page

## [​](https://docs.keywordsai.co/get-started/quickstart/tracing\#what-is-traces)  What is traces?

Traces are a chained collection of workflows and tasks. You can use tree views and waterfalls to better track dependencies and latency.

![Agent tracing visualization](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/documentation/get-started/overview/trace_tree_v1.png)

## [​](https://docs.keywordsai.co/get-started/quickstart/tracing\#use-agent-tracing)  Use agent tracing

### [​](https://docs.keywordsai.co/get-started/quickstart/tracing\#1-get-your-keywords-ai-api-key)  1\. Get your Keywords AI API key

After you create an account on [Keywords AI](https://platform.keywordsai.co/), you can get your API key from the [API keys page](https://platform.keywordsai.co/platform/api/api-keys).

![](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/documentation/admin/kai_create_api_key_v0.png)

### [​](https://docs.keywordsai.co/get-started/quickstart/tracing\#2-keywords-ai-native-opentelemetry)  2\. Keywords AI Native (OpenTelemetry)

You just need to add the `keywordsai_tracing` package to your project and annotate your workflows.

- Python

- JS/TS


1

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/tracing#)

Install the SDK

**Python Requirement**: This package requires **Python 3.9** or later.

pip

Copy

```
pip install keywordsai-tracing
```

2

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/tracing#)

Set up Environment Variables

Get your API key from the [API Keys page](https://platform.keywordsai.co/platform/api/api-keys) in Settings, then configure it in your environment:

.env

Copy

```
KEYWORDSAI_BASE_URL="https://api.keywordsai.co/api"
KEYWORDSAI_API_KEY="YOUR_KEYWORDSAI_API_KEY"
```

3

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/tracing#)

A full example with LLM calls

Use the `@workflow` and `@task` decorators to instrument your code:

Python

Copy

```
import os
from openai import OpenAI
from keywordsai_tracing.decorators import workflow, task
from keywordsai_tracing.main import KeywordsAITelemetry

# Initialize Keywords AI Telemetry
os.environ["KEYWORDSAI_API_KEY"] = "YOUR_KEYWORDSAI_API_KEY"
k_tl = KeywordsAITelemetry()

# Initialize OpenAI client
client = OpenAI()

@task(name="joke_creation")
def create_joke():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Tell me a joke about AI"}],
        temperature=0.7,
        max_tokens=100,
    )
    return completion.choices[0].message.content

@workflow(name="simple_joke_workflow")
def joke_workflow():
    joke = create_joke()
    return joke

if __name__ == "__main__":
    result = joke_workflow()
    print(result)
```

1

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/tracing#)

Install the SDK

Install the package using your preferred package manager:

Copy

```
npm install @keywordsai/tracing
# or yarn

yarn add @keywordsai/tracing
```

2

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/tracing#)

Set up Environment Variables

Get your API key from the [API Keys page](https://platform.keywordsai.co/platform/api/api-keys) in Settings, then configure it in your environment:

.env

Copy

```
KEYWORDSAI_BASE_URL="https://api.keywordsai.co/api"
KEYWORDSAI_API_KEY="YOUR_KEYWORDSAI_API_KEY"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

3

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/tracing#)

Create a simple workflow

server.ts

Copy

```
import { KeywordsAITelemetry } from '@keywordsai/tracing';
import OpenAI from 'openai';

// Initialize Keywords AI Telemetry
const keywordsAi = new KeywordsAITelemetry({
    apiKey: process.env.KEYWORDSAI_API_KEY || "",
    appName: 'test-app',
    disableBatch: true  // For testing, disable batching
});

// Initialize OpenAI client
const openai = new OpenAI();

async function createJoke() {
    return await keywordsAi.withTask(
        { name: 'joke_creation' },
        async () => {
            const completion = await openai.chat.completions.create({
                messages: [{ role: 'user', content: 'Tell me a joke about AI' }],
                model: 'gpt-4o-mini',
                temperature: 0.7,
                max_tokens: 100
            });
            return completion.choices[0].message.content;
        }
    );
}

async function simpleJokeWorkflow() {
    return await keywordsAi.withWorkflow(
        { name: 'simple_joke_workflow' },
        async () => {
            const joke = await createJoke();
            return joke;
        }
    );
}

// Run the workflow
async function main() {
    const result = await simpleJokeWorkflow();
    console.log(result);
}

main().catch(console.error);
```

Optional HTTP instrumentation
If you see logs like:install the OpenTelemetry instrumentations to enable and silence these messages:

Copy

```
pip install opentelemetry-instrumentation-requests opentelemetry-instrumentation-urllib3
```

This is optional; tracing works without them. Add only if your app uses `requests` or `urllib3`.

### [​](https://docs.keywordsai.co/get-started/quickstart/tracing\#3-view-your-traces)  3\. View your traces

You can now see your traces in the [Traces](https://platform.keywordsai.co/platform/traces).

![Agent tracing visualization](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/documentation/get-started/overview/trace_tree_v1.png)

## [​](https://docs.keywordsai.co/get-started/quickstart/tracing\#integrate-with-your-existing-ai-framework)  Integrate with your existing AI framework

Keywords AI also integrates seamlessly with popular AI frameworks to give you complete observability into your agent workflows.

[![OpenAI Agents SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/openai_agent_v0.png)![OpenAI Agents SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/openai_agent_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/tracing/openai-agents-sdk)[![Vercel AI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/vercel_v0.png)![Vercel AI SDK](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/vercel_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/tracing/vercel-tracing)[![Mastra](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/mastra_v0.png)![Mastra](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/Integrations/integration_cards/mastra_v0_black.png)](https://docs.keywordsai.co/integration/development-frameworks/tracing/mastra)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/keywords-ai/keywords-ai-docs/edit/main/get-started/quickstart/tracing.mdx) [Raise issue](https://github.com/keywords-ai/keywords-ai-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/get-started/quickstart/tracing)

[Previous](https://docs.keywordsai.co/get-started/quickstart/logging) [AI gatewayKeywords AI AI gateway supports you call 250+ LLMs using the same input/output format.\\
\\
Next](https://docs.keywordsai.co/get-started/quickstart/gateway)

⌘I

[linkedin](https://www.linkedin.com/company/keywordsai/) [github](https://github.com/keywordsai) [discord](https://discord.com/invite/KEanfAafQQ)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=keywordsai)

On this page

- [What is traces?](https://docs.keywordsai.co/get-started/quickstart/tracing#what-is-traces)
- [Use agent tracing](https://docs.keywordsai.co/get-started/quickstart/tracing#use-agent-tracing)
- [1\. Get your Keywords AI API key](https://docs.keywordsai.co/get-started/quickstart/tracing#1-get-your-keywords-ai-api-key)
- [2\. Keywords AI Native (OpenTelemetry)](https://docs.keywordsai.co/get-started/quickstart/tracing#2-keywords-ai-native-opentelemetry)
- [3\. View your traces](https://docs.keywordsai.co/get-started/quickstart/tracing#3-view-your-traces)
- [Integrate with your existing AI framework](https://docs.keywordsai.co/get-started/quickstart/tracing#integrate-with-your-existing-ai-framework)