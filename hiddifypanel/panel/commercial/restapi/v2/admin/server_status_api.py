from apiflask import Schema
from apiflask.fields import Dict
from flask import current_app as app
from flask import g, request
from flask.views import MethodView

from hiddifypanel import hutils
from hiddifypanel.auth import login_required
from hiddifypanel.models import DailyUsage, Role
from hiddifypanel.models.usage import DailyUsage


class ServerStatusOutputSchema(Schema):
    stats = Dict(required=True,  metadata={"description": "System stats"})
    usage_history = Dict(required=True,  metadata={"description": "System usage history"})


class AdminServerStatusApi(MethodView):
    decorators = [login_required({Role.super_admin, Role.admin, Role.agent})]

    @app.output(ServerStatusOutputSchema)  # type: ignore
    def get(self):
        """System: ServerStatus"""
        dto = ServerStatusOutputSchema()
        dto.stats = {  # type: ignore
            'system': hutils.system.system_stats(),
            'top5': hutils.system.top_processes()
        }
        admin_id = request.args.get("admin_id") or g.account.id
        dto.usage_history = DailyUsage.get_daily_usage_stats(admin_id)  # type: ignore
        return dto
