from django.db import models
from django.utils import timezone

CONDITIONS = (
	(1,'新規'),
	(2,'作業中'),
	(3,'完了'),
)

class Category(models.Model):
	author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	text = models.CharField('カテゴリー',max_length=32)

	def __str__(self):
		return self.text

class Task(models.Model):
	author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	title = models.CharField('タイトル',max_length=32)
	content = models.TextField('本文',default='None')
	conditions = models.IntegerField('状態', choices=CONDITIONS,default=1)
	created_at = models.DateTimeField('作成日',default=timezone.now)

	def __str__(self):
		return self.title
