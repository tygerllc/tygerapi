from django.template import RequestContext
from django.views.generic import ListView, DetailView
from bench.models import Bench

class BenchListView(ListView):
    model = Bench
    template_name = 'bench_list.html'
    context_object_name = 'open_challenge_list'

    def get_queryset(self):
        return Bench.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BenchListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context

class BenchDetailView(DetailView):
    model = Bench
    template_name = 'bench_detail.html'
    context_object_name = 'b'

    def get_queryset(self):
        return Bench.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BenchDetailView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context