
from pycloud.netdisk import NetDisk
from pycloud.util import gnr_path
from tqdm import tqdm


nd = NetDisk(mode='slow')
nd.login_with_cookie()

items = [
    ('https://pan.baidu.com/s/1NxtrD9QbONy0xRxqXut5Bw', '8irj'),
    ('https://pan.baidu.com/s/1YJw9auKFnKMSeJaYb1PJTg', 'mqxz'),
    ('https://pan.baidu.com/s/17YYdXFyHjVAvbka0J2BFug', 'f8aa'),
    ('https://pan.baidu.com/s/1010Vnz9YZq6ygcsawKqiPw', 'fw38'),
    ('https://pan.baidu.com/s/1T4Chc6h14NOWLPSQI7VVQw', '7tuk'),
    ('https://pan.baidu.com/s/1tvDg7beobRmmFgtLP0zgXQ', 'a9z2'),
    ('https://pan.baidu.com/s/11-cMUa52HGoP_B13yDKhCw', 'p7da'),
]

for url, pwd in tqdm(items):
    nd.save(url=url, pwd=pwd, save_path=gnr_path(), verbose=False)

