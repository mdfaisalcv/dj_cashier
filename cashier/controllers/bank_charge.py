from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_cid import date_time_list
from ..common_fn import active_calendar,check_role,get_sl,check_active_date

@action("bank_charge/index")
@action.uses("bank_charge/index.html",session,flash,db)
def index(id=None):
    task_id='bank_charge_manage'
    task_id_view='bank_charge_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    return dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)


@action("bank_charge/create", method=['GET', 'POST'])
@action.uses("bank_charge/create.html", session,auth,T,db,flash)
def create(id=None): 
    task_id='bank_charge_manage'
    task_id_view='bank_charge_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))
    cid = session.get('cid')
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
    
    return dict(branchList=branchList,active_date=active_date,expire_at=expire_at,formatted_date=formatted_date,date_time_list=date_time_list,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)


@action("bank_charge/submit", method=['POST'])
@action.uses("bank_charge/index.html", session,auth,T,db,flash)
def submit(id=None): 
    sl=get_sl()
    cid = session.get('cid')
    transaction_date=request.forms.get('transaction_date').strip()        
    branch_name=request.forms.get('branch_name').strip()   

    if 'bank_name' not in request.POST or request.POST['bank_name'] == "":        
        bank_name = ""
    else:
        bank_name=request.POST.get('bank_name')
        if isinstance(bank_name, list):
            bank_name = bank_name
        else:
            bank_name = [bank_name]
    
    amount = []    
    for i in bank_name:
        value = request.POST.get(f'amount_{i}')        
        if isinstance(value, list):
            amount_values = ",".join(str(v) for v in value)
        else:
            amount_values = value        
        amount.append(amount_values)
        

    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_bcharge_h.cid ==cid)&(db.tr_bcharge_h.branch_id==branch_name)&(db.tr_bcharge_h.trans_date==transaction_date)).select(db.tr_bcharge_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid ==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('bank_charge','create')) 
    # insert function
    trans_id=db.tr_bcharge_h.insert(
        cid=cid,
        sl=branchRecord.name[:3].upper()+'-'+sl,
        branch_id=branchRecord.id,
        branch_name=branchRecord.name,
        trans_date=transaction_date
    )
    
    # Prepare data for bulk insert
    bank_charge = []
    for index in range(len(bank_name)):
        bankRecord = db((db.bank.cid ==cid)&(db.bank.id == bank_name[index])).select().first()

        # if index < 8:  # Limit print to first 8 items
        #     print(f"{index + 1} → {brand_name[index]}")
    
        bank_charge.append({
            'trans_id': trans_id,
            'cid':cid,
            'trans_sl': branchRecord.name[:3].upper() + '-' + sl,
            'branch_id': branchRecord.id,
            'branch_name': branchRecord.name,
            'trans_date':transaction_date,
            'bank_id':bankRecord.id,
            'bank_name':bankRecord.name,
            'amount': amount[index] if index < len(amount) else 0
        })

    if bank_charge:
        db.tr_bcharge_d.bulk_insert(bank_charge)
        
    flash.set('Bank Charge added successfully', 'success')
    redirect(URL('bank_charge','index'))   

