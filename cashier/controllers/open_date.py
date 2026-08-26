from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from cashier.models import OpenDate, Branch, User


# =========================================================
# INDEX
# =========================================================
@login_required
def index(request):
    return render(request, 'open_date/index.html')


# =========================================================
# CREATE
# =========================================================
@login_required
def create(request):
    cid = request.session.get('cid')
    branch_ids = request.session.get('branchList', [])
    role = request.session.get('role')

    queryset = Branch.objects.filter(status=1, cid=cid)

    # Non-super-admin হলে assigned branch only
    if role != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [
                int(branch_id)
                for branch_id in branch_ids.split(',')
                if branch_id.strip()
            ]
        elif isinstance(branch_ids, list):
            branch_ids = [
                int(branch_id)
                for branch_id in branch_ids
                if branch_id
            ]

        if branch_ids:
            queryset = queryset.filter(id__in=branch_ids)

    branchList = queryset.order_by('name')
    userList = User.objects.filter(is_active=1)

    return render(
        request,
        'open_date/create.html',
        {
            'branchList': branchList,
            'userList': userList,
        }
    )


# =========================================================
# SUBMIT
# =========================================================
@login_required
def submit(request):
    cid = request.session.get('cid')
    if request.method != 'POST':
        return redirect('cashier:open_date-index')

    branch_id = request.POST.get('branch_name', '').strip()
    user_id = request.POST.get('user_id', '').strip()
    raw_dates = request.POST.get('active_date', '').strip()
    expire_at = request.POST.get('expire_at', '').strip()
    status = 1 if request.POST.get('status') == '1' else 0

    # Clean active dates
    if raw_dates:
        date_list = [
            date.strip()
            for date in raw_dates.split(',')
            if date.strip()
        ]
        date_string = ','.join(date_list)
    else:
        date_string = ''

    # -------------------------
    # Validation
    # -------------------------
    errors = []

    if not branch_id:
        errors.append('Enter branch name')

    elif not user_id:
        errors.append('Enter user name')

    else:
        if OpenDate.objects.filter(
            cid=cid,
            branch_id=branch_id,
            user_id=user_id,
            expire_at=expire_at
        ).exists():
            errors.append('Branch already exists')

    if errors:
        for msg in errors:
            messages.warning(request, msg)

        return redirect('cashier:open_date-create')

    # -------------------------
    # Insert
    # -------------------------
    OpenDate.objects.create(
        cid=cid,
        branch_id=branch_id,
        user_id=user_id,
        active_date=date_string,
        expire_at=expire_at,
        status=status,
        created_by=request.user
    )

    messages.success(request, 'Record added successfully')
    return redirect('cashier:open_date-index')


