class MPGSurfacesRouter:
    """
    Routes all mpgsurfacesapp models to mpgsurface_db.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mpgsurfacesapp':
            return 'mpgsurface_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mpgsurfacesapp':
            return 'mpgsurface_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default', 'mpgsurface_db')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mpgsurfacesapp':
            return db == 'mpgsurface_db'
        return db == 'default'
