from typing import Dict, List, Optional
from .opa_client import OPAClient, PolicyResult, PolicyDecision


class User:
    def __init__(self, user_id: str, role: str = "viewer", 
                 permissions: List[str] = None, 
                 restrictions: List[str] = None,
                 department: str = "internal",
                 status: str = "active"):
        self.id = user_id
        self.role = role
        self.permissions = permissions or []
        self.restrictions = restrictions or []
        self.department = department
        self.status = status
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "role": self.role,
            "permissions": self.permissions,
            "restrictions": self.restrictions,
            "department": self.department,
            "status": self.status
        }


class PolicyEvaluator:
    def __init__(self, opa_url: str = "http://localhost:8181", use_mock: bool = True):
        self.opa_client = OPAClient(opa_url, use_mock)
    
    async def evaluate_request(self, user: User, text: str, 
                               validation_result: Dict, 
                               attack_result: Dict,
                               action: str = "code_generation") -> Dict:
        """Evaluate complete request against all policies"""
        
        overall_risk_score = (
            validation_result.get("risk_score", 0) + 
            attack_result.get("risk_score", 0)
        )
        
        input_data = {
            "user": user.to_dict(),
            "text": text,
            "action": action,
            "validation_result": validation_result,
            "attack_result": attack_result,
            "overall_risk_score": overall_risk_score
        }
        
        rbac_result = await self.opa_client.evaluate_policy(
            "mcpsecurity/rbac", 
            input_data
        )
        
        security_result = await self.opa_client.evaluate_policy(
            "mcpsecurity/security",
            input_data
        )
        
        compliance_result = await self.opa_client.evaluate_policy(
            "mcpsecurity/compliance",
            input_data
        )
        
        final_decision = self._combine_decisions(
            rbac_result, 
            security_result, 
            compliance_result
        )
        
        return {
            "decision": final_decision.value,
            "allowed": self._is_allowed(rbac_result, security_result, compliance_result),
            "rbac": rbac_result.to_dict(),
            "security": security_result.to_dict(),
            "compliance": compliance_result.to_dict(),
            "overall_risk_score": overall_risk_score,
            "requires_audit": (
                rbac_result.requires_audit or 
                security_result.requires_audit or 
                compliance_result.requires_audit
            ),
            "requires_encryption": (
                rbac_result.requires_encryption or 
                security_result.requires_encryption or 
                compliance_result.requires_encryption
            )
        }
    
    def _is_allowed(self, rbac: PolicyResult, security: PolicyResult, 
                    compliance: PolicyResult) -> bool:
        """Check if all policies allow the request"""
        return rbac.allowed and security.allowed and compliance.allowed
    
    def _combine_decisions(self, rbac: PolicyResult, security: PolicyResult,
                           compliance: PolicyResult) -> PolicyDecision:
        """Combine multiple policy decisions"""
        if not self._is_allowed(rbac, security, compliance):
            return PolicyDecision.DENY
        
        if (rbac.decision == PolicyDecision.WARN or 
            security.decision == PolicyDecision.WARN or 
            compliance.decision == PolicyDecision.WARN):
            return PolicyDecision.WARN
        
        return PolicyDecision.ALLOW
    
    def close(self):
        """Close OPA client"""
        self.opa_client.close()

