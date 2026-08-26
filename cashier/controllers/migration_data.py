from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.db import connections, transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from cashier.models import (Branch,Bank, BranchBank,BankAccount,Segment, Brand,BrandBranch,OpeningHead,OpeningDetail,User, UsersBranch,TrReceiptHead,TrReceiptDetail,TrBchargeHead, TrBchargeDetail,TrPettyCashHead,TrDepositHead, TrDepositDetail,TrOsReconHead,TrOsReconDetail, TrImprBnkHead,TrImprBnkDetail)


# =========================================================
# Common Helper Functions
# =========================================================

def source_query(sql, params=None):
    """
    Read data from old/source database.
    Database alias: source_db
    """

    with connections["source_db"].cursor() as cursor:
        cursor.execute(sql, params or [])

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def safe(value, default=""):
    return default if value is None else value


def safe_zero(value):
    return 0 if value is None else value


def safe_datetime(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    return value


def safe_decimal(value):
    if value is None:
        return Decimal("0")

    if isinstance(value, Decimal):
        return value

    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def migration_response(message, count=0, data=None):
    response = {
        "status": "success",
        "message": message,
        "count": count,
    }

    if data is not None:
        response["data"] = data

    return JsonResponse(
        response,
        safe=False
    )


def bulk_insert(model, objects, batch_size=1000):
    """
    Bulk insert into Django database.
    """

    if not objects:
        return 0

    with transaction.atomic():
        model.objects.bulk_create(
            objects,
            batch_size=batch_size
        )

    return len(objects)


# =========================================================
# Submit / Test
# =========================================================

# @require_http_methods(["GET", "POST"])
# def submit(request):

#     str_vl = request.POST.get(
#         "str_vl",
#         request.GET.get("str_vl", "")
#     )

#     LoadTest.objects.create(
#         str_vl=str_vl,
#         created_on=datetime.now()
#     )

#     return JsonResponse({
#         "status": "success",
#         "message": "Done"
#     })


# =========================================================
# Branch
# Source: branches
# Destination: branch
# =========================================================
@csrf_exempt
@require_http_methods(["POST"])
def branch(request):

    records = source_query("""
        SELECT *
        FROM branches
    """)

    objects = []

    for data in records:

        objects.append(
            Branch(
                id=data.get("id"),
                cid="CASHIER",

                code=data.get("code") or "",
                name=data.get("name") or "",
                short_name=data.get("short_name") or "",
                email=data.get("email") or "",
                address=data.get("address1") or "",

                status=data.get("status") or "",

                field1=data.get("field1") or "",
                field2=data.get("field2") or 0,
                note=data.get("note") or "",

                created_on=data.get("created_at"),
                created_by_id=None,

                updated_on=data.get("updated_at"),
                updated_by_id=None,
            )
        )

    count = bulk_insert(
        Branch,
        objects
    )

    return migration_response(
        "Branch migration completed",
        count
    )
# =========================================================
# Bank
# Source: banks
# Destination: bank
# =========================================================
@csrf_exempt
@require_http_methods(["GET", "POST"])
def bank(request):

    records = source_query("""
        SELECT *
        FROM banks
    """)

    objects = []

    for data in records:

        objects.append(
            Bank(
                id=data.get("id"),
                cid="CASHIER",

                name=data.get("name", "") or "",
                short_name=data.get("short_name", "") or "",
                address=data.get("address", "") or "",

                status=data.get("status", "") or "",

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", "") or "",

                created_on=data.get("created_at"),
                created_by_id=data.get("created_by") or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get("updated_by") or None,
            )
        )

    count = bulk_insert(
        Bank,
        objects
    )

    return migration_response(
        "Bank migration completed",
        count
    )


# =========================================================
# Branch Bank
# Source: branch_bank
# Destination: branch_bank
# =========================================================
@csrf_exempt
@require_http_methods(["GET", "POST"])
def branch_bank(request):

    records = source_query("""
        SELECT *
        FROM branch_bank
    """)

    objects = []

    for data in records:

        objects.append(
            BranchBank(
                id=data.get("id"),
                cid="CASHIER",

                branch_id=data.get("branch_id") or "",
                bank_id=data.get("bank_id") or "",

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", "") or "",

                created_on=data.get("created_at"),
                created_by_id=data.get("created_by") or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get("updated_by") or None,
            )
        )

    count = bulk_insert(
        BranchBank,
        objects
    )

    return migration_response(
        "Branch Bank migration completed",
        count
    )


# =========================================================
# Bank Account
# Source: bank_accounts
# Destination: bank_account
# =========================================================
@csrf_exempt
@require_http_methods(["GET", "POST"])
def bank_account(request):

    records = source_query("""
        SELECT *
        FROM bank_accounts
    """)

    objects = []

    for data in records:

        objects.append(
            BankAccount(
                id=data.get("id"),
                cid="CASHIER",

                branch_id=data.get("branch_id") or "",
                bank_id=data.get("bank_id") or "",

                account_number=data.get(
                    "account_number",
                    ""
                ),

                account_type=data.get(
                    "account_type",
                    ""
                ),

                status=data.get("status", "") or "",

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", "") or "",

                created_on=data.get("created_at"),
                created_by_id= None,

                updated_on=data.get("updated_at"),
                updated_by_id= None,
            )
        )

    count = bulk_insert(
        BankAccount,
        objects
    )

    return migration_response(
        "Bank Account migration completed",
        count
    )


# =========================================================
# Segment
# Source: brands
# Destination: segment
# =========================================================

def get_valid_user(user_id):
    if not user_id:
        return None

    return User.objects.filter(
        id=user_id
    ).first()

@csrf_exempt
@require_http_methods(["POST"])
def segment(request):

    records = source_query("""
        SELECT *
        FROM brands
    """)

    objects = []

    for data in records:

        objects.append(
            Segment(
                id=data.get("id"),
                cid="CASHIER",

                name=data.get("name", "") or "",

                status=data.get("status", "") or "",

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=get_valid_user(data.get("created_by")), 

                updated_on=data.get("updated_at"),
                updated_by_id=get_valid_user(data.get("updated_by")),
            )
        )

    count = bulk_insert(
        Segment,
        objects
    )

    return migration_response(
        "Segment migration completed",
        count
    )


# =========================================================
# Brand
# Source: products
# Destination: brand
# =========================================================

@csrf_exempt
@require_http_methods(["POST"])
def brand(request):

    records = source_query("""
        SELECT *
        FROM products
    """)

    objects = []

    for data in records:

        objects.append(
            Brand(
                id=data.get("id"),
                cid="CASHIER",

                name=data.get("name", "") or "",
                code=data.get("code", "") or "",
                short_name=data.get("short_name", "") or "",

                segment_id=data.get("brand_id") or 0,
                # segment_name=data.get("brand_name", "") or "",

                status=data.get("status", "") or "",

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", "") or "",

                created_on=data.get("created_at"),
                created_by_id=get_valid_user(data.get("created_by")),

                updated_on=data.get("updated_at"),
                updated_by_id=get_valid_user(data.get("updated_by")),
            )
        )

    count = bulk_insert(
        Brand,
        objects
    )

    return migration_response(
        "Brand migration completed",
        count
    )


# =========================================================
# Brand Branch
# Source: product_branch
# Destination: brand_branch
# =========================================================
@csrf_exempt
@require_http_methods(["POST"])
def brand_branch(request):

    records = source_query("""
        SELECT *
        FROM product_branch
    """)

    objects = []

    for data in records:

        objects.append(
            BrandBranch(
                id=data.get("id"),
                cid="CASHIER",

                brand_id=data.get("product_id") or 0,
                branch_id=data.get("branch_id") or 0,

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", "") or "",

                created_on=data.get("created_at"),
                created_by_id=get_valid_user(data.get("created_by")),

                updated_on=data.get("updated_at"),
                updated_by_id=get_valid_user(data.get("updated_by")),
            )
        )

    count = bulk_insert(
        BrandBranch,
        objects
    )

    return migration_response(
        "Brand Branch migration completed",
        count
    )


# =========================================================
# Opening Amount Head
# Source: setup_opening_summary
# Destination: opening_h
# =========================================================

@csrf_exempt
@require_http_methods(["POST"])
def opening_amount_head(request):

    records = source_query("""
        SELECT *
        FROM setup_opening_summary
    """)

    objects = []

    for data in records:

        objects.append(
            OpeningHead(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id") or 0,
                branch_name=data.get("branch_name") or "",

                trans_date=data.get("trans_date") or None,

                pc_bank_amount=safe_decimal(
                    data.get("pc_bank_amount")
                ) or 0,

                pc_cash_amount=safe_decimal(
                    data.get("pc_cash_amount")
                ) or 0,

                approve=data.get("approve") or 0,

                approve_by=data.get(
                    "approve_by"
                ) or "",

                year=data.get("year") or 0,
                month=data.get("month") or 0,
                status=data.get("status") or 0,

                field1=data.get("field1", "") or "",
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=get_valid_user(data.get(
                    "created_by"
                )),

                updated_on=data.get("updated_at"),
                updated_by_id=get_valid_user(data.get(
                    "updated_by"
                )),
            )
        )

    count = bulk_insert(
        OpeningHead,
        objects
    )

    return migration_response(
        "Opening Amount Head migration completed",
        count
    )


# =========================================================
# Opening Amount Details
# Source: setup_opening_details
# Destination: opening_d
# =========================================================
@csrf_exempt
@require_http_methods(["POST"])
def opening_amount_details(request):

    records = source_query("""
        SELECT *
        FROM setup_opening_details
    """)

    objects = []

    for data in records:

        objects.append(
            OpeningDetail(
                id=data.get("id"),
                cid="CASHIER",

                trans_id=data.get("trans_id") or 0,
                trans_sl=data.get("trans_sl") or 0,

                branch_id=data.get("branch_id") or 0,
                branch_name=data.get("branch_name") or "",

                trans_date=data.get("trans_date") or None,

                segment_id=data.get("brand_id") or 0,
                segment_name=data.get("brand_name") or "",

                brand_id=data.get("product_id") or 0,
                brand_name=data.get("product_name") or "",

                collection=safe_decimal(
                    data.get("collection")
                ) or 0,

                outstanding=safe_decimal(
                    data.get("outstanding")
                ) or 0,

                pc_bank_amount=safe_decimal(
                    data.get("pc_bank_amount")
                ) or 0,

                pc_cash_amount=safe_decimal(
                    data.get("pc_cash_amount")
                ) or 0,

                approve=data.get("approve") or 0,

                approve_by=data.get(
                    "approve_by"
                ) or None,

                year=data.get("year") or 0,
                month=data.get("month") or 0,
                status=data.get("status") or 0,

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=get_valid_user(data.get(
                    "created_by"
                )) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=get_valid_user(data.get(
                    "updated_by"
                )) or None,
            )
        )

    count = bulk_insert(
        OpeningDetail,
        objects
    )

    return migration_response(
        "Opening Amount Details migration completed",
        count
    )


# =========================================================
# User
# Source: users
# Destination: users
# =========================================================
@csrf_exempt
@require_http_methods(["POST"])
def user(request):

    records = source_query("""
        SELECT *
        FROM users
    """)

    objects = []

    # -----------------------------------------------
    # Get role mapping in ONE query
    # Instead of querying role_user for every user
    # -----------------------------------------------

    # role_records = source_query("""
    #     SELECT
    #         ru.user_id,
    #         r.name AS role_name
    #     FROM role_user ru
    #     LEFT JOIN roles r
    #         ON r.id = ru.role_id
    # """)

    role_map = {}

    # for row in role_records:
    #     role_map[
    #         str(row.get("user_id"))
    #     ] = row.get("role_name", "")

    for data in records:

        user_id = data.get("id")

        objects.append(
            User(
                id=user_id,
                # cid="CASHIER",

                first_name=data.get(
                    "first_name",
                    ""
                ),

                last_name=data.get(
                    "last_name",
                    ""
                ),

                username=data.get(
                    "username",
                    ""
                ),

                is_superuser=0,

                email=data.get(
                    "email",
                    ""
                ),

                password="12345678",

                # role=role_map.get(
                #     str(user_id),
                #     ""
                # ),

                is_staff=data.get(
                    "is_staff",
                    "1"
                ) or 1,

                is_active=data.get(
                    "is_active",
                    "1"
                ) or 1,

                date_joined=data.get(
                    "created_at"
                ),
                last_login=data.get(
                    "updated_at"
                ),
            )
        )

    count = bulk_insert(
        User,
        objects
    )

    return migration_response(
        "User migration completed",
        count
    )


# =========================================================
# User Branch
# Source: user_branch
# Destination: users_branch
# =========================================================

@require_http_methods(["GET", "POST"])
def user_branch(request):

    records = source_query("""
        SELECT *
        FROM user_branch
    """)

    objects = []

    for data in records:

        objects.append(
            UsersBranch(
                id=data.get("id"),
                cid="CASHIER",

                user_id=data.get("user_id"),
                branch_id=data.get("branch_id"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get("created_by") or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get("updated_by") or None,
            )
        )

    count = bulk_insert(
        UsersBranch,
        objects
    )

    return migration_response(
        "User Branch migration completed",
        count
    )


# =========================================================
# Date Wise Receipt Head
# Source: transactions_date_wise_summary
# Destination: tr_receipt_h
# =========================================================

@require_http_methods(["GET", "POST"])
def date_wise_receipt(request):

    records = source_query("""
        SELECT *
        FROM transactions_date_wise_summary
    """)

    objects = []

    for data in records:

        objects.append(
            TrReceiptH(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                approve=data.get("approve"),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get("status"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrReceiptH,
        objects
    )

    return migration_response(
        "Date Wise Receipt Head migration completed",
        count
    )


# =========================================================
# Date Wise Receipt Details
# Source: transactions_date_wise_details
# Destination: tr_receipt_d
# =========================================================

@require_http_methods(["GET", "POST"])
def date_wise_receipt_details(request):

    records = source_query("""
        SELECT *
        FROM transactions_date_wise_details
    """)

    objects = []

    for data in records:

        objects.append(
            TrReceiptD(
                id=data.get("id"),
                cid="CASHIER",

                trans_id=data.get("trans_id"),
                trans_sl=data.get("trans_sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                segment_id=data.get("brand_id"),
                segment_name=data.get("brand_name"),

                brand_id=data.get("product_id"),
                brand_name=data.get("product_name"),

                collection=safe_decimal(
                    data.get("collection")
                ),

                money_receipt=safe_decimal(
                    data.get("money_receipt")
                ),

                adv_receipt=safe_decimal(
                    data.get("adv_receipt")
                ),

                short_receipt=safe_decimal(
                    data.get("short_receipt")
                ),

                adv_adj=safe_decimal(
                    data.get("adv_adj")
                ),

                adj_plus=safe_decimal(
                    data.get("adj_plus")
                ),

                adj_minus=safe_decimal(
                    data.get("adj_minus")
                ),

                mr_reverse=safe_decimal(
                    data.get("mr_reverse")
                ),

                approve=data.get("approve"),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get("status"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrReceiptD,
        objects
    )

    return migration_response(
        "Date Wise Receipt Details migration completed",
        count
    )


# =========================================================
# Bank Charge Head
# Source: transactions_bank_charge_summary
# Destination: tr_bcharge_h
# =========================================================

@require_http_methods(["GET", "POST"])
def bank_charge_head(request):

    records = source_query("""
        SELECT *
        FROM transactions_bank_charge_summary
    """)

    objects = []

    for data in records:

        objects.append(
            TrBchargeH(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                approve=data.get("approve"),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get("status"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrBchargeH,
        objects
    )

    return migration_response(
        "Bank Charge Head migration completed",
        count
    )


# =========================================================
# Bank Charge Details
# Source: transactions_bank_charge_details
# Destination: tr_bcharge_d
# =========================================================

@require_http_methods(["GET", "POST"])
def bank_charge_details(request):

    records = source_query("""
        SELECT *
        FROM transactions_bank_charge_details
    """)

    objects = []

    for data in records:

        objects.append(
            TrBchargeD(
                id=data.get("id"),
                cid="CASHIER",

                trans_id=data.get("trans_id"),
                trans_sl=data.get("trans_sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                bank_id=data.get("bank_id"),
                bank_name=data.get("bank_name"),

                amount=safe_decimal(
                    data.get("amount")
                ),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrBchargeD,
        objects
    )

    return migration_response(
        "Bank Charge Details migration completed",
        count
    )


# =========================================================
# Petty Cash Head
# Source:
# transactions_petty_cash_summary
#
# Details:
# transactions_petty_cash_details
#
# Destination:
# tr_petty_cash_h
# =========================================================

@require_http_methods(["GET", "POST"])
def petty_cash_head(request):

    detail_records = source_query("""
        SELECT
            id,
            trans_id,
            SUM(total_receipt_hq) AS total_receipt_hq,
            SUM(transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(m_receipt) AS m_receipt,
            SUM(total_exp) AS total_exp,
            SUM(total_expense_cq) AS total_expense_cq
        FROM transactions_petty_cash_details
        GROUP BY trans_id
        ORDER BY id
    """)

    detail_map = {}

    for row in detail_records:

        detail_map[
            str(row.get("trans_id"))
        ] = {
            "id": row.get("id"),

            "total_receipt_hq": row.get(
                "total_receipt_hq"
            ),

            "transfer_imprest_cash": row.get(
                "transfer_imprest_cash"
            ),

            "m_receipt": row.get(
                "m_receipt"
            ),

            "total_exp": row.get(
                "total_exp"
            ),

            "total_expense_cq": row.get(
                "total_expense_cq"
            ),
        }

    records = source_query("""
        SELECT *
        FROM transactions_petty_cash_summary
    """)

    objects = []

    for data in records:

        details = detail_map.get(
            str(data.get("id")),
            {}
        )

        objects.append(
            TrPettyCashH(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                total_receipt_hq=safe_decimal(
                    details.get("total_receipt_hq")
                ),

                transfer_imprest_cash=safe_decimal(
                    details.get("transfer_imprest_cash")
                ),

                m_receipt=safe_decimal(
                    details.get("m_receipt")
                ),

                total_expense_cq=safe_decimal(
                    details.get("total_expense_cq")
                ),

                total_exp=safe_decimal(
                    details.get("total_exp")
                ),

                approve=data.get("approve"),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get("status"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrPettyCashH,
        objects
    )

    return migration_response(
        "Petty Cash Head migration completed",
        count
    )


# =========================================================
# Deposit Head
# Source: transactions_deposit_summary
# Destination: tr_deposit_h
# =========================================================

@require_http_methods(["GET", "POST"])
def deposit_head(request):

    records = source_query("""
        SELECT *
        FROM transactions_deposit_summary
    """)

    objects = []

    for data in records:

        objects.append(
            TrDepositH(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                approve=data.get("approve"),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get("status"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrDepositH,
        objects
    )

    return migration_response(
        "Deposit Head migration completed",
        count
    )


# =========================================================
# Deposit Details
# Source: transactions_deposit_details
# Destination: tr_deposit_d
# =========================================================

@require_http_methods(["GET", "POST"])
def deposit_details(request):

    records = source_query("""
        SELECT *
        FROM transactions_deposit_details
    """)

    objects = []

    for data in records:

        objects.append(
            TrDepositD(
                id=data.get("id"),
                cid="CASHIER",

                trans_id=data.get("trans_id"),
                trans_sl=data.get("trans_sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                segment_id=data.get("brand_id"),
                segment_name=data.get("brand_name"),

                brand_id=data.get("product_id"),
                brand_name=data.get("product_name"),

                bank_id=data.get("bank_id"),
                bank_name=data.get("bank_name"),

                amount=safe_decimal(
                    data.get("amount")
                ),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrDepositD,
        objects
    )

    return migration_response(
        "Deposit Details migration completed",
        count
    )


# =========================================================
# OS Reconciliation Head
# Source: transactions_os_reconciliation_summary
# Destination: tr_os_recon_h
# =========================================================

@require_http_methods(["GET", "POST"])
def os_reconciliation_head(request):

    records = source_query("""
        SELECT *
        FROM transactions_os_reconciliation_summary
    """)

    objects = []

    for data in records:

        objects.append(
            TrOsReconH(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                total_sales=safe_decimal(
                    data.get("total_sales")
                ),

                total_return=safe_decimal(
                    data.get("total_return")
                ),

                total_net_sales=safe_decimal(
                    data.get("total_net_sales")
                ),

                approve=data.get("approve"),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get("status"),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrOsReconH,
        objects
    )

    return migration_response(
        "OS Reconciliation Head migration completed",
        count
    )


# =========================================================
# OS Reconciliation Details
# Source: transactions_os_reconciliation_details
# Destination: tr_os_recon_d
# =========================================================

@require_http_methods(["GET", "POST"])
def os_reconciliation_details(request):

    records = source_query("""
        SELECT *
        FROM transactions_os_reconciliation_details
    """)

    objects = []

    for data in records:

        objects.append(
            TrOsReconD(
                id=data.get("id"),
                cid="CASHIER",

                trans_id=data.get("trans_id"),
                trans_sl=data.get("trans_sl"),

                branch_id=data.get("branch_id"),
                branch_name=data.get("branch_name"),

                trans_date=data.get("trans_date"),

                segment_id=data.get("brand_id"),
                segment_name=data.get("brand_name"),

                brand_id=data.get("product_id"),
                brand_name=data.get("product_name"),

                sales_tp=safe_decimal(
                    data.get("sales_tp")
                ),

                sales_vat=safe_decimal(
                    data.get("sales_vat")
                ),

                sales_discount=safe_decimal(
                    data.get("sales_discount")
                ),

                sales_sp_disc=safe_decimal(
                    data.get("sales_sp_disc")
                ),

                sales_total=safe_decimal(
                    data.get("sales_total")
                ),

                return_tp=safe_decimal(
                    data.get("return_tp")
                ),

                return_vat=safe_decimal(
                    data.get("return_vat")
                ),

                return_discount=safe_decimal(
                    data.get("return_discount")
                ),

                return_sp_disc=safe_decimal(
                    data.get("return_sp_disc")
                ),

                return_total=safe_decimal(
                    data.get("return_total")
                ),

                net_sales_tp=safe_decimal(
                    data.get("net_sales_tp")
                ),

                net_sales_vat=safe_decimal(
                    data.get("net_sales_vat")
                ),

                net_sales_discount=safe_decimal(
                    data.get("net_sales_discount")
                ),

                net_sales_sp_disc=safe_decimal(
                    data.get("net_sales_sp_disc")
                ),

                net_sales_total=safe_decimal(
                    data.get("net_sales_total")
                ),

                field1=data.get("field1", ""),
                field2=data.get("field2") or 0,
                note=data.get("note", ""),

                created_on=data.get("created_at"),
                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get("updated_at"),
                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrOsReconD,
        objects
    )

    return migration_response(
        "OS Reconciliation Details migration completed",
        count
    )


# =========================================================
# Imprest Bank Reconciliation Head
# Source: trns_impr_bnk_summary
# Destination: tr_impr_bnk_h
# =========================================================

@require_http_methods(["GET", "POST"])
def imprest_bank_recon_head(request):

    records = source_query("""
        SELECT *
        FROM trns_impr_bnk_summary
    """)

    objects = []

    for data in records:

        objects.append(
            TrImprBnkH(
                id=data.get("id"),
                cid="CASHIER",

                sl=data.get("sl"),

                branch_id=data.get("branch_id"),
                branch_code=data.get("branch_code"),

                bank_id=data.get("bank_id"),
                account_number=data.get("account_number"),

                opening_balance=safe_decimal(
                    data.get("opening_balance")
                ),

                bank_interest=safe_decimal(
                    data.get("bank_interest")
                ),

                bank_charge=safe_decimal(
                    data.get("bank_charge")
                ),

                closing_balance=safe_decimal(
                    data.get("closing_balance")
                ),

                closing_per_bank=safe_decimal(
                    data.get("closing_per_bank")
                ),

                closing_per_bank_book=safe_decimal(
                    data.get("closing_per_bank_book")
                ),

                preparation_date=data.get(
                    "preparation_date"
                ),

                trans_date=data.get(
                    "trans_date"
                ),

                approve=data.get(
                    "approve"
                ),

                approve_by_id=data.get(
                    "approve_by"
                ) or None,

                status=data.get(
                    "status"
                ),

                year=data.get(
                    "year"
                ),

                month=data.get(
                    "month"
                ),

                field1=data.get(
                    "field1",
                    ""
                ),

                field2=data.get(
                    "field2"
                ) or 0,

                note=data.get(
                    "note",
                    ""
                ),

                created_on=data.get(
                    "created_at"
                ),

                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get(
                    "updated_at"
                ),

                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrImprBnkH,
        objects
    )

    return migration_response(
        "Imprest Bank Reconciliation Head migration completed",
        count
    )


# =========================================================
# Imprest Bank Reconciliation Details
# Source: trns_impr_bnk_details
# Destination: tr_impr_bnk_d
# =========================================================

def get_imprest_type(value):

    type_map = {
        "1": "DEPOSITED_BUT_NOT_SHOW_BANK_BOOK",
        "2": "DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK",
        "3": "CHEQUE_ISSUED",
        "4": "DEPOSITED_OR_RECEIVED",
        "5": "LESS_CHECK_ISSUED",
        "6": "LESS_CHECK_ISSUED_CQ",
    }

    return type_map.get(
        str(value),
        ""
    )


@require_http_methods(["GET", "POST"])
def imprest_bank_recon_details(request):

    records = source_query("""
        SELECT *
        FROM trns_impr_bnk_details
    """)

    objects = []

    for data in records:

        objects.append(
            TrImprBnkD(
                id=data.get("id"),
                cid="CASHIER",

                trans_id=data.get(
                    "trans_id"
                ),

                trans_sl=data.get(
                    "trans_sl"
                ),

                branch_id=data.get(
                    "branch_id"
                ),

                branch_code=data.get(
                    "branch_code"
                ),

                bank_id=data.get(
                    "bank_id"
                ),

                account_number=data.get(
                    "account_number"
                ),

                entry_date=data.get(
                    "entry_date"
                ),

                amount=safe_decimal(
                    data.get("amount")
                ),

                types=get_imprest_type(
                    data.get("types")
                ),

                ref_no=data.get(
                    "ref_no"
                ),

                trans_date=data.get(
                    "trans_date"
                ),

                year=data.get(
                    "year"
                ),

                month=data.get(
                    "month"
                ),

                field1=data.get(
                    "field1",
                    ""
                ),

                field2=data.get(
                    "field2"
                ) or 0,

                note=data.get(
                    "note",
                    ""
                ),

                created_on=data.get(
                    "created_at"
                ),

                created_by_id=data.get(
                    "created_by"
                ) or None,

                updated_on=data.get(
                    "updated_at"
                ),

                updated_by_id=data.get(
                    "updated_by"
                ) or None,
            )
        )

    count = bulk_insert(
        TrImprBnkD,
        objects
    )

    return migration_response(
        "Imprest Bank Reconciliation Details migration completed",
        count
    )