import re
from typing import Dict, List
from .patterns import SecurityPatterns


class AttackResult:
    def __init__(self):
        self.is_attack: bool = False
        self.attack_types: List[str] = []
        self.detections: List[Dict[str, str]] = []
        self.risk_score: int = 0
    
    def add_detection(self, attack_type: str, pattern: str, matched_text: str, severity: str = "HIGH"):
        self.is_attack = True
        if attack_type not in self.attack_types:
            self.attack_types.append(attack_type)
        
        self.detections.append({
            "type": attack_type,
            "pattern": pattern,
            "matched": matched_text[:100] + "..." if len(matched_text) > 100 else matched_text,
            "severity": severity
        })
        
        self.risk_score += 40 if severity == "CRITICAL" else 25
    
    def to_dict(self) -> Dict:
        return {
            "is_attack": self.is_attack,
            "attack_types": self.attack_types,
            "detections": self.detections,
            "risk_score": self.risk_score,
            "total_detections": len(self.detections)
        }


class AttackDetector:
    def __init__(self):
        self.jailbreak_phrases = SecurityPatterns.JAILBREAK_PHRASES
        self.injection_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in SecurityPatterns.PROMPT_INJECTION_PATTERNS
        ]
        self.encoded_patterns = [
            re.compile(pattern) 
            for pattern in SecurityPatterns.ENCODED_PAYLOAD_PATTERNS
        ]
    
    def detect(self, text: str) -> AttackResult:
        result = AttackResult()
        
        self._check_jailbreak(text, result)
        self._check_prompt_injection(text, result)
        self._check_encoded_payloads(text, result)
        self._check_multi_turn_attack(text, result)
        
        return result
    
    def _check_jailbreak(self, text: str, result: AttackResult):
        text_lower = text.lower()
        
        for phrase in self.jailbreak_phrases:
            if phrase in text_lower:
                result.add_detection(
                    attack_type="jailbreak",
                    pattern=f"jailbreak_phrase: {phrase}",
                    matched_text=phrase,
                    severity="CRITICAL"
                )
    
    def _check_prompt_injection(self, text: str, result: AttackResult):
        for pattern in self.injection_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                result.add_detection(
                    attack_type="prompt_injection",
                    pattern="injection_pattern",
                    matched_text=match.group(0),
                    severity="CRITICAL"
                )
    
    def _check_encoded_payloads(self, text: str, result: AttackResult):
        for pattern in self.encoded_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                encoded_text = match.group(0)
                if len(encoded_text) > 100:
                    result.add_detection(
                        attack_type="encoded_payload",
                        pattern="suspicious_encoding",
                        matched_text=encoded_text,
                        severity="HIGH"
                    )
    
    def _check_multi_turn_attack(self, text: str, result: AttackResult):
        multi_turn_indicators = [
            r"(?i)in\s+your\s+next\s+response",
            r"(?i)when\s+I\s+say\s+['\"].*['\"],?\s+you\s+(?:will|must|should)",
            r"(?i)remember\s+this\s+for\s+later",
            r"(?i)in\s+future\s+conversations?",
        ]
        
        for indicator_pattern in multi_turn_indicators:
            pattern = re.compile(indicator_pattern)
            if pattern.search(text):
                result.add_detection(
                    attack_type="multi_turn_attack",
                    pattern="multi_turn_setup",
                    matched_text=pattern.search(text).group(0),
                    severity="HIGH"
                )
    
    def is_safe(self, text: str) -> bool:
        result = self.detect(text)
        return not result.is_attack

