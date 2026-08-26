from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_fn import active_calendar,check_role,get_sl,check_active_date,check_active_date_imprest
from ..common_cid import date_time_list
import calendar
import random
import datetime

@action("imprest_bank_reconciliation/index")
@action.uses("imprest_bank_reconciliation/index.html",session,flash,db)
def index(id=None):
    task_id='impress_bank_reconcile_manage'
    task_id_view='impress_bank_reconcile_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    return  dict(access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)

@action("imprest_bank_reconciliation/create", method=['GET', 'POST'])
@action.uses("imprest_bank_reconciliation/create.html", session,auth,T,db,flash)
def create(id=None): 
    task_id='impress_bank_reconcile_manage'
    task_id_view='impress_bank_reconcile_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')
    branch_ids = session.get('branchList')
    query = ((db.branch.cid == cid) & (db.branch.status == 1))

    if session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            query &= db.branch.id.belongs(branch_ids)

    branchList = db(query).select()

    return dict(branchList=branchList,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)


@action("imprest_bank_reconciliation/check", method=['POST'])
@action.uses("imprest_bank_reconciliation/index.html", session,auth,T,db,flash)
def check(id=None):
    cid = session.get('cid')      
    branch_name = request.forms.get('branch_name')
    bank_name = request.forms.get('bank_name')
    account_number = request.forms.get('account_number')
    yearCombo = request.forms.get('yearCombo')
    monthCombo = request.forms.get('monthCombo')

    branch_name = branch_name.strip() if branch_name else ''
    bank_name = bank_name.strip() if bank_name else ''
    account_number = account_number.strip() if account_number else ''
    yearCombo = yearCombo.strip() if yearCombo else ''
    monthCombo = monthCombo.strip() if monthCombo else ''

    errors = []
    if branch_name == '':
        errors.append('Enter branch name')
    if yearCombo == '':
        errors.append('Enter year')
    if monthCombo == '':
        errors.append('Enter month')
    else:
        rows_check = db(
            (db.tr_impr_bnk_h.cid == cid) &
            (db.tr_impr_bnk_h.branch_id == branch_name) &
            (db.tr_impr_bnk_h.year == yearCombo) &
            (db.tr_impr_bnk_h.month == monthCombo)
        ).select(db.tr_impr_bnk_h.id, limitby=(0, 1))

        if rows_check:
            errors.append('Already Data Entered For Given Month!')

    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('imprest_bank_reconciliation','create')) 
    
    # flash.set('Record found successfully', 'success')
    redirect(URL('imprest_bank_reconciliation','create_page',vars=dict(branch_name=branch_name,bank_name=bank_name,account_number=account_number,year=yearCombo,month=monthCombo)))  

@action("imprest_bank_reconciliation/create_page", method=['GET', 'POST'])
@action.uses("imprest_bank_reconciliation/create_page.html", session,auth,T,db,flash)
def create_page(id=None): 
    task_id='impress_bank_reconcile_manage'
    task_id_view='impress_bank_reconcile_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')
    branch_id = request.query.get('branch_name')
    bank_name = request.query.get('bank_name')
    account_number = request.query.get('account_number')
    yearCombo = request.query.get('year')
    monthCombo = request.query.get('month')
    
    if monthCombo and monthCombo.isdigit():
        month_name = calendar.month_name[int(monthCombo)]
    
    closing_per_bank=0
    closing_per_bank_book=0
    rows_check = db(
        (db.tr_impr_bnk_h.cid == cid) &
        (db.tr_impr_bnk_h.branch_id == branch_id)
    ).select(db.tr_impr_bnk_h.id,db.tr_impr_bnk_h.closing_per_bank,db.tr_impr_bnk_h.closing_per_bank_book, orderby=~db.tr_impr_bnk_h.id, limitby=(0, 1))
    # return db._lastsql
    if rows_check:
        closing_per_bank = rows_check[0].closing_per_bank
        closing_per_bank_book = rows_check[0].closing_per_bank_book
    #     yearCombo = rows_check[0].year
    #     monthCombo = rows_check[0].month
        
    #     if monthCombo and monthCombo.isdigit():
    #         month_name = calendar.month_name[int(monthCombo)]
    
    branchRec = db((db.branch.cid == cid) & (db.branch.id==branch_id)).select(db.branch.code,db.branch.name).first()
    bankRec = db((db.bank.cid == cid) & (db.bank.id==bank_name)& (db.bank.status=='1')).select(db.bank.id,db.bank.name).first()

    return dict(branch_id=branch_id,branchRec=branchRec,bankRec=bankRec,account_number=account_number,yearCombo=yearCombo,monthCombo=monthCombo,month_name=month_name,closing_per_bank_book=closing_per_bank_book,closing_per_bank=closing_per_bank,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role)
   


