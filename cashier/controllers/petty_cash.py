from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_cid import date_time_list
from ..common_fn import active_calendar,check_role,get_sl,check_active_date

@action("petty_cash/index")
@action.uses("petty_cash/index.html",session,flash,db)
def index(id=None):
    task_id='petty_cash_manage'
    task_id_view='petty_cash_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    return  dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

@action("petty_cash/create", method=['GET', 'POST'])
@action.uses("petty_cash/create.html", session,auth,T,db,flash)
def create(id=None): 
    task_id='petty_cash_manage'
    task_id_view='petty_cash_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))
    cid = session.get('cid')
    branch_ids = session.get('branchList')
    query = ((db.branch.status == 1)&(db.branch.cid ==cid))

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


@action("petty_cash/submit", method=['POST'])
@action.uses("petty_cash/index.html", session,auth,T,db,flash)
def submit(id=None): 
    sl=get_sl()
    cid = session.get('cid')
    transaction_date=request.forms.get('transaction_date').strip()        
    branch_name=request.forms.get('branch_name').strip()        
    total_receipt_hq=request.forms.get('total_receipt_hq').strip()        
    transfer_imprest_cash=request.forms.get('transfer_imprest_cash').strip()    
    m_receipt=request.forms.get('m_receipt').strip()    
    total_expense_cq=request.forms.get('total_expense_cq').strip()    
    total_exp=request.forms.get('total_exp').strip()       
    
    if total_receipt_hq=="":
        total_receipt_hq=0
    if transfer_imprest_cash=="":
        transfer_imprest_cash=0
    if m_receipt=="":
        m_receipt=0
    if total_expense_cq=="":
        total_expense_cq=0
    if total_exp=="":
        total_exp=0
        
    
    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_petty_cash_h.cid ==cid)&(db.tr_petty_cash_h.branch_id==branch_name)&(db.tr_petty_cash_h.trans_date==transaction_date)).select(db.tr_petty_cash_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid ==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('petty_cash','create')) 
    # insert function
    db.tr_petty_cash_h.insert(
        cid=cid,
        sl=branchRecord.name[:3].upper()+'-'+sl,
        branch_id=branchRecord.id,
        branch_name=branchRecord.name,
        trans_date=transaction_date,
        total_receipt_hq=total_receipt_hq,
        transfer_imprest_cash=transfer_imprest_cash,
        m_receipt=m_receipt,
        total_expense_cq=total_expense_cq,
        total_exp=total_exp
    )
        
    flash.set('Petty cash added successfully', 'success')
    redirect(URL('petty_cash','index'))   

@action("petty_cash/edit", method=['GET', 'POST'])
@action.uses("petty_cash/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    task_id='petty_cash_manage'
    task_id_view='petty_cash_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_petty_cash_h.cid ==cid)&(db.tr_petty_cash_h.id == request_id)).select().first()
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
    return dict(record=record,branchList=branchList,active_date=active_date,expire_at=expire_at,date_time_list=date_time_list,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role,check_active_date=check_active_date_val)

@action("petty_cash/update", method=['POST'])
@action.uses("petty_cash/index.html", session,auth,T,db,flash)
def update(id=None): 
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_petty_cash_h.cid ==cid)&(db.tr_petty_cash_h.id == request_id)).select().first()
    transaction_date=request.forms.get('transaction_date').strip()        
    branch_name=request.forms.get('branch_name').strip()        
    total_receipt_hq=request.forms.get('total_receipt_hq').strip()        
    transfer_imprest_cash=request.forms.get('transfer_imprest_cash').strip()    
    m_receipt=request.forms.get('m_receipt').strip()    
    total_expense_cq=request.forms.get('total_expense_cq').strip()    
    total_exp=request.forms.get('total_exp').strip()       
    
    if total_receipt_hq=="":
        total_receipt_hq=0
    if transfer_imprest_cash=="":
        transfer_imprest_cash=0
    if m_receipt=="":
        m_receipt=0
    if total_expense_cq=="":
        total_expense_cq=0
    if total_exp=="":
        total_exp=0
        
    
    errors=[]
    if transaction_date=='' or transaction_date is None:
        errors.append('Enter transaction date') 
    elif branch_name=='' or branch_name is None:
        errors.append('Enter branch name') 
    else:
        rows_check=db((db.tr_petty_cash_h.cid ==cid)&(db.tr_petty_cash_h.branch_id==branch_name)&(db.tr_petty_cash_h.trans_date==transaction_date)&(db.tr_petty_cash_h.id!=request_id)).select(db.tr_petty_cash_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Record already exist')

        branchRecord = db((db.branch.cid ==cid)&(db.branch.id == branch_name)).select().first()
                
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('petty_cash','edit',vars=dict(id=request_id))) 
    
    
    # petty cash log
    old_petty_cash = {
        'branch_id': record.branch_id,        
        'branch_name': record.branch_name,        
        'trans_date': record.trans_date,        
        'total_receipt_hq': record.total_receipt_hq,
        'transfer_imprest_cash': record.transfer_imprest_cash,
        'm_receipt': record.m_receipt,
        'total_expense_cq': record.total_expense_cq,
        'total_exp': record.total_exp        
    }
    
    new_petty_cash = {
        'branch_id': branchRecord.id,        
        'branch_name': branchRecord.name,        
        'trans_date': transaction_date,        
        'total_receipt_hq': total_receipt_hq,
        'transfer_imprest_cash': transfer_imprest_cash,
        'm_receipt': m_receipt,
        'total_expense_cq': total_expense_cq,
        'total_exp': total_exp  
    }
    
    # segment log
    # insert function
    record.update_record(
        branch_id=branchRecord.id,
        branch_name=branchRecord.name,
        trans_date=transaction_date,
        total_receipt_hq=total_receipt_hq,
        transfer_imprest_cash=transfer_imprest_cash,
        m_receipt=m_receipt,
        total_expense_cq=total_expense_cq,
        total_exp=total_exp,
        note=old_petty_cash
        ) 
    # db.bank_log.insert(
    #     bank_name=bank_name,
    #     old_bank=old_bank,
    #     new_bank=new_bank,
    # )
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('petty_cash','index'))  


@action("petty_cash/delete")
@action.uses("petty_cash/index.html",session,flash,db)
def delete(id=None):
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        db((db.tr_petty_cash_h.cid ==cid)&(db.tr_petty_cash_h.id == request_id)).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('petty_cash', 'index')))

    return locals()


@action("petty_cash/get_data", method=['GET', 'POST'])
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
    total_rows = len(db.executesql( "SELECT * FROM tr_petty_cash_h where 1 "+conditions, as_dict=True))

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
    SELECT * FROM tr_petty_cash_h WHERE 1 """ + conditions + """ ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
    """

    data = db.executesql(sql, as_dict=True)    

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
