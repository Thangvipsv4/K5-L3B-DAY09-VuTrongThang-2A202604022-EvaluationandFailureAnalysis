# Trace Case — FM-03: Ticket Trust

## Trial
- Regression trial: `seeded_regression`, claim `C-002`, seed `11`
- Control trial: `fixed`, claim `C-002`, seed `11`
- Run ID: Not emitted by the trace command.

## Symptom
The seeded regression fails the Lab8 grader:
`status resolved != denied`.

The resulting refund is 20,000 VND, while the expected label is:
- `refund_vnd`: 0
- `refund_count`: 0
- `status`: denied

The fixed control passes the Lab8 grader and matches all three expected values.

## First wrong step
- Event: Step 3
- Kind: `model_override`
- Payload: `{"delay_days": 5}`

This event appears in `seeded_regression` but not in `fixed`.
After the override, the seeded trial produces a 20,000 VND quote and records a refund. The fixed trial produces a 0 VND quote with reason `no_entitlement`.

## Why this is the first wrong step
Steps 1 and 2 complete the handoff and investigator lookup. The first visible divergence is the `model_override` event at step 3. Subsequent quote, reply, and ledger values differ from the expected label.

## Failure mode
- ID: `FM-03`
- Name: Ticket Trust
- A model-provided or ticket-derived value overrides the trusted order facts used to determine policy eligibility.

## Fixed control
For `fixed C-002@11`:
- No `model_override` event.
- Quote: 0 VND, reason `no_entitlement`.
- Ledger refund: 0 VND.
- Ledger refund count: 0.
- Result status: `denied`.
- Lab8 grader: PASS.

## Regression test
Implemented in `tests/test_lab9_trace_case.py`:

- Test: `test_c002_ticket_trust_regression_and_fixed_control`
- Runs both `seeded_regression` and `fixed` through `investigate()`.
- Asserts that the regression trace contains `model_override` and the fixed trace does not.
- Asserts that `DbFactKept` fails for the regression and passes for the fixed control.
- Asserts that the fixed control's refund amount, refund count, and status match the expected label.
- Verification: `python -m pytest .\tests\test_lab9_trace_case.py -q -o addopts=""` — 1 passed.

## Unknowns
The trace establishes the first visible divergence and its downstream effects. It does not, by itself, establish the internal implementation reason why the override was accepted.
