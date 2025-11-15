from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect

from eapp import db, app
from eapp.models import Category, Product, UserRole


class AdminView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(AdminView):
    column_list = ['id', 'name', 'price', 'active', 'category_id']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    can_export = True
    edit_modal = True
    column_editable_list = ['name']
    page_size = 6

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name='Viettel Store Admin')

admin.add_view(AdminView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name='Đăng xuất'))