

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields =('name', 'description',)
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('name', 'description',)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
