# AdaOS Rasa NLU Porting Contract

This document is the control point for the port. If a change does not help this
contract, it is probably out of scope for the AdaOS Rasa NLU port.

## Objective

Provide a maintained, minimal, Python 3.11.9-compatible NLU toolkit derived from
Rasa 3.6.x that AdaOS can embed without carrying the full Rasa server and Core
product surface.

## Public Capability Contract

The port must support these capabilities:

- Train an NLU-only model from a small Rasa-style project directory.
- Load a trained NLU model artifact from disk.
- Parse a single text message and return intent, confidence, entities, and
  component metadata in a stable structure.
- Expose a narrow AdaOS adapter that can be tested without starting a Rasa server.
- Keep a compatibility path for `python -m rasa train nlu` during the transition.

The final AdaOS-facing API should be small and explicit. A likely shape is:

```python
from pathlib import Path

from adaos_rasa_nlu import load_model, train_nlu

result = train_nlu(project_dir=Path("bot"), output_dir=Path("models"))
runtime = load_model(result.model_path)
parsed = runtime.parse("hello")
```

The exact module name can change during packaging, but the contract should stay
close to this shape.

## In Scope

- NLU data import and validation required for training.
- NLU pipeline graph construction and execution.
- Tokenizers, featurizers, classifiers, entity extractors, response selectors.
- DIET-classifier path and its TensorFlow helper code.
- Model archive creation, loading, and metadata required for inference.
- Minimal compatibility shims for upstream imports used by the NLU path.

## Out Of Scope

- Full Rasa HTTP server.
- Production channels: Slack, Telegram, Twilio, Webex, Facebook, and similar.
- Event brokers and external tracker stores.
- Dialogue policies as an AdaOS product surface.
- Action server and mandatory `rasa-sdk` dependency.
- Rasa X, enterprise/cloud flows, telemetry product behavior.
- Upstream documentation site, CI, release automation, and example projects.

If an out-of-scope module is still present, it is only a temporary compatibility
shim until tests prove it can be removed or replaced.

## Python 3.11.9 Baseline

The port must run on Python 3.11.9. Dependency work should prefer explicit,
boring pins over resolver guesswork. Known areas that need attention:

- TensorFlow must use a Python 3.11-capable version.
- Numeric stack pins must be explicit: NumPy, SciPy, scikit-learn, and related
  libraries should not float to incompatible modern releases.
- Optional UI, plotting, channel, broker, and server dependencies should not be
  installed for the NLU-only package.
- Windows support is first-class because AdaOS development currently happens on
  Windows.

## External Test Control Loop

Phase 2 must add tests before deeper refactoring. These tests are the guardrails
for Phase 3.

Minimum control tests:

- Import smoke test for the AdaOS NLU package on Python 3.11.9.
- Dependency resolution/install test in a clean environment.
- Tiny fixture training test using an NLU-only project.
- Model loading test against the trained fixture artifact.
- Parse contract test for intent confidence and entity output shape.
- Negative test proving server/channel/broker dependencies are not required.
- Compatibility test for `python -m rasa train nlu` while the CLI shim exists.

The tests should be runnable without the old backup tree and without full Rasa
server dependencies.

## Acceptance Criteria For The First Usable Port

- A clean Python 3.11.9 environment can install the NLU port.
- A tiny AdaOS fixture can train an NLU model successfully.
- The trained model can be loaded and used to parse text.
- No default AdaOS NLU path imports removed server, channel, broker, or Rasa SDK
  modules.
- The result is documented enough that we can decide what to delete next without
  guessing.

