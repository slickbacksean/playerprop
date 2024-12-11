import re
import logging
from typing import Dict, List

class PasswordStrengthValidator:
    """
    Comprehensive password strength validation system.
    """
    
    @staticmethod
    def validate_password(password: str) -> Dict[str, bool]:
        """
        Validate password strength across multiple dimensions.
        
        Args:
            password (str): Password to validate
        
        Returns:
            Dict of validation criteria and their status
        """
        if not password:
            return {
                'length': False,
                'complexity': False,
                'no_common_patterns': False,
                'no_personal_info': False,
                'overall_strength': False
            }
        
        validation_results = {
            'length': len(password) >= 12,
            'complexity': PasswordStrengthValidator._check_complexity(password),
            'no_common_patterns': not PasswordStrengthValidator._has_common_patterns(password),
            'no_personal_info': not PasswordStrengthValidator._contains_personal_info(password)
        }
        
        validation_results['overall_strength'] = all(validation_results.values())
        
        return validation_results
    
    @staticmethod
    def _check_complexity(password: str) -> bool:
        """
        Check password complexity requirements.
        
        Args:
            password (str): Password to check
        
        Returns:
            bool: True if password meets complexity requirements
        """
        complexity_checks = [
            bool(re.search(r'[A-Z]', password)),  # Uppercase letter
            bool(re.search(r'[a-z]', password)),  # Lowercase letter
            bool(re.search(r'\d', password)),     # Digit
            bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))  # Special character
        ]
        
        return sum(complexity_checks) >= 3
    
    @staticmethod
    def _has_common_patterns(password: str) -> bool:
        """
        Check for common password patterns.
        
        Args:
            password (str): Password to check
        
        Returns:
            bool: True if common patterns are found
        """
        common_patterns = [
            r'123', r'abc', r'qwerty', r'password', r'letmein', 
            r'admin', r'welcome', r'login', r'111', r'000'
        ]
        
        return any(pattern in password.lower() for pattern in common_patterns)
    
    @staticmethod
    def _contains_personal_info(password: str) -> bool:
        """
        Check if password contains potential personal information.
        
        Args:
            password (str): Password to check
        
        Returns:
            bool: True if personal info is found
        """
        # Note: In a real implementation, this would use actual user data
        potential_personal_info = [
            'birthday', 'birthdate', 'name', 'username', 
            'email', 'phone', 'address'
        ]
        
        return any(info in password.lower() for info in potential_personal_info)
    
    @classmethod
    def get_password_strength_feedback(cls, password: str) -> List[str]:
        """
        Provide specific feedback about password strength.
        
        Args:
            password (str): Password to analyze
        
        Returns:
            List of improvement suggestions
        """
        validation = cls.validate_password(password)
        feedback = []
        
        if not validation['length']:
            feedback.append("Password should be at least 12 characters long")
        
        if not validation['complexity']:
            feedback.append("Include a mix of uppercase, lowercase, numbers, and special characters")
        
        if validation['no_common_patterns']:
            feedback.append("Avoid using common patterns or simple sequences")
        
        if validation['no_personal_info']:
            feedback.append("Avoid using personal information in your password")
        
        return feedback