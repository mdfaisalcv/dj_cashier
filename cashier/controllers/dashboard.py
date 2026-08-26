from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
# from cashier.models import dashboard

# ── Format helpers (defined at module level, safe to call anywhere) ────────
# def _fmt_m(val):
#     """Format value as Millions string, e.g. 3518238706 -> '3,518.24M'"""
#     v = float(val or 0)
#     return '{:,.2f}M'.format(v / 1_000_000)

# def _fmt_cr(val):
#     """Format value as Crore string, e.g. 3518238706 -> '351.82 Cr'"""
#     v = float(val or 0)
#     return '{:,.2f} Cr'.format(v / 10_000_000)

# def _fmt_num(val):
#     v = float(val or 0)
#     return '{:,.2f}'.format(v)

# def _fmt_month(m):
#     try:
#         dt = datetime.strptime(m, '%Y-%m')
#         return dt.strftime('%b, %Y')
#     except Exception:
#         return m or ''


@login_required
def index(request):        
    return render(request, 'dashboard/index.html')



# ==============================================================================
# COMMON HELPERS FOR DASHBOARD APIs
# ==============================================================================

# def _get_common_filters():
#     cid = session.cid
#     branch_conditions = ""
#     if session.get('role') != 'super_admin':
#         branch_id_session = session.get('branchList')
#         if branch_id_session:
#             branch_id_list = [str(c).strip() for c in branch_id_session if str(c).strip()]
#             if branch_id_list:
#                 branch_conditions = " AND h.branch_id IN ({})".format(
#                     ",".join("'{}'".format(bid) for bid in branch_id_list)
#                 )

#     month_first_date = (
#         date_time_list["current_year"] + '-' +
#         date_time_list["current_month"] + '-01'
#     )
#     current_date = date_time_list["current_date"]
    
#     date_conditions = ""
#     if current_date:
#         date_conditions = (
#             " AND h.trans_date >= '{}' AND h.trans_date <= '{}'".format(
#                 month_first_date, current_date
#             )
#         )
    
#     conditions = branch_conditions + date_conditions
#     return cid, branch_conditions, date_conditions, conditions, month_first_date, current_date

# def _get_active_segments():
#     segment_rows = db.executesql("SELECT id AS segment_id, name AS segment_name FROM segment WHERE status = 1 ORDER BY name DESC", as_dict=True)
#     active_segment_ids = [str(row['segment_id']) for row in segment_rows]
#     if active_segment_ids:
#         seg_id_list = ",".join(active_segment_ids)
#         active_seg_recon   = " AND d.segment_id IN ({})".format(seg_id_list)
#         active_seg_receipt = " AND d.segment_id IN ({})".format(seg_id_list)
#         active_seg_deposit = " AND d.segment_id IN ({})".format(seg_id_list)
#     else:
#         active_seg_recon   = " AND 1=0"
#         active_seg_receipt = " AND 1=0"
#         active_seg_deposit = " AND 1=0"
#     return segment_rows, active_seg_recon, active_seg_receipt, active_seg_deposit

# def _calculate_outstanding(cid, branch_conditions, end_dt_obj, active_seg_receipt, active_seg_recon, end_dt, historyStart):
#     query = f"""
#     SELECT
#         f.branch_id,
#         f.trans_date,
#         SUM(f.opening_balance)  AS opening_balance,
#         SUM(f.net_sales_total)  AS net_sales_total,
#         SUM(f.net_collection)   AS net_collection,
#         SUM(f.mr_reverse)       AS mr_reverse,
#         SUM(f.adjustment_plus)  AS adjustment_plus,
#         SUM(f.adjustment_minus) AS adjustment_minus,
#         MAX(f.is_checkpoint)    AS is_checkpoint
#     FROM
#     (   
#         SELECT
#             h.branch_id, h.trans_date,
#             0 AS opening_balance, 0 AS net_sales_total,
#             SUM(d.collection) AS net_collection, SUM(d.mr_reverse) AS mr_reverse,
#             SUM(d.adj_plus) AS adjustment_plus, SUM(d.adj_minus) AS adjustment_minus,
#             0 AS is_checkpoint
#         FROM tr_receipt_h h
#         JOIN tr_receipt_d d ON h.id = d.trans_id
#         WHERE h.cid = '{cid}' AND h.trans_date >= '{historyStart}' AND h.trans_date <= '{end_dt}'
#         {branch_conditions} {active_seg_receipt}
#         GROUP BY h.branch_id, h.trans_date

