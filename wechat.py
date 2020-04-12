import itchat,time,threading,sys,os,platform
from itchat.content import *

def mkdir():
    folder=['Picture','Attachment','Video','Recording']
    for i in folder:
        if not os.path.exists(i):
            os.mkdir(i)
def touch_html():
    html_text="""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%s</title>
</head>
<body>
  
</body>
</html>"""
    file=['Personal-log.html','Group-log.html']
    for i in file:
        if os.path.isfile(i):
            continue
        else:
            with open(i,'w') as f:
                f.write(html_text%i)

def write_html(filename,code):
    with open(filename,'r',encoding='utf-8') as f:
        lines = []
        for line in f: 
            lines.append(line)
        lines.insert(-2, '%s\n'%code) # 在倒数第二行插入
        s = ''.join(lines)
    with open(filename,'w',encoding='utf-8') as f:
        f.write(s)

def send_mess():
    time.sleep(1)
    while True:
        choose=input('Please enter content>')
        if choose == '1':
            num=1
            for i in itchat.get_friends(update=True):
                if i['RemarkName'] == "":
                    print(str(num)+"、"+i['NickName']+" (未备注)")
                    num+=1
                    continue
                print(str(num)+"、"+i['RemarkName'])
                num+=1
            continue
        elif choose == '2':
            num=1
            for i in itchat.get_chatrooms(update=True):
                print(str(num)+"、"+i['NickName'])
                num+=1
            continue
        elif choose == '3':
            send_mess_personal(False)
            continue
        elif choose == '4':
            send_mess_group(False)
            continue
        elif choose == '5':
            review()
            continue
        elif choose.lower() == 'help':
            print("輸入1查看所有联系人\n輸入2查看所有群聊\n輸入3进入个人聊天\n輸入4进入群組聊天\n輸入\'exit\'或\'quit\'退出聊天程序")
        elif choose.lower() == 'exit' or choose.lower() == 'quit':
            return itchat.logout,sys.exit()
        else:
            print("輸入help查看帮助")

def send_mess_personal(flag):
    while True:
        if flag == False:
            search_name=input('Please enter contact person:')
        else:
            pass
        if search_name == False:
            continue
        elif search_name == '1':
            num=1
            for i in itchat.get_friends(update=True):
                if i['RemarkName'] == "":
                    print(str(num)+"、"+i['NickName']+"(未备注)")
                    num+=1
                    continue
                print(str(num)+"、"+i['RemarkName'])
                num+=1
            continue
        elif search_name == '2':
            num=1
            for i in itchat.get_chatrooms(update=True):
                print(str(num)+"、"+i['NickName'])
                num+=1
            continue
        if search_name == '3':
            return send_mess_personal(False)
        elif search_name == '4':
            return send_mess_group(False)
        elif search_name.lower() == 'exit' or search_name.lower() == 'quit':
            return itchat.logout,sys.exit()
        elif search_name.lower() == 'back':
            break
        elif search_name.lower() == 'help':
            print("輸入1查看所有联系人\n輸入'exit'或'quit'退出聊天程序\n輸入'back'返回")
            continue
        contact_person=itchat.search_friends(name=search_name)
        if len(contact_person) == False:
            print("联系人不存在")
            continue
        to=contact_person[0]['UserName']
        Text=input('Please enter message:').lower()
        if Text.lower() == 'exit' or Text.lower() == 'quit':
            return itchat.logout,sys.exit()
        elif Text.lower() == 'back':
            flag=False
            continue
        else:
            itchat.send(Text,toUserName=to)
            flag=True

def send_mess_group(flag):
    while True:
        if flag == False:
            search_group=input("Please enter group name >")
        else:
            pass
        if search_group == False:
            continue
        elif search_group.lower() == 'help':
            print("輸入1查看所有群聊\n輸入'exit'或'quit'退出聊天程序\n輸入'back'返回")
            continue
        elif search_group.lower() == 'exit' or search_group.lower() == 'quit':
            return itchat.logout,sys.exit()
        elif search_group.lower() == 'back':
            break
        elif search_group == '1':
            num=1
            for i in itchat.get_friends(update=True):
                if i['RemarkName'] == "":
                    print(str(num)+"、"+i['NickName']+"(未备注)")
                    num+=1
                    continue
                print(str(num)+"、"+i['RemarkName'])
                num+=1
            continue
        elif search_group == '2':
            num=1
            for i in itchat.get_chatrooms(update=True):
                print(str(num)+"、"+i['NickName'])
                num+=1
            continue
        contact_group=itchat.search_chatrooms(name=search_group)
        if len(contact_group) == False:
            print("群聊不存在")
            continue
        to=contact_group[0]['UserName']
        Text=input('Please enter message:').lower()
        if Text.lower() == 'quit' or Text.lower() == 'exit':
            return itchat.logout,sys.exit()
        elif Text.lower() == 'back':
            flag = False
            continue
        else:
            itchat.send(Text,toUserName=to)
            flag=True

def mv_file(filename,file_dir):  #判断操作系统 移动文件到对应文件夹
    cmd = ((platform.system() == 'Windows') and 'move %s %s/'%(filename,file_dir) or 'mv %s %s/'%(filename,file_dir))
    os.system(cmd)

