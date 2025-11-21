from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class UserModel(BaseModel):
    id: str = Field(..., description="User ID")
    role: str = Field(default="viewer", description="User role: admin, developer, viewer")
    permissions: List[str] = Field(default_factory=list, description="User permissions")
    restrictions: List[str] = Field(default_factory=list, description="User restrictions")
    department: str = Field(default="internal", description="User department")
    status: str = Field(default="active", description="User status: active, suspended")


class PolicyCheckRequest(BaseModel):
    user: UserModel
    text: str = Field(..., description="Text to check")
    action: str = Field(default="code_generation", description="Action to perform")


class PolicyCheckResponse(BaseModel):
    decision: str
    allowed: bool
    rbac: Dict
    security: Dict
    compliance: Dict
    overall_risk_score: int
    requires_audit: bool
    requires_encryption: bool

