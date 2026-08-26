from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_fn import check_role, easy_format
from ..common_cid import date_time_list
from datetime import datetime, timedelta
import csv
import io

@action("report/index")
@action.uses("report/index.html",session,flash,db)
def index(id=None):
    task_id='report_manage'
    task_id_view='report_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    cid = session.get('cid')    
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
    segmentList = db(db.segment.status == 1).select()  
    brandList = db(db.brand.status == 1).select() 
      
    formatted_date=date_time_list["date_fixed"].strftime(date_time_list["date_format"])
    month_first_date = formatted_date[:7] + "-01"
    
    mr_deposit_report_btn = request.forms.get('mr_deposit_report_btn')
    collection_deposit_report_btn = request.forms.get('collection_deposit_report_btn')
    date_wise_imprest_money_cash_report_btn = request.forms.get('date_wise_imprest_money_cash_report_btn')
    date_wise_imprest_money_bank_report_btn = request.forms.get('date_wise_imprest_money_bank_report_btn')
    branch_wise_imprest_money_cash_reconciliation_report_btn = request.forms.get('branch_wise_imprest_money_cash_reconciliation_report_btn')
    branch_wise_imprest_money_bank_reconciliation_report_btn = request.forms.get('branch_wise_imprest_money_bank_reconciliation_report_btn')
    branch_wise_outstanding_report_btn = request.forms.get('branch_wise_outstanding_report_btn')
    
    brand_wise_outstanding_reconciliation_report_btn = request.forms.get('brand_wise_outstanding_reconciliation_report_btn')
    branch_brand_wise_outstanding_summary_report_btn = request.forms.get('branch_brand_wise_outstanding_summary_report_btn')
    brand_wise_collection_reconciliation_report_btn = request.forms.get('brand_wise_collection_reconciliation_report_btn')
    consolidate_bank_reconciliation_statement_btn = request.forms.get('consolidate_bank_reconciliation_statement_btn')

    if mr_deposit_report_btn or collection_deposit_report_btn or date_wise_imprest_money_cash_report_btn or date_wise_imprest_money_bank_report_btn or branch_wise_imprest_money_cash_reconciliation_report_btn or branch_wise_imprest_money_bank_reconciliation_report_btn or branch_wise_outstanding_report_btn or brand_wise_outstanding_reconciliation_report_btn or branch_brand_wise_outstanding_summary_report_btn or brand_wise_collection_reconciliation_report_btn or consolidate_bank_reconciliation_statement_btn:   

        fromDt = request.params.get('from_date')
        toDt = request.params.get('to_date')
        yearCombo = request.params.get('yearCombo')
        monthCombo = request.params.get('monthCombo')
        
        dateFlag = True
        dateFlagRange = True

        try:
            startDate = datetime.strptime(fromDt, '%Y-%m-%d')
            endDate = datetime.strptime(toDt, '%Y-%m-%d') #+ timedelta(days=1)
            if startDate > endDate:
                dateFlag = False
            elif (endDate - startDate).days > 366:
                dateFlagRange = False

        except Exception:
            dateFlag = False
            dateFlagRange = False
        
        branch = request.forms.get('branch')
        segment = request.forms.get('segment')
        brand = request.forms.get('brand')
        session.rep_branch=branch
        session.rep_segment=segment
        session.rep_brand=brand
        session.yearCombo=yearCombo
        session.monthCombo=monthCombo
        if dateFlag:
            session.rep_fromDt = startDate.strftime('%Y-%m-%d')
            session.rep_toDt = endDate.strftime('%Y-%m-%d')
        else:
            session.rep_fromDt = fromDt
            session.rep_toDt = toDt
        if mr_deposit_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'mr_deposit_report'
                )
            )
        if collection_deposit_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'collection_deposit_report'
                )
            )
        if date_wise_imprest_money_cash_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'date_wise_imprest_money_cash_report'
                )
            )
        if date_wise_imprest_money_bank_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'date_wise_imprest_money_bank_report'
                )
            )
        if branch_wise_imprest_money_cash_reconciliation_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'branch_wise_imprest_money_cash_reconciliation_report'
                )
            )
        if branch_wise_imprest_money_bank_reconciliation_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'branch_wise_imprest_money_bank_reconciliation_report'
                )
            )
        if branch_wise_outstanding_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'branch_wise_outstanding_report'
                )
            )
        
        if branch_brand_wise_outstanding_summary_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'branch_brand_wise_outstanding_summary_report'
                )
            )
        if brand_wise_outstanding_reconciliation_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'brand_wise_outstanding_reconciliation_report'
                )
            )
        
        if brand_wise_collection_reconciliation_report_btn:
            if dateFlag == False:
                flash.set('Invalid Date !', 'warning')
            elif dateFlagRange == False:
                flash.set("Period not more then 1 year", 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'brand_wise_collection_reconciliation_report'
                )
            )
        
        if consolidate_bank_reconciliation_statement_btn:
            if not yearCombo:
                flash.set('Invalid Year !', 'warning')
            elif not monthCombo:
                flash.set('Invalid Month !', 'warning')
            else:
                redirect(
                URL(
                    'report',
                    'consolidate_bank_reconciliation_statement'
                )
            )
        



    return dict(month_first_date=month_first_date,access_permission=access_permission,access_permission_view=access_permission_view,session=session,check_role=check_role,branchList=branchList,segmentList=segmentList,brandList=brandList,formatted_date=formatted_date)

@action("report/get_brands_by_segment")
@action.uses(db)
def get_brands_by_segment():
    segments = request.params.get('segments')
    if not segments:
        brands = db(db.brand.status == 1).select(db.brand.id, db.brand.name, orderby=db.brand.name)
    else:
        segment_list = [int(s) for s in segments.split(',') if s.strip()]
        brands = db((db.brand.status == 1) & (db.brand.segment_id.belongs(segment_list))).select(db.brand.id, db.brand.name, orderby=db.brand.name)
    
    return dict(brands=[dict(id=b.id, name=b.name) for b in brands])

