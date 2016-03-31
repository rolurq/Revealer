from flask.ext.admin.contrib import sqla
from flask.ext.login import current_user


class RevealerModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()


class UserAdmin(RevealerModelView):
    column_exclude_list = ('password_hash', )
    column_searchable_list = ('name', 'username', 'email')
    column_editable_list = ('name', 'email')

    form_excluded_columns = column_exclude_list


class SlideshowAdmin(RevealerModelView):
    can_create = False
    column_exclude_list = ('presentations', 'created', 'last_presented')
    column_searchable_list = ('title',)
    column_editable_list = ('title',)
    column_filters = ('user', 'title')

    form_excluded_columns = column_exclude_list
