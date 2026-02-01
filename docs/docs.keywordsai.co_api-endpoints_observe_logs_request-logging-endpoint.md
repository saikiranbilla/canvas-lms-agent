---
url: "https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint"
title: "Create log - Docs"
---

[Skip to main content](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#content-area)

[Docs home page![light logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/light.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=7a97b614ddd4af346e9de4ba118e1fd7)![dark logo](https://mintcdn.com/keywordsai/1fjj1P2W0uxV0htN/logo/dark.svg?fit=max&auto=format&n=1fjj1P2W0uxV0htN&q=85&s=b4d210c0b5c294be66b448eab084f3e5)](https://www.keywordsai.co/)

Search...

Ctrl K

##### Observe

- Logs

  - [POST\\
    \\
    Create log](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint)
  - [POST\\
    \\
    List logs](https://docs.keywordsai.co/api-endpoints/observe/logs/logs-list-endpoint)
  - [POST\\
    \\
    Get logs summary](https://docs.keywordsai.co/api-endpoints/observe/logs/logs-summary-endpoint)
  - [GET\\
    \\
    Retrieve log](https://docs.keywordsai.co/api-endpoints/observe/logs/get-log-endpoint)
  - [PATCH\\
    \\
    Update single log](https://docs.keywordsai.co/api-endpoints/observe/logs/update-single-log-endpoint)
  - [PATCH\\
    \\
    Update log](https://docs.keywordsai.co/api-endpoints/observe/logs/logs-update-endpoint)
  - [DEL\\
    \\
    Delete log](https://docs.keywordsai.co/api-endpoints/observe/logs/delete-log-endpoint)
  - [POST\\
    \\
    Ingest Logs from traces](https://docs.keywordsai.co/api-endpoints/observe/logs/ingest)
- Traces

- Threads

- Users


##### Develop

- Gateway

- OpenAI Batch

- Multimodal

- Prompts

- Testsets

- Experiments


##### Evals

- Evaluators

- Datasets

- Scores

- Log Scores


##### Manage

- Models

- Temporary API Keys


##### Automation

- Conditions

- Automations


##### Reference

- [Filters API Reference](https://docs.keywordsai.co/api-endpoints/reference/filters_api_reference)

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

Logs

Create log

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

[Documentation](https://docs.keywordsai.co/get-started/overview) [Integrations](https://docs.keywordsai.co/integration/overview) [API reference](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint) [SDKs](https://docs.keywordsai.co/tracing-sdk/quickstart) [Changelog](https://docs.keywordsai.co/changelog)

Logs

# Create log

Copy page

Copy page

POST

https://api.keywordsai.co

/

api

/

request-logs

Try it

Create log

cURL

Copy

```
curl --request POST \
  --url https://api.keywordsai.co/api/request-logs/ \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "input": {},
  "output": {},
  "log_type": "<string>",
  "model": "<string>",
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 123,
    "total_tokens": 123,
    "prompt_tokens_details": {},
    "cache_creation_prompt_tokens": 123
  },
  "cost": 123,
  "latency": 123,
  "time_to_first_token": 123,
  "tokens_per_second": 123,
  "metadata": {},
  "customer_identifier": "<string>",
  "customer_params": {
    "customer_identifier": "<string>",
    "name": "<string>",
    "email": "<string>"
  },
  "thread_identifier": "<string>",
  "custom_identifier": "<string>",
  "group_identifier": "<string>",
  "trace_unique_id": "<string>",
  "span_workflow_name": "<string>",
  "span_name": "<string>",
  "span_parent_id": "<string>",
  "tools": [\
    {\
      "type": "<string>",\
      "function": {\
        "name": "<string>",\
        "description": "<string>",\
        "parameters": {}\
      }\
    }\
  ],
  "tool_choice": {},
  "response_format": {},
  "temperature": 123,
  "top_p": 123,
  "frequency_penalty": 123,
  "presence_penalty": 123,
  "max_tokens": 123,
  "stop": {},
  "status_code": 123,
  "error_message": "<string>",
  "warnings": {},
  "status": "<string>",
  "stream": true,
  "prompt_id": "<string>",
  "prompt_name": "<string>",
  "is_custom_prompt": true,
  "timestamp": "<string>",
  "start_time": "<string>",
  "full_request": {},
  "full_response": {},
  "prompt_unit_price": 123,
  "completion_unit_price": 123,
  "keywordsai_api_controls": {
    "block": true
  },
  "positive_feedback": true
}
'
```

This guide shows you how to log any type of LLM request to Keywords AI using the **universal input/output design** that supports all span types.

**Log size limit: 20MB**Each log payload has a maximum size limit of 20MB. This includes the `input`, `output`, and all other fields combined. Logs exceeding this limit will be rejected.

## [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#input/output)  Input/Output

**Keywords AI uses universal `input` and `output` fields across all span types.**

- **Chat completions**: Messages arrays
- **Embeddings**: Text strings or arrays
- **Transcriptions**: Audio metadata → text
- **Speech**: Text → audio
- **Workflows/Tasks**: Any custom data structure
- **Agent operations**: Complex nested objects

**How it works:**

1. You provide `input` and `output` fields in any structure (string, object, array, etc.)
2. Set `log_type` to indicate span type (`"chat"`, `"embedding"`, `"workflow"`, etc.)
3. Keywords AI automatically extracts type-specific fields for backward compatibility
4. Your data is stored efficiently and retrieved with both universal and type-specific fields

For complete `log_type` specifications, see [log types](https://docs.keywordsai.co/get-started/observability_data_model#log-types).

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#legacy-field-support)  Legacy field support

For backward compatibility, Keywords AI still supports legacy fields:

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-prompt-messages)

prompt\_messages

array

**Legacy field.** Use `input` instead.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-completion-message)

completion\_message

object

**Legacy field.** Use `output` instead.

## [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#request-body)  Request body

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#core-fields)  Core fields

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-input)

input

string \| object \| array

Universal input field for the span. Structure depends on `log_type`:

- **Chat**: JSON string of messages array or messages array directly
- **Embedding**: Text string or array of strings
- **Workflow/Task**: Any JSON-serializable structure
- **Transcription**: Audio file reference or metadata object
- **Speech**: Text string or TTS configuration object

See the **Span Types** section below for complete specifications.

Example for Chat

Copy

```
"input": "[{\"role\":\"system\",\"content\":\"You are helpful.\"},{\"role\":\"user\",\"content\":\"Hello\"}]"
```

Example for Embedding

Copy

```
"input": "Keywords AI is an LLM observability platform"
```

Example for Workflow

Copy

```
"input": "{\"query\":\"Help with order #12345\",\"context\":{\"user_id\":\"123\"}}"
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-output)

output

string \| object \| array

Universal output field for the span. Structure depends on `log_type`:

- **Chat**: JSON string of completion message or message object directly
- **Embedding**: Array of vector embeddings
- **Workflow/Task**: Any JSON-serializable result structure
- **Transcription**: Transcribed text string
- **Speech**: Audio file reference or base64 audio data

Example for Chat

Copy

```
"output": "{\"role\":\"assistant\",\"content\":\"Hello! How can I help you?\"}"
```

Example for Embedding

Copy

```
"output": "[0.123, -0.456, 0.789, ...]"
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-log-type)

log\_type

string

default:"chat"

Type of span being logged. Determines how `input` and `output` are parsed.**Supported types:**

- `"chat"` \- Chat completion requests (default)
- `"completion"` \- Legacy completion requests
- `"response"` \- OpenAI Response API
- `"embedding"` \- Embedding generation
- `"transcription"` \- Speech-to-text
- `"speech"` \- Text-to-speech
- `"workflow"` or `"agent"` \- Workflow/agent execution
- `"task"` or `"tool"` \- Task/tool execution
- `"function"` \- Function call
- `"generation"` \- Generation span
- `"handoff"` \- Agent handoff
- `"guardrail"` \- Safety check
- `"custom"` \- Custom span type

Default Behavior

If not specified, defaults to `"chat"`. For chat types, the system automatically extracts `prompt_messages` and `completion_message` from `input` and `output` for backward compatibility.For complete specifications of each type, see [log types](https://docs.keywordsai.co/get-started/observability_data_model#log-types).

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-model)

model

string

The model used for the inference. Optional but recommended for chat/completion/embedding types.

Example

Copy

```
"model": "gpt-4o-mini"
```

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#telemetry)  Telemetry

Performance metrics and cost tracking for monitoring LLM efficiency.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-usage)

usage

object

Token usage information for the request.

Properties

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-prompt-tokens)

prompt\_tokens

integer

Number of tokens in the prompt/input.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-completion-tokens)

completion\_tokens

integer

Number of tokens in the completion/output.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-total-tokens)

total\_tokens

integer

Total tokens (prompt + completion).

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-prompt-tokens-details)

prompt\_tokens\_details

object

Detailed breakdown of prompt tokens (e.g., cached tokens).

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-cache-creation-prompt-tokens)

cache\_creation\_prompt\_tokens

integer

For Anthropic models: tokens used to create the cache.

Example

Copy

```
{
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 85,
    "total_tokens": 235,
    "prompt_tokens_details": {
      "cached_tokens": 10
    }
  }
}
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-cost)

cost

float

Cost of the inference in US dollars. If not provided, will be calculated automatically based on model pricing.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-latency)

latency

float

Total request latency in seconds (replaces deprecated `generation_time`).

Previously called `generation_time`. For backward compatibility, both field names are supported.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-time-to-first-token)

time\_to\_first\_token

float

Time to first token (TTFT) in seconds. Useful for streaming responses and voice AI applications.

Previously called `ttft`. Both field names are supported.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-tokens-per-second)

tokens\_per\_second

float

Generation speed in tokens per second.

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#metadata)  Metadata

Custom tracking and identification parameters for advanced analytics and filtering.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-metadata)

metadata

object

You can add any key-value pair to this metadata field for your reference. Useful for custom analytics and filtering.

Example

Copy

```
{
  "metadata": {
    "language": "en",
    "environment": "production",
    "version": "v1.0.0",
    "feature": "chat_support",
    "user_tier": "premium"
  }
}
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-customer-identifier)

customer\_identifier

string

An identifier for the customer that invoked this request. Helps with visualizing user activities. See [customer identifier details](https://docs.keywordsai.co/documentation/products/users/customer-identifier).

Example

Copy

```
"customer_identifier": "user_123"
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-customer-params)

customer\_params

object

Extended customer information (alternative to individual customer fields).

Properties

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-customer-identifier-1)

customer\_identifier

string

Customer identifier.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-name)

name

string

Customer name.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-email)

email

string

Customer email.

Example

Copy

```
{
  "customer_params": {
    "customer_identifier": "customer_123",
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
}
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-thread-identifier)

thread\_identifier

string

A unique identifier for the conversation thread. Useful for multi-turn conversations.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-custom-identifier)

custom\_identifier

string

Same functionality as `metadata`, but indexed for faster querying.

Example

Copy

```
"custom_identifier": "ticket_12345"
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-group-identifier)

group\_identifier

string

Group identifier. Use to group related logs together.

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#workflow-&-tracing)  Workflow & tracing

Parameters for distributed tracing and workflow tracking.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-trace-unique-id)

trace\_unique\_id

string

Unique identifier for the trace. Used to link multiple spans together in distributed tracing.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-span-workflow-name)

span\_workflow\_name

string

Name of the workflow this span belongs to.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-span-name)

span\_name

string

Name of this specific span/task within the workflow.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-span-parent-id)

span\_parent\_id

string

ID of the parent span. Used to build the trace hierarchy.

## [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#advanced-parameters)  Advanced parameters

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#tool-calls-and-function-calling)  Tool calls and function calling

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-tools)

tools

array

A list of tools the model may call. Currently, only functions are supported as a tool.

Properties

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-type)

type

string

required

The type of the tool. Currently, only `function` is supported.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-function)

function

object

required

Properties

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-name-1)

name

string

required

The name of the function.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-description)

description

string

A description of what the function does.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-parameters)

parameters

object

The parameters the function accepts.

Example

Copy

```
"tools": [\
    {\
        "type": "function",\
        "function": {\
            "name": "get_current_weather",\
            "description": "Get the current weather in a given location",\
            "parameters": {\
                "type": "object",\
                "properties": {\
                    "location": {\
                        "type": "string",\
                        "description": "The city and state, e.g. San Francisco, CA"\
                    },\
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}\
                },\
                "required": ["location"]\
            }\
        }\
    }\
]
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-tool-choice)