@action("report/mr_deposit_report")
@action.uses("report/mr_deposit_report.html",session,flash,db)
def mr_deposit_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []
    
    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # print(f"Branch: {branch}, Segment: {segment}")
    
    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    # To get the correct Opening Balance for startDate, we need to find the latest
    # balance record (checkpoint) on or before startDate for each branch, 
    # and then pull all transactions since the earliest of those checkpoints.
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    # print(check_query)
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])
    
    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.total_mr)         AS total_mr,
        SUM(f.mr_reverse)       AS mr_reverse,

        SUM(f.pharma_plus)      AS pharma_plus,
        SUM(f.cbd_plus)         AS cbd_plus,
        SUM(f.diagnostic_plus)  AS diagnostic_plus,

        SUM(f.pharma_minus)     AS pharma_minus,
        SUM(f.cbd_minus)        AS cbd_minus,
        SUM(f.diagnostic_minus) AS diagnostic_minus,

        SUM(f.short_receipt)      AS short_receipt,

        SUM(f.total_deposit)    AS total_deposit,
        0 AS closing_balance

    FROM
    (
        /* ===== RECEIPT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,

            SUM(d.money_receipt) AS total_mr,
            SUM(d.mr_reverse) AS mr_reverse,

            SUM(CASE WHEN d.segment_name = 'Pharma' THEN d.adv_receipt ELSE 0 END) AS pharma_plus,
            SUM(CASE WHEN d.segment_name = 'CBD' THEN d.adv_receipt ELSE 0 END) AS cbd_plus,
            SUM(CASE WHEN d.segment_name = 'DIAGNOSTIC' THEN d.adv_receipt ELSE 0 END) AS diagnostic_plus,

            SUM(CASE WHEN d.segment_name = 'Pharma' THEN d.adv_adj ELSE 0 END) AS pharma_minus,
            SUM(CASE WHEN d.segment_name = 'CBD' THEN d.adv_adj ELSE 0 END) AS cbd_minus,
            SUM(CASE WHEN d.segment_name = 'DIAGNOSTIC' THEN d.adv_adj ELSE 0 END) AS diagnostic_minus,

            SUM(d.short_receipt)      AS short_receipt,

            0 AS total_deposit,
            0 AS closing_balance

        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== DEPOSIT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            0 AS total_mr,
            0 AS mr_reverse,

            0 AS pharma_plus,
            0 AS cbd_plus,
            0 AS diagnostic_plus,

            0 AS pharma_minus,
            0 AS cbd_minus,
            0 AS diagnostic_minus,
            0 AS short_receipt,

            SUM(d.amount) AS total_deposit,
            0 AS closing_balance

        FROM cashier.tr_deposit_h h
        JOIN cashier.tr_deposit_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            h.opening_balance as opening_balance,
            0 AS total_mr,
            0 AS mr_reverse,

            0 AS pharma_plus,
            0 AS cbd_plus,
            0 AS diagnostic_plus,

            0 AS pharma_minus,
            0 AS cbd_minus,
            0 AS diagnostic_minus,
            0 AS total_deposit,
            0 AS short_receipt,
            0 AS closing_balance

        FROM cashier.opening_h h  
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.branch_id, f.trans_date
    """

    print(query)

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()
    
    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()
        
        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    # All unique branches in the results (or selected branches)
    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance and starting date for each branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        # Find the latest balance checkpoint on or before start_dt
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            # Fallback to the first transaction date or start_dt
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt
    
    while temp_dt <= end_dt:
        # Aggregated row for this specific date
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'opening_balance': 0,
            'total_mr': 0, 'mr_reverse': 0,
            'pharma_plus': 0, 'cbd_plus': 0, 'diagnostic_plus': 0,
            'pharma_minus': 0, 'cbd_minus': 0, 'diagnostic_minus': 0,
            'short_receipt': 0,
            'total_deposit': 0, 'closing_balance': 0
        }
        
        has_activity = False # Tracks if any branch has data or started its timeline
        
        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue
            
            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})
            
            ob = state['running_bal']
            tmr = bid_data.get('total_mr') or 0
            mrev = bid_data.get('mr_reverse') or 0
            pp = bid_data.get('pharma_plus') or 0
            pm = bid_data.get('pharma_minus') or 0
            cp = bid_data.get('cbd_plus') or 0
            cm = bid_data.get('cbd_minus') or 0
            dp = bid_data.get('diagnostic_plus') or 0
            dm = bid_data.get('diagnostic_minus') or 0
            sr = bid_data.get('short_receipt') or 0
            tdep = bid_data.get('total_deposit') or 0
            
            # Daily calculation for this branch
            cb = ob + tmr - mrev + pp - pm + cp - cm + dp - dm + sr - tdep
            state['running_bal'] = cb # Carry over for next day
            
            # Aggregate into the daily row
            date_row['opening_balance'] += ob
            date_row['total_mr'] += tmr
            date_row['mr_reverse'] += mrev
            date_row['pharma_plus'] += pp
            date_row['pharma_minus'] += pm
            date_row['cbd_plus'] += cp
            date_row['cbd_minus'] += cm
            date_row['diagnostic_plus'] += dp
            date_row['diagnostic_minus'] += dm
            date_row['short_receipt'] += sr
            date_row['total_deposit'] += tdep
            date_row['closing_balance'] += cb

        if temp_dt >= start_dt and has_activity:
            # Rounding for display
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            recordList.append(date_row)
            
        temp_dt += timedelta(days=1)

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_mr_deposit_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_mr_deposit_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.get('cid')

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start
        FROM (
            SELECT MAX(trans_date) as max_dt
            FROM cashier.opening_h h
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.total_mr)         AS total_mr,
        SUM(f.mr_reverse)       AS mr_reverse,

        SUM(f.pharma_plus)      AS pharma_plus,
        SUM(f.cbd_plus)         AS cbd_plus,
        SUM(f.diagnostic_plus)  AS diagnostic_plus,

        SUM(f.pharma_minus)     AS pharma_minus,
        SUM(f.cbd_minus)        AS cbd_minus,
        SUM(f.diagnostic_minus) AS diagnostic_minus,
        SUM(f.short_receipt)    AS short_receipt,
        SUM(f.total_deposit)    AS total_deposit,
        0 AS closing_balance

    FROM
    (
        /* ===== RECEIPT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,

            SUM(d.money_receipt) AS total_mr,
            SUM(d.mr_reverse) AS mr_reverse,

            SUM(CASE WHEN d.segment_name = 'Pharma' THEN d.adv_receipt ELSE 0 END) AS pharma_plus,
            SUM(CASE WHEN d.segment_name = 'CBD' THEN d.adv_receipt ELSE 0 END) AS cbd_plus,
            SUM(CASE WHEN d.segment_name = 'DIAGNOSTIC' THEN d.adv_receipt ELSE 0 END) AS diagnostic_plus,

            SUM(CASE WHEN d.segment_name = 'Pharma' THEN d.adv_adj ELSE 0 END) AS pharma_minus,
            SUM(CASE WHEN d.segment_name = 'CBD' THEN d.adv_adj ELSE 0 END) AS cbd_minus,
            SUM(CASE WHEN d.segment_name = 'DIAGNOSTIC' THEN d.adv_adj ELSE 0 END) AS diagnostic_minus,

            SUM(d.short_receipt)    AS short_receipt,
            0 AS total_deposit,
            0 AS closing_balance

        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== DEPOSIT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            0 AS total_mr,
            0 AS mr_reverse,

            0 AS pharma_plus,
            0 AS cbd_plus,
            0 AS diagnostic_plus,

            0 AS pharma_minus,
            0 AS cbd_minus,
            0 AS diagnostic_minus,
            0 AS short_receipt,
            SUM(d.amount) AS total_deposit,
            0 AS closing_balance

        FROM cashier.tr_deposit_h h
        JOIN cashier.tr_deposit_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            h.opening_balance as opening_balance,
            0 AS total_mr,
            0 AS mr_reverse,

            0 AS pharma_plus,
            0 AS cbd_plus,
            0 AS diagnostic_plus,

            0 AS pharma_minus,
            0 AS cbd_minus,
            0 AS diagnostic_minus,
            0 AS short_receipt,
            0 AS total_deposit,
            0 AS closing_balance

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'

        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.branch_id, f.trans_date
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic (identical to mr_deposit_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()

    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()

        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt

    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'opening_balance': 0,
            'total_mr': 0, 'mr_reverse': 0,
            'pharma_plus': 0, 'cbd_plus': 0, 'diagnostic_plus': 0,
            'pharma_minus': 0, 'cbd_minus': 0, 'diagnostic_minus': 0,
            'short_receipt': 0,
            'total_deposit': 0, 'closing_balance': 0
        }

        has_activity = False

        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue

            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})

            ob = state['running_bal']
            tmr = bid_data.get('total_mr') or 0
            mrev = bid_data.get('mr_reverse') or 0
            pp = bid_data.get('pharma_plus') or 0
            pm = bid_data.get('pharma_minus') or 0
            cp = bid_data.get('cbd_plus') or 0
            cm = bid_data.get('cbd_minus') or 0
            dp = bid_data.get('diagnostic_plus') or 0
            dm = bid_data.get('diagnostic_minus') or 0
            sr = bid_data.get('short_receipt') or 0
            tdep = bid_data.get('total_deposit') or 0

            cb = ob + tmr - mrev + pp - pm + cp - cm + dp - dm + sr - tdep
            state['running_bal'] = cb

            date_row['opening_balance'] += ob
            date_row['total_mr'] += tmr
            date_row['mr_reverse'] += mrev
            date_row['pharma_plus'] += pp
            date_row['pharma_minus'] += pm
            date_row['cbd_plus'] += cp
            date_row['cbd_minus'] += cm
            date_row['diagnostic_plus'] += dp
            date_row['diagnostic_minus'] += dm
            date_row['short_receipt'] += sr
            date_row['total_deposit'] += tdep
            date_row['closing_balance'] += cb

        if temp_dt >= start_dt and has_activity:
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            recordList.append(date_row)

        temp_dt += timedelta(days=1)

    # --- Step 4: Build the CSV ---
    # import csv
    # import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["1.1 MR & Deposit Reconciliation Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Date', 'trans_date'),
        ('Opening Balance', 'opening_balance'),
        ('Total MR', 'total_mr'),
        ('MR Reverse', 'mr_reverse'),
        ('Pharma Adv.', 'pharma_plus'),
        ('Pharma Adj.', 'pharma_minus'),
        ('CBD Adv.', 'cbd_plus'),
        ('CBD Adj.', 'cbd_minus'),
        ('Diagnostic Adv.', 'diagnostic_plus'),
        ('Diagnostic Adj.', 'diagnostic_minus'),
        ('Short Receipt', 'short_receipt'),
        ('Total Deposit', 'total_deposit'),
        ('Closing Balance', 'closing_balance'),
    ]

    writer.writerow([col[0] for col in export_columns])

    totals = {key: 0 for _, key in export_columns if key != 'trans_date'}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in totals:
            totals[key] += row.get(key) or 0

    # Total row (mirrors the HTML table's footer row; Closing Balance left blank, as in index.html)
    total_row = ['Total', '']
    total_row += [
        totals['total_mr'], totals['mr_reverse'],
        totals['pharma_plus'], totals['pharma_minus'],
        totals['cbd_plus'], totals['cbd_minus'],
        totals['diagnostic_plus'], totals['diagnostic_minus'],
        totals['short_receipt'],
        totals['total_deposit'], ''
    ]
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="MR_Deposit_Reconciliation_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility
  
# @action("report/collection_deposit_report")
# @action.uses("report/collection_deposit_report.html",session,flash,db)
# def collection_deposit_report():
#     branch = session.rep_branch
#     segment = session.rep_segment
#     brand = session.rep_brand
#     startDate = session.rep_fromDt
#     endDate = session.rep_toDt
#     cid = session.cid

#     # Normalize inputs to lists of non-empty strings
#     if branch:
#         if not isinstance(branch, (list, tuple)): branch = [branch]
#         branch = [str(b) for b in branch if str(b).strip()]
#     else:
#         branch = []

#     if segment:
#         if not isinstance(segment, (list, tuple)): segment = [segment]
#         segment = [str(s) for s in segment if str(s).strip()]
#     else:
#         segment = []

#     if brand:
#         if not isinstance(brand, (list, tuple)): brand = [brand]
#         brand = [str(b) for b in brand if str(b).strip()]
#     else:
#         brand = []

#     # Safe retrieval of branch name
#     branch_name = "All Branches"
#     if branch:
#         branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
#         if branch_rows:
#             branch_name = ", ".join([r.name for r in branch_rows])

#     # Filter conditions
#     branch_cond = ""
#     if branch:
#         branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

#     segment_cond = ""
#     if segment:
#         segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

#     brand_cond = ""
#     if brand:
#         brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

#     # --- Step 1: Find the History Start ---
#     # We need to find the latest balance checkpoint on or before startDate for each branch
#     check_query = f"""
#         SELECT MIN(max_dt) as history_start 
#         FROM (
#             SELECT MAX(trans_date) as max_dt 
#             FROM cashier.opening_h h 
#             WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
#             {branch_cond}
#             GROUP BY h.branch_id
#         ) t
#     """
#     res = db.executesql(check_query, as_dict=True)
#     historyStart = startDate
#     if res and res[0]['history_start']:
#         historyStart = str(res[0]['history_start'])

#     # --- Step 2: Main Data Query ---
#     query = f"""
#     SELECT
#         f.cid,
#         f.branch_id,
#         f.trans_date,

#         SUM(f.opening_balance)  AS opening_balance,
#         SUM(f.collection)       AS collection,
#         SUM(f.total_deposit)    AS total_deposit,
#         SUM(f.payment_to_imprest) AS payment_to_imprest,
#         SUM(f.adv_receipt)      AS adv_receipt,
#         SUM(f.adv_adj)          AS adv_adj,
#         SUM(f.as_per_physical)  AS as_per_physical,
#         0 AS closing_balance,
#         0 AS difference       

#     FROM
#     (
#         /* ===== RECEIPT ===== */
#         SELECT
#             h.cid,
#             h.branch_id,
#             h.trans_date,

#             0 AS opening_balance,
#             SUM(d.money_receipt) AS collection,
#             0 AS total_deposit,
#             0 AS payment_to_imprest,
#             SUM(d.adv_receipt) AS adv_receipt,
#             SUM(d.adv_adj) AS adv_adj,
#             0 AS as_per_physical            

#         FROM cashier.tr_receipt_h h
#         JOIN cashier.tr_receipt_d d ON h.id = d.trans_id

#         WHERE h.cid = '{cid}'
#         AND h.trans_date >= '{historyStart}'
#         AND h.trans_date <= '{endDate}'
#         {branch_cond}
#         {segment_cond}
#         {brand_cond}

#         GROUP BY h.cid, h.branch_id, h.trans_date


#         UNION ALL


#         /* ===== DEPOSIT ===== */
#         SELECT
#             h.cid,
#             h.branch_id,
#             h.trans_date,

#             0 AS opening_balance,
#             0 AS collection,
#             SUM(d.amount) AS total_deposit,
#             0 AS payment_to_imprest,
#             0 AS adv_receipt,
#             0 AS adv_adj,
#             0 AS as_per_physical

#         FROM cashier.tr_deposit_h h
#         JOIN cashier.tr_deposit_d d ON h.id = d.trans_id

#         WHERE h.cid = '{cid}'
#         AND h.trans_date >= '{historyStart}'
#         AND h.trans_date <= '{endDate}'
#         {branch_cond}
#         {segment_cond}
#         {brand_cond}

#         GROUP BY h.cid, h.branch_id, h.trans_date


#         UNION ALL


#         /* ===== BALANCE CHECKPOINT ===== */
#         SELECT
#             h.cid,
#             h.branch_id,
#             h.trans_date,

#             h.opening_balance AS opening_balance,
#             0 AS collection,
#             0 AS total_deposit,
#             0 AS payment_to_imprest,
#             0 AS adv_receipt,
#             0 AS adv_adj,
#             0 AS as_per_physical

#         FROM cashier.opening_h h
#         JOIN cashier.opening_d d ON h.id = d.trans_id

#         WHERE h.cid = '{cid}'        
        
#         GROUP BY h.cid, h.branch_id, h.trans_date

#     ) f

#     GROUP BY f.cid, f.branch_id, f.trans_date
#     ORDER BY f.trans_date, f.branch_id
#     """

#     recordListRaw = db.executesql(query, as_dict=True)

#     # --- Step 3: Process and Aggregation Logic ---
#     start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
#     end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
#     historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()
    
#     data_map = {}
#     for row in recordListRaw:
#         bid = row['branch_id']
#         dt = row['trans_date']
#         if isinstance(dt, str):
#             dt = datetime.strptime(dt, '%Y-%m-%d').date()
        
#         if bid not in data_map:
#             data_map[bid] = {}
#         data_map[bid][dt] = row

#     branches_to_process = []
#     if branch:
#         branches_to_process = [int(b) for b in branch]
#     else:
#         branches_to_process = sorted(list(data_map.keys()))

#     # Initialize running balance per branch
#     branch_states = {}
#     for bid in branches_to_process:
#         bid_data = data_map.get(bid, {})
#         balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
#         if balance_dates:
#             checkpoint_dt = balance_dates[-1]
#             branch_states[bid] = {
#                 'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
#                 'start_dt': checkpoint_dt
#             }
#         else:
#             trans_dates = sorted(bid_data.keys())
#             branch_states[bid] = {
#                 'running_bal': 0,
#                 'start_dt': trans_dates[0] if trans_dates else start_dt
#             }

#     recordList = []
#     temp_dt = historyStart_dt
    
#     while temp_dt <= end_dt:
#         date_row = {
#             'trans_date': temp_dt.strftime('%d-%b-%Y'),
#             'opening_balance': 0,
#             'collection': 0,
#             'total_deposit': 0,
#             'payment_to_imprest': 0,
#             'closing_balance': 0,
#             'adv_receipt': 0,
#             'adv_adj': 0,
#             'as_per_physical': 0,
#             'difference': 0
#         }
        
#         has_activity = False
        
#         for bid in branches_to_process:
#             state = branch_states[bid]
#             if temp_dt < state['start_dt']:
#                 continue
            
#             has_activity = True
#             bid_data = data_map.get(bid, {}).get(temp_dt, {})
            
#             ob = state['running_bal']
#             coll = bid_data.get('collection') or 0
#             tdep = bid_data.get('total_deposit') or 0
#             pimpr = bid_data.get('payment_to_imprest') or 0
            
#             # Formula: Closing = Opening + Collection - Deposit - PaymentToImprest
#             cb = ob + coll - tdep - pimpr
#             state['running_bal'] = cb
            
#             # Other fields
#             ar = bid_data.get('adv_receipt') or 0
#             aa = bid_data.get('adv_adj') or 0
#             app = bid_data.get('as_per_physical') or 0
            
#             # Aggregation
#             date_row['opening_balance'] += ob
#             date_row['collection'] += coll
#             date_row['total_deposit'] += tdep
#             date_row['payment_to_imprest'] += pimpr
#             date_row['closing_balance'] += cb
#             date_row['adv_receipt'] += ar
#             date_row['adv_adj'] += aa
#             date_row['as_per_physical'] += app

#         if temp_dt >= start_dt and has_activity:
#             # Final touchups
#             date_row['closing_balance'] = round(date_row['closing_balance'], 2)
#             if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            
#             # Difference = Closing - As Per Physical
#             date_row['difference'] = round(date_row['closing_balance'] - date_row['as_per_physical'], 2)
#             if date_row['difference'] == 0: date_row['difference'] = 0.0
            
#             recordList.append(date_row)
            
#         temp_dt += timedelta(days=1)

#     return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)


@action("report/collection_deposit_report")
@action.uses("report/collection_deposit_report.html",session,flash,db)
def collection_deposit_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    # We need to find the latest balance checkpoint on or before startDate for each branch
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.collection)       AS collection,
        SUM(f.total_deposit)    AS total_deposit,
        SUM(f.payment_to_imprest) AS payment_to_imprest,
        SUM(f.adv_receipt)      AS adv_receipt,
        SUM(f.adv_adj)          AS adv_adj,
        SUM(f.as_per_physical)  AS as_per_physical,
        0 AS closing_balance,
        0 AS difference       

    FROM
    (
        /* ===== RECEIPT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            SUM(d.collection) AS collection,
            0 AS total_deposit,
            0 AS payment_to_imprest,
            SUM(d.adv_receipt) AS adv_receipt,
            SUM(d.adv_adj) AS adv_adj,
            0 AS as_per_physical            

        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== DEPOSIT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            0 AS collection,
            SUM(d.amount) AS total_deposit,
            0 AS payment_to_imprest,
            0 AS adv_receipt,
            0 AS adv_adj,
            0 AS as_per_physical

        FROM cashier.tr_deposit_h h
        JOIN cashier.tr_deposit_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date

         UNION ALL


        /* ===== Petty Cash Expense ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            0 AS collection,
            0 AS total_deposit,
            transfer_imprest_cash AS payment_to_imprest,
            0 AS adv_receipt,
            0 AS adv_adj,
            0 AS as_per_physical

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            h.opening_balance AS opening_balance,
            0 AS collection,
            0 AS total_deposit,
            0 AS payment_to_imprest,
            0 AS adv_receipt,
            0 AS adv_adj,
            0 AS as_per_physical

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()
    
    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()
        
        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance per branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt
    
    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'opening_balance': 0,
            'collection': 0,
            'total_deposit': 0,
            'payment_to_imprest': 0,
            'closing_balance': 0,
            'adv_receipt': 0,
            'adv_adj': 0,
            'as_per_physical': 0,
            'difference': 0
        }
        
        has_activity = False
        
        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue
            
            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})
            
            ob = state['running_bal']
            coll = bid_data.get('collection') or 0
            tdep = bid_data.get('total_deposit') or 0
            pimpr = bid_data.get('payment_to_imprest') or 0
            # Other fields
            ar = bid_data.get('adv_receipt') or 0
            aa = bid_data.get('adv_adj') or 0
            app = bid_data.get('as_per_physical') or 0
                        
            # Formula: Closing = Opening + Collection + Advance Receipt - Advance Adjustment - Deposit - PaymentToImprest
            cb = ob + coll - tdep
            state['running_bal'] = cb
            
            # Aggregation
            date_row['opening_balance'] += ob
            date_row['collection'] += coll
            date_row['total_deposit'] += tdep
            date_row['payment_to_imprest'] += pimpr
            date_row['closing_balance'] += cb
            date_row['adv_receipt'] += ar
            date_row['adv_adj'] += aa
            date_row['as_per_physical'] += app

        if temp_dt >= start_dt and has_activity:
            # Final touchups
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            
            # Difference = Closing - As Per Physical
            date_row['difference'] = round(date_row['closing_balance'] - date_row['as_per_physical'], 2)
            if date_row['difference'] == 0: date_row['difference'] = 0.0
            
            recordList.append(date_row)
            
        temp_dt += timedelta(days=1)

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)


@action("report/download_collection_deposit_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_collection_deposit_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.collection)       AS collection,
        SUM(f.total_deposit)    AS total_deposit,
        SUM(f.payment_to_imprest) AS payment_to_imprest,
        SUM(f.adv_receipt)      AS adv_receipt,
        SUM(f.adv_adj)          AS adv_adj,
        SUM(f.as_per_physical)  AS as_per_physical,
        0 AS closing_balance,
        0 AS difference       

    FROM
    (
        /* ===== RECEIPT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            SUM(d.collection) AS collection,
            0 AS total_deposit,
            0 AS payment_to_imprest,
            SUM(d.adv_receipt) AS adv_receipt,
            SUM(d.adv_adj) AS adv_adj,
            0 AS as_per_physical            

        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== DEPOSIT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            0 AS opening_balance,
            0 AS collection,
            SUM(d.amount) AS total_deposit,
            0 AS payment_to_imprest,
            0 AS adv_receipt,
            0 AS adv_adj,
            0 AS as_per_physical

        FROM cashier.tr_deposit_h h
        JOIN cashier.tr_deposit_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        {segment_cond}
        {brand_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,

            h.opening_balance AS opening_balance,
            0 AS collection,
            0 AS total_deposit,
            0 AS payment_to_imprest,
            0 AS adv_receipt,
            0 AS adv_adj,
            0 AS as_per_physical

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic (identical to collection_deposit_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()

    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()

        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance per branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt

    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'opening_balance': 0,
            'collection': 0,
            'total_deposit': 0,
            'payment_to_imprest': 0,
            'closing_balance': 0,
            'adv_receipt': 0,
            'adv_adj': 0,
            'as_per_physical': 0,
            'difference': 0
        }

        has_activity = False

        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue

            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})

            ob = state['running_bal']
            coll = bid_data.get('collection') or 0
            tdep = bid_data.get('total_deposit') or 0
            pimpr = bid_data.get('payment_to_imprest') or 0

            ar = bid_data.get('adv_receipt') or 0
            aa = bid_data.get('adv_adj') or 0
            app = bid_data.get('as_per_physical') or 0

            # Formula: Closing = Opening + Collection + Advance Receipt - Advance Adjustment - Deposit - PaymentToImprest
            cb = ob + coll - tdep
            state['running_bal'] = cb

            date_row['opening_balance'] += ob
            date_row['collection'] += coll
            date_row['total_deposit'] += tdep
            date_row['payment_to_imprest'] += pimpr
            date_row['closing_balance'] += cb
            date_row['adv_receipt'] += ar
            date_row['adv_adj'] += aa
            date_row['as_per_physical'] += app

        if temp_dt >= start_dt and has_activity:
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0

            date_row['difference'] = round(date_row['closing_balance'] - date_row['as_per_physical'], 2)
            if date_row['difference'] == 0: date_row['difference'] = 0.0

            recordList.append(date_row)

        temp_dt += timedelta(days=1)

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Collection & Deposit Reconciliation Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Date', 'trans_date'),
        ('Opening Balance', 'opening_balance'),
        ('Collection', 'collection'),
        ('Total Deposit', 'total_deposit'),
        ('Payment To Imprest', 'payment_to_imprest'),
        ('Adv Receipt', 'adv_receipt'),
        ('Adv Adj', 'adv_adj'),
        ('Closing Balance', 'closing_balance'),
        ('As Per Physical', 'as_per_physical'),
        ('Difference', 'difference'),
    ]

    writer.writerow([col[0] for col in export_columns])

    totals = {key: 0 for _, key in export_columns if key != 'trans_date'}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in totals:
            totals[key] += row.get(key) or 0

    # Total row (Closing Balance / Difference left blank since they're running balances, not sums)
    total_row = ['Total', '']
    total_row += [
        totals['collection'], totals['total_deposit'], totals['payment_to_imprest'],
        totals['adv_receipt'], totals['adv_adj'], '', totals['as_per_physical'], ''
    ]
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Collection_Deposit_Reconciliation_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility


@action("report/date_wise_imprest_money_cash_report")
@action.uses("report/date_wise_imprest_money_cash_report.html",session,flash,db)
def date_wise_imprest_money_cash_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,
        f.time,
        f.checked_by,
        f.verified_by,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.transfer_imprest_cash)     AS total_receipt,
        SUM(f.m_receipt)                 AS miss_receipt,
        SUM(f.total_exp)                 AS total_expenses,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            
            0 AS opening_balance,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.m_receipt) AS m_receipt,
            SUM(h.total_exp) AS total_exp

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        

        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            h.pc_cash_amount AS opening_balance,
            0 AS transfer_imprest_cash,
            0 AS m_receipt,
            0 AS total_exp

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()
    
    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()
        
        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance per branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt
    
    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'time': '-',
            'checked_by': '-',
            'verified_by': '-',
            'opening_balance': 0,
            'total_receipt': 0,
            'miss_receipt': 0,
            'total_expenses': 0,
            'closing_balance': 0
        }
        
        has_activity = False
        
        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue
            
            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})
            
            ob = state['running_bal']
            tr = bid_data.get('total_receipt') or 0
            mr = bid_data.get('miss_receipt') or 0
            te = bid_data.get('total_expenses') or 0
            
            # Formula: Closing = Opening + Total Receipt + Miss. Receipt - Total Expenses
            cb = ob + tr + mr - te
            state['running_bal'] = cb
            
            # Aggregation
            date_row['opening_balance'] += ob
            date_row['total_receipt'] += tr
            date_row['miss_receipt'] += mr
            date_row['total_expenses'] += te
            date_row['closing_balance'] += cb

        if temp_dt >= start_dt and has_activity:
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            recordList.append(date_row)
            
        temp_dt += timedelta(days=1)

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_date_wise_imprest_money_cash_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_date_wise_imprest_money_cash_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,
        f.time,
        f.checked_by,
        f.verified_by,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.transfer_imprest_cash)     AS total_receipt,
        SUM(f.m_receipt)                 AS miss_receipt,
        SUM(f.total_exp)                 AS total_expenses,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            
            0 AS opening_balance,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.m_receipt) AS m_receipt,
            SUM(h.total_exp) AS total_exp

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        

        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            h.pc_cash_amount AS opening_balance,
            0 AS transfer_imprest_cash,
            0 AS m_receipt,
            0 AS total_exp

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic (identical to date_wise_imprest_money_cash_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()

    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d').date()

        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance per branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt

    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'time': '-',
            'checked_by': '-',
            'verified_by': '-',
            'opening_balance': 0,
            'total_receipt': 0,
            'miss_receipt': 0,
            'total_expenses': 0,
            'closing_balance': 0
        }

        has_activity = False

        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue

            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})

            ob = state['running_bal']
            tr = bid_data.get('total_receipt') or 0
            mr = bid_data.get('miss_receipt') or 0
            te = bid_data.get('total_expenses') or 0

            # Formula: Closing = Opening + Total Receipt + Miss. Receipt - Total Expenses
            cb = ob + tr + mr - te
            state['running_bal'] = cb

            # Aggregation
            date_row['opening_balance'] += ob
            date_row['total_receipt'] += tr
            date_row['miss_receipt'] += mr
            date_row['total_expenses'] += te
            date_row['closing_balance'] += cb

        if temp_dt >= start_dt and has_activity:
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            recordList.append(date_row)

        temp_dt += timedelta(days=1)

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Date Wise Imprest Money Cash Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Date', 'trans_date'),
        ('Time', 'time'),
        ('Checked By', 'checked_by'),
        ('Verified By', 'verified_by'),
        ('Opening Balance', 'opening_balance'),
        ('Total Receipt', 'total_receipt'),
        ('Miss. Receipt', 'miss_receipt'),
        ('Total Expenses', 'total_expenses'),
        ('Closing Balance', 'closing_balance'),
    ]

    writer.writerow([col[0] for col in export_columns])

    numeric_keys = ['opening_balance', 'total_receipt', 'miss_receipt', 'total_expenses']
    totals = {key: 0 for key in numeric_keys}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in numeric_keys:
            totals[key] += row.get(key) or 0

    # Total row (Closing Balance left blank since it's a running balance, not a sum)
    total_row = ['Total', '', '', '', totals['opening_balance'], totals['total_receipt'], totals['miss_receipt'], totals['total_expenses'], '']
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Date_Wise_Imprest_Money_Cash_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/date_wise_imprest_money_bank_report")
@action.uses("report/date_wise_imprest_money_bank_report.html",session,flash,db)
def date_wise_imprest_money_bank_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,
        f.time,
        f.checked_by,
        f.verified_by,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.total_receipt_from_hq)     AS total_receipt_from_hq,
        SUM(f.transfer_imprest_cash)     AS transfer_imprest_cash,
        SUM(f.total_expense_cq)          AS total_expense_cq,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            
            0 AS opening_balance,
            SUM(h.total_receipt_hq) AS total_receipt_from_hq,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.total_expense_cq) AS total_expense_cq

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            h.pc_bank_amount AS opening_balance,
            0 AS total_receipt_from_hq,
            0 AS transfer_imprest_cash,
            0 AS total_expense_cq

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()
    
    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except:
                dt = date(1900, 1, 1)
        elif isinstance(dt, datetime):
            dt = dt.date()
        
        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance per branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt
    
    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'time': '-',
            'checked_by': '-',
            'verified_by': '-',
            'opening_balance': 0,
            'total_receipt_from_hq': 0,
            'transfer_imprest_cash': 0,
            'total_expense_cq': 0,
            'closing_balance': 0
        }
        
        has_activity = False
        
        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue
            
            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})
            
            ob = state['running_bal']
            hq = bid_data.get('total_receipt_from_hq') or 0
            tic = bid_data.get('transfer_imprest_cash') or 0
            ecq = bid_data.get('total_expense_cq') or 0
            
            # Formula: Closing = Opening + total_receipt_from_hq - transfer_imprest_cash - total_expense_cq
            cb = ob + hq - tic - ecq
            state['running_bal'] = cb
            
            # Aggregation
            date_row['opening_balance'] += ob
            date_row['total_receipt_from_hq'] += hq
            date_row['transfer_imprest_cash'] += tic
            date_row['total_expense_cq'] += ecq
            date_row['closing_balance'] += cb

        if temp_dt >= start_dt and has_activity:
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            recordList.append(date_row)
            
        temp_dt += timedelta(days=1)

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_date_wise_imprest_money_bank_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_date_wise_imprest_money_bank_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.trans_date,
        f.time,
        f.checked_by,
        f.verified_by,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.total_receipt_from_hq)     AS total_receipt_from_hq,
        SUM(f.transfer_imprest_cash)     AS transfer_imprest_cash,
        SUM(f.total_expense_cq)          AS total_expense_cq,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            
            0 AS opening_balance,
            SUM(h.total_receipt_hq) AS total_receipt_from_hq,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.total_expense_cq) AS total_expense_cq

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.trans_date,
            '-' as time,
            '-' as checked_by,
            '-' as verified_by,
            h.pc_bank_amount AS opening_balance,
            0 AS total_receipt_from_hq,
            0 AS transfer_imprest_cash,
            0 AS total_expense_cq

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic (identical to date_wise_imprest_money_bank_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    historyStart_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()

    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except:
                dt = date(1900, 1, 1)
        elif isinstance(dt, datetime):
            dt = dt.date()

        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row

    branches_to_process = []
    if branch:
        branches_to_process = [int(b) for b in branch]
    else:
        branches_to_process = sorted(list(data_map.keys()))

    # Initialize running balance per branch
    branch_states = {}
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            branch_states[bid] = {
                'running_bal': bid_data[checkpoint_dt].get('opening_balance') or 0,
                'start_dt': checkpoint_dt
            }
        else:
            trans_dates = sorted(bid_data.keys())
            branch_states[bid] = {
                'running_bal': 0,
                'start_dt': trans_dates[0] if trans_dates else start_dt
            }

    recordList = []
    temp_dt = historyStart_dt

    while temp_dt <= end_dt:
        date_row = {
            'trans_date': temp_dt.strftime('%d-%b-%Y'),
            'time': '-',
            'checked_by': '-',
            'verified_by': '-',
            'opening_balance': 0,
            'total_receipt_from_hq': 0,
            'transfer_imprest_cash': 0,
            'total_expense_cq': 0,
            'closing_balance': 0
        }

        has_activity = False

        for bid in branches_to_process:
            state = branch_states[bid]
            if temp_dt < state['start_dt']:
                continue

            has_activity = True
            bid_data = data_map.get(bid, {}).get(temp_dt, {})

            ob = state['running_bal']
            hq = bid_data.get('total_receipt_from_hq') or 0
            tic = bid_data.get('transfer_imprest_cash') or 0
            ecq = bid_data.get('total_expense_cq') or 0

            # Formula: Closing = Opening + total_receipt_from_hq - transfer_imprest_cash - total_expense_cq
            cb = ob + hq - tic - ecq
            state['running_bal'] = cb

            # Aggregation
            date_row['opening_balance'] += ob
            date_row['total_receipt_from_hq'] += hq
            date_row['transfer_imprest_cash'] += tic
            date_row['total_expense_cq'] += ecq
            date_row['closing_balance'] += cb

        if temp_dt >= start_dt and has_activity:
            date_row['closing_balance'] = round(date_row['closing_balance'], 2)
            if date_row['closing_balance'] == 0: date_row['closing_balance'] = 0.0
            recordList.append(date_row)

        temp_dt += timedelta(days=1)

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Date Wise Imprest Money Bank Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Date', 'trans_date'),
        ('Time', 'time'),
        ('Checked By', 'checked_by'),
        ('Verified By', 'verified_by'),
        ('Opening Balance', 'opening_balance'),
        ('Total Receipt From HQ', 'total_receipt_from_hq'),
        ('Transfer Imprest Cash', 'transfer_imprest_cash'),
        ('Total Expense (CQ)', 'total_expense_cq'),
        ('Closing Balance', 'closing_balance'),
    ]

    writer.writerow([col[0] for col in export_columns])

    numeric_keys = ['opening_balance', 'total_receipt_from_hq', 'transfer_imprest_cash', 'total_expense_cq']
    totals = {key: 0 for key in numeric_keys}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in numeric_keys:
            totals[key] += row.get(key) or 0

    # Total row (Closing Balance left blank since it's a running balance, not a sum)
    total_row = ['Total', '', '', '', totals['opening_balance'], totals['total_receipt_from_hq'], totals['transfer_imprest_cash'], totals['total_expense_cq'], '']
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Date_Wise_Imprest_Money_Bank_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/branch_wise_imprest_money_cash_reconciliation_report")
@action.uses("report/branch_wise_imprest_money_cash_reconciliation_report.html",session,flash,db)
def branch_wise_imprest_money_cash_reconciliation_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.branch_name,
        f.trans_date,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.transfer_imprest_cash)     AS total_receipt,
        SUM(f.m_receipt)                 AS miss_receipt,
        SUM(f.total_exp)                 AS total_expenses,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            
            0 AS opening_balance,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.m_receipt) AS m_receipt,
            SUM(h.total_exp) AS total_exp

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */

        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            h.pc_cash_amount AS opening_balance,
            0 AS transfer_imprest_cash,
            0 AS m_receipt,
            0 AS total_exp

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    
    data_map = {}
    branch_names = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except:
                dt = date(1900, 1, 1)
        elif isinstance(dt, datetime):
            dt = dt.date()
        
        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row
        if row['branch_name'] and row['branch_name'] != '-':
            branch_names[bid] = row['branch_name']

    branches_to_process = sorted(list(data_map.keys()))

    recordList = []
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        
        # 1. Find Initial Balance
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        running_bal = 0
        current_dt = start_dt
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates:
                current_dt = trans_dates[0]
        
        # Play forward to startDate
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            tr = day_data.get('total_receipt') or 0
            mr = day_data.get('miss_receipt') or 0
            te = day_data.get('total_expenses') or 0
            running_bal = running_bal + tr + mr - te
            current_dt += timedelta(days=1)
        
        # Now at startDate
        report_opening_balance = running_bal
        report_total_receipt = 0
        report_miss_receipt = 0
        report_total_expenses = 0
        
        # Accumulate within range
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            tr = day_data.get('total_receipt') or 0
            mr = day_data.get('miss_receipt') or 0
            te = day_data.get('total_expenses') or 0
            
            report_total_receipt += tr
            report_miss_receipt += mr
            report_total_expenses += te
            
            running_bal = running_bal + tr + mr - te
            current_dt += timedelta(days=1)
        
        # Add to results
        recordList.append({
            'branch_name': branch_names.get(bid, f"Branch {bid}"),
            'opening_balance': report_opening_balance,
            'total_receipt': report_total_receipt,
            'miss_receipt': report_miss_receipt,
            'total_expenses': report_total_expenses,
            'closing_balance': running_bal
        })

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_branch_wise_imprest_money_cash_reconciliation_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_branch_wise_imprest_money_cash_reconciliation_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.branch_name,
        f.trans_date,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.transfer_imprest_cash)     AS total_receipt,
        SUM(f.m_receipt)                 AS miss_receipt,
        SUM(f.total_exp)                 AS total_expenses,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            
            0 AS opening_balance,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.m_receipt) AS m_receipt,
            SUM(h.total_exp) AS total_exp

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */

        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            h.pc_cash_amount AS opening_balance,
            0 AS transfer_imprest_cash,
            0 AS m_receipt,
            0 AS total_exp

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic (identical to branch_wise_imprest_money_cash_reconciliation_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()

    data_map = {}
    branch_names = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except:
                dt = date(1900, 1, 1)
        elif isinstance(dt, datetime):
            dt = dt.date()

        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row
        if row['branch_name'] and row['branch_name'] != '-':
            branch_names[bid] = row['branch_name']

    branches_to_process = sorted(list(data_map.keys()))

    recordList = []
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})

        # 1. Find Initial Balance
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        running_bal = 0
        current_dt = start_dt

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates:
                current_dt = trans_dates[0]

        # Play forward to startDate
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            tr = day_data.get('total_receipt') or 0
            mr = day_data.get('miss_receipt') or 0
            te = day_data.get('total_expenses') or 0
            running_bal = running_bal + tr + mr - te
            current_dt += timedelta(days=1)

        # Now at startDate
        report_opening_balance = running_bal
        report_total_receipt = 0
        report_miss_receipt = 0
        report_total_expenses = 0

        # Accumulate within range
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            tr = day_data.get('total_receipt') or 0
            mr = day_data.get('miss_receipt') or 0
            te = day_data.get('total_expenses') or 0

            report_total_receipt += tr
            report_miss_receipt += mr
            report_total_expenses += te

            running_bal = running_bal + tr + mr - te
            current_dt += timedelta(days=1)

        # Add to results
        recordList.append({
            'branch_name': branch_names.get(bid, f"Branch {bid}"),
            'opening_balance': report_opening_balance,
            'total_receipt': report_total_receipt,
            'miss_receipt': report_miss_receipt,
            'total_expenses': report_total_expenses,
            'closing_balance': running_bal
        })

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Branch Wise Imprest Money Cash Reconciliation Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Branch Name', 'branch_name'),
        ('Opening Balance', 'opening_balance'),
        ('Total Receipt', 'total_receipt'),
        ('Miss. Receipt', 'miss_receipt'),
        ('Total Expenses', 'total_expenses'),
        ('Closing Balance', 'closing_balance'),
    ]

    writer.writerow([col[0] for col in export_columns])

    numeric_keys = ['opening_balance', 'total_receipt', 'miss_receipt', 'total_expenses', 'closing_balance']
    totals = {key: 0 for key in numeric_keys}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in numeric_keys:
            totals[key] += row.get(key) or 0

    # Total row
    total_row = ['Total', totals['opening_balance'], totals['total_receipt'], totals['miss_receipt'], totals['total_expenses'], totals['closing_balance']]
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Branch_Wise_Imprest_Money_Cash_Reconciliation_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/branch_wise_imprest_money_bank_reconciliation_report")
@action.uses("report/branch_wise_imprest_money_bank_reconciliation_report.html",session,flash,db)
def branch_wise_imprest_money_bank_reconciliation_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.branch_name,
        f.trans_date,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.total_receipt_from_hq)     AS total_receipt_from_hq,
        SUM(f.transfer_imprest_cash)     AS transfer_imprest_cash,
        SUM(f.total_expense_cq)          AS total_expense_cq,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            
            0 AS opening_balance,
            SUM(h.total_receipt_hq) AS total_receipt_from_hq,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.total_expense_cq) AS total_expense_cq

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.branch_name, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            h.pc_bank_amount AS opening_balance,
            0 AS total_receipt_from_hq,
            0 AS transfer_imprest_cash,
            0 AS total_expense_cq

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date


    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    
    data_map = {}
    branch_names = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except:
                dt = date(1900, 1, 1)
        elif isinstance(dt, datetime):
            dt = dt.date()
        
        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row
        if row['branch_name'] and row['branch_name'] != '-':
            branch_names[bid] = row['branch_name']

    branches_to_process = sorted(list(data_map.keys()))

    recordList = []
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        
        # 1. Find Initial Balance
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        running_bal = 0
        current_dt = start_dt
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates:
                current_dt = trans_dates[0]
        
        # Play forward to startDate
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            hq = day_data.get('total_receipt_from_hq') or 0
            tic = day_data.get('transfer_imprest_cash') or 0
            ecq = day_data.get('total_expense_cq') or 0
            running_bal = running_bal + hq - tic - ecq
            current_dt += timedelta(days=1)
        
        # Now at startDate
        report_opening_balance = running_bal
        report_total_receipt_from_hq = 0
        report_transfer_imprest_cash = 0
        report_total_expense_cq = 0
        
        # Accumulate within range
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            hq = day_data.get('total_receipt_from_hq') or 0
            tic = day_data.get('transfer_imprest_cash') or 0
            ecq = day_data.get('total_expense_cq') or 0
            
            report_total_receipt_from_hq += hq
            report_transfer_imprest_cash += tic
            report_total_expense_cq += ecq
            
            running_bal = running_bal + hq - tic - ecq
            current_dt += timedelta(days=1)
        
        # Filter: Only add if there is some activity or balance
        if abs(report_opening_balance) > 0.001 or \
           abs(report_total_receipt_from_hq) > 0.001 or \
           abs(report_transfer_imprest_cash) > 0.001 or \
           abs(report_total_expense_cq) > 0.001 or \
           abs(running_bal) > 0.001:
            
            recordList.append({
                'branch_name': branch_names.get(bid, f"Branch {bid}"),
                'opening_balance': report_opening_balance,
                'total_receipt_from_hq': report_total_receipt_from_hq,
                'transfer_imprest_cash': report_transfer_imprest_cash,
                'total_expense_cq': report_total_expense_cq,
                'closing_balance': running_bal
            })

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_branch_wise_imprest_money_bank_reconciliation_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_branch_wise_imprest_money_bank_reconciliation_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.branch_name,
        f.trans_date,

        SUM(f.opening_balance)           AS opening_balance,
        SUM(f.total_receipt_from_hq)     AS total_receipt_from_hq,
        SUM(f.transfer_imprest_cash)     AS transfer_imprest_cash,
        SUM(f.total_expense_cq)          AS total_expense_cq,
        0 AS closing_balance     

    FROM
    (
        /* ===== PETTY CASH ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            
            0 AS opening_balance,
            SUM(h.total_receipt_hq) AS total_receipt_from_hq,
            SUM(h.transfer_imprest_cash) AS transfer_imprest_cash,
            SUM(h.total_expense_cq) AS total_expense_cq

        FROM cashier.tr_petty_cash_h h

        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}

        GROUP BY h.cid, h.branch_id, h.branch_name, h.trans_date


        UNION ALL


        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            h.pc_bank_amount AS opening_balance,
            0 AS total_receipt_from_hq,
            0 AS transfer_imprest_cash,
            0 AS total_expense_cq

        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id

        WHERE h.cid = '{cid}'        
        
        GROUP BY h.cid, h.branch_id, h.trans_date


    ) f

    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Process and Aggregation Logic (identical to branch_wise_imprest_money_bank_reconciliation_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()

    data_map = {}
    branch_names = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except:
                dt = date(1900, 1, 1)
        elif isinstance(dt, datetime):
            dt = dt.date()

        if bid not in data_map:
            data_map[bid] = {}
        data_map[bid][dt] = row
        if row['branch_name'] and row['branch_name'] != '-':
            branch_names[bid] = row['branch_name']

    branches_to_process = sorted(list(data_map.keys()))

    recordList = []
    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})

        # 1. Find Initial Balance
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        running_bal = 0
        current_dt = start_dt

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates:
                current_dt = trans_dates[0]

        # Play forward to startDate
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            hq = day_data.get('total_receipt_from_hq') or 0
            tic = day_data.get('transfer_imprest_cash') or 0
            ecq = day_data.get('total_expense_cq') or 0
            running_bal = running_bal + hq - tic - ecq
            current_dt += timedelta(days=1)

        # Now at startDate
        report_opening_balance = running_bal
        report_total_receipt_from_hq = 0
        report_transfer_imprest_cash = 0
        report_total_expense_cq = 0

        # Accumulate within range
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            hq = day_data.get('total_receipt_from_hq') or 0
            tic = day_data.get('transfer_imprest_cash') or 0
            ecq = day_data.get('total_expense_cq') or 0

            report_total_receipt_from_hq += hq
            report_transfer_imprest_cash += tic
            report_total_expense_cq += ecq

            running_bal = running_bal + hq - tic - ecq
            current_dt += timedelta(days=1)

        # Filter: Only add if there is some activity or balance
        if abs(report_opening_balance) > 0.001 or \
           abs(report_total_receipt_from_hq) > 0.001 or \
           abs(report_transfer_imprest_cash) > 0.001 or \
           abs(report_total_expense_cq) > 0.001 or \
           abs(running_bal) > 0.001:

            recordList.append({
                'branch_name': branch_names.get(bid, f"Branch {bid}"),
                'opening_balance': report_opening_balance,
                'total_receipt_from_hq': report_total_receipt_from_hq,
                'transfer_imprest_cash': report_transfer_imprest_cash,
                'total_expense_cq': report_total_expense_cq,
                'closing_balance': running_bal
            })

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Branch Wise Imprest Money Bank Reconciliation Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Branch Name', 'branch_name'),
        ('Opening Balance', 'opening_balance'),
        ('Total Receipt From HQ', 'total_receipt_from_hq'),
        ('Transfer Imprest Cash', 'transfer_imprest_cash'),
        ('Total Expense (CQ)', 'total_expense_cq'),
        ('Closing Balance', 'closing_balance'),
    ]

    writer.writerow([col[0] for col in export_columns])

    numeric_keys = ['opening_balance', 'total_receipt_from_hq', 'transfer_imprest_cash', 'total_expense_cq', 'closing_balance']
    totals = {key: 0 for key in numeric_keys}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in numeric_keys:
            totals[key] += row.get(key) or 0

    # Total row
    total_row = ['Total', totals['opening_balance'], totals['total_receipt_from_hq'], totals['transfer_imprest_cash'], totals['total_expense_cq'], totals['closing_balance']]
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Branch_Wise_Imprest_Money_Bank_Reconciliation_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/branch_wise_outstanding_report")
@action.uses("report/branch_wise_outstanding_report.html",session,flash,db)
def branch_wise_outstanding_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    # print(check_query)
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        MAX(f.branch_name) as branch_name,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.sales_tp)         AS sales_tp,
        SUM(f.sales_vat)        AS sales_vat,
        SUM(f.sales_discount)   AS sales_discount,
        SUM(f.sales_sp_disc)    AS sales_sp_disc,
        SUM(f.sales_total)      AS sales_total,

        SUM(f.return_tp)        AS return_tp,
        SUM(f.return_vat)       AS return_vat,
        SUM(f.return_discount)  AS return_discount,
        SUM(f.return_sp_disc)   AS return_sp_disc,
        SUM(f.return_total)     AS return_total,

        SUM(f.net_sales_tp)     AS net_sales_tp,
        SUM(f.net_sales_vat)    AS net_sales_vat,
        SUM(f.net_sales_discount) AS net_sales_discount,
        SUM(f.net_sales_sp_disc)  AS net_sales_sp_disc,
        SUM(f.net_sales_total)    AS net_sales_total,

        SUM(f.net_collection)   AS net_collection,
        SUM(f.mr_reverse)       AS mr_reverse,
        SUM(f.adv_receipt)       AS adv_receipt,
        SUM(f.adv_adj)       AS adv_adj,
        SUM(f.adjustment_plus)  AS adjustment_plus,
        SUM(f.adjustment_minus) AS adjustment_minus,

        MAX(f.as_per_pdf) AS as_per_pdf,
        MAX(f.diff_pdf) AS diff_pdf,
        MAX(f.as_per_sales) AS as_per_sales,
        MAX(f.diff_sales) AS diff_sales,
        MAX(f.remarks) AS remarks

    FROM
    (   
        /* ===== Receipt ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            0 AS opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            SUM(d.money_receipt) AS net_collection,
            SUM(d.adv_receipt) AS adv_receipt,
            SUM(d.mr_reverse) AS mr_reverse,
            SUM(d.adv_adj) AS adv_adj,
            SUM(d.adj_plus) AS adjustment_plus,
            SUM(d.adj_minus) AS adjustment_minus,
            '-' AS as_per_pdf, '-' AS diff_pdf, '-' AS as_per_sales, '-' AS diff_sales, '-' AS remarks
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, h.trans_date

        UNION ALL

        /* ===== Date Wise Sales ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            0 AS opening_balance,
            SUM(d.sales_tp) AS sales_tp, SUM(d.sales_vat) AS sales_vat, SUM(d.sales_discount) AS sales_discount, SUM(d.sales_sp_disc) AS sales_sp_disc, SUM(d.sales_total) AS sales_total,
            SUM(d.return_tp) AS return_tp, SUM(d.return_vat) AS return_vat, SUM(d.return_discount) AS return_discount, SUM(d.return_sp_disc) AS return_sp_disc, SUM(d.return_total) AS return_total,
            SUM(d.net_sales_tp) AS net_sales_tp, SUM(d.net_sales_vat) AS net_sales_vat, SUM(d.net_sales_discount) AS net_sales_discount, SUM(d.net_sales_sp_disc) AS net_sales_sp_disc, SUM(d.net_sales_total) AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus,
            '-' AS as_per_pdf, '-' AS diff_pdf, '-' AS as_per_sales, '-' AS diff_sales, '-' AS remarks
        FROM cashier.tr_os_recon_h h
        JOIN cashier.tr_os_recon_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, h.trans_date

        UNION ALL

        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            SUM(d.outstanding) as opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus,
            '-' AS as_per_pdf, '-' AS diff_pdf, '-' AS as_per_sales, '-' AS diff_sales, '-' AS remarks            
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f
    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Playback Logic ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    
    data_map = {}
    branch_names = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except: dt = date(1900, 1, 1)
        elif isinstance(dt, datetime): dt = dt.date()
        
        if bid not in data_map: data_map[bid] = {}
        data_map[bid][dt] = row
        if row['branch_name'] and row['branch_name'] != '-': branch_names[bid] = row['branch_name']

    branches_to_process = sorted(list(data_map.keys()))
    recordList = []

    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        running_bal = 0
        current_dt = start_dt
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates: current_dt = trans_dates[0]
        
        # Play forward to startDate
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            rev = day_data.get('mr_reverse') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0
            running_bal = running_bal + ns - col + rev + ap - am
            current_dt += timedelta(days=1)
        
        # Collect daily rows within range
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            rev = day_data.get('mr_reverse') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0
            
            opening_bal = running_bal
            running_bal = opening_bal + ns - col + rev + ap - am
            
            recordList.append({
                'trans_date': current_dt.strftime('%d-%b-%Y'),
                'branch_name': branch_names.get(bid, f"Branch {bid}"),
                'opening_balance': opening_bal,
                'sales_tp': day_data.get('sales_tp') or 0,
                'sales_vat': day_data.get('sales_vat') or 0,
                'sales_discount': day_data.get('sales_discount') or 0,
                'sales_sp_disc': day_data.get('sales_sp_disc') or 0,
                'sales_total': day_data.get('sales_total') or 0,
                'return_tp': day_data.get('return_tp') or 0,
                'return_vat': day_data.get('return_vat') or 0,
                'return_discount': day_data.get('return_discount') or 0,
                'return_sp_disc': day_data.get('return_sp_disc') or 0,
                'return_total': day_data.get('return_total') or 0,
                'net_sales_tp': day_data.get('net_sales_tp') or 0,
                'net_sales_vat': day_data.get('net_sales_vat') or 0,
                'net_sales_discount': day_data.get('net_sales_discount') or 0,
                'net_sales_sp_disc': day_data.get('net_sales_sp_disc') or 0,
                'net_sales_total': ns,
                'net_collection': col,
                'adv_receipt': adv_receipt,
                'adv_adj': adv_adj,
                'mr_reverse': rev,
                'adjustment_plus': ap,
                'adjustment_minus': am,
                'closing_balance': running_bal,
                'as_per_pdf': day_data.get('as_per_pdf') or '-',
                'diff_pdf': day_data.get('diff_pdf') or '-',
                'as_per_sales': day_data.get('as_per_sales') or '-',
                'diff_sales': day_data.get('diff_sales') or '-',
                'remarks': day_data.get('remarks') or '-'
            })
            current_dt += timedelta(days=1)

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_branch_wise_outstanding_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_branch_wise_outstanding_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        MAX(f.branch_name) as branch_name,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.sales_tp)         AS sales_tp,
        SUM(f.sales_vat)        AS sales_vat,
        SUM(f.sales_discount)   AS sales_discount,
        SUM(f.sales_sp_disc)    AS sales_sp_disc,
        SUM(f.sales_total)      AS sales_total,

        SUM(f.return_tp)        AS return_tp,
        SUM(f.return_vat)       AS return_vat,
        SUM(f.return_discount)  AS return_discount,
        SUM(f.return_sp_disc)   AS return_sp_disc,
        SUM(f.return_total)     AS return_total,

        SUM(f.net_sales_tp)     AS net_sales_tp,
        SUM(f.net_sales_vat)    AS net_sales_vat,
        SUM(f.net_sales_discount) AS net_sales_discount,
        SUM(f.net_sales_sp_disc)  AS net_sales_sp_disc,
        SUM(f.net_sales_total)    AS net_sales_total,

        SUM(f.net_collection)   AS net_collection,
        SUM(f.mr_reverse)       AS mr_reverse,
        SUM(f.adv_receipt)       AS adv_receipt,
        SUM(f.adv_adj)       AS adv_adj,
        SUM(f.adjustment_plus)  AS adjustment_plus,
        SUM(f.adjustment_minus) AS adjustment_minus,

        MAX(f.as_per_pdf) AS as_per_pdf,
        MAX(f.diff_pdf) AS diff_pdf,
        MAX(f.as_per_sales) AS as_per_sales,
        MAX(f.diff_sales) AS diff_sales,
        MAX(f.remarks) AS remarks

    FROM
    (   
        /* ===== Receipt ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            0 AS opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            SUM(d.money_receipt) AS net_collection,
            SUM(d.adv_receipt) AS adv_receipt,
            SUM(d.mr_reverse) AS mr_reverse,
            SUM(d.adv_adj) AS adv_adj,
            SUM(d.adj_plus) AS adjustment_plus,
            SUM(d.adj_minus) AS adjustment_minus,
            '-' AS as_per_pdf, '-' AS diff_pdf, '-' AS as_per_sales, '-' AS diff_sales, '-' AS remarks
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, h.trans_date

        UNION ALL

        /* ===== Date Wise Sales ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            0 AS opening_balance,
            SUM(d.sales_tp) AS sales_tp, SUM(d.sales_vat) AS sales_vat, SUM(d.sales_discount) AS sales_discount, SUM(d.sales_sp_disc) AS sales_sp_disc, SUM(d.sales_total) AS sales_total,
            SUM(d.return_tp) AS return_tp, SUM(d.return_vat) AS return_vat, SUM(d.return_discount) AS return_discount, SUM(d.return_sp_disc) AS return_sp_disc, SUM(d.return_total) AS return_total,
            SUM(d.net_sales_tp) AS net_sales_tp, SUM(d.net_sales_vat) AS net_sales_vat, SUM(d.net_sales_discount) AS net_sales_discount, SUM(d.net_sales_sp_disc) AS net_sales_sp_disc, SUM(d.net_sales_total) AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus,
            '-' AS as_per_pdf, '-' AS diff_pdf, '-' AS as_per_sales, '-' AS diff_sales, '-' AS remarks
        FROM cashier.tr_os_recon_h h
        JOIN cashier.tr_os_recon_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, h.trans_date

        UNION ALL

        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            h.branch_name,
            h.trans_date,
            SUM(d.outstanding) as opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus,
            '-' AS as_per_pdf, '-' AS diff_pdf, '-' AS as_per_sales, '-' AS diff_sales, '-' AS remarks            
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, h.trans_date

    ) f
    GROUP BY f.cid, f.branch_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Playback Logic (identical to branch_wise_outstanding_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()

    data_map = {}
    branch_names = {}
    for row in recordListRaw:
        bid = row['branch_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except: dt = date(1900, 1, 1)
        elif isinstance(dt, datetime): dt = dt.date()

        if bid not in data_map: data_map[bid] = {}
        data_map[bid][dt] = row
        if row['branch_name'] and row['branch_name'] != '-': branch_names[bid] = row['branch_name']

    branches_to_process = sorted(list(data_map.keys()))
    recordList = []

    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        running_bal = 0
        current_dt = start_dt

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates: current_dt = trans_dates[0]

        # Play forward to startDate
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            rev = day_data.get('mr_reverse') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0
            running_bal = running_bal + ns - col + rev + ap - am
            current_dt += timedelta(days=1)

        # Collect daily rows within range
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            rev = day_data.get('mr_reverse') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0

            opening_bal = running_bal
            running_bal = opening_bal + ns - col + rev + ap - am

            recordList.append({
                'trans_date': current_dt.strftime('%d-%b-%Y'),
                'branch_name': branch_names.get(bid, f"Branch {bid}"),
                'opening_balance': opening_bal,
                'sales_tp': day_data.get('sales_tp') or 0,
                'sales_vat': day_data.get('sales_vat') or 0,
                'sales_discount': day_data.get('sales_discount') or 0,
                'sales_sp_disc': day_data.get('sales_sp_disc') or 0,
                'sales_total': day_data.get('sales_total') or 0,
                'return_tp': day_data.get('return_tp') or 0,
                'return_vat': day_data.get('return_vat') or 0,
                'return_discount': day_data.get('return_discount') or 0,
                'return_sp_disc': day_data.get('return_sp_disc') or 0,
                'return_total': day_data.get('return_total') or 0,
                'net_sales_tp': day_data.get('net_sales_tp') or 0,
                'net_sales_vat': day_data.get('net_sales_vat') or 0,
                'net_sales_discount': day_data.get('net_sales_discount') or 0,
                'net_sales_sp_disc': day_data.get('net_sales_sp_disc') or 0,
                'net_sales_total': ns,
                'net_collection': col,
                'adv_receipt': adv_receipt,
                'adv_adj': adv_adj,
                'mr_reverse': rev,
                'adjustment_plus': ap,
                'adjustment_minus': am,
                'closing_balance': running_bal,
                'as_per_pdf': day_data.get('as_per_pdf') or '-',
                'diff_pdf': day_data.get('diff_pdf') or '-',
                'as_per_sales': day_data.get('as_per_sales') or '-',
                'diff_sales': day_data.get('diff_sales') or '-',
                'remarks': day_data.get('remarks') or '-'
            })
            current_dt += timedelta(days=1)

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Branch Wise Outstanding Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Date', 'trans_date'),
        ('Branch Name', 'branch_name'),
        ('Opening Balance', 'opening_balance'),
        ('Sales TP', 'sales_tp'),
        ('Sales VAT', 'sales_vat'),
        ('Sales Discount', 'sales_discount'),
        ('Sales Sp. Disc', 'sales_sp_disc'),
        ('Sales Total', 'sales_total'),
        ('Return TP', 'return_tp'),
        ('Return VAT', 'return_vat'),
        ('Return Discount', 'return_discount'),
        ('Return Sp. Disc', 'return_sp_disc'),
        ('Return Total', 'return_total'),
        ('Net Sales TP', 'net_sales_tp'),
        ('Net Sales VAT', 'net_sales_vat'),
        ('Net Sales Discount', 'net_sales_discount'),
        ('Net Sales Sp. Disc', 'net_sales_sp_disc'),
        ('Net Sales Total', 'net_sales_total'),
        ('Net Collection', 'net_collection'),
        ('Adv. Receipt', 'adv_receipt'),
        ('Adv. Adj.', 'adv_adj'),
        ('MR Reverse', 'mr_reverse'),
        ('Adjustment (+)', 'adjustment_plus'),
        ('Adjustment (-)', 'adjustment_minus'),
        ('Closing Balance', 'closing_balance'),
        ('As Per PDF', 'as_per_pdf'),
        ('Diff. PDF', 'diff_pdf'),
        ('As Per Sales', 'as_per_sales'),
        ('Diff. Sales', 'diff_sales'),
        ('Remarks', 'remarks'),
    ]

    writer.writerow([col[0] for col in export_columns])

    numeric_keys = [
        'opening_balance', 'sales_tp', 'sales_vat', 'sales_discount', 'sales_sp_disc', 'sales_total',
        'return_tp', 'return_vat', 'return_discount', 'return_sp_disc', 'return_total',
        'net_sales_tp', 'net_sales_vat', 'net_sales_discount', 'net_sales_sp_disc', 'net_sales_total',
        'net_collection', 'adv_receipt', 'adv_adj', 'mr_reverse', 'adjustment_plus', 'adjustment_minus'
    ]
    totals = {key: 0 for key in numeric_keys}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in numeric_keys:
            totals[key] += row.get(key) or 0

    # Total row (Closing Balance and text/remarks columns left blank since not summable)
    total_row = ['Total', '']
    for key in numeric_keys:
        total_row.append(totals[key])
    total_row += ['', '-', '-', '-', '-', '-']  # closing_balance, as_per_pdf, diff_pdf, as_per_sales, diff_sales, remarks
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Branch_Wise_Outstanding_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/brand_wise_outstanding_reconciliation_report")
@action.uses("report/brand_wise_outstanding_reconciliation_report.html",session,flash,db)
def brand_wise_outstanding_reconciliation_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.brand_id,
        MAX(f.brand_name) as brand_name,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.sales_tp)         AS sales_tp,
        SUM(f.sales_vat)        AS sales_vat,
        SUM(f.sales_discount)   AS sales_discount,
        SUM(f.sales_sp_disc)    AS sales_sp_disc,
        SUM(f.sales_total)      AS sales_total,

        SUM(f.return_tp)        AS return_tp,
        SUM(f.return_vat)       AS return_vat,
        SUM(f.return_discount)  AS return_discount,
        SUM(f.return_sp_disc)   AS return_sp_disc,
        SUM(f.return_total)     AS return_total,

        SUM(f.net_sales_tp)     AS net_sales_tp,
        SUM(f.net_sales_vat)    AS net_sales_vat,
        SUM(f.net_sales_discount) AS net_sales_discount,
        SUM(f.net_sales_sp_disc)  AS net_sales_sp_disc,
        SUM(f.net_sales_total)    AS net_sales_total,

        SUM(f.net_collection)   AS net_collection,
        SUM(f.adv_receipt)       AS adv_receipt,
        SUM(f.adv_adj)       AS adv_adj,
        SUM(f.mr_reverse)       AS mr_reverse,
        SUM(f.adjustment_plus)  AS adjustment_plus,
        SUM(f.adjustment_minus) AS adjustment_minus

    FROM
    (   
        /* ===== Receipt ===== */
        SELECT
            h.cid,
            d.brand_id,
            d.brand_name,
            h.trans_date,
            0 AS opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            SUM(d.money_receipt) AS net_collection,
            SUM(d.adv_receipt) AS adv_receipt,
            SUM(d.adv_adj) AS adv_adj,
            SUM(d.mr_reverse) AS mr_reverse,
            SUM(d.adj_plus) AS adjustment_plus,
            SUM(d.adj_minus) AS adjustment_minus
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, d.brand_id, h.trans_date

        UNION ALL

        /* ===== Date Wise Sales ===== */
        SELECT
            h.cid,
            d.brand_id,
            d.brand_name,
            h.trans_date,
            0 AS opening_balance,
            SUM(d.sales_tp) AS sales_tp, SUM(d.sales_vat) AS sales_vat, SUM(d.sales_discount) AS sales_discount, SUM(d.sales_sp_disc) AS sales_sp_disc, SUM(d.sales_total) AS sales_total,
            SUM(d.return_tp) AS return_tp, SUM(d.return_vat) AS return_vat, SUM(d.return_discount) AS return_discount, SUM(d.return_sp_disc) AS return_sp_disc, SUM(d.return_total) AS return_total,
            SUM(d.net_sales_tp) AS net_sales_tp, SUM(d.net_sales_vat) AS net_sales_vat, SUM(d.net_sales_discount) AS net_sales_discount, SUM(d.net_sales_sp_disc) AS net_sales_sp_disc, SUM(d.net_sales_total) AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.tr_os_recon_h h
        JOIN cashier.tr_os_recon_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, d.brand_id, h.trans_date

        UNION ALL

        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            d.brand_id,
            d.brand_name,
            h.trans_date,
            SUM(d.outstanding) as opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, d.brand_id, h.trans_date

    ) f
    GROUP BY f.cid, f.brand_id, f.trans_date
    ORDER BY f.trans_date, f.brand_id
    """
    print(query)
    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Playback and Aggregation ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    
    data_map = {}
    brand_names = {}
    for row in recordListRaw:
        brid = row['brand_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except: dt = date(1900, 1, 1)
        elif isinstance(dt, datetime): dt = dt.date()
        
        if brid not in data_map: data_map[brid] = {}
        data_map[brid][dt] = row
        if row['brand_name'] and row['brand_name'] != '-': brand_names[brid] = row['brand_name']

    brands_to_process = sorted(list(data_map.keys()))
    recordList = []

    for brid in brands_to_process:
        brid_data = data_map.get(brid, {})
        balance_dates = sorted([d for d, r in brid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        running_bal = 0
        current_dt = start_dt
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = brid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(brid_data.keys())
            if trans_dates: current_dt = trans_dates[0]
        
        # Play forward to startDate
        while current_dt < start_dt:
            day_data = brid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            rev = day_data.get('mr_reverse') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0
            running_bal = running_bal + ns - col + rev + ap - am
            current_dt += timedelta(days=1)
        
        # Accumulate activity within range
        report_opening_balance = running_bal
        
        act_sales_tp = 0; act_sales_vat = 0; act_sales_discount = 0; act_sales_sp_disc = 0; act_sales_total = 0
        act_return_tp = 0; act_return_vat = 0; act_return_discount = 0; act_return_sp_disc = 0; act_return_total = 0
        act_net_sales_tp = 0; act_net_sales_vat = 0; act_net_sales_discount = 0; act_net_sales_sp_disc = 0; act_net_sales_total = 0
        act_net_collection = 0; act_mr_reverse = 0; act_adjustment_plus = 0; act_adjustment_minus = 0

        while current_dt <= end_dt:
            day_data = brid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            rev = day_data.get('mr_reverse') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0
            
            act_sales_tp += (day_data.get('sales_tp') or 0)
            act_sales_vat += (day_data.get('sales_vat') or 0)
            act_sales_discount += (day_data.get('sales_discount') or 0)
            act_sales_sp_disc += (day_data.get('sales_sp_disc') or 0)
            act_sales_total += (day_data.get('sales_total') or 0)

            act_return_tp += (day_data.get('return_tp') or 0)
            act_return_vat += (day_data.get('return_vat') or 0)
            act_return_discount += (day_data.get('return_discount') or 0)
            act_return_sp_disc += (day_data.get('return_sp_disc') or 0)
            act_return_total += (day_data.get('return_total') or 0)

            act_net_sales_tp += (day_data.get('net_sales_tp') or 0)
            act_net_sales_vat += (day_data.get('net_sales_vat') or 0)
            act_net_sales_discount += (day_data.get('net_sales_discount') or 0)
            act_net_sales_sp_disc += (day_data.get('net_sales_sp_disc') or 0)
            act_net_sales_total += ns

            act_net_collection += col
            act_mr_reverse += rev
            act_adjustment_plus += ap
            act_adjustment_minus += am
            
            running_bal = running_bal + ns - col + rev + ap - am
            current_dt += timedelta(days=1)
        
        # Filter: Only add if there is activity or non-zero balances
        # if abs(report_opening_balance) > 0.001 or abs(act_net_sales_total) > 0.001 or \
        #    abs(act_net_collection) > 0.001 or abs(running_bal) > 0.001:
            
        recordList.append({
            'brand_name': brand_names.get(brid, f"Brand {brid}"),
            'opening_balance': report_opening_balance,
            
            'sales_tp': act_sales_tp,
            'sales_vat': act_sales_vat,
            'sales_discount': act_sales_discount,
            'sales_sp_disc': act_sales_sp_disc,
            'sales_total': act_sales_total,

            'return_tp': act_return_tp,
            'return_vat': act_return_vat,
            'return_discount': act_return_discount,
            'return_sp_disc': act_return_sp_disc,
            'return_total': act_return_total,

            'net_sales_tp': act_net_sales_tp,
            'net_sales_vat': act_net_sales_vat,
            'net_sales_discount': act_net_sales_discount,
            'net_sales_sp_disc': act_net_sales_sp_disc,
            'net_sales_total': act_net_sales_total,

            'net_collection': act_net_collection,
            'adv_receipt': adv_receipt,
            'adv_adj': adv_adj,
            'mr_reverse': act_mr_reverse,
            'adjustment_plus': act_adjustment_plus,
            'adjustment_minus': act_adjustment_minus,
            'closing_balance': running_bal
        })

    return dict(startDate=startDate,endDate=endDate,session=session,branch_name=branch_name,recordList=recordList,check_role=check_role,easy_format=easy_format)

@action("report/download_brand_wise_outstanding_reconciliation_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_brand_wise_outstanding_reconciliation_report():
    # --- Step 0: Get parameters from query string (falls back to session for convenience) ---
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name (used in the CSV header line)
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.brand_id,
        MAX(f.brand_name) as brand_name,
        f.trans_date,

        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.sales_tp)         AS sales_tp,
        SUM(f.sales_vat)        AS sales_vat,
        SUM(f.sales_discount)   AS sales_discount,
        SUM(f.sales_sp_disc)    AS sales_sp_disc,
        SUM(f.sales_total)      AS sales_total,

        SUM(f.return_tp)        AS return_tp,
        SUM(f.return_vat)       AS return_vat,
        SUM(f.return_discount)  AS return_discount,
        SUM(f.return_sp_disc)   AS return_sp_disc,
        SUM(f.return_total)     AS return_total,

        SUM(f.net_sales_tp)     AS net_sales_tp,
        SUM(f.net_sales_vat)    AS net_sales_vat,
        SUM(f.net_sales_discount) AS net_sales_discount,
        SUM(f.net_sales_sp_disc)  AS net_sales_sp_disc,
        SUM(f.net_sales_total)    AS net_sales_total,

        SUM(f.net_collection)   AS net_collection,
        SUM(f.adv_receipt)       AS adv_receipt,
        SUM(f.adv_adj)       AS adv_adj,
        SUM(f.mr_reverse)       AS mr_reverse,
        SUM(f.adjustment_plus)  AS adjustment_plus,
        SUM(f.adjustment_minus) AS adjustment_minus

    FROM
    (   
        /* ===== Receipt ===== */
        SELECT
            h.cid,
            d.brand_id,
            d.brand_name,
            h.trans_date,
            0 AS opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            SUM(d.money_receipt) AS net_collection,
            SUM(d.adv_receipt) AS adv_receipt,
            SUM(d.adv_adj) AS adv_adj,
            SUM(d.mr_reverse) AS mr_reverse,
            SUM(d.adj_plus) AS adjustment_plus,
            SUM(d.adj_minus) AS adjustment_minus
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, d.brand_id, h.trans_date

        UNION ALL

        /* ===== Date Wise Sales ===== */
        SELECT
            h.cid,
            d.brand_id,
            d.brand_name,
            h.trans_date,
            0 AS opening_balance,
            SUM(d.sales_tp) AS sales_tp, SUM(d.sales_vat) AS sales_vat, SUM(d.sales_discount) AS sales_discount, SUM(d.sales_sp_disc) AS sales_sp_disc, SUM(d.sales_total) AS sales_total,
            SUM(d.return_tp) AS return_tp, SUM(d.return_vat) AS return_vat, SUM(d.return_discount) AS return_discount, SUM(d.return_sp_disc) AS return_sp_disc, SUM(d.return_total) AS return_total,
            SUM(d.net_sales_tp) AS net_sales_tp, SUM(d.net_sales_vat) AS net_sales_vat, SUM(d.net_sales_discount) AS net_sales_discount, SUM(d.net_sales_sp_disc) AS net_sales_sp_disc, SUM(d.net_sales_total) AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.tr_os_recon_h h
        JOIN cashier.tr_os_recon_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, d.brand_id, h.trans_date

        UNION ALL

        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            d.brand_id,
            d.brand_name,
            h.trans_date,
            SUM(d.outstanding) as opening_balance,
            0 AS sales_tp, 0 AS sales_vat, 0 AS sales_discount, 0 AS sales_sp_disc, 0 AS sales_total,
            0 AS return_tp, 0 AS return_vat, 0 AS return_discount, 0 AS return_sp_disc, 0 AS return_total,
            0 AS net_sales_tp, 0 AS net_sales_vat, 0 AS net_sales_discount, 0 AS net_sales_sp_disc, 0 AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 as adv_receipt, 0 as adv_adj, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.cid, d.brand_id, h.trans_date

    ) f
    GROUP BY f.cid, f.brand_id, f.trans_date
    ORDER BY f.trans_date, f.brand_id
    """

    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Playback and Aggregation (identical to brand_wise_outstanding_reconciliation_report) ---
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()

    data_map = {}
    brand_names = {}
    for row in recordListRaw:
        brid = row['brand_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except: dt = date(1900, 1, 1)
        elif isinstance(dt, datetime): dt = dt.date()

        if brid not in data_map: data_map[brid] = {}
        data_map[brid][dt] = row
        if row['brand_name'] and row['brand_name'] != '-': brand_names[brid] = row['brand_name']

    brands_to_process = sorted(list(data_map.keys()))
    recordList = []

    for brid in brands_to_process:
        brid_data = data_map.get(brid, {})
        balance_dates = sorted([d for d, r in brid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        running_bal = 0
        current_dt = start_dt

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = brid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(brid_data.keys())
            if trans_dates: current_dt = trans_dates[0]

        # Play forward to startDate
        while current_dt < start_dt:
            day_data = brid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            rev = day_data.get('mr_reverse') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0
            running_bal = running_bal + ns - col + rev + ap - am
            current_dt += timedelta(days=1)

        # Accumulate activity within range
        report_opening_balance = running_bal

        act_sales_tp = 0; act_sales_vat = 0; act_sales_discount = 0; act_sales_sp_disc = 0; act_sales_total = 0
        act_return_tp = 0; act_return_vat = 0; act_return_discount = 0; act_return_sp_disc = 0; act_return_total = 0
        act_net_sales_tp = 0; act_net_sales_vat = 0; act_net_sales_discount = 0; act_net_sales_sp_disc = 0; act_net_sales_total = 0
        act_net_collection = 0; act_mr_reverse = 0; act_adjustment_plus = 0; act_adjustment_minus = 0

        while current_dt <= end_dt:
            day_data = brid_data.get(current_dt, {})
            ns = day_data.get('net_sales_total') or 0
            col = day_data.get('net_collection') or 0
            adv_receipt = day_data.get('adv_receipt') or 0
            adv_adj = day_data.get('adv_adj') or 0
            rev = day_data.get('mr_reverse') or 0
            ap = day_data.get('adjustment_plus') or 0
            am = day_data.get('adjustment_minus') or 0

            act_sales_tp += (day_data.get('sales_tp') or 0)
            act_sales_vat += (day_data.get('sales_vat') or 0)
            act_sales_discount += (day_data.get('sales_discount') or 0)
            act_sales_sp_disc += (day_data.get('sales_sp_disc') or 0)
            act_sales_total += (day_data.get('sales_total') or 0)

            act_return_tp += (day_data.get('return_tp') or 0)
            act_return_vat += (day_data.get('return_vat') or 0)
            act_return_discount += (day_data.get('return_discount') or 0)
            act_return_sp_disc += (day_data.get('return_sp_disc') or 0)
            act_return_total += (day_data.get('return_total') or 0)

            act_net_sales_tp += (day_data.get('net_sales_tp') or 0)
            act_net_sales_vat += (day_data.get('net_sales_vat') or 0)
            act_net_sales_discount += (day_data.get('net_sales_discount') or 0)
            act_net_sales_sp_disc += (day_data.get('net_sales_sp_disc') or 0)
            act_net_sales_total += ns

            act_net_collection += col
            act_mr_reverse += rev
            act_adjustment_plus += ap
            act_adjustment_minus += am

            running_bal = running_bal + ns - col + rev + ap - am
            current_dt += timedelta(days=1)

        recordList.append({
            'brand_name': brand_names.get(brid, f"Brand {brid}"),
            'opening_balance': report_opening_balance,

            'sales_tp': act_sales_tp,
            'sales_vat': act_sales_vat,
            'sales_discount': act_sales_discount,
            'sales_sp_disc': act_sales_sp_disc,
            'sales_total': act_sales_total,

            'return_tp': act_return_tp,
            'return_vat': act_return_vat,
            'return_discount': act_return_discount,
            'return_sp_disc': act_return_sp_disc,
            'return_total': act_return_total,

            'net_sales_tp': act_net_sales_tp,
            'net_sales_vat': act_net_sales_vat,
            'net_sales_discount': act_net_sales_discount,
            'net_sales_sp_disc': act_net_sales_sp_disc,
            'net_sales_total': act_net_sales_total,

            'net_collection': act_net_collection,
            'adv_receipt': adv_receipt,
            'adv_adj': adv_adj,
            'mr_reverse': act_mr_reverse,
            'adjustment_plus': act_adjustment_plus,
            'adjustment_minus': act_adjustment_minus,
            'closing_balance': running_bal
        })

    # --- Step 4: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    # Context header rows
    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Brand Wise Outstanding Reconciliation Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    export_columns = [
        ('Brand Name', 'brand_name'),
        ('Opening Balance', 'opening_balance'),
        ('Sales TP', 'sales_tp'),
        ('Sales VAT', 'sales_vat'),
        ('Sales Discount', 'sales_discount'),
        ('Sales Sp. Disc', 'sales_sp_disc'),
        ('Sales Total', 'sales_total'),
        ('Return TP', 'return_tp'),
        ('Return VAT', 'return_vat'),
        ('Return Discount', 'return_discount'),
        ('Return Sp. Disc', 'return_sp_disc'),
        ('Return Total', 'return_total'),
        ('Net Sales TP', 'net_sales_tp'),
        ('Net Sales VAT', 'net_sales_vat'),
        ('Net Sales Discount', 'net_sales_discount'),
        ('Net Sales Sp. Disc', 'net_sales_sp_disc'),
        ('Net Sales Total', 'net_sales_total'),
        ('Net Collection', 'net_collection'),
        ('Adv. Receipt', 'adv_receipt'),
        ('Adv. Adj.', 'adv_adj'),
        ('MR Reverse', 'mr_reverse'),
        ('Adjustment (+)', 'adjustment_plus'),
        ('Adjustment (-)', 'adjustment_minus'),
        ('Closing Balance', 'closing_balance'),
    ]

    writer.writerow([col[0] for col in export_columns])

    numeric_keys = [
        'opening_balance', 'sales_tp', 'sales_vat', 'sales_discount', 'sales_sp_disc', 'sales_total',
        'return_tp', 'return_vat', 'return_discount', 'return_sp_disc', 'return_total',
        'net_sales_tp', 'net_sales_vat', 'net_sales_discount', 'net_sales_sp_disc', 'net_sales_total',
        'net_collection', 'adv_receipt', 'adv_adj', 'mr_reverse', 'adjustment_plus', 'adjustment_minus',
        'closing_balance'
    ]
    totals = {key: 0 for key in numeric_keys}

    for row in recordList:
        writer.writerow([row.get(col[1], '') for col in export_columns])
        for key in numeric_keys:
            totals[key] += row.get(key) or 0

    # Total row
    total_row = ['Total']
    for key in numeric_keys:
        total_row.append(totals[key])
    writer.writerow(total_row)

    # --- Step 5: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Brand_Wise_Outstanding_Reconciliation_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/branch_brand_wise_outstanding_summary_report")
@action.uses("report/branch_brand_wise_outstanding_summary_report.html",session,flash,db)
def branch_brand_wise_outstanding_summary_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not endDate:
        endDate = datetime.now().strftime('%Y-%m-%d')

    # Normalize branch input to a list of ints
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    # Filter branches by authorized branch list
    branch_ids = session.get('branchList')
    auth_branch_ids = []
    if session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            auth_branch_ids = [str(b).strip() for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            auth_branch_ids = [str(b).strip() for b in branch_ids if b]

    if auth_branch_ids:
        if branch:
            branch = list(set(branch).intersection(auth_branch_ids))
        else:
            branch = auth_branch_ids

    # Query active/authorized branches (for column headers)
    branch_query = (db.branch.status == 1)
    if branch:
        branch_query &= db.branch.id.belongs(branch)
    elif auth_branch_ids:
        branch_query &= db.branch.id.belongs(auth_branch_ids)
    active_branches = db(branch_query).select(db.branch.id, db.branch.name, db.branch.code, db.branch.short_name, orderby=db.branch.name)
    branch_ids_list = [str(b.id) for b in active_branches]

    # Query active brands (for row headers)
    brand_query = (db.brand.status == 1)
    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
        brand_query &= db.brand.id.belongs(brand)
    elif segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
        brand_query &= db.brand.segment_id.belongs(segment)
    active_brands = db(brand_query).select(db.brand.id, db.brand.name, db.brand.segment_id, orderby=db.brand.segment_id)
    brand_ids_list = [str(b.id) for b in active_brands]

    if not branch_ids_list or not brand_ids_list:
        as_of_date_formatted = datetime.strptime(endDate, '%Y-%m-%d').strftime('%d %b %Y')
        return dict(
            session=session,
            as_of_date_formatted=as_of_date_formatted,
            active_branches=[],
            recordList=[],
            col_totals={},
            grand_total=0.0,
            check_role=check_role,
            easy_format=easy_format
        )

    # Filter conditions for SQL
    branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch_ids_list))
    brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand_ids_list))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{endDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = endDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.brand_id,
        f.trans_date,
        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.net_sales_total)  AS net_sales_total,
        SUM(f.net_collection)   AS net_collection,
        SUM(f.mr_reverse)       AS mr_reverse,
        SUM(f.adjustment_plus)  AS adjustment_plus,
        SUM(f.adjustment_minus) AS adjustment_minus
    FROM
    (   
        /* ===== Receipt ===== */
        SELECT
            h.cid,
            h.branch_id,
            d.brand_id,
            h.trans_date,
            0 AS opening_balance,
            0 AS net_sales_total,
            SUM(d.money_receipt) AS net_collection,
            SUM(d.mr_reverse) AS mr_reverse,
            SUM(d.adj_plus) AS adjustment_plus,
            SUM(d.adj_minus) AS adjustment_minus
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, d.brand_id, h.trans_date

        UNION ALL

        /* ===== Date Wise Sales ===== */
        SELECT
            h.cid,
            h.branch_id,
            d.brand_id,
            h.trans_date,
            0 AS opening_balance,
            SUM(d.net_sales_total) AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.tr_os_recon_h h
        JOIN cashier.tr_os_recon_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, d.brand_id, h.trans_date

        UNION ALL

        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            d.brand_id,
            h.trans_date,
            SUM(d.outstanding) as opening_balance,
            0 AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, d.brand_id, h.trans_date
    ) f
    GROUP BY f.cid, f.branch_id, f.brand_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id, f.brand_id
    """
    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Playback Engine ---
    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        brid = row['brand_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except: dt = date(1900, 1, 1)
        elif isinstance(dt, datetime): dt = dt.date()
        
        key = (bid, brid)
        if key not in data_map:
            data_map[key] = {}
        data_map[key][dt] = row

    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    start_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()

    outstanding_map = {}
    
    for branch_rec in active_branches:
        bid = branch_rec.id
        for brand_rec in active_brands:
            brid = brand_rec.id
            key = (bid, brid)
            
            key_data = data_map.get(key, {})
            balance_dates = sorted([d for d, r in key_data.items() if d <= end_dt and r.get('opening_balance', 0) != 0])
            
            running_bal = 0
            current_dt = start_dt
            
            if balance_dates:
                checkpoint_dt = balance_dates[-1]
                running_bal = key_data[checkpoint_dt].get('opening_balance') or 0
                current_dt = checkpoint_dt
            else:
                trans_dates = sorted(key_data.keys())
                if trans_dates:
                    current_dt = trans_dates[0]
            
            while current_dt <= end_dt:
                day_data = key_data.get(current_dt, {})
                ns = day_data.get('net_sales_total') or 0
                col = day_data.get('net_collection') or 0
                rev = day_data.get('mr_reverse') or 0
                ap = day_data.get('adjustment_plus') or 0
                am = day_data.get('adjustment_minus') or 0
                
                if balance_dates and current_dt == balance_dates[-1]:
                    running_bal = running_bal + ns - col + rev + ap - am
                else:
                    running_bal = running_bal + ns - col + rev + ap - am
                
                current_dt += timedelta(days=1)
                
            outstanding_map[(brid, bid)] = running_bal

    # --- Step 4: Formatting Dataset for Table Pivot ---
    recordList = []
    col_totals = {b.id: 0.0 for b in active_branches}
    grand_total = 0.0

    for brand_rec in active_brands:
        brid = brand_rec.id
        brand_balances = {}
        row_total = 0.0
        for branch_rec in active_branches:
            bid = branch_rec.id
            bal = outstanding_map.get((brid, bid), 0.0)
            brand_balances[bid] = bal
            row_total += bal
            col_totals[bid] += bal

        grand_total += row_total
        recordList.append({
            'brand_name': brand_rec.name,
            'balances': brand_balances,
            'row_total': row_total
        })

    as_of_date_formatted = datetime.strptime(endDate, '%Y-%m-%d').strftime('%d %b %Y')

    return dict(
        startDate=startDate,
        endDate=endDate,
        session=session,
        as_of_date_formatted=as_of_date_formatted,
        active_branches=active_branches,
        recordList=recordList,
        col_totals=col_totals,
        grand_total=grand_total,
        check_role=check_role,
        easy_format=easy_format
    )

@action("report/download_branch_brand_wise_outstanding_summary_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_branch_brand_wise_outstanding_summary_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not endDate:
        endDate = datetime.now().strftime('%Y-%m-%d')

    # Normalize branch input to a list of strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    # Filter branches by authorized branch list
    branch_ids = session.get('branchList')
    auth_branch_ids = []
    if session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            auth_branch_ids = [str(b).strip() for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            auth_branch_ids = [str(b).strip() for b in branch_ids if b]

    if auth_branch_ids:
        if branch:
            branch = list(set(branch).intersection(auth_branch_ids))
        else:
            branch = auth_branch_ids

    # Query active/authorized branches (for column headers)
    branch_query = (db.branch.status == 1)
    if branch:
        branch_query &= db.branch.id.belongs(branch)
    elif auth_branch_ids:
        branch_query &= db.branch.id.belongs(auth_branch_ids)
    active_branches = db(branch_query).select(db.branch.id, db.branch.name, db.branch.code, db.branch.short_name, orderby=db.branch.name)
    branch_ids_list = [str(b.id) for b in active_branches]

    # Query active brands (for row headers)
    brand_query = (db.brand.status == 1)
    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
        brand_query &= db.brand.id.belongs(brand)
    elif segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
        brand_query &= db.brand.segment_id.belongs(segment)
    active_brands = db(brand_query).select(db.brand.id, db.brand.name, db.brand.segment_id, orderby=db.brand.segment_id)
    brand_ids_list = [str(b.id) for b in active_brands]

    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    if not branch_ids_list or not brand_ids_list:
        writer.writerow(["Branch Brand Wise Outstanding Summary Report"])
        writer.writerow(["As of Date:", endDate])
        writer.writerow([])
        writer.writerow(["No data available for the selected filters."])

        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = 'attachment; filename="Branch_Brand_Wise_Outstanding_Summary_Report_{}.csv"'.format(endDate)
        return "\ufeff" + output.getvalue()

    # Filter conditions for SQL
    branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch_ids_list))
    brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand_ids_list))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{endDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = endDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Main Data Query ---
    query = f"""
    SELECT
        f.cid,
        f.branch_id,
        f.brand_id,
        f.trans_date,
        SUM(f.opening_balance)  AS opening_balance,
        SUM(f.net_sales_total)  AS net_sales_total,
        SUM(f.net_collection)   AS net_collection,
        SUM(f.mr_reverse)       AS mr_reverse,
        SUM(f.adjustment_plus)  AS adjustment_plus,
        SUM(f.adjustment_minus) AS adjustment_minus
    FROM
    (   
        /* ===== Receipt ===== */
        SELECT
            h.cid,
            h.branch_id,
            d.brand_id,
            h.trans_date,
            0 AS opening_balance,
            0 AS net_sales_total,
            SUM(d.money_receipt) AS net_collection,
            SUM(d.mr_reverse) AS mr_reverse,
            SUM(d.adj_plus) AS adjustment_plus,
            SUM(d.adj_minus) AS adjustment_minus
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, d.brand_id, h.trans_date

        UNION ALL

        /* ===== Date Wise Sales ===== */
        SELECT
            h.cid,
            h.branch_id,
            d.brand_id,
            h.trans_date,
            0 AS opening_balance,
            SUM(d.net_sales_total) AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.tr_os_recon_h h
        JOIN cashier.tr_os_recon_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, d.brand_id, h.trans_date

        UNION ALL

        /* ===== BALANCE CHECKPOINT ===== */
        SELECT
            h.cid,
            h.branch_id,
            d.brand_id,
            h.trans_date,
            SUM(d.outstanding) as opening_balance,
            0 AS net_sales_total,
            0 AS net_collection, 0 AS mr_reverse, 0 AS adjustment_plus, 0 AS adjustment_minus
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond} {brand_cond}
        GROUP BY h.cid, h.branch_id, d.brand_id, h.trans_date
    ) f
    GROUP BY f.cid, f.branch_id, f.brand_id, f.trans_date
    ORDER BY f.trans_date, f.branch_id, f.brand_id
    """
    recordListRaw = db.executesql(query, as_dict=True)

    # --- Step 3: Playback Engine (identical to branch_brand_wise_outstanding_summary_report) ---
    data_map = {}
    for row in recordListRaw:
        bid = row['branch_id']
        brid = row['brand_id']
        dt = row['trans_date']
        if isinstance(dt, str):
            try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
            except: dt = date(1900, 1, 1)
        elif isinstance(dt, datetime): dt = dt.date()

        key = (bid, brid)
        if key not in data_map:
            data_map[key] = {}
        data_map[key][dt] = row

    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()
    start_dt = datetime.strptime(historyStart, '%Y-%m-%d').date()

    outstanding_map = {}

    for branch_rec in active_branches:
        bid = branch_rec.id
        for brand_rec in active_brands:
            brid = brand_rec.id
            key = (bid, brid)

            key_data = data_map.get(key, {})
            balance_dates = sorted([d for d, r in key_data.items() if d <= end_dt and r.get('opening_balance', 0) != 0])

            running_bal = 0
            current_dt = start_dt

            if balance_dates:
                checkpoint_dt = balance_dates[-1]
                running_bal = key_data[checkpoint_dt].get('opening_balance') or 0
                current_dt = checkpoint_dt
            else:
                trans_dates = sorted(key_data.keys())
                if trans_dates:
                    current_dt = trans_dates[0]

            while current_dt <= end_dt:
                day_data = key_data.get(current_dt, {})
                ns = day_data.get('net_sales_total') or 0
                col = day_data.get('net_collection') or 0
                rev = day_data.get('mr_reverse') or 0
                ap = day_data.get('adjustment_plus') or 0
                am = day_data.get('adjustment_minus') or 0

                running_bal = running_bal + ns - col + rev + ap - am
                current_dt += timedelta(days=1)

            outstanding_map[(brid, bid)] = running_bal

    # --- Step 4: Formatting Dataset for Table Pivot ---
    recordList = []
    col_totals = {b.id: 0.0 for b in active_branches}
    grand_total = 0.0

    for brand_rec in active_brands:
        brid = brand_rec.id
        brand_balances = {}
        row_total = 0.0
        for branch_rec in active_branches:
            bid = branch_rec.id
            bal = outstanding_map.get((brid, bid), 0.0)
            brand_balances[bid] = bal
            row_total += bal
            col_totals[bid] += bal

        grand_total += row_total
        recordList.append({
            'brand_name': brand_rec.name,
            'balances': brand_balances,
            'row_total': row_total
        })

    as_of_date_formatted = datetime.strptime(endDate, '%Y-%m-%d').strftime('%d %b %Y')

    # --- Step 5: Build the CSV ---
    writer.writerow(["Branch Brand Wise Outstanding Summary Report"])
    writer.writerow(["As of Date:", as_of_date_formatted])
    writer.writerow([])  # blank line before the table

    # Total column right after Brand Name, matching the on-screen view
    header_row = ["Brand Name", "Total"] + [b.name for b in active_branches]
    writer.writerow(header_row)

    for row in recordList:
        csv_row = [row['brand_name'], row['row_total']]
        for b in active_branches:
            csv_row.append(row['balances'].get(b.id, 0.0))
        writer.writerow(csv_row)

    # Total row
    total_row = ["Total", grand_total]
    for b in active_branches:
        total_row.append(col_totals.get(b.id, 0.0))
    writer.writerow(total_row)

    # --- Step 6: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Branch_Brand_Wise_Outstanding_Summary_Report_{}.csv"'.format(endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/brand_wise_collection_reconciliation_report")
@action.uses("report/brand_wise_collection_reconciliation_report.html",session,flash,db)
def brand_wise_collection_reconciliation_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))
    
    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Fetch Metadata (Segments, Brands, Banks) ---
    
    segment_query = db.segment.cid == cid
    if segment:
        segment_query &= db.segment.id.belongs(segment)
    segments_db = db(segment_query).select(db.segment.id, db.segment.name, orderby=db.segment.id)
    
    brand_query = db.brand.cid == cid
    if brand:
        brand_query &= db.brand.id.belongs(brand)
    if segment:
        brand_query &= db.brand.segment_id.belongs(segment)
    brands_db = db(brand_query).select(db.brand.id, db.brand.name, db.brand.segment_id, orderby=db.brand.id)
    
    segment_hierarchy = []
    brand_map = {}
    for s in segments_db:
        seg_dict = {'id': s.id, 'name': s.name, 'brands': []}
        for b in brands_db:
            if b.segment_id == s.id:
                safe_name = b.name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('+', '').replace('-', '_').replace('.', '_').replace('&', '_')
                b_dict = {'id': b.id, 'name': b.name, 'safe_col': safe_name}
                seg_dict['brands'].append(b_dict)
                brand_map[b.id] = b_dict
        if seg_dict['brands']:
            segment_hierarchy.append(seg_dict)

    deposit_banks_sql = f"""
        SELECT DISTINCT d.bank_name 
        FROM cashier.tr_deposit_d d
        JOIN cashier.tr_deposit_h h ON h.id = d.trans_id
        WHERE d.cid = '{cid}' 
        AND d.trans_date >= '{startDate}' 
        AND d.trans_date <= '{endDate}'
        {branch_cond}
        ORDER BY d.bank_name
    """
    db_banks = db.executesql(deposit_banks_sql)
    bank_names = [b[0] for b in db_banks if b[0]]

    # --- Step 3: Fetch Transaction Data ---
    
    receipts_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            MAX(h.branch_name) as branch_name,
            d.brand_id,
            SUM(d.money_receipt) as collection,
            SUM(d.mr_reverse) as mr_reverse,
            SUM(d.adv_receipt) as adv_receipt,
            SUM(d.adv_adj) as adv_adj,
            SUM(d.short_receipt) as short_receipt
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.trans_date, h.branch_id, d.brand_id
    """
    receipts_data = db.executesql(receipts_sql, as_dict=True)

    deposits_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            d.bank_name,
            SUM(d.amount) as deposit_amount
        FROM cashier.tr_deposit_h h
        JOIN cashier.tr_deposit_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.trans_date, h.branch_id, d.bank_name
    """
    deposits_data = db.executesql(deposits_sql, as_dict=True)

    bcharges_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            SUM(d.amount) as bank_charge
        FROM cashier.tr_bcharge_h h
        JOIN cashier.tr_bcharge_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        GROUP BY h.trans_date, h.branch_id
    """
    bcharges_data = db.executesql(bcharges_sql, as_dict=True)
    
    opening_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            h.opening_balance as opening_balance
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond}
        GROUP BY h.trans_date, h.branch_id
    """
    opening_data = db.executesql(opening_sql, as_dict=True)

    # --- Step 4: Data Aggregation per Branch and Date ---
    from datetime import datetime, timedelta, date
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()

    data_map = {}
    
    def get_or_create_day(bid, dt):
        if bid not in data_map: data_map[bid] = {}
        if dt not in data_map[bid]:
            data_map[bid][dt] = {
                'branch_name': '',
                'opening_balance': 0,
                'brands': {},
                'adv_receipt': 0,
                'adv_adj': 0,
                'short_receipt': 0,
                'deposits': {},
                'bank_charge': 0
            }
        return data_map[bid][dt]

    def parse_dt(dt):
        if isinstance(dt, str):
            try: return datetime.strptime(dt, '%Y-%m-%d').date()
            except: return date(1900, 1, 1)
        elif isinstance(dt, datetime): return dt.date()
        return dt

    for row in opening_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        day_data['opening_balance'] += (row['opening_balance'] or 0)

    for row in receipts_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        if row['branch_name'] and row['branch_name'] != '-':
            day_data['branch_name'] = row['branch_name']
            
        brid = row['brand_id']
        if brid not in day_data['brands']:
            day_data['brands'][brid] = {'collection': 0, 'mr_reverse': 0}
        
        day_data['brands'][brid]['collection'] += (row['collection'] or 0)
        day_data['brands'][brid]['mr_reverse'] += (row['mr_reverse'] or 0)
        day_data['adv_receipt'] += (row['adv_receipt'] or 0)
        day_data['adv_adj'] += (row['adv_adj'] or 0)
        day_data['short_receipt'] += (row['short_receipt'] or 0)

    for row in deposits_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        bname = row['bank_name']
        if bname not in day_data['deposits']:
            day_data['deposits'][bname] = 0
        day_data['deposits'][bname] += (row['deposit_amount'] or 0)

    for row in bcharges_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        day_data['bank_charge'] += (row['bank_charge'] or 0)

    # --- Step 5: Playback & Calculate Final List ---
    recordList = []
    branches_to_process = sorted(list(data_map.keys()))
    
    global_branch_names = {}
    for bid in data_map:
        for dt in data_map[bid]:
            if data_map[bid][dt]['branch_name']:
                global_branch_names[bid] = data_map[bid][dt]['branch_name']

    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])
        
        running_bal = 0
        current_dt = start_dt
        
        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates: current_dt = trans_dates[0]
            
        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            total_col = sum(b['collection'] for b in day_data.get('brands', {}).values())
            total_mr = sum(b['mr_reverse'] for b in day_data.get('brands', {}).values())
            adv_r = day_data.get('adv_receipt', 0)
            adv_a = day_data.get('adv_adj', 0)
            short = day_data.get('short_receipt', 0)
            dep = sum(day_data.get('deposits', {}).values())
            bc = day_data.get('bank_charge', 0)
            
            running_bal = running_bal + total_col - total_mr + adv_r - adv_a + short - dep - bc
            current_dt += timedelta(days=1)
            
        branch_records = []
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})
            
            total_col = sum(b['collection'] for b in day_data.get('brands', {}).values())
            total_mr = sum(b['mr_reverse'] for b in day_data.get('brands', {}).values())
            adv_r = day_data.get('adv_receipt', 0)
            adv_a = day_data.get('adv_adj', 0)
            short = day_data.get('short_receipt', 0)
            dep = sum(day_data.get('deposits', {}).values())
            bc = day_data.get('bank_charge', 0)
            
            opening_bal = running_bal
            grand_total_col = opening_bal + total_col - total_mr + adv_r - adv_a + short
            running_bal = grand_total_col - dep - bc
            
            # if abs(opening_bal) > 0.001 or total_col > 0 or dep > 0 or abs(running_bal) > 0.001:
            row_dict = {
                'trans_date': current_dt.strftime('%d-%b-%Y'),
                'branch_name': global_branch_names.get(bid, f"Branch {bid}"),
                'opening_balance': opening_bal,
                'adv_receipt': adv_r,
                'adv_adj': adv_a,
                'short_receipt': short,
                'grand_total': grand_total_col,
                'total_collection': total_col,
                'total_mr_reverse': total_mr,
                'total_deposit': dep,
                'bank_charge': bc,
                'closing_balance': running_bal,
                'brands': day_data.get('brands', {}),
                'deposits': day_data.get('deposits', {})
            }
            branch_records.append(row_dict)
            recordList.append(row_dict)

            current_dt += timedelta(days=1)

        # Append branch total row
        if branch_records:
            branch_total = {
                'is_total': True,
                'trans_date': 'Total:',
                'branch_name': '',
                'opening_balance': sum(r['opening_balance'] for r in branch_records),
                'brands': {},
                'seg_col': {},
                'seg_mr': {},
                'total_collection': sum(r['total_collection'] for r in branch_records),
                'total_mr_reverse': sum(r['total_mr_reverse'] for r in branch_records),
                'short_receipt': sum(r['short_receipt'] for r in branch_records),
                'adv_receipt': sum(r['adv_receipt'] for r in branch_records),
                'adv_adj': sum(r['adv_adj'] for r in branch_records),
                'grand_total': sum(r['grand_total'] for r in branch_records),
                'deposits': {},
                'total_deposit': sum(r['total_deposit'] for r in branch_records),
                'bank_charge': sum(r['bank_charge'] for r in branch_records),
                'closing_balance': branch_records[-1]['closing_balance']
            }
            
            # Aggregate brands and segments collection and mr_reverse
            for seg in segment_hierarchy:
                seg_col = 0
                seg_mr = 0
                for b in seg['brands']:
                    bid_val = b['id']
                    b_col = sum(r['brands'].get(bid_val, {}).get('collection', 0) for r in branch_records)
                    b_mr = sum(r['brands'].get(bid_val, {}).get('mr_reverse', 0) for r in branch_records)
                    branch_total['brands'][bid_val] = {
                        'collection': b_col,
                        'mr_reverse': b_mr
                    }
                    seg_col += b_col
                    seg_mr += b_mr
                branch_total['seg_col'][seg['id']] = seg_col
                branch_total['seg_mr'][seg['id']] = seg_mr
                    
            # Aggregate deposits
            for bname in bank_names:
                branch_total['deposits'][bname] = sum(r['deposits'].get(bname, 0) for r in branch_records)
                
            recordList.append(branch_total)

    # --- Step 6: Calculate Grand Totals ---
    normal_records = [r for r in recordList if not r.get('is_total')]
    totals = {
        'opening': sum(r['opening_balance'] for r in normal_records),
        'all_col': sum(r['total_collection'] for r in normal_records),
        'all_mr': sum(r['total_mr_reverse'] for r in normal_records),
        'short': sum(r['short_receipt'] for r in normal_records),
        'adv_r': sum(r['adv_receipt'] for r in normal_records),
        'adv_a': sum(r['adv_adj'] for r in normal_records),
        'grand': sum(r['grand_total'] for r in normal_records),
        'dep': sum(r['total_deposit'] for r in normal_records),
        'charge': sum(r['bank_charge'] for r in normal_records),
        'closing': sum(r['closing_balance'] for r in normal_records),
        'brands_col': {},
        'brands_mr': {},
        'seg_col': {},
        'seg_mr': {},
        'banks': {}
    }

    # Initialize dynamic totals
    for seg in segment_hierarchy:
        totals['seg_col'][seg['id']] = 0
        totals['seg_mr'][seg['id']] = 0
        for b in seg['brands']:
            totals['brands_col'][b['id']] = 0
            totals['brands_mr'][b['id']] = 0

    for bname in bank_names:
        totals['banks'][bname] = 0

    # Accumulate dynamic totals
    for r in normal_records:
        for seg in segment_hierarchy:
            seg_col = 0
            seg_mr = 0
            for b in seg['brands']:
                b_data = r['brands'].get(b['id'], {'collection': 0, 'mr_reverse': 0})
                totals['brands_col'][b['id']] += b_data.get('collection', 0)
                totals['brands_mr'][b['id']] += b_data.get('mr_reverse', 0)
                seg_col += b_data.get('collection', 0)
                seg_mr += b_data.get('mr_reverse', 0)
            totals['seg_col'][seg['id']] += seg_col
            totals['seg_mr'][seg['id']] += seg_mr
        for bname in bank_names:
            totals['banks'][bname] += r['deposits'].get(bname, 0)

    return dict(startDate=startDate,endDate=endDate,session=session, branch_name=branch_name, recordList=recordList, 
                segment_hierarchy=segment_hierarchy, bank_names=bank_names, 
                check_role=check_role, easy_format=easy_format, totals=totals)


@action("report/download_brand_wise_collection_reconciliation_report", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_brand_wise_collection_reconciliation_report():
    branch = session.rep_branch
    segment = session.rep_segment
    brand = session.rep_brand
    startDate = session.rep_fromDt
    endDate = session.rep_toDt
    cid = session.cid

    if not startDate or not endDate:
        return "Please provide startDate and endDate"

    # Normalize inputs to lists of non-empty strings
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [str(b) for b in branch if str(b).strip()]
    else:
        branch = []

    if segment:
        if not isinstance(segment, (list, tuple)): segment = [segment]
        segment = [str(s) for s in segment if str(s).strip()]
    else:
        segment = []

    if brand:
        if not isinstance(brand, (list, tuple)): brand = [brand]
        brand = [str(b) for b in brand if str(b).strip()]
    else:
        brand = []

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # Filter conditions
    branch_cond = ""
    if branch:
        branch_cond = " AND h.branch_id IN ({}) ".format(','.join(branch))

    segment_cond = ""
    if segment:
        segment_cond = " AND d.segment_id IN ({}) ".format(','.join(segment))

    brand_cond = ""
    if brand:
        brand_cond = " AND d.brand_id IN ({}) ".format(','.join(brand))

    # --- Step 1: Find the History Start ---
    check_query = f"""
        SELECT MIN(max_dt) as history_start 
        FROM (
            SELECT MAX(trans_date) as max_dt 
            FROM cashier.opening_h h 
            WHERE h.cid = '{cid}' AND h.trans_date <= '{startDate}'
            {branch_cond}
            GROUP BY h.branch_id
        ) t
    """
    res = db.executesql(check_query, as_dict=True)
    historyStart = startDate
    if res and res[0]['history_start']:
        historyStart = str(res[0]['history_start'])

    # --- Step 2: Fetch Metadata (Segments, Brands, Banks) ---

    segment_query = db.segment.cid == cid
    if segment:
        segment_query &= db.segment.id.belongs(segment)
    segments_db = db(segment_query).select(db.segment.id, db.segment.name, orderby=db.segment.id)

    brand_query = db.brand.cid == cid
    if brand:
        brand_query &= db.brand.id.belongs(brand)
    if segment:
        brand_query &= db.brand.segment_id.belongs(segment)
    brands_db = db(brand_query).select(db.brand.id, db.brand.name, db.brand.segment_id, orderby=db.brand.id)

    segment_hierarchy = []
    brand_map = {}
    for s in segments_db:
        seg_dict = {'id': s.id, 'name': s.name, 'brands': []}
        for b in brands_db:
            if b.segment_id == s.id:
                safe_name = b.name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('+', '').replace('-', '_').replace('.', '_').replace('&', '_')
                b_dict = {'id': b.id, 'name': b.name, 'safe_col': safe_name}
                seg_dict['brands'].append(b_dict)
                brand_map[b.id] = b_dict
        if seg_dict['brands']:
            segment_hierarchy.append(seg_dict)

    deposit_banks_sql = f"""
        SELECT DISTINCT d.bank_name 
        FROM cashier.tr_deposit_d d
        JOIN cashier.tr_deposit_h h ON h.id = d.trans_id
        WHERE d.cid = '{cid}' 
        AND d.trans_date >= '{startDate}' 
        AND d.trans_date <= '{endDate}'
        {branch_cond}
        ORDER BY d.bank_name
    """
    db_banks = db.executesql(deposit_banks_sql)
    bank_names = [b[0] for b in db_banks if b[0]]

    # --- Step 3: Fetch Transaction Data ---
    # NOTE: fixed to select money_receipt (matches the on-screen report and the
    # actual tr_receipt_d column name) — previously selected d.collection, a
    # column that doesn't hold the receipt amount, which silently produced
    # wrong/blank collection figures in the CSV.
    receipts_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            MAX(h.branch_name) as branch_name,
            d.brand_id,
            SUM(d.money_receipt) as collection,
            SUM(d.mr_reverse) as mr_reverse,
            SUM(d.adv_receipt) as adv_receipt,
            SUM(d.adv_adj) as adv_adj,
            SUM(d.short_receipt) as short_receipt
        FROM cashier.tr_receipt_h h
        JOIN cashier.tr_receipt_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.trans_date, h.branch_id, d.brand_id
    """
    receipts_data = db.executesql(receipts_sql, as_dict=True)

    deposits_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            d.bank_name,
            SUM(d.amount) as deposit_amount
        FROM cashier.tr_deposit_h h
        JOIN cashier.tr_deposit_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond} {segment_cond} {brand_cond}
        GROUP BY h.trans_date, h.branch_id, d.bank_name
    """
    deposits_data = db.executesql(deposits_sql, as_dict=True)

    bcharges_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            SUM(d.amount) as bank_charge
        FROM cashier.tr_bcharge_h h
        JOIN cashier.tr_bcharge_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        AND h.trans_date >= '{historyStart}'
        AND h.trans_date <= '{endDate}'
        {branch_cond}
        GROUP BY h.trans_date, h.branch_id
    """
    bcharges_data = db.executesql(bcharges_sql, as_dict=True)

    opening_sql = f"""
        SELECT 
            h.trans_date,
            h.branch_id,
            h.opening_balance as opening_balance
        FROM cashier.opening_h h
        JOIN cashier.opening_d d ON h.id = d.trans_id
        WHERE h.cid = '{cid}'
        {branch_cond}
        GROUP BY h.trans_date, h.branch_id
    """
    opening_data = db.executesql(opening_sql, as_dict=True)

    # --- Step 4: Data Aggregation per Branch and Date ---
    from datetime import datetime, timedelta, date
    start_dt = datetime.strptime(startDate, '%Y-%m-%d').date()
    end_dt = datetime.strptime(endDate, '%Y-%m-%d').date()

    data_map = {}

    def get_or_create_day(bid, dt):
        if bid not in data_map: data_map[bid] = {}
        if dt not in data_map[bid]:
            data_map[bid][dt] = {
                'branch_name': '',
                'opening_balance': 0,
                'brands': {},
                'adv_receipt': 0,
                'adv_adj': 0,
                'short_receipt': 0,
                'deposits': {},
                'bank_charge': 0
            }
        return data_map[bid][dt]

    def parse_dt(dt):
        if isinstance(dt, str):
            try: return datetime.strptime(dt, '%Y-%m-%d').date()
            except: return date(1900, 1, 1)
        elif isinstance(dt, datetime): return dt.date()
        return dt

    for row in opening_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        day_data['opening_balance'] += (row['opening_balance'] or 0)

    for row in receipts_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        if row['branch_name'] and row['branch_name'] != '-':
            day_data['branch_name'] = row['branch_name']

        brid = row['brand_id']
        if brid not in day_data['brands']:
            day_data['brands'][brid] = {'collection': 0, 'mr_reverse': 0}

        day_data['brands'][brid]['collection'] += (row['collection'] or 0)
        day_data['brands'][brid]['mr_reverse'] += (row['mr_reverse'] or 0)
        day_data['adv_receipt'] += (row['adv_receipt'] or 0)
        day_data['adv_adj'] += (row['adv_adj'] or 0)
        day_data['short_receipt'] += (row['short_receipt'] or 0)

    for row in deposits_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        bname = row['bank_name']
        if bname not in day_data['deposits']:
            day_data['deposits'][bname] = 0
        day_data['deposits'][bname] += (row['deposit_amount'] or 0)

    for row in bcharges_data:
        bid = row['branch_id']
        dt = parse_dt(row['trans_date'])
        day_data = get_or_create_day(bid, dt)
        day_data['bank_charge'] += (row['bank_charge'] or 0)

    # --- Step 5: Playback & Calculate Final List (identical logic to the on-screen report) ---
    recordList = []
    branches_to_process = sorted(list(data_map.keys()))

    global_branch_names = {}
    for bid in data_map:
        for dt in data_map[bid]:
            if data_map[bid][dt]['branch_name']:
                global_branch_names[bid] = data_map[bid][dt]['branch_name']

    for bid in branches_to_process:
        bid_data = data_map.get(bid, {})
        balance_dates = sorted([d for d, r in bid_data.items() if d <= start_dt and r.get('opening_balance', 0) != 0])

        running_bal = 0
        current_dt = start_dt

        if balance_dates:
            checkpoint_dt = balance_dates[-1]
            running_bal = bid_data[checkpoint_dt].get('opening_balance') or 0
            current_dt = checkpoint_dt
        else:
            trans_dates = sorted(bid_data.keys())
            if trans_dates: current_dt = trans_dates[0]

        while current_dt < start_dt:
            day_data = bid_data.get(current_dt, {})
            total_col = sum(b['collection'] for b in day_data.get('brands', {}).values())
            total_mr = sum(b['mr_reverse'] for b in day_data.get('brands', {}).values())
            adv_r = day_data.get('adv_receipt', 0)
            adv_a = day_data.get('adv_adj', 0)
            short = day_data.get('short_receipt', 0)
            dep = sum(day_data.get('deposits', {}).values())
            bc = day_data.get('bank_charge', 0)

            running_bal = running_bal + total_col - total_mr + adv_r - adv_a + short - dep - bc
            current_dt += timedelta(days=1)

        branch_records = []
        while current_dt <= end_dt:
            day_data = bid_data.get(current_dt, {})

            total_col = sum(b['collection'] for b in day_data.get('brands', {}).values())
            total_mr = sum(b['mr_reverse'] for b in day_data.get('brands', {}).values())
            adv_r = day_data.get('adv_receipt', 0)
            adv_a = day_data.get('adv_adj', 0)
            short = day_data.get('short_receipt', 0)
            dep = sum(day_data.get('deposits', {}).values())
            bc = day_data.get('bank_charge', 0)

            opening_bal = running_bal
            grand_total_col = opening_bal + total_col - total_mr + adv_r - adv_a + short
            running_bal = grand_total_col - dep - bc

            # NOTE: previously this block was gated behind a threshold check
            # (`if abs(opening_bal) > 0.001 or total_col > 0 ...`) which
            # silently dropped zero-activity days from the CSV while the
            # on-screen report kept every day in range. That made the two
            # outputs disagree and made "missing day" gaps in the running
            # balance invisible in the download. Every day is now included,
            # matching the on-screen report exactly.
            row_dict = {
                'trans_date': current_dt.strftime('%d-%b-%Y'),
                'branch_name': global_branch_names.get(bid, f"Branch {bid}"),
                'opening_balance': opening_bal,
                'adv_receipt': adv_r,
                'adv_adj': adv_a,
                'short_receipt': short,
                'grand_total': grand_total_col,
                'total_collection': total_col,
                'total_mr_reverse': total_mr,
                'total_deposit': dep,
                'bank_charge': bc,
                'closing_balance': running_bal,
                'brands': day_data.get('brands', {}),
                'deposits': day_data.get('deposits', {})
            }
            branch_records.append(row_dict)
            recordList.append(row_dict)

            current_dt += timedelta(days=1)

        # Append branch total row
        if branch_records:
            branch_total = {
                'is_total': True,
                'trans_date': 'Total:',
                'branch_name': '',
                'opening_balance': sum(r['opening_balance'] for r in branch_records),
                'brands': {},
                'seg_col': {},
                'seg_mr': {},
                'total_collection': sum(r['total_collection'] for r in branch_records),
                'total_mr_reverse': sum(r['total_mr_reverse'] for r in branch_records),
                'short_receipt': sum(r['short_receipt'] for r in branch_records),
                'adv_receipt': sum(r['adv_receipt'] for r in branch_records),
                'adv_adj': sum(r['adv_adj'] for r in branch_records),
                'grand_total': sum(r['grand_total'] for r in branch_records),
                'deposits': {},
                'total_deposit': sum(r['total_deposit'] for r in branch_records),
                'bank_charge': sum(r['bank_charge'] for r in branch_records),
                'closing_balance': branch_records[-1]['closing_balance']
            }

            # Aggregate brands and segments collection and mr_reverse
            for seg in segment_hierarchy:
                seg_col = 0
                seg_mr = 0
                for b in seg['brands']:
                    bid_val = b['id']
                    b_col = sum(r['brands'].get(bid_val, {}).get('collection', 0) for r in branch_records)
                    b_mr = sum(r['brands'].get(bid_val, {}).get('mr_reverse', 0) for r in branch_records)
                    branch_total['brands'][bid_val] = {
                        'collection': b_col,
                        'mr_reverse': b_mr
                    }
                    seg_col += b_col
                    seg_mr += b_mr
                branch_total['seg_col'][seg['id']] = seg_col
                branch_total['seg_mr'][seg['id']] = seg_mr

            # Aggregate deposits
            for bname in bank_names:
                branch_total['deposits'][bname] = sum(r['deposits'].get(bname, 0) for r in branch_records)

            recordList.append(branch_total)

    # --- Step 6: Calculate Grand Totals ---
    normal_records = [r for r in recordList if not r.get('is_total')]
    totals = {
        'opening': sum(r['opening_balance'] for r in normal_records),
        'all_col': sum(r['total_collection'] for r in normal_records),
        'all_mr': sum(r['total_mr_reverse'] for r in normal_records),
        'short': sum(r['short_receipt'] for r in normal_records),
        'adv_r': sum(r['adv_receipt'] for r in normal_records),
        'adv_a': sum(r['adv_adj'] for r in normal_records),
        'grand': sum(r['grand_total'] for r in normal_records),
        'dep': sum(r['total_deposit'] for r in normal_records),
        'charge': sum(r['bank_charge'] for r in normal_records),
        'closing': sum(r['closing_balance'] for r in normal_records),
        'brands_col': {},
        'brands_mr': {},
        'seg_col': {},
        'seg_mr': {},
        'banks': {}
    }

    for seg in segment_hierarchy:
        totals['seg_col'][seg['id']] = 0
        totals['seg_mr'][seg['id']] = 0
        for b in seg['brands']:
            totals['brands_col'][b['id']] = 0
            totals['brands_mr'][b['id']] = 0

    for bname in bank_names:
        totals['banks'][bname] = 0

    for r in normal_records:
        for seg in segment_hierarchy:
            seg_col = 0
            seg_mr = 0
            for b in seg['brands']:
                b_data = r['brands'].get(b['id'], {'collection': 0, 'mr_reverse': 0})
                totals['brands_col'][b['id']] += b_data.get('collection', 0)
                totals['brands_mr'][b['id']] += b_data.get('mr_reverse', 0)
                seg_col += b_data.get('collection', 0)
                seg_mr += b_data.get('mr_reverse', 0)
            totals['seg_col'][seg['id']] += seg_col
            totals['seg_mr'][seg['id']] += seg_mr
        for bname in bank_names:
            totals['banks'][bname] += r['deposits'].get(bname, 0)

    # --- Step 7: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Brand Wise MR Reconciliation Report"])
    writer.writerow(["Date:", "{} to {}".format(startDate, endDate)])
    writer.writerow([])  # blank line before the table

    # Build dynamic header: one Collection + MR Reverse column pair per brand
    header_row = ["Date", "Branch Name", "Opening Balance"]
    brand_order = []  # list of brand ids in header order
    for seg in segment_hierarchy:
        for b in seg['brands']:
            header_row.append("{} MR".format(b['name']))
            header_row.append("{} MR Reverse".format(b['name']))
            brand_order.append(b['id'])

    header_row += [
        "Adv. Receipt", "Adv. Adj.", "Short Receipt", "Grand Total",
        "Total MR", "Total MR Reverse"
    ]

    for bname in bank_names:
        header_row.append("Deposit - {}".format(bname))

    header_row += ["Total Deposit", "Bank Charge", "Closing Balance"]

    writer.writerow(header_row)

    def build_row(r):
        row = [
            r.get('trans_date', ''),
            r.get('branch_name', ''),
            r.get('opening_balance', 0),
        ]
        for brid in brand_order:
            b_data = r.get('brands', {}).get(brid, {'collection': 0, 'mr_reverse': 0})
            row.append(b_data.get('collection', 0))
            row.append(b_data.get('mr_reverse', 0))

        row += [
            r.get('adv_receipt', 0),
            r.get('adv_adj', 0),
            r.get('short_receipt', 0),
            r.get('grand_total', 0),
            r.get('total_collection', 0),
            r.get('total_mr_reverse', 0),
        ]

        for bname in bank_names:
            row.append(r.get('deposits', {}).get(bname, 0))

        row += [
            r.get('total_deposit', 0),
            r.get('bank_charge', 0),
            r.get('closing_balance', 0),
        ]
        return row

    for r in recordList:
        writer.writerow(build_row(r))

    # Grand total row across all branches
    grand_row = ["Grand Total:", ""]
    grand_row.append(totals['opening'])
    for brid in brand_order:
        grand_row.append(totals['brands_col'].get(brid, 0))
        grand_row.append(totals['brands_mr'].get(brid, 0))
    grand_row += [
        totals['adv_r'],
        totals['adv_a'],
        totals['short'],
        totals['grand'],
        totals['all_col'],
        totals['all_mr'],
    ]
    for bname in bank_names:
        grand_row.append(totals['banks'].get(bname, 0))
    grand_row += [
        totals['dep'],
        totals['charge'],
        totals['closing'],
    ]
    writer.writerow(grand_row)

    # --- Step 8: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Brand_Wise_MR_Reconciliation_Report_{}_to_{}.csv"'.format(startDate, endDate)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility

@action("report/consolidate_bank_reconciliation_statement")
@action.uses("report/consolidate_bank_reconciliation_statement.html",session,flash,db)
def consolidate_bank_reconciliation_statement():
    task_id='report_manage'
    task_id_view='report_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    branch = session.rep_branch
    yearCombo = session.yearCombo
    monthCombo = session.monthCombo
    cid = session.cid 
    # Normalize branch input to a list of ints
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [int(b) for b in branch if str(b).strip().isdigit()]
    else:
        branch = []

    # Get allowed branches based on role/permissions
    allowed_branch_ids = session.get('branchList')
    if session.get('role') != 'super_admin' and allowed_branch_ids:
        if isinstance(allowed_branch_ids, str):
            allowed_branch_ids = [int(b) for b in allowed_branch_ids.split(',') if b.strip()]
        elif isinstance(allowed_branch_ids, list):
            allowed_branch_ids = [int(b) for b in allowed_branch_ids if b]

        if allowed_branch_ids:
            if branch:
                branch = list(set(branch) & set(allowed_branch_ids))
                if not branch:
                    branch = [-1]  # No overlapping access
            else:
                branch = allowed_branch_ids

    # Query matching reconciliation headers
    query = (db.tr_impr_bnk_h.year == yearCombo) & (db.tr_impr_bnk_h.month == monthCombo) & (db.tr_impr_bnk_h.cid == cid)
    if branch:
        query &= db.tr_impr_bnk_h.branch_id.belongs(branch)

    headers = db(query).select(orderby=db.tr_impr_bnk_h.branch_id)

    # Pre-map branch names & codes for performance
    branch_map = {}
    for b in db(db.branch.id > 0).select(db.branch.id, db.branch.name, db.branch.code):
        branch_map[b.id] = {'name': b.name, 'code': b.code}

    recordList = []
    for h in headers:
        # Fetch details for aggregation
        details = db(db.tr_impr_bnk_d.trans_id == h.id).select(db.tr_impr_bnk_d.types, db.tr_impr_bnk_d.amount)
        details_agg = {
            'DEPOSITED_OR_RECEIVED': 0.0,
            'LESS_CHECK_ISSUED': 0.0,
            'LESS_CHECK_ISSUED_CQ': 0.0,
            'DEPOSITED_BUT_NOT_SHOW_BANK_BOOK': 0.0,
            'CHEQUE_ISSUED': 0.0,
            'DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK': 0.0,
        }
        for d in details:
            dtype = d.types
            if dtype in details_agg:
                details_agg[dtype] += d.amount or 0.0

        opening_balance = h.opening_balance or 0.0
        bank_interest = h.bank_interest or 0.0
        bank_charge = h.bank_charge or 0.0
        closing_per_bank_book = h.closing_per_bank_book or 0.0
        closing_per_bank = h.closing_per_bank or 0.0

        deposited_hq = details_agg['DEPOSITED_OR_RECEIVED']
        cheque_issued_cash = details_agg['LESS_CHECK_ISSUED']
        cheque_issued_cq = details_agg['LESS_CHECK_ISSUED_CQ']
        less_cheque_issued = cheque_issued_cash + cheque_issued_cq

        difference = closing_per_bank - closing_per_bank_book

        credited_by_bank = details_agg['DEPOSITED_BUT_NOT_SHOW_BANK_BOOK']
        cheque_issued_but_not_debited = details_agg['CHEQUE_ISSUED']
        debited_by_bank = details_agg['DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK']

        adjusted_closing_balance = closing_per_bank_book + credited_by_bank + cheque_issued_but_not_debited - debited_by_bank
        discrepancy = adjusted_closing_balance - closing_per_bank

        b_info = branch_map.get(h.branch_id, {'name': 'Unknown', 'code': str(h.branch_code)})

        recordList.append({
            'branch_code': b_info['code'],
            'branch_name': b_info['name'],
            'opening_balance': opening_balance,
            'deposited_hq': deposited_hq,
            'bank_interest': bank_interest,
            'less_cheque_issued': less_cheque_issued,
            'bank_charge': bank_charge,
            'closing_per_bank_book': closing_per_bank_book,
            'closing_per_bank': closing_per_bank,
            'difference': difference,
            'credited_by_bank': credited_by_bank,
            'cheque_issued_but_not_debited': cheque_issued_but_not_debited,
            'debited_by_bank': debited_by_bank,
            'adjusted_closing_balance': adjusted_closing_balance,
            'discrepancy': discrepancy,
            'tranf_to_cash': cheque_issued_cash,
            'payment_by_cq': cheque_issued_cq,
        })

    # Grand Totals
    grand_totals = {
        'opening_balance': sum(r['opening_balance'] for r in recordList),
        'deposited_hq': sum(r['deposited_hq'] for r in recordList),
        'bank_interest': sum(r['bank_interest'] for r in recordList),
        'less_cheque_issued': sum(r['less_cheque_issued'] for r in recordList),
        'bank_charge': sum(r['bank_charge'] for r in recordList),
        'closing_per_bank_book': sum(r['closing_per_bank_book'] for r in recordList),
        'closing_per_bank': sum(r['closing_per_bank'] for r in recordList),
        'difference': sum(r['difference'] for r in recordList),
        'credited_by_bank': sum(r['credited_by_bank'] for r in recordList),
        'cheque_issued_but_not_debited': sum(r['cheque_issued_but_not_debited'] for r in recordList),
        'debited_by_bank': sum(r['debited_by_bank'] for r in recordList),
        'adjusted_closing_balance': sum(r['adjusted_closing_balance'] for r in recordList),
        'discrepancy': sum(r['discrepancy'] for r in recordList),
        'tranf_to_cash': sum(r['tranf_to_cash'] for r in recordList),
        'payment_by_cq': sum(r['payment_by_cq'] for r in recordList),
    }

    # Resolve month name
    import calendar
    month_name = ""
    if monthCombo and monthCombo.isdigit():
        month_name = calendar.month_name[int(monthCombo)]

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    from ..common_fn import easy_format

    return dict(
        session=session,
        branch_name=branch_name,
        yearCombo=yearCombo,
        monthCombo=monthCombo,
        month_name=month_name,
        recordList=recordList,
        grand_totals=grand_totals,
        check_role=check_role,
        easy_format=easy_format
    )