@action("imprest_bank_reconciliation/submit", method=['POST'])
@action.uses("imprest_bank_reconciliation/index.html", session,auth,T,db,flash)
def submit(id=None): 
    cid = session.get('cid')
    branch_id=request.forms.get('branch_id').strip()        
    bank_id=request.forms.get('bank_id').strip()       
    yearCombo=request.forms.get('yearCombo').strip()       
    monthCombo=request.forms.get('monthCombo').strip()       
    account_number=request.forms.get('account_number').strip()        
    opening_balance=request.forms.get('opening_balance').strip()        
    bankInterest=request.forms.get('bankInterest').strip()        
    bankCharge=request.forms.get('bankCharge').strip()        
    closing_balance_bank_statement=request.forms.get('closing_balance_bank_statement').strip()        
    closingBalanceAsPerBankBook=request.forms.get('closingBalanceAsPerBankBook').strip()        
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=1
    
    errors=[]
    if branch_id=='' or branch_id is None:
        errors.append('Enter branch name') 
    elif bank_id=='' or bank_id is None:
        errors.append('Enter bank name') 
    elif account_number=='' or account_number is None:
        errors.append('Enter account number') 
    else:
        rows_check=db((db.tr_impr_bnk_h.cid == cid) & (db.tr_impr_bnk_h.branch_id==branch_id)&(db.tr_impr_bnk_h.trans_date==str(date_time_list['current_date']))&(db.tr_impr_bnk_h.year==yearCombo)&(db.tr_impr_bnk_h.month==monthCombo)).select(db.tr_impr_bnk_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Branch already exist')    
        
        branchRecord = db((db.branch.cid == cid) & (db.branch.id == branch_id)).select().first()        
     
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('imprest_bank_reconciliation','create')) 
    
    sl=get_sl()
    # insert function
    trans_id=db.tr_impr_bnk_h.insert(
        cid=cid,
        sl=branchRecord.name[:3].upper()+'-'+sl,
        branch_id=branch_id,
        branch_code=branchRecord.code,
        bank_id=bank_id,
        account_number=account_number,
        opening_balance=opening_balance,
        bank_interest=bankInterest,
        bank_charge=bankCharge,
        closing_balance=closing_balance_bank_statement,
        closing_per_bank=closing_balance_bank_statement,
        closing_per_bank_book=closingBalanceAsPerBankBook,
        preparation_date=str(date_time_list['current_date']),
        trans_date=str(date_time_list['current_date']),
        year=yearCombo,
        month=monthCombo,
        status=status
    )

    # Insert Deposited/Received Rows
    # -----------------------------
    for i in range(1, 11):   # you have 10 rows
        date_str = request.POST.get(f"deposited_received_date_{i}")
        amount = request.POST.get(f"deposited_received_from_corporate_amount_{i}")
        ref_no = request.POST.get(f"deposited_received_from_corporate_ref_no_{i}")
        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=trans_id,
            cid=cid,
            trans_sl=branchRecord.name[:3].upper()+'-'+sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="DEPOSITED_OR_RECEIVED",
            ref_no=ref_no,
            trans_date=str(date_time_list['current_date']),
            year=yearCombo,
            month=monthCombo
        )

    # -----------------------------
    # Insert Less Check Issued Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"less_check_issued_date_{i}")
        amount = request.POST.get(f"less_check_issued_amount_{i}")
        ref_no = request.POST.get(f"less_check_issued_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=trans_id,
            cid=cid,
            trans_sl=branchRecord.name[:3].upper()+'-'+sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="LESS_CHECK_ISSUED",
            ref_no=ref_no,
            trans_date=str(date_time_list['current_date']),
            year=yearCombo,
            month=monthCombo
        )

    # -----------------------------
    # Insert Less Check Issued CQ Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"less_check_issuedCQ_date_{i}")
        amount = request.POST.get(f"less_check_issuedCQ_amount_{i}")
        ref_no = request.POST.get(f"less_check_issuedCQ_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=trans_id,
            cid=cid,
            trans_sl=branchRecord.name[:3].upper()+'-'+sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="LESS_CHECK_ISSUED_CQ",
            ref_no=ref_no,
            trans_date=str(date_time_list['current_date']),
            year=yearCombo,
            month=monthCombo
        )


    # -----------------------------
    # Insert deposited but not show bank book Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"deposited_but_not_show_bank_book_date_{i}")
        amount = request.POST.get(f"deposited_but_not_show_bank_book_amount_{i}")
        ref_no = request.POST.get(f"deposited_but_not_show_bank_book_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=trans_id,
            cid=cid,
            trans_sl=branchRecord.name[:3].upper()+'-'+sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="DEPOSITED_BUT_NOT_SHOW_BANK_BOOK",
            ref_no=ref_no,
            trans_date=str(date_time_list['current_date']),
            year=yearCombo,
            month=monthCombo
        )

    # -----------------------------
    # Insert debited by bank but notShowing bank book Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"debited_by_bank_but_notShowing_bank_book_date_{i}")
        amount = request.POST.get(f"debited_by_bank_but_notShowing_bank_book_amount_{i}")
        ref_no = request.POST.get(f"debited_by_bank_but_notShowing_bank_book_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=trans_id,
            cid=cid,
            trans_sl=branchRecord.name[:3].upper()+'-'+sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK",
            ref_no=ref_no,
            trans_date=str(date_time_list['current_date']),
            year=yearCombo,
            month=monthCombo
        )


    # -----------------------------
    # Insert cheque issued Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"cheque_issued_date_{i}")
        amount = request.POST.get(f"cheque_issued_amount_{i}")
        ref_no = request.POST.get(f"cheque_issued_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=trans_id,
            cid=cid,
            trans_sl=branchRecord.name[:3].upper()+'-'+sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="CHEQUE_ISSUED",
            ref_no=ref_no,
            trans_date=str(date_time_list['current_date']),
            year=yearCombo,
            month=monthCombo
        )

        
    flash.set('Record added successfully', 'success')
    redirect(URL('imprest_bank_reconciliation','index'))   

