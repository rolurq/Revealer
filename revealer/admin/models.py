from flask.ext.admin.contrib import sqla
from flask.ext.login import current_user


class RevealerModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1


class UserAdmin(RevealerModelView):
    column_exclude_list = ('password_hash', )
    form_excluded_columns = column_exclude_list


class SlideshowAdmin(RevealerModelView):
    can_create = False
    column_exclude_list = ('presentations', 'created', 'last_presented')
    
    form_excluded_columns = column_exclude_list
