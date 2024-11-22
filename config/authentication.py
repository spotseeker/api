from spotseeker.user.models import User


def authentication_rule(user: User):
    return user is not None and user.is_active
