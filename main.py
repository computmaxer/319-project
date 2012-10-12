import os

from lib.flask import Flask
from lib.flask.views import MethodView
from lib.flask.templating import render_template

import auth
from auth import views as auth_views

from tournament import views as tournament_views
from tournament.templatetags import ttags


app = Flask(__name__)


class MainHandler(auth.UserAwareView):
    def get(self):
        context = dict()

        if self.user:
            context['username'] = self.user.username

#        self.render_response('home.html', context)
        return render_template('home.html')

#Define URLs
app.add_url_rule('/', view_func=MainHandler.as_view('home'))
app.add_url_rule('/auth/login/', view_func=auth_views.login.as_view('login'))
app.add_url_rule('/auth/logout/', view_func=auth_views.logout.as_view('logout'))
app.add_url_rule('/auth/register/', view_func=auth_views.logout.as_view('register'))
app.add_url_rule('/auth/check_username/', view_func=auth_views.logout.as_view('check_username'))

app.add_url_rule('/tournament/new/', view_func=tournament_views.new_tournament.as_view('new-tourney'))

#Setup other things
ttags.setup_jinja2_environment(app)

if __name__ == '__main__':
    app.run(debug=True)