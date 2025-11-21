from fastapi import APIRouter, HTTPException
from guardrails.input_validator import InputValidator
from guardrails.attack_detector import AttackDetector
from opa.policy_evaluator import PolicyEvaluator, User
from .opa_schemas import (
    UserModel,
    PolicyCheckRequest,
    PolicyCheckResponse
)

router = APIRouter(prefix="/policy", tags=["OPA Policy Engine"])

validator = InputValidator()
attack_detector = AttackDetector()
policy_evaluator = PolicyEvaluator(use_mock=True)


@router.post("/check", response_model=PolicyCheckResponse)
async def check_policy(request: PolicyCheckRequest):
    """
    Check request against all policies (RBAC, Security, Compliance).
    Evaluates user permissions, security violations, and compliance requirements.
    """
    validation_result = validator.validate(request.text)
    attack_result = attack_detector.detect(request.text)
    
    user = User(
        user_id=request.user.id,
        role=request.user.role,
        permissions=request.user.permissions,
        restrictions=request.user.restrictions,
        department=request.user.department,
        status=request.user.status
    )
    
    result = await policy_evaluator.evaluate_request(
        user=user,
        text=request.text,
        validation_result=validation_result.to_dict(),
        attack_result=attack_result.to_dict(),
        action=request.action
    )
    
    return PolicyCheckResponse(**result)


@router.get("/roles")
async def get_available_roles():
    """Get list of available user roles"""
    return {
        "roles": [
            {
                "name": "admin",
                "description": "Full access to all features",
                "permissions": ["*"]
            },
            {
                "name": "developer",
                "description": "Can generate and review code",
                "permissions": ["code_generation", "code_review", "read"]
            },
            {
                "name": "viewer",
                "description": "Read-only access",
                "permissions": ["read"]
            }
        ]
    }


@router.get("/permissions")
async def get_available_permissions():
    """Get list of available permissions"""
    return {
        "permissions": [
            {
                "name": "pii_access",
                "description": "Access to PII data"
            },
            {
                "name": "internal_network_access",
                "description": "Access to internal network resources"
            },
            {
                "name": "code_generation",
                "description": "Generate code"
            },
            {
                "name": "code_review",
                "description": "Review code"
            },
            {
                "name": "read",
                "description": "Read access"
            }
        ]
    }


@router.get("/restrictions")
async def get_available_restrictions():
    """Get list of available restrictions"""
    return {
        "restrictions": [
            {
                "name": "no_network_code",
                "description": "Cannot generate network-related code"
            },
            {
                "name": "no_file_system",
                "description": "Cannot generate file system code"
            }
        ]
    }