#         UNION ALL

#         SELECT
#             h.branch_id, h.trans_date,
#             0 AS opening_balance, SUM(d.net_sales_total) AS net_sales_total,
#             0 AS net_collection, 0 AS mr_reverse, 0 AS adjustment_plus, 0 AS adjustment_minus,
#             0 AS is_checkpoint
#         FROM tr_os_recon_h h
#         JOIN tr_os_recon_d d ON h.id = d.trans_id
#         WHERE h.cid = '{cid}' AND h.trans_date >= '{historyStart}' AND h.trans_date <= '{end_dt}'
#         {branch_conditions} {active_seg_recon}
#         GROUP BY h.branch_id, h.trans_date

#         UNION ALL

#         SELECT
#             h.branch_id, h.trans_date,
#             SUM(d.outstanding) as opening_balance,
#             0 AS net_sales_total, 0 AS net_collection, 0 AS mr_reverse, 0 AS adjustment_plus, 0 AS adjustment_minus,
#             1 AS is_checkpoint
#         FROM opening_h h
#         JOIN opening_d d ON h.id = d.trans_id
#         WHERE h.cid = '{cid}' {branch_conditions} {active_seg_recon}
#         GROUP BY h.branch_id, h.trans_date
#     ) f
#     GROUP BY f.branch_id, f.trans_date
#     ORDER BY f.trans_date, f.branch_id
#     """
    
#     recordListRaw = db.executesql(query, as_dict=True)
#     data_map = {}
#     for row in recordListRaw:
#         bid = row['branch_id']
#         dt = row['trans_date']
#         if isinstance(dt, str):
#             try: dt = datetime.strptime(dt, '%Y-%m-%d').date()
#             except: dt = date(1900, 1, 1)
#         elif isinstance(dt, datetime): dt = dt.date()
        
#         if bid not in data_map: data_map[bid] = {}
#         data_map[bid][dt] = row

#     total_outstanding = 0
#     branch_outstanding = {}
#     branch_dt_balance = {}  # {bid: {dt: balance}}
    
#     for bid, bid_data in data_map.items():
#         trans_dates = sorted(bid_data.keys())
#         if not trans_dates: continue
            
#         running_bal = 0
#         current_dt = trans_dates[0]
#         branch_dt_balance[bid] = {}
        
#         while current_dt <= end_dt_obj:
#             day_data = bid_data.get(current_dt, {})
#             if day_data.get('is_checkpoint') == 1:
#                 running_bal = float(day_data.get('opening_balance') or 0)
                
#             ns = float(day_data.get('net_sales_total') or 0)
#             col = float(day_data.get('net_collection') or 0)
#             rev = float(day_data.get('mr_reverse') or 0)
#             ap = float(day_data.get('adjustment_plus') or 0)
#             am = float(day_data.get('adjustment_minus') or 0)
            
#             running_bal = running_bal + ns - col + rev + ap - am
#             branch_dt_balance[bid][current_dt] = running_bal
            
#             current_dt += timedelta(days=1)
            
#         total_outstanding += running_bal
#         branch_outstanding[str(bid)] = running_bal
        
#     return total_outstanding, branch_outstanding, branch_dt_balance

# def _check_access():
#     task_id = 'dashboard_manage'
#     task_id_view = 'dashboard_view'
#     if not (check_role(task_id) or check_role(task_id_view)):
#         return False
#     return True

# # ==============================================================================
# # NEW API ENDPOINTS
# # ==============================================================================

# @action("dashboard/api_summary_cards", method=["GET", "POST"])
# @action.uses(session, db)
# def api_summary_cards():
#     if not _check_access(): return dict(error="Access is Denied")
#     cid, branch_conditions, date_conditions, conditions, month_first_date, current_date = _get_common_filters()
#     segment_rows, active_seg_recon, active_seg_receipt, active_seg_deposit = _get_active_segments()
    
