from flask import Blueprint

from tit.admin.inventory.routes import inventory
# from tit.admin.reporting.routes import reporting
admin = Blueprint('admin', __name__, url_prefix='/admin')

admin.register_blueprint(inventory)
# admin.register_blueprint(reporting)
