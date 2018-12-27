# Generated by Django 2.1.4 on 2018-12-27 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_id', models.IntegerField()),
                ('scheduled_time', models.DateTimeField(null=True, verbose_name='scheduled time')),
                ('real_time', models.DateTimeField(null=True, verbose_name='real time')),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=18)),
                ('direction', models.CharField(max_length=200)),
                ('trip', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('x_coordinate', models.IntegerField(default=0)),
                ('y_coordinate', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StopsOfLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miner.Line')),
                ('stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miner.Stop')),
            ],
        ),
        migrations.AddField(
            model_name='departure',
            name='line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='miner.Line'),
        ),
        migrations.AddField(
            model_name='departure',
            name='stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='miner.Stop'),
        ),
    ]
