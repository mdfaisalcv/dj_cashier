from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash
from ..common_fn import check_role
import re

@action("change_password/index")
@action.uses("change_password/index.html",session,flash,db)
def index(id=None):
    
    return dict(session=session,check_role=check_role)


@action("change_password/submit", method=['POST'])
@action.uses("change_password/index.html", session,auth,T,db,flash)
def submit(id=None):  
    old_password=request.forms.get('old_password').strip()        
    new_password=request.forms.get('new_password').strip()        
    confirm_password=request.forms.get('confirm_password').strip()        
    errors=[]
    
    if old_password=='' or old_password is None:
        errors.append('Enter Old Password') 
    if new_password=='' or new_password is None:
        errors.append('Enter New Password') 
    if confirm_password=='' or confirm_password is None:
        errors.append('Enter Confirm Password') 
    else:
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#\-_=+])[A-Za-z\d@$!%*?&^#\-_=+]{8,}$'
        if not re.match(pattern, new_password):
            errors.append(
                "Password must be at least 8 characters long, include uppercase, lowercase, a number and a special character."
            )
    if confirm_password=='' or confirm_password is None:
        errors.append('Enter Confirm Password .') 
    else:
        if new_password != confirm_password:
            errors.append('Password and Confirm Password do not match.')

    rows=db((db.users.id==session.get('id'))&(db.users.status=='1')).select(db.users.id,limitby=(0,1))
    if not rows:
        errors.append('User not found')    

    rows_check=db((db.users.id==session.get('id'))&(db.users.password==old_password)).select(db.users.password,limitby=(0,1))
    if not rows_check:
        errors.append('Old Password is not correct')    

    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        redirect(URL('change_password','index')) 
    # insert function
    db(db.users.id == session.get('id')).update(
        password=new_password
    )
        
    flash.set('Password changed successfully', 'success')
    redirect(URL('change_password','index'))   

