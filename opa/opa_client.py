import httpx
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class PolicyDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"


class PolicyResult:
    def __init__(self):
        self.decision: PolicyDecision = PolicyDecision.DENY
        self.allowed: bool = False
        self.denied_reasons: List[str] = []
        self.warnings: List[str] = []
        self.requires_audit: bool = False
        self.requires_encryption: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "decision": self.decision.value,
            "allowed": self.allowed,
            "denied_reasons": self.denied_reasons,
            "warnings": self.warnings,
            "requires_audit": self.requires_audit,
            "requires_encryption": self.requires_encryption
        }


class OPAClient:
    def __init__(self, opa_url: str = "http://localhost:8181", use_mock: bool = True):
        self.opa_url = opa_url
        self.use_mock = use_mock
        self.client = httpx.Client(timeout=5.0)
    
    async def evaluate_policy(self, policy_package: str, input_data: Dict) -> PolicyResult:
        """Evaluate policy using OPA or mock"""
        if self.use_mock:
            return self._mock_evaluate(policy_package, input_data)
        
        try:
            return await self._opa_evaluate(policy_package, input_data)
        except Exception as e:
            print(f"OPA evaluation failed, using mock: {e}")
            return self._mock_evaluate(policy_package, input_data)
    
    async def _opa_evaluate(self, policy_package: str, input_data: Dict) -> PolicyResult:
        """Evaluate using actual OPA server"""
        url = f"{self.opa_url}/v1/data/{policy_package}"
        
        response = self.client.post(
            url,
            json={"input": input_data}
        )
        response.raise_for_status()
        
        opa_result = response.json()
        return self._parse_opa_response(opa_result)
    
    def _parse_opa_response(self, opa_result: Dict) -> PolicyResult:
        """Parse OPA response into PolicyResult"""
        result = PolicyResult()
        
        data = opa_result.get("result", {})
        
        result.allowed = data.get("allow", False)
        result.denied_reasons = list(data.get("deny", []))
        result.warnings = list(data.get("warn", []))
        result.requires_audit = data.get("requires_audit", False)
        result.requires_encryption = data.get("requires_encryption", False)
        
        if result.allowed and len(result.denied_reasons) == 0:
            result.decision = PolicyDecision.ALLOW
        elif len(result.warnings) > 0:
            result.decision = PolicyDecision.WARN
        else:
            result.decision = PolicyDecision.DENY
        
        return result
    
    def _mock_evaluate(self, policy_package: str, input_data: Dict) -> PolicyResult:
        """Mock policy evaluation for development/testing"""
        result = PolicyResult()
        
        if "rbac" in policy_package:
            return self._mock_rbac_policy(input_data)
        elif "security" in policy_package:
            return self._mock_security_policy(input_data)
        elif "compliance" in policy_package:
            return self._mock_compliance_policy(input_data)
        
        result.allowed = True
        result.decision = PolicyDecision.ALLOW
        return result
    
    def _mock_rbac_policy(self, input_data: Dict) -> PolicyResult:
        """Mock RBAC policy evaluation"""
        result = PolicyResult()
        user = input_data.get("user", {})
        action = input_data.get("action", "")
        
        role = user.get("role", "viewer")
        status = user.get("status", "active")
        
        if status == "suspended":
            result.denied_reasons.append(f"User '{user.get('id', 'unknown')}' is suspended")
            result.decision = PolicyDecision.DENY
            return result
        
        if role == "admin":
            result.allowed = True
            result.decision = PolicyDecision.ALLOW
        elif role == "developer":
            if action in ["code_generation", "code_review", "read"]:
                result.allowed = True
                result.decision = PolicyDecision.ALLOW
            else:
                result.denied_reasons.append(f"Developer role not authorized for action '{action}'")
                result.decision = PolicyDecision.DENY
        elif role == "viewer":
            if action == "read":
                result.allowed = True
                result.decision = PolicyDecision.ALLOW
            else:
                result.denied_reasons.append(f"Viewer role not authorized for action '{action}'")
                result.decision = PolicyDecision.DENY
        else:
            result.denied_reasons.append(f"Unknown role: {role}")
            result.decision = PolicyDecision.DENY
        
        return result
    
    def _mock_security_policy(self, input_data: Dict) -> PolicyResult:
        """Mock security policy evaluation"""
        result = PolicyResult()
        
        validation = input_data.get("validation_result", {})
        attack = input_data.get("attack_result", {})
        risk_score = input_data.get("overall_risk_score", 0)
        
        if attack.get("is_attack", False):
            result.denied_reasons.append(f"Attack detected: {attack.get('attack_types', [])}")
            result.decision = PolicyDecision.DENY
            return result
        
        critical_violations = [
            v for v in validation.get("violations", [])
            if v.get("severity") == "CRITICAL"
        ]
        
        if critical_violations:
            result.denied_reasons.append("Request contains critical security violations")
            result.decision = PolicyDecision.DENY
            return result
        
        if risk_score >= 80:
            result.denied_reasons.append(f"Risk score too high: {risk_score} (threshold: 80)")
            result.decision = PolicyDecision.DENY
            return result
        
        if risk_score >= 40:
            result.warnings.append("Medium risk detected - review recommended")
            result.decision = PolicyDecision.WARN
        
        if len(result.denied_reasons) == 0:
            result.allowed = True
            if len(result.warnings) == 0:
                result.decision = PolicyDecision.ALLOW
        
        return result
    
    def _mock_compliance_policy(self, input_data: Dict) -> PolicyResult:
        """Mock compliance policy evaluation"""
        result = PolicyResult()
        
        user = input_data.get("user", {})
        validation = input_data.get("validation_result", {})
        risk_score = input_data.get("overall_risk_score", 0)
        
        permissions = user.get("permissions", [])
        
        pii_violations = [
            v for v in validation.get("violations", [])
            if v.get("category") == "pii"
        ]
        
        if pii_violations and "pii_access" not in permissions:
            result.denied_reasons.append("PII detected but user lacks pii_access permission")
            result.decision = PolicyDecision.DENY
        
        ip_violations = [
            v for v in validation.get("violations", [])
            if v.get("category") == "internal_ip"
        ]
        
        if ip_violations and "internal_network_access" not in permissions:
            result.denied_reasons.append("Internal IP detected but user lacks internal_network_access permission")
            result.decision = PolicyDecision.DENY
        
        if user.get("department") == "external" or risk_score > 50:
            result.requires_audit = True
        
        if any(v.get("category") in ["secret", "pii"] for v in validation.get("violations", [])):
            result.requires_encryption = True
        
        if len(result.denied_reasons) == 0:
            result.allowed = True
            result.decision = PolicyDecision.ALLOW
        
        return result
    
    def close(self):
        """Close HTTP client"""
        self.client.close()