tool\_choice

string \| object

Controls which (if any) tool is called by the model. Can be `"none"`, `"auto"`, or an object specifying a specific tool.

Example

Copy

```
"tool_choice": {
    "type": "function",
    "function": {
        "name": "get_current_weather"
    }
}
```

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#response-configuration)  Response configuration

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-response-format)

response\_format

object

Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs.

Possible types

- **Text**: `{ "type": "text" }` \- Default response format
- **JSON Schema**: `{ "type": "json_schema", "json_schema": {...} }` \- Structured outputs
- **JSON Object**: `{ "type": "json_object" }` \- Legacy JSON format

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#model-configuration)  Model configuration

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-temperature)

temperature

number

default:1

Controls randomness in the output (0-2). Higher values produce more random responses.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-top-p)

top\_p

number

default:1

Nucleus sampling parameter. Alternative to temperature.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-frequency-penalty)

frequency\_penalty

number

Penalizes tokens based on their frequency in the text so far.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-presence-penalty)

presence\_penalty

number

Penalizes tokens based on whether they appear in the text so far.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-max-tokens)

max\_tokens

integer

Maximum number of tokens to generate.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-stop)

stop

array\[string\]

Stop sequences where generation will stop.

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#error-handling-and-status)  Error handling and status

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-status-code)