@action("imprest_bank_reconciliation/edit", method=['GET', 'POST'])
@action.uses("imprest_bank_reconciliation/edit.html", session,auth,T,db,flash)
def edit(id=None): 
    task_id='impress_bank_reconcile_manage'
    task_id_view='impress_bank_reconcile_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        record = db((db.tr_impr_bnk_h.cid == cid) & (db.tr_impr_bnk_h.id == request_id)).select().first()
        
        if record.month and record.month.isdigit():
            month_name = calendar.month_name[int(record.month)]
        
        record_details = db((db.tr_impr_bnk_d.cid == cid) & (db.tr_impr_bnk_d.trans_id == request_id)).select()

        branchRec = db((db.branch.cid == cid) & (db.branch.id==record.branch_id)).select().first()
        bankRec = db((db.bank.cid == cid) & (db.bank.id==record.bank_id) & (db.bank.status=='1')).select().first()
        check_active_date_val = check_active_date_imprest(record.trans_date)
    return dict(record=record,record_details=record_details,branchRec=branchRec,bankRec=bankRec,month_name=month_name,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role,check_active_date=check_active_date_val)

@action("imprest_bank_reconciliation/update", method=['POST'])
@action.uses("imprest_bank_reconciliation/index.html", session,auth,T,db,flash)
def update(id=None): 
    request_id = request.query.get('id')
    cid = session.get('cid')
    if request_id:
        record = db((db.tr_impr_bnk_h.cid == cid) & (db.tr_impr_bnk_h.id == request_id)).select().first()
        
    branch_id=request.forms.get('branch_id').strip()        
    bank_id=request.forms.get('bank_id').strip()       
    yearCombo=request.forms.get('year').strip()       
    monthCombo=request.forms.get('month').strip()  
    account_number=request.forms.get('account_number').strip()        
    opening_balance=request.forms.get('opening_balance').strip()        
    bankInterest=request.forms.get('bankInterest').strip()        
    bankCharge=request.forms.get('bankCharge').strip()        
    closing_balance_bank_statement=request.forms.get('closing_balance_bank_statement').strip()        
    closingBalanceAsPerBankBook=request.forms.get('closingBalanceAsPerBankBook').strip()  
    status=request.forms.get('status')
    
    if str(status)!="1":
        status=0
    
    errors=[]
    if branch_id=='' or branch_id is None:
        errors.append('Enter branch name') 
    elif bank_id=='' or bank_id is None:
        errors.append('Enter bank name') 
    elif account_number=='' or account_number is None:
        errors.append('Enter account number') 
    else:
        rows_check=db((db.tr_impr_bnk_h.cid == cid) & (db.tr_impr_bnk_h.branch_id==branch_id)&(db.tr_impr_bnk_h.trans_date==str(date_time_list['current_date'])) & (db.tr_impr_bnk_h.id != request_id)&(db.tr_impr_bnk_h.year==yearCombo)&(db.tr_impr_bnk_h.month==monthCombo)) .select(db.tr_impr_bnk_h.id,limitby=(0,1))
        if rows_check:
            errors.append('Branch already exist')    
        
        branchRecord = db((db.branch.cid == cid) & (db.branch.id == branch_id)).select().first() 
            
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('imprest_bank_reconciliation','edit',vars=dict(id=request_id))) 
    
    
    # category log
    old_imp_bank_rec = {
        'branch_id': record.branch_id,        
        'bank_id': record.bank_id,        
        'account_number': record.account_number,        
        'status': record.status
    }

    new_imp_bank_rec = {
        'branch_id': branch_id,
        'bank_id': bank_id,
        'account_number': account_number,
        'status': status
    }
    
    # insert function
    record.update_record(
        branch_id=branch_id,
        branch_code=branchRecord.code,
        bank_id=bank_id,
        account_number=account_number,
        opening_balance=opening_balance,
        bank_interest=bankInterest,
        bank_charge=bankCharge,
        closing_balance=closing_balance_bank_statement,
        closing_per_bank=closing_balance_bank_statement,
        closing_per_bank_book=closingBalanceAsPerBankBook,
        preparation_date=str(date_time_list['current_date']),
        # trans_date=str(date_time_list['current_date']),
        year=record.year,
        month=record.month,
        status=status,
        note=old_imp_bank_rec
        ) 
    db(db.tr_impr_bnk_d.trans_id == request_id).delete()
    # db.bank_log.insert(
    #     bank_name=bank_name,
    #     old_bank=old_bank,
    #     new_bank=new_bank,
    # )
    
    # Insert Deposited/Received Rows
    # -----------------------------
    for i in range(1, 11):   # you have 10 rows
        date_str = request.POST.get(f"deposited_received_date_{i}")
        amount = request.POST.get(f"deposited_received_from_corporate_amount_{i}")
        ref_no = request.POST.get(f"deposited_received_from_corporate_ref_no_{i}")
        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=request_id,
            cid=cid,
            trans_sl=record.sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="DEPOSITED_OR_RECEIVED",
            ref_no=ref_no,
            trans_date=record.trans_date,
            year=record.year,
            month=record.month
        )

    # -----------------------------
    # Insert Less Check Issued Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"less_check_issued_date_{i}")
        amount = request.POST.get(f"less_check_issued_amount_{i}")
        ref_no = request.POST.get(f"less_check_issued_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=request_id,
            cid=cid,
            trans_sl=record.sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="LESS_CHECK_ISSUED",
            ref_no=ref_no,
            trans_date=record.trans_date,
            year=record.year,
            month=record.month
        )

    # -----------------------------
    # Insert Less Check Issued CQ Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"less_check_issuedCQ_date_{i}")
        amount = request.POST.get(f"less_check_issuedCQ_amount_{i}")
        ref_no = request.POST.get(f"less_check_issuedCQ_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=request_id,
            cid=cid,
            trans_sl=record.sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="LESS_CHECK_ISSUED_CQ",
            ref_no=ref_no,
            trans_date=record.trans_date,
            year=record.year,
            month=record.month
        )


    # -----------------------------
    # Insert deposited but not show bank book Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"deposited_but_not_show_bank_book_date_{i}")
        amount = request.POST.get(f"deposited_but_not_show_bank_book_amount_{i}")
        ref_no = request.POST.get(f"deposited_but_not_show_bank_book_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=request_id,
            cid=cid,
            trans_sl=record.sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="DEPOSITED_BUT_NOT_SHOW_BANK_BOOK",
            ref_no=ref_no,
            trans_date=record.trans_date,
            year=record.year,
            month=record.month
        )

    # -----------------------------
    # Insert debited by bank but notShowing bank book Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"debited_by_bank_but_notShowing_bank_book_date_{i}")
        amount = request.POST.get(f"debited_by_bank_but_notShowing_bank_book_amount_{i}")
        ref_no = request.POST.get(f"debited_by_bank_but_notShowing_bank_book_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=request_id,
            cid=cid,
            trans_sl=record.sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK",
            ref_no=ref_no,
            trans_date=record.trans_date,
            year=record.year,
            month=record.month
        )


    # -----------------------------
    # Insert cheque issued Rows
    # -----------------------------
    for i in range(1, 11):   # also max 10 rows
        date_str = request.POST.get(f"cheque_issued_date_{i}")
        amount = request.POST.get(f"cheque_issued_amount_{i}")
        ref_no = request.POST.get(f"cheque_issued_ref_no_{i}")

        # ensure numeric value
        if not amount or amount in ('', 'None'):
            amount = 0
        else:
            amount = float(amount)

        # handle date
        entry_date = None
        if date_str:
            try:
                entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                pass

        db.tr_impr_bnk_d.insert(
            trans_id=request_id,
            cid=cid,
            trans_sl=record.sl,
            branch_id=branch_id,
            branch_code=branchRecord.code,
            bank_id=bank_id,
            account_number=account_number,
            entry_date=entry_date,
            amount=amount,
            types="CHEQUE_ISSUED",
            ref_no=ref_no,
            trans_date=record.trans_date,
            year=record.year,
            month=record.month
        )
        
        
    flash.set('Record updated successfully', 'success')
    redirect(URL('imprest_bank_reconciliation','index'))  


