from flask import request
from flask.templating import render_template

import auth
import forms
import models

class new_tournament(auth.UserAwareView):
    def get(self):
        context = {
            'fields':{'step':1},
        }
        thing = models.Match(round=1, has_been_played=False, next_match=None)
        thing.put()
        return self.render_new_tourney(context)

    def post(self):
        context = {'fields':{}}
        step = int(request.form.get('step'))
        if step == 1:
            form = forms.NewTournamentStep1(request.form)
            if form.validate():
                context['fields'].update(form.data)
                context['fields'].update({'step':2})
                context['form'] = forms.NewTournamentStep2()
                return self.render_new_tourney(context)
            else:
                return self.render_new_tourney({'fields':{'step':1}, 'form':form})
        elif step == 2:
            form = forms.NewTournamentStep2(request.form)
            if form.validate():
                context['fields'].update(form.data)
                context['fields'].update({
                    'tournament_security':request.form.get('tournament_security')})
                context['fields'].update({'step':3})
                context['form'] = forms.NewTournamentStep3()
                return self.render_new_tourney(context)
            else:
                return self.render_new_tourney({'fields':{'step':2}, 'form':form})
        elif step == 3:
            pass

    #Made this so I don't have to type the template a bunch of times
    def render_new_tourney(self, context):
        if 'fields' in context:
            step = context['fields'].get('step', 1)
        else:
            step = 1
        #self.render_response('new_tournament/new_tournament_%s.html' % step, context)
        return render_template('new_tournament/new_tournament_%s.html' % step, **context)