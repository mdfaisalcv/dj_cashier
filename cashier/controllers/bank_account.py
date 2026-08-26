from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import BankAccount, Branch

@login_required
def index(request):
    return render(request, 'bank_account/index.html')

@login_required
def create(request):
    cid = request.session.get('cid')
    branch_ids = request.session.get('branchList')
    role = request.session.get('role')

    branches = Branch.objects.filter(cid=cid, status=1)

    if role != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            branches = branches.filter(id__in=branch_ids)
   
    return render(request, 'bank_account/create.html',{'branchList': branches})


@login_required
def submit(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        branch_name = request.POST.get('branch_name', '').strip()
        bank_name = request.POST.get('bank_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        status = request.POST.get('status')

        status = 1 if str(status) == "1" else 0

        errors = []
        if not branch_name:
            errors.append('Enter branch name')
        elif not bank_name:
            errors.append('Enter bank name')
        elif not account_number:
            errors.append('Enter account number')
        else:
            exists = BankAccount.objects.filter(
                cid=cid,
                branch_id=branch_name,
                bank_id=bank_name
            ).exists()
            if exists:
                errors.append('Bank name already exist')

        if errors:
            msg = '<br>'.join(errors)
            messages.warning(request, msg)
            return redirect('cashier:bank_account-create')

        BankAccount.objects.create(
            cid=cid,
            branch_id=branch_name,
            bank_id=bank_name,
            account_number=account_number,
            status=status
        )

    messages.success(request, 'Record added successfully')
    return redirect('cashier:bank_account-index') 


@login_required
def edit(request):
    cid = request.session.get('cid')
    request_id = request.GET.get('id')
    record = None
    branchList = []

    if request_id:
        record = get_object_or_404(BankAccount, id=request_id)

        role = request.session.get('role')
        branch_ids = request.session.get('branchList')
        branches = Branch.objects.filter(status=1)

        if role != 'super_admin' and branch_ids:
            if isinstance(branch_ids, str):
                branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
            elif isinstance(branch_ids, list):
                branch_ids = [int(b) for b in branch_ids if b]

            if branch_ids:
                branches = branches.filter(id__in=branch_ids)

        branchList = branches

    
    return render(request, 'bank_account/edit.html', {
        'record': record,
        'branchList': branchList,
    })


@login_required
def update(request):
    cid = request.session.get('cid')
    request_id = request.GET.get('id')
    record = get_object_or_404(BankAccount, id=request_id) if request_id else None
    if record is None:
        messages.warning(request, 'Record not found')
        return redirect('cashier:bank_account-index')

    if request.method == 'POST':
        branch_name = request.POST.get('branch_name', '').strip()
        bank_name = request.POST.get('bank_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        status = request.POST.get('status')

        status = 1 if str(status) == "1" else 0

        errors = []
        if branch_name == '':
            errors.append('Enter branch name')
        if bank_name == '':
            errors.append('Enter bank name')
        if account_number == '':
            errors.append('Enter account number')

        # Only run the duplicate-check query once we know all fields are populated
        if not errors:
            exists = BankAccount.objects.filter(
                cid=cid,
                branch_id=branch_name,
                bank_id=bank_name
            ).exclude(id=request_id).exists()
            if exists:
                errors.append('Bank name already exist')

        if errors:
            msg = '<br>'.join(errors)
            messages.warning(request, msg)
            return redirect("cashier:bank_account-edit?id=" + request_id)

        # snapshot old values for audit note
        old_bank = {
            'branch_id': record.branch_id,
            'bank_id': record.bank_id,
            'account_number': record.account_number,
            'status': record.status,
        }

        record.branch_id = branch_name
        record.bank_id = bank_name
        record.account_number = account_number
        record.status = status
        record.note = old_bank
        record.save()

        messages.success(request, 'Record updated successfully')
        return redirect('cashier:bank_account-index')

    return redirect('cashier:bank_account-index')

@login_required
def delete(request):
    request_id = request.GET.get('id')
    cid=request.session.get('cid')
    if request_id:
        get_object_or_404(BankAccount, id=request_id, cid=cid).delete()
        messages.error(request, 'Record Delete successfully')
    return redirect('cashier:bank_account-index')

@login_required
def get_data(request):
    cid=request.session.get('cid')
    qs = BankAccount.objects.select_related('branch', 'bank').filter(cid=cid).all()

    role = request.session.get('role')
    if role != 'super_admin':
        branch_id_session = request.session.get('branchList')
        if branch_id_session:
            branch_id_list = [str(c).strip() for c in branch_id_session if str(c).strip()]
            if branch_id_list:
                qs = qs.filter(branch__id__in=branch_id_list)

    branch_name = request.GET.get('branch_name')
    if branch_name:
        qs = qs.filter(branch__id=branch_name)

    bank_name = request.GET.get('bank_name')
    if bank_name:
        qs = qs.filter(bank__id=bank_name)

    account_number = request.GET.get('account_number')
    if account_number:
        qs = qs.filter(id=account_number)  # kept identical to original logic (see note below)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    total_rows = qs.count()

    # Pagination
    start_param = request.GET.get('start')
    length_param = request.GET.get('length')
    rows_per_page = int(length_param) if length_param else 16

    if rows_per_page == -1:
        rows_per_page = total_rows or 1

    start = int(start_param) if start_param else 0
    page_start = start
    page_end = start + rows_per_page

    # Ordering — whitelist allowed columns to prevent invalid/unsafe ordering
    allowed_sort_columns = {
        'id': 'id',
        'branch_name': 'branch_id__name',
        'bank_name': 'bank_id__name',
        'account_number': 'account_number',
        'status': 'status',
    }
    sort_column_index = request.GET.get('order[0][column]', '0')
    sort_column_data = request.GET.get(f'columns[{sort_column_index}][data]', 'id')
    sort_direction = request.GET.get('order[0][dir]', 'desc')

    sort_column_name = allowed_sort_columns.get(sort_column_data, 'id')
    if sort_direction == 'desc':
        sort_column_name = '-' + sort_column_name

    qs = qs.order_by(sort_column_name)

    page_qs = qs[page_start:page_end]

    data = [
        {
            'id': row.id,
            'branch_name': row.branch.name if row.branch else None,
            'bank_name': row.bank.name if row.bank else None,
            'account_number': row.account_number,
            'status': row.status,
        }
        for row in page_qs
    ]
    
    return JsonResponse({
        'data': data,
        'total_rows': total_rows,
        'recordsFiltered': total_rows,
        'recordsTotal': total_rows,
        'sort_column_name': sort_column_data,
    })
