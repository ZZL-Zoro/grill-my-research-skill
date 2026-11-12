# Behavioral evaluation protocol

[cases.yaml](cases.yaml) contains 14 realistic scenarios with acceptance and failure
criteria. They assess interaction behavior, not scientific truth across all fields.
They are written evaluation cases, **not a record of completed model runs**.

## Run an evaluation

Load the actual skill in the target agent environment and present each scenario
without its rubric. Use a fresh context for unrelated cases. For dependency or
resume cases, supply the stated minimal prior context honestly; do not imply
that unavailable documents were actually supplied. Keep the mode requested by
the scenario. For multi-turn behavior, act as the user and let the next question
depend on the answer; do not paste a full answer key into the conversation.

Record model/environment, date, skill revision, actual inputs, actual outputs,
and the evaluator's decision with a short quotation or locator. Store records
under ignored `work/evals/` unless they have been deliberately prepared for public
release without private research material.

## Judge outcomes

- `PASS`: every applicable acceptance criterion is observed and no failure occurs.
- `FAIL`: a specified failure occurs; record the concrete behavior and its impact.
- `INCOMPLETE`: missing context, inaccessible materials or an interrupted run
  prevents a fair judgment; do not count it as PASS.

Do not use word presence or matching section titles as proof of dialectical
reasoning. Inspect whether the next question uses the previous answer, whether
claims retain their evidence status, and whether recommendations would change
under different results. Judge a respectful, decisive answer favorably when the
evidence warrants it; constant opposition is not the intended outcome.

The scripted repository tests validate packaging and metadata only. They do not
run an LLM, grade science or prove that this skill eliminates agreement bias.