#     sales_data = db.executesql(f"SELECT sum(d.net_sales_total) as total_net_sales FROM tr_os_recon_h h LEFT JOIN tr_os_recon_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_recon}", as_dict=True)
#     collection_data = db.executesql(f"SELECT SUM(d.collection) as collection, SUM(d.mr_reverse) as mr_reverse, SUM(d.adj_plus) as adj_plus, SUM(d.adj_minus) as adj_minus FROM tr_receipt_h h LEFT JOIN tr_receipt_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_receipt}", as_dict=True)
#     deposit_data = db.executesql(f"SELECT SUM(d.amount) as amount FROM tr_deposit_h h LEFT JOIN tr_deposit_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_deposit}", as_dict=True)
#     petty_cash_data = db.executesql(f"SELECT sum(h.total_exp) as total_exp FROM tr_petty_cash_h h WHERE 1 {conditions}", as_dict=True)

#     total_net_sales  = sum(float(r.get('total_net_sales') or 0) for r in sales_data)
#     total_collection = sum(float(r.get('collection') or 0) for r in collection_data)
#     total_mr_reverse = sum(float(r.get('mr_reverse') or 0) for r in collection_data)
#     total_adj_plus = sum(float(r.get('adj_plus') or 0) for r in collection_data)
#     total_adj_minus = sum(float(r.get('adj_minus') or 0) for r in collection_data)
#     total_deposit    = sum(float(r.get('amount') or 0) for r in deposit_data)
#     total_expense    = float((petty_cash_data[0].get('total_exp') or 0) if petty_cash_data else 0)

#     end_dt = current_date if current_date else str(date.today())
#     end_dt = datetime.strptime(end_dt, '%Y-%m-%d') - timedelta(days=1)
#     end_dt = end_dt.strftime('%Y-%m-%d')
#     end_dt_obj = datetime.strptime(end_dt, '%Y-%m-%d').date()

#     check_query = f"SELECT MIN(max_dt) as history_start FROM (SELECT MAX(trans_date) as max_dt FROM opening_h h WHERE h.cid = '{cid}' AND h.trans_date <= '{end_dt}' {branch_conditions} GROUP BY h.branch_id) t"
#     res = db.executesql(check_query, as_dict=True)
#     historyStart = str(res[0]['history_start']) if res and res[0]['history_start'] else end_dt
    
#     total_outstanding, _, _ = _calculate_outstanding(cid, branch_conditions, end_dt_obj, active_seg_receipt, active_seg_recon, end_dt, historyStart)

#     try:
#         curr_dt = datetime.strptime(month_first_date, '%Y-%m-%d')
#         current_month_label = curr_dt.strftime('%B, %Y')
#     except Exception:
#         current_month_label = date_time_list.get("current_month", "")

#     return dict(
#         summary_cards=dict(
#             month_label   = current_month_label,
#             sales_m       = _fmt_m(total_net_sales),
#             sales_cr      = _fmt_cr(total_net_sales),
#             collection_m  = _fmt_m(total_collection + total_mr_reverse + total_adj_plus - total_adj_minus),
#             collection_cr = _fmt_cr(total_collection + total_mr_reverse + total_adj_plus - total_adj_minus),
#             deposit_m     = _fmt_m(total_deposit),
#             deposit_cr    = _fmt_cr(total_deposit),
#             expense_m     = _fmt_m(total_expense),
#             expense_cr    = _fmt_cr(total_expense),
#             outstanding_m = _fmt_m(total_outstanding),
#             outstanding_cr= _fmt_cr(total_outstanding),
#         )
#     )

# @action("dashboard/api_segment_breakdown", method=["GET", "POST"])
# @action.uses(session, db)
# def api_segment_breakdown():
#     if not _check_access(): return dict(error="Access is Denied")
#     cid, branch_conditions, date_conditions, conditions, month_first_date, current_date = _get_common_filters()
#     segment_rows, active_seg_recon, active_seg_receipt, active_seg_deposit = _get_active_segments()

