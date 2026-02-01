---
url: "https://docs.keywordsai.co/get-started/quickstart/prompt_management"
title: "Create a prompt - Docs"
---

[Skip to main content](https://docs.keywordsai.co/get-started/quickstart/prompt_management#content-area)

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

Create a prompt

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

Quickstart

# Create a prompt

Copy page

A complete guide to create, deploy, and use prompts in your codebase.

Copy page

## [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#what-is-prompt-management)  What is prompt management?

Prompt management helps you create, version, share, and deploy prompt templates easily. Instead of hardcoding prompts in your application, you can manage them centrally, collaborate with your team, and monitor their performance.

## [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#why-use-prompt-management)  Why use prompt management?

Instead of hardcoding prompts in your application, reference them by ID.

Without prompt

With prompt

Copy

```
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[\
        {\
            "role": "system",\
            "content": "You are a helpful customer support agent for TechCorp."\
        },\
        {\
            "role": "user",\
            "content": f"Customer {customer_name} is asking about {issue_type}"\
        }\
    ]
)
```

## [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#use-prompt-management)  Use prompt management

### [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#1-get-your-keywords-ai-api-key)  1\. Get your Keywords AI API key

After you create an account on [Keywords AI](https://platform.keywordsai.co/), you can get your API key from the [API keys page](https://platform.keywordsai.co/platform/api/api-keys).

![Create API key placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/api-keys.png)

### [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#2-set-up-llm-provider-api-key)  2\. Set up LLM provider API key

**Environment Management**: To separate test and production environments, create separate API keys for each environment instead of using an `env` parameter. This approach provides better security and clearer separation between your development and production workflows.

For all AI gateway users, you have to add your own credentials to activate AI gateway. We will use your credentials to call LLMs on your behalf.

For example, if you want to use OpenAI, you have to add your OpenAI API key to activate AI gateway.
We won’t use your credentials for any other purposes.

- [Set up LLM provider API key](https://platform.keywordsai.co/platform/api/providers)

### [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#3-create-your-first-prompt)  3\. Create your first prompt

1

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/prompt_management#)

Create a new prompt

Once you have signed up and created an account, you can create a new prompt on the platform. Go to the [Prompts page](https://platform.keywordsai.co/platform/prompts) and click on the “Create new prompt” button. You should name your prompt and could add a description to it.![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/create-new-prompt.png)

2

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/prompt_management#)

Configure the prompt

Once you have created a new prompt, you can configure it. Go to the `Editor` tab and you can begin to write your prompt. The right side of the screen defines your prompt. You can set parameters like `Model`, `Temperature`, `Max Tokens`, and `Top P`. You can also add function calls and fallback models to your prompt. Check out the details [here](https://docs.keywordsai.co/api-endpoints/observe/logs/create).![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/configure-prompt.png)

3

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/prompt_management#)

Write the content

Once you have configured your prompt, you can write the content of your prompt. Click on the `+ Add message` button to add a new message to your prompt. You can change the role of the message to `user` or `assistant` by clicking on the role name.![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/write-prompt.png)

4

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/prompt_management#)

Variables in the prompt

You can also add variables to your prompt. Variables are placeholders for dynamic content that can be used to generate prompts. Simply add double curly braces `{{variable_name}}` to your prompt and you will be able to use the variable in your prompt.Replace the User message with this:

Copy

```
Please develop an optimized Python function to {{task_description}},
utilizing {{specific_library}},include error handling, and write unit tests for the function.
```

The format of the variable can’t be `{{task description}}`. It should be `{{task_description}}` with ”\_” instead of spaces.

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/prompt-variables.png)

5

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/prompt_management#)

Commit the first version

After did this, you can:

1. Add a value for each variable in the `Variables` tab.
2. Click `Run` to test your prompt.

You now just finished writing your first version of the prompt.You can click on the `Commit` button and write a commit message, which is helpful for you to track the changes you made to your prompt.

**Avoid “Commit + deploy”**: The `Commit + deploy` button will both commit your changes and immediately deploy them to production, making them live instantly. Only use this button if you understand that your changes will go live immediately and have tested them thoroughly.

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/prompt-commit.png)Congrats! You just created your first prompt on Keywords AI platform.

6

[Navigate to header](https://docs.keywordsai.co/get-started/quickstart/prompt_management#)

Deploy to production

Once you have committed your prompt, you can deploy it to production. Go to the `Deployments` tab and click on the `Deploy` button. You can choose the environment you want to deploy to.

**Immediate Live Effect**: Deploying a prompt will immediately reflect live in your production environment. All API calls using this prompt will start using the deployed version right away. Make sure you’ve tested your prompt thoroughly before deploying.

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/prompt/prompts-deploy.jpg)

* * *

### [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#4-find-your-prompt-id)  4\. Find your prompt ID

After creating your prompt, you’ll need its ID to use it in code. Find the Prompt ID in the Overview panel on the [Prompts page](https://platform.keywordsai.co/platform/prompts).

![Find Prompt ID](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/prompt/prompt-id.png)

* * *

### [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#5-use-your-prompt-in-code)  5\. Use your prompt in code

Now you can call your prompt from your application using the Keywords AI API.

- OpenAI Python SDK

- OpenAI TypeScript SDK

- Standard API


Copy

```
from openai import OpenAI

client = OpenAI(
    base_url="https://api.keywordsai.co/api/",
    api_key="YOUR_KEYWORDSAI_API_KEY",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",  # This will be overridden by prompt config
    messages=[{"role": "user", "content": "placeholder"}],  # This will be overridden
    extra_body={
        "prompt": {
            "prompt_id": "042f5f",  # Your prompt ID here
            "variables": {
                "task_description": "Square a number",
                "specific_library": "math"
            },
            "override": True  # Use prompt config instead of SDK parameters
        }
    }
)

print(response.choices[0].message.content)
```

Copy

```
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://api.keywordsai.co/api",
    apiKey: "YOUR_KEYWORDSAI_API_KEY",
});

const response = await client.chat.completions.create({
    messages: [{ role: "user", content: "placeholder" }],
    model: "gpt-4o-mini",
    // @ts-expect-error
    prompt: {
        prompt_id: "042f5f",  // Your prompt ID here
        variables: {
            task_description: "Square a number",
            specific_library: "math"
        },
        override: true
    }
});

console.log(response.choices[0].message.content);
```

Copy

```
import requests

def call_prompt(api_key="YOUR_KEYWORDSAI_API_KEY"):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        'prompt': {
            'prompt_id': '042f5f',  # Your prompt ID here
            'variables': {
                'task_description': 'Square a number',
                'specific_library': 'math'
            }
        }
    }

    response = requests.post(
        'https://api.keywordsai.co/api/chat/completions',
        headers=headers,
        json=data
    )
    return response.json()

result = call_prompt()
print(result['choices'][0]['message']['content'])
```

### [​](https://docs.keywordsai.co/get-started/quickstart/prompt_management\#6-monitor-your-prompts)  6\. Monitor your prompts

View your prompt usage and performance on the [Logs page](https://platform.keywordsai.co/platform/requests). You can:

- Filter logs by prompt name
- See response times and token usage
- Debug individual prompt executions
- Track prompt performance over time

![Monitor prompts](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/prompt/prompt-logs.png)

* * *

Was this page helpful?

YesNo

[Suggest edits](https://github.com/keywords-ai/keywords-ai-docs/edit/main/get-started/quickstart/prompt_management.mdx) [Raise issue](https://github.com/keywords-ai/keywords-ai-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/get-started/quickstart/prompt_management)

[Previous](https://docs.keywordsai.co/get-started/quickstart/gateway) [EvaluationsEvaluate and improve your LLM applications with automated testing and scoring\\
\\
Next](https://docs.keywordsai.co/get-started/quickstart/evaluation)

Ctrl+I

[linkedin](https://www.linkedin.com/company/keywordsai/) [github](https://github.com/keywordsai) [discord](https://discord.com/invite/KEanfAafQQ)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=keywordsai)

On this page

- [What is prompt management?](https://docs.keywordsai.co/get-started/quickstart/prompt_management#what-is-prompt-management)
- [Why use prompt management?](https://docs.keywordsai.co/get-started/quickstart/prompt_management#why-use-prompt-management)
- [Use prompt management](https://docs.keywordsai.co/get-started/quickstart/prompt_management#use-prompt-management)
- [1\. Get your Keywords AI API key](https://docs.keywordsai.co/get-started/quickstart/prompt_management#1-get-your-keywords-ai-api-key)
- [2\. Set up LLM provider API key](https://docs.keywordsai.co/get-started/quickstart/prompt_management#2-set-up-llm-provider-api-key)
- [3\. Create your first prompt](https://docs.keywordsai.co/get-started/quickstart/prompt_management#3-create-your-first-prompt)
- [4\. Find your prompt ID](https://docs.keywordsai.co/get-started/quickstart/prompt_management#4-find-your-prompt-id)
- [5\. Use your prompt in code](https://docs.keywordsai.co/get-started/quickstart/prompt_management#5-use-your-prompt-in-code)
- [6\. Monitor your prompts](https://docs.keywordsai.co/get-started/quickstart/prompt_management#6-monitor-your-prompts)

Assistant

Responses are generated using AI and may contain mistakes.

![Create API key placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/api-keys.png)

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/create-new-prompt.png)

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/configure-prompt.png)

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/write-prompt.png)

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/prompt-variables.png)

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/get-started/prompt-commit.png)

![Create prompt placeholder](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/prompt/prompts-deploy.jpg)

![Find Prompt ID](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/prompt/prompt-id.png)

![Monitor prompts](https://keywordsai-static.s3.us-east-1.amazonaws.com/docs/prompt/prompt-logs.png)