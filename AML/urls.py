# AML/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from pet import views  # signup_view 사용

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👤 인증 관련 뷰 (로그인, 로그아웃, 회원가입)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # 🐾 pet 앱의 URL 연결 (네임스페이스 포함)
    path('', include(('pet.urls', 'pet'), namespace='pet')),
]

# 🖼️ 개발 환경에서 media 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