#     sales_data = db.executesql(f"SELECT max(d.segment_name) as segment_name, sum(d.net_sales_total) as total_net_sales FROM tr_os_recon_h h LEFT JOIN tr_os_recon_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_recon} GROUP BY d.segment_id", as_dict=True)
#     collection_data = db.executesql(f"SELECT d.segment_name, SUM(d.collection) as collection, SUM(d.money_receipt) as money_receipt, SUM(d.mr_reverse) as mr_reverse, SUM(d.adj_plus) as adj_plus, SUM(d.adj_minus) as adj_minus FROM tr_receipt_h h LEFT JOIN tr_receipt_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_receipt} GROUP BY d.segment_id", as_dict=True)
#     deposit_data = db.executesql(f"SELECT d.segment_name, SUM(d.amount) as amount FROM tr_deposit_h h LEFT JOIN tr_deposit_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_deposit} GROUP BY d.segment_id", as_dict=True)

#     seg_map = {row['segment_name']: {'sales': 0.0, 'collection': 0.0, 'money_receipt': 0.0, 'deposit': 0.0} for row in segment_rows}
#     seg_map['Unknown'] = {'sales': 0.0, 'collection': 0.0, 'money_receipt': 0.0, 'deposit': 0.0}

#     total_sales = total_coll = total_mr = total_dep = 0.0

#     for r in sales_data:
#         seg = r.get('segment_name') or 'Unknown'
#         if seg not in seg_map: seg = 'Unknown'
#         val = float(r.get('total_net_sales') or 0)
#         seg_map[seg]['sales'] += val
#         total_sales += val

#     for r in collection_data:
#         seg = r.get('segment_name') or 'Unknown'
#         if seg not in seg_map: seg = 'Unknown'
#         coll_val = float(r.get('collection') or 0) + float(r.get('mr_reverse') or 0) + float(r.get('adj_plus') or 0) - float(r.get('adj_minus') or 0)
#         mr_val = float(r.get('money_receipt') or 0) + float(r.get('mr_reverse') or 0) + float(r.get('adj_plus') or 0) - float(r.get('adj_minus') or 0)
#         seg_map[seg]['collection'] += coll_val
#         seg_map[seg]['money_receipt'] += mr_val
#         total_coll += coll_val
#         total_mr += mr_val

#     for r in deposit_data:
#         seg = r.get('segment_name') or 'Unknown'
#         if seg not in seg_map: seg = 'Unknown'
#         val = float(r.get('amount') or 0)
#         seg_map[seg]['deposit'] += val
#         total_dep += val

#     seg_list = []
#     for row in segment_rows:
#         seg = row['segment_name']
#         d = seg_map[seg]
#         seg_list.append(dict(
#             name=seg,
#             sales_num=_fmt_num(d['sales']), sales_m=_fmt_cr(d['sales']),
#             collection_num=_fmt_num(d['collection']), collection_m=_fmt_cr(d['collection']),
#             money_receipt_num=_fmt_num(d['money_receipt']), money_receipt_m=_fmt_cr(d['money_receipt']),
#             deposit_num=_fmt_num(d['deposit']), deposit_m=_fmt_cr(d['deposit']),
#         ))

#     return dict(
#         seg_list=seg_list,
#         seg_totals=dict(
#             sales_num=_fmt_num(total_sales), sales_m=_fmt_cr(total_sales),
#             collection_num=_fmt_num(total_coll), collection_m=_fmt_cr(total_coll),
#             money_receipt_num=_fmt_num(total_mr), money_receipt_m=_fmt_cr(total_mr),
#             deposit_num=_fmt_num(total_dep), deposit_m=_fmt_cr(total_dep),
#         )
#     )

# @action("dashboard/api_branch_breakdown", method=["GET", "POST"])
# @action.uses(session, db)
# def api_branch_breakdown():
#     if not _check_access(): return dict(error="Access is Denied")
#     cid, branch_conditions, date_conditions, conditions, month_first_date, current_date = _get_common_filters()
#     segment_rows, active_seg_recon, active_seg_receipt, active_seg_deposit = _get_active_segments()

