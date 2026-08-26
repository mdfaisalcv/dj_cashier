from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_cid import date_time_list
from ..common_fn import active_calendar,check_role,get_sl,check_active_date

@action("outstanding_reconciliation/index")
@action.uses("outstanding_reconciliation/index.html",session,flash,db)
def index(id=None):
    task_id='date_wise_sales_manage'
    task_id_view='date_wise_sales_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    return  dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

@action("outstanding_reconciliation/create", method=['GET', 'POST'])
@action.uses("outstanding_reconciliation/create.html", session,auth,T,db,flash)
def create(id=None): 
    task_id='date_wise_sales_manage'
    task_id_view='date_wise_sales_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')

    rows = db((db.brand.cid ==cid)).select(
    db.brand.id,
    db.brand.code,
    db.brand.name,
    db.brand.segment_id,
    db.brand.segment_name,
    orderby=[~db.brand.segment_name]
    )
    branch_ids = session.get('branchList')
    query = ((db.branch.cid ==cid)&(db.branch.status == 1))

    if session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            query &= db.branch.id.belongs(branch_ids)

    branchList = db(query).select()
    calendar_dates = active_calendar()
    active_date = calendar_dates['active_date'] if calendar_dates else None
    expire_at = calendar_dates['expire_at'] if calendar_dates else None
    formatted_date=date_time_list["date_fixed"].strftime(date_time_list["date_format"])
    
    return dict(rows=rows,branchList=branchList,active_date=active_date,expire_at=expire_at,formatted_date=formatted_date,date_time_list=date_time_list,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

@action("outstanding_reconciliation/submit", method=['POST'])
@action.uses("outstanding_reconciliation/index.html", session,auth,T,db,flash)
def submit(id=None): 
    sl=get_sl()
    cid = session.get('cid')
    transaction_date=request.forms.get('transaction_date').strip()        
    branch_name=request.forms.get('branch_name').strip()   

    if 'brand_name' not in request.POST or request.POST['brand_name'] == "":        
        brand_name = ""
    else:
        brand_name=request.POST.get('brand_name')
        if isinstance(brand_name, list):
            brand_name = brand_name
        else:
            brand_name = [brand_name]
    
    sales_tp = []
    sales_vat = []
    sales_discount = []
    sales_special_discount = []
    sales_total = []
    return_tp = []
    return_vat = []
    return_discount = []
    return_special_discount = []
    return_total = []
    net_sales_tp = []
    net_sales_vat = []
    net_sales_discount = []
    net_sales_special_discount = []
    net_sales_total = []
    
    for i in brand_name:
        #   ======Sales Data========
        value = request.POST.get(f's_tp_{i}') or 0        
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        sales_tp.append(value)

        value = request.POST.get(f's_vat_{i}') or 0            
        if isinstance(value, list):
            value = [float(v or 0) for v in value]         
        sales_vat.append(value)

        value = request.POST.get(f's_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]     
        sales_discount.append(value)

        value = request.POST.get(f's_sp_disc_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        sales_special_discount.append(value)

        value = request.POST.get(f's_total_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]     
        sales_total.append(value)

        # ===== Return Data=====
        value = request.POST.get(f'r_tp_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        return_tp.append(value)

        value = request.POST.get(f'r_vat_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]         
        return_vat.append(value)

        value = request.POST.get(f'r_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        return_discount.append(value)

        value = request.POST.get(f'r_sp_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]        
        return_special_discount.append(value)

        value = request.POST.get(f'r_total_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]            
        return_total.append(value)

        # ===== Net Sales Data=====
        value = request.POST.get(f'n_tp_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        net_sales_tp.append(value)

        value = request.POST.get(f'n_vat_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]          
        net_sales_vat.append(value)

        value = request.POST.get(f'n_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]          
        net_sales_discount.append(value)

        value = request.POST.get(f'n_sp_disc_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        net_sales_special_discount.append(value)

        value = request.POST.get(f'n_total_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        net_sales_total.append(value)
   

    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.branch_id==branch_name)&(db.tr_os_recon_h.trans_date==transaction_date)).select(db.tr_os_recon_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid ==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('outstanding_reconciliation','create')) 
    # insert function
    trans_id=db.tr_os_recon_h.insert(
        cid=cid,
        sl=branchRecord.name[:3].upper()+'-'+sl,
        branch_id=branchRecord.id,
        branch_name=branchRecord.name,
        trans_date=transaction_date
    )
    
    # Prepare data for bulk insert
    total_sales = 0.0
    return_sales = 0.0
    net_sales = 0.0
    outstanding_reconciliation = []

    for idx, brand_id in enumerate(brand_name):
        brand = db.brand[brand_id]
        if not brand:
            continue

        # safe get with default 0
        sales_tp_val       = float(sales_tp[idx]) if idx < len(sales_tp) else 0
        sales_vat_val      = float(sales_vat[idx]) if idx < len(sales_vat) else 0
        sales_disc_val     = float(sales_discount[idx]) if idx < len(sales_discount) else 0
        sales_sp_disc_val  = float(sales_special_discount[idx]) if idx < len(sales_special_discount) else 0
        sales_total_val    = float(sales_total[idx]) if idx < len(sales_total) else 0

        return_tp_val      = float(return_tp[idx]) if idx < len(return_tp) else 0
        return_vat_val     = float(return_vat[idx]) if idx < len(return_vat) else 0
        return_disc_val    = float(return_discount[idx]) if idx < len(return_discount) else 0
        return_sp_disc_val = float(return_special_discount[idx]) if idx < len(return_special_discount) else 0
        return_total_val   = float(return_total[idx]) if idx < len(return_total) else 0

        net_tp_val         = float(net_sales_tp[idx]) if idx < len(net_sales_tp) else 0
        net_vat_val        = float(net_sales_vat[idx]) if idx < len(net_sales_vat) else 0
        net_disc_val       = float(net_sales_discount[idx]) if idx < len(net_sales_discount) else 0
        net_sp_disc_val    = float(net_sales_special_discount[idx]) if idx < len(net_sales_special_discount) else 0
        net_total_val      = float(net_sales_total[idx]) if idx < len(net_sales_total) else 0

        # totals
        total_sales  += sales_total_val
        return_sales += return_total_val
        net_sales    += net_total_val

        outstanding_reconciliation.append({
            'trans_id': trans_id,
            'cid':cid,
            'trans_sl': f"{branchRecord.name[:3].upper()}-{sl}",
            'branch_id': branchRecord.id,
            'branch_name': branchRecord.name,
            'trans_date': transaction_date,
            'segment_id': brand.segment_id,
            'segment_name': brand.segment_name,
            'brand_id': brand_id,
            'brand_name': brand.name,
            'sales_tp': sales_tp_val,
            'sales_vat': sales_vat_val,
            'sales_discount': sales_disc_val,
            'sales_sp_disc': sales_sp_disc_val,
            'sales_total': sales_total_val,
            'return_tp': return_tp_val,
            'return_vat': return_vat_val,
            'return_discount': return_disc_val,
            'return_sp_disc': return_sp_disc_val,
            'return_total': return_total_val,
            'net_sales_tp': net_tp_val,
            'net_sales_vat': net_vat_val,
            'net_sales_discount': net_disc_val,
            'net_sales_sp_disc': net_sp_disc_val,
            'net_sales_total': net_total_val
        })

    # bulk insert + update header
    if outstanding_reconciliation:
        db.tr_os_recon_d.bulk_insert(outstanding_reconciliation)

    db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.id == trans_id)).update(
        total_sales=total_sales,
        total_return=return_sales,
        total_net_sales=net_sales
    )

    flash.set('Outstanding reconciliation added successfully', 'success')
    redirect(URL('outstanding_reconciliation','index'))   

@action("outstanding_reconciliation/edit", method=['GET', 'POST'])
@action.uses("outstanding_reconciliation/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    task_id='date_wise_sales_manage'
    task_id_view='date_wise_sales_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.id == request_id)).select().first()
        record_detail = db((db.tr_os_recon_d.cid ==cid)&(db.tr_os_recon_d.trans_id == request_id)).select()

        branch_ids = session.get('branchList')
        query = ((db.branch.cid ==cid)&(db.branch.status == 1))

        if session.get('role') != 'super_admin' and branch_ids:
            if isinstance(branch_ids, str):
                branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
            elif isinstance(branch_ids, list):
                branch_ids = [int(b) for b in branch_ids if b]

            if branch_ids:
                query &= db.branch.id.belongs(branch_ids)

        branchList = db(query).select()

        rows = db((db.brand.cid ==cid)).select(
        db.brand.id,
        db.brand.code,
        db.brand.name,
        db.brand.segment_id,
        db.brand.segment_name,
        orderby=[~db.brand.segment_name]
        )
        calendar_dates = active_calendar()
        active_date = calendar_dates['active_date'] if calendar_dates else None
        expire_at = calendar_dates['expire_at'] if calendar_dates else None
        check_active_date_val = check_active_date(record.trans_date)
    return dict(record=record,record_detail=record_detail,rows=rows,branchList=branchList,active_date=active_date,expire_at=expire_at,date_time_list=date_time_list,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role,check_active_date=check_active_date_val)


@action("outstanding_reconciliation/update", method=['POST'])
@action.uses("outstanding_reconciliation/index.html", session,auth,T,db,flash)
def update(id=None): 
    request_id = request.query.get('id')
    cid = session.get('cid')
    if request_id:
        record = db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.id == request_id)).select().first()
        
    transaction_date=request.forms.get('transaction_date').strip()        
    branch_name=request.forms.get('branch_name').strip()   

    if 'brand_name' not in request.POST or request.POST['brand_name'] == "":        
        brand_name = ""
    else:
        brand_name=request.POST.get('brand_name')
        if isinstance(brand_name, list):
            brand_name = brand_name
        else:
            brand_name = [brand_name]
    
    sales_tp = []
    sales_vat = []
    sales_discount = []
    sales_special_discount = []
    sales_total = []
    return_tp = []
    return_vat = []
    return_discount = []
    return_special_discount = []
    return_total = []
    net_sales_tp = []
    net_sales_vat = []
    net_sales_discount = []
    net_sales_special_discount = []
    net_sales_total = []
    
    for i in brand_name:
        #   ======Sales Data========
        value = request.POST.get(f's_tp_{i}') or 0        
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        sales_tp.append(value)

        value = request.POST.get(f's_vat_{i}') or 0            
        if isinstance(value, list):
            value = [float(v or 0) for v in value]         
        sales_vat.append(value)

        value = request.POST.get(f's_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]     
        sales_discount.append(value)

        value = request.POST.get(f's_sp_disc_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        sales_special_discount.append(value)

        value = request.POST.get(f's_total_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]     
        sales_total.append(value)

        # ===== Return Data=====
        value = request.POST.get(f'r_tp_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        return_tp.append(value)

        value = request.POST.get(f'r_vat_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]         
        return_vat.append(value)

        value = request.POST.get(f'r_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        return_discount.append(value)

        value = request.POST.get(f'r_sp_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]        
        return_special_discount.append(value)

        value = request.POST.get(f'r_total_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]            
        return_total.append(value)

        # ===== Net Sales Data=====
        value = request.POST.get(f'n_tp_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        net_sales_tp.append(value)

        value = request.POST.get(f'n_vat_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]          
        net_sales_vat.append(value)

        value = request.POST.get(f'n_disc_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]          
        net_sales_discount.append(value)

        value = request.POST.get(f'n_sp_disc_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        net_sales_special_discount.append(value)

        value = request.POST.get(f'n_total_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        net_sales_total.append(value)
   

    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.branch_id==branch_name)&(db.tr_os_recon_h.trans_date==transaction_date)&(db.tr_os_recon_h.id!=request_id)).select(db.tr_os_recon_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid ==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('outstanding_reconciliation','edit',vars=dict(id=request_id))) 
    
    
    # date wise receipt log
    old_outstanding_reconciliation = {
        'branch_id': record.branch_id,        
        'branch_name': record.branch_name,        
        'trans_date': record.trans_date
    }
    
    new_outstanding_reconciliation = {
        'branch_id': branch_name,        
        'branch_name': branchRecord.name,        
        'trans_date': transaction_date
    }
    
    # outstanding_reconciliation log
    # insert function
    record.update_record(
        branch_id=branch_name,
        branch_name=branchRecord.name,
        trans_date=transaction_date,
        note=old_outstanding_reconciliation
        ) 
    
    # Prepare data for bulk insert
    total_sales = 0.0
    return_sales = 0.0
    net_sales = 0.0
    outstanding_reconciliation = []

    for idx, brand_id in enumerate(brand_name):
        brand = db.brand[brand_id]
        if not brand:
            continue

        # safe get with default 0
        sales_tp_val       = float(sales_tp[idx]) if idx < len(sales_tp) else 0
        sales_vat_val      = float(sales_vat[idx]) if idx < len(sales_vat) else 0
        sales_disc_val     = float(sales_discount[idx]) if idx < len(sales_discount) else 0
        sales_sp_disc_val  = float(sales_special_discount[idx]) if idx < len(sales_special_discount) else 0
        sales_total_val    = float(sales_total[idx]) if idx < len(sales_total) else 0

        return_tp_val      = float(return_tp[idx]) if idx < len(return_tp) else 0
        return_vat_val     = float(return_vat[idx]) if idx < len(return_vat) else 0
        return_disc_val    = float(return_discount[idx]) if idx < len(return_discount) else 0
        return_sp_disc_val = float(return_special_discount[idx]) if idx < len(return_special_discount) else 0
        return_total_val   = float(return_total[idx]) if idx < len(return_total) else 0

        net_tp_val         = float(net_sales_tp[idx]) if idx < len(net_sales_tp) else 0
        net_vat_val        = float(net_sales_vat[idx]) if idx < len(net_sales_vat) else 0
        net_disc_val       = float(net_sales_discount[idx]) if idx < len(net_sales_discount) else 0
        net_sp_disc_val    = float(net_sales_special_discount[idx]) if idx < len(net_sales_special_discount) else 0
        net_total_val      = float(net_sales_total[idx]) if idx < len(net_sales_total) else 0

        # totals
        total_sales  += sales_total_val
        return_sales += return_total_val
        net_sales    += net_total_val

        outstanding_reconciliation.append({
            'trans_id': request_id,
            'cid':cid,
            'trans_sl':record.sl,
            'branch_id': branchRecord.id,
            'branch_name': branchRecord.name,
            'trans_date': transaction_date,
            'segment_id': brand.segment_id,
            'segment_name': brand.segment_name,
            'brand_id': brand_id,
            'brand_name': brand.name,
            'sales_tp': sales_tp_val,
            'sales_vat': sales_vat_val,
            'sales_discount': sales_disc_val,
            'sales_sp_disc': sales_sp_disc_val,
            'sales_total': sales_total_val,
            'return_tp': return_tp_val,
            'return_vat': return_vat_val,
            'return_discount': return_disc_val,
            'return_sp_disc': return_sp_disc_val,
            'return_total': return_total_val,
            'net_sales_tp': net_tp_val,
            'net_sales_vat': net_vat_val,
            'net_sales_discount': net_disc_val,
            'net_sales_sp_disc': net_sp_disc_val,
            'net_sales_total': net_total_val
        })

    # bulk insert + update header
    if outstanding_reconciliation:
        db((db.tr_os_recon_d.cid ==cid)&(db.tr_os_recon_d.trans_id == request_id)).delete()
        db.tr_os_recon_d.bulk_insert(outstanding_reconciliation)

    db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.id == request_id)).update(
        total_sales=total_sales,
        total_return=return_sales,
        total_net_sales=net_sales
    )

    # db.segment_log.insert(
    #     segment_name=segment_name,
    #     old_segment=old_segment,
    #     new_segment=new_segment,
    # )
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('outstanding_reconciliation','index'))  


@action("outstanding_reconciliation/delete")
@action.uses("outstanding_reconciliation/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        db((db.tr_os_recon_h.cid ==cid)&(db.tr_os_recon_h.id == request_id)).delete()
        db((db.tr_os_recon_d.cid ==cid)&(db.tr_os_recon_d.trans_id == request_id)).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('outstanding_reconciliation', 'index')))

    return locals()


@action("outstanding_reconciliation/get_data", method=['GET', 'POST'])
@action.uses(db,session)
def get_data():
    cid = session.get('cid')
    #Search Start##
    conditions = ""
    if session.get('role') != 'super_admin':
        branch_id_session = session.get('branchList')  # this is already a list
        if branch_id_session:
            branch_id_list = [str(c).strip() for c in branch_id_session if str(c).strip()]
            if branch_id_list:
                conditions += " AND branch_id IN ({})".format(
                    ",".join("'{}'".format(branch_id) for branch_id in branch_id_list)
                )

    
    if  request.query.get('branch_name') != None and request.query.get('branch_name') !='':
        conditions += " and branch_id = '"+str(request.query.get('branch_name'))+"'"

    if  request.query.get('from_date') != None and request.query.get('from_date') !='' and  request.query.get('to_date') != None and request.query.get('to_date') !='':
        conditions += " and trans_date >= '"+str(request.query.get('from_date'))+"' and trans_date <= '"+str(request.query.get('to_date'))+"'" 

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( """
    SELECT 
    id as id,
    sl as sl,
    branch_id as branch_id,
    branch_name as branch_name,
    trans_date as trans_date,
    total_sales as total_sales,
    total_return as total_return,
    total_net_sales as total_net_sales,                                   
    status as status    
    FROM tr_os_recon_h 
    WHERE 1 """ + conditions + """ group by id""", as_dict=True))

    page = int(int(request.query.get('start'))/int(request.query.get('length')) +1 or 1)
    rows_per_page = int(request.query.get('length') or 16)
    if rows_per_page == -1:
        rows_per_page = total_rows
    start = (page - 1) * rows_per_page         
    end = rows_per_page
    #Paginate End##


    #Ordering Start##
    sort_column_index = int(request.query.get('order[0][column]') or 0)
    sort_column_name = request.query.get('columns[' + str(sort_column_index) + '][data]') or 'id'
    sort_direction = request.query.get('order[0][dir]') or 'desc'
    #Ordering End##

    ##Query Start##
    sql = """
    SELECT 
    id as id,
    sl as sl,
    branch_id as branch_id,
    branch_name as branch_name,
    trans_date as trans_date,
    total_sales as total_sales,
    total_return as total_return,
    total_net_sales as total_net_sales,                                   
    status as status     
    FROM tr_os_recon_h
    WHERE 1 """ + conditions + """ ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
    """
    print(sql)
    data = db.executesql(sql, as_dict=True)    

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
