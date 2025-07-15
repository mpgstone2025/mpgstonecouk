# multi_store_project/db_routers.py

class MPGSurfacesRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mpgsurfaces':
            return 'mpgsurface_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mpgsurfaces':
            return 'mpgsurface_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mpgsurfaces':
            return db == 'mpgsurface_db'
        return None
