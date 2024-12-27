from flask_admin import BaseView, expose


class StatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")
