#App 만들면 python manage.py startapp blog 다음에 settings.py로 가서 해당 앱 추가해주세요!!

from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) #유일한값 가져야 함
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True) #읽을 수 있는 text로 url #한글 사용 가능

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    class Meta: #복수형 지정
        verbose_name_plural='Categories'

#Post 모델 만들기
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100,blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)  #비어있어도 괜찮음, 필수 조건 ㄴㄴ
    #%Y 2022, %y 22
    file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True) #시간을 한국으로 설정하기 위해서는 settings.py 가서 TIME_ZONE ='Asia/Seoul'로 변경
    updated_at = models.DateTimeField(auto_now=True) #auto_now_add=True auto_now=True admin에서 입력 필드 사라짐

    #추후 author 작성
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #다대일 관계 정의 #user사라지면 None 되는 구조

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL) #유효성 검사시 공간 허용
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self): #admin 페이지에서 보이는 이름 설정
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}'

    def get_absolute_url(self): #개별 레코드 고유 url정의
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1] #a.txt => a txt

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'
    def get_absolute_url(self): #개별 레코드 고유 url정의
        return f'{self.post.get_absolute_url()}#comment-{{self.pk}}'
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'