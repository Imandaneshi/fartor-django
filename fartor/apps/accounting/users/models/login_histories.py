from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class LoginHistory(models.Model):
    """
    This model is used to log user login attempts no matter they were successful or not

    .. todo:: Add a command for removing old login histories
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             verbose_name=_('User'), )
    time = models.DateTimeField(_('Time'), auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField(_('IP'), max_length=50, null=True, blank=True)
    successful = models.BooleanField(_('Successful'), default=False)

    def __str__(self):
        return f"{self.ip or ''} - {self.id}"

    @staticmethod
    def create_history(user, ip=None, successful=True):
        login_history = LoginHistory(user=user, ip=ip, successful=successful)
        login_history.save()
        return login_history
