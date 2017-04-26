import os
from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import File, Link


class FileTestCase(TestCase):

    def setUp(self):
        self.path = os.path.join(settings.MEDIA_ROOT,
                                 datetime.now().strftime(File.UPLOAD_TO))
        self.total_files = len(os.listdir(self.path))

    def tst_anonymous_user(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('files-list'))
        self.assertEqual(response.status_code, 302)

    def tst_authorization(self):
        data = {'username': 'qqq', 'password': 'qqq'}
        response = self.client.post(reverse('index'), data)
        self.assertEqual(response.status_code, 404)

    def tst_registration1(self):
        data = {'username': 'qqq', 'password': 'qqq', 'is_register': 1}
        response = self.client.post(reverse('index'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sessionid' in response.cookies)

    def tst_authorized_user(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('files-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([], response.json())

    def tst_file_upload1(self):
        data = {'file': SimpleUploadedFile('xxx.txt', b'x' * 4096)}
        response = self.client.post(reverse('files-list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.all().count(), 1)
        self.assertEqual(File.objects.all().count(), 1)
        with self.assertRaises(ValueError):
            response.json()
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 1)

    def tst_file_upload2(self):
        """Дубликат первого."""
        data = {'file': SimpleUploadedFile('qqq.txt', b'x' * 4096)}
        response = self.client.post(reverse('files-list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.all().count(), 2)
        self.assertEqual(File.objects.all().count(), 1)
        self.assertEqual([['qqq', 'xxx.txt']], response.json())
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 1)

    def tst_file_upload3(self):
        """Дубликат первого, но на один байт больше (одинаковый MD5)."""
        data = {'file': SimpleUploadedFile('hhh.txt', b'x' * 4097)}
        response = self.client.post(reverse('files-list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.all().count(), 3)
        self.assertEqual(File.objects.all().count(), 2)
        with self.assertRaises(ValueError):
            response.json()
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 2)

    def tst_file_download1(self):
        response = self.client.get(reverse('download',
                                   kwargs={'pk': 1, 'name': 'any.ext'}))
        self.assertEqual(response.status_code, 200)

    def tst_file_download2(self):
        """Анонимно."""
        self.client.cookies.load({'sessionid': ''})
        response = self.client.get(reverse('download',
                                   kwargs={'pk': 2, 'name': 'any.ext'}))
        self.assertEqual(response.status_code, 200)

    def tst_file_download404(self):
        """Несуществующий файл."""
        response = self.client.get(reverse('download',
                                   kwargs={'pk': 404, 'name': 'any.ext'}))
        self.assertEqual(response.status_code, 404)

    def tst_registration2(self):
        data = {'username': 'hhh', 'password': 'hhh', 'is_register': 1}
        response = self.client.post(reverse('index'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sessionid' in response.cookies)

    def tst_file_upload4(self):
        data = {'file': SimpleUploadedFile('kkk.txt', b'q' * 4096)}
        response = self.client.post(reverse('files-list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.all().count(), 4)
        self.assertEqual(File.objects.all().count(), 3)
        with self.assertRaises(ValueError):
            response.json()
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 3)

    def tst_file_upload5(self):
        """Дубликат первого и второго."""
        data = {'file': SimpleUploadedFile('mmm.txt', b'x' * 4096)}
        response = self.client.post(reverse('files-list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Link.objects.all().count(), 5)
        self.assertEqual(File.objects.all().count(), 3)
        self.assertEqual([['qqq', 'xxx.txt'], ['qqq', 'qqq.txt']], response.json())
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 3)

    def tst_file_delete5(self):
        """Удаление дубликата первого и второго."""
        response = self.client.delete(reverse('files-detail', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Link.objects.all().count(), 4)
        self.assertEqual(File.objects.all().count(), 3)
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 3)

    def tst_file_delete4(self):
        response = self.client.delete(reverse('files-detail', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Link.objects.all().count(), 3)
        self.assertEqual(File.objects.all().count(), 2)
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 2)

    def tst_file_delete404(self):
        """Удаление файла, которого нет."""
        response = self.client.delete(reverse('files-detail', kwargs={'pk': 404}))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        for link in Link.objects.all():
            link.delete()
        self.assertEqual(Link.objects.all().count(), 0)
        self.assertEqual(File.objects.all().count(), 0)
        self.assertEqual(len(os.listdir(self.path)) - self.total_files, 0)

    def test_files(self):
        self.tst_anonymous_user()
        self.tst_authorization()
        self.tst_registration1()
        self.tst_authorized_user()
        self.tst_file_upload1()
        self.tst_file_upload2()
        self.tst_file_upload3()
        self.tst_file_download1()
        self.tst_file_download2()
        self.tst_file_download404()
        self.tst_registration2()
        self.tst_file_upload4()
        self.tst_file_upload5()
        self.tst_file_delete5()
        self.tst_file_delete4()
        self.tst_file_delete404()
