"""
User managers
"""
import uuid
from rest_framework import status
from django.core.validators import validate_email
from django.contrib.auth.models import BaseUserManager
from utils import validate_date, validate_password, report, ERROR
from django.core.exceptions import ValidationError, ObjectDoesNotExist

##### Classes #####
class CustomUserManager(BaseUserManager):
    """
    AF(name, id, password) = a CustomUser based on the specified information

    Definitions
        first-time 
            with valid non-existing email creditionals

            The user's email was valid and not in the database, the user was a first-time

    Representation Invariant
        - inherits from BaseUserManager
        - user must be a first-time
        - password must ...
                        ... be of length >= 8 characters
                        ... include at least 1 capital letter
                        ... include at least 1 lowercase letter
                        ... include at least 1 number 
                        ... include at least 1 special character
                        ... can't include the user's name, date of birth or email

    Representation Exposure
        - inherits from BaseUserManager
    """
    use_in_migrations = True
    
    def create(self, id, name, password = None):
        """
        Creates and saves first-time user first_name last_name born on date_of_birth with email and password
        
        Definitions 
            user 
                ployem memeber with access to everything except any administative, private, and regulatory functions

                A user can view public tools but can not regulate them without permission

        Inputs
            :param first_name: <str> first name of the user
            :param last_name: <str> last name of the user
            :param date_of_birth: <datetime> date of birth of the user
            :param email: <str> email of the user
            :param password: <str> password protecting user's account

        Outputs
            :returns: <CustomUser> representing the newly created and saved user  
                      Status ...
                             ... HTTP_201_CREATED if the user is signed up successfully
                             ... HTTP_403_FORBIDDEN if email is unreachable 
                             ... HTTP_412_PRECONDITION_FAILED if one ore more of the request fields don't meet their precondition(s)          
        """
        try: 
            # validate_password(password)
            if self.get(id=id): 
                raise ValidationError(f"User {id} exists")
    
        except ValidationError as error:
            print(f"Error occured while signing up user\n{report(error, mode=ERROR, debug=True)}")
            return None, status.HTTP_412_PRECONDITION_FAILED

        except ObjectDoesNotExist as error:
            user = self.model(
                id=id,
                name=name
            )
    
            user.set_password(password)
            user.save(using=self._db)

            return user, status.HTTP_201_CREATED

    def create_superuser(self, id, name, password = None):
        """
        Creates and saves first-time user first_name last_name born on date_of_birth with email and password
        
        Definitions 
            user 
                ployem memeber with access to everything except any administative, private, and regulatory functions

                A user can view public tools but can not regulate them without permission

        Inputs
            :param first_name: <str> first name of the user
            :param last_name: <str> last name of the user
            :param date_of_birth: <datetime> date of birth of the user
            :param email: <str> email of the user
            :param password: <str> password protecting user's account

        Outputs
            :returns: <CustomUser> representing the newly created and saved user  
                      Status ...
                             ... HTTP_201_CREATED if the user is signed up successfully
                             ... HTTP_403_FORBIDDEN if email is unreachable 
                             ... HTTP_412_PRECONDITION_FAILED if one ore more of the request fields don't meet their precondition(s)          
        """
        user, user_status = self.create(id, name, password=password)

        if user_status == status.HTTP_201_CREATED:
            print("User created\nSetting permissions ...")
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
            user.save(using = self._db)
        else: print(f"Failed to create user: {user_status}")

        return user, user_status


    def upgrade(self):
        """             
        """
        raise NotImplementedError
