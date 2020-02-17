from .models import Member

# receives a request object and membername + password parameters


def authenticate(request, email=None, password=None):
    try:
        member = Member.objects.get(email=email)
        # compare password with database
        if member.check_password(password):
            return member
        return None
    except member.DoesNotExist:
        return None


class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """

    # retrieve Member object for duration (Dauer) of the member session
    def get_member(self, member_id):
        try:
            member = Member.objects.get(pk=member_id)
            return member
        except member.DoesNotExist:
            return None
