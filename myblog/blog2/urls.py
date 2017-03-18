from django.conf.urls import url
import blog2.views as bv


urlpatterns = [
    url(r'^index2/', bv.index2),
    url(r'^map/$', bv.index),
]