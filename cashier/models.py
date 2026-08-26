from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Signature(models.Model):
    field1 = models.CharField(max_length=100, blank=True, default='')
    field2 = models.IntegerField(default=0)
    note = models.CharField(max_length=255, blank=True, default='')

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_created_by')

    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(app_label)s_%(class)s_updated_by')


    class Meta:
        abstract = True

class Status(models.IntegerChoices):
    INACTIVE = 0, "Inactive"
    ACTIVE = 1, "Active"

class Branch(Signature):
    cid = models.CharField(max_length=10)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=255)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = "branch"
        managed = False

class Bank(Signature):
    cid = models.CharField(max_length=20, db_index=True)

    name = models.CharField(max_length=100)

    short_name = models.CharField(max_length=50)

    address = models.CharField(max_length=100)

    status = models.IntegerField(default=1)

    class Meta:
        db_table = "bank"
        managed = False

class BranchBank(Signature):
    cid = models.CharField(max_length=20)

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="banks"
    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    class Meta:
        db_table = "branch_bank"
        unique_together = ("branch", "bank")
        managed = False

    def __str__(self):
        return f"{self.branch} - {self.bank}"

class BankAccount(Signature):
    cid = models.CharField(max_length=20)

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="bank_accounts"
    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="accounts"
    )

    account_number = models.CharField(max_length=20)

    account_type = models.CharField(max_length=50)

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ACTIVE
    )

    class Meta:
        db_table = "bank_account"
        managed = False

    def __str__(self):
        return self.account_number

class Segment(Signature):
    cid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = "segment"
        managed = False

class Brand(Signature):
    cid = models.CharField(max_length=20, db_index=True)

    code = models.CharField(max_length=50)

    name = models.CharField(max_length=100)

    short_name = models.CharField(max_length=50)

    segment = models.ForeignKey(
        Segment,
        on_delete=models.PROTECT,
        related_name="brand"
    )

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.ACTIVE
    )

    class Meta:
        db_table = "brand"
        managed = False

class BrandBranch(Signature):
    cid = models.CharField(max_length=20)

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="brand_branches"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="branch_brands"
    )

    class Meta:
        db_table = "brand_branch"
        unique_together = ("brand", "branch")
        managed = False

    def __str__(self):
        return f"{self.brand} - {self.branch}"

class OpeningHead(Signature):
    cid = models.CharField(max_length=20, default='')
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    opening_balance = models.FloatField(default=0)
    pc_bank_amount = models.FloatField(default=0)
    pc_cash_amount = models.FloatField(default=0)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    month = models.CharField(max_length=10, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'opening_h'
        managed = False


class OpeningDetail(Signature):
    cid = models.CharField(max_length=20, default='')
    trans_id = models.IntegerField(default=0)
    trans_sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    segment_id = models.IntegerField(default=0)
    segment_name = models.CharField(max_length=50, blank=True, null=True)
    brand_id = models.IntegerField(default=0)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    collection = models.FloatField(default=0)
    outstanding = models.FloatField(default=0)
    pc_bank_amount = models.FloatField(default=0)
    pc_cash_amount = models.FloatField(default=0)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)
    year = models.CharField(max_length=4, blank=True, null=True)
    month = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'opening_d'
        managed = False

class OpenDate(Signature):
    cid = models.CharField(max_length=20, default='')

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    active_date = models.TextField()
    expire_at = models.DateField()
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'open_date'
        managed = False


class TrReceiptHead(Signature):
    cid = models.CharField(max_length=20, default='')  # pydal default=cid was a runtime session value; set via view/serializer, not a static default
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'tr_receipt_h'
        managed = False  # matches migrate=False — Django won't create/alter this table


class TrReceiptDetail(Signature):
    cid = models.CharField(max_length=20, default='')
    trans_id = models.IntegerField(default=0)
    trans_sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    segment_id = models.IntegerField(default=0)
    segment_name = models.CharField(max_length=50, blank=True, null=True)
    brand_id = models.IntegerField(default=0)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    collection = models.FloatField(default=0)
    money_receipt = models.FloatField(default=0)
    adv_receipt = models.FloatField(default=0)
    short_receipt = models.FloatField(default=0)
    adv_adj = models.FloatField(default=0)
    adj_plus = models.FloatField(default=0)
    adj_minus = models.FloatField(default=0)
    mr_reverse = models.FloatField(default=0)

    class Meta:
        db_table = 'tr_receipt_d'
        managed = False


class TrBchargeHead(Signature):
    cid = models.CharField(max_length=20, default='')
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'tr_bcharge_h'
        managed = False


class TrBchargeDetail(Signature):
    cid = models.CharField(max_length=20, default='')
    trans_id = models.IntegerField(default=0)
    trans_sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    bank_id = models.IntegerField(default=0)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(default=0)

    class Meta:
        db_table = 'tr_bcharge_d'
        managed = False