#     branch_sales_data = db.executesql(f"SELECT h.branch_id, MAX(h.branch_name) as branch_name, SUM(d.net_sales_total) as total_net_sales FROM tr_os_recon_h h LEFT JOIN tr_os_recon_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_recon} GROUP BY h.branch_id", as_dict=True)
#     branch_coll_data = db.executesql(f"SELECT h.branch_id, MAX(h.branch_name) as branch_name, SUM(d.money_receipt) as money_receipt, SUM(d.mr_reverse) as mr_reverse, SUM(d.adj_plus) as adj_plus, SUM(d.adj_minus) as adj_minus FROM tr_receipt_h h LEFT JOIN tr_receipt_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_receipt} GROUP BY h.branch_id", as_dict=True)
#     branch_dep_data = db.executesql(f"SELECT h.branch_id, MAX(h.branch_name) as branch_name, SUM(d.amount) as amount FROM tr_deposit_h h LEFT JOIN tr_deposit_d d ON h.id = d.trans_id WHERE 1 {conditions} {active_seg_deposit} GROUP BY h.branch_id", as_dict=True)

#     end_dt = current_date if current_date else str(date.today())
#     end_dt = datetime.strptime(end_dt, '%Y-%m-%d') - timedelta(days=1)
#     end_dt = end_dt.strftime('%Y-%m-%d')
#     end_dt_obj = datetime.strptime(end_dt, '%Y-%m-%d').date()
    
#     check_query = f"SELECT MIN(max_dt) as history_start FROM (SELECT MAX(trans_date) as max_dt FROM opening_h h WHERE h.cid = '{cid}' AND h.trans_date <= '{end_dt}' {branch_conditions} GROUP BY h.branch_id) t"
#     res = db.executesql(check_query, as_dict=True)
#     historyStart = str(res[0]['history_start']) if res and res[0]['history_start'] else end_dt
    
#     _, branch_outstanding, _ = _calculate_outstanding(cid, branch_conditions, end_dt_obj, active_seg_receipt, active_seg_recon, end_dt, historyStart)

#     branch_map = {}
#     all_bids = set([str(b) for b in branch_outstanding.keys()])
#     for r in branch_sales_data + branch_coll_data + branch_dep_data:
#         all_bids.add(str(r['branch_id']))

#     if all_bids:
#         branch_rows = db(db.branch.id.belongs(list(all_bids))).select(db.branch.id, db.branch.name)
#         bname_dict = {str(r.id): r.name for r in branch_rows}
#     else:
#         bname_dict = {}

#     for bid in all_bids:
#         branch_map[bid] = {'name': bname_dict.get(bid, f"Branch {bid}"), 'sales': 0.0, 'money_receipt': 0.0, 'deposit': 0.0, 'outstanding': branch_outstanding.get(bid, 0.0)}

#     for r in branch_sales_data: branch_map[str(r['branch_id'])]['sales'] += float(r.get('total_net_sales') or 0)
#     for r in branch_coll_data: branch_map[str(r['branch_id'])]['money_receipt'] += float(r.get('money_receipt') or 0) + float(r.get('mr_reverse') or 0) + float(r.get('adj_plus') or 0) - float(r.get('adj_minus') or 0)
#     for r in branch_dep_data: branch_map[str(r['branch_id'])]['deposit'] += float(r.get('amount') or 0)

#     branch_list = []
#     for bid in sorted(branch_map.keys(), key=lambda x: branch_map[x]['name']):
#         d = branch_map[bid]
#         branch_list.append(dict(
#             name=d['name'], sales_val=d['sales'],
#             sales_num=_fmt_num(d['sales']), sales_m=_fmt_cr(d['sales']),
#             money_receipt_num=_fmt_num(d['money_receipt']), money_receipt_m=_fmt_cr(d['money_receipt']),
#             deposit_num=_fmt_num(d['deposit']), deposit_m=_fmt_cr(d['deposit']),
#             outstanding_num=_fmt_num(d['outstanding']), outstanding_m=_fmt_cr(d['outstanding']),
#         ))

