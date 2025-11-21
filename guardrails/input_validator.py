import re
from typing import Dict, List, Tuple
from .patterns import SecurityPatterns


class ValidationResult:
    def __init__(self):
        self.is_safe: bool = True
        self.violations: List[Dict[str, str]] = []
        self.risk_score: int = 0
        
    def add_violation(self, category: str, pattern_name: str, matched_text: str):
        self.is_safe = False
        self.violations.append({
            "category": category,
            "pattern": pattern_name,
            "matched": matched_text[:50] + "..." if len(matched_text) > 50 else matched_text,
            "severity": self._get_severity(category)
        })
        self.risk_score += self._get_risk_score(category)
    
    def _get_severity(self, category: str) -> str:
        severity_map = {
            "secret": "CRITICAL",
            "pii": "HIGH",
            "internal_ip": "HIGH",
            "internal_domain": "MEDIUM",
        }
        return severity_map.get(category, "MEDIUM")
    
    def _get_risk_score(self, category: str) -> int:
        score_map = {
            "secret": 50,
            "pii": 30,
            "internal_ip": 30,
            "internal_domain": 20,
        }
        return score_map.get(category, 10)
    
    def to_dict(self) -> Dict:
        return {
            "is_safe": self.is_safe,
            "violations": self.violations,
            "risk_score": self.risk_score,
            "total_violations": len(self.violations)
        }


class InputValidator:
    def __init__(self):
        self.secret_patterns = SecurityPatterns.get_all_secret_patterns()
        self.ip_patterns = SecurityPatterns.get_all_ip_patterns()
        self.pii_patterns = SecurityPatterns.get_all_pii_patterns()
        self.domain_patterns = SecurityPatterns.get_all_domain_patterns()
    
    def validate(self, text: str) -> ValidationResult:
        result = ValidationResult()
        
        self._check_secrets(text, result)
        self._check_internal_ips(text, result)
        self._check_pii(text, result)
        self._check_internal_domains(text, result)
        
        return result
    
    def _check_secrets(self, text: str, result: ValidationResult):
        for name, pattern in self.secret_patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                result.add_violation(
                    category="secret",
                    pattern_name=name,
                    matched_text=match.group(0)
                )
    
    def _check_internal_ips(self, text: str, result: ValidationResult):
        for name, pattern in self.ip_patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                result.add_violation(
                    category="internal_ip",
                    pattern_name=name,
                    matched_text=match.group(0)
                )
    
    def _check_pii(self, text: str, result: ValidationResult):
        for name, pattern in self.pii_patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                result.add_violation(
                    category="pii",
                    pattern_name=name,
                    matched_text=match.group(0)
                )
    
    def _check_internal_domains(self, text: str, result: ValidationResult):
        for name, pattern in self.domain_patterns.items():
            matches = pattern.finditer(text)
            for match in matches:
                result.add_violation(
                    category="internal_domain",
                    pattern_name=name,
                    matched_text=match.group(0)
                )
    
    def quick_check(self, text: str) -> bool:
        result = self.validate(text)
        return result.is_safe

