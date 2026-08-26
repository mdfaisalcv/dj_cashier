from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import  Branch, Bank, Segment, BankAccount, Brand, User

@login_required
def get_branch(request):
    # Select2 AJAX stub
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    branches = Branch.objects.filter(cid=cid, name__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.name} for b in branches]
    return JsonResponse({'results': results})

@login_required
def get_branch_code(request):
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    branches = Branch.objects.filter(cid=cid, code__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.code} for b in branches]
    return JsonResponse({'results': results})
    
@login_required
def get_branch_name(request):
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    branches = Branch.objects.filter(cid=cid, name__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.name} for b in branches]
    return JsonResponse({'results': results})

# @login_required
# def get_branch_name(request):
#     role = request.session.get("role")

#     qs = Branch.objects.all()

#     if role != "super_admin":
#         branch_list = request.session.get("branchList", [])
#         if branch_list:
#             qs = qs.filter(id__in=branch_list)

#     data = list(
#         qs.order_by("name").values(
#             "id",
#             "name"
#         )
#     )

#     return JsonResponse({"results": data})

@login_required
def get_bank(request):
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    banks = Bank.objects.filter(cid=cid, name__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.name} for b in banks]
    return JsonResponse({'results': results})

@login_required
def get_bank_account(request):
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    bank_accounts = BankAccount.objects.filter(cid=cid, account_number__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.account_number} for b in bank_accounts]
    return JsonResponse({'results': results})

@login_required
def get_banks_by_branch(request):    
    cid = request.session.get('cid')
    branch_id = request.GET.get("branch_id")

    sql = """
        SELECT b.id, b.name, b.short_name
        FROM bank b
        LEFT JOIN branch_bank bb ON b.id = bb.bank_id
        WHERE bb.branch_id = "{branch_id}" and b.status='1' and b.cid='{cid}'
    """.format(branch_id=branch_id, cid=cid)    
    
    data = Bank.objects.raw(sql)
    
    results = [{'id': b.id, 'name': b.name} for b in data]
    return JsonResponse({'results': results})

@login_required
def get_brand_code(request):
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    brands = Brand.objects.filter(cid=cid, code__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.code} for b in brands]
    return JsonResponse({'results': results})

@login_required
def get_brand_name(request):
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    brands = Brand.objects.filter(cid=cid, name__icontains=q)[:20]
    results = [{'id': b.id, 'text': b.name} for b in brands]
    return JsonResponse({'results': results})


@login_required
def get_user_name(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(is_active=True, username__icontains=q)[:20]
    results = [{'id': u.id, 'text': u.username} for u in users]
    return JsonResponse({'results': results})


@login_required
def get_segment(request):
    # Select2 AJAX stub
    cid = request.session.get('cid')
    q = request.GET.get('q', '')
    segments = Segment.objects.filter(cid=cid, name__icontains=q)[:20]
    results = [{'id': s.id, 'text': s.name} for s in segments]
    return JsonResponse({'results': results})
    

