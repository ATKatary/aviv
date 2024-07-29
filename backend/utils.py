import logging
from django.db import models
from datetime import datetime
from rest_framework import status
from django.core.validators import RegexValidator 
from django.core.exceptions import ValidationError

WARN = "warn"
INFO = "info"
TITLE_LEN = 50
ERROR = "error"
FILE = "[utils]"
UPDATED = "updated"
logger = logging.getLogger('django')
password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

logger.setLevel(20)
def report(message: str, mode: str = INFO, debug: bool = False):
    # if logger.getEffectiveLevel() != 10: return 
    
    if mode == INFO: logger.info(message)
    if mode == WARN: logger.warn(message)
    if mode == ERROR: 
        logger.error(message, exc_info=debug)
        
def is_subset(A: list, B: list) -> status:
    for elm in A:
        if elm not in B: 
            return status.HTTP_412_PRECONDITION_FAILED
    
    return status.HTTP_200_OK

def get_or_create(model: models.Model, **kwargs): 
    result = None
    try:
        result = model.objects.get(**kwargs)
        report(f"{FILE}[get_or_create] >> found {result}!")
    except Exception as error:
        report(f"{FILE}[get_or_create] >> could not find {model.__class__.__name__} with {kwargs}")
        report(error, mode=ERROR, debug=True)
        if 'create' in kwargs and kwargs['create']:
            result = model.objects.create(**kwargs)
            report(f"{FILE}[get_or_create] >> created {result}")
            
    return result
    

validate_password = RegexValidator(password_regex)
leap_year = lambda year : year % 4 == 0

##### Functions #####
def validate_date(date):
    """
    Validates that a date is within 1900-01-01 through 2011-12-31 

    Inputs
        :param date: <str> formatted as YYYY-MM-DD
    
    Outputs
        :raises: <ValidationError> if the date is formatted incorrectly or the date does not exist 
    """
    try:
        return datetime(1950, 1, 1).date() < date < datetime.now().date()
    except ValidationError as error: print(f"Invalid date {date}\n{report(error)}")

def format(_format, variables):
    result = ""
    for part in _format: 
        if part.startswith("!"):
            result += f"{variables[part[1:]]}"
        else: result += part
    return result 
