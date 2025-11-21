# Security Policies for MCPSecurity Gateway
package mcpsecurity.security

import rego.v1

# Default allow for security checks
default allow := false

# Allow if no high-risk violations
allow if {
    count(deny) == 0
}

# Deny if request contains secrets
deny contains msg if {
    input.validation_result.violations[_].severity == "CRITICAL"
    msg := "Request contains critical security violations (secrets detected)"
}

# Deny if attack detected
deny contains msg if {
    input.attack_result.is_attack == true
    msg := sprintf("Attack detected: %v", [input.attack_result.attack_types])
}

# Deny if risk score is too high
deny contains msg if {
    input.overall_risk_score >= 80
    msg := sprintf("Risk score too high: %d (threshold: 80)", [input.overall_risk_score])
}

# Warn if medium risk
warn contains msg if {
    input.overall_risk_score >= 40
    input.overall_risk_score < 80
    msg := "Medium risk detected - review recommended"
}

# Block network access for certain users
deny contains msg if {
    input.user.restrictions[_] == "no_network_code"
    contains(lower(input.text), "import requests")
    msg := "User is restricted from generating network-related code"
}

deny contains msg if {
    input.user.restrictions[_] == "no_network_code"
    contains(lower(input.text), "import socket")
    msg := "User is restricted from generating network-related code"
}

# Block file system access for certain users
deny contains msg if {
    input.user.restrictions[_] == "no_file_system"
    contains(lower(input.text), "open(")
    msg := "User is restricted from generating file system code"
}

