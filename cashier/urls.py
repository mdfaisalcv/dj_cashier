from django.urls import path
from .controllers import login, dashboard, segment, default, branch, bank, bank_account, brand, opening_amount, open_date, user, migration_data

app_name = 'cashier'

urlpatterns = [
    path('', login.index, name='login'),
    path('login/logout', login.logout, name='logout'),
    path('dashboard/index', dashboard.index, name='dashboard'),  

    # Branch
    path('branch/index', branch.index, name='branch-index'),
    path('branch/create', branch.create, name='branch-create'),
    path('branch/edit', branch.edit, name='branch-edit'),
    path('branch/submit', branch.submit, name='branch-submit'),
    path('branch/update', branch.update, name='branch-update'),
    path('branch/delete', branch.delete, name='branch-delete'),
    path('branch/get_data', branch.get_data, name='branch-get_data'),
    
    # Default/Ajax stubs
    path('default/get_branch', default.get_branch, name='get_branch'),
    path('default/get_branch_code', default.get_branch_code, name='get_branch_code'),
    path('default/get_branch_name', default.get_branch_name, name='get_branch_name'),


    # Bank
    path('bank/index', bank.index, name='bank-index'),
    path('bank/create', bank.create, name='bank-create'),
    path('bank/edit', bank.edit, name='bank-edit'),
    path('bank/submit', bank.submit, name='bank-submit'),
    path('bank/update', bank.update, name='bank-update'),
    path('bank/delete', bank.delete, name='bank-delete'),
    path('bank/get_data', bank.get_data, name='bank-get_data'),
    
    # Default/Ajax stubs
    path('default/get_bank', default.get_bank, name='get_bank'),

    # Bank Account
    path('bank_account/index', bank_account.index, name='bank_account-index'),
    path('bank_account/create', bank_account.create, name='bank_account-create'),
    path('bank_account/edit', bank_account.edit, name='bank_account-edit'),
    path('bank_account/submit', bank_account.submit, name='bank_account-submit'),
    path('bank_account/update', bank_account.update, name='bank_account-update'),
    path('bank_account/delete', bank_account.delete, name='bank_account-delete'),
    path('bank_account/get_data', bank_account.get_data, name='bank_account-get_data'),

    # Default/Ajax stubs
    path('default/get_bank_account', default.get_bank_account, name='get_bank_account'),
    path('default/get_banks_by_branch', default.get_banks_by_branch, name='get_banks_by_branch'),

    # Segment
    path('segment/index', segment.index, name='segment-index'),
    path('segment/create', segment.create, name='segment-create'),
    path('segment/edit', segment.edit, name='segment-edit'),
    path('segment/submit', segment.submit, name='segment-submit'),
    path('segment/update', segment.update, name='segment-update'),
    path('segment/delete', segment.delete, name='segment-delete'),
    path('segment/get_data', segment.get_data, name='segment-get_data'),
    
    # Default/Ajax stubs
    path('default/get_segment', default.get_segment, name='get_segment'),

    # Brand
    path('brand/index', brand.index, name='brand-index'),
    path('brand/create', brand.create, name='brand-create'),
    path('brand/edit', brand.edit, name='brand-edit'),
    path('brand/submit', brand.submit, name='brand-submit'),
    path('brand/update', brand.update, name='brand-update'),
    path('brand/delete', brand.delete, name='brand-delete'),
    path('brand/get_data', brand.get_data, name='brand-get_data'),

    # Default/Ajax stubs
    path('default/get_brand_code', default.get_brand_code, name='get_brand_code'),
    path('default/get_brand_name', default.get_brand_name, name='get_brand_name'),

    # Opening amount
    path('opening_amount/index', opening_amount.index, name='opening_amount-index'),
    path('opening_amount/create', opening_amount.create, name='opening_amount-create'),
    path('opening_amount/edit', opening_amount.edit, name='opening_amount-edit'),
    path('opening_amount/submit', opening_amount.submit, name='opening_amount-submit'),
    path('opening_amount/update', opening_amount.update, name='opening_amount-update'),
    path('opening_amount/delete', opening_amount.delete, name='opening_amount-delete'),
    path('opening_amount/get_data', opening_amount.get_data, name='opening_amount-get_data'),

    # Open Date
    path('open_date/index', open_date.index, name='open_date-index'),
    path('open_date/create', open_date.create, name='open_date-create'),
    path('open_date/edit', open_date.edit, name='open_date-edit'),
    path('open_date/submit', open_date.submit, name='open_date-submit'),
    path('open_date/update', open_date.update, name='open_date-update'),
    path('open_date/delete', open_date.delete, name='open_date-delete'),
    path('open_date/get_data', open_date.get_data, name='open_date-get_data'),

    # Default/Ajax stubs
    path('default/get_user_name', default.get_user_name, name='get_user_name'),

    # User
    path('user/index', user.index, name='user-index'),
    path('user/create', user.create, name='user-create'),
    path('user/submit', user.submit, name='user-submit'),
    path('user/get_data', user.get_data, name='user-get_data'),



    # Migration
    # path(
    #     "migration_data/submit",
    #     migration_data.submit,
    #     name="migration_submit"
    # ),

    path(
        "migration_data/branch",
        migration_data.branch,
        name="migration_branch"
    ),

    path(
        "migration_data/bank",
        migration_data.bank,
        name="migration_bank"
    ),

    path(
        "migration_data/branch_bank",
        migration_data.branch_bank,
        name="migration_branch_bank"
    ),

    path(
        "migration_data/bank_account",
        migration_data.bank_account,
        name="migration_bank_account"
    ),

    path(
        "migration_data/segment",
        migration_data.segment,
        name="migration_segment"
    ),

    path(
        "migration_data/brand",
        migration_data.brand,
        name="migration_brand"
    ),

    path(
        "migration_data/brand_branch",
        migration_data.brand_branch,
        name="migration_brand_branch"
    ),

    path(
        "migration_data/opening_amount_head",
        migration_data.opening_amount_head,
        name="migration_opening_amount_head"
    ),

    path(
        "migration_data/opening_amount_details",
        migration_data.opening_amount_details,
        name="migration_opening_amount_details"
    ),

    path(
        "migration_data/user",
        migration_data.user,
        name="migration_user"
    ),

    path(
        "migration_data/user_branch",
        migration_data.user_branch,
        name="migration_user_branch"
    ),

    path(
        "migration_data/date_wise_receipt",
        migration_data.date_wise_receipt,
        name="migration_date_wise_receipt"
    ),

    path(
        "migration_data/date_wise_receipt_details",
        migration_data.date_wise_receipt_details,
        name="migration_date_wise_receipt_details"
    ),

    path(
        "migration_data/bank_charge_head",
        migration_data.bank_charge_head,
        name="migration_bank_charge_head"
    ),

    path(
        "migration_data/bank_charge_details",
        migration_data.bank_charge_details,
        name="migration_bank_charge_details"
    ),

    path(
        "migration_data/petty_cash_head",
        migration_data.petty_cash_head,
        name="migration_petty_cash_head"
    ),

    path(
        "migration_data/deposit_head",
        migration_data.deposit_head,
        name="migration_deposit_head"
    ),

    path(
        "migration_data/deposit_details",
        migration_data.deposit_details,
        name="migration_deposit_details"
    ),

    path(
        "migration_data/os_reconciliation_head",
        migration_data.os_reconciliation_head,
        name="migration_os_reconciliation_head"
    ),

    path(
        "migration_data/os_reconciliation_details",
        migration_data.os_reconciliation_details,
        name="migration_os_reconciliation_details"
    ),

    path(
        "migration_data/imprest_bank_recon_head",
        migration_data.imprest_bank_recon_head,
        name="migration_imprest_bank_recon_head"
    ),

    path(
        "migration_data/imprest_bank_recon_details",
        migration_data.imprest_bank_recon_details,
        name="migration_imprest_bank_recon_details"
    ),

    
]
