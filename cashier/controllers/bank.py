from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from cashier.models import Bank

@login_required
def index(request):
    return render(request, 'bank/index.html')

@login_required
def create(request):
    return render(request, 'bank/create.html')

@login_required
def submit(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        short_name = request.POST.get('short_name')
        address = request.POST.get('address')
        status = request.POST.get('status', '0') # Checkbox returns '1' if checked, else default to '0'
        
        if bank_name:
            Bank.objects.create(
                cid=cid,
                name=bank_name,
                short_name=short_name,
                address=address,
                status=int(status),
                created_by=request.user
            )
            messages.success(request, "Bank created successfully!")
            return redirect('cashier:bank-index')
        else:
            messages.error(request, "Bank Name is required.")
            return redirect('cashier:bank-create')
            
    return redirect('cashier:bank-index')

@login_required
def edit(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(Bank, id=id, cid=cid)
    return render(request, 'bank/edit.html', {'record': record})

@login_required
def update(request):
    cid = request.session.get('cid')
    if request.method == 'POST':
        id = request.GET.get('id')
        record = get_object_or_404(Bank, id=id, cid=cid)
        
        bank_name = request.POST.get('bank_name')
        short_name = request.POST.get('short_name')
        address = request.POST.get('address')
        status = request.POST.get('status', '0')
        
        if bank_name:
            record.name = bank_name
            record.short_name = short_name
            record.address = address
            record.status = int(status)
            record.updated_by = request.user
            record.save()
            messages.success(request, "Bank updated successfully!")
        else:
            messages.error(request, "Bank Name is required.")
            
    return redirect('cashier:bank-index')

@login_required
def delete(request):
    cid = request.session.get('cid')
    id = request.GET.get('id')
    record = get_object_or_404(Bank, id=id, cid=cid)
    record.delete()
    messages.warning(request, "Bank deleted successfully.")
    return redirect('cashier:bank-index')

@login_required
def get_data(request):
    # 🔍 Filtering
    cid = request.session.get('cid')
    queryset = Bank.objects.filter(cid=cid)

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

# from py4web import action, request, abort, redirect, URL,response,Session
# from py4web.utils.form import Form, FormStyleDefault
# from yatl.helpers import A,TAG, XML
# from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
# from ..common import db, session, T, auth,flash
# from ..common_fn import check_role

# @action("bank/index")
# @action.uses("bank/index.html",session,flash,db)
# def index(id=None):
#     task_id='bank_manage'
#     task_id_view='bank_view'
#     access_permission = check_role(task_id)
#     access_permission_view = check_role(task_id_view)
#     if not (access_permission or access_permission_view):
#         flash.set('Access is Denied !', 'warning')
#         redirect(URL('login', 'index'))
    
#     return dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

# @action("bank/create", method=['GET', 'POST'])
# @action.uses("bank/create.html", session,auth,T,db,flash)
# def create(id=None): 
#     task_id='bank_manage'
#     task_id_view='bank_view'
#     access_permission = check_role(task_id)
#     access_permission_view = check_role(task_id_view)
#     if not (access_permission or access_permission_view):
#         flash.set('Access is Denied !', 'warning')
#         redirect(URL('login', 'index'))

#     return dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

# @action("bank/submit", method=['POST'])
# @action.uses("bank/index.html", session,auth,T,db,flash)
# def submit(id=None): 
#     bank_name=request.forms.get('bank_name').strip()        
#     short_name=request.forms.get('short_name').strip()        
#     address=request.forms.get('address').strip()        
#     status=request.forms.get('status')
    
#     if str(status)!="1":
#         status=0
    
#     errors=[]
#     if bank_name=='' or bank_name is None:
#         errors.append('Enter bank name') 
#     else:
#         rows_check=db((db.bank.name==bank_name)).select(db.bank.name,limitby=(0,1))
#         if rows_check:
#             errors.append('Bank name already exist')    
        
#     if errors:
#         msg = ''
#         for item in errors:
#             msg = msg + item + 'rdrdrd'
#         flash.set(msg, 'warning')
#         redirect(URL('bank','create')) 
#     # insert function
#     db.bank.insert(
#         name=bank_name,
#         short_name=short_name,
#         address=address,
#         status=status
#     )
        
#     flash.set('Record added successfully', 'success')
#     redirect(URL('bank','index'))   

# @action("bank/edit", method=['GET', 'POST'])
# @action.uses("bank/edit.html", session,auth,T,db,flash)
# def edit(id=None): 
#     task_id='bank_manage'
#     task_id_view='bank_view'
#     access_permission = check_role(task_id)
#     access_permission_view = check_role(task_id_view)
#     if not (access_permission or access_permission_view):
#         flash.set('Access is Denied !', 'warning')
#         redirect(URL('login', 'index'))

#     request_id = request.query.get('id')
#     if request_id:
#         record = db(db.bank.id == request_id).select().first()
    
#     return dict(record=record,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

# @action("bank/update", method=['POST'])
# @action.uses("bank/index.html", session,auth,T,db,flash)
# def update(id=None): 
#     request_id = request.query.get('id')
#     if request_id:
#         record = db(db.bank.id == request_id).select().first()
        
#     bank_name=request.forms.get('bank_name').strip() 
#     short_name=request.forms.get('short_name').strip()        
#     address=request.forms.get('address').strip()   
#     status=request.forms.get('status')
    
#     if str(status)!="1":
#         status=0
    
#     errors=[]
#     if bank_name=='':
#         errors.append('Enter bank name') 
#     else:
#         rows_check=db((db.bank.name==bank_name) & (db.bank.id!=request_id)).select(db.bank.name,limitby=(0,1))
#         if rows_check:
#             errors.append('Bank name already exist')
            
#     if errors:
#         msg = ''
#         for item in errors:
#             msg = msg + item + 'rdrdrd'
#         flash.set(msg, 'warning')
#         redirect(URL('bank','edit',vars=dict(id=request_id))) 
    
    
#     # category log
#     old_bank = {
#         'name': record.name,        
#         'short_name': record.short_name,        
#         'address': record.address,        
#         'status': record.status
#     }
    
#     new_bank = {
#         'name': bank_name,
#         'short_name': short_name,
#         'address': address,
#         'status': status
#     }
    
#     # segment log
#     # insert function
#     record.update_record(
#         name=bank_name,
#         short_name=short_name,
#         address=address,
#         status=status,
#         note=old_bank
#         ) 
#     # db.bank_log.insert(
#     #     bank_name=bank_name,
#     #     old_bank=old_bank,
#     #     new_bank=new_bank,
#     # )
        
#     flash.set('Record updated successfully', 'success')
#     redirect(URL('bank','index'))  


# @action("bank/delete")
# @action.uses("bank/index.html",session,flash,db)
# def delete(id=None):
#     # if session['status']!='success':
#     #     return 'Access Denied'
#     request_id = request.query.get('id')
#     if request_id:
#         db(db.bank.id == request_id).delete()
        
#         flash.set('Record Delete successfully', 'error')      
#         return dict(redirect(URL('bank', 'index')))

#     return locals()


# @action("bank/get_data", method=['GET', 'POST'])
# @action.uses(db)
# def get_data():
#     # if session.status=="" or session.status==None:
#     #   redirect(URL(c='login',f='index'))
#     #Search Start##
#     conditions = ""
#     # if  request.query.get('cid') != None and request.query.get('cid') !='':
#     #     cid = str(request.query.get('cid'))
#     #     conditions += " and cid = '"+cid+"'"
    
#     if  request.query.get('name') != None and request.query.get('name') !='':
#         conditions += " and id = '"+str(request.query.get('name'))+"'"

#     if  request.query.get('status') != None and request.query.get('status') !='':
#         conditions += " and status = '"+str(request.query.get('status'))+"'"
#     #Search End## 
    
#     ##Paginate Start##
#     total_rows = len(db.executesql( "SELECT * FROM bank where 1 "+conditions, as_dict=True))

#     page = int(int(request.query.get('start'))/int(request.query.get('length')) +1 or 1)
#     rows_per_page = int(request.query.get('length') or 16)
#     if rows_per_page == -1:
#         rows_per_page = total_rows
#     start = (page - 1) * rows_per_page         
#     end = rows_per_page
#     #Paginate End##


#     #Ordering Start##
#     sort_column_index = int(request.query.get('order[0][column]') or 0)
#     sort_column_name = request.query.get('columns[' + str(sort_column_index) + '][data]') or 'id'
#     sort_direction = request.query.get('order[0][dir]') or 'desc'
#     #Ordering End##

#     ##Query Start##
#     sql = """
#     SELECT * FROM bank WHERE 1 """ + conditions + """ ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
#     """

#     data = db.executesql(sql, as_dict=True)    

#     return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
#     # return json.dumps(data)