status\_code

integer

default:200

The HTTP status code for the request. Default is 200 (success).

Supported status codes

All valid HTTP status codes are supported: `200`, `201`, `400`, `401`, `403`, `404`, `429`, `500`, `502`, `503`, `504`, etc.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-error-message)

error\_message

string

Error message if the request failed. Default is empty string.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-warnings)

warnings

string \| object

Any warnings that occurred during the request.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-status)

status

string

Request status. Common values: `"success"`, `"error"`.

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#additional-configuration)  Additional configuration

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-stream)

stream

boolean

default:false

Whether the response was streamed.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-prompt-id)

prompt\_id

string

ID of the prompt template used. See [Prompts documentation](https://docs.keywordsai.co/documentation/products/prompt_management/creating_prompts/create_prompt).

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-prompt-name)

prompt\_name

string

Name of the prompt template.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-is-custom-prompt)

is\_custom\_prompt

boolean

default:false

Whether the prompt is a custom prompt. Set to `true` if using custom `prompt_id`.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-timestamp)

timestamp

string

ISO 8601 timestamp when the request completed.

Example

Copy

```
"timestamp": "2025-01-01T10:30:00Z"
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-start-time)

start\_time

string

ISO 8601 timestamp when the request started.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-full-request)

full\_request

object

The full request object. Useful for logging additional configuration parameters.

Tool calls and other nested objects will be automatically extracted from `full_request`.

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-full-response)

full\_response

object

The full response object from the model provider.

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#pricing-configuration)  Pricing configuration

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-prompt-unit-price)

prompt\_unit\_price

number

Custom price per 1M prompt tokens. Used for self-hosted or fine-tuned models.

Example

Copy

```
"prompt_unit_price": 0.0042  // $0.0042 per 1M tokens
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-completion-unit-price)

