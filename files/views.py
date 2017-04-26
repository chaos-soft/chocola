from rest_framework import viewsets
from django.http import HttpResponseNotFound, FileResponse, \
    HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views import View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Link
from .serializers import LinkSerializer
from .forms import LoginForm, UploadForm, FileForm


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    form_class = FileForm

    def get_queryset(self):
        return Link.objects.filter(user_id=self.request.user.id)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            links = Link.objects.select_related('user'). \
                only('file_id', 'name', 'user__username'). \
                filter(file__md5=form.cleaned_data['md5'],
                       file__size=form.cleaned_data['size']).order_by()
            data = dict(name=form.cleaned_data['file_name'],
                        user_id=self.request.user.id)

            if links:
                data['file_id'] = links[0].file_id
                users = [(v.user.username, v.name) for v in links]
            else:
                file = form.save()
                data['file_id'] = file.id

            link = Link(**data)
            link.save()

            if links and users:
                return JsonResponse(users, safe=False,
                                    json_dumps_params={'ensure_ascii': False})

            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class DownloadView(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        try:
            link = Link.objects.select_related('file').only('file__file'). \
                get(id=kwargs['pk'])
            return FileResponse(link.file.file,
                                content_type='application/force-download')
        except Link.DoesNotExist:
            return HttpResponseNotFound()


class IndexView(FormView):
    http_method_names = ('get', 'post')
    template_name='base.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = context['form']
        context['upload_form'] = UploadForm
        return context

    def form_invalid(self, form):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if not user:
            if User.objects.filter(username=form.cleaned_data['username']).count():
                return HttpResponseBadRequest()

            if form.cleaned_data['is_register']:
                user = User.objects.create_user(form.cleaned_data['username'],
                                                password=form.cleaned_data['password'])
            else:
                return HttpResponseNotFound()

        login(self.request, user)
        return HttpResponse()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseBadRequest()

        return super().post(request, *args, **kwargs)
