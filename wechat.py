import itchat,time,threading,sys,os
from itchat.content import *

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


@itchat.msg_register([TEXT])
def Personal_reply(msg):
    date='\n---------------'+str(time.strftime('%Y/%m/%d  %H:%M:%S',time.localtime(time.time())))+'---------------'    #获取时间
    rst=msg['User']['RemarkName']+":"    #消息來源
    if msg['Type'] == 'Text':
        print(date+'\n'+rst+msg['Text'])
        #history
        mesg=str(rst+msg['Text'])
        with open('Personal-log','a') as f:
            f.write(date+'\n')
            f.write(mesg+'\n')

@itchat.msg_register([TEXT], isGroupChat=True)
def Group_reply(msg):     
    G_date='\n---------------'+str(time.strftime('%Y/%m/%d  %H:%M:%S',time.localtime(time.time())))+'---------------'    #获取时间
    G_rst=msg['User']['NickName']+"(\'"+msg['ActualNickName']+"\'):"    #消息來源
    if msg['Type'] == 'Text':
        G_Text=msg['Text']    
        print(G_date+'\n'+G_rst+G_Text)
        #history
        mesg=str(G_rst+msg['Text'])
        with open('Group-log','a') as f:
            f.write(G_date+'\n')
            f.write(mesg+'\n')

    

itchat.auto_login(enableCmdQR=2,hotReload=True)
threading.Thread(target=send_mess).start()
itchat.run()
