from random import random
from importlib import _bootstrap_external
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import Branch, Brand, OpeningHead, OpeningDetail
from cashier.common_fn import get_sl
from itertools import groupby
from operator import attrgetter
from django.db.models import Sum

@login_required
def index(request):
    return render(request, 'opening_amount/index.html')


@login_required
def create(request):
    rows = Brand.objects.all().order_by('segment__name', 'name').select_related('segment')

    branch_ids = request.session.get('branchList')
    branch_qs = Branch.objects.filter(status=1)

    if request.session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            branch_qs = branch_qs.filter(id__in=branch_ids)

    branchList = branch_qs

    # Build the grouped structure here, in Python
    segments = []
    for segment_name, brand_iter in groupby(rows, key=attrgetter('segment.name')):
        segments.append({
            'segment_name': segment_name,
            'brands': list(brand_iter),
        })

    context = {
        'segments': segments,
        'branchList': branchList,
    }
    return render(request, 'opening_amount/create.html', context)


@login_required
def submit(request):
    if request.method == 'POST':       

        transaction_date = request.POST.get('transaction_date', '').strip()
        transaction_year, transaction_month, _ = transaction_date.split('-')

        months_map = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12
        }

        if transaction_month.isdigit():
            month_number = int(transaction_month)
        else:
            month_number = months_map[transaction_month.lower()]

        branch_name = request.POST.get('branch_name', '').strip()
        opening_balance = request.POST.get('opening_balance', '').strip()
        cash_amount_pc = request.POST.get('cash_amount_pc', '').strip()
        bank_amount_pc = request.POST.get('bank_amount_pc', '').strip()

        if 'brand_name' not in request.POST or request.POST.get('brand_name') == "":
            brand_name = []
        else:
            # getlist handles both single and multi-value form fields cleanly
            brand_name = request.POST.getlist('brand_name')

        collection = []
        outstanding = []
        for i in brand_name:
            values = request.POST.getlist(f'collection_{i}')
            collection_values = ",".join(str(v) for v in values) if len(values) > 1 else (values[0] if values else None)
            collection.append(collection_values)

            values = request.POST.getlist(f'outstanding_{i}')
            outstanding_values = ",".join(str(v) for v in values) if len(values) > 1 else (values[0] if values else None)
            outstanding.append(outstanding_values)

        errors = []
        branchRecord = None
        if not transaction_date:
            errors.append('Enter transaction date')
        elif not branch_name:
            errors.append('Enter branch name')
        elif not opening_balance:
            errors.append('Enter opening balance')
        else:
            record_exists = OpeningHead.objects.filter(
                branch_id=branch_name, trans_date=transaction_date
            ).exists()
            if record_exists:
                errors.append('Record already exist')

            branchRecord = Branch.objects.filter(id=branch_name).first()

        if errors:
            msg = ' '.join(errors)  # 'rdrdrd' separator dropped — join with space or your preferred delimiter
            messages.warning(request, msg)
            return redirect('cashier:opening_amount-create')
            
        sl = get_sl()
        head = OpeningHead.objects.create(
            sl=branchRecord.name[:3].upper() + '-' + sl,
            branch_id=branchRecord.id,
            branch_name=branchRecord.name,
            trans_date=transaction_date,
            opening_balance=opening_balance,
            pc_cash_amount=cash_amount_pc,
            pc_bank_amount=bank_amount_pc,
            year=transaction_year,
            month=month_number,
        )

        date_wise_opening_amount = []
        for index in range(len(brand_name)):
            brandRecord = Brand.objects.filter(id=brand_name[index]).first()
            date_wise_opening_amount.append(OpeningDetail(
                trans_id=head.id,
                trans_sl=branchRecord.name[:3].upper() + '-' + sl,
                branch_id=branchRecord.id,
                branch_name=branchRecord.name,
                trans_date=transaction_date,
                segment_id=brandRecord.segment_id,
                segment_name=brandRecord.segment.name if brandRecord and brandRecord.segment else '',
                brand_id=brand_name[index],
                brand_name=brandRecord.name,
                collection=collection[index] if index < len(collection) else 0,
                outstanding=outstanding[index] if index < len(outstanding) else 0,
                pc_cash_amount=cash_amount_pc,
                pc_bank_amount=bank_amount_pc,
                year=transaction_year,
                month=transaction_month,
            ))

        if date_wise_opening_amount:
            OpeningDetail.objects.bulk_create(date_wise_opening_amount)

        messages.success(request, 'Opening amount added successfully')
    return redirect('cashier:opening_amount-index')

