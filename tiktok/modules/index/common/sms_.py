import json

import random
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


# 生成验证码
def _gen_code():
    return str(random.randint(10000, 99999))


# 发送验证码
def _send_sms(phone, code):
    client = AcsClient('LTAI4Fq9XBoAHmBvmsoPd1A2', 'ImqUMrh7fxHvcK6nRuaLggo4IpYgAJ', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "聚炯抖商联盟")
    request.add_query_param('TemplateCode', "SMS_180062072")
    request.add_query_param('TemplateParam', json.dumps(dict(code=code)))

    client.do_action_with_exception(request)


def send_code(phone):
    # 生成code
    code = _gen_code()
    # 发送短信
    _send_sms(phone, code)
    return code

