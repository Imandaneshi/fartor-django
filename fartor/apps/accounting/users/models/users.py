import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Our own custom User model
    """
    full_name = models.CharField(_('Full Name'), max_length=300, null=True, blank=True)
    # We use public id in order to not expose the pk(id),
    # You should never change users public id
    public_id = models.CharField(_('Public ID'), unique=True, max_length=50)

    def save(self, *args, **kwargs):
        self.set_public_id()
        super(User, self).save(*args, **kwargs)

    def set_public_id(self):
        # only set public_id for the first time
        if not self.public_id:
            # assign a random string to public_id
            self.public_id = User.get_public_id()

    @staticmethod
    def create_user(username, password, email, first_name=None, last_name=None):
        """
        This function create a new user

        :param username: user's username
        :type username: str
        :param password: user's password
        :type password: str
        :param email: user's email
        :type email: str
        :param first_name: users's first_name
        :type first_name: str
        :param last_name: user's last_name
        :type last_name: str
        :return: User object or None
        :rtype User
        """
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)

    @staticmethod
    def get_public_id():
        length = settings.USERS_MIN_PASSWORD_LENGTH
        allowed_chars = string.ascii_lowercase
        random_string = get_random_string(allowed_chars=allowed_chars, length=length)
        while User.objects.filter(public_id=random_string).exists():
            random_string = get_random_string(allowed_chars=allowed_chars, length=length)
        return random_string
