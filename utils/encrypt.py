import hmac
from . import ConfigData

def encryption(data):
    key = ConfigData.APP_CONFIG.GITSECRETKEY.encode('utf-8')
    obj = hmac.new(key, msg=data, digestmod='sha1')
    return obj.hexdigest()