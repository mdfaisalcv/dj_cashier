from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import Segment

@login_required
def index(request):
    return render(request, 'segment/index.html')

@login_required
def create(request):
    return render(request, 'segment/create.html')

@login_required
def submit(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        name = request.POST.get('segment_name')
        status = request.POST.get('status', '0') # Checkbox returns '1' if checked, else default to '0'
        
        if name:
            Segment.objects.create(
                cid=cid,
                name=name,
                status=int(status),
                created_by=request.user
            )
            messages.success(request, "Segment created successfully!")
            return redirect('cashier:segment-index')
        else:
            messages.error(request, "Segment Name is required.")
            return redirect('cashier:segment-create')
            
    return redirect('cashier:segment-index')

@login_required
def edit(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(Segment, id=id, cid=cid)
    return render(request, 'segment/edit.html', {'record': record})

@login_required
def update(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        id = request.GET.get('id')
        record = get_object_or_404(Segment, id=id, cid=cid)
        
        name = request.POST.get('segment_name')
        status = request.POST.get('status', '0')
        
        if name:
            record.name = name
            record.status = int(status)
            record.updated_by = request.user
            record.save()
            messages.success(request, "Segment updated successfully!")
        else:
            messages.error(request, "Segment Name is required.")
            
    return redirect('cashier:segment-index')

@login_required
def delete(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(Segment, id=id, cid=cid)
    record.delete()
    messages.warning(request, "Segment deleted successfully.")
    return redirect('cashier:segment-index')

@login_required
def get_data(request):
    # 🔍 Filtering
    cid = request.session.get('cid')
    queryset = Segment.objects.filter(cid=cid)

    name = request.GET.get('name')
    status = request.GET.get('status')

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

    # 📦 Data convert
    data = list(data_qs.values())

    return JsonResponse({
        'data': data,
        'recordsTotal': total_rows,
        'recordsFiltered': total_rows,
    })

