from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Project, BlogPost, Contact, Testimonial, QuoteRequest
from django import forms
from django.core.paginator import Paginator


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'category', 'image', 'description', 'date', 'client', 'location']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content', 'author', 'date', 'comments_count']


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'position', 'image', 'content']


def index(request):
    projects = Project.objects.all()[:6]
    blog_posts = BlogPost.objects.all()[:3]
    testimonials = Testimonial.objects.all()
    return render(request, 'index.html', {
        'projects': projects,
        'blog_posts': blog_posts,
        'testimonials': testimonials
    })


def project(request):
    projects = Project.objects.all()
    return render(request, 'project.html', {'projects': projects})


def about(request):
    return render(request, 'about.html')


def team(request):
    return render(request, 'team.html')


def blog(request):
    blog_posts_list = BlogPost.objects.all()
    paginator = Paginator(blog_posts_list, 6)  # Har sahifada 6 ta post
    page_number = request.GET.get('page')
    blog_posts = paginator.get_page(page_number)
    return render(request, 'blog.html', {'blog_posts': blog_posts})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('contact')
    return render(request, 'contact.html')


def work_single(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'work-single.html', {'project': project})


def blog_single(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    recent_posts = BlogPost.objects.exclude(id=post_id)[:3]
    return render(request, 'blog-single.html', {'post': post, 'recent_posts': recent_posts})


def main(request):
    return render(request, 'main.html')


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        return redirect('index')
    return redirect('index')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol xato.')
    return render(request, 'admin_login.html')


def admin_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} uchun hisob yaratildi! Endi tizimga kirishingiz mumkin.')
            return redirect('admin_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'admin_regiser.html', {'form': form})


def admin_logout(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz!')
    return redirect('index')


def admin_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Iltimos, tizimga kiring.')
        return redirect('admin_login')

    section = request.GET.get('section', 'dashboard')
    context = {'section': section, 'user': request.user}

    if section == 'projects':
        context['projects'] = Project.objects.all()
    elif section == 'blog_posts':
        context['blog_posts'] = BlogPost.objects.all()
    elif section == 'contacts':
        context['contacts'] = Contact.objects.all()
    elif section == 'testimonials':
        context['testimonials'] = Testimonial.objects.all()

    return render(request, 'admin_dashboard.html', context)


def admin_add_project(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loyiha muvaffaqiyatli qo‘shildi!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Forma to‘ldirishda xatolik yuz berdi.')
    else:
        form = ProjectForm()
    return render(request, 'admin_form.html', {'form': form, 'title': 'Yangi Loyiha Qo‘shish'})


def admin_edit_project(request, project_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loyiha muvaffaqiyatli tahrirlandi!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Forma to‘ldirishda xatolik yuz berdi.')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'admin_form.html', {'form': form, 'title': 'Loyihani Tahrirlash'})


def admin_delete_project(request, project_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, 'Loyiha muvaffaqiyatli o‘chirildi!')
    return redirect('admin_dashboard')


def admin_add_blog_post(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post muvaffaqiyatli qo‘shildi!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Forma to‘ldirishda xatolik yuz berdi.')
    else:
        form = BlogPostForm()
    return render(request, 'admin_form.html', {'form': form, 'title': 'Yangi Blog Post Qo‘shish'})


def admin_edit_blog_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post muvaffaqiyatli tahrirlandi!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Forma to‘ldirishda xatolik yuz berdi.')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'admin_form.html', {'form': form, 'title': 'Blog Postni Tahrirlash'})


def admin_delete_blog_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    messages.success(request, 'Blog post muvaffaqiyatli o‘chirildi!')
    return redirect('admin_dashboard')


def admin_delete_contact(request, contact_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, 'Kontakt muvaffaqiyatli o‘chirildi!')
    return redirect('admin_dashboard')


def admin_add_testimonial(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial muvaffaqiyatli qo‘shildi!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Forma to‘ldirishda xatolik yuz berdi.')
    else:
        form = TestimonialForm()
    return render(request, 'admin_form.html', {'form': form, 'title': 'Yangi Testimonial Qo‘shish'})


def admin_edit_testimonial(request, testimonial_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial muvaffaqiyatli tahrirlandi!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Forma to‘ldirishda xatolik yuz berdi.')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'admin_form.html', {'form': form, 'title': 'Testimonialni Tahrirlash'})


def admin_delete_testimonial(request, testimonial_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    messages.success(request, 'Testimonial muvaffaqiyatli o‘chirildi!')
    return redirect('admin_dashboard')

def quote_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Ma'lumotlarni saqlash
        QuoteRequest.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Muvaffaqiyat xabari
        messages.success(request, 'Sizning so‘rovingiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog‘lanamiz.')
        return redirect(request.META.get('HTTP_REFERER', 'index'))  # Foydalanuvchi qaysi sahifadan kelgan bo‘lsa, o‘sha sahifaga qaytarish

    return redirect('index')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Ma'lumotlarni saqlash
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Muvaffaqiyat xabari
        messages.success(request, 'Sizning xabaringiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog‘lanamiz.')
        return redirect('contact')

    return render(request, 'contact.html')