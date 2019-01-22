from django.contrib.auth.decorators import login_required

class LoginCheck(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view  = super(LoginCheck, cls).as_view(**initkwargs)
        return login_required(view)