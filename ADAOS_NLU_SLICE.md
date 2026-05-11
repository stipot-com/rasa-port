# AdaOS Rasa NLU Slice

This repository intentionally keeps a trimmed Rasa 3.6.x source subset for AdaOS
NLU porting work.

The slice is no longer treated as a temporary folder next to `rasa-backup`. It is
now the controlled source tree for the AdaOS Rasa NLU port. Deleted or omitted
upstream files should only be restored when they are needed by the contract in
`PORTING_CONTRACT.md`.

## Kept Runtime Areas

- `rasa/nlu`: tokenizers, featurizers, classifiers, extractors, selectors.
- `rasa/engine`: graph training/loading/runtime infrastructure.
- `rasa/graph_components`: graph providers/converters/validators used by recipes.
- `rasa/shared`: shared NLU data structures, importers, schemas, and minimal Core
  structures referenced by the graph.
- `rasa/utils/tensorflow`: TensorFlow helper layers and training utilities used by
  DIET-style components.
- A minimal `rasa.__main__` and `rasa.cli.train` path for `rasa train nlu`.
- A small Core compatibility shell that Rasa 3.6 still imports while
  loading/parsing graph models.

## Intentionally Excluded

- Upstream docs, examples, deployment assets, release tooling, and CI files.
- Full server/channel/broker surfaces not needed by AdaOS embedded NLU.
- Non-NLU CLI commands such as `run`, `shell`, `interactive`, `x`, `export`,
  `evaluate`, and related argument modules.
- Product integrations that would force optional dependencies into the NLU port.

## Rule Of Thumb

Keep code only if it is required to train, load, or parse through the NLU
contract. Everything else is either a temporary shim or a candidate for removal
once the Phase 2 tests prove it is not needed.
