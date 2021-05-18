from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from module.managers import UserManager


class Role(models.Model):
    role_name = models.CharField(_('Роль'), max_length=30)


class Team(models.Model):
    team_name = models.SmallIntegerField(_('Номер команды'))


class User(AbstractBaseUser):
    username = models.CharField(_('Логин'), max_length=30, unique=True)
    email = models.EmailField(_('Email адрес'), unique=True)
    first_name = models.CharField(_('Имя'), max_length=30)
    middle_name = models.CharField(_('Отчество'), max_length=30)
    last_name = models.CharField(_('Фамилия'), max_length=30)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Фото профиля')
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    group_id = models.SmallIntegerField(_('Группа'), default=0)
    knowledge = models.TextField(_('Знает'), blank=True)
    skills = models.TextField(_('Умеет'), blank=True)
    technology = models.TextField(_('Владеет'), blank=True)
    vk_link = models.URLField(_('ВК'), unique=True, blank=True)
    student_ticket = models.CharField(_('Студенческий билет'), max_length=9, unique=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'middle_name', 'last_name']

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)