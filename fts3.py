ip='127.0.0.1'
port=8000
size=10000000 #10mb
r_size=10001111

import socket,os,pickle


def get_name(path):
    name=[]
    for ch in path:
        if ch=='/':
            name=[]
        else:
            name.append(ch)
    return ''.join(name)



def sender(loc):

    d_name=get_name(loc)
    client.send(d_name.encode())
    ready=client.recv(1024).decode()
    if ready=='yes':
        finished=False
        finished_reading=False
        file_opened=False
        
        cont=os.listdir(loc)
        l=len(cont)
        it=0
        for c in cont:
            finished=False
            finished_reading=False
            file_opened=False
            it+=1
            while(not finished):
                if not file_opened:
                    print("file "+c+" created...")
                    f=open(loc+'/'+c,'rb')
                    file_opened=True
                    cab=['1'.encode(),c.encode()]
                    client.send(pickle.dumps(cab))
                elif not finished_reading:
                    print(c+" reading...")
                    content=f.read(size)
                    if len(content)==0:
                        print(c+" finished reading...")
                        finished_reading=True
                    else:
                        cab=['2'.encode(),content]
                        client.send(pickle.dumps(cab))
                elif file_opened==True and finished_reading==True:
                    finished=True
                    f.close()
                    cab=['3'.encode(),'close file'.encode()]
                    client.send(pickle.dumps(cab))

    if it==l:
        print('success')
    else:
        print('error')
    print ("finished server suicided")









                    
                    
                        
            
            




def rec(home):
    mk=client.recv(1024).decode()
    os.chdir(home)
    os.mkdir(mk)
    os.chdir(home+'/'+mk) #dir recreated succesfully, awaiting file name
    home=home+'/'+mk
    client.send('yes'.encode())



    ##action begins here
    cab=pickle.loads(client.recv(r_size))
    if cab:
        proc=True
    else:
        proc=False
        return 1
    prot=cab[0].decode()
    while(proc):
        if prot=='1':
            fname=cab[1].decode()
            f=open(home+'/'+fname,'wb')
        elif prot=='2':
            print("writing to "+fname)
            f.write(cab[1])
        elif prot=='3':
            print("closing "+fname)
            f.close()
        elif prot=='4':
            proc=False
            print("end reached...")
        try:
            cab=pickle.loads(client.recv(r_size))
            prot=cab[0].decode()
        except:   
            prot='3'
    
        
        






        




if __name__=='__main__':
    ready='no'
    reading_file=False
    file_opened=False
    file_closed=False
    finished=False
    finished_reading=False
    mode=input("enter 1 for server mode, 2 for client mode")
    if mode=='1':
        print('''
                 |=============|                 
                 | server mode |
                 |             |
                 |   (.)__(.)  |
                 |      \/     |
                 |     ****    |
                 |             |
                 |=============|

                 ''')
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SERVER SOCKET
        host=socket.gethostbyname('0.0.0.0')
        server.bind((host,port))
        server.listen(2)
        print("server socket made...awaiting clients")
        (client,ad)=server.accept()
        print("client connected...")
        loc=input("Enter abs location of the file to send: ")
        sender(loc)
    elif mode=='2':
        print('''
                 |=============|                 
                 |reciever mode|
                 |             |
                 |   (.)__(.)  |
                 |      \/     |
                 |     ****    |
                 |             |
                 |=============|

                 ''')
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((ip,port))
        print("connected to server!!!")
        home=input("Enter the abs location to save files")
        rec(home)
        

                
            
    
    
                
                
                    
                
            
