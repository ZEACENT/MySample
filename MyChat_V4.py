import socket
import sys
import threading
import tkinter.messagebox
import tkinter.scrolledtext

MSG_Line = 0.0


def addMSG(data, SendOrReceive):
    global MSG_Line
    data = SendOrReceive + ':' + data
    text.insert(16.0, data)
    with open('MsgHistory.txt', 'a') as f:
        f.writelines(data + '\n')
    text.insert(16.0, '\n')
    MSG_Line += 1.0
    if MSG_Line >= 15:
        text.delete(0.0, 16.0)
        MSG_Line = 0


def Find_His():
    his = tkinter.Tk()
    his.title('ChatHistory')
    his['height'] = 400
    his['width'] = 320
    text_his = tkinter.Text(his)
    text_his.place(x=10, y=30, width=300, height=200)
    with open('MsgHistory.txt', 'r') as f:
        lines = f.readlines()
    text_his.insert(16.0, lines)


def Exit():
    s.close()
    sys.exit()


def receive_thread():
    while True:
        data = s.recv(1024)
        data = data.decode()
        addMSG(data, 'Received')
        print('Received:', data)


def send():
    data = varSend.get()
    if data != '':
        varSend.set('')
        try:
            s.sendall(data.encode())
        except:
            print('Network error.')
        else:
            addMSG(data, 'Sended')
            print('Sended:', data)


def enter_click():
    while True:
        key = sys.stdin.read(1)
        if key == 's':
            send()


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('MyChat')
    root['height'] = 400
    root['width'] = 320
    labelReceive = tkinter.Label(root, text='Received',
                                 justify=tkinter.CENTER, width=320)
    labelReceive.place(x=0, y=5, width=320, height=20)
    text = tkinter.Text(root)
    text.place(x=10, y=30, width=300, height=200)
    labelSend = tkinter.Label(root, text='Sending',
                              justify=tkinter.CENTER, width=320)
    labelSend.place(x=0, y=240, width=320, height=20)
    varSend = tkinter.StringVar(value='')
    entrySend = tkinter.Entry(root, width=320,
                              textvariable=varSend)
    entrySend.place(x=10, y=270, width=320, height=40)
    buttonSend = tkinter.Button(root, text='Send',
                                width=100, command=send)
    buttonSend.place(x=50, y=340, width=60, height=20)
    buttonHis = tkinter.Button(root, text='History',
                               width=100, command=Find_His)
    buttonHis.place(x=130, y=340, width=60, height=20)
    buttonExit = tkinter.Button(root, text='Exit',
                                width=100, command=Exit)
    buttonExit.place(x=210, y=340, width=60, height=20)

    HOST = '172.16.50.28'
    PORT = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print('Server not found or not open')
        tkinter.messagebox.showerror(title='Error', message='No Service.')
        sys.exit()
    threadReceive = threading.Thread(target=receive_thread)
    threadReceive.start()
    threadKeyboard = threading.Thread(target=enter_click)
    threadKeyboard.start()
    root.mainloop()