@action("bank_charge/edit", method=['GET', 'POST'])
@action.uses("bank_charge/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    task_id='bank_charge_manage'
    task_id_view='bank_charge_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_bcharge_h.cid ==cid)&(db.tr_bcharge_h.id == request_id)).select().first()
        record_detail = db((db.tr_bcharge_d.cid ==cid)&(db.tr_bcharge_d.trans_id == request_id)).select()

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
        check_active_date_val = check_active_date(record.trans_date)
    return dict(record=record,record_detail=record_detail,branchList=branchList,active_date=active_date,expire_at=expire_at,date_time_list=date_time_list,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role,check_active_date=check_active_date_val)

@action("bank_charge/update", method=['POST'])
@action.uses("bank_charge/index.html", session,auth,T,db,flash)
def update(id=None): 
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_bcharge_h.cid ==cid)&(db.tr_bcharge_h.id == request_id)).select().first()
        
    transaction_date=request.forms.get('transaction_date').strip()        
    branch_name=request.forms.get('branch_name').strip()   
    
    if 'bank_name' not in request.POST or request.POST['bank_name'] == "":        
        bank_name = ""
    else:
        bank_name=request.POST.get('bank_name')
        if isinstance(bank_name, list):
            bank_name = bank_name
        else:
            bank_name = [bank_name]
    
    amount = []    
    for i in bank_name:
        value = request.POST.get(f'amount_{i}')        
        if isinstance(value, list):
            amount_values = ",".join(str(v) for v in value)
        else:
            amount_values = value        
        amount.append(amount_values)
        

    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_bcharge_h.cid ==cid)&(db.tr_bcharge_h.branch_id==branch_name)&(db.tr_bcharge_h.trans_date==transaction_date)&(db.tr_bcharge_h.id!=request_id)).select(db.tr_bcharge_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid ==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('bank_charge','edit',vars=dict(id=request_id))) 
    
    
    # date wise receipt log
    old_bank_charge = {
        'branch_id': record.branch_id,        
        'branch_name': record.branch_name,        
        'trans_date': record.trans_date,
        'approve': record.approve,
        'approve_by': record.approve_by
    }
    
    new_bank_charge = {
        'branch_id': branch_name,        
        'branch_name': branchRecord.name,        
        'trans_date': transaction_date
    }
    
    # bank charge log
    # insert function
    record.update_record(
        branch_id=branch_name,
        branch_name=branchRecord.name,
        trans_date=transaction_date,
        note=old_bank_charge
        ) 
    
    # Prepare data for bulk insert
    bank_charge = []
    for index in range(len(bank_name)):
        bankRecord = db(db.bank.id == bank_name[index]).select().first()

        # if index < 8:  # Limit print to first 8 items
        #     print(f"{index + 1} → {brand_name[index]}")
    
        bank_charge.append({
            'trans_id': request_id,
            'cid':cid,
            'trans_sl': record.sl,
            'branch_id': branchRecord.id,
            'branch_name': branchRecord.name,
            'trans_date':transaction_date,
            'bank_id':bankRecord.id,
            'bank_name':bankRecord.name,
            'amount': amount[index] if index < len(amount) else 0
        })
    
    if bank_charge:
        db((db.tr_bcharge_d.cid == cid)&(db.tr_bcharge_d.trans_id == request_id)).delete()
        db.tr_bcharge_d.bulk_insert(bank_charge)

    # db.segment_log.insert(
    #     segment_name=segment_name,
    #     old_segment=old_segment,
    #     new_segment=new_segment,
    # )
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('bank_charge','index'))  


@action("bank_charge/delete")
@action.uses("bank_charge/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        db((db.tr_bcharge_h.cid ==cid)&(db.tr_bcharge_h.id == request_id)).delete()
        db((db.tr_bcharge_d.cid ==cid)&(db.tr_bcharge_d.trans_id == request_id)).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('bank_charge', 'index')))

    return locals()


@action("bank_charge/get_data", method=['GET', 'POST'])
@action.uses(db,session)
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    cid = session.get('cid')
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
    h.approve as approve,
    d.bank_id as bank_id,
    d.bank_name as bank_name,                               
    SUM(d.amount) as amount     
    FROM tr_bcharge_h h
    LEFT JOIN 
    tr_bcharge_d d on h.id = d.trans_id
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
    h.approve as approve,
    d.bank_id as bank_id,
    d.bank_name as bank_name,                               
    SUM(d.amount) as amount     
    FROM tr_bcharge_h h
    LEFT JOIN 
    tr_bcharge_d d on h.id = d.trans_id
    WHERE 1 """ + conditions + """ group by h.id ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
    """
    print(sql)
    data = db.executesql(sql, as_dict=True)    

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
