from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_fn import active_calendar,check_role,get_sl,check_active_date
from ..common_cid import date_time_list
from datetime import datetime, timedelta

import json
from collections import defaultdict
from google.cloud import bigquery
import os
import pandas as pd
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cashier@tdcl-bq-analytics.iam.gserviceaccount.com.json")
# print(SERVICE_ACCOUNT_FILE)
client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

@action("sync_bq/import_receipt")
@action.uses("sync_bq/import_receipt.html",session,flash,db)
def import_receipt(id=None):
    # task_id='diposit_manage'
    # task_id_view='diposit_view'
    # access_permission = check_role(task_id)
    # access_permission_view = check_role(task_id_view)
    # if not (access_permission or access_permission_view):
    #     flash.set('Access is Denied !', 'warning')
    #     redirect(URL('login', 'index'))

    cid = session.get('cid')

    rows = db(db.brand.cid == cid).select(
    db.brand.id,
    db.brand.code,
    db.brand.name,
    db.brand.segment_id,
    db.brand.segment_name,
    orderby=[~db.brand.segment_name]
)
    branch_ids = session.get('branchCodeList')
    print("branch_ids",branch_ids)
    query = ((db.branch.cid == cid)&(db.branch.status == 1))

    if session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            query &= db.branch.code.belongs(branch_ids)

    branchList = db(query).select()
    print(branchList)   
    calendar_dates = active_calendar()
    active_date = calendar_dates['active_date'] if calendar_dates else None
    expire_at = calendar_dates['expire_at'] if calendar_dates else None
    
    formatted_date=date_time_list["date_fixed"].strftime(date_time_list["date_format"])

    return dict(session=session,check_role=check_role,rows=rows,branchList=branchList,active_date=active_date,expire_at=expire_at,formatted_date=formatted_date,date_time_list=date_time_list)

@action("sync_bq/submit",method="POST")
@action.uses(session,flash,db)
def submit():
    sl=get_sl()
    cid = session.get('cid')
    transaction_date = request.forms.get('transaction_date').strip()
    branch_name = request.forms.get('branch_name').strip()
    
    if transaction_date=='' or transaction_date==None or branch_name=='' or branch_name==None:
        res_data = {"status": "Failed", "message": "Transaction Date or Branch Name Missing"}
    else:
        # if str(company_id)!="eskayef":
        #     res_data = {"status": "Failed", "message": "Invalid Company ID"}
        # else:
        try:              
            emp_list=[]
            condition=""
            cond2=""
            # if employee_id!=None and employee_id!='':
            #     condition=f" and emp.emp_id='{employee_id}'"
            #     cond2=f" and emp_id='{employee_id}'"
            sql=f"""
                Select * from mrep_summary.cashier_collection where collection_date='{transaction_date}' and depot_id='{branch_name}'
                """
            
            query_job = client.query(sql)
            # Use REST endpoint only (default), no storage API
            df = query_job.result().to_dataframe()
            emp_list = df.to_dict(orient="records")
            
            branchRecord = db((db.branch.cid == cid) & (db.branch.code == branch_name)).select().first()
            if not branchRecord:
                return {"status": "Failed", "message": "Invalid Branch."}
            
            # Check if header already exists
            exists = db((db.tr_receipt_h.trans_date == transaction_date) & 
                        (db.tr_receipt_h.branch_id == branchRecord.id) & 
                        (db.tr_receipt_h.cid == cid)).select().first()
            if exists:
                # To prevent duplicates, we skip or return an error
                return {"status": "Failed", "message": "Receipt already synced for this date and branch."}
            
            # Insert Header
            trans_id = db.tr_receipt_h.insert(
                cid=cid,
                sl=branchRecord.name[:3].upper()+'-'+sl,
                branch_id=branchRecord.id,
                branch_name=branchRecord.name,
                trans_date=transaction_date
            )
            
            # Insert Details
            date_wise_receipt = []
            for row in emp_list:
                brand_name_str = row.get('brand')
                brandRecord = db((db.brand.cid == cid) & (db.brand.name == brand_name_str)).select().first()
                if not brandRecord:
                    continue
                
                date_wise_receipt.append({
                    'trans_id': trans_id,
                    'cid': cid,
                    'trans_sl': branchRecord.name[:3].upper() + '-' + sl,
                    'branch_id': branchRecord.id,
                    'branch_name': branchRecord.name,
                    'trans_date': transaction_date,
                    'segment_id': brandRecord.segment_id,
                    'segment_name': brandRecord.segment_name,
                    'brand_id': brandRecord.id,
                    'brand_name': brandRecord.name,
                    # 'collection': row.get('money_receipt', 0) or 0,
                    'collection': round(float(row.get('money_receipt', 0) or 0)),
                    'money_receipt': row.get('money_receipt', 0) or 0,
                    'adv_receipt': row.get('adv_receipt', 0) or 0,
                    'short_receipt': row.get('short_receipt', 0) or 0,
                    'adv_adj': row.get('adv_adj', 0) or 0,
                    'adj_plus': row.get('adj_minus', 0) or 0,#note: in mreporting adj_minus in cashier is adj_plus, VAT & AIT deducted from party
                    'adj_minus': row.get('adj_plus', 0) or 0,#note: in mreporting adj_plus in cashier is adj_minus, VAT & AIT deducted from party
                    'mr_reverse': row.get('mr_reverse', 0) or 0
                })
                
            if date_wise_receipt:
                db.tr_receipt_d.bulk_insert(date_wise_receipt)

            
        except Exception as e:
            res_data = {"status": "Failed", "message": str(e)}
            return res_data
            
    redirect(URL('date_wise_receipt', 'edit', vars=dict(id=trans_id)))


