"""
User models
"""
import uuid
from utils import report
from django.db import models
from asgiref.sync import sync_to_async
from user.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

##### Global Constants #####
alphabet_size = 26

##### Classes #####
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    AF(first_name, last_name, date_of_birth, email) = user first_name last_name born on date_of_birth reachable at email
    
    Represnetation Invariant
        - inherits from AbstractBaseUser

    Representation Exposure
        - inherits from AbstractBaseUser
        - access is allowed to all fields but they are all immutable
    """
    
    ##### Representation #####
    name = models.CharField(max_length=2*alphabet_size)
    
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    id = models.UUIDField(primary_key=True, unique =True, editable=True)
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def has_permission(self, permission, obj = None) -> bool:
        """
        Checks if the user has the given permission on an obj
        
        Inputs
            :param permission: <str> referencing the functionailty in question
            :param obj: <object> with the permission
        
        Outputs
            :returns: <bool> True if has the given permission on the obj, False otherwise
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Override AbstractBaseUser.__str__() """
        return f"{self.name}: {self.id}"
    
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
    async def ajson(self):
        return await sync_to_async(self.json)()
