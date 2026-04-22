from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.login_view,          name='login'),
    path('welcome/',           views.welcome_view,        name='welcome'),
    path('step2/',             views.step2_view,          name='step2'),
    path('loading/',           views.loading_view,        name='loading'),
    path('step3/',             views.step3_view,          name='step3'),
    path('step4/',             views.step4_view,          name='step4'),
    path('step5/',             views.step5_view,          name='step5'),
    path('success/library/',   views.success_library_view, name='success_library'),
    path('success/coffee/',    views.success_coffee_view,  name='success_coffee'),
    path('rejected/',          views.final_rejection_view, name='final_rejection'),
    path('logout/',            views.logout_view,          name='logout'),
]