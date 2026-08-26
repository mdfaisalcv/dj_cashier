from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import random

# def user_log(task_name, activity, previous_json_data, current_json_data):
#     cid = str(session.get('cid'))
#     user_id = str(session.get('id'))
#     username = str(session.get('username'))
    
#     log_time = date_fixed  # Assuming already formatted

#     if previous_json_data:
#         keys_to_remove = ['field1','field2','note','created_by','updated_by','created_on', 'updated_on']
#         for key in keys_to_remove:
#             previous_json_data.pop(key, None)

#     if current_json_data:
#         keys_to_remove = ['field1','field2','note','created_by','updated_by','created_on', 'updated_on']
#         for key in keys_to_remove:
#             current_json_data.pop(key, None)

#     db.user_logs.insert(
#         cid=cid,
#         taskname=str(task_name),
#         activity=str(activity),
#         user_id=user_id,
#         username=username,
#         log_time=log_time,
#         current_data=current_json_data,  # Optionally store json_data
#         previous_data=previous_json_data,  # Optionally store json_data
#     )
#     db.commit()


# def check_role(task_id):
#     # Retrieve the task list from the session
#     task_list_str = session.get('task_listStr')  # Use 'current.session' for safe access
#     if not task_list_str:
#         return False  # Return False if the task list is not available

#     # Split task_listStr into a list and check for task_id
#     return task_id in task_list_str.split(',')

# def active_calendar():
#     if session.get('role') == 'super_admin':
#         return None  

#     record = db(
#         (db.open_date.user_id == session.get('id')) &
#         (db.open_date.expire_at == date_fixed)
#     ).select().first()

#     if not record:
#         return None

#     return {
#         "active_date": record.active_date,
#         "expire_at": record.expire_at
#     }


# def check_active_date(input_date):   
    
#     # today_date = datetime.now().date()
#     today_date = date_time_list["date_fixed"].strftime(date_time_list["date_format"])

#     today_date = datetime.strptime(str(today_date), "%Y-%m-%d").date()

#     last_three_active_dates = [
#         (today_date - timedelta(days=i)).strftime("%Y-%m-%d")
#         for i in range(4)
#     ]

#     record = db(
#         (db.open_date.user_id == session.get('id')) &
#         (db.open_date.expire_at == date_fixed)
#     ).select().first()

#     active_date = []

#     # return str(record)
#     if record and record.active_date:
#         # If active_date stored as comma-separated string
#         active_date = [d.strip() for d in str(record.active_date).split(",") if d.strip()]
#     # return str(active_date)
    

#     # return str(active_date)
#     if str(input_date) in active_date:
#         return "True"

#     # # Check whether any active date is within last 3 days including today
#     if str(input_date) in last_three_active_dates:
#         # return last_three_active_dates
#         return "True"
#     # return str(input_date)

#     return "False"

# def check_active_date_imprest(input_date):   
    
#     # today_date = datetime.now().date()
#     today_date = date_time_list["date_fixed"].strftime(date_time_list["date_format"])

#     today_date = datetime.strptime(str(today_date), "%Y-%m-%d").date()

#     last_three_active_dates = [
#         (today_date - timedelta(days=i)).strftime("%Y-%m-%d")
#         for i in range(31)
#     ]

#     record = db(
#         (db.open_date.user_id == session.get('id')) &
#         (db.open_date.expire_at == date_fixed)
#     ).select().first()

#     active_date = []

#     # return str(record)
#     if record and record.active_date:
#         # If active_date stored as comma-separated string
#         active_date = [d.strip() for d in str(record.active_date).split(",") if d.strip()]
#     # return str(active_date)
    

#     # return str(active_date)
#     if str(input_date) in active_date:
#         return "True"

#     # # Check whether any active date is within last 3 days including today
#     if str(input_date) in last_three_active_dates:
#         # return last_three_active_dates
#         return "True"
#     # return str(input_date)

#     return "False"




def get_sl():  
    random_number = random.randint(10, 99)    
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    trans_sl = current_datetime + str(random_number)
    return trans_sl

#=================== two digit after decimal point
def easy_format(amount,temp):
    return '{0:.2f}'.format(amount)

def easy_format(num):
    if num is not None:
        try:
            val = float(num)
            if round(val, 2) == 0:
                val = 0.0
            num = val
        except:
            pass
    return '{0:20,.2f}'.format(num)


