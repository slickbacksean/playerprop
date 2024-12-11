from typing import Dict, List
from datetime import datetime, timedelta
import json
import uuid

class UserConsentManager:
    def __init__(self, consent_file: str = 'user_consents.json'):
        """
        Initialize User Consent Manager with persistent storage.
        
        Args:
            consent_file (str): Path to store consent records
        """
        self._consent_file = consent_file
        self._consents = self._load_consents()

    def _load_consents(self) -> Dict[str, Dict]:
        """
        Load existing consent records from file.
        
        Returns:
            Dict[str, Dict]: Loaded consent records
        """
        try:
            with open(self._consent_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_consents(self):
        """
        Save consent records to file.
        """
        with open(self._consent_file, 'w') as f:
            json.dump(self._consents, f, indent=4)

    def register_consent(self, user_id: str, consent_purposes: List[str], version: str = '1.0') -> str:
        """
        Register user consent for specific purposes.
        
        Args:
            user_id (str): Unique user identifier
            consent_purposes (List[str]): List of consent purposes
            version (str): Consent version
        
        Returns:
            str: Unique consent record ID
        """
        consent_id = str(uuid.uuid4())
        consent_record = {
            'consent_id': consent_id,
            'user_id': user_id,
            'purposes': consent_purposes,
            'version': version,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'active'
        }
        
        self._consents[consent_id] = consent_record
        self._save_consents()
        
        return consent_id

    def revoke_consent(self, consent_id: str):
        """
        Revoke a specific consent record.
        
        Args:
            consent_id (str): Consent record ID to revoke
        """
        if consent_id in self._consents:
            self._consents[consent_id]['status'] = 'revoked'
            self._consents[consent_id]['revocation_timestamp'] = datetime.utcnow().isoformat()
            self._save_consents()

    def check_consent(self, user_id: str, purpose: str) -> bool:
        """
        Check if a user has given consent for a specific purpose.
        
        Args:
            user_id (str): User identifier
            purpose (str): Purpose to check consent for
        
        Returns:
            bool: Whether consent is active for the purpose
        """
        user_consents = [
            consent for consent in self._consents.values()
            if consent['user_id'] == user_id and 
               purpose in consent['purposes'] and 
               consent['status'] == 'active'
        ]
        
        return len(user_consents) > 0

    def get_user_consents(self, user_id: str) -> List[Dict]:
        """
        Retrieve all consent records for a user.
        
        Args:
            user_id (str): User identifier
        
        Returns:
            List[Dict]: List of user's consent records
        """
        return [
            consent for consent in self._consents.values()
            if consent['user_id'] == user_id
        ]

def main():
    # Example usage
    consent_manager = UserConsentManager()
    
    # Register consent
    user_id = 'user123'
    consent_id = consent_manager.register_consent(
        user_id, 
        ['data_processing', 'marketing_emails']
    )
    
    # Check consent
    print("Consent for data processing:", 
        consent_manager.check_consent(user_id, 'data_processing')
    )
    
    # Revoke consent
    consent_manager.revoke_consent(consent_id)

if __name__ == "__main__":
    main()