class TrPettyCashHead(Signature):
    cid = models.CharField(max_length=20, default='')
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    total_receipt_hq = models.FloatField(default=0)
    transfer_imprest_cash = models.FloatField(default=0)
    m_receipt = models.FloatField(default=0)
    total_expense_cq = models.FloatField(default=0)
    total_exp = models.FloatField(default=0)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'tr_petty_cash_h'
        managed = False

class TrDepositHead(Signature):
    cid = models.CharField(max_length=20, default='')
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'tr_deposit_h'
        managed = False


class TrDepositDetail(Signature):
    cid = models.CharField(max_length=20, default='')
    trans_id = models.IntegerField(default=0)
    trans_sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    segment_id = models.IntegerField(default=0)
    segment_name = models.CharField(max_length=50, blank=True, null=True)
    brand_id = models.IntegerField(default=0)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    bank_id = models.IntegerField(default=0)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(default=0)

    class Meta:
        db_table = 'tr_deposit_d'
        managed = False


class TrOsReconHead(Signature):
    cid = models.CharField(max_length=20, default='')
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    total_sales = models.FloatField(default=0)
    total_return = models.FloatField(default=0)
    total_net_sales = models.FloatField(default=0)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'tr_os_recon_h'
        managed = False


class TrOsReconDetail(Signature):
    cid = models.CharField(max_length=20, default='')
    trans_id = models.IntegerField(default=0)
    trans_sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    segment_id = models.IntegerField(default=0)
    segment_name = models.CharField(max_length=50, blank=True, null=True)
    brand_id = models.IntegerField(default=0)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    sales_tp = models.FloatField(default=0)
    sales_vat = models.FloatField(default=0)
    sales_discount = models.FloatField(default=0)
    sales_sp_disc = models.FloatField(default=0)
    sales_total = models.FloatField(default=0)
    return_tp = models.FloatField(default=0)
    return_vat = models.FloatField(default=0)
    return_discount = models.FloatField(default=0)
    return_sp_disc = models.FloatField(default=0)
    return_total = models.FloatField(default=0)
    net_sales_tp = models.FloatField(default=0)
    net_sales_vat = models.FloatField(default=0)
    net_sales_discount = models.FloatField(default=0)
    net_sales_sp_disc = models.FloatField(default=0)
    net_sales_total = models.FloatField(default=0)
    op_out = models.FloatField(default=0)
    close_out = models.FloatField(default=0)
    pdf = models.FloatField(default=0)
    as_sales = models.FloatField(default=0)

    class Meta:
        db_table = 'tr_os_recon_d'
        managed = False


class TrImprBnkHead(Signature):
    cid = models.CharField(max_length=20, default='')
    sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_code = models.CharField(max_length=50, blank=True, null=True)
    bank_id = models.IntegerField(default=0)
    account_number = models.CharField(max_length=20, default='0')  # original default=0 on a string field — kept as string '0'
    opening_balance = models.FloatField(default=0)
    bank_interest = models.FloatField(default=0)
    bank_charge = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0)
    closing_per_bank = models.FloatField(default=0)
    closing_per_bank_book = models.FloatField(default=0)
    preparation_date = models.DateField(blank=True, null=True)
    trans_date = models.DateField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    month = models.CharField(max_length=10, blank=True, null=True)
    approve = models.IntegerField(default=0)
    approve_by = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'tr_impr_bnk_h'
        managed = False


class TrImprBnkDetail(Signature):
    cid = models.CharField(max_length=20, default='')
    trans_id = models.IntegerField(default=0)
    trans_sl = models.CharField(max_length=50, blank=True, null=True)
    branch_id = models.IntegerField(default=0)
    branch_code = models.CharField(max_length=50, blank=True, null=True)
    bank_id = models.IntegerField(default=0)
    account_number = models.CharField(max_length=20, default='0')
    entry_date = models.DateField(blank=True, null=True)
    amount = models.FloatField(default=0)
    types = models.CharField(max_length=255, blank=True, null=True)  # pydal 'string' with no length = unbounded; Django CharField requires max_length, adjust as needed or use TextField
    ref_no = models.CharField(max_length=255, default='0')
    trans_date = models.DateField(blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    month = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'tr_impr_bnk_d'
        managed = False



class UsersBranch(Signature):
    cid = models.CharField(
        max_length=20,
        default=''
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='branch_profile'
    )

    branches = models.ManyToManyField(
        Branch,
        blank=True,
        related_name='users'
    )

    class Meta:
        db_table = "users_branch"

# class UserProfile(models.Model):
#     cid = models.CharField(max_length=20)
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='profile'
#     )


#     branches = models.ManyToManyField(
#         Branch,
#         blank=True,
#         related_name='user_profiles'
#     )

#     def __str__(self):
#         return self.user.username


