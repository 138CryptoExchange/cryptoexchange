# Generated by Django 2.0.4 on 2018-05-02 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('currency_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('currency_type', models.CharField(choices=[('CR', 'Cryptocurrency'), ('UD', 'Currency')], max_length=2)),
                ('converted_currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currency_to_convert', to='market.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='DebitCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('card_number', models.CharField(max_length=19, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('expiry_date', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentSource',
            fields=[
                ('payment_source_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('created_on', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PmntSrc_HAS_Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.CharField(max_length=100)),
                ('currency_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Currency')),
                ('pmnt_src_id', models.ForeignKey(db_column='payment_source_id', on_delete=django.db.models.deletion.CASCADE, to='market.PaymentSource')),
            ],
        ),
        migrations.CreateModel(
            name='Trader_TradesUsing_Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('transaction_currency', models.CharField(max_length=100)),
                ('amount', models.PositiveIntegerField()),
                ('date', models.CharField(max_length=20)),
                ('currency_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_currency_name', to='market.Trader_TradesUsing_Currency')),
                ('trader_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions_traderID', to='market.Trader_TradesUsing_Currency')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('user_type', models.CharField(choices=[('AD', 'Admin'), ('TR', 'Trader')], default='TR', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_limit', models.PositiveSmallIntegerField()),
                ('wallet_pmnt_src_id', models.ForeignKey(db_column='payment_source_id', on_delete=django.db.models.deletion.CASCADE, to='market.PaymentSource', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='trader_tradesusing_currency',
            name='trader_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
        migrations.AddField(
            model_name='paymentsource',
            name='u_id',
            field=models.ForeignKey(db_column='user_id', default=None, on_delete=django.db.models.deletion.CASCADE, to='market.User'),
        ),
        migrations.AddField(
            model_name='debitcard',
            name='card_pmnt_src_id',
            field=models.ForeignKey(db_column='payment_source_id', on_delete=django.db.models.deletion.CASCADE, to='market.PaymentSource', unique=True),
        ),
    ]
