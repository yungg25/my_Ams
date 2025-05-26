from django.db import models
from django.contrib.auth.models import User


class Animal(models.Model):
    GENDER_CHOICES = [
        ('수컷', '수컷'),
        ('암컷', '암컷'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='암컷')
    neutered = models.BooleanField(default=False)
    vaccinated = models.BooleanField(default=False)
    personality = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='animal_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_animals', blank=True)

    def __str__(self):
        return f"{self.name} ({self.species})"


class AnimalComment(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.animal.name}"


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('health', '건강 관리'),
        ('training', '훈련 팁'),
        ('tips', '팁 & 조언'),
        ('community', '커뮤니티'),
        ('events', '이벤트'),
        ('daily', '일상 공유'),
        ('food', '반려동물 음식'),
        ('funny', '웃긴 순간들'),
        ('travel', '여행과 외출'),
        ('question', '질문 있어요'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class MissingAnimal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Animal.GENDER_CHOICES, default='암컷')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='missing_animals/', blank=True)
    location = models.CharField(max_length=255)
    date_missing = models.DateField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.location} ({self.date_missing})"


class PetFood(models.Model):
    title = models.CharField("요리 제목", max_length=100)
    ingredients = models.TextField("재료")
    instructions = models.TextField("조리 방법")
    image = models.ImageField("이미지", upload_to='pet_foods/', blank=True)
    created_at = models.DateTimeField("등록일", auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_petfoods', blank=True)

    def __str__(self):
        return self.title


class PetFoodRecommendation(models.Model):
    FOOD_TYPE_CHOICES = [
        ('raw', '생식'),
        ('snack', '간식'),
        ('meal', '식사'),
    ]

    title = models.CharField("추천 제목", max_length=100)
    description = models.TextField("설명")
    food_type = models.CharField("음식 유형", max_length=20, choices=FOOD_TYPE_CHOICES, default='raw')
    suitable_for = models.CharField("적합한 동물", max_length=100, help_text="예: 강아지, 고양이 등")
    image = models.ImageField("이미지", upload_to='pet_food_recommendations/', blank=True)
    created_at = models.DateTimeField("추천일", auto_now_add=True)
    recommended_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="추천자")

    def __str__(self):
        return f"{self.title} ({self.get_food_type_display()})"