# =========================================================
# EDIT
# =========================================================
@login_required
def edit(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')

    record = get_object_or_404(
        OpenDate,
        id=id,
        cid=cid
    )

    branchList = Branch.objects.filter(
        cid=cid,
        status=1
    )

    userList = User.objects.filter(is_active=1)

    return render(
        request,
        'open_date/edit.html',
        {
            'record': record,
            'branchList': branchList,
            'userList': userList,
        }
    )


# =========================================================
# UPDATE
# =========================================================
@login_required
def update(request):
    if request.method != 'POST':
        return redirect('cashier:open_date-index')

    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(OpenDate, id=id)

    branch_id = request.POST.get('branch_name', '').strip()
    user_id = request.POST.get('user_id', '').strip()
    raw_dates = request.POST.get('active_date', '').strip()
    expire_at = request.POST.get('expire_at', '').strip()
    status = 1 if request.POST.get('status') == '1' else 0

    # -------------------------
    # Clean active dates
    # -------------------------
    if raw_dates:
        date_list = [
            date.strip()
            for date in raw_dates.split(',')
            if date.strip()
        ]
        date_string = ','.join(date_list)
    else:
        date_string = ''

    # -------------------------
    # Validation
    # -------------------------
    errors = []

    if not branch_id:
        errors.append('Enter branch name')

    elif not user_id:
        errors.append('Enter user name')

    else:
        exists = OpenDate.objects.filter(
            cid=cid,
            branch_id=branch_id,
            user_id=user_id,
            expire_at=expire_at
        ).exclude(id=id).exists()

        if exists:
            errors.append('Branch already exists')

    if errors:
        for msg in errors:
            messages.warning(request, msg)

        return redirect(f'/cashier/open_date/edit?id={id}')

    # -------------------------
    # Update
    # -------------------------
    record.branch_id = branch_id
    record.user_id = user_id
    record.active_date = date_string
    record.expire_at = expire_at
    record.status = status
    record.updated_by = request.user
    record.save()

    messages.success(request, 'Record updated successfully')
    return redirect('cashier:open_date-index')


# =========================================================
# DELETE
# =========================================================
@login_required
def delete(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')

    record = get_object_or_404(OpenDate, id=id, cid=cid)
    record.delete()

    messages.warning(request, 'Record deleted successfully')
    return redirect('cashier:open_date-index')


@login_required
def get_data(request):

    # 🔍 CID Filtering
    cid = request.session.get('cid')

    queryset = OpenDate.objects.select_related(
        'branch',
        'user'
    ).filter(
        cid=cid
    )

    # =====================================================
    # Role Based Branch Filter
    # =====================================================
    role = request.session.get('role')
    branch_ids = request.session.get('branchList', [])

    if role != 'super_admin' and branch_ids:

        if isinstance(branch_ids, str):
            branch_ids = [
                int(branch_id.strip())
                for branch_id in branch_ids.split(',')
                if branch_id.strip().isdigit()
            ]

        elif isinstance(branch_ids, (list, tuple)):
            branch_ids = [
                int(branch_id)
                for branch_id in branch_ids
                if str(branch_id).strip().isdigit()
            ]

        if branch_ids:
            queryset = queryset.filter(
                branch_id__in=branch_ids
            )

    # 🔍 Filtering
    branch_name = request.GET.get('branch_name')
    user_name = request.GET.get('user_name')
    status = request.GET.get('status')

    if branch_name:
        queryset = queryset.filter(branch_id=branch_name)

    if user_name:
        queryset = queryset.filter(user_id=user_name)

    if status:
        queryset = queryset.filter(status=status)

    # 📊 Total rows
    total_rows = queryset.count()

    # 📄 Pagination
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
    except (TypeError, ValueError):
        start = 0
        length = 10

    # 🔽 Ordering
    sort_column_index = request.GET.get('order[0][column]', 0)
    sort_column_name = request.GET.get(
        f'columns[{sort_column_index}][data]',
        'id'
    )
    sort_direction = request.GET.get('order[0][dir]', 'desc')

    # DataTable column → Django field
    ordering_map = {
        'id': 'id',
        'branch_name': 'branch__name',
        'user_id': 'user_id',
        'user_name': 'user__user_name',
        'active_date': 'active_date',
        'expire_at': 'expire_at',
        'status': 'status',
    }

    sort_field = ordering_map.get(
        sort_column_name,
        'id'
    )

    if sort_direction == 'desc':
        sort_field = '-' + sort_field

    queryset = queryset.order_by(sort_field)

    # 📄 Pagination after ordering
    if length == -1:
        data_qs = queryset
    else:
        data_qs = queryset[start:start + length]

    # 📦 Data convert
    data = []

    for row in data_qs:
        data.append({
            'id': row.id,

            'branch_id': row.branch_id,

            'branch_name': (
                row.branch.name
                if row.branch_id
                else ''
            ),

            'user_id': row.user_id,

            # User Name
            'user_name': (
                row.user.username
                if row.user_id and hasattr(row.user, 'username')
                else ''
            ),

            'active_date': row.active_date or '',

            'expire_at': (
                row.expire_at.strftime('%Y-%m-%d')
                if row.expire_at
                else ''
            ),

            'status': row.status,
        })

    # 📤 Response
    return JsonResponse({
        'data': data,
        'recordsTotal': total_rows,
        'recordsFiltered': total_rows,
    })