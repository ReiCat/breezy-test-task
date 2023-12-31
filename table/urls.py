from django.urls import path

from table import views

urlpatterns = [
    path(
        r'table', 
        views.generate_table, 
        name='generate-table'
    ),
    path(
        r'table/<int:table_id>',
        views.update_table_structure,
        name='update-table-structure'
    ),
    path(
        r'table/<int:table_id>/row',
        views.add_table_row,
        name='add-table-row'
    ),
    path(
        r'table/<int:table_id>/rows',
        views.get_table_rows,
        name='get-table-rows'
    ),
]
