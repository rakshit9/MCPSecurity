# RBAC Policies for MCPSecurity Gateway
package mcpsecurity.rbac

import rego.v1

# Default deny
default allow := false

# Admin role can do everything
allow if {
    input.user.role == "admin"
}

# Developer role permissions
allow if {
    input.user.role == "developer"
    input.action in ["code_generation", "code_review", "read"]
}

# Viewer role permissions
allow if {
    input.user.role == "viewer"
    input.action == "read"
}

# Deny dangerous actions for non-admins
deny contains msg if {
    input.user.role != "admin"
    input.action in ["delete", "modify_policies", "admin_access"]
    msg := sprintf("User '%s' with role '%s' is not authorized for action '%s'", [input.user.id, input.user.role, input.action])
}

# Deny if user is suspended
deny contains msg if {
    input.user.status == "suspended"
    msg := sprintf("User '%s' is suspended", [input.user.id])
}