from collections import OrderedDict
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from cashier.models import OpeningHead, OpeningDetail, Brand, Branch


from collections import OrderedDict
from decimal import Decimal, InvalidOperation


def to_decimal(value):
    if value is None or value == '':
        return Decimal('0.00')

    try:
        return Decimal(str(value))
    except (ValueError, TypeError, InvalidOperation):
        return Decimal('0.00')


@login_required
def edit(request):

    request_id = request.GET.get('id')

    if not request_id:
        messages.error(request, 'Opening Amount ID is missing.')
        return redirect('cashier:opening_amount-index')

    record = get_object_or_404(
        OpeningHead,
        id=request_id
    )

    # Opening Details
    record_details = OpeningDetail.objects.filter(
        trans_id=record.id
    )

    # Detail Map
    detail_map = {}

    for detail in record_details:

        key = (
            detail.segment_id,
            detail.brand_id
        )

        detail_map[key] = {
            'collection': to_decimal(detail.collection),
            'outstanding': to_decimal(detail.outstanding),
        }


    # Brand List
    brands = Brand.objects.select_related(
        'segment'
    ).order_by(
        'segment__name',
        'name'
    )


    # Segment Grouping
    segments = OrderedDict()

    grand_collection = Decimal('0.00')
    grand_outstanding = Decimal('0.00')


    for brand in brands:

        segment_name = (
            brand.segment.name
            if brand.segment
            else 'No Segment'
        )

        segment_id = brand.segment_id


        # Get detail
        detail = detail_map.get(
            (segment_id, brand.id),
            {
                'collection': Decimal('0.00'),
                'outstanding': Decimal('0.00'),
            }
        )


        # নিশ্চিত করুন Decimal
        collection = to_decimal(detail.get('collection'))
        outstanding = to_decimal(detail.get('outstanding'))


        # Create Segment
        if segment_name not in segments:

            segments[segment_name] = {
                'collection': Decimal('0.00'),
                'outstanding': Decimal('0.00'),
                'brands': []
            }


        # Segment Total
        segments[segment_name]['collection'] += collection

        segments[segment_name]['outstanding'] += outstanding


        # Grand Total
        grand_collection += collection

        grand_outstanding += outstanding


        # Brand Data
        segments[segment_name]['brands'].append({
            'id': brand.id,
            'name': brand.name,
            'segment_id': segment_id,
            'collection': collection,
            'outstanding': outstanding,
        })


    # Convert to Template-friendly List
    segment_list = []

    for segment_name, data in segments.items():

        segment_list.append({
            'name': segment_name,
            'collection': data['collection'],
            'outstanding': data['outstanding'],
            'brands': data['brands'],
        })


    # Branch List
    branch_ids = request.session.get('branchList')
    role = request.session.get('role')

    branch_query = Branch.objects.filter(status=1)

    if role != 'super_admin' and branch_ids:

        if isinstance(branch_ids, str):

            branch_ids = [
                int(b.strip())
                for b in branch_ids.split(',')
                if b.strip().isdigit()
            ]

        elif isinstance(branch_ids, list):

            branch_ids = [
                int(b)
                for b in branch_ids
                if str(b).strip().isdigit()
            ]

        if branch_ids:

            branch_query = branch_query.filter(
                id__in=branch_ids
            )


    context = {
        'record': record,
        'segment_list': segment_list,
        'branchList': branch_query,
        'grand_collection': grand_collection,
        'grand_outstanding': grand_outstanding,
    }

    return render(
        request,
        'opening_amount/edit.html',
        context
    )

from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction


def to_decimal(value):
    if value is None or value == '':
        return Decimal('0.00')

    try:
        return Decimal(str(value))
    except (ValueError, TypeError, InvalidOperation):
        return Decimal('0.00')


