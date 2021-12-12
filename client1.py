import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


hostname = socket.gethostname()
BITS = 1024
HOST = '127.0.0.1' 
PORT = 55555


class Client:
    #Initializes everything
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname: ", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    #Grahics loop that constantly displays the GUI
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="grey")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="grey")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message", bg="grey")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    #Functionality of the send_button
    def write(self):
        message = str(self.nickname) + "-> " + self.input_area.get('1.0', 'end')
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    #Ending command to shut everything
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    #How to handle receiving 
    def receive(self):
        while self.running:
            try: 
                message = self.sock.recv(BITS).decode('utf-8')
                if message == 'Welcome': #Setting the nickname and sending to server
                    self.sock.send(self.nickname.encode('utf-8'))
                else: #All other messages after the nickname
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break

            except:
                print("Error")
                self.sock.close()
                break

#Initializes here
client = Client(HOST, PORT)