#     return dict(
#         branch_list=branch_list,
#         branch_totals=dict(
#             sales_num=_fmt_num(sum(d['sales'] for d in branch_map.values())), sales_m=_fmt_cr(sum(d['sales'] for d in branch_map.values())),
#             money_receipt_num=_fmt_num(sum(d['money_receipt'] for d in branch_map.values())), money_receipt_m=_fmt_cr(sum(d['money_receipt'] for d in branch_map.values())),
#             deposit_num=_fmt_num(sum(d['deposit'] for d in branch_map.values())), deposit_m=_fmt_cr(sum(d['deposit'] for d in branch_map.values())),
#             outstanding_num=_fmt_num(sum(d['outstanding'] for d in branch_map.values())), outstanding_m=_fmt_cr(sum(d['outstanding'] for d in branch_map.values())),
#         )
#     )

# @action("dashboard/api_monthly_trend", method=["GET", "POST"])
# @action.uses(session, db)
# def api_monthly_trend():
#     if not _check_access(): return dict(error="Access is Denied")
#     cid, branch_conditions, date_conditions, conditions, month_first_date, current_date = _get_common_filters()
#     segment_rows, active_seg_recon, active_seg_receipt, active_seg_deposit = _get_active_segments()

#     month_sales = db.executesql(f"SELECT substr(h.trans_date,1,7) as month, SUM(d.net_sales_total) as total_net_sales FROM tr_os_recon_h h LEFT JOIN tr_os_recon_d d ON h.id = d.trans_id WHERE 1 {branch_conditions} {active_seg_recon} GROUP BY substr(h.trans_date,1,7) ORDER BY substr(h.trans_date,1,7) DESC LIMIT 6", as_dict=True)
#     month_collection = db.executesql(f"SELECT substr(h.trans_date,1,7) as month, SUM(d.collection) as total_collection, SUM(d.mr_reverse) as total_reverse, SUM(d.adj_plus) as total_adjustment_plus, SUM(d.adj_minus) as total_adjustment_minus FROM tr_receipt_h h LEFT JOIN tr_receipt_d d ON h.id = d.trans_id WHERE 1 {branch_conditions} {active_seg_receipt} GROUP BY substr(h.trans_date,1,7) ORDER BY substr(h.trans_date,1,7) DESC LIMIT 6", as_dict=True)
#     month_money_receipt = db.executesql(f"SELECT substr(h.trans_date,1,7) as month, SUM(d.money_receipt) as total_moneyReceipt, SUM(d.mr_reverse) as total_reverse, SUM(d.adj_plus) as total_adjustment_plus, SUM(d.adj_minus) as total_adjustment_minus FROM tr_receipt_h h LEFT JOIN tr_receipt_d d ON h.id = d.trans_id WHERE 1 {branch_conditions} {active_seg_receipt} GROUP BY substr(h.trans_date,1,7) ORDER BY substr(h.trans_date,1,7) DESC LIMIT 6", as_dict=True)
#     month_deposit = db.executesql(f"SELECT substr(h.trans_date,1,7) as month, SUM(d.amount) as total_deposit_amount FROM tr_deposit_h h LEFT JOIN tr_deposit_d d ON h.id = d.trans_id WHERE 1 {branch_conditions} {active_seg_deposit} GROUP BY substr(h.trans_date,1,7) ORDER BY substr(h.trans_date,1,7) DESC LIMIT 6", as_dict=True)
#     month_petty = db.executesql(f"SELECT substr(h.trans_date,1,7) as month, SUM(h.total_exp) as total_exp FROM tr_petty_cash_h h WHERE 1 {branch_conditions} GROUP BY substr(h.trans_date,1,7) ORDER BY substr(h.trans_date,1,7) DESC LIMIT 6", as_dict=True)

#     ms_map = {r['month']: r for r in month_sales}
#     mc_map = {r['month']: r for r in month_collection}
#     mmr_map = {r['month']: r for r in month_money_receipt}
#     md_map = {r['month']: r for r in month_deposit}
#     mp_map = {r['month']: r for r in month_petty}

#     all_month_keys = sorted(set(list(ms_map.keys()) + list(mc_map.keys()) + list(md_map.keys()) + list(mp_map.keys())), reverse=True)

