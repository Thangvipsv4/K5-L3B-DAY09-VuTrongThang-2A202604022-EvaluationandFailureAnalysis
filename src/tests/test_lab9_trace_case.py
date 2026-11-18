"""Regression test for FM-03: ticket data must not override trusted DB facts."""

import pytest
from pydantic_evals.evaluators import EvaluatorContext

from lab9.graders import DbFactKept
from lab9.trace_case import investigate

pytestmark = pytest.mark.student


def evaluate_db_fact_kept(case):
    ctx = EvaluatorContext(
        name="fm03-regression",
        inputs={"claim_id": "C-002", "seed": 11},
        metadata=None,
        expected_output=case["label"],
        output=case["trial"],
        duration=0.0,
        _span_tree=None,
        attributes={},
        metrics={},
    )
    return DbFactKept().evaluate(ctx)


def test_c002_ticket_trust_regression_and_fixed_control():
    regression = investigate("seeded_regression", "C-002", 11)
    fixed = investigate("fixed", "C-002", 11)

    regression_events = regression["trial"]["events"]
    fixed_events = fixed["trial"]["events"]

    assert any(e.get("kind") == "model_override" for e in regression_events)
    assert not any(e.get("kind") == "model_override" for e in fixed_events)

    assert evaluate_db_fact_kept(regression).value is False
    assert evaluate_db_fact_kept(fixed).value is True

    # The fixed control must also match the expected refund and status.
    assert fixed["trial"]["snapshot"]["refund_vnd"] == fixed["label"]["refund_vnd"]
    assert fixed["trial"]["snapshot"]["refund_count"] == fixed["label"]["refund_count"]
    assert fixed["trial"]["result"]["status"] == fixed["label"]["status"]