@action("report/download_consolidate_bank_reconciliation_statement", method=['GET', 'POST'])
@action.uses(db, session, T, flash)
def download_consolidate_bank_reconciliation_statement():
    task_id = 'report_manage'
    task_id_view = 'report_view'
    access_permission = check_role(task_id)
    access_permission_view = check_role(task_id_view)
    if not (access_permission or access_permission_view):
        flash.set('Access is Denied !', 'warning')
        redirect(URL('login', 'index'))

    branch = session.rep_branch
    yearCombo = session.yearCombo
    monthCombo = session.monthCombo
    cid = session.cid

    if not yearCombo or not monthCombo:
        return "Please provide yearCombo and monthCombo"

    # Normalize branch input to a list of ints
    if branch:
        if not isinstance(branch, (list, tuple)): branch = [branch]
        branch = [int(b) for b in branch if str(b).strip().isdigit()]
    else:
        branch = []

    # Get allowed branches based on role/permissions
    allowed_branch_ids = session.get('branchList')
    if session.get('role') != 'super_admin' and allowed_branch_ids:
        if isinstance(allowed_branch_ids, str):
            allowed_branch_ids = [int(b) for b in allowed_branch_ids.split(',') if b.strip()]
        elif isinstance(allowed_branch_ids, list):
            allowed_branch_ids = [int(b) for b in allowed_branch_ids if b]

        if allowed_branch_ids:
            if branch:
                branch = list(set(branch) & set(allowed_branch_ids))
                if not branch:
                    branch = [-1]  # No overlapping access
            else:
                branch = allowed_branch_ids

    # --- Step 1: Query matching reconciliation headers ---
    query = (db.tr_impr_bnk_h.year == yearCombo) & (db.tr_impr_bnk_h.month == monthCombo) & (db.tr_impr_bnk_h.cid == cid)
    if branch:
        query &= db.tr_impr_bnk_h.branch_id.belongs(branch)

    headers = db(query).select(orderby=db.tr_impr_bnk_h.branch_id)

    # Pre-map branch names & codes for performance
    branch_map = {}
    for b in db(db.branch.id > 0).select(db.branch.id, db.branch.name, db.branch.code):
        branch_map[b.id] = {'name': b.name, 'code': b.code}

    recordList = []
    for h in headers:
        details = db(db.tr_impr_bnk_d.trans_id == h.id).select(db.tr_impr_bnk_d.types, db.tr_impr_bnk_d.amount)
        details_agg = {
            'DEPOSITED_OR_RECEIVED': 0.0,
            'LESS_CHECK_ISSUED': 0.0,
            'LESS_CHECK_ISSUED_CQ': 0.0,
            'DEPOSITED_BUT_NOT_SHOW_BANK_BOOK': 0.0,
            'CHEQUE_ISSUED': 0.0,
            'DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK': 0.0,
        }
        for d in details:
            dtype = d.types
            if dtype in details_agg:
                details_agg[dtype] += d.amount or 0.0

        opening_balance = h.opening_balance or 0.0
        bank_interest = h.bank_interest or 0.0
        bank_charge = h.bank_charge or 0.0
        closing_per_bank_book = h.closing_per_bank_book or 0.0
        closing_per_bank = h.closing_per_bank or 0.0

        deposited_hq = details_agg['DEPOSITED_OR_RECEIVED']
        cheque_issued_cash = details_agg['LESS_CHECK_ISSUED']
        cheque_issued_cq = details_agg['LESS_CHECK_ISSUED_CQ']
        less_cheque_issued = cheque_issued_cash + cheque_issued_cq

        difference = closing_per_bank - closing_per_bank_book

        credited_by_bank = details_agg['DEPOSITED_BUT_NOT_SHOW_BANK_BOOK']
        cheque_issued_but_not_debited = details_agg['CHEQUE_ISSUED']
        debited_by_bank = details_agg['DEBITED_BY_BANK_BUT_NOT_SHOWING_BANK_BOOK']

        adjusted_closing_balance = closing_per_bank_book + credited_by_bank + cheque_issued_but_not_debited - debited_by_bank
        discrepancy = adjusted_closing_balance - closing_per_bank

        b_info = branch_map.get(h.branch_id, {'name': 'Unknown', 'code': str(h.branch_code)})

        recordList.append({
            'branch_code': b_info['code'],
            'branch_name': b_info['name'],
            'opening_balance': opening_balance,
            'deposited_hq': deposited_hq,
            'bank_interest': bank_interest,
            'less_cheque_issued': less_cheque_issued,
            'bank_charge': bank_charge,
            'closing_per_bank_book': closing_per_bank_book,
            'closing_per_bank': closing_per_bank,
            'difference': difference,
            'credited_by_bank': credited_by_bank,
            'cheque_issued_but_not_debited': cheque_issued_but_not_debited,
            'debited_by_bank': debited_by_bank,
            'adjusted_closing_balance': adjusted_closing_balance,
            'discrepancy': discrepancy,
            'tranf_to_cash': cheque_issued_cash,
            'payment_by_cq': cheque_issued_cq,
        })

    # --- Step 2: Grand Totals ---
    grand_totals = {
        'opening_balance': sum(r['opening_balance'] for r in recordList),
        'deposited_hq': sum(r['deposited_hq'] for r in recordList),
        'bank_interest': sum(r['bank_interest'] for r in recordList),
        'less_cheque_issued': sum(r['less_cheque_issued'] for r in recordList),
        'bank_charge': sum(r['bank_charge'] for r in recordList),
        'closing_per_bank_book': sum(r['closing_per_bank_book'] for r in recordList),
        'closing_per_bank': sum(r['closing_per_bank'] for r in recordList),
        'difference': sum(r['difference'] for r in recordList),
        'credited_by_bank': sum(r['credited_by_bank'] for r in recordList),
        'cheque_issued_but_not_debited': sum(r['cheque_issued_but_not_debited'] for r in recordList),
        'debited_by_bank': sum(r['debited_by_bank'] for r in recordList),
        'adjusted_closing_balance': sum(r['adjusted_closing_balance'] for r in recordList),
        'discrepancy': sum(r['discrepancy'] for r in recordList),
        'tranf_to_cash': sum(r['tranf_to_cash'] for r in recordList),
        'payment_by_cq': sum(r['payment_by_cq'] for r in recordList),
    }

    # Resolve month name
    import calendar
    month_name = ""
    if monthCombo and str(monthCombo).isdigit():
        month_name = calendar.month_name[int(monthCombo)]

    # Safe retrieval of branch name
    branch_name = "All Branches"
    if branch:
        branch_rows = db(db.branch.id.belongs(branch)).select(db.branch.name)
        if branch_rows:
            branch_name = ", ".join([r.name for r in branch_rows])

    # --- Step 3: Build the CSV ---
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Branch Name:", branch_name])
    writer.writerow(["Consolidate Bank Reconciliation Statement"])
    writer.writerow(["Period:", "{} {}".format(month_name, yearCombo)])
    writer.writerow([])  # blank line before the table

    # Two-row header to mirror the on-screen report's grouped columns
    header_row_1 = [
        "SL", "Branch Code", "Branch Name",
        "Opening Balance As",
        "Add. Deposited / Received",
        "Add. Bank Interest",
        "Less. Cheque Issued", "",
        "Less. Bank Charges / AIT / Excise",
        "Closing Balance as per Bank Book",
        "Closing Balance as per Bank",
        "Difference",
        "Reconciliation Items", "", "",
        "Adjusted Closing Balance",
        "Discrepancy (Should Be Zero)",
    ]
    header_row_2 = [
        "", "", "",
        "", "", "",
        "Tranf. to Cash", "Payment by CQ",
        "",
        "", "", "",
        "Add: Credited By Bank", "Add: Cheque Issued By", "Less: Debited By Bank",
        "", "",
    ]
    writer.writerow(header_row_1)
    writer.writerow(header_row_2)

    def build_row(sl, r):
        return [
            sl,
            r.get('branch_code', ''),
            r.get('branch_name', ''),
            r.get('opening_balance', 0),
            r.get('deposited_hq', 0),
            r.get('bank_interest', 0),
            r.get('tranf_to_cash', 0),
            r.get('payment_by_cq', 0),
            r.get('bank_charge', 0),
            r.get('closing_per_bank_book', 0),
            r.get('closing_per_bank', 0),
            r.get('difference', 0),
            r.get('credited_by_bank', 0),
            r.get('cheque_issued_but_not_debited', 0),
            r.get('debited_by_bank', 0),
            r.get('adjusted_closing_balance', 0),
            r.get('discrepancy', 0),
        ]

    for idx, r in enumerate(recordList, start=1):
        writer.writerow(build_row(idx, r))

    # Grand total row
    grand_row = [
        "", "GRAND TOTAL", "",
        grand_totals['opening_balance'],
        grand_totals['deposited_hq'],
        grand_totals['bank_interest'],
        grand_totals['tranf_to_cash'],
        grand_totals['payment_by_cq'],
        grand_totals['bank_charge'],
        grand_totals['closing_per_bank_book'],
        grand_totals['closing_per_bank'],
        grand_totals['difference'],
        grand_totals['credited_by_bank'],
        grand_totals['cheque_issued_but_not_debited'],
        grand_totals['debited_by_bank'],
        grand_totals['adjusted_closing_balance'],
        grand_totals['discrepancy'],
    ]
    writer.writerow(grand_row)

    # --- Step 4: Serve the file as a CSV download ---
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename="Consolidate_Bank_Reconciliation_Statement_{}_{}.csv"'.format(
        month_name or monthCombo, yearCombo)

    return "\ufeff" + output.getvalue()  # BOM prefix for Excel compatibility