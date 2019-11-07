from django.db import models
from django.utils import timezone

CONDITIONS = (
	(1,'新規'),
	(2,'作業中'),
	(3,'完了'),
)
class Task(models.Model):
	title = models.CharField('タイトル',max_length=32)
	content = models.TextField('本文')
	conditions = models.IntegerField('状態', choices=CONDITIONS,default=1)
	created_at = models.DateTimeField('作成日',default=timezone.now)

	def __str__(self):
		return self.title