@action("imprest_bank_reconciliation/delete")
@action.uses("imprest_bank_reconciliation/index.html",session,flash,db)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    cid = session.get('cid')
    request_id = request.query.get('id')
    if request_id:
        db((db.tr_impr_bnk_h.cid == cid) & (db.tr_impr_bnk_h.id == request_id)).delete()
        db((db.tr_impr_bnk_d.cid == cid) & (db.tr_impr_bnk_d.trans_id == request_id)).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('imprest_bank_reconciliation', 'index')))

    return locals()


@action("imprest_bank_reconciliation/get_data", method=['GET', 'POST'])
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
                conditions += " AND b.id IN ({})".format(
                    ",".join("'{}'".format(branch_id) for branch_id in branch_id_list)
                )

    
    if  request.query.get('branch_name') != None and request.query.get('branch_name') !='':
        conditions += " and ba.branch_id = '"+str(request.query.get('branch_name'))+"'"

    if  request.query.get('from_date') != None and request.query.get('from_date') !='' and  request.query.get('to_date') != None and request.query.get('to_date') !='':
        conditions += " and ba.trans_date >= '"+str(request.query.get('from_date'))+"' and ba.trans_date <= '"+str(request.query.get('to_date'))+"'" 

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and ba.status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( """SELECT 
    ba.id AS id,
    ba.sl AS sl,
    ba.trans_date AS trans_date,
    b.name AS branch_name,
    bk.name AS bank_name,
    ba.account_number AS account_number,
    ba.opening_balance AS opening_balance,
    ba.closing_per_bank AS closing_per_bank,
    ba.closing_per_bank_book AS closing_per_bank_book,
    ba.month AS month,
    ba.status AS status
    FROM tr_impr_bnk_h ba
    LEFT JOIN
        branch b ON ba.branch_id = b.id
    LEFT JOIN
        bank bk ON ba.bank_id = bk.id where 1 """+conditions, as_dict=True))

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
    ba.id AS id,
    ba.sl AS sl,
    ba.trans_date AS trans_date,
    b.name AS branch_name,
    bk.name AS bank_name,
    ba.account_number AS account_number,
    ba.opening_balance AS opening_balance,
    ba.closing_per_bank AS closing_per_bank,
    ba.closing_per_bank_book AS closing_per_bank_book,
    ba.month AS month,
    ba.status AS status 
    FROM tr_impr_bnk_h ba    
    LEFT JOIN
        branch b ON ba.branch_id = b.id
    LEFT JOIN
        bank bk ON ba.bank_id = bk.id
    WHERE 1 """ + conditions + """ ORDER BY """ + sort_column_name + """ """ + sort_direction + """ LIMIT """ + str(start) + """, """ + str(end) + """;
    """
    print(sql)
    data = db.executesql(sql, as_dict=True)    

    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
