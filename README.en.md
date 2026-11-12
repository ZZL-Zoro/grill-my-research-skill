# Grill My Research

[中文](README.md) · [Skill](SKILL.md) · [Design](docs/DESIGN.md) · [Examples](examples/interactive-example.md) · [Evaluations](evals/README.md) · [Contributing](CONTRIBUTING.md)

A research-thinking skill that connects adaptive questions, evidence-weighted
feedback and project organization. Start with an unfinished idea or a full
proposal; arrive at a bounded research question, competing explanations,
discriminating evidence and decisions that change with the results.

## How it behaves

- Ask one main question at a time and use the actual answer to choose the next.
- Preserve the strongest part of a claim, examine relevant alternatives, then
  judge according to evidence rather than automatic agreement or opposition.
- Distinguish user reports, inspected materials/literature, working assumptions,
  AI inferences and unknowns. Never invent experiments or user answers.
- Repair an uncertain answer with a clearer formulation or an information route,
  rather than repeatedly asking the same question.
- Treat six main questions as a default checkpoint, not an endless interrogation.
  Summarize whenever the user asks.
- Separate a coherent design from an empirically supported conclusion.

Dialectical feedback does not require equal weight for every possible objection.
A well-supported bounded claim should be allowed to stand. This skill provides
behavioral guidance, not a guarantee that any model will reason correctly.

## Install

The core skill requires only its instruction and reference files. On GitHub,
select **Code → Download ZIP** and extract the archive. Rename the folder
containing `SKILL.md` to `grill-my-research-skill` and move it into `~/.agents/skills`.
On Windows, use `%USERPROFILE%\.agents\skills\grill-my-research-skill`.
Back up and reconcile an existing same-name version before copying. Restart the
session/app if the new skill is not visible. See the
[official skill documentation](https://learn.chatgpt.com/docs/build-skills).

Python 3.11+ and `requirements-dev.txt` are only for repository maintenance.
The skill does not automatically install itself or upload research material;
access by a cloud model follows the host product's behavior.

## Use

```text
Use $grill-my-research-skill to challenge my project. Ask one pivotal question at
a time, use my answer for the follow-up, and give evidence-weighted feedback.
Within six questions, summarize my research question, competing explanations,
discriminating design, outcome branches and next decision. My idea is: ...
```

For a one-shot review, request **a complete audit without waiting for an interview**.
For a defense rehearsal, explicitly request **simulated questions and answers**;
generated answers must be labeled as examples and their assumptions remain
unverified. Say “summarize now” whenever you want a stage result.

The agent follows the user's language. Examples are clearly marked fictional
conversations, not a record of real experiments or evaluated model runs.

## Outcome

The default deliverable is an inline research brief: refined question and scope,
current judgment, strongest competing explanation, evidence and gaps, minimal
discriminating action, an outcome–decision matrix, prioritized next steps and a
coherent project narrative. Save files only when useful or requested, using the
[brief](assets/research-brief.md), [decision matrix](assets/decision-matrix.md) and
[session snapshot](assets/session-state.yaml) templates. There is no automatic
cross-chat memory.

Status labels describe the argument, not a numerical quality score:

| State | Meaning |
|---|---|
| `OPEN` | A critical link or premise remains missing |
| `DESIGN_READY` | Question, evidence strategy, analysis, outcome decisions and necessary conditions align |
| `INCONCLUSIVE` | Existing results cannot distinguish key explanations adequately |
| `SUPPORTED_WITHIN_SCOPE` | Traceable evidence supports a bounded conclusion |
| `REFRAME` | The current question or route needs narrowing or restructuring |

The skill adapts to experimental, observational, computational, theoretical,
qualitative, exploratory and replication work. It does not impose one causal
experiment template on every field. Unsupported novelty, invented citations,
automatic sample sizes and publication probabilities are not acceptable outputs.

See [design notes](docs/DESIGN.md) and
[methodological background](references/methodological-notes.md) for boundaries.

## Validate and evaluate

```text
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
python scripts/package_skill.py --output dist/grill-my-research-skill.zip
```

Repository tests check metadata, links, file scope and packaging. They do not run
an LLM or grade science. The [14 behavioral scenarios](evals/cases.yaml) and
[evaluation protocol](evals/README.md) are prepared for actual target-model runs;
they are not already-passed behavioral tests. See [validation scope](docs/VALIDATION.md).

GitHub Actions runs the repository checks on Windows and Linux with Python 3.11
and 3.12. Open the **Actions** tab to see results for a specific commit. To
publish a separate copy, follow the [GitHub publishing guide](docs/GITHUB_UPLOAD.md).

## License and contributions

Repository code, templates and documentation use the [MIT License](LICENSE).
External sources retain their rights. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[CHANGELOG.md](CHANGELOG.md).
