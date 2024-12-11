import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import json
import os

class ConsentManager:
    """
    Comprehensive user consent management system for privacy and compliance.
    """
    
    CONSENT_STORAGE_PATH = 'user_consents/'
    CONSENT_EXPIRY = timedelta(days=365)
    
    @classmethod
    def _ensure_storage_directory(cls):
        """
        Ensure consent storage directory exists.
        """
        os.makedirs(cls.CONSENT_STORAGE_PATH, exist_ok=True)
    
    @classmethod
    def create_consent_record(
        self, 
        user_id: str, 
        consent_types: List[str],
        ip_address: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Create a new consent record for a user.
        
        Args:
            user_id (str): Unique user identifier
            consent_types (List[str]): List of consent types
            ip_address (str, optional): IP address of consent
        
        Returns:
            Dict containing consent details
        """
        self._ensure_storage_directory()
        
        consent_record = {
            'consent_id': str(uuid.uuid4()),
            'user_id': user_id,
            'consents': {
                consent_type: {
                    'status': 'GRANTED',
                    'timestamp': datetime.now().isoformat(),
                    'ip_address': ip_address
                } for consent_type in consent_types
            },
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        # Save consent record
        consent_file = os.path.join(
            self.CONSENT_STORAGE_PATH, 
            f'{user_id}_consent.json'
        )
        
        with open(consent_file, 'w') as f:
            json.dump(consent_record, f, indent=4)
        
        logging.info(f"Consent record created for user {user_id}")
        return consent_record
    
    @classmethod
    def update_consent(
        self, 
        user_id: str, 
        consent_type: str, 
        status: str,
        ip_address: Optional[str] = None
    ) -> bool:
        """
        Update consent for a specific type.
        
        Args:
            user_id (str): Unique user identifier
            consent_type (str): Type of consent to update
            status (str): New consent status (GRANTED/REVOKED)
            ip_address (str, optional): IP address of consent change
        
        Returns:
            bool: True if update successful, False otherwise
        """
        consent_file = os.path.join(
            self.CONSENT_STORAGE_PATH, 
            f'{user_id}_consent.json'
        )
        
        try:
            with open(consent_file, 'r') as f:
                consent_record = json.load(f)
            
            # Update specific consent type
            consent_record['consents'][consent_type] = {
                'status': status.upper(),
                'timestamp': datetime.now().isoformat(),
                'ip_address': ip_address
            }
            
            consent_record['last_updated'] = datetime.now().isoformat()
            
            # Save updated record
            with open(consent_file, 'w') as f:
                json.dump(consent_record, f, indent=4)
            
            logging.info(
                f"Consent updated for user {user_id}: "
                f"{consent_type} set to {status}"
            )
            return True
        
        except FileNotFoundError:
            logging.warning(f"No consent record found for user {user_id}")
            return False
        except Exception as e:
            logging.error(f"Consent update failed: {e}")
            return False
    
    @classmethod
    def check_consent(
        self, 
        user_id: str, 
        consent_type: str
    ) -> bool:
        """
        Check if a specific consent is currently granted.
        
        Args:
            user_id (str): Unique user identifier
            consent_type (str): Type of consent to check
        
        Returns:
            bool: True if consent is granted, False otherwise
        """
        consent_file = os.path.join(
            self.CONSENT_STORAGE_PATH, 
            f'{user_id}_consent.json'
        )
        
        try:
            with open(consent_file, 'r') as f:
                consent_record = json.load(f)
            
            # Check if consent exists and is granted
            consent = consent_record['consents'].get(consent_type, {})
            return consent.get('status', '').upper() == 'GRANTED'
        
        except FileNotFoundError:
            return False
        except Exception as e:
            logging.error(f"Consent check failed: {e}")
            return False
    
    @classmethod
    def get_consent_history(
        self, 
        user_id: str
    ) -> Optional[Dict]:
        """
        Retrieve full consent history for a user.
        
        Args:
            user_id (str): Unique user identifier
        
        Returns:
            Dict of consent history or None if not found
        """
        consent_file = os.path.join(
            self.CONSENT_STORAGE_PATH, 
            f'{user_id}_consent.json'
        )
        
        try:
            with open(consent_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"No consent history found for user {user_id}")
            return None
        except Exception as e:
            logging.error(f"Consent history retrieval failed: {e}")
            return None
    
    @classmethod
    def revoke_all_consents(
        self, 
        user_id: str, 
        ip_address: Optional[str] = None
    ) -> bool:
        """
        Revoke all consents for a user.
        
        Args:
            user_id (str): Unique user identifier
            ip_address (str, optional): IP address of consent revocation
        
        Returns:
            bool: True if successful, False otherwise
        """
        consent_file = os.path.join(
            self.CONSENT_STORAGE_PATH, 
            f'{user_id}_consent.json'
        )
        
        try:
            with open(consent_file, 'r') as f:
                consent_record = json.load(f)
            
            # Revoke all consents
            for consent_type in consent_record['consents']:
                consent_record['consents'][consent_type]['status'] = 'REVOKED'
                consent_record['consents'][consent_type]['revoked_at'] = datetime.now().isoformat()
                consent_record['consents'][consent_type]['revoke_ip_address'] = ip_address
            
            consent_record['last_updated'] = datetime.now().isoformat()
            
            # Save updated record
            with open(consent_file, 'w') as f:
                json.dump(consent_record, f, indent=4)
            
            logging.info(f"All consents revoked for user {user_id}")
            return True
        
        except FileNotFoundError:
            logging.warning(f"No consent record found for user {user_id}")
            return False
        except Exception as e:
            logging.error(f"Consent revocation failed: {e}")
            return False
    
    @classmethod
    def cleanup_expired_consents(self):
        """
        Remove or update expired consent records.
        """
        self._ensure_storage_directory()
        
        for filename in os.listdir(self.CONSENT_STORAGE_PATH):
            file_path = os.path.join(self.CONSENT_STORAGE_PATH, filename)
            
            try:
                with open(file_path, 'r') as f:
                    consent_record = json.load(f)
                
                created_at = datetime.fromisoformat(consent_record['created_at'])
                
                # Check if consent record has expired
                if datetime.now() - created_at > self.CONSENT_EXPIRY:
                    # Optional: Instead of deleting, you might want to archive
                    os.remove(file_path)
                    logging.info(f"Expired consent record removed: {filename}")
            
            except Exception as e:
                logging.error(f"Error processing consent record {filename}: {e}")

# Predefined Consent Types (example)
class ConsentTypes:
    """
    Standardized consent types for the application.
    """
    DATA_COLLECTION = 'DATA_COLLECTION'
    MARKETING_COMMUNICATIONS = 'MARKETING_COMMUNICATIONS'
    THIRD_PARTY_SHARING = 'THIRD_PARTY_SHARING'
    PERFORMANCE_TRACKING = 'PERFORMANCE_TRACKING'
    PERSONALIZATION = 'PERSONALIZATION'