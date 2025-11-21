# Compliance Policies for MCPSecurity Gateway
package mcpsecurity.compliance

import rego.v1

# Default allow
default allow := false

# Allow if all compliance checks pass
allow if {
    count(deny) == 0
}

# Deny if PII detected and user doesn't have PII access
deny contains msg if {
    input.validation_result.violations[_].category == "pii"
    not input.user.permissions[_] == "pii_access"
    msg := "PII detected but user lacks pii_access permission"
}

# Deny internal IP access without permission
deny contains msg if {
    input.validation_result.violations[_].category == "internal_ip"
    not input.user.permissions[_] == "internal_network_access"
    msg := "Internal IP detected but user lacks internal_network_access permission"
}

# Require audit for sensitive actions
requires_audit if {
    input.user.department == "external"
}

requires_audit if {
    input.overall_risk_score > 50
}

# Data retention policy
requires_encryption if {
    input.validation_result.violations[_].category in ["secret", "pii"]
}

