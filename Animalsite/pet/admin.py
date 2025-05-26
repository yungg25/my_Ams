from django.contrib import admin
from .models import (
    Animal,
    Comment,
    Post,
    MissingAnimal,
    AnimalComment,
    PetFood,
    PetFoodRecommendation  
)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'gender', 'neutered', 'vaccinated', 'created_at')
    search_fields = ('name', 'species', 'breed')
    list_filter = ('species', 'gender', 'neutered', 'vaccinated')  # 필터 추가해서 관리 편리하게

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title', 'content')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('category',)  # 카테고리별 필터 추가

@admin.register(MissingAnimal)
class MissingAnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'gender', 'location', 'date_missing', 'reported_by')
    search_fields = ('name', 'species', 'location', 'reported_by__username')
    list_filter = ('species', 'gender')  # 필터 추가

@admin.register(AnimalComment)
class AnimalCommentAdmin(admin.ModelAdmin):
    list_display = ('animal', 'user', 'created_at')
    search_fields = ('animal__name', 'user__username', 'content')

@admin.register(PetFood)
class PetFoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'ingredients', 'instructions')

@admin.register(PetFoodRecommendation)  
class PetFoodRecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'food_type', 'suitable_for', 'recommended_by', 'created_at')
    search_fields = ('title', 'description', 'suitable_for', 'recommended_by__username')
    list_filter = ('food_type',)
