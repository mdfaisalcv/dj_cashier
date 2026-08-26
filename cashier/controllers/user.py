from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.db import transaction
from cashier.models import Branch, UsersBranch
import re

@login_required
def index(request):
    return render(request, 'user/index.html')

@login_required
def create(request):
    cid = request.session.get('cid')
    branch_ids = request.session.get('branchList')
    branches = Branch.objects.filter(status=1, cid=cid)

    if Group != 'super_admin' and branch_ids:
        if isinstance(branch_ids, str):
            branch_ids = [int(b) for b in branch_ids.split(',') if b.strip()]
        elif isinstance(branch_ids, list):
            branch_ids = [int(b) for b in branch_ids if b]

        if branch_ids:
            branches = branches.filter(id__in=branch_ids)

    branchList = branches

    context = { 
        'branchList': branchList
    }

    groups = Group.objects.all()
    return render(request, 'user/create.html', {'groups': groups, 'branchList': branchList})

@login_required
def submit(request):

    cid = request.session.get('cid')

    if request.method == 'POST':

        # --------------------------------------------------
        # Form Data
        # --------------------------------------------------

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('user_name', '').strip()
        email = request.POST.get('email', '').strip()

        password = request.POST.get('pass', '').strip()

        password_confirm = request.POST.get(
            'pass_confirmation',
            ''
        ).strip()

        role = request.POST.get('role', '').strip()

        branch_list = request.POST.getlist('branch_list')

        status = 1 if request.POST.get('status') == '1' else 0


        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        errors = []

        if not first_name:
            errors.append('Enter first name')

        elif not last_name:
            errors.append('Enter last name')

        elif not username:
            errors.append('Enter user name')

        elif not email:
            errors.append('Enter email')

        elif not password:
            errors.append('Enter password')

        elif not password_confirm:
            errors.append('Enter password confirmation')

        elif password != password_confirm:
            errors.append(
                'Password and confirm password do not match'
            )

        elif not role:
            errors.append('Enter role')

        elif not branch_list:
            errors.append('Enter branch list')


        # --------------------------------------------------
        # Password Validation
        # --------------------------------------------------

        # if password:

            # pattern = (
            #     r'^(?=.*[a-z])'
            #     r'(?=.*[A-Z])'
            #     r'(?=.*\d)'
            #     r'(?=.*[@$!%*?&^#\-_=+])'
            #     r'[A-Za-z\d@$!%*?&^#\-_=+]{8,}$'
            # )

            # if not re.match(pattern, password):

            #     errors.append(
            #         'Password must be at least 8 characters long, '
            #         'include uppercase, lowercase, a number and '
            #         'a special character.'
            #     )


        # --------------------------------------------------
        # Duplicate Check
        # --------------------------------------------------

        if username and User.objects.filter(
            username__iexact=username
        ).exists():

            errors.append('User name already exists')


        # --------------------------------------------------
        # Error
        # --------------------------------------------------

        if errors:

            for msg in errors:
                messages.warning(request, msg)

            return redirect('cashier:user-create')


        # --------------------------------------------------
        # Insert User + Role + Branch
        # --------------------------------------------------

        try:

            with transaction.atomic():

                # ------------------------------------------
                # Create User
                # ------------------------------------------

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                print(user)
                user.is_active = True if status == 1 else False
                user.save()


                # ------------------------------------------
                # Assign Role / Group
                # ------------------------------------------

                group = Group.objects.filter(
                    name=role
                ).first()
                print(group)
                if group:

                    user.groups.add(group)


                # ------------------------------------------
                # Create User Branch
                # ------------------------------------------

                branch = UsersBranch.objects.create(
                    cid=cid,
                    user=user
                )
                print(branch)

                # ------------------------------------------
                # Assign Multiple Branches
                # ------------------------------------------

                branches = Branch.objects.filter(
                    cid=cid,
                    id__in=branch_list
                )
                print(branches)
                branch.branches.set(branches)


        except Exception as e:
            print(e)
            messages.error(
                request,
                f'User creation failed: {str(e)}'
            )

            return redirect('cashier:user-create')


        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        messages.success(
            request,
            'User created successfully!'
        )

        return redirect('cashier:user-index')


    return redirect('cashier:user-index')


@login_required
def get_data(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 16))

    users = User.objects.all().order_by('username')

    records_total = users.count()

    users = users[start:start + length]

    data = []

    for item in users:
        data.append({
            'id': item.id,
            'username': item.username,
            'first_name': item.first_name,
            'last_name': item.last_name,
            'email': item.email,
            'role': '',
            'branches': '',
            'status': 1 if item.is_active else 0,
        })

    return JsonResponse({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_total,
        'data': data,
    })