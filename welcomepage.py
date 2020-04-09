import cx_Oracle as Cx
from tkinter import *
from adminhomepage import *
from studenthomepage import *
import  RatingFetcherFromCodeforces

def doRegistration(root, sid, name, pwd, vj, cf):
    print(sid, name, pwd, vj, cf)
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select userid from user_info where userid= \'' + sid + '\''
    cur.execute(stmt)
    rs = cur.fetchall()
    new = Tk()
    new.geometry('600x400')
    root.resizable(FALSE, FALSE)
    if len(rs) == 0:
        Label(new, text='Adding to database').place(x=80, y=50)
        stmt = 'insert into pending_req values(\'' + sid + '\',\'' + name + '\',\'' + pwd + '\',\'' + vj + '\',\'' + cf + '\')'
        print(stmt)
        rating = RatingFetcherFromCodeforces.cfRating(cf)
        if rating == -1:
            Label(new, text='Provide CF Rating Properly').place(x=80, y=50)
            startpage(root)
        else:
            try:
                cur.execute(stmt)
            except Cx.IntegrityError:
                Label(new, text='You already have a request pending, ask admin to solve it').place(x=80, y=50)
                startpage(root)
            else:
                conn.commit()
                Label(new, text='Request Added, Wait for Approval').place(x=80, y=50)
                startpage(root)
    else:
        Label(new, text='Student ID is already registered').place(x=80, y=50)


def login(root, sid, pwd):
    conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
    cur = conn.cursor()
    stmt = 'select password,adminaccess from user_info where userid = \'' + sid + '\''
    cur.execute(stmt)
    rs = cur.fetchall()
    new = Tk()
    new.geometry('800x400')
    root.resizable(FALSE, FALSE)
    if len(rs) != 0:
        if rs[0][0] == pwd:
            Label(new, text='Logged In').place(x=80, y=50)
            if rs[0][1]==1:
                adminWelcomePage(root)
            else:
                studentWelcomePage(root,sid)

        else:
            Label(new, text='Weong Password').place(x=80, y=50)
            startpage(root)
    else:
        stmt = 'select password from pending_req where userid = \'' + sid + '\''
        cur.execute(stmt)
        rs = cur.fetchall()
        if len(rs) != 0:
            Label(new, text='Your account needs approval, ask your admin').place(x=80, y=50)
            startpage(root)
        else:
            Label(new, text='You are not registered, register first').place(x=80, y=50)
            startpage(root)
    new.mainloop()


def registration(root):
    root.destroy()
    root = Tk()
    root.geometry('500x500')
    root.resizable(FALSE, FALSE)
    root.title("Registration Form")
    label_0 = Label(root, text="Registration form", width=20, font=("bold", 20))
    label_0.place(x=90, y=53)
    label_1 = Label(root, text="Student ID", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    entry_1 = Entry(root)
    entry_1.place(x=240, y=130)
    label_2 = Label(root, text="Name", width=20, font=("bold", 10))
    label_2.place(x=68, y=180)
    entry_2 = Entry(root)
    entry_2.place(x=240, y=180)
    label_3 = Label(root, text="Password", width=20, font=("bold", 10))
    label_3.place(x=68, y=230)
    entry_3 = Entry(root, show='*')
    entry_3.place(x=240, y=230)
    label_4 = Label(root, text="Vjudge Handle", width=20, font=("bold", 10))
    label_4.place(x=68, y=280)
    entry_4 = Entry(root)
    entry_4.place(x=240, y=280)
    label_5 = Label(root, text="Codeforces Handle", width=20, font=("bold", 10))
    label_5.place(x=68, y=330)
    entry_5 = Entry(root)
    entry_5.place(x=240, y=330)

    Button(root, text='Submit', width=20, bg='brown', fg='white',
           command=lambda: doRegistration(root, entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(),
                                          entry_5.get())).place(x=120, y=380)
    Button(root, text='Go Back', width=20, bg='brown', fg='white', command=lambda: startpage(root)).place(x=280,
                                                                                                          y=380)

    root.mainloop()


# margin left 50%
# loginpage

def loginpage(root):
    root.destroy()
    root = Tk()
    root.geometry('500x500')
    root.resizable(FALSE, FALSE)
    root.title("Login Form")
    label_0 = Label(root, text="Login form", width=20, fg='Red', font=("bold", 20))
    label_0.place(x=90, y=53)
    label_1 = Label(root, text="Student ID", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    entry_1 = Entry(root)
    entry_1.place(x=240, y=130)
    label_2 = Label(root, text="Password", width=20, font=("bold", 10))
    label_2.place(x=80, y=180)
    entry_2 = Entry(root, show='*')
    entry_2.place(x=240, y=180)
    Button(root, text='Submit', width=20, bg='brown', fg='white',
           command=lambda: login(root, entry_1.get(), entry_2.get())).place(x=100, y=380)
    Button(root, text='Go Back', width=20, bg='brown', fg='white', command=lambda: startpage(root)).place(x=270, y=380)
    root.mainloop()


# welcome page
def startpage(root):
    root.destroy()
    root = Tk()
    root.title('welcome page')
    root.geometry('500x500')
    root.resizable(FALSE, FALSE)
    frame = Frame(root).place(x=500, y=500)
    Label(root, text="Welcome to IUTPC Rating System", font=("bold", 16)).place(x=80, y=120)
    Button(root, text='Register', width=20, bg='brown', fg='white', command=lambda: registration(root)).place(x=100, y=320)
    Button(root, text='Login', width=20, bg='brown', fg='white', command=lambda: loginpage(root)).place(
        x=280, y=320)
    root.mainloop()


# init welcome page
if __name__ == "__main__":
    root=Tk()
    startpage(root)

# registrationpage