#     end_dt = current_date if current_date else str(date.today())
#     end_dt = datetime.strptime(end_dt, '%Y-%m-%d') - timedelta(days=1)
#     end_dt = end_dt.strftime('%Y-%m-%d')
#     end_dt_obj = datetime.strptime(end_dt, '%Y-%m-%d').date()

#     if all_month_keys:
#         earliest_month = all_month_keys[-1]
#         earliest_date_str = f"{earliest_month}-01"
#     else:
#         earliest_date_str = end_dt

#     month_end_dates = {}
#     for m in all_month_keys:
#         yr, mn = map(int, m.split('-'))
#         if mn == 12: next_month = date(yr + 1, 1, 1)
#         else: next_month = date(yr, mn + 1, 1)
#         month_end = next_month - timedelta(days=1)
#         if month_end > end_dt_obj: month_end = end_dt_obj
#         month_end_dates[m] = month_end

#     check_query = f"SELECT MIN(max_dt) as history_start FROM (SELECT MAX(trans_date) as max_dt FROM opening_h h WHERE h.cid = '{cid}' AND h.trans_date <= '{earliest_date_str}' {branch_conditions} GROUP BY h.branch_id) t"
#     res = db.executesql(check_query, as_dict=True)
#     historyStart = str(res[0]['history_start']) if res and res[0]['history_start'] else earliest_date_str

#     _, _, branch_dt_balance = _calculate_outstanding(cid, branch_conditions, end_dt_obj, active_seg_receipt, active_seg_recon, end_dt, historyStart)

#     branch_month_outstanding = {}
#     for m, m_end in month_end_dates.items():
#         branch_month_outstanding[m] = {}
#         for bid, dts in branch_dt_balance.items():
#             if m_end in dts:
#                 branch_month_outstanding[m][bid] = dts[m_end]
#             else:
#                 available_dts = [d for d in dts.keys() if d <= m_end]
#                 if available_dts:
#                     branch_month_outstanding[m][bid] = dts[max(available_dts)]
#                 else:
#                     branch_month_outstanding[m][bid] = 0

#     month_cols = []
#     for m in all_month_keys:
#         ms_v  = float(ms_map.get(m, {}).get('total_net_sales') or 0)
#         mc_v  = float(mc_map.get(m, {}).get('total_collection') or 0)
#         mmr_v = float(mmr_map.get(m, {}).get('total_moneyReceipt') or 0)
#         t_rev = float(mc_map.get(m, {}).get('total_reverse') or 0)
#         t_adp = float(mc_map.get(m, {}).get('total_adjustment_plus') or 0)
#         t_adm = float(mc_map.get(m, {}).get('total_adjustment_minus') or 0)
#         md_v  = float(md_map.get(m, {}).get('total_deposit_amount') or 0)
#         mp_v  = float(mp_map.get(m, {}).get('total_exp') or 0)
#         out_v = sum(branch_month_outstanding.get(m, {}).values())

#         month_cols.append(dict(
#             label        = _fmt_month(m),
#             sales_m      = _fmt_cr(ms_v), sales_cr = _fmt_cr(ms_v), sales_chart = round(ms_v / 10000000, 2),
#             coll_m       = _fmt_cr(mc_v+t_rev+t_adp-t_adm), coll_cr = _fmt_cr(mc_v+t_rev+t_adp-t_adm), coll_chart = round((mc_v+t_rev+t_adp-t_adm) / 10000000, 2),
#             money_receipt_m = _fmt_cr(mmr_v+t_rev+t_adp-t_adm), money_receipt_cr = _fmt_cr(mmr_v+t_rev+t_adp-t_adm), money_receipt_chart = round((mmr_v+t_rev+t_adp-t_adm) / 10000000, 2),
#             dep_m        = _fmt_cr(md_v), dep_cr = _fmt_cr(md_v), dep_chart = round(md_v / 10000000, 2),
#             exp_m        = _fmt_cr(mp_v), exp_cr = _fmt_cr(mp_v), exp_chart = round(mp_v / 10000000, 2),
#             out_m        = _fmt_cr(out_v), out_cr = _fmt_cr(out_v), out_chart = round(out_v / 10000000, 2),
#         ))

#     return dict(month_cols=month_cols, has_months=len(month_cols) > 0)