@login_required
def update(request):

    if request.method != 'POST':
        return redirect('cashier:opening_amount-index')

    cid = request.session.get('cid')
    request_id = request.GET.get('id')

    if not request_id:
        messages.warning(request, 'Opening Amount ID is missing.')
        return redirect('cashier:opening_amount-index')

    # গুরুত্বপূর্ণ:
    # cid mismatch-এর কারণে 404 হচ্ছিল
    record = get_object_or_404(
        OpeningHead,
        id=request_id
    )

    # =========================
    # POST DATA
    # =========================

    transaction_date = request.POST.get(
        'transaction_date', ''
    ).strip()

    branch_name = request.POST.get(
        'branch_name', ''
    ).strip()

    opening_balance = request.POST.get(
        'opening_balance', ''
    ).strip()

    cash_amount_pc = request.POST.get(
        'cash_amount_pc', ''
    ).strip()

    bank_amount_pc = request.POST.get(
        'bank_amount_pc', ''
    ).strip()

    # =========================
    # DATE VALIDATION
    # =========================

    if not transaction_date:
        messages.warning(request, 'Enter transaction date')
        return redirect(
            f"{reverse('cashier:opening_amount-edit')}?id={request_id}"
        )

    try:
        transaction_year, transaction_month, transaction_day = (
            transaction_date.split('-')
        )
    except ValueError:
        messages.warning(
            request,
            'Invalid transaction date format. Use YYYY-MM-DD.'
        )
        return redirect(
            f"{reverse('cashier:opening_amount-edit')}?id={request_id}"
        )

    months_map = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    if transaction_month.isdigit():
        month_number = int(transaction_month)
    else:
        month_number = months_map.get(
            transaction_month.lower()
        )

    # =========================
    # BRAND LIST
    # =========================

    brand_name = request.POST.getlist('brand_name')

    collection = []
    outstanding = []

    for brand_id in brand_name:

        collection_value = request.POST.get(
            f'collection_{brand_id}',
            '0'
        )

        outstanding_value = request.POST.get(
            f'outstanding_{brand_id}',
            '0'
        )

        collection.append(
            to_decimal(collection_value)
        )

        outstanding.append(
            to_decimal(outstanding_value)
        )

    # =========================
    # VALIDATION
    # =========================

    errors = []

    if not branch_name:
        errors.append('Enter branch name')

    if not opening_balance:
        errors.append('Enter opening balance')

    if errors:
        messages.warning(request, ' '.join(errors))

        return redirect(
            f"{reverse('cashier:opening_amount-edit')}?id={request_id}"
        )

    # =========================
    # DUPLICATE CHECK
    # =========================

    duplicate_query = OpeningHead.objects.filter(
        branch_id=branch_name,
        trans_date=transaction_date
    ).exclude(
        id=record.id
    )

    # cid থাকলে cid দিয়েও check করুন
    if cid:
        duplicate_query = duplicate_query.filter(
            cid=cid
        )

    if duplicate_query.exists():

        messages.warning(
            request,
            'Record already exists'
        )

        return redirect(
            f"{reverse('cashier:opening_amount-edit')}?id={request_id}"
        )

    # =========================
    # BRANCH RECORD
    # =========================

    branchRecord = Branch.objects.filter(
        id=branch_name
    ).first()

    if not branchRecord:

        messages.warning(
            request,
            'Invalid branch selected'
        )

        return redirect(
            f"{reverse('cashier:opening_amount-edit')}?id={request_id}"
        )

    # =========================
    # SAVE
    # =========================

    with transaction.atomic():

        # Old Data
        old_date_wise_opening_amount = {
            'branch_id': record.branch_id,
            'branch_name': record.branch_name,
            'trans_date': str(record.trans_date),
            'opening_balance': str(record.opening_balance),
            'pc_cash_amount': str(record.pc_cash_amount),
            'pc_bank_amount': str(record.pc_bank_amount),
        }

        # Update Header
        record.branch_id = branch_name
        record.branch_name = branchRecord.name
        record.trans_date = transaction_date
        record.opening_balance = to_decimal(opening_balance)
        record.pc_cash_amount = to_decimal(cash_amount_pc)
        record.pc_bank_amount = to_decimal(bank_amount_pc)
        record.year = transaction_year
        record.month = month_number
        record.note = str(old_date_wise_opening_amount)

        record.save()

        # পুরোনো Detail Delete
        OpeningDetail.objects.filter(
            trans_id=record.id
        ).delete()

        # New Detail প্রস্তুত
        date_wise_opening_amount = []

        for index, brand_id in enumerate(brand_name):

            brandRecord = Brand.objects.filter(
                id=brand_id
            ).select_related(
                'segment'
            ).first()

            if not brandRecord:
                continue

            date_wise_opening_amount.append(
                OpeningDetail(
                    cid=record.cid,
                    trans_id=record.id,
                    trans_sl=record.sl,

                    branch_id=branchRecord.id if False else branchRecord.id,
                    branch_name=branchRecord.name,

                    trans_date=transaction_date,

                    segment_id=brandRecord.segment_id or 0,
                    segment_name=(
                        brandRecord.segment.name
                        if brandRecord.segment
                        else ''
                    ),

                    brand_id=brandRecord.id,
                    brand_name=brandRecord.name,

                    collection=(
                        collection[index]
                        if index < len(collection)
                        else Decimal('0.00')
                    ),

                    outstanding=(
                        outstanding[index]
                        if index < len(outstanding)
                        else Decimal('0.00')
                    ),

                    pc_cash_amount=to_decimal(cash_amount_pc),
                    pc_bank_amount=to_decimal(bank_amount_pc),

                    year=transaction_year,
                    month=month_number,
                )
            )

        # Bulk Create
        if date_wise_opening_amount:

            OpeningDetail.objects.bulk_create(
                date_wise_opening_amount
            )

    messages.success(
        request,
        'Record updated successfully'
    )

    return redirect(
        'cashier:opening_amount-index'
    )


