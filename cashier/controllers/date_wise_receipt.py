from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_cid import date_time_list
from ..common_fn import active_calendar,check_role,get_sl,check_active_date

@action("date_wise_receipt/index")
@action.uses("date_wise_receipt/index.html",session,flash,db)
def index(id=None):
    task_id='date_wise_receipt_manage'
    task_id_view='date_wise_receipt_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    return  dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

@action("date_wise_receipt/create", method=['GET', 'POST'])
@action.uses("date_wise_receipt/create.html", session,auth,T,db,flash)
def create(id=None): 
    task_id='date_wise_receipt_manage'
    task_id_view='date_wise_receipt_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')

    rows = db(db.brand.cid == cid).select(
    db.brand.id,
    db.brand.code,
    db.brand.name,
    db.brand.segment_id,
    db.brand.segment_name,
    orderby=[~db.brand.segment_name]
)
    branch_ids = session.get('branchList')
    query = ((db.branch.cid == cid)&(db.branch.status == 1))

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
    # print(expire_at)

    return dict(rows=rows,branchList=branchList,active_date=active_date,expire_at=expire_at,formatted_date=formatted_date,date_time_list=date_time_list,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

@action("date_wise_receipt/submit", method=['POST'])
@action.uses("date_wise_receipt/index.html", session,auth,T,db,flash)
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
    
    collection = []
    money_receipt = []
    advance_receipt = []
    srt_ex_receipt = []
    adv_adjustment = []
    adv_adjustment_plus = []
    adv_adjustment_minus = []
    mr_reverse = []
    for i in brand_name:
        value = request.POST.get(f'collection_{i}')        
        if isinstance(value, list):
            collection_values = ",".join(str(v) for v in value)
        else:
            collection_values = value        
        collection.append(collection_values)

        value = request.POST.get(f'money_receipt_{i}')        
        if isinstance(value, list):
            money_receipt_values = ",".join(str(v) for v in value)
        else:
            money_receipt_values = value        
        money_receipt.append(money_receipt_values)

        value = request.POST.get(f'advance_receipt_{i}')        
        if isinstance(value, list):
            advance_receipt_values = ",".join(str(v) for v in value)
        else:
            advance_receipt_values = value        
        advance_receipt.append(advance_receipt_values)

        value = request.POST.get(f'srt_ex_receipt_{i}')        
        if isinstance(value, list):
            srt_ex_receipt_values = ",".join(str(v) for v in value)
        else:
            srt_ex_receipt_values = value        
        srt_ex_receipt.append(srt_ex_receipt_values)

        value = request.POST.get(f'adv_adjustment_{i}')        
        if isinstance(value, list):
            adv_adjustment_values = ",".join(str(v) for v in value)
        else:
            adv_adjustment_values = value        
        adv_adjustment.append(adv_adjustment_values)
    
        value = request.POST.get(f'adv_adjustment_plus_{i}')        
        if isinstance(value, list):
            adv_adjustment_plus_values = ",".join(str(v) for v in value)
        else:
            adv_adjustment_plus_values = value        
        adv_adjustment_plus.append(adv_adjustment_plus_values)

        value = request.POST.get(f'adv_adjustment_minus_{i}')        
        if isinstance(value, list):
            adv_adjustment_minus_values = ",".join(str(v) for v in value)
        else:
            adv_adjustment_minus_values = value        
        adv_adjustment_minus.append(adv_adjustment_minus_values)

        value = request.POST.get(f'mr_reverse_{i}')        
        if isinstance(value, list):
            mr_reverse_values = ",".join(str(v) for v in value)
        else:
            mr_reverse_values = value        
        mr_reverse.append(mr_reverse_values)
    

    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_receipt_h.cid==cid)&(db.tr_receipt_h.branch_id==branch_name)&(db.tr_receipt_h.trans_date==transaction_date)).select(db.tr_receipt_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')
        
        branchRecord = db((db.branch.cid==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('date_wise_receipt','create')) 
    # insert function
    trans_id=db.tr_receipt_h.insert(
        cid=cid,
        sl=branchRecord.name[:3].upper()+'-'+sl,
        branch_id=branchRecord.id,
        branch_name=branchRecord.name,
        trans_date=transaction_date
    )
    
    # Prepare data for bulk insert
    date_wise_receipt = []
    for index in range(len(brand_name)):
        brandRecord = db((db.brand.cid==cid)&(db.brand.id == brand_name[index])).select().first()

        # if index < 8:  # Limit print to first 8 items
        #     print(f"{index + 1} → {brand_name[index]}")
    
        date_wise_receipt.append({
            'trans_id': trans_id,
            'cid':cid,
            'trans_sl': branchRecord.name[:3].upper() + '-' + sl,
            'branch_id': branchRecord.id,
            'branch_name': branchRecord.name,
            'trans_date':transaction_date,
            'segment_id':brandRecord.segment_id,
            'segment_name':brandRecord.segment_name,
            'brand_id': brand_name[index],
            'brand_name': brandRecord.name,
            'collection': collection[index] if index < len(collection) else 0,
            'money_receipt': money_receipt[index] if index < len(money_receipt) else 0,
            'adv_receipt': advance_receipt[index] if index < len(advance_receipt) else 0,
            'short_receipt': srt_ex_receipt[index] if index < len(srt_ex_receipt) else 0,
            'adv_adj': adv_adjustment[index] if index < len(adv_adjustment) else 0,
            'adj_plus': adv_adjustment_plus[index] if index < len(adv_adjustment_plus) else 0,
            'adj_minus': adv_adjustment_minus[index] if index < len(adv_adjustment_minus) else 0,
            'mr_reverse': mr_reverse[index] if index < len(mr_reverse) else 0
        })

    if date_wise_receipt:
        db.tr_receipt_d.bulk_insert(date_wise_receipt)
        
    flash.set('Date wise receipts added successfully', 'success')
    redirect(URL('date_wise_receipt','index'))   

@action("date_wise_receipt/edit", method=['GET', 'POST'])
@action.uses("date_wise_receipt/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    task_id='date_wise_receipt_manage'
    task_id_view='date_wise_receipt_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_receipt_h.cid==cid)&(db.tr_receipt_h.id == request_id)).select().first()
        record_detail = db((db.tr_receipt_d.cid==cid)&(db.tr_receipt_d.trans_id == request_id)).select()

        branch_ids = session.get('branchList')
        query = (db.branch.status == 1)

        if session.get('role') != 'super_admin' and branch_ids:
            if isinstance(branch_ids, str):
                branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
            elif isinstance(branch_ids, list):
                branch_ids = [int(b) for b in branch_ids if b]

            if branch_ids:
                query &= db.branch.id.belongs(branch_ids)

        branchList = db(query).select()
        
        rows = db(db.brand).select(
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

@action("date_wise_receipt/update", method=['POST'])
@action.uses("date_wise_receipt/index.html", session,auth,T,db,flash)
def update(id=None): 
    request_id = request.query.get('id')
    cid = session.get('cid')
    if request_id:
        record = db((db.tr_receipt_h.cid==cid)&(db.tr_receipt_h.id == request_id)).select().first()
        
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
    
    collection = []
    money_receipt = []
    advance_receipt = []
    srt_ex_receipt = []
    adv_adjustment = []
    adv_adjustment_plus = []
    adv_adjustment_minus = []
    mr_reverse = []
    for i in brand_name:
        value = request.POST.get(f'collection_{i}') or 0    
        if isinstance(value, list):
            value = [float(v or 0) for v in value]      
        collection.append(value)

        value = request.POST.get(f'money_receipt_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]           
        money_receipt.append(value)

        value = request.POST.get(f'advance_receipt_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]             
        advance_receipt.append(value)

        value = request.POST.get(f'srt_ex_receipt_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]          
        srt_ex_receipt.append(value)

        value = request.POST.get(f'adv_adjustment_{i}') or 0          
        if isinstance(value, list):
            value = [float(v or 0) for v in value]       
        adv_adjustment.append(value)
    
        value = request.POST.get(f'adv_adjustment_plus_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]     
        adv_adjustment_plus.append(value)

        value = request.POST.get(f'adv_adjustment_minus_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]      
        adv_adjustment_minus.append(value)

        value = request.POST.get(f'mr_reverse_{i}') or 0         
        if isinstance(value, list):
            value = [float(v or 0) for v in value]          
        mr_reverse.append(value)

       
    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_receipt_h.cid==cid)&(db.tr_receipt_h.branch_id==branch_name)&(db.tr_receipt_h.trans_date==transaction_date)&(db.tr_receipt_h.id!=request_id)).select(db.tr_receipt_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('date_wise_receipt','edit',vars=dict(id=request_id))) 
    
    
    # date wise receipt log
    old_date_wise_receipt = {
        'branch_id': record.branch_id,        
        'branch_name': record.branch_name,        
        'trans_date': record.trans_date
    }
    
    new_date_wise_receipt = {
        'branch_id': branch_name,        
        'branch_name': branchRecord.name,        
        'trans_date': transaction_date
    }
    
    # segment log
    # insert function
    record.update_record(
        branch_id=branch_name,
        branch_name=branchRecord.name,
        trans_date=transaction_date,
        note=old_date_wise_receipt
        ) 
    
    # Prepare data for bulk insert
    date_wise_receipt = []
    for index in range(len(brand_name)):
        brandRecord = db((db.brand.cid==cid)&(db.brand.id == brand_name[index])).select().first()

        date_wise_receipt.append({
            'trans_id': request_id,
            'cid':cid,
            'trans_sl':record.sl,
            'branch_id': branchRecord.id,
            'branch_name': branchRecord.name,
            'trans_date':transaction_date,
            'segment_id':brandRecord.segment_id,
            'segment_name':brandRecord.segment_name,
            'brand_id': brand_name[index],
            'brand_name': brandRecord.name,
            'collection': collection[index] if index < len(collection) else 0,
            'money_receipt': money_receipt[index] if index < len(money_receipt) else 0,
            'adv_receipt': advance_receipt[index] if index < len(advance_receipt) else 0,
            'short_receipt': srt_ex_receipt[index] if index < len(srt_ex_receipt) else 0,
            'adv_adj': adv_adjustment[index] if index < len(adv_adjustment) else 0,
            'adj_plus': adv_adjustment_plus[index] if index < len(adv_adjustment_plus) else 0,
            'adj_minus': adv_adjustment_minus[index] if index < len(adv_adjustment_minus) else 0,
            'mr_reverse': mr_reverse[index] if index < len(mr_reverse) else 0
        })
    
    if date_wise_receipt:
        db((db.tr_receipt_d.cid == cid)&(db.tr_receipt_d.trans_id == request_id)).delete()
        db.tr_receipt_d.bulk_insert(date_wise_receipt)

    # db.segment_log.insert(
    #     segment_name=segment_name,
    #     old_segment=old_segment,
    #     new_segment=new_segment,
    # )
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('date_wise_receipt','index'))  


@action("date_wise_receipt/delete")
@action.uses("date_wise_receipt/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    request_id = request.query.get('id')
    cid = session.get('cid')
    if request_id:
        db((db.tr_receipt_h.cid ==cid)&(db.tr_receipt_h.id == request_id)).delete()
        db((db.tr_receipt_d.cid == cid)&(db.tr_receipt_d.trans_id == request_id)).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('date_wise_receipt', 'index')))

    return locals()


@action("date_wise_receipt/get_data", method=['GET', 'POST'])
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
                conditions += " AND h.branch_id IN ({})".format(
                    ",".join("'{}'".format(branch_id) for branch_id in branch_id_list)
                )

    
    if  request.query.get('branch_name') != None and request.query.get('branch_name') !='':
        conditions += " and h.branch_id = '"+str(request.query.get('branch_name'))+"'"

    if  request.query.get('from_date') != None and request.query.get('from_date') !='' and  request.query.get('to_date') != None and request.query.get('to_date') !='':
        conditions += " and h.trans_date >= '"+str(request.query.get('from_date'))+"' and h.trans_date <= '"+str(request.query.get('to_date'))+"'" 

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and h.status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( """
    SELECT 
    h.id as id,
    h.sl as sl,
    h.branch_id as branch_id,
    h.branch_name as branch_name,
    h.trans_date as trans_date,
    h.status as status,
    d.segment_name as segment_name,
    d.brand_name as brand_name,
    SUM(d.collection) as collection,
    SUM(d.money_receipt) as money_receipt,
    SUM(d.adv_receipt) as adv_receipt,
    SUM(d.short_receipt) as short_receipt,
    SUM(d.adv_adj) as adv_adj,
    SUM(d.adj_plus) as adj_plus,
    SUM(d.adj_minus) as adj_minus,
    SUM(d.mr_reverse) as mr_reverse   
    FROM tr_receipt_h h
    LEFT JOIN 
    tr_receipt_d d on h.id = d.trans_id
    WHERE 1 """ + conditions + """ group by h.id""", as_dict=True))

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
    h.id as id,
    h.sl as sl,
    h.branch_id as branch_id,
    h.branch_name as branch_name,
    h.trans_date as trans_date,
    h.status as status,
    d.segment_name as segment_name,
    d.brand_name as brand_name,
    SUM(d.collection) as collection,
    SUM(d.money_receipt) as money_receipt,
    SUM(d.adv_receipt) as adv_receipt,
    SUM(d.short_receipt) as short_receipt,
    SUM(d.adv_adj) as adv_adj,
    SUM(d.adj_plus) as adj_plus,
    SUM(d.adj_minus) as adj_minus,
    SUM(d.mr_reverse) as mr_reverse   
    FROM tr_receipt_h h
    LEFT JOIN 
    tr_receipt_d d on h.id = d.trans_id
    WHERE 1 """ + conditions + """ group by h.id ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
    """
    print(sql)
    data = db.executesql(sql, as_dict=True)    

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
