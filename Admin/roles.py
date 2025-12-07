from rolepermissions.roles import AbstractUserRole

class AdminRole(AbstractUserRole):
    available_permissions = {
        'create_bin': True,
    }

class DriverRole(AbstractUserRole):
    available_permissions = {
        'see_assigned_bins': True,

    }
    
class UserRole(AbstractUserRole):
    available_permissions = {
        'view_bins': True,

    }
