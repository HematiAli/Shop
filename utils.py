from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('Your APIKey')
        params = { 'sender' : '2000660110', 'receptor': phone_number, 'message' :f'your code : {code}' }
        response = api.sms_send(params)
    except Exception as e:
        print(e)

"""
pip install -i https://mirror-pypi.runflare.com/simple
"""


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
    
    

"""
celery beat => برای تسک های دوره ای مثلا بگی هر دقیقه  این کار رو انجام بده
read => supervisor and celery demonization
"""
