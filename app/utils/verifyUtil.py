def verify_hook_token(x_token,local_token,payload):
    if x_token is None or local_token is None or len(x_token)<=0 or len(local_token)<=0:
        return False
    return x_token==local_token;


