# LangGraph Workflow Orchestration — Altair AI

Altair AI processes requests by compiling and executing a stateful Directed Acyclic Graph (DAG) using LangGraph.

---

## 💾 Graph State: `ChatState`

The state of the graph is shared between nodes using a typed dictionary:

```python
class ChatState(TypedDict):
    request_id: str
    trace_id: str
    correlation_id: str
    user_id: str
    session_id: str
    messages: list[dict]
    model_id: str
    routing_strategy: str
    prompt_name: Optional[str]
    prompt_variables: Optional[dict]
    output_schema: Optional[dict]
    temperature: Optional[float]
    max_tokens: Optional[int]
    
    # Execution states
    final_response: str
    structured_output: Optional[dict]
    usage: dict
    retry_count: int
    error: Optional[str]
    guardrail_violations: list[str]
    validation_errors: list[str]
    metadata: dict
```

---

## 📍 Graph Nodes and Edge Transitions

The state machine is configured inside `app/graph/workflow.py`:

```
[Start] -> input_validation -> prompt_render -> router -> llm_call -> output_validation
                                                            ^             │
                                                            │             ├─► (schema errors) ─► retry
                                                            │             │                        │
                                                            └─────────────┴──────── (retries ok) ──┘
                                                                          │
                                                                    (success)
                                                                          ▼
                                                                     persist
                                                                          ▼
                                                                   token_tracking
                                                                          ▼
                                                                   usage_analytics
                                                                          ▼
                                                                   experiment_logging
                                                                          ▼
                                                                   audit_logging
                                                                          ▼
                                                                   celery_trigger -> [End]
```

### Conditional Edge Rules:
1. **`_after_input`**: If `error` exists in state (e.g. guardrail block), route directly to `end_error`, skipping the LLM call.
2. **`_after_output`**: If JSON parsing fails and `retry_count < MAX_RETRIES`, route to `retry` to compile error messages and re-invoke the model. If retries are exhausted, set `error` and route to `end_error`.
