from enum import Enum, auto
from typing import List, Dict, Set
import logging

class RolePermission(Enum):
    """
    Comprehensive enumeration of system permissions.
    """
    # User-related permissions
    CREATE_USER = auto()
    UPDATE_USER = auto()
    DELETE_USER = auto()
    VIEW_USER_PROFILE = auto()
    
    # Prediction-related permissions
    CREATE_PREDICTION = auto()
    UPDATE_PREDICTION = auto()
    DELETE_PREDICTION = auto()
    VIEW_PREDICTION = auto()
    
    # System-level permissions
    ADMIN_ACCESS = auto()
    SYSTEM_CONFIG = auto()
    AUDIT_LOG_VIEW = auto()

class RoleBasedAccessControl:
    """
    Centralized role-based access control system.
    """
    
    # Role to permission mappings
    _ROLE_PERMISSIONS: Dict[str, Set[RolePermission]] = {
        'ADMIN': {
            RolePermission.CREATE_USER,
            RolePermission.UPDATE_USER,
            RolePermission.DELETE_USER,
            RolePermission.VIEW_USER_PROFILE,
            RolePermission.CREATE_PREDICTION,
            RolePermission.UPDATE_PREDICTION,
            RolePermission.DELETE_PREDICTION,
            RolePermission.VIEW_PREDICTION,
            RolePermission.ADMIN_ACCESS,
            RolePermission.SYSTEM_CONFIG,
            RolePermission.AUDIT_LOG_VIEW
        },
        'ANALYST': {
            RolePermission.CREATE_PREDICTION,
            RolePermission.UPDATE_PREDICTION,
            RolePermission.VIEW_PREDICTION
        },
        'USER': {
            RolePermission.CREATE_PREDICTION,
            RolePermission.VIEW_PREDICTION
        },
        'GUEST': {
            RolePermission.VIEW_PREDICTION
        }
    }
    
    @classmethod
    def check_permission(cls, role: str, permission: RolePermission) -> bool:
        """
        Check if a specific role has a given permission.
        
        Args:
            role (str): User's role
            permission (RolePermission): Permission to check
        
        Returns:
            bool: True if role has permission, False otherwise
        """
        try:
            return permission in cls._ROLE_PERMISSIONS.get(role.upper(), set())
        except Exception as e:
            logging.error(f"Permission check failed: {e}")
            return False
    
    @classmethod
    def get_role_permissions(cls, role: str) -> Set[RolePermission]:
        """
        Get all permissions for a specific role.
        
        Args:
            role (str): Role to retrieve permissions for
        
        Returns:
            Set of permissions for the role
        """
        return cls._ROLE_PERMISSIONS.get(role.upper(), set())
    
    @classmethod
    def upgrade_user_role(cls, current_role: str, target_role: str) -> bool:
        """
        Check if a role upgrade is possible.
        
        Args:
            current_role (str): Current user role
            target_role (str): Role to upgrade to
        
        Returns:
            bool: True if upgrade is allowed, False otherwise
        """
        role_hierarchy = {
            'GUEST': ['USER', 'ANALYST', 'ADMIN'],
            'USER': ['ANALYST', 'ADMIN'],
            'ANALYST': ['ADMIN'],
            'ADMIN': []
        }
        
        try:
            current_role = current_role.upper()
            target_role = target_role.upper()
            
            return target_role in role_hierarchy.get(current_role, [])
        except Exception as e:
            logging.error(f"Role upgrade check failed: {e}")
            return False