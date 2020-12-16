# Generated by Django 3.1.3 on 2020-12-16 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0002_alter_group_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.CharField(choices=[('open', 'open'), ('closed', 'closed')], default='open', max_length=56, verbose_name='status')),
                ('quantity', models.DecimalField(decimal_places=5, max_digits=12, verbose_name='quantity')),
                ('side', models.CharField(choices=[('buy', 'buy'), ('sell', 'sell')], max_length=56, verbose_name='side')),
                ('type', models.CharField(choices=[('market', 'market'), ('limit', 'limit'), ('stop', 'stop'), ('stop_limit', 'stop limit'), ('trailing_stop', 'trailing stop')], max_length=56, verbose_name='side')),
                ('time_in_force', models.CharField(choices=[('day', 'day'), ('gtc', 'good till cancelled'), ('opg', 'order on open'), ('cls', 'order on close'), ('ioc', 'immediate or cancel'), ('fok', 'fill or kill')], max_length=56, verbose_name='time in force')),
                ('limit_price', models.DecimalField(blank=True, decimal_places=5, max_digits=12, null=True, verbose_name='limit price')),
                ('stop_price', models.DecimalField(blank=True, decimal_places=5, max_digits=12, null=True, verbose_name='stop price')),
                ('trail_price', models.DecimalField(blank=True, decimal_places=5, max_digits=12, null=True, verbose_name='trail price')),
                ('trail_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='trail percentage')),
                ('extended_hours', models.BooleanField(default=False)),
                ('client_order_id', models.UUIDField(editable=False, unique=True)),
                ('order_class', models.CharField(blank=True, choices=[('simple', 'simple'), ('bracket', 'bracket'), ('oco', 'one cancels other'), ('oto', 'one triggers other')], max_length=56, null=True, verbose_name='order class')),
                ('take_profit', models.JSONField(blank=True, null=True, verbose_name='take profit')),
                ('stop_loss', models.JSONField(blank=True, null=True, verbose_name='stop loss')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='assets.asset', verbose_name='symbols')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
    ]
