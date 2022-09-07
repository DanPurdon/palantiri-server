# Generated by Django 4.1 on 2022-09-06 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Circler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=250)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateField()),
                ('circler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circler')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_sent', models.DateField()),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circle')),
                ('circler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circler')),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circle')),
                ('circler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circler')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateField()),
                ('circler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circler')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.post')),
            ],
        ),
        migrations.CreateModel(
            name='CircleMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circle')),
                ('circler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circler')),
            ],
        ),
        migrations.AddField(
            model_name='circle',
            name='circler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='palantiriAPI.circler'),
        ),
    ]
