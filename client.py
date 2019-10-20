'''
Created on Dec 21, 2011

@author: stas
'''
# Test
import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import decode_header
from email.header import Header
from email.parser import Parser
import poplib
import email
import string


class MainWindow:
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("email client")
        
        content = ttk.Frame(parent)
        content.grid(column=0, row=0, sticky=(N, W, E, S))
        
        label_server = ttk.Label(content, text="Server:")
        label_server.grid(column=1, row=1, sticky=N)
        self.server_addres = StringVar()
        server_addr = ttk.Entry(content, width=20, textvariable=self.server_addres)
        server_addr.grid(column=2, row=1, sticky=(W, E))
        server_addr.insert('1', 'pop3.mail.ru')
        
#        label_port = ttk.Label(content, text="Port:")
#        label_port.grid(column=1, row=1, sticky=N)
#        server_port = StringVar()
#        s_port = ttk.Entry(content, width=80, textvariable=server_addres)
#        s_port.grid(column=4, row=1, sticky=(W, E), columnspan=2)
#        s_port.insert('1', '110')
        
        label_user = ttk.Label(content, text="User:")
        label_user.grid(column=1, row=2, sticky=N)
        self.user = StringVar()
        in_user = ttk.Entry(content, width=20, textvariable=self.user)
        in_user.grid(column=2, row=2, sticky=(W, E))
        in_user.insert(1, "poos2011")
        
        label_pass = ttk.Label(content, text="Password:")
        label_pass.grid(column=3, row=2, sticky=N)
        self.password = StringVar()
        in_pass = ttk.Entry(content, width=20, textvariable=self.password)
        in_pass.grid(column=4, row=2, sticky=(W, E))
        in_pass.config(show="*")
        in_pass.insert(1, "gjjc2011")
        
        self.list_message = Listbox(content, height=20, width=80)
        self.list_message.grid(column=1, row=6, sticky=W, columnspan=4)
        
        get_head = ttk.Button(content, text="Get Message", command=self.get_headers)
        get_head.grid(column=4, row=1, sticky=E)
        
        see = ttk.Button(content, text="View", command=self.viewer)
        see.grid(column=1, row=7, sticky=W)
        
        delete_m = ttk.Button(content, text="Delete", command=self.delete_mes)
        delete_m.grid(column=2, row=7, sticky=W)
        
        send_m = ttk.Button(content, text="Send Message", command=self.send_mes)
        send_m.grid(column=3, row=7, sticky=W)
        
        open_message = ttk.Button(content, text="Open Message", command=self.open_mes)
        open_message.grid(column=4, row=7, sticky=W)
        
    def get_headers(self):
        self.list_message.delete(0, END)
        connect = poplib.POP3(self.server_addres.get())
        connect.getwelcome()
        connect.user(self.user.get())
        connect.pass_(self.password.get())
#        response, lst, octets = connect.list()
        numMessages = len(connect.list()[1])
        for i in range(numMessages):
            #print(i)
            response = connect.top(i+1,0)
            # return in format: (response, ['line', ...], octets)
            raw_message = response[1]
            message = email.message_from_bytes(b'\n'.join(raw_message))
            #print(str_message['to'])
            mes_to = message['to']
            mes_from = message['from']
            mes_subj = message['subject']
            headers,charset = decode_header(mes_subj)[0]
#            subject,charset = email.Header.decode_header(message["Subject"])[0]
#            Header()
            buf_str = "To: " + mes_to + " From: " + mes_from + " Subject: " + headers.decode(charset)
            self.list_message.insert(END, buf_str)
            #print(str_message)
        connect.quit()
        
    def viewer(self):
        form = view(self.parent, self.server_addres.get(), self.user.get(), self.password.get(), self.list_message.index(self.list_message.curselection()))
        
    def send_mes(self):
        form = send_message(self.parent)
        
    def open_mes(self):
#        print("123")
        f = filedialog.askopenfilename()
        form = open_mes(self.parent, f)
        
    def delete_mes(self):
        i = self.list_message.curselection()
        
        connect = poplib.POP3(self.server_addres.get())
        connect.getwelcome()
        connect.user(self.user.get())
        connect.pass_(self.password.get())
#        response, lst, octets = connect.list()
        numMessages = len(connect.list()[1])
        connect.dele(i)
        connect.quit()
        #self.get_header()
        
class view(tkinter.Toplevel):
        
    def __init__(self, parent, server, user, password, index):
        super(view, self).__init__(parent)
        self.parent = parent
        self.title("Message")
#        self.pas = password
        connect = poplib.POP3(server)
        connect.getwelcome()
        connect.user(user)
        connect.pass_(password)
#        response, lst, octets = connect.list()
        #numMessages = len(connect.list()[1])
        numMessages = len(connect.list()[1])
