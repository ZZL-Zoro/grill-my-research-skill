# Contributing

Focus changes on observable research-thinking behavior. Describe the user input,
what the agent actually did and which decision was affected. Use fictionalized or
redistributable examples; remove private projects, personal information and data.

## Repository checks

```text
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

These commands validate repository plumbing only. For a behavior change, run the
relevant [evaluation scenarios](evals/README.md) in the target agent environment
when available and record the actual input/output, environment and revision.
If no model run was performed, state that instead of claiming behavioral PASS.

## Changes worth preserving

- Next questions should depend on actual answers, with one main question per turn.
- Both agreement and opposition must be evidence-weighted and bounded.
- Simulated answers, reports, assumptions and inspected evidence remain distinct.
- User goals, research type, stop requests and unresolved gaps stay visible.
- A coherent narrative must not silently become an empirical discovery.

Avoid rigid universal question lists or automatic quality scores. Add a rule when
it fixes a demonstrated failure and does not unnecessarily constrain other fields.
Keep core behavior in [SKILL.md](SKILL.md), detailed routes in references, and
user-facing templates in assets. Update documentation and evaluation cases when
behavior changes.

Contributions to this repository are distributed under its [MIT License](LICENSE).
