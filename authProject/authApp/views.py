from django.shortcuts import render, redirect
# 8. 从 Django 的 auth 模块导入三个重要的函数：authenticate、login 和 logout
from django.contrib.auth import authenticate, login, logout
# 9. 一种装饰器，用于限制仅登录用户访问某些视图。如果用户未登录，他们将被重定向到登录页面。
from django.contrib.auth.decorators import login_required
# 10. 基于类的视图中使用的 mixin，需要登录才能访问视图。类似于 login_required 装饰器，但用于基于类的视图
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
# 11. Django 中的默认用户模型，代表应用程序中的用户，User 模型是用于处理用户身份验证和用户信息的一个核心模型
from django.contrib.auth.models import User
# 12. 自定义表单（可能用于用户注册），将在 forms.py 文件中定义。
from .forms import RegisterForm
# Create your views here.


def register_view(request):
    # 13. 检查请求方法是否为 POST：用于将数据发送到服务器。当用户提交表单（如注册表单）时，数据将通过 POST 请求发送到服务器进行处理。如果方法为 “POST”，则表示用户已填写并提交表单。此时，我们需要处理表单数据（即，验证它，创建用户，并让他们登录）。
    if request.method == "POST":
        #  14. 创建 RegisterForm 实例，并传入用户提交的数据： 该行 form = RegisterForm(request.POST) 创建 RegisterForm 类的实例，并传入用户通过 POST 请求提交的数据。获取用户提交的表单数据：request.POST 包含用户在网页上输入的内容，比如用户名、密码等。我们把这些数据传递给表单 RegisterForm，这样表单就知道用户提交了什么信息。
        form = RegisterForm(request.POST)
        # 15. 这一步检查用户提交的表单数据是否通过了验证。Django 会自动根据 RegisterForm 中定义的字段规则（如用户名长度、密码格式等）来判断数据是否符合要求。
        if form.is_valid():
            # 16. 如果表单数据有效，获取清理后的用户名。
            # 16. cleaned username 是指在 Django 表单中，用户输入的数据经过验证和处理后的结果。具体来说，它是从原始输入中提取出的合法、安全的数据。这个过程称为数据清理（data cleaning）。
            username = form.cleaned_data.get("username")
            # 17. 同样地，获取经过验证的密码。
            password = form.cleaned_data.get("password")
            # 18. 使用 Django 提供的 User 模型，创建一个新的用户对象。create_user() 函数会自动处理密码的加密存储。这里把你之前获得的用户名传递给这个方法，把你获得的密码也传递给这个方法。
            user = User.objects.create_user(
                username=username, password=password)
            # 19. Django 会在用户的会话中创建一个标记，表明该用户已经通过身份验证。这意味着用户在后续的请求中不需要重新登录，保持会话状态，同时，Django 会在会话中存储与用户相关的信息（如用户的 ID），以便在未来的请求中快速查找用户。
            login(request, user)
            # 20. 重定向到主页：使得用户在完成某个操作后（如注册、登录等）被引导到另一个页面，提供了良好的用户体验。

            return redirect('home')
    else:
        # 21。 创建空表单: 如果表单数据无效（即 form.is_valid() 返回 False），则创建一个新的空表单实例并渲染注册页面，以便用户可以重新输入信息。创建了一个RegisterForm表单类实例。
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    error_message = None
    # 22. 检查请求的方法是否为 POST：即检查用户是否填写并提交了表单
    if request.method == "POST":
        # 23. 获得用户名和密码：从 POST 请求中提取用户输入的用户名和密码。这两个变量将用于身份验证。
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 24. 验证用户身份：使用 authenticate() 函数来验证提供的用户名和密码。如果提供的凭证正确，则返回一个 User 对象，否则返回 None。
        user = authenticate(request, username=username, password=password)
        # 25. 用户身份信息匹配： 如果 user 不为 None，说明用户名和密码正确，用户已成功通过身份验证
        if user is not None:
            # 26. 标记用户已登录：调用 login() 函数，将用户登录到系统中。这会在用户的会话中创建一个标记，表示用户已经成功登录。
            login(request, user)
            # 27. 成功登录重定向到主页： 从 POST 请求或 GET 请求中提取重定向 URL（如果有的话），如果没有，则默认重定向到 'home' 页面。这确保用户在成功登录后被引导到他们想要访问的页面。
            next_url = request.POST.get(
                "next") or request.GET.get("next") or 'home'
            return redirect(next_url)
        else:
            # 如果用户提供的凭证不正确，则创建一个错误消息，提示用户凭证无效。
            error_message = "Invalid Credentials!"
        # 使用 render() 函数重新渲染登录页面，并将错误消息传递给模板，以便在页面上显示给用户。
    return render(request, 'accounts/login.html', {"error": error_message})


# 用于处理用户注销的逻辑
# 28. 函数接收一个 request 对象，该对象代表用户发出的 HTTP 请求。根据请求的类型（POST 或 GET），执行不同的操作。
def logout_view(request):
    # 29. 这里检查请求是否为 POST 方法。如果是 POST 请求，表示用户明确要求登出（例如点击“登出”按钮）。
    if request.method == "GET":
        # 30. 调用 Django 提供的 logout() 函数，清除当前用户的会话（session），即将用户从登录状态中移除。
        logout(request)
        # 31. 注销后，用户被重定向到名为 login 的 URL（通常是登录页面）。
        return redirect('login')
    else:
        # 32. 在这种情况下，用户将被重定向到名为 home 的页面。这可能是应用的主页，表示用户并未请求登出操作。
        print("Logout attempted with GET method.")
        return redirect('home')

# 33. 是 Django 提供的一个装饰器，用于限制对某些视图的访问。如果未登录的用户尝试访问这个视图，Django 会自动将他们重定向到登录页面。用户必须登录后才能访问这个视图，未登录用户将会被重定向到登录页面。


@login_required
# 35. 登录后，视图会渲染并显示 home/home.html 页面，这是网站的主页或用户登录后的主界面。
def home_view(request):
    return render(request, 'auth1_app/home.html')

# Protected View

# 36. 是 Django 提供的一个用于类视图的混入类 (Mixin)，用来确保只有登录的用户才能访问该视图。如果用户未登录，Django 会自动将他们重定向到指定的登录页面。
# 37. 在这个类中，用户必须登录后才能访问 ProtectedView，否则会被重定向到指定的 login_url，即 /login/。


class ProtectedView(LoginRequiredMixin, View):
    # 38. 指定当用户未登录时，应该被重定向到的登录页面的 URL。在这个例子中，未登录用户会被重定向到 /login/。
    login_url = '/login/'
    # 39. 当用户未登录时，Django 会自动在 URL 中附加一个参数，用于指示用户登录成功后应该重定向的页面。
    redirect_field_name = 'redirect_to'

# 40. 这个方法定义了当用户通过 GET 请求访问此视图时的响应逻辑。
    def get(self, request):
        # 41. 该行代码表示渲染 registration/protected.html 模板文件，并将其返回给用户。
        return render(request, 'registration/protected.html')
