# 引入相关模块
import socket
import select
import time
import os
import threading
import sys
import platform

max_thread = 70     # 并发最大线程数
timeout = 2         # 等待时间
socket.setdefaulttimeout(timeout)
# 设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。
# 代表经过timeout秒后，如果还未下载成功，自动跳入下一次操作，此次下载失败。
sleep_time = 0.001      #推迟调用线程的运行，单位是秒



#输出心形
def xin():
    print('\n'.join([''.join([('--www.WENOIF.COM'[(x-y)%16]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))


#调用系统清屏函数
def clear():
    sysy = platform.system()
    if sysy == "Windows":
        os.system('cls')
    elif sysy == "Linux":
        os.system('clear')
        

# 读取域名后缀列表
def get_top_level_domain_name_suffix():
    top_level_domain_name_suffix_list = list()
    #创建一个叫top_level_domain_name_suffix_list的列表，列表类似于数组，用于储存一串信息，从0开始计数
    with open('top_level_domain_name_suffix','r') as f:
        for line in f:
            if not line.startswith('//'):
            # startswith() 方法用于检查字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False。
            # 如果不是以'//'开头则追加到列表
                top_level_domain_name_suffix_list.append(line)
    return top_level_domain_name_suffix_list

# 判断检测
def whois_query(domain_name, domain_name_server, domain_name_whois_server):
# 域名信息，域名后缀，whois服务器
    retry = 3
    #重复相应连接次数
    domain = domain_name + '.' + domain_name_server
    # 重组 域名.域名后缀
    infomation = ''
    while(not infomation and retry > 0):
    # 如果info为空且retry剩余尝试连接次数大于0
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((domain_name_whois_server, 43))
            # 主动初始化TCP服务器连接，。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
            
            s.send(f'{domain} \r\n'.encode())
            # 发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。
            # encode() 方法以 encoding 指定的编码格式编码字符串。errors参数可以指定不同的错误处理方案。
            
            while True:   
                res = s.recv(1024)  
                # 接收TCP数据，数据以字符串形式返回，1024指定要接收的最大数据量。
                if not len(res):  
                    break    
                infomation += str(res)
            s.close()
            
            retry -= 1
            time.sleep(sleep_time)
        except:
            pass
    return infomation
    


# 输出结果写入文件
def get_reginfomation(domain_name, domain_name_suffix_infomation):
    infomation = whois_query(domain_name, domain_name_suffix_infomation[0], domain_name_suffix_infomation[1])
    # 调用“whois_query” 获得返回
    
    reg = domain_name_suffix_infomation[2]
#判断有没有返回信息
    if not infomation:
        with open(f'failure.txt','a') as f:
            f.write(f'{domain_name}.{domain_name_suffix_infomation[0]} 查询失败\n')
        print(f'域名{domain_name}.{domain_name_suffix_infomation[0]}查询失败！')
        return
#判断返回信息包不包含没注册的标志
    if infomation.find(reg) >= 0:
    # Python find() 方法检测字符串中是否包含子字符串 str ，
    #如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果包含子字符串返回开始的索引值，否则返回-1
        with open(f'success.txt','a') as f:
            f.write(f'{domain_name}.{domain_name_suffix_infomation[0]}\n')
        print(f'域名{domain_name}.{domain_name_suffix_infomation[0]} 未注册，已保存在本程序同目录下的"success.txt"文件中')
    else:
        print(f'域名{domain_name}.{domain_name_suffix_infomation[0]} 已注册')



#指定“后缀”和“字典”检测能否注册
def specify_suffix_and_dictionary():
    domain_name_suffix = input("输入域名后缀(如:com,cn)____:")
    domain_dictionary = input("输入字典名(如:demo.txt)____:")
    domain_name_length = int(input("输入过滤长度(如:7)____:"))
    
    domain_name_list = []
    with open(domain_dictionary,'r') as f:
       for line in f:
            if line:
                if (len(line) < domain_name_length):
                    domain_name_list.append(line.strip())
   
    top_level_domain_name_suffix_list = get_top_level_domain_name_suffix()[1:]
    top_level_domain_name_suffix_array = [x.split('=')[0] for x in top_level_domain_name_suffix_list]

    if domain_name_suffix not in top_level_domain_name_suffix_array:
        print(f'域名后缀 {domain_name_suffix} 不在top_level_domain_name_suffix中')
        
    top_level_domain_name_suffix_index = top_level_domain_name_suffix_array.index(domain_name_suffix)
    top_level_domain_name_par_list = [x.split('=')[:-1] for x in top_level_domain_name_suffix_list]
    
    for domain_name in domain_name_list:
        while threading.active_count() > max_thread:
            pass
        t = threading.Thread(target=get_reginfomation, args=(domain_name,top_level_domain_name_par_list[top_level_domain_name_suffix_index],))
        t.start()
        time.sleep(sleep_time)
    
#指定”域名“检测”所有后缀“能否注册
def specify_the_domain_name():
    domain_name = input("输入想要的域名(如wenoif.com只输入wenoif)____:")
    top_level_domain_name_suffix_list = get_top_level_domain_name_suffix()
    top_level_domain_name_suffix_array = [x.split('=')[:-1] for x in top_level_domain_name_suffix_list][1:]
     # split() 通过指定分隔符对字符串进行切片
    # x.split('=')表示：以"="为分隔符进行切片
    # [:-1]表示：直到倒数第一个即最后一个
    # for x in tld_list表示：在 tld_list 中进行切片，切片之后类似于多维数组
    # [1:]表示：切片后从第二个(下标为1)开始放入top_level_domain_name_suffix_array中（第一个是作者信息）
    for domain_name_suffix in top_level_domain_name_suffix_array:
        while threading.active_count() > max_thread:
        # 返回当前活跃的Thread对象数量   直到大于指定的线程数量
            pass
        t = threading.Thread(target=get_reginfomation, args=(domain_name,domain_name_suffix,))
        # Python Thread类表示在单独的控制线程中运行的活动。给构造函数传递回调对象
        t.start()
        # 开始，休息
        time.sleep(sleep_time)

# 指定”字典“检测”所有后缀“能否注册
def specify_a_dictionary():
    domain_dictionary = input("输入字典名(如:demo.txt)____:")
    domain_name_length = int(input("输入过滤长度(如:7)____:"))
    
    domain_dictionary_list = []
    with open(domain_dictionary,'r') as f:
       for line in f:
            if line:
                if (len(line) < domain_name_length):
                    domain_dictionary_list.append(line.strip())
                    #strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
                    #append() 方法用于在列表末尾添加新的对象
                    #追加到name_list列表

    top_level_domain_name_suffix_list = get_top_level_domain_name_suffix()
    top_level_domain_name_suffix_array = [x.split('=')[:-1] for x in top_level_domain_name_suffix_list][1:]

    for domain_name_suffix in top_level_domain_name_suffix_array:
        for domain_name in domain_dictionary_list:
            while threading.active_count() > max_thread:
                pass
            t = threading.Thread(target=get_reginfomation, args=(domain_name,domain_name_suffix,))
            t.start()
            time.sleep(sleep_time)    
    
# 退出函数  
def exit():
    print(  22 * '-' + '再见' + 22 * '-' + '\n\n' 
            + '感谢您的使用，技术能力有限，功能尚不完善，还请多多包涵。\n' 
            + '我有一个梦想，只是有一个梦想。你还有梦想吗，是否只是个梦想？\n'
            + """望君牢记：
        我们
        没有如果
        我的网站是 WeNoIf.COM
        """
            + '欢迎随时来撩，我们没有如果：WeNoIf.COM\n'
            + '\n' + 22 * '-' + '------' + 22 * '-'
        )

# 欢迎函数
def welcome():
    clear()
    xin()
    print(4 * '=' + '关于' + 4 * '=' +  '获取帮助:http://wenoif.com/44'+ 8 * '=' 
            + '\n\n你好，这是一个可以快速检验域名是否被注册，支持扫描超过200个顶级域名的域名工具。\n' 
            + '参考于Github上的"Har-Kuun/DomainMegaBot"和"luodaoyi/DomainScan"项目,感谢前辈的付出。\n'
            + '程序查询过程中，会将未注册的域名保存到程序同级目录中的"success.txt"文件中。\n'
            + '用户可以将自己想要查找的域名(不带后缀)写入同目录中的”demo.txt“文件中，每行一个。\n'
        )
        
    print(4 * '=' + '菜单' + 4 * '=' +  '获取帮助:http://wenoif.com/44'+ 8 * '=' 
            + '\n\n'
            + '1.指定”域名“检测”所有后缀“能否注册\n'
            + '2.指定”字典“检测”所有后缀“能否注册\n'
            + '3.指定“后缀”和“字典”检测能否注册\n'
            
            + '---------------------结束程序请输序号：0' + '\n'
            + '---------------------请输入你选择的序号：' , end=""
        )
        
    select = input()
    return select

    

# 主函数
if __name__ == '__main__':
    select = welcome()
    # 接受welcone函数返回的用户选项
    if (select == "0"):
    # if 判断函数，如果选项为0则执行以下【if后面的括号可有可无】
        clear()
        exit()
    elif (select == "1"):
        clear()
        specify_the_domain_name()
    elif (select == "2"):
        clear()
        specify_a_dictionary()
    elif select == "3":
    # else if 否则，如果选项为1则执行以下【if后面的括号可有可无】
        clear()
        specify_suffix_and_dictionary()   
    else:
    #如果到最后都不符合，则执行以下【print中可以使用单/双/三 引号】
        clear()
        print("\n输入错误 程序结束，仍需使用请重新运行。\n ")
        exit()
    