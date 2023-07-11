import openai
import time
from egorovsystem import Egorov

flag_initialized = True
try:
    openai_keys = Egorov["openai_keys"]

    org , keys = openai_keys.strip().split(" ")
    openai.organization = org
    openai.api_key = keys

except Exception:
    flag_initialized = False
    print( "YTools: openai initialize fail!" )


def post_chatgpt(messages, model):
    '''这个函数的目的是反复发送同一条信息直到成功发送。因为chatgpt小概率会随机报错。'''
    if not flag_initialized:
        return None
    fail_time = 0
    ret_msg = None
    while True:
        try:
            ret_msg = openai.ChatCompletion.create(
                model = model,
                messages = messages , 
            )
        except Exception:
            fail_time = fail_time + 1
            if fail_time < 10:
                time.sleep(1) # 休息一下
                continue 
            else:
                break
        break
    return ret_msg


def ask_chatgpt(prompt, model = "gpt-4"):
    '''跟chatgpt进行单次对话。'''
    ret_msg = post_chatgpt([{"role": "user", "content": prompt}], model)
    if ret_msg is None:
        return None
    ret = ret_msg ["choices"][0]["message"]["content"] #type: ignore
    return ret



