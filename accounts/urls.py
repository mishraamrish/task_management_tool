from django.conf.urls import url
from . import views as v

urlpatterns = [
    url(r'^signup/$', v.signup, name='signup'),
]
