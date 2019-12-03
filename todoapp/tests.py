from django.test import TestCase
from django.contrib import messages
from .models import Task
from . import views
from django.urls import reverse,resolve
from django.utils import timezone
import datetime
import pytz
from django.forms import ModelForm

# モデルテスト
class TaskModelTests(TestCase):
    def test_conditions1_display(self):
        conditions1 = Task(conditions=1)
        self.assertEqual(conditions1.get_conditions_display(),'新規')

    def test_conditions2_display(self):
        conditions2 = Task(conditions=2)
        self.assertEqual(conditions2.get_conditions_display(),'作業中')

    def test_conditions3_display(self):
        conditions3 = Task(conditions=3)
        self.assertEqual(conditions3.get_conditions_display(),'完了')

def create_task(title,content,conditions):
    return Task.objects.create(title=title,content=content,conditions=conditions)

# 一覧ビューテスト
class TaskListsViewTests(TestCase):
    def test_no_tasks(self):
        response = self.client.get(reverse('todoapp:lists'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No tasks are registed.")
        self.assertQuerysetEqual(response.context['object_list'],[])

    def test_view_class(self):
        create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        view = resolve('/')
        self.assertEqual(view.func.view_class,views.Lists)

    def test_conditions1_task(self):
        create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: conditions1 task>'])

    def test_conditions2_task(self):
        create_task(title="conditions2 task",content="conditions2 task",conditions=2)
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: conditions2 task>'])

    def test_conditions3_task(self):
        create_task(title="conditions3 task",content="conditions3 task",conditions=3)
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: conditions3 task>'])

    def test_conditions1_task_and_test_conditions2_task_and_test_conditions3_task(self):
        create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        create_task(title="conditions2 task",content="conditions2 task",conditions=2)
        create_task(title="conditions3 task",content="conditions3 task",conditions=3)
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: conditions3 task>','<Task: conditions2 task>','<Task: conditions1 task>'])

    def test_two_conditions1_task(self):
        create_task(title="conditions1-1 task",content="conditions1-1 task",conditions=1)
        create_task(title="conditions1-2 task",content="conditions1-2 task",conditions=1)
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: conditions1-1 task>','<Task: conditions1-2 task>'])

    def test_conditions_change(self):
        conditions1_task = create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        conditions1_id = conditions1_task.id
        url = reverse('todoapp:conditions_change',args=(conditions1_task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,"/")
        response = self.client.get(reverse('todoapp:lists'))
        # リダイレクト先の状態変化が実装されているかテスト
        response_object = response.context['object_list']
        for item in response_object:
            conditions3 = item.conditions
            self.assertEqual(conditions3,3)

# 詳細ビューテスト
class TaskDetailViewTests(TestCase):
    def test_conditions1_task_status_code(self):
        conditions1_task = create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        url = reverse('todoapp:detail',args=(conditions1_task.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_conditions1_task_equal_contains(self):
        # conditions1_task = create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        conditions1_task = Task.objects.create(title="conditions1 task",content="conditions1 task",conditions=1,created_at=datetime.datetime.now())
        url = reverse('todoapp:detail',args=(conditions1_task.id,))
        response = self.client.get(url)
        tz = pytz.timezone('Japan')
        dt = conditions1_task.created_at
        d = tz.localize(dt)

        # responseの方は0:11でこっちは00:11になってる
        # >>%-mとすることで0埋めを回避(デフォルトでは0埋めされる仕様)
        strf_created_at = d.strftime('%Y年%-m月%-d日%-H:%M')
        self.assertContains(response,conditions1_task.title)
        self.assertContains(response,conditions1_task.content)
        self.assertContains(response,conditions1_task.conditions)
        self.assertContains(response,strf_created_at)

    def test_conditions2_task_equal_contains(self):
        conditions2_task = create_task(title="conditions2 task",content="conditions2 task",conditions=2)
        # conditions2_task = Task.objects.create(title="conditions2 task",content="conditions2 task",conditions=2,created_at=timezone.localtime(timezone.now()))
        url = reverse('todoapp:detail',args=(conditions2_task.id,))
        response = self.client.get(url)
        self.assertContains(response,conditions2_task.title)
        self.assertContains(response,conditions2_task.content)
        self.assertContains(response,conditions2_task.conditions)

    def test_conditions3_task_equal_contains(self):
        conditions3_task = create_task(title="conditions3 task",content="conditions3 task",conditions=3)
        # conditions3_task = Task.objects.create(title="conditions3 task",content="conditions3 task",conditions=3,created_at=timezone.localtime(timezone.now()))
        url = reverse('todoapp:detail',args=(conditions3_task.id,))
        response = self.client.get(url)
        self.assertContains(response,conditions3_task.title)
        self.assertContains(response,conditions3_task.content)
        self.assertContains(response,conditions3_task.conditions)

    def test_view_class(self):
        create_task(title="conditions3 task",content="conditions3 task",conditions=3)
        view = resolve('/1')
        self.assertEqual(view.func.view_class,views.Detail)

# 編集ビューテスト
class TaskUpdateViewTestCase(TestCase):
    def setUp(self):
        self.conditions1_task = create_task(title="conditions1 task",content="conditions1 task",conditions=1)
        self.conditions2_task = create_task(title="conditions2 task",content="conditions2 task",conditions=2)
        self.conditions3_task = create_task(title="conditions3 task",content="conditions3 task",conditions=3)

    def test_conditions1_task_status_code(self):
        url = reverse('todoapp:update',args=(self.conditions1_task.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_view_class(self):
        view = resolve('/update/1')
        self.assertEqual(view.func.view_class,views.Update)

    def test_csrf(self):
        url = reverse('todoapp:update',args=(self.conditions1_task.pk,))
        response = self.client.get(url)
        self.assertContains(response,'csrfmiddlewaretoken')

    def test_form_inputs(self):
        url = reverse('todoapp:update',args=(self.conditions2_task.pk,))
        response = self.client.get(url)
        form = response.context.get('form')
        #form_classがTaskFromだと思ったが違った
        # 解決方法にform_classをmodelformにするといける
        # >>何が元になっているかが大事(TaskFormというform_classが問題ではなかった)。
        # ModelForm使っていたのでModelForm指定すればテスト通った(import大事)
        self.assertIsInstance(form,ModelForm)

    def test_form_inputs(self):
        url = reverse('todoapp:update',args=(self.conditions3_task.pk,))
        response = self.client.get(url)
        # csrf,conditions,title
        self.assertContains(response,'<input',3)
        # content
        self.assertContains(response,'<textarea',1)

    def test_succsess_redirection(self):
        url = reverse('todoapp:update',args=(self.conditions1_task.pk,))
        response = self.client.post(url,{'title':'edit','content':'edit','conditions':2})
        lists_url = reverse('todoapp:lists')
        # 編集してからのリダイレクト先にきちんとリダイレクトされているか
        self.assertRedirects(response,lists_url)

    def test_succsess_post_changed(self):
        url = reverse('todoapp:update',args=(self.conditions1_task.pk,))
        response = self.client.post(url,{'title':'edit','content':'edit','conditions':2})
        # 変更post設定したあとそれで対象タスクをupdateビューで更新、その後モデルに変更されているかアクセス
        self.conditions1_task.refresh_from_db()
        self.assertEquals(self.conditions1_task.title,'edit')

    def test_invalid_status_code(self):
        url = reverse('todoapp:update',args=(self.conditions2_task.pk,))
        response = self.client.post(url,{})
        # 普通にcontextで取得するとcookieオブジェクトが帰ってきてforを使わざるを得なくなる
        # その対応策として下記の３文
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '保存できませんでした')

        self.assertEqual(response.status_code,200)

    def test_invalid_form_errors(self):
        url = reverse('todoapp:update',args=(self.conditions2_task.pk,))
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertTrue(form.errors)

# 追加ビューテスト
class TaskCreateViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('todoapp:create')

class TaskCreateViewTests(TaskCreateViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_view_class(self):
        view = resolve('/create')
        self.assertEqual(view.func.view_class,views.Create)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response,'<input',3)
        self.assertContains(self.response,'<textarea',1)

class SuccsessTaskCreateViewTests(TaskCreateViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url,{'title':'タイトル','content':'本文','conditions':1})

    def test_redirection(self):
        lists_url = reverse('todoapp:lists')
        self.assertRedirects(self.response,lists_url)

    def test_post_changed(self):
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: タイトル>'])

class InvalidTaskCreateViewTests(TaskCreateViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url,{})

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_error_message(self):
        message = list(self.response.context['messages'])
        self.assertEqual(len(message),1)
        self.assertEqual(str(message[0]),'保存できませんでした')

# 削除機能テスト
class TaskDeleteViewTestCase(TestCase):
    def setUp(self):
        self.task = create_task(title="テストタスク",content="テストテスト",conditions=1)
        self.task2 = create_task(title="テストタスク2",content="テストテスト2",conditions=2)
        self.url = reverse('todoapp:delete2',args=(self.task.pk,))

class TaskDeleteViewTests(TaskDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,302)

    def test_view_class(self):
        view = resolve('/delete2/1')
        self.assertEqual(view.func,views.delete)

class SuccessTaskDeleteView(TaskDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_redirection(self):
        lists_url = reverse('todoapp:lists')
        self.assertRedirects(self.response,lists_url)

    def test_delete_changegd(self):
        response = self.client.get(reverse('todoapp:lists'))
        self.assertQuerysetEqual(response.context['object_list'],['<Task: テストタスク2>'])

class InvalidTaskDeleteView(TaskDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.invalid_url = reverse('todoapp:delete2',args=(3,))
        self.response = self.client.get(self.invalid_url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,404)
