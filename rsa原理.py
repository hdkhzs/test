import random
import sys


def gcd(a, b):
    if(a < b):
        t = a
        a = b
        b = t
    if(a % b == 0):
        return b
    else:
        return gcd(a % b, b)

def mod(base, exponent, factor, divisor):
    '''
    求模base的exponent次方乘于factor模divisor的结果
    '''
    i = 1
    num = base
    while(i < exponent and num < divisor):
        num *= base
        i += 1
        
    if(i == exponent):
        return (num * factor) % divisor
    else:
        integer = exponent // i  #将base的exponent次方表示成base的i次方的interger次方再乘于base的remainder次方
        remainder = exponent % i
        new_base = num % divisor    #base的i次方模divisor结果为new_base,base的i次方的interger次方与new_base的interger次方模divisor同余
        factor *= pow(base, remainder)
        return mod(new_base, integer, factor, divisor)
        

if __name__ == '__main__':
    p = 0x00fcf6b478f383979b533573421c4f288d7b62ea57294f13d927e2408ff3007948ef5d27fc69260acacd3461518385c563d6f5abf23a8f84b754bca7835f5f8e140c753fdb3c8d79210edf7ccf5d20f218c56d8f6fc41448a2de5963301adb6e9d2a6f724fdc35d50af46309f0b5c41782cbadb10ac859bc2888b30b638c31b4a9
    #质数p
    q = 0x00d8067dce17990476449068ed1608ad215359702657e9639c54e279cf4105ce82c45b2243d67aab407a4a6a98fbe908976c355130efe86f3f92badec98ccb17c9701d4342e50742489a26c6b8b1a10aa9c81e27f345ba624fb0bf3c0b83396cc208e7a1b7820a93760a4108059047dae51f7248f53f26d9d1b0d286379404d6c9
    #质数q
    n = p * q
    r = (p - 1) * (q - 1)
    #r为欧拉函数
    e = 0x010001
    #e < r 且 gcd(e, r) = 1 公钥为(n, e)
    d = 0x008a2e4f61bb151ea30d3810cda77021fd76006c3b420b5700dc49feec60f5f0dde6afb728a088f7d99f918e2175cd486fad1198b6f0c6f1ee9615de236fe4779f6c9251e933314539a00e206a77be9ec7ecb43986c115aa06a17efca8ba849ea63689b2a07c69171330c898d48257165e858745ba4d3383e7e38e8317718b9b487ae5ca1ebd8a591386e6e3534efeb656a1cdc8145d24cba3951c03844c03dbc3323018afb83b29903f8f55041aa64e324a3ae0b8c7d0bfa0e39bfb0a5edfc37b6e4407be8bd9ec3594c5f9970ee40d5d516fdf9422b3741984473e9b81a95a2d21cb96ef0efb33adc473ef724bf67e66ad711fd653fb94785e113cefed491601
    #ed %r = 1 私钥为(n, d)
    sys.setrecursionlimit(e)

    client_plaintext = random.randint(1, n - 1)   #客户端明文，明文不得大于n
    client_ciphertext = mod(client_plaintext, e, 1, n)  #客户端密文
    server_decode = mod(client_ciphertext, d, 1, n) #服务器解密

    if(client_plaintext == server_decode):
        print('client_plaintext == server_decode')
        print('client_plaintext = %d' %(client_plaintext))
        print('server_decode = %d' %(server_decode))        
    else:
        print('client_plaintext != server_decode')

    server_plaintext = random.randint(1, n - 1)   #服务器明文
    server_ciphertext = mod(server_plaintext, d, 1, n)  #服务器密文
    client_decode = mod(server_ciphertext, e, 1, n) #客户端解密

    if(server_plaintext == client_decode):
        print('server_plaintext == client_decode')
        print('server_plaintext = %d' %(server_plaintext))
        print('client_decode = %d' %(client_decode))        
    else:
        print('server_plaintext != client_decode')

    third_plaintext = random.randint(1, n - 1)   #第三方伪造的明文
    third_ciphertext = mod(third_plaintext, e, 1, n)    #第三方通过公钥加密的密文
    client_decode = mod(third_ciphertext, e, 1, n) #客户端通过公钥解密第三方伪造的密文

    if(third_plaintext == client_decode):
        print('third_plaintext == client_decode')        
    else:
        print('third_plaintext != client_decode')
        print('third_plaintext = %d' %(third_plaintext))
        print('client_decode = %d' %(client_decode))

    client_plaintext = random.randint(1, p - 1) * q    #当客户端的明文是q的倍数时
    client_ciphertext = mod(client_plaintext, e, 1, n)
    server_decode = mod(client_ciphertext, d, 1, n)

    if(client_plaintext == server_decode):
        print('client_plaintext == server_decode')
        print('client_plaintext = %d' %(client_plaintext))
        print('server_decode = %d' %(server_decode))
    else:
        print('client_plaintext != server_decode')

    third_plaintext = random.randint(1, p - 1) * q #当第三方伪造的明文是q的倍数时
    third_ciphertext = mod(third_plaintext, e, 1, n)
    client_decode = mod(client_ciphertext, e, 1, n)

    if(third_plaintext == client_decode):
        print('third_plaintext == client_decode')
    else:
        print('third_plaintext != client_decode')
        print('third_plaintext = %d' %(third_plaintext))
        print('client_decode = %d' %(client_decode))

    server_plaintext = random.randint(1, p - 1) * q    #当服务端的明文是q的倍数时
    server_ciphertext = mod(server_plaintext, d, 1, n)
    client_decode = mod(server_ciphertext, e, 1, n)

    if(server_plaintext == client_decode):
        print('server_plaintext == client_decode')
        print('server_plaintext = %d' %(server_plaintext))
        print('client_decode = %d' %(client_decode))        
    else:
        print('server_plaintext != client_decode')

    client_plaintext = random.randint(1, n) #相同的明文客户端加密后大概率和服务端加密后的密文不同
    server_palintext = client_plaintext
    client_ciphertext = mod(client_plaintext, e, 1, n)
    server_ciphertext = mod(server_plaintext, d, 1, n)

    if(client_ciphertext == server_ciphertext):
        print('client_ciphertext == server_ciphertext')        
    else:
        print('client_ciphertext != server_ciphertext')
        print('client_ciphertext = %d' %(client_ciphertext))
        print('server_ciphertext = %d' %(server_ciphertext))
    
        #备注
