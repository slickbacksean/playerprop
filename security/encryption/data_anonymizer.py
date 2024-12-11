import hashlib
import re
from typing import Dict, Any
from cryptography.fernet import Fernet

class DataAnonymizer:
    def __init__(self):
        # Generate a key for encryption
        self._encryption_key = Fernet.generate_key()
        self._cipher_suite = Fernet(self._encryption_key)

    def hash_sensitive_data(self, data: str) -> str:
        """
        Hash sensitive data using SHA-256 for irreversible anonymization.
        
        Args:
            data (str): The sensitive data to be hashed
        
        Returns:
            str: Hashed representation of the data
        """
        return hashlib.sha256(data.encode()).hexdigest()

    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypt sensitive data using Fernet symmetric encryption.
        
        Args:
            data (str): The data to be encrypted
        
        Returns:
            bytes: Encrypted data
        """
        return self._cipher_suite.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypt previously encrypted data.
        
        Args:
            encrypted_data (bytes): The encrypted data
        
        Returns:
            str: Decrypted data
        """
        return self._cipher_suite.decrypt(encrypted_data).decode()

    def anonymize_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize user data by hashing or encrypting sensitive fields.
        
        Args:
            user_data (Dict[str, Any]): Original user data dictionary
        
        Returns:
            Dict[str, Any]: Anonymized user data
        """
        anonymized_data = user_data.copy()
        
        # Fields to anonymize
        anonymized_data['email'] = self.hash_sensitive_data(user_data['email'])
        anonymized_data['phone'] = self.hash_sensitive_data(user_data['phone']) if 'phone' in user_data else None
        
        # Optional: Encrypt more sensitive information
        if 'full_name' in user_data:
            anonymized_data['name_encrypted'] = self.encrypt_data(user_data['full_name'])
        
        return anonymized_data

    def validate_anonymization(self, original_data: Dict[str, Any], anonymized_data: Dict[str, Any]) -> bool:
        """
        Validate that anonymization process maintains data integrity.
        
        Args:
            original_data (Dict[str, Any]): Original user data
            anonymized_data (Dict[str, Any]): Anonymized user data
        
        Returns:
            bool: Whether anonymization was successful and reversible
        """
        try:
            # Validate hashed email
            assert self.hash_sensitive_data(original_data['email']) == anonymized_data['email']
            
            # Optional decryption validation
            if 'full_name' in original_data:
                decrypted_name = self.decrypt_data(anonymized_data['name_encrypted'])
                assert decrypted_name == original_data['full_name']
            
            return True
        except AssertionError:
            return False

def main():
    # Example usage
    anonymizer = DataAnonymizer()
    user_data = {
        'email': 'user@example.com',
        'phone': '1234567890',
        'full_name': 'John Doe',
        'age': 30
    }
    
    anonymized_data = anonymizer.anonymize_user_data(user_data)
    print("Anonymized Data:", anonymized_data)
    
    # Validate anonymization
    is_valid = anonymizer.validate_anonymization(user_data, anonymized_data)
    print("Anonymization Valid:", is_valid)

if __name__ == "__main__":
    main()