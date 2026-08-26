# from django.apps import apps
# from django.db import connection
# from django.db.models import AutoField


# class Command(BaseCommand):
#     help = "Reorder MySQL table columns based on Django model field order"

#     def handle(self, *args, **options):

#         cursor = connection.cursor()

#         for model in apps.get_models():

#             table = model._meta.db_table

#             previous = None

#             for field in model._meta.local_fields:

#                 if isinstance(field, AutoField):
#                     previous = field.column
#                     continue

#                 db_type = field.db_type(connection)

#                 if db_type is None:
#                     continue

#                 nullable = "NULL" if field.null else "NOT NULL"

#                 default = ""

#                 if field.has_default() and field.default is not None:
#                     if isinstance(field.default, str):
#                         default = f"DEFAULT '{field.default}'"
#                     else:
#                         default = f"DEFAULT {field.default}"

#                 if previous:

#                     sql = f"""
#                     ALTER TABLE `{table}`
#                     MODIFY COLUMN `{field.column}`
#                     {db_type}
#                     {nullable}
#                     {default}
#                     AFTER `{previous}`;
#                     """

#                     try:
#                         cursor.execute(sql)
#                     except Exception as e:
#                         self.stdout.write(str(e))

#                 previous = field.column

#         self.stdout.write(self.style.SUCCESS("Column reorder completed."))