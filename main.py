# This software is licensed under Custom License
# Redistribution allowed only with meaningful changes

import tkinter as tk
import paramiko as pk

class Window():
    def __init__(self):
        self.r = tk.Tk()
        self.r.geometry('850x650')
        self.r.title("mcsm")
        self.r.config(bg="#202020")

        self.titlelab = tk.Label(self.r, text="Minecraft Server Manager", fg='#efefef', bg='#202020', font=('',20))
        self.titlelab.pack(pady=10)
        self.authorlab = tk.Label(self.r, text='By Xenavia', bg="#202020", fg="#afafaf")
        self.authorlab.pack()

        # SSH CONNECTION
        self.sshf = tk.Frame(self.r, bg="#202020")
        self.sst = tk.Label(self.r, text="SSH section", fg='#efefef', bg='#202020', font=('',16))
        self.sst.pack(pady=5)
        self.hosten = tk.Entry(self.sshf, bg='#2f2f2f', fg='white')
        self.usen = tk.Entry(self.sshf, bg='#2f2f2f', fg='white')
        self.passn = tk.Entry(self.sshf, bg='#2f2f2f', fg='white')
        self.sshab = tk.Button(self.sshf, text="Apply", bg='#2f2f2f', fg='white', command=self.setssh)

        self.hosten.grid(row=0, column=0)
        self.usen.grid(row=0, column=1)
        self.passn.grid(row=0, column=2)
        self.sshab.grid(row=2, column=1)

        self.hosten.insert('0', "Host")
        self.usen.insert('0', "Username")
        self.passn.insert('0', "Password")

        self.sshf.pack()

        # TMUX SESSION
        self.tmuxf = tk.Frame(self.r, bg='#303030')
        self.tmuxt = tk.Label(self.r, text="TMUX section", fg='#efefef', bg='#202020', font=('', 16))
        self.tmuxt.pack(pady=7)
        self.tmen = tk.Entry(self.tmuxf, bg='#2f2f2f', fg='white', width=25)
        self.tmen.grid(row=1, column=1)
        self.tmen.insert('1', 'TMUX Session name')
        self.tscen = tk.Entry(self.tmuxf, bg='#2f2f2f', fg='white', width=25)
        self.tscen.grid(row=1, column=2)
        self.tscen.insert('1', 'Server Category')
        self.tsfen = tk.Entry(self.tmuxf, bg='#2f2f2f', fg='white', width=25)
        self.tsfen.grid(row=1, column=3)
        self.tsfen.insert('1', 'Server start file (./"NAME")')
        self.tab = tk.Button(self.tmuxf, text="Apply", bg='#2f2f2f', fg='white', command=lambda: self.tmuxpart(1))
        self.tab.grid(row=1, column=4)
        self.tcb = tk.Button(self.tmuxf, text="Create", bg='#2f2f2f', fg='white', command=lambda: self.tmuxpart(2))
        self.tcb.grid(row=1, column=5)
        self.tdb = tk.Button(self.tmuxf, text="Delete", bg='#2f2f2f', fg='white', command=lambda: self.tmuxpart(3))
        self.tdb.grid(row=1, column=6)
        self.tmuxf.pack()

        # COMMUNICATION WITH SERVER
        self.comf = tk.Frame(self.r, bg='#202020')
        self.comt = tk.Label(self.r, text="COMM section", fg='#efefef', bg='#202020', font=('', 16))
        self.comt.pack(pady=7)
        self.logbox = tk.Text(self.comf, width=80, height=15, bg='#2f2f2f', fg='white')
        self.logbox.grid(row=0, column=0)

        self.tcbf = tk.Frame(self.comf, bg='#202020')

        self.tcen = tk.Entry(self.tcbf, width=50, bg='#2f2f2f', fg='white')
        self.tcen.grid(row=1, column=0)
        self.tcapb = tk.Button(self.tcbf, text="Capture", bg='#2f2f2f', fg='white', command=lambda: self.tmuxpart(4))
        self.tcapb.grid(row=1, column=1)
        self.tsenb = tk.Button(self.tcbf, text="Send", bg='#2f2f2f', fg='white', command=lambda: self.tmuxpart(5))
        self.tsenb.grid(row=1, column=2)
        self.tsfsb = tk.Button(self.tcbf, text="Start", bg='#2f2f2f', fg='white', command=lambda: self.tmuxpart(6))
        self.tsfsb.grid(row=1, column=3)

        self.tcbf.grid(row=1,column=0)

        self.comf.pack()



        self.client = pk.SSHClient()
        self.client.set_missing_host_key_policy(pk.AutoAddPolicy())
        self.hostname = "0.0.0.0"
        self.username = "yeaterlol"
        self.password = "smellyfish"
        self.tsession = "server"
        self.servercat = "/home/yeaterlol/1201/"
        self.startfile = "./start"

    def sshlogic(self, dotask):
        def logic(command):
            try:
                self.client.connect(hostname=self.hostname, username=self.username, password=self.password)

                stdin, stdout, stderr = self.client.exec_command(command)
                output = stdout.read().decode()
                return output
            finally:
                self.client.close()
        return logic(dotask)

    def setssh(self):
        def returne():
            self.sshab.config(text='Apply')
        hostname = str(self.hosten.get())
        username = str(self.usen.get())
        password = str(self.passn.get())
        self.hostname = hostname
        self.username = username
        self.password = password
        self.sshab.config(text='Applied')
        self.r.after(1, returne)

    def tmuxpart(self, func):
        def apply():
            def returne():
                self.tab.config(text='Apply')
            tmuxsession = str(self.tmen.get())
            servercat = str(self.tscen.get())
            startfile = str(self.tsfen.get())
            self.servercat = servercat
            self.startfile = startfile
            self.tsession = tmuxsession
            self.sshlogic(f'tmux send-keys "cd {self.servercat}" C-m')
            self.tab.config(text='Applied')
            self.r.after(1, returne)

        def create():
            def returne():
                self.tcb.config(text='Create')
            tmuxsession = str(self.tmen.get())
            servercat = str(self.tscen.get())
            self.tsession = tmuxsession
            self.servercat = servercat
            self.sshlogic(f'tmux new -s {self.tsession} -d')
            self.sshlogic(f'tmux send-keys "cd {self.servercat}" C-m')
            self.tcb.config(text='Created')
            self.r.after(1, returne)

        def delete():
            def returne():
                self.tdb.config(text='Delete')
            tmuxsession = str(self.tmen.get())
            self.tsession = tmuxsession
            self.sshlogic(f'tmux kill-session -t {self.tsession}')
            self.tdb.config(text='Deleted')
            self.r.after(1, returne)

        def capture():
            def returne():
                self.tcapb.config(text='Capture')
            tmuxsession = str(self.tmen.get())
            self.tsession = tmuxsession
            output = self.sshlogic(f'tmux capture-pane -t {self.tsession} -p')
            self.tcapb.config(text='Captured')
            self.logbox.delete('1.0', tk.END)
            self.logbox.insert('1.0', output)
            self.logbox.see(tk.END)
            self.r.after(1, returne)


        def sendcom(commands):
            def returne():
                self.tsenb.config(text='Send')
            tmuxsession = str(self.tmen.get())
            self.tsession = tmuxsession
            self.sshlogic(f'tmux send-keys "{commands}" C-m')
            self.tsenb.config(text='Sent')
            self.r.after(100, returne)
            capture()

        def startser():
            def returne():
                self.tsfsb.config(text="Start")
            startfile = str(self.tsfen.get())
            self.startfile = startfile
            self.sshlogic(f'tmux send-keys "{self.startfile}" C-m')
            self.tsfsb.config(text="Started")
            self.r.after(100, returne)

        if func == 1:
            apply()
        elif func == 2:
            create()
        elif func == 3:
            delete()
        elif func == 4:
            capture()
        elif func == 5:
            command = str(self.tcen.get())
            sendcom(command)
        elif func == 6:
            startser()


if __name__ == "__main__":
    window = Window()
    # You may add here default ssh and tmux info:
    window.r.mainloop()