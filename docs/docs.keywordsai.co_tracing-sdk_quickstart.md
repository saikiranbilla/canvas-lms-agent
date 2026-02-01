---
url: "https://docs.keywordsai.co/tracing-sdk/quickstart"
title: "Quickstart - Docs"
---

[Skip to main content](https://docs.keywordsai.co/tracing-sdk/quickstart#content-area)

[Docs home page![light logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/light.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=7a97b614ddd4af346e9de4ba118e1fd7)![dark logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/dark.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=b4d210c0b5c294be66b448eab084f3e5)](https://www.keywordsai.co/)

Search...

Ctrl K

##### Python Tracing SDK

- Getting Started

  - [Quickstart](https://docs.keywordsai.co/tracing-sdk/quickstart)
  - [Examples](https://docs.keywordsai.co/tracing-sdk/examples)
- Decorators

- Client API

- Contexts

- Instrumentation


##### TypeScript Tracing SDK

- Getting Started

- Methods

- Client API

- Configuration

- Instrumentation


##### Keywords AI SDK

- Getting Started

- Logs

- Prompts

- Experiments


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

Getting Started

Quickstart

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

Getting Started

# Quickstart

Copy page

Get started with the keywordsai-tracing Python SDK

Copy page

## [​](https://docs.keywordsai.co/tracing-sdk/quickstart\#installation)  Installation

**Python Requirement**: This package requires **Python 3.9** or later.

Copy

```
pip install keywordsai-tracing
```

## [​](https://docs.keywordsai.co/tracing-sdk/quickstart\#configure-credentials)  Configure credentials

Copy

```
import os
from keywordsai_tracing import KeywordsAITelemetry

os.environ["KEYWORDSAI_API_KEY"] = "your-api-key"
os.environ["KEYWORDSAI_BASE_URL"] = "https://api.keywordsai.co/api"

k_tl = KeywordsAITelemetry()
```

## [​](https://docs.keywordsai.co/tracing-sdk/quickstart\#trace-a-workflow-and-task)  Trace a workflow and task

Copy

```
from keywordsai_tracing.decorators import workflow, task

@workflow(name="hello_world")
def hello_world():
    @task(name="compute")
    def compute():
        return "Hello Tracing"
    return compute()

print(hello_world())
```

## [​](https://docs.keywordsai.co/tracing-sdk/quickstart\#class-methods-usage)  Class methods usage

Copy

```
from openai import OpenAI
from keywordsai_tracing import KeywordsAITelemetry
from keywordsai_tracing.decorators import workflow, task

k_tl = KeywordsAITelemetry()
client = OpenAI()

@workflow(name="joke_agent", method_name="run")
class JokeAgent:
    @task(name="joke_creation")
    def create_joke(self):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Tell me a joke about tracing"}],
        )
        return completion.choices[0].message.content

    def run(self):
        return self.create_joke()

print(JokeAgent().run())
```

## [​](https://docs.keywordsai.co/tracing-sdk/quickstart\#next-steps)  Next Steps

- Learn the [workflow decorator](https://docs.keywordsai.co/tracing-sdk/decorators/workflow)
- Learn the [task decorator](https://docs.keywordsai.co/tracing-sdk/decorators/task)
- Explore the [Client API](https://docs.keywordsai.co/tracing-sdk/client/get-client)
- Configure [Instrumentation](https://docs.keywordsai.co/tracing-sdk/instrumentation/overview)

Was this page helpful?

YesNo

[Suggest edits](https://github.com/keywords-ai/keywords-ai-docs/edit/main/tracing-sdk/quickstart.mdx) [Raise issue](https://github.com/keywords-ai/keywords-ai-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/tracing-sdk/quickstart)

[ExamplesReal examples from the keywordsai-tracing repo\\
\\
Next](https://docs.keywordsai.co/tracing-sdk/examples)

Ctrl+I

[linkedin](https://www.linkedin.com/company/keywordsai/) [github](https://github.com/keywordsai) [discord](https://discord.com/invite/KEanfAafQQ)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=keywordsai)

On this page

- [Installation](https://docs.keywordsai.co/tracing-sdk/quickstart#installation)
- [Configure credentials](https://docs.keywordsai.co/tracing-sdk/quickstart#configure-credentials)
- [Trace a workflow and task](https://docs.keywordsai.co/tracing-sdk/quickstart#trace-a-workflow-and-task)
- [Class methods usage](https://docs.keywordsai.co/tracing-sdk/quickstart#class-methods-usage)
- [Next Steps](https://docs.keywordsai.co/tracing-sdk/quickstart#next-steps)

Assistant

Responses are generated using AI and may contain mistakes.