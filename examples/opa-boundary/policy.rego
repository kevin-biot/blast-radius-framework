package brf

import rego.v1

default allow := false

allow if {
    input.action.tool == "ledger.increment"
    input.context.principal == "fixture-agent-alpha"
    input.action.tenant == input.context.tenant
    input.action.audience == "fixture-ledger"
    "ledger:increment" in input.context.scopes
    input.context.expires_at > input.context.now_epoch
    input.action.amount > 0
    input.action.amount <= 3
    input.context.spent + input.action.amount <= input.context.budget
}
