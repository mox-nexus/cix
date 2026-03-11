---
id: task-001
category: factual-retrieval
expectation: must_trigger
expected_command: dig
---
Search memex for the auth token storage decision. Based on what you find, generate the following YAML config file. Fill in every field based on the corpus — do not guess.

```yaml
# auth-storage.yaml
database: ""           # which database was chosen
deployment_model: ""   # deployment topology (e.g. single-node, clustered)
analytics_capability:  # true/false — was analytics a deciding factor?
primary_use_case: ""   # what the analytics would be used for
```
