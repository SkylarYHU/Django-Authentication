from django import forms
# 3. 用于从 Django 框架的认证系统中导入 User 模型。这个模型用于表示应用程序中的用户账户，提供了用户注册、登录、登出、权限管理等功能。
from django.contrib.auth.models import User

# 4. 这个表单继承自 ModelForm，这使得它与 Django 的模型（在这里是 User 模型）相关联


class RegisterForm(forms.ModelForm):
    # 5. password 和 password_confirm 字段使用 PasswordInput 小部件，这样用户在输入密码时就会以掩码形式显示
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    # 6. 是 Django 表单和模型中的一个特殊类，用于定义与该表单或模型相关的元数据
    class Meta:
        model = User  # 表示这个表单将与Django的内置User模型关联。User 模型用于处理用户的认证和权限
        # 指定了在表单中要包含的字段列表。只有这些字段会被自动生成并包含在表单中。
        fields = ['username', 'password', 'password_confirm']

    # 6. clean 方法用于实现自定义的验证逻辑。它会检查两个密码字段的值是否匹配。如果不匹配，将引发一个 ValidationError
    def clean(self):
        # 调用父类的 clean（即 forms.ModelForm） 方法以获取已清理的数据
        cleaned_data = super().clean()
        # 从 cleaned_data 中获取 password 和 password_confirm
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            # 如果不匹配，抛出一个验证错误
            raise forms.ValidationError("Passwords do not match!")
        # 返回清理后的数据
        return cleaned_data