@action("sync_bq/import_sales")
@action.uses("sync_bq/import_sales.html",session,flash,db)
def import_sales(id=None):
    cid = session.get('cid')

    rows = db(db.brand.cid == cid).select(
    db.brand.id,
    db.brand.code,
    db.brand.name,
    db.brand.segment_id,
    db.brand.segment_name,
    orderby=[~db.brand.segment_name]
)
    branch_ids = session.get('branchCodeList')
    # print("branch_ids",branch_ids)
    query = ((db.branch.cid == cid)&(db.branch.status == 1))

    if session.get('role') != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            query &= db.branch.code.belongs(branch_ids)

    branchList = db(query).select()
    calendar_dates = active_calendar()
    active_date = calendar_dates['active_date'] if calendar_dates else None
    expire_at = calendar_dates['expire_at'] if calendar_dates else None
    
    formatted_date=date_time_list["date_fixed"].strftime(date_time_list["date_format"])

    return dict(session=session,check_role=check_role,rows=rows,branchList=branchList,active_date=active_date,expire_at=expire_at,formatted_date=formatted_date,date_time_list=date_time_list)


@action("sync_bq/sales_submit",method="POST")
@action.uses(session,flash,db)
def sales_submit():
    sl=get_sl()
    cid = session.get('cid')
    transaction_date = request.forms.get('transaction_date').strip()
    branch_name = request.forms.get('branch_name').strip()
    
    if transaction_date=='' or transaction_date==None or branch_name=='' or branch_name==None:
        res_data = {"status": "Failed", "message": "Transaction Date or Branch Name Missing"}
    else:
        try:              
            emp_list=[]           
            sql=f"""
                Select * from mrep_summary.cashier_sales where sales_date='{transaction_date}' and depot_id='{branch_name}'
                """
            
            query_job = client.query(sql)
            # Use REST endpoint only (default), no storage API
            df = query_job.result().to_dataframe()
            emp_list = df.to_dict(orient="records")
            
            branchRecord = db((db.branch.cid == cid) & (db.branch.code == branch_name)).select().first()
            if not branchRecord:
                return {"status": "Failed", "message": "Invalid Branch."}
            
            # Check if header already exists
            exists = db((db.tr_os_recon_h.trans_date == transaction_date) & 
                        (db.tr_os_recon_h.branch_id == branchRecord.id) & 
                        (db.tr_os_recon_h.cid == cid)).select().first()
            if exists:
                # To prevent duplicates, we skip or return an error
                return {"status": "Failed", "message": "Receipt already synced for this date and branch."}
            
            # Insert Header
            trans_id = db.tr_os_recon_h.insert(
                cid=cid,
                sl=branchRecord.name[:3].upper()+'-'+sl,
                branch_id=branchRecord.id,
                branch_name=branchRecord.name,
                trans_date=transaction_date
            )
            
            # Insert Details using BigQuery rows directly
            total_sales = 0.0
            return_sales = 0.0
            net_sales = 0.0
            outstanding_reconciliation = []

            for row in emp_list:
                brand_name_str = row.get('brand')
                brandRecord = db((db.brand.cid == cid) & (db.brand.name == brand_name_str)).select().first()
                if not brandRecord:
                    continue

                sales_tp_val      = float(row.get('sales_tp', 0) or 0)
                sales_vat_val     = float(row.get('sales_vat', 0) or 0)
                sales_disc_val    = float(row.get('sales_discount', 0) or 0)
                sales_sp_disc_val = float(row.get('sales_sp_disc', 0) or 0)
                sales_total_val   = float(row.get('sales_total', 0) or 0)

                return_tp_val      = float(row.get('return_tp', 0) or 0)
                return_vat_val     = float(row.get('return_vat', 0) or 0)
                return_disc_val    = float(row.get('return_discount', 0) or 0)
                return_sp_disc_val = float(row.get('return_sp_disc', 0) or 0)
                return_total_val   = float(row.get('return_total', 0) or 0)

                net_tp_val        = float(row.get('net_sales_tp', 0) or 0)
                net_vat_val       = float(row.get('net_sales_vat', 0) or 0)
                net_disc_val      = float(row.get('net_sales_discount', 0) or 0)
                net_sp_disc_val   = float(row.get('net_sales_sp_disc', 0) or 0)
                net_total_val     = float(row.get('net_sales_total', 0) or 0)

                total_sales  += sales_total_val
                return_sales += return_total_val
                net_sales    += net_total_val

                outstanding_reconciliation.append({
                    'trans_id': trans_id,
                    'cid': cid,
                    'trans_sl': f"{branchRecord.name[:3].upper()}-{sl}",
                    'branch_id': branchRecord.id,
                    'branch_name': branchRecord.name,
                    'trans_date': transaction_date,
                    'segment_id': brandRecord.segment_id,
                    'segment_name': brandRecord.segment_name,
                    'brand_id': brandRecord.id,
                    'brand_name': brandRecord.name,
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

            # Bulk insert details
            if outstanding_reconciliation:
                db.tr_os_recon_d.bulk_insert(outstanding_reconciliation)

            # Update header totals
            db((db.tr_os_recon_h.cid == cid) & (db.tr_os_recon_h.id == trans_id)).update(
                total_sales=total_sales,
                total_return=return_sales,
                total_net_sales=net_sales
            )

        except Exception as e:
            res_data = {"status": "Failed", "message": str(e)}
            return res_data

    redirect(URL('outstanding_reconciliation', 'edit', vars=dict(id=trans_id)))

