from django.urls import path
from . import views

app_name = 'pet'

urlpatterns = [
    # 홈
    path('', views.pet_home, name='pet_home'),

    # ---------------------
    # 🐾 동물 관련
    # ---------------------
    path('animals/', views.animal_list, name='animal_list'),
    path('animals/add/', views.animal_create, name='animal_create'),
    path('animals/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animals/<int:pk>/edit/', views.animal_update, name='animal_update'),
    path('animals/<int:pk>/delete/', views.animal_delete, name='animal_delete'),
    path('animals/<int:pk>/like/', views.animal_like, name='animal_like'),
    path('animals/<int:pk>/comment/', views.animal_comment, name='animal_comment'),
    path('animals/<int:pk>/comment/<int:comment_id>/delete/', views.delete_animal_comment, name='delete_animal_comment'),

    # ---------------------
    # 📝 게시글 관련
    # ---------------------
    path('posts/', views.post_list, name='post_list'),
    path('posts/add/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_update, name='post_update'),  # ✅ 추가됨
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:pk>/like/', views.post_like, name='post_like'),
    path('posts/<int:pk>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # ---------------------
    # 👤 회원가입
    # ---------------------
    path('signup/', views.signup_view, name='signup'),

    # ---------------------
    # 🍖 펫 푸드 관련
    # ---------------------
    path('food/', views.pet_food_list, name='pet_food_list'),
    path('food/create/', views.pet_food_create, name='pet_food_create'),
    path('food/<int:pk>/', views.pet_food_detail, name='pet_food_detail'),
    path('food/<int:pk>/like/', views.pet_food_like, name='pet_food_like'),

    # ---------------------
    # 📍 생식거리 추천
    # ---------------------
    path('recommendations/', views.recommendation_list, name='recommendation_list'),
    path('recommendations/add/', views.recommendation_create, name='recommendation_create'),
    path('recommendations/<int:pk>/', views.recommendation_detail, name='recommendation_detail'),
    path('recommendations/<int:pk>/edit/', views.recommendation_update, name='recommendation_update'),
    path('recommendations/<int:pk>/delete/', views.recommendation_delete, name='recommendation_delete'),
]
