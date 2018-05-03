from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    ADMIN = 'AD'
    TRADER = 'TR'
    USER_TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (TRADER, 'Trader'),
    )
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES, default=TRADER)


class PaymentSource(models.Model):
    payment_source_id = models.AutoField(primary_key=True, unique=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", default=None)
    name = models.CharField(max_length=100)
    created_on = models.CharField(max_length=20)


class Wallet(models.Model):
    wallet_pmnt_src_id = models.ForeignKey(PaymentSource, on_delete=models.CASCADE, unique=True,
                                           db_column="payment_source_id")
    max_limit = models.PositiveSmallIntegerField()


class DebitCard(models.Model):
    card_pmnt_src_id = models.ForeignKey(PaymentSource, on_delete=models.CASCADE, unique=True,
                                         db_column="payment_source_id")
    bank_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=19, unique=True)
    name = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=20)


class Currency(models.Model):
    currency_name = models.CharField(max_length=100, primary_key=True)

    CRYPTO = "CR"
    USD = "UD"
    CURRENCY_TYPE_CHOICES = (
        (CRYPTO, 'Cryptocurrency'),
        (USD, 'Currency'),
    )
    currency_type = models.CharField(max_length=2, choices=CURRENCY_TYPE_CHOICES)

    converted_currency = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='currency_to_convert')


class PaymentSourceHasCurrency(models.Model):
    balance = models.CharField(max_length=100)
    pmnt_src_id = models.ForeignKey(PaymentSource, on_delete=models.CASCADE, db_column="payment_source_id")
    currency_name = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class META:
        unique_together = (("pmnt_src_id", "currency_name"),)


class TraderTradesUsingCurrency(models.Model):
    trader_id = models.ForeignKey(User, on_delete=models.CASCADE)
    currency_name = models.ForeignKey(Currency, on_delete=models.CASCADE)

    class META:
        unique_together = (("trader_id", "currency_name"),)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, unique=True)
    amount = models.PositiveIntegerField()
    date = models.CharField(max_length=20)
    # auto_now updates the object when it is saved [Model.save()]
    trader_id = models.ForeignKey(TraderTradesUsingCurrency, on_delete=models.CASCADE, related_name='transactions_traderID')
    currency_name = models.ForeignKey(TraderTradesUsingCurrency, on_delete=models.CASCADE, related_name='transactions_currency_name')

    class META:
        unique_together = (("trader_id", "currency_name"),)
