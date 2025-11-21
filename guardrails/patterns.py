import re
from typing import Dict, List

class SecurityPatterns:
    SECRET_PATTERNS: Dict[str, str] = {
        "aws_access_key": r'AKIA[0-9A-Z]{16}',
        "aws_secret_key": r'[\'"][0-9a-zA-Z\/+]{40}[\'"]',
        "openai_key": r'sk-[a-zA-Z0-9]{20,}',
        "anthropic_key": r'sk-ant-[a-zA-Z0-9\-]{95,}',
        "github_token": r'ghp_[a-zA-Z0-9]{36,}',
        "github_oauth": r'gho_[a-zA-Z0-9]{36,}',
        "jwt_token": r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
        "stripe_key": r'(?:sk|pk)_(test|live)_[0-9a-zA-Z]{24,}',
        "slack_token": r'xox[baprs]-[0-9]{10,12}-[0-9]{10,12}-[a-zA-Z0-9]{24,}',
        "private_key": r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----',
        "password_in_url": r'[a-zA-Z]{3,10}://[^:]+:[^@]+@.+',
        "basic_auth": r'[Aa]uthorization:\s*[Bb]asic\s+[a-zA-Z0-9+/=]+',
        "bearer_token": r'[Aa]uthorization:\s*[Bb]earer\s+[a-zA-Z0-9\-._~+/]+=*',
        "generic_secret": r'(secret|password|passwd|pwd|api[_-]?key|apikey|access[_-]?token|auth[_-]?token)\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{8,}["\']?',
    }
    
    IP_PATTERNS: Dict[str, str] = {
        "internal_ip_10": r'\b10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}\b',
        "internal_ip_172": r'\b172\.(?:1[6-9]|2[0-9]|3[0-1])\.(?:[0-9]{1,3}\.)[0-9]{1,3}\b',
        "internal_ip_192": r'\b192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}\b',
        "localhost": r'\b127\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}\b',
    }
    
    PII_PATTERNS: Dict[str, str] = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "ssn": r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b',
        "credit_card": r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b',
        "phone_us": r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
    }
    
    DOMAIN_PATTERNS: Dict[str, str] = {
        "internal_domain": r'\b[a-zA-Z0-9-]+\.(internal|local|corp|lan|private)\b',
        "k8s_service": r'\b[a-zA-Z0-9-]+\.svc\.cluster\.local\b',
    }
    
    JAILBREAK_PHRASES: List[str] = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "disregard previous instructions",
        "forget previous instructions",
        "ignore the above",
        "disregard the above",
        "act as DAN",
        "developer mode",
        "jailbreak mode",
        "bypass guardrails",
        "bypass all restrictions",
        "remove all filters",
        "disable safety",
        "you are now in",
        "pretend you are",
        "simulate being",
        "override your programming",
        "ignore your guidelines",
        "forget your rules",
        "you are free from",
        "no longer bound by",
        "strip all restrictions",
    ]
    
    PROMPT_INJECTION_PATTERNS: List[str] = [
        r"(?i)system\s*:\s*(?:ignore|override|bypass)",
        r"(?i)new\s+(?:instruction|directive|command|rule)s?\s*:",
        r"(?i)(?:reveal|show|display|tell me)\s+(?:your|the)\s+(?:prompt|instruction|system message)",
        r"(?i)what\s+(?:are|were)\s+(?:your|the)\s+(?:original|initial|system)\s+(?:instruction|prompt|directive)",
        r"(?i)\\n\\n(?:===+|---+)\\n+system:",
        r"(?i)sudo\s+mode",
        r"(?i)admin\s+access",
        r"(?i)elevated\s+privilege",
    ]
    
    ENCODED_PAYLOAD_PATTERNS: List[str] = [
        r'(?:[A-Za-z0-9+/]{4}){10,}={0,2}',  # Base64
        r'(?:0x)?[0-9a-fA-F]{32,}',  # Hex
        r'\\x[0-9a-fA-F]{2}',  # Hex escape
        r'\\u[0-9a-fA-F]{4}',  # Unicode escape
    ]
    
    @classmethod
    def compile_patterns(cls, patterns: Dict[str, str]) -> Dict[str, re.Pattern]:
        return {name: re.compile(pattern) for name, pattern in patterns.items()}
    
    @classmethod
    def get_all_secret_patterns(cls) -> Dict[str, re.Pattern]:
        return cls.compile_patterns(cls.SECRET_PATTERNS)
    
    @classmethod
    def get_all_ip_patterns(cls) -> Dict[str, re.Pattern]:
        return cls.compile_patterns(cls.IP_PATTERNS)
    
    @classmethod
    def get_all_pii_patterns(cls) -> Dict[str, re.Pattern]:
        return cls.compile_patterns(cls.PII_PATTERNS)
    
    @classmethod
    def get_all_domain_patterns(cls) -> Dict[str, re.Pattern]:
        return cls.compile_patterns(cls.DOMAIN_PATTERNS)

