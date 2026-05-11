# AdaOS Rasa NLU Port

This repository contains an AdaOS-controlled port of the Rasa 3.6.x NLU runtime
and training stack.

The goal is not to keep a full Rasa distribution alive. The goal is to preserve
the NLU parts AdaOS can reuse safely on Python 3.11.9: data loading, component
graphs, tokenizers, featurizers, classifiers, entity extractors, model training,
model loading, and parsing.

## Current State

- Source base: Rasa Open Source 3.6.x / 3.6.21.
- License: Apache-2.0. Keep `LICENSE.txt` and `NOTICE` with redistributed code.
- Runtime target: Python 3.11.9, Windows first, Linux later.
- Package state: not yet installable as a clean AdaOS package.
- Dependency state: still upstream-shaped and must be reduced in the next phase.
- Test state: contract tests are planned before deeper refactoring starts.

## What Stays

- NLU training and inference primitives.
- Rasa graph engine pieces needed by NLU recipes.
- Shared data structures, importers, schemas, and utilities used by NLU.
- TensorFlow helper code required by DIET-style components.
- A minimal compatibility CLI for `python -m rasa train nlu`.
- A small Core compatibility shell only where NLU loading/parsing still imports it.

## What Does Not Stay

- Full Rasa server/runtime.
- Dialogue management as a product surface.
- Production channels and connectors.
- Event brokers, action server, Rasa SDK coupling, Rasa X, telemetry product flows.
- Upstream CI, release tooling, docs site, examples, and training projects.

## Porting Contract

The contract for this port is defined in `PORTING_CONTRACT.md`.

In short, AdaOS should be able to train a tiny NLU model, load that model, parse a
message, and receive stable intent/entity output without pulling the full Rasa
application surface back in.

## Roadmap

1. Define the porting contract and scope boundaries.
2. Build a Python 3.11.9 dependency baseline plus external contract tests.
3. Refactor toward a small AdaOS-facing NLU API while keeping tests green.
4. Remove unused upstream surfaces only when tests prove the NLU path still works.
5. Integrate the resulting package into AdaOS as a controlled dependency.

