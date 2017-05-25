from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Task
from .common import is_chance, delete_all_tasks


class TaskTestCase(TestCase):

    def tst_views_test1(self):
        """Количество объектов в БД при разных вероятностях."""
        total = Task.objects.all().count()
        response = self.client.get(reverse('tasks_test1'))
        total2 = Task.objects.all().count()

        print(response.status_code, total2)

        if response.status_code == 200:
            self.assertEqual(total2, total + 2)
        else:
            self.assertEqual(total2, total + 1)

    def test_views_test1(self):
        """Запускает tst_views_test1() пять раз."""
        [self.tst_views_test1() for _ in range(5)]

    def test_is_chance(self):
        """Тест функции вероятности."""
        self.assertTrue(is_chance(100))
        self.assertFalse(is_chance())
        self.assertFalse(is_chance(''))
        self.assertFalse(is_chance(1000))

    def test_delete_all_tasks(self):
        self.assertEqual(None, delete_all_tasks())
