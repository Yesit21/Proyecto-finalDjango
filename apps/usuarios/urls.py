from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    path('lista/', views.usuarios_lista, name='lista'),
    path('crear/', views.usuario_crear, name='crear'),
    path('<int:pk>/editar/', views.usuario_editar, name='editar'),
    path('<int:pk>/eliminar/', views.usuario_eliminar, name='eliminar'),
    path('<int:pk>/toggle-activo/', views.usuario_toggle_activo, name='toggle_activo'),
    
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/password_reset.html',
             email_template_name='emails/password_reset.html',
             success_url='/usuarios/password-reset/done/'
         ), 
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuarios/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/password_reset_confirm.html',
             success_url='/usuarios/reset/done/'
         ),
         name='password_reset_confirm'),
    
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuarios/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
