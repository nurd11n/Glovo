# Generated by Django 4.2.7 on 2023-11-13 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=60, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('is_company', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('activation_code', models.CharField(blank=True, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('languages', models.CharField(blank=True, max_length=256)),
                ('programming_languages', models.CharField(blank=True, max_length=256)),
                ('education', models.TextField(blank=True)),
                ('stack', models.CharField(blank=True, max_length=50)),
                ('about', models.TextField(blank=True)),
                ('age', models.IntegerField(blank=True)),
                ('work_experience', models.TextField(blank=True)),
                ('achievements', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='user/')),
                ('projects', models.ManyToManyField(blank=True, related_name='user', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('about', models.TextField(blank=True)),
                ('achievements', models.TextField(blank=True)),
                ('direction', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='company/')),
                ('members', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='accounts.userprofile')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='projects.project')),
            ],
        ),
    ]