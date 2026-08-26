from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import Branch, Bank, BranchBank

@login_required
def index(request):
    return render(request, 'branch/index.html')

@login_required
def create(request):
    cid = request.session.get('cid')
    banksList = Bank.objects.filter(cid=cid)
    return render(request, 'branch/create.html', {'banksList': banksList})

@login_required
def submit(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        code       = request.POST.get('branch_code', '').strip()
        name       = request.POST.get('branch_name', '').strip()
        short_name = request.POST.get('short_name', '').strip()
        email      = request.POST.get('email', '').strip()
        address    = request.POST.get('address', '').strip()
        bank_list  = request.POST.getlist('bank_list')  # returns [] if not submitted
        status     = 1 if request.POST.get('status') == '1' else 0

        # --- Validation ---
        errors = []
        if not code:
            errors.append('Enter branch code')
        elif not name:
            errors.append('Enter branch name')
        elif not bank_list:
            errors.append('Enter bank list')
        else:
            if Branch.objects.filter(cid=cid, code=code).exists():
                errors.append('Branch code already exists')
            elif Branch.objects.filter(cid=cid, name=name).exists():
                errors.append('Branch name already exists')

        if errors:
            for msg in errors:
                messages.warning(request, msg)
            return redirect('cashier:branch-create')

        # --- Insert ---
        branch = Branch.objects.create(
            cid=cid,
            code=code,
            name=name,
            short_name=short_name,
            email=email,
            address=address,
            status=status,
            created_by=request.user
        )

        for bank_id in bank_list:
            BranchBank.objects.create(
                cid=cid,
                branch=branch,
                bank_id=bank_id,
                created_by=request.user
            )

        messages.success(request, "Branch created successfully!")
        return redirect('cashier:branch-index')

    return redirect('cashier:branch-index')

@login_required
def edit(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(Branch, id=id, cid=cid)
    branch_bank_rec = BranchBank.objects.filter(branch=record, cid=cid)
    branch_bank_records = [row.bank_id for row in branch_bank_rec]  # list of bank_ids
    
    banksList = Bank.objects.filter(cid=cid)
    return render(request, 'branch/edit.html', {'record': record, 'banksList': banksList, 'branch_bank_records': branch_bank_records})

@login_required
def update(request):
    cid = request.session.get('cid')
    id         = request.GET.get('id')
    record     = get_object_or_404(Branch, id=id, cid=cid)
    if record is None:
        messages.warning(request, 'Record not found')
        return redirect('cashier:branch-index')

    if request.method == 'POST':
        code       = request.POST.get('branch_code', '').strip()
        name       = request.POST.get('branch_name', '').strip()
        short_name = request.POST.get('short_name', '').strip()
        email      = request.POST.get('email', '').strip()
        address    = request.POST.get('address', '').strip()
        bank_list  = request.POST.getlist('bank_list')
        status     = 1 if request.POST.get('status') == '1' else 0

        # --- Validation ---
        errors = []
        if not code:
            errors.append('Enter branch code')
        elif not name:
            errors.append('Enter branch name')
        elif not bank_list:
            errors.append('Enter bank list')
        else:
            if Branch.objects.filter(cid=cid, code=code).exclude(id=id).exists():
                errors.append('Branch code already exists')
            elif Branch.objects.filter(cid=cid, name=name).exclude(id=id).exists():
                errors.append('Branch name already exists')

        if errors:
            for msg in errors:
                messages.warning(request, msg)
            return redirect(f'/cashier/branch/edit?id={id}')

        # --- Update ---
        record.code       = code
        record.name       = name
        record.short_name = short_name
        record.email      = email
        record.address    = address
        record.status     = status
        record.updated_by = request.user
        record.save()

        # --- Update BranchBank (delete old, insert new) ---
        BranchBank.objects.filter(branch=record).delete()
        for bank_id in bank_list:
            BranchBank.objects.create(
                branch=record,
                cid=cid,
                bank_id=bank_id,
                created_by=request.user
            )

        messages.success(request, "Branch updated successfully!")

    return redirect('cashier:branch-index')

@login_required
def delete(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(Branch, id=id, cid=cid)
    record.delete()
    messages.warning(request, "Branch deleted successfully.")
    return redirect('cashier:branch-index')

@login_required
def get_data(request):
    # 🔍 Filtering
    cid = request.session.get('cid')
    queryset = Branch.objects.filter(cid=cid)

    code = request.GET.get('code')
    name = request.GET.get('name')
    status = request.GET.get('status')

    if code:
        queryset = queryset.filter(id=code)
    if name:
        queryset = queryset.filter(id=name)

    if status:
        queryset = queryset.filter(status=status)

    # 📊 Total rows
    total_rows = queryset.count()

    # 📄 Pagination
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))

    if length == -1:
        data_qs = queryset
    else:
        data_qs = queryset[start:start + length]

    # 🔽 Ordering
    sort_column_index = request.GET.get('order[0][column]', 0)
    sort_column_name = request.GET.get(f'columns[{sort_column_index}][data]', 'id')
    sort_direction = request.GET.get('order[0][dir]', 'desc')

    if sort_direction == 'desc':
        sort_column_name = '-' + sort_column_name

    queryset = queryset.order_by(sort_column_name)

    # আবার slice করতে হবে (ordering এর পরে)
    if length != -1:
        data_qs = queryset[start:start + length]
    else:
        data_qs = queryset

    # 📦 Data convert (include related bank short names)
    data = []
    for branch in data_qs:
        bank_short_names = list(
            BranchBank.objects.filter(branch=branch)
            .values_list('bank__short_name', flat=True)
        )
        data.append({
            'id':             branch.id,
            'code':           branch.code,
            'name':           branch.name,
            'short_name':     branch.short_name,
            'email':          branch.email,
            'address':        branch.address,
            'status':         branch.status,
            'bank_short_name': ', '.join(bank_short_names),
        })

    return JsonResponse({
        'data': data,
        'recordsTotal': total_rows,
        'recordsFiltered': total_rows,
    })

