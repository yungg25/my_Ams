from django import forms
from .models import (
    Animal, Post, Comment, MissingAnimal, AnimalComment,
    PetFood, PetFoodRecommendation  # ✅ PetFoodRecommendation 모델 import
)


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'name', 'species', 'breed', 'age', 'gender',
            'neutered', 'vaccinated', 'personality',
            'description', 'image', 'location'
        ]
        labels = {
            'name': '🐾 이름',
            'species': '📘 동물 종류 (예: 강아지, 고양이)',
            'breed': '🔖 품종 (선택사항)',
            'age': '🎂 나이 (숫자만 입력)',
            'gender': '⚧ 성별',
            'neutered': '🩺 중성화 여부',
            'vaccinated': '💉 예방접종 여부',
            'personality': '🧠 성격 설명',
            'description': '📝 추가 설명',
            'image': '📷 사진 업로드',
        }
        widgets = {
            'personality': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '댓글을 입력하세요...'
            })
        }


class AnimalCommentForm(forms.ModelForm):
    class Meta:
        model = AnimalComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '동물에 대한 댓글을 입력하세요...'
            })
        }


class MissingAnimalForm(forms.ModelForm):
    class Meta:
        model = MissingAnimal
        fields = [
            'name', 'species', 'age', 'gender',
            'description', 'image', 'location', 'date_missing'
        ]
        labels = {
            'name': '이름',
            'species': '종',
            'age': '나이',
            'gender': '성별',
            'description': '설명',
            'image': '이미지',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date_missing': forms.DateInput(attrs={'type': 'date'}),
        }


class PetFoodForm(forms.ModelForm):
    class Meta:
        model = PetFood
        fields = ['title', 'ingredients', 'instructions', 'image']


# ✅ 생식거리 추천 등록 폼
class PetFoodRecommendationForm(forms.ModelForm):
    class Meta:
        model = PetFoodRecommendation
        fields = ['title', 'description', 'food_type', 'suitable_for', 'image']
        labels = {
            'title': '추천 제목',
            'description': '설명',
            'food_type': '음식 유형',
            'suitable_for': '적합한 동물',
            'image': '이미지',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
