from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Animal, Post, Comment, AnimalComment, PetFood, PetFoodRecommendation
from .forms import AnimalForm, PostForm, CommentForm, AnimalCommentForm, PetFoodForm, PetFoodRecommendationForm


# 홈
def pet_home(request):
    species = request.GET.get('species')
    if species == '강아지':
        animals = Animal.objects.filter(species='강아지').order_by('-created_at')[:6]
    elif species == '고양이':
        animals = Animal.objects.filter(species='고양이').order_by('-created_at')[:6]
    else:
        animals = Animal.objects.order_by('-created_at')[:6]
    featured = Animal.objects.order_by('?').first()
    posts = Post.objects.order_by('-created_at')[:5]
    return render(request, 'pet/pet_home.html', {
        'animals': animals,
        'posts': posts,
        'selected_species': species or '전체',
        'featured': featured,
    })


# 동물 CRUD 및 좋아요
@login_required
def animal_create(request):
    form = AnimalForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('pet:animal_list')
    return render(request, 'pet/animal_form.html', {'form': form})


@login_required
def animal_update(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    form = AnimalForm(request.POST or None, request.FILES or None, instance=animal)
    if form.is_valid():
        form.save()
        return redirect('pet:animal_detail', pk=pk)
    return render(request, 'pet/animal_form.html', {'form': form, 'title': '동물 정보 수정'})


@login_required
def animal_delete(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        animal.delete()
        return redirect('pet:animal_list')
    return redirect('pet:animal_detail', pk=pk)


def animal_list(request):
    species = request.GET.get('species')
    if species == '강아지':
        animals = Animal.objects.filter(species='강아지')
    elif species == '고양이':
        animals = Animal.objects.filter(species='고양이')
    else:
        animals = Animal.objects.all()
    featured = Animal.objects.order_by('?').first()
    return render(request, 'pet/pet_home.html', {
        'animals': animals,
        'selected_species': species or '전체',
        'featured': featured,
    })


@login_required
def animal_like(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.user in animal.likes.all():
        animal.likes.remove(request.user)
    else:
        animal.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def animal_comment(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    form = AnimalCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.animal = animal
        comment.user = request.user
        comment.save()
    return redirect('pet:animal_detail', pk=pk)


@login_required
def delete_animal_comment(request, pk, comment_id):
    comment = get_object_or_404(AnimalComment, id=comment_id, animal_id=pk)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
    return redirect('pet:animal_detail', pk=pk)


def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    comments = animal.animalcomment_set.order_by('-created_at')
    return render(request, 'pet/pet_detail.html', {
        'animal': animal,
        'comments': comments,
        'comment_form': AnimalCommentForm(),
        'prev_animal': Animal.objects.filter(pk__lt=pk).order_by('-pk').first(),
        'next_animal': Animal.objects.filter(pk__gt=pk).order_by('pk').first(),
    })


# 게시글 목록 및 상세, 생성, 수정, 삭제
def post_list(request):
    category = request.GET.get('category')
    if category:
        posts = Post.objects.filter(category=category).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'pet/post_list.html', {
        'posts': posts,
        'form': form,
    })


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST' and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect(reverse('pet:post_detail', args=[pk]) + "#comments")
    return render(request, 'pet/post_detail.html', {
        'post': post,
        'comments': post.comments.all(),
        'comment_form': comment_form
    })


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('pet:post_list')
    return render(request, 'pet/post_form.html', {'form': form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user and not request.user.is_superuser:
        return redirect('pet:post_detail', pk=pk)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('pet:post_detail', pk=pk)
    return render(request, 'pet/post_form.html', {'form': form, 'title': '게시글 수정'})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('pet:post_list')
    return redirect('pet:post_detail', pk=pk)


@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=pk)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
    return redirect('pet:post_detail', pk=pk)


# 게시글 좋아요
@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# 회원가입
def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("/")
    return render(request, "registration/signup.html", {"form": form})


# 펫 푸드 관련
def pet_food_list(request):
    foods = PetFood.objects.order_by('-created_at')
    return render(request, 'pet/pet_food_list.html', {'foods': foods})


def pet_food_detail(request, pk):
    food = get_object_or_404(PetFood, pk=pk)
    return render(request, 'pet/pet_food_detail.html', {'food': food})


@login_required
def pet_food_create(request):
    form = PetFoodForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('pet:pet_food_list')
    return render(request, 'pet/pet_food_form.html', {'form': form})


@login_required
def pet_food_like(request, pk):
    food = get_object_or_404(PetFood, pk=pk)
    if request.user in food.likes.all():
        food.likes.remove(request.user)
    else:
        food.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))


# 생식거리 추천 관련
def recommendation_list(request):
    items = PetFoodRecommendation.objects.order_by('-created_at')
    return render(request, 'pet/pet_fresh.html', {'items': items})


def recommendation_detail(request, pk):
    item = get_object_or_404(PetFoodRecommendation, pk=pk)
    prev_item = PetFoodRecommendation.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_item = PetFoodRecommendation.objects.filter(pk__gt=pk).order_by('pk').first()
    return render(request, 'pet/pet_fresh_detail.html', {
        'item': item,
        'prev_item': prev_item,
        'next_item': next_item,
    })


@login_required
def recommendation_create(request):
    form = PetFoodRecommendationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        recommendation = form.save(commit=False)
        recommendation.recommended_by = request.user
        recommendation.save()
        return redirect('pet:recommendation_list')
    return render(request, 'pet/pet_fresh_form.html', {'form': form})


@login_required
def recommendation_update(request, pk):
    recommendation = get_object_or_404(PetFoodRecommendation, pk=pk)
    if request.user != recommendation.recommended_by and not request.user.is_superuser:
        return redirect('pet:recommendation_detail', pk=pk)
    form = PetFoodRecommendationForm(request.POST or None, request.FILES or None, instance=recommendation)
    if form.is_valid():
        form.save()
        return redirect('pet:recommendation_detail', pk=pk)
    return render(request, 'pet/pet_fresh_form.html', {'form': form, 'title': '생식거리 추천 수정'})


@login_required
def recommendation_delete(request, pk):
    recommendation = get_object_or_404(PetFoodRecommendation, pk=pk)
    if request.user == recommendation.recommended_by or request.user.is_superuser:
        if request.method == 'POST':
            recommendation.delete()
            return redirect('pet:recommendation_list')
    return redirect('pet:recommendation_detail', pk=pk)
