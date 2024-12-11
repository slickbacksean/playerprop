from datetime import date, datetime
import re

class AgeVerificationManager:
    @staticmethod
    def validate_age(birthdate: date, minimum_age: int = 18) -> bool:
        """
        Validate user's age against a minimum age requirement.
        
        Args:
            birthdate (date): User's birthdate
            minimum_age (int): Minimum age required (default 18)
        
        Returns:
            bool: Whether user meets age requirement
        """
        today = date.today()
        age = today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
        )
        return age >= minimum_age

    @staticmethod
    def parse_birthdate(birthdate_str: str) -> date:
        """
        Parse birthdate from various string formats.
        
        Args:
            birthdate_str (str): Birthdate in various formats
        
        Returns:
            date: Parsed birthdate
        
        Raises:
            ValueError: If birthdate cannot be parsed
        """
        date_formats = [
            '%Y-%m-%d',  # ISO format
            '%m/%d/%Y',  # US format
            '%d/%m/%Y',  # European format
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(birthdate_str, fmt).date()
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse birthdate: {birthdate_str}")

    def verify_and_log_age_compliance(self, user_data: dict, log_file: str = 'age_verification.log') -> bool:
        """
        Comprehensive age verification with logging.
        
        Args:
            user_data (dict): User registration data
            log_file (str): Path to log verification attempts
        
        Returns:
            bool: Whether user is compliant with age requirements
        """
        try:
            birthdate = self.parse_birthdate(user_data['birthdate'])
            is_age_compliant = self.validate_age(birthdate)
            
            # Log verification attempt
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now().isoformat()} - "
                          f"User: {user_data.get('email', 'Unknown')} - "
                          f"Age Compliant: {is_age_compliant}\n")
            
            return is_age_compliant
        
        except (KeyError, ValueError) as e:
            # Log and handle invalid data
            with open(log_file, 'a') as log:
                log.write(f"{datetime.now().isoformat()} - "
                          f"Verification Error: {str(e)}\n")
            return False

def main():
    # Example usage
    age_verifier = AgeVerificationManager()
    
    # Test cases
    test_users = [
        {'email': 'adult@example.com', 'birthdate': '1990-05-15'},
        {'email': 'minor@example.com', 'birthdate': '2010-05-15'}
    ]
    
    for user in test_users:
        is_compliant = age_verifier.verify_and_log_age_compliance(user)
        print(f"{user['email']} Age Compliant: {is_compliant}")

if __name__ == "__main__":
    main()