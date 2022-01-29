from flask import Blueprint

from tit.admin.inventory.routes import inventory
admin = Blueprint('admin', __name__, url_prefix='/admin')
admin.register_blueprint(inventory)