@login_required
def delete(request):
    cid = request.session.get('cid')
    request_id = request.GET.get('id')
    if request_id:
        OpeningHead.objects.filter(id=request_id, cid=cid).delete()
        OpeningDetail.objects.filter(trans_id=request_id, cid=cid).delete()
        messages.error(request, 'Record Delete successfully')
        return redirect('cashier:opening_amount-index')

    return redirect('cashier:opening_amount-index')

@login_required
# Only real OpeningH fields can be used for DB-level ordering.
# segment_name/brand_name/collection/outstanding live on OpeningD (per-detail-row),
# so they can't be ordered at the header level without changing what "one row" means.



def get_data(request):
    # 🔍 Filtering
    role = request.session.get('role')
    queryset = OpeningHead.objects.all()
    ALLOWED_SORT_COLUMNS = {
        'id', 'sl', 'branch_id', 'branch_name', 'trans_date',
        'status', 'opening_balance', 'pc_bank_amount', 'pc_cash_amount',
    }
    if role != 'super_admin':
        branch_list = request.session.get('branchList')  # already a list
        if branch_list:
            branch_id_list = [str(b).strip() for b in branch_list if str(b).strip()]
            if branch_id_list:
                queryset = queryset.filter(branch_id__in=branch_id_list)

    name = request.GET.get('name')
    status = request.GET.get('status')

    if name:
        queryset = queryset.filter(branch_id=name)
    if status:
        queryset = queryset.filter(status=status)

    # 📊 Total rows
    total_rows = queryset.count()

    # 🔽 Ordering
    sort_column_index = request.GET.get('order[0][column]', 0)
    sort_column_name = request.GET.get(f'columns[{sort_column_index}][data]', 'id')
    sort_direction = request.GET.get('order[0][dir]', 'desc')

    if sort_column_name not in ALLOWED_SORT_COLUMNS:
        sort_column_name = 'id'
    if sort_direction == 'desc':
        sort_column_name = '-' + sort_column_name

    queryset = queryset.order_by(sort_column_name)

    # 📄 Pagination (after ordering)
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 16))

    if length == -1:
        data_qs = queryset
    else:
        data_qs = queryset[start:start + length]

    # 📦 Data convert (aggregate related opening_d rows per header)
    data = []
    for h in data_qs:
        details = OpeningDetail.objects.filter(trans_id=h.id)
        agg = details.aggregate(
            collection=Sum('collection'),
            outstanding=Sum('outstanding'),
        )
        first_detail = details.first()  # mirrors the old MySQL "any value" GROUP BY behavior

        data.append({
            'id':              h.id,
            'sl':              h.sl,
            'branch_id':       h.branch_id,
            'branch_name':     h.branch_name,
            'trans_date':      h.trans_date,
            'status':          h.status,
            'segment_name':    first_detail.segment_name if first_detail else None,
            'brand_name':      first_detail.brand_name if first_detail else None,
            'collection':      agg['collection'] or 0,
            'outstanding':     agg['outstanding'] or 0,
            'opening_balance': h.opening_balance,
            'pc_bank_amount':  h.pc_bank_amount,
            'pc_cash_amount':  h.pc_cash_amount,
        })

    return JsonResponse({
        'data': data,
        'recordsTotal': total_rows,
        'recordsFiltered': total_rows,
    })