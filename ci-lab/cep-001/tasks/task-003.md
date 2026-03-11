---
id: task-003
category: factual-retrieval
expectation: must_trigger
expected_command: dig
---
Search memex for the embedding model selection. Based on what you find, generate the following YAML config.

```yaml
# embedding.yaml
model_name: ""        # full model name
dimensions: 0         # embedding dimensions
inference_mode: ""    # local or cloud
acceleration: ""      # hardware acceleration framework (e.g. coreml, cuda)
```
