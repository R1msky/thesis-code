# Generated by Django 3.1.7 on 2021-04-22 13:59

from django.db import migrations, models
import module.managers


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', module.managers.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Фото профиля'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email адрес'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='knowledge',
            field=models.TextField(blank=True, verbose_name='Знает'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='middle_name',
            field=models.CharField(max_length=30, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role_id',
            field=models.SmallIntegerField(verbose_name='role id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='skills',
            field=models.TextField(blank=True, verbose_name='Умеет'),
        ),
        migrations.AlterField(
            model_name='user',
            name='team_id',
            field=models.SmallIntegerField(verbose_name='team id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='technology',
            field=models.TextField(blank=True, verbose_name='Владеет'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Логин'),
        ),
    ]