completion\_unit\_price

number

Custom price per 1M completion tokens. Used for self-hosted or fine-tuned models.

Example

Copy

```
"completion_unit_price": 0.0042  // $0.0042 per 1M tokens
```

### [​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint\#api-controls)  API controls

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-keywordsai-api-controls)

keywordsai\_api\_controls

object

Control the behavior of the Keywords AI logging API.

Properties

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-block)

block

boolean

default:true

If `false`, the server immediately returns initialization status without waiting for log completion.

Example

Copy

```
{
  "keywordsai_api_controls": {
    "block": true
  }
}
```

[​](https://docs.keywordsai.co/api-endpoints/observe/logs/request-logging-endpoint#param-positive-feedback)

positive\_feedback

boolean

Whether the user liked the output. `true` means positive feedback.

Was this page helpful?

YesNo

[Suggest edits](https://github.com/keywords-ai/keywords-ai-docs/edit/main/api-endpoints/observe/logs/request-logging-endpoint.mdx) [Raise issue](https://github.com/keywords-ai/keywords-ai-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/api-endpoints/observe/logs/request-logging-endpoint)

[List logs\\
\\
Next](https://docs.keywordsai.co/api-endpoints/observe/logs/logs-list-endpoint)

Ctrl+I

[linkedin](https://www.linkedin.com/company/keywordsai/) [github](https://github.com/keywordsai) [discord](https://discord.com/invite/KEanfAafQQ)

[Powered by](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=keywordsai)

Create log

cURL

Copy

```
curl --request POST \
  --url https://api.keywordsai.co/api/request-logs/ \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "input": {},
  "output": {},
  "log_type": "<string>",
  "model": "<string>",
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 123,
    "total_tokens": 123,
    "prompt_tokens_details": {},
    "cache_creation_prompt_tokens": 123
  },
  "cost": 123,
  "latency": 123,
  "time_to_first_token": 123,
  "tokens_per_second": 123,
  "metadata": {},
  "customer_identifier": "<string>",
  "customer_params": {
    "customer_identifier": "<string>",
    "name": "<string>",
    "email": "<string>"
  },
  "thread_identifier": "<string>",
  "custom_identifier": "<string>",
  "group_identifier": "<string>",
  "trace_unique_id": "<string>",
  "span_workflow_name": "<string>",
  "span_name": "<string>",
  "span_parent_id": "<string>",
  "tools": [\
    {\
      "type": "<string>",\
      "function": {\
        "name": "<string>",\
        "description": "<string>",\
        "parameters": {}\
      }\
    }\
  ],
  "tool_choice": {},
  "response_format": {},
  "temperature": 123,
  "top_p": 123,
  "frequency_penalty": 123,
  "presence_penalty": 123,
  "max_tokens": 123,
  "stop": {},
  "status_code": 123,
  "error_message": "<string>",
  "warnings": {},
  "status": "<string>",
  "stream": true,
  "prompt_id": "<string>",
  "prompt_name": "<string>",
  "is_custom_prompt": true,
  "timestamp": "<string>",
  "start_time": "<string>",
  "full_request": {},
  "full_response": {},
  "prompt_unit_price": 123,
  "completion_unit_price": 123,
  "keywordsai_api_controls": {
    "block": true
  },
  "positive_feedback": true
}
'
```

Assistant

Responses are generated using AI and may contain mistakes.