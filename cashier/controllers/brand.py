from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import Brand, BrandBranch, Segment, Branch

@login_required
def index(request):
    return render(request, 'brand/index.html')

@login_required
def create(request):
    cid = request.session.get('cid')
    segmentList = Segment.objects.filter(cid=cid)

    role = request.session.get('role')
    branch_ids = request.session.get('branchList')
    branches = Branch.objects.filter(status=1, cid=cid)

    if role != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            branches = branches.filter(id__in=branch_ids)

    branchList = branches

    context = {
        'segmentList': segmentList,
        'branchList': branchList
    }
    return render(request, 'brand/create.html', context)

@login_required
def submit(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        brand_code = request.POST.get('brand_code', '').strip()
        brand_name = request.POST.get('brand_name', '').strip()
        short_name = request.POST.get('short_name', '').strip()
        segment = request.POST.get('segment', '').strip()

        branch_list = request.POST.getlist('branch_list')  # handles multi-select properly

        status = request.POST.get('status')
        status = 1 if str(status) == "1" else 0

        errors = []
        if brand_code == '':
            errors.append('Enter branch code')
        elif brand_name == '':
            errors.append('Enter branch name')
        elif segment == '':
            errors.append('Enter segment')
        elif not branch_list:
            errors.append('Enter branch list')
        else:
            if Brand.objects.filter(cid=cid, code=brand_code).exists():
                errors.append('Brand code already exist')
            elif Brand.objects.filter(cid=cid, name=brand_name).exists():
                errors.append('Brand name already exist')

        segment_rec = Segment.objects.filter(cid=cid, id=segment).first()
        segment_name = segment_rec.name if segment_rec else None
        
        if errors:
            msg = '<br>'.join(errors)
            messages.warning(request, msg)
            return redirect('cashier:brand-create')

        brand = Brand.objects.create(
            cid=cid,
            code=brand_code,
            name=brand_name,
            short_name=short_name,
            segment_id=segment,
            status=status,
            created_by=request.user
        )

        brand_branch_objs = [
            BrandBranch(cid=cid,brand_id=brand.id, branch_id=branch_id)
            for branch_id in branch_list
        ]
        if brand_branch_objs:
            BrandBranch.objects.bulk_create(brand_branch_objs)

        messages.success(request, 'Record added successfully')
        return redirect('cashier:brand-index')

    return redirect('cashier:brand-index')

@login_required
def edit(request):
    cid = request.session.get('cid')
    request_id = request.GET.get('id')

    if request_id:
        record = get_object_or_404(Brand, cid=cid, id=request_id)
    else:
        record = None

    brand_branch_records = []
    segmentList = Segment.objects.filter(cid=cid)
    branchList = []


    brand_branch_records = list(
        BrandBranch.objects.filter(cid=cid,brand_id=request_id).values_list('branch_id', flat=True)
    )

    role = request.session.get('role')
    branch_ids = request.session.get('branchList')
    branches = Branch.objects.filter(cid=cid,status=1)

    if role != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            branches = branches.filter(id__in=branch_ids)

    branchList = branches
    
    context = {
        'record': record,
        'brand_branch_records': brand_branch_records,
        'segmentList': segmentList,
        'branchList': branchList
    }
    return render(request, 'brand/edit.html', context)


@login_required
def update(request):
    cid = request.session.get('cid')
    request_id = request.GET.get('id')
    record     = get_object_or_404(Brand, id=request_id, cid=cid)
    if record is None:
        messages.warning(request, 'Record not found')
        return redirect('cashier:brand-index')

    if request.method == 'POST':
        brand_code = request.POST.get('brand_code', '').strip()
        brand_name = request.POST.get('brand_name', '').strip()
        short_name = request.POST.get('short_name', '').strip()
        segment = request.POST.get('segment', '').strip()

        branch_list = request.POST.getlist('branch_list')

        status = request.POST.get('status')
        status = 1 if str(status) == "1" else 0

        errors = []
        if brand_code == '':
            errors.append('Enter branch code')
        elif brand_name == '':
            errors.append('Enter branch name')
        elif segment == '':
            errors.append('Enter segment')
        elif not branch_list:
            errors.append('Enter branch list')
        else:
            if Brand.objects.filter(cid=cid, code=brand_code).exclude(id=request_id).exists():
                errors.append('Branch code already exist')
            elif Brand.objects.filter(cid=cid,name=brand_name).exclude(id=request_id).exists():
                errors.append('Branch name already exist')

        segment_rec = Segment.objects.filter(cid=cid,id=segment).first()
        segment_name = segment_rec.name if segment_rec else None

        if errors:
            msg = '<br>'.join(errors)
            messages.warning(request, msg)
            return redirect('cashier:brand-edit', id=request_id)

        # audit snapshot
        old_brand = {
            'code': record.code,
            'name': record.name,
            'short_name': record.short_name,
            'segment_id': record.segment_id,
            'status': record.status,
        }

        record.code = brand_code
        record.name = brand_name
        record.short_name = short_name
        record.segment_id = segment
        record.status = status
        record.note = old_brand
        record.save()

        # Refresh branch associations: delete existing, then re-insert
        BrandBranch.objects.filter(cid=cid,brand_id=request_id).delete()
        brand_branch_objs = [
            BrandBranch(cid=cid, brand_id=request_id, branch_id=branch_id)
            for branch_id in branch_list
        ]
        if brand_branch_objs:
            BrandBranch.objects.bulk_create(brand_branch_objs)

        # BrandLog.objects.create(brand_name=brand_name, old_brand=old_brand, new_brand=new_brand)

        messages.success(request, 'Record updated successfully')
        return redirect('cashier:brand-index')    
    
    return redirect('cashier:brand-index')

@login_required
def delete(request):
    cid = request.session.get('cid')
    request_id = request.GET.get('id')
    if request_id:
        get_object_or_404(Brand, cid=cid,id=request_id).delete()
        messages.error(request, 'Record Delete successfully')

    return redirect('cashier:brand-index')


@login_required
def get_data(request):
    cid = request.session.get('cid')
    qs = Brand.objects.filter(cid=cid)

    role = request.session.get('role')
    if role != 'super_admin':
        branch_id_session = request.session.get('branchList')
        if branch_id_session:
            if isinstance(branch_id_session, str):
                branch_id_list = [c.strip() for c in branch_id_session.split(',') if c.strip()]
            else:
                branch_id_list = [str(c).strip() for c in branch_id_session if str(c).strip()]
            if branch_id_list:
                qs = qs.filter(brandbranch__branch_id__in=branch_id_list)

    code = request.GET.get('code')
    if code:
        qs = qs.filter(id=code)

    name = request.GET.get('name')
    if name:
        qs = qs.filter(id=name)

    segment = request.GET.get('segment')
    if segment:
        qs = qs.filter(segment_id=segment)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    qs = qs.distinct()
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

    # Ordering — whitelist allowed columns
    allowed_sort_columns = {
        'id': 'id',
        'code': 'code',
        'brand_name': 'name',
        'segment_name': 'segment_name',
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

    data = []
    for row in page_qs:
        branch_names = list(
            BrandBranch.objects.filter(brand_id=row.id)
            .select_related('branch_id')
            .values_list('branch_id__short_name', flat=True)
        )
        segmentName = Segment.objects.filter(id=row.segment_id).first()
        segment_name = segmentName.name if segmentName else ""
        
        data.append({
            'id': row.id,
            'code': row.code,
            'brand_name': row.name,
            'segment_name': segment_name,
            'status': row.status,
            'branch_name': ', '.join(filter(None, branch_names)),
        })
    # print(data)
    return JsonResponse({
        'data': data,
        'total_rows': total_rows,
        'recordsFiltered': total_rows,
        'recordsTotal': total_rows,
        'sort_column_name': sort_column_data,
    })
