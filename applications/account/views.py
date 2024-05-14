# from ..account.forms import LoginForm, CustomUserCreationForm, OTPForm
from applications.account.forms import LoginForm, CustomUserCreationForm, OTPForm
# from .models import User, Profile
from applications.account.models import User, Profile
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
# from .forms import OTPForm, VerifyOTPForm
from applications.account.forms import OTPForm, VerifyOTPForm
# from .tasks import send_otp_email_task, send_activation_email_task
from applications.account.tasks import send_otp_email_task, send_activation_email_task
from config.redis import RedisDB
from django.contrib.auth import login, get_user_model
import random
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator


class SendOTPCodeView(View):
    template_name = 'accounts/otp_form.html'
    form_class = OTPForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if User.objects.filter(username=email).exists():
                subject = 'Login Code'
                message = str(random.randint(10000, 99999))
                RedisDB.set_redis(email, message)
                send_otp_email_task.delay(subject, message, email)
                request.session['email'] = email
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'لطفاً ابتدا ثبت نام کنید.')
                return render(request, self.template_name, {'form': form})

        return redirect('accounts:verify_otp')


class VerifyOTPView(View):
    template_name = 'accounts/verify_otp.html'
    form_class = VerifyOTPForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['otp']
            email = request.session.get('email')

            stored_code = RedisDB.get_redis(email).decode('utf-8')
            if stored_code and entered_code == stored_code:
                user = get_user_model().objects.get(email=email)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, 'ورود موفقیت آمیز بود.')
                    RedisDB.delete_redis(email)
                    return redirect('home')
                else:
                    messages.error(request, 'ورود با خطا مواجه شد.')
            else:
                messages.error(request, 'کد وارد شده صحیح نیست.')
        else:
            messages.error(request, 'خطایی رخ داده است. لطفا دوباره تلاش کنید.')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse_lazy('storage:home')

    def form_valid(self, form):
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('storage:home')


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.is_active = False
            user.save()

            Profile.objects.create(user=user)

            self.send_activation_email(request, user)

            return render(request, 'accounts/activate_email.html')

        return render(request, self.template_name, {'form': form})

    def send_activation_email(self, request, user):
        token = default_token_generator.make_token(user)
        activation_url = reverse('accounts:activate', args=[str(token)])
        activation_url = request.build_absolute_uri(activation_url)
        RedisDB.set_redis(token, user.id)
        send_activation_email_task.delay(user.id, activation_url)


class ActivateAccountView(View):
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        user_id = RedisDB.get_redis(token)
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, 'حساب کاربری با موفقیت فعال شد. اکنون می‌توانید وارد شوید.')
                    RedisDB.delete_redis('token')
                    return redirect('accounts:login')
                else:
                    messages.info(request, 'حساب کاربری شما قبلاً فعال شده است.')
            except User.DoesNotExist:
                pass
        else:
            messages.error(request, 'لینک فعال‌سازی نامعتبر است یا منقضی شده است.')

        return redirect('storage:home')

        # def get_user_by_token(self, token):
    #
    #     try:
    #         user_id = default_token_generator.check_token(str(token))
    #         return User.objects.get(id=user_id)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         return None


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