#        print(range(numMessages))
#        for i in range(numMessages):
#            for j in connect.retr(i+1)[1]:
#                print(j)
        #print(index[0])
        response = connect.retr(index+1)
        raw_message = response[1]
        self.new_message = b'\n'.join(raw_message)
        self.message = email.message_from_bytes(self.new_message)
        
        mes_to = self.message['to']
        mes_from = self.message['from']
        mes_subj = self.message['subject']
        headers,charset = decode_header(mes_subj)[0]
        mes_subj = headers.decode(charset)
#            subject,charset = email.Header.decode_header(message["Subject"])[0]
#            Header()
#        buf_str = "To: " + mes_to + " From: " + mes_from + " Subject: " + headers.decode(charset)
        content = ttk.Frame(self)
        content.grid(column=0, row=0, sticky=(N, W, E, S))
        
        label_from = ttk.Label(content, text="From: " + mes_from)
        label_from.grid(column=1, row=1, sticky=W)
        label_to = ttk.Label(content, text="To: " + mes_to)
        label_to.grid(column=1, row=2, sticky=W)
        label_subject = ttk.Label(content, text="Subject: " + mes_subj)
        label_subject.grid(column=1, row=3, sticky=W)
        
        mes_text = Text(content, width=80)
        mes_text.grid(column=1, row=4, sticky=(W,E), columnspan=3)
        #mes_text.insert(1, message)  Надо заполнить мессаге
        
        label_file = ttk.Label(content, text="File:")
        label_file.grid(column=1, row=5, sticky=W)
        self.list_file = Listbox(content, height=5, width=80)
        self.list_file.grid(column=1, row=6, sticky=W, columnspan=3)
        
        if not self.message.is_multipart():
            payload = self.message.get_payload(decode=True)
            charset = self.message.get_content_charset('iso-8859-1')
            text_mes = payload.decode(charset)
            mes_text.insert('1.0', text_mes)
        else:
            for s in self.message.walk():
                if s.get_content_type() == 'text/plain' :
                    payload = s.get_payload(decode=True)
                    charset = s.get_content_charset('iso-8859-1')
                    text_mes = payload.decode(charset)
                    mes_text.insert('1.0', text_mes)
                else:
                    filename = s.get_filename()
                    self.list_file.insert(END, filename)
        
        
        see = ttk.Button(content, text="Save File", command=self.file_save)
        see.grid(column=1, row=7, sticky=W)
        
        see = ttk.Button(content, text="Save Message", command=self.message_save)
        see.grid(column=2, row=7, sticky=W)
        
        see = ttk.Button(content, text="Exit", command=self.quit)
        see.grid(column=3, row=7, sticky=W)
        
        connect.quit()
        
    def file_save(self):
        filename = self.list_file.selection_get()
        #print(filename)
        for s in self.message.walk():
            file_n = s.get_filename()
            if file_n == filename:
                data = s.get_payload(decode=True)
                fi_ = filedialog.asksaveasfile(mode="wb")
                fi_.write(data)
                #print("TE")
        #print("FILE SAVE")
        
    def message_save(self):
        fi_ = filedialog.asksaveasfile(mode="wb")
        fi_.write(self.new_message)
        print("Message Save")
        
    def quit(self):
        print("EXIT")
        self.destroy()
        
class open_mes(tkinter.Toplevel):
        
    def __init__(self, parent, file_name):
        super(open_mes, self).__init__(parent)
        self.parent = parent
        self.title("Message")
        
#        print(file_name)
        f = open(file_name, "r")
        self.message = email.message_from_file(f)
        
        mes_to = self.message['to']
        mes_from = self.message['from']
        mes_subj = self.message['subject']
        headers,charset = decode_header(mes_subj)[0]
        mes_subj = headers.decode(charset)

        content = ttk.Frame(self)
        content.grid(column=0, row=0, sticky=(N, W, E, S))
        
        label_from = ttk.Label(content, text="From: " + mes_from)
        label_from.grid(column=1, row=1, sticky=W)
        label_to = ttk.Label(content, text="To: " + mes_to)
        label_to.grid(column=1, row=2, sticky=W)
        label_subject = ttk.Label(content, text="Subject: " + mes_subj)
        label_subject.grid(column=1, row=3, sticky=W)
        
        mes_text = Text(content, width=80)
        mes_text.grid(column=1, row=4, sticky=(W,E), columnspan=3)
        
        label_file = ttk.Label(content, text="File:")
        label_file.grid(column=1, row=5, sticky=W)
        self.list_file = Listbox(content, height=5, width=80)
        self.list_file.grid(column=1, row=6, sticky=W, columnspan=3)
        
        if not self.message.is_multipart():
            payload = self.message.get_payload(decode=True)
            charset = self.message.get_content_charset('iso-8859-1')
            text_mes = payload.decode(charset)
            mes_text.insert('1.0', text_mes)
        else:
            for s in self.message.walk():
                if s.get_content_type() == 'text/plain' :
                    payload = s.get_payload(decode=True)
                    charset = s.get_content_charset('iso-8859-1')
                    text_mes = payload.decode(charset)
                    mes_text.insert('1.0', text_mes)
                else:
                    filename = s.get_filename()
                    self.list_file.insert(END, filename)
        
        
        see = ttk.Button(content, text="Save File", command=self.file_save)
        see.grid(column=1, row=7, sticky=W)
        
        see = ttk.Button(content, text="Save Message", command=self.message_save)
        see.grid(column=2, row=7, sticky=W)
        
        see = ttk.Button(content, text="Exit", command=self.quit)
        see.grid(column=3, row=7, sticky=W)
        
    def file_save(self):
        filename = self.list_file.selection_get()
        #print(filename)
        for s in self.message.walk():
            file_n = s.get_filename()
            if file_n == filename:
                data = s.get_payload(decode=True)
                fi_ = filedialog.asksaveasfile(mode="wb")
                fi_.write(data)
                #print("TE")
        #print("FILE SAVE")
        
    def message_save(self):
        fi_ = filedialog.asksaveasfile(mode="wb")
        fi_.write(self.new_message)
        print("Message Save")
        
    def quit(self):
        print("EXIT")
        self.destroy()
        
        
class send_message(tkinter.Toplevel):
    
    def __init__(self, parent):
        super(send_message, self).__init__(parent)
        self.parent = parent
        self.title("Send")
        content = ttk.Frame(self)
        content.grid(column=0, row=0, sticky=(N, W, E, S))

        ## Input E-mail adress
        label_mail = ttk.Label(content, text="E-mail:")
        label_mail.grid(column=1, row=1, sticky=N)

        self.adress = StringVar()
        adr = ttk.Entry(content, width=80, textvariable=self.adress)
        adr.grid(column=2, row=1, sticky=(W, E), columnspan=2)
        adr.insert('1', 'litvss@gmail.com')

        ## Input Title
        label_title = ttk.Label(content, text="Title:")
        label_title.grid(column=1, row=2, sticky=N)

        self.title = StringVar()
        self.title = ttk.Entry(content, width=80, textvariable=self.title)
        self.title.grid(column=2, row=2, sticky=(W, E), columnspan=2)
        self.title.insert('1', 'TEST')

        ## Input Message
        label_message = ttk.Label(content, text="Message:")
        label_message.grid(column=1, row=3, sticky=N)

        self.message = Text(content, width=80)
        self.message.grid(column=1, row=4, sticky=(W,E), columnspan=3)
        #message.pack()
        self.message.insert('1.0', 'Message')

        ## Add File
        self.lbox = Listbox(content, height=5, width=100)
        self.lbox.grid(column=1, row=6, sticky=W, columnspan=3)

        ## FILE
        label_file = ttk.Label(content, text="File:")
        label_file.grid(column=1, row=5, sticky=W)
        ## Button
        add_file = ttk.Button(content, text="Add File", command=self.add_file)
        add_file.grid(column=2, row=11, sticky=E)

        delete_file = ttk.Button(content, text="Delete File", command=self.delete_file)
        delete_file.grid(column=3, row=11, sticky=W)

        send = ttk.Button(content, text="SEND", command=self.send)
        send.grid(column=1, row=11, sticky=W)
        
    def add_file(self):
        f = filedialog.askopenfilename()
        self.lbox.insert(0, f)
        print("Add_File")
    
    def delete_file(self):
        i = self.lbox.curselection()
        print(i)
        self.lbox.delete(i)
        print("Delete_File")
    
    def send(self):
        smtp = smtplib.SMTP()
        smtp.connect('smtp.mail.ru', 2525)
        smtp.login('poos2011@mail.ru', 'gjjc2011')    
        from_addr = "Stas Litvinenko <poos2011@mail.ru>"
        to_addr = self.adress.get()
        subj = self.title.get()
        message_text = self.message.get('1.0', 'end')
        #date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
        m=MIMEMultipart()
        m["to"]=to_addr
        m["from"]=from_addr
        m["subject"]=Header(subj, 'utf-8')
        ##m.add_header("subject", MIMEText(subj, 'plain', 'utf-8'))
        i = 0
        #    m2 = MIMEApplication()
        print(self.lbox.size())
        while i < self.lbox.size():
            path = self.lbox.get(i)
            (dirname, filename) = os.path.split(path)
            print(filename)
            fp = open(path, 'rb')
            m2 = MIMEApplication(fp.read())
            m2.add_header('Content-Disposition', 'attachment', filename=filename)
            m.attach(m2)
            fp.close()
            i += 1
    
        m.attach(MIMEText(message_text, 'plain', 'utf-8'))    
        smtp.sendmail(from_addr, to_addr, m.as_string())
        smtp.quit()

application = tkinter.Tk()
window = MainWindow(application)
application.mainloop()
