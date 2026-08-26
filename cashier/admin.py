from django.contrib import admin
from .models import Segment, Branch, UsersBranch


admin.site.register(Segment)
admin.site.register(Branch)
# admin.site.register(Users)
admin.site.register(UsersBranch)
# admin.site.register(UsersLogs)

