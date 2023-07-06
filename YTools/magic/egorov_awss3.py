from egorovsystem import Egorov, get_variable
import boto3
from typing import Literal
from .awss3 import AWSS3

try: 
    key_id , key_sec , region , bucket = get_variable("aws_access").split(" ")
    awss3 = AWSS3(key_id, key_sec, region, bucket)
except RuntimeError:
    awss3 = None

def sets3(data, tar_path, format: Literal["binary" , "str" , "pickle"] = "pickle"):
    if awss3 is None:
        raise RuntimeWarning("no aws account found")
    
    return awss3.set(data, tar_path, format)

def gets3(tar_path, format: Literal["binary" , "str" , "pickle"] = "pickle"):
    if awss3 is None:
        raise RuntimeWarning("no aws account found")
    return awss3.get(tar_path, format)