@itchat.msg_register([TEXT,RECORDING,PICTURE,VIDEO])
def Personal_reply(msg):
    date='---------------'+str(time.strftime('%Y/%m/%d  %H:%M:%S',time.localtime(time.time())))+'---------------'    #获取时间
    rst=msg['User']['NickName']+": "    #消息来源
    mesg='<p>'+str(rst)+'</p>'
    if msg['Type'] == 'Text':
        print(date+'\n'+rst+msg['Text'])
        #history
        html_code = '<p>%s</p>\n%s\n%s\n'%(date,rst,Text)
        write_html('Group-log.html',html_code)
    elif msg['Type'] == 'Recording':    #语音消息
        msg['Text'](msg['FileName'])
        mv_file(msg['FileName'],msg['Type'])
        code='<audio controls="controls" height="100" width="100"> \n\t <source src="Recording/%s" type="audio/mp3" /> \n\t <source src="Recording/%s" type="audio/ogg" /> \n <embed height="100" width="100" src="Recording/%s" /> \n </audio>' %(msg["FileName"],msg["FileName"],msg["FileName"])
        html_code='<p>%s</p>\n%s\n%s\n'%(date,mesg,code)
        write_html('Personal-log.html',html_code)
        print(date+'\n'+'收到一条语音消息: '+rst+msg['FileName'])
    elif msg['Type'] == 'Picture':   #圖片  
        msg['Text'](msg['FileName'])   #儲存文件
        mv_file(msg['FileName'],msg['Type'])
        code="<img width=\"25%\" height=\"25%\" src=\"Picture/"+msg['FileName']+"\">"
        html_code='<p>%s</p>\n%s\n%s\n'%(date,mesg,code)
        write_html('Personal-log.html',html_code)
        print(date+'\n'+'收到一张图片: '+rst+msg['FileName'])
    elif msg['Type'] == 'Video':
        msg['Text'](msg['FileName'])
        mv_file(msg['FileName'],msg['Type'])
        code='<video width="320" height="240" controls="controls"> \n\t <source src="Video/%s" type="video/mp4" /> \n\t <source src="Video/%s" type="video/ogg" /> \n\t <source src="Video/%s" type="video/webm" /> \n\t <object data="Video/%s" width="320" height="240"> \n\t\t <embed width="320" height="240" src="Video/%s" /> \n\t </object> \n </Video>' %(msg["FileName"],msg["FileName"],msg["FileName"],msg["FileName"],msg["FileName"])   #網站目錄
        html_code='<p>%s</p>\n%s\n%s\n'%(date,mesg,code)
        write_html('Personal-log.html',html_code)
        print(date+'\n'+'收到一段视频: '+rst+msg['FileName'])

@itchat.msg_register([TEXT,RECORDING,PICTURE,VIDEO], isGroupChat=True)
def Group_reply(msg):     
    date='---------------'+str(time.strftime('%Y/%m/%d  %H:%M:%S',time.localtime(time.time())))+'---------------'    #获取时间
    rst=msg['User']['NickName']+": "    #消息来源
    mesg='<p>'+str(rst)+'</p>'
    if msg['Type'] == 'Text':
        Text=msg['Text']    
        print(date+'\n'+rst+Text)
        #history
        html_code = '<p>%s</p>\n%s\n%s\n'%(date,rst,Text)
        write_html('Group-log.html',html_code)
    elif msg['Type'] == 'Recording':    #语音消息
        msg['Text'](msg['FileName'])
        mv_file(msg['FileName'],msg['Type'])
        code='<audio controls="controls" height="100" width="100"> \n\t <source src="Recording/%s" type="audio/mp3" /> \n\t <source src="Recording/%s" type="audio/ogg" /> \n <embed height="100" width="100" src="Recording/%s" /> \n </audio>' %(msg["FileName"],msg["FileName"],msg["FileName"])
        html_code='<p>%s</p>\n%s\n%s\n'%(date,mesg,code)
        write_html('Group-log.html',html_code)
        print(date+'\n'+'收到一条语音消息: '+rst+msg['FileName'])
    elif msg['Type'] == 'Picture':   #圖片
        msg['Text'](msg['FileName'])   #儲存文件
        mv_file(msg['FileName'],msg['Type'])
        code="<img width=\"25%\" height=\"25%\" src=\"Picture/"+msg['FileName']+"\">"
        html_code='<p>%s</p>\n%s\n%s\n'%(date,mesg,code)
        write_html('Personal-log.html',html_code)
        print(date+'\n'+'收到一张图片: '+rst+msg['FileName'])
    elif msg['Type'] == 'Video':
        msg['Text'](msg['FileName'])
        mv_file(msg['FileName'],msg['Type'])
        code='<video width="320" height="240" controls="controls"> \n\t <source src="Video/%s" type="video/mp4" /> \n\t <source src="Video/%s" type="video/ogg" /> \n\t <source src="Video/%s" type="video/webm" /> \n\t <object data="Video/%s" width="320" height="240"> \n\t\t <embed width="320" height="240" src="Video/%s" /> \n\t </object> \n </Video>' %(msg["FileName"],msg["FileName"],msg["FileName"],msg["FileName"],msg["FileName"])   #網站目錄
        html_code='<p>%s</p>\n%s\n%s\n'%(date,mesg,code)
        write_html('Group-log.html',html_code)
        print(date+'\n'+'收到一段视频: '+rst+msg['FileName'])
    
mkdir() 
touch_html()
itchat.auto_login(enableCmdQR=2,hotReload=True)
threading.Thread(target=send_mess).start()
itchat.run()
