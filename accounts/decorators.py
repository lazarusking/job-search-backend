from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def recruiter_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a recruiter
    redirects to the login page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_recruiter,
        login_url=login_url,
        redirect_field_name=redirect_field_name)

    if function:
        return actual_decorator(function)
    return actual_decorator


def normal_user_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a normal 
    user redirects to the login page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_recruiter,
        login_url=login_url,
        redirect_field_name=redirect_field_name)

    if function:
        return actual_decorator(function)
    return actual_decorator
