from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# class WithdrawMoney(forms.Form):    
#     amount = forms.IntegerField(max_value=10000000)
#     usdt_address = forms.CharField(max_length=200)  




class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'name':'username',
            'type':"text",
            'placeholder':'Mobile Number',
            'required': 'required'
        })

        self.fields["password1"].widget.attrs.update({
            'name':'password1',
            'type':"password",
            'placeholder':'Password',
            'required': 'required'
        })

        self.fields["password2"].widget.attrs.update({
            'name':'password2',
            'type':"password",
            'placeholder':'Confirm password',
            'required': 'required'
        })

        self.fields["introducer"].widget.attrs.update({
            'name':'q',
            'type':"text",
            'max_length': 10,
            'required': 'required',
            'hidden':'hidden'
        })

        self.fields["referrel_code"].widget.attrs.update({
            'name':'referrel_code',
            'type':"text",
            'max_length': 10,            
            'hidden':'hidden'
        })
    class Meta:
        model = CustomUser
        fields = ['username','password1','password2','introducer','referrel_code']