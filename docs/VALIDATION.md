# Validation scope

Prepared locally on 2026-10-30. The core skill is instruction-only. Repository
validation does not require a model API and does not grade scientific reasoning.

## Structural checks

- Skill frontmatter, exact invocation name and UI metadata.
- Python/YAML syntax, local Markdown targets and required repository files.
- Evaluation-case schema and unique case IDs, not whether a model passes them.
- Public source-file scope, excluding private work directories and environments.
- The Codex skill-creator `quick_validate.py` can additionally validate `SKILL.md`.

## Six repository-tool regression tests

`python -m unittest discover -s tests -v` checks:

1. A clean ZIP contains every public source file, including hidden GitHub configuration, with matching bytes.
2. Local research, private, input/output, environment and cache directories are excluded.
3. A broken skill-reference link is detected and blocks packaging.
4. Unfinished entry-point instructions and an incorrect invocation name are detected.
5. An accidental environment file in public source scope blocks packaging.
6. An archive target containing a parent-directory segment is correctly normalized.

These are file/tool invariants. They do not simulate a scientist or score a
conversation by matching keywords.

## Behavioral evaluation remains separate

[../evals/cases.yaml](../evals/cases.yaml) defines 14 scenarios for adaptive
questioning, evidence status, false balance, causal overclaims, inconclusive
results, different research types, stop requests and circular confirmation.
They are prepared scenarios, **not completed model evaluation runs**. Follow the
[evaluation protocol](../evals/README.md) to record actual target-model behavior.
The examples are fictional illustrations, not empirical evidence of effectiveness.

## Environment and portability

Local structural validation and unit tests use Windows with Python 3.11.1 and
PyYAML 6.x. GitHub Actions additionally configures Windows/Linux with Python
3.11/3.12. Those remote jobs have not run merely because the workflow is present.

The skill does not promise current exhaustive literature knowledge, error-free
domain methods or persistent cross-chat memory. Source-specific scientific and
novelty claims still require actual evidence. A logical design can remain useful
while its outcome is unknown or its original hypothesis is contradicted.
