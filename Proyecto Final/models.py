from tkinter import *
from sqlalchemy import Column, Integer, String, and_
import db
from db import Base
from tkinter import messagebox, ttk
from snake_app import run_snake_game
import turtle


def delete_window(screen):
    close = messagebox.askyesno(
        message="Do you want to cancel?",
        title="Confirm"
    )
    if close:
        screen.destroy()
        open_admin()

def open_admin():
    admin = AdminScreen()

def _apply_row_colors(table):
    for index, row in enumerate(table.get_children()):
        if index % 2 == 0:
            table.item(row, tags=('even',))
        else:
            table.item(row, tags=('odd',))
    table.tag_configure('even', background='lightgrey')
    table.tag_configure('odd', background='white')


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False, default="Desconocido")
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, default="N/A")
    score = Column(Integer, default=0)

    def __init__(self, user, email, password):
        self.user = user
        self.email = email
        self.password = password

#--------------------ADD SCREEN------------------#
class AddScreen():
    def __init__(self):
        #--------------------SCREEN--------------------#
        self.screen = Tk()
        self.screen.protocol("WM_DELETE_WINDOW", self.close_window)

        self.screen.title("Snake Tournament")
        self.screen.wm_iconbitmap('resources/icon.ico')
        self.screen.resizable(0, 0)

        self.logo = Canvas(width=200, height=200)
        self.logo_img = PhotoImage(file="resources/logo.png")
        self.logo.create_image(100, 100, image=self.logo_img)
        self.logo.grid(row=0, column=1, pady=25)
        # --------------------ADD FRAME--------------------#
        self.frame_add = LabelFrame(self.screen, text="Add", font=("Comic Sans MS", 20, "bold"))
        self.frame_add.grid(row=1, column=0, columnspan=3, pady=25, padx=75, sticky=W + E)

        self.add_user_label = Label(self.frame_add, text="User:", font=("Comic Sans MS", 15))
        self.add_user_label.grid(row=2, column=0)
        self.add_user_entry = Entry(self.frame_add, font=("Comic Sans MS", 10))
        self.add_user_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        self.add_email_label = Label(self.frame_add, text="Email:", font=("Comic Sans MS", 15))
        self.add_email_label.grid(row=3, column=0)
        self.add_email_entry = Entry(self.frame_add, font=("Comic Sans MS", 10))
        self.add_email_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        self.add_password_label = Label(self.frame_add, text="Password:", font=("Comic Sans MS", 15))
        self.add_password_label.grid(row=4, column=0)
        self.add_password_entry = Entry(self.frame_add, font=("Comic Sans MS", 10))
        self.add_password_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        self.add_button = Button(self.frame_add, text="Add", command=self.add_user, font=("Comic Sans MS", 10, "bold"))
        self.add_button.grid(row=5, column=0,  padx=10, pady=10, sticky=W + E)
        self.cancel_button = Button(self.frame_add, text="Cancel", command=self.close_window, font=("Comic Sans MS", 10, "bold"))
        self.cancel_button.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky=W + E)

        self.screen.mainloop()

    def close_window(self):
        delete_window(self.screen)

    def add_user(self):
        user_info = self.add_user_entry.get().lower()
        email_info = self.add_email_entry.get().lower()
        password_info = self.add_password_entry.get().lower()
        if user_info != "" and email_info != "" and password_info != "":
            result_user = db.session.query(User).filter(User.user == user_info).first()
            result_email = db.session.query(User).filter(User.email == email_info).first()
            if result_user is None and result_email is None:
                correct_info = messagebox.askokcancel(title="Confirm Info",
                                                      message=f"Do you want to create this user?:\n"
                                                              f"User: {user_info}\n"
                                                              f"Email: {email_info}\n"
                                                              f"Password: {password_info}")
                if correct_info:
                    new_user = User(user=user_info, email=email_info, password=password_info)
                    db.session.add(new_user)
                    db.session.commit()
                    db.session.close()
                    self.add_user_entry.delete(0, END)
                    self.add_email_entry.delete(0, END)
                    self.add_password_entry.delete(0, END)
                    self.screen.destroy()
                    admin = AdminScreen()

                else:
                    pass
            elif result_user is not None and result_email is None:
                messagebox.showerror(title="Error", message="User already in use")
            elif result_email is not None and result_user is None:
                messagebox.showerror(title="Error", message="Email already in use")
            else:
                messagebox.showerror(title="Error", message="User and Email already in use")
        else:
            messagebox.showerror(title="Error", message="Missing Info")


#-------------------EDIT SCREEN---------------------#
class EditScreen():
    def __init__(self, player):
        self.player = player
        #--------------------SCREEN--------------------#
        self.screen = Tk()
        self.screen.protocol("WM_DELETE_WINDOW", self.close_window)
        self.screen.title("Snake Tournament")
        self.screen.wm_iconbitmap('resources/icon.ico')
        self.screen.resizable(0, 0)

        self.logo = Canvas(width=200, height=200)
        self.logo_img = PhotoImage(file="resources/logo.png")
        self.logo.create_image(100, 100, image=self.logo_img)
        self.logo.grid(row=0, column=1, pady=25)
        # --------------------EDIT FRAME--------------------#
        self.frame_edit = LabelFrame(self.screen, text="Edit", font=("Comic Sans MS", 20, "bold"))
        self.frame_edit.grid(row=1, column=0, columnspan=3, pady=25, padx=75, sticky=W + E)

        self.old_user_label = Label(self.frame_edit, text="Old User:", font=("Comic Sans MS", 15))
        self.old_user_label.grid(row=2, column=0)
        self.old_user_entry = Entry(self.frame_edit, font=("Comic Sans MS", 10))
        self.old_user_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        self.old_user_entry.insert(0, f"{self.player.user}")
        self.old_user_entry.config(state="readonly")
        self.new_user_label = Label(self.frame_edit, text="New User:", font=("Comic Sans MS", 15))
        self.new_user_label.grid(row=3, column=0)
        self.new_user_entry = Entry(self.frame_edit, font=("Comic Sans MS", 10))
        self.new_user_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        self.old_email_label = Label(self.frame_edit, text="Old Email:", font=("Comic Sans MS", 15))
        self.old_email_label.grid(row=4, column=0)
        self.old_email_entry = Entry(self.frame_edit, font=("Comic Sans MS", 10))
        self.old_email_entry.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
        self.old_email_entry.insert(0, f"{self.player.email}")
        self.old_email_entry.config(state="readonly")
        self.new_email_label = Label(self.frame_edit, text="New Email:", font=("Comic Sans MS", 15))
        self.new_email_label.grid(row=5, column=0)
        self.new_email_entry = Entry(self.frame_edit, font=("Comic Sans MS", 10))
        self.new_email_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

        self.old_password_label = Label(self.frame_edit, text="Old Password:", font=("Comic Sans MS", 15))
        self.old_password_label.grid(row=6, column=0)
        self.old_password_entry = Entry(self.frame_edit, font=("Comic Sans MS", 10))
        self.old_password_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=10)
        self.old_password_entry.insert(0, f"{self.player.password}")
        self.old_password_entry.config(state="readonly")
        self.new_password_label = Label(self.frame_edit, text="Old Password:", font=("Comic Sans MS", 15))
        self.new_password_label.grid(row=7, column=0)
        self.new_password_entry = Entry(self.frame_edit, font=("Comic Sans MS", 10))
        self.new_password_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=10)

        self.edit_button = Button(self.frame_edit, text="Edit", font=("Comic Sans MS", 10, "bold"),
                                  command=self.edit_user)
        self.edit_button.grid(row=8, column=0, padx=10, pady=10, sticky=W + E)
        self.cancel_button = Button(self.frame_edit, text="Cancel", command=self.close_window,
                                    font=("Comic Sans MS", 10, "bold"))
        self.cancel_button.grid(row=8, column=1, columnspan=3, padx=10, pady=10, sticky=W + E)

    def close_window(self):
        delete_window(self.screen)

    def edit_user(self):
        new_user = self.new_user_entry.get().lower()
        new_email = self.new_email_entry.get().lower()
        new_password = self.new_password_entry.get()
        if new_user == "":
            new_user = self.player.user
        if new_email == "":
            new_email = self.player.email
        if new_password == "":
            new_password = self.player.password
        confirm_info = messagebox.askokcancel(title="Confirm Info", message=f"Is This Info Correct?\n"
                                                                            f"New User ---> {new_user}\n"
                                                                            f"New Email ---> {new_email}\n"
                                                                            f"New Password ---> {new_password}")
        if confirm_info:
            self.player.user = new_user
            self.player.email = new_email
            self.player.password = new_password
            db.session.commit()
            self.screen.destroy()
            admin = AdminScreen()


#-------------------ADMIN SCREEN---------------------#
class AdminScreen:
    def __init__(self):
        self.screen = Tk()
        self.screen.title("Snake Tournament")
        self.screen.wm_iconbitmap('resources/icon.ico')
        self.screen.resizable(0, 0)

        self.logo = Canvas(width=200, height=200)
        self.logo_img = PhotoImage(file="resources/logo.png")
        self.logo.create_image(100, 100, image=self.logo_img)
        self.logo.grid(row=0, column=2, pady=25)
        # --------------------TABLE RANKING--------------------#
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=1, bd=1, relief="solid",
                             font=('Comic Sans MS', 15), rowheight=40)
        self.style.configure("mystyle.Treeview.Heading", highlightthickness=1, bd=1,
                             font=('Comic Sans MS', 25, 'bold'), relief="raised")
        self.canvas = Canvas(self.screen, borderwidth=0, relief="solid")
        self.canvas.grid(row=2, column=0, columnspan=4)

        self.scroll = Scrollbar(self.canvas)
        self.scroll.grid(row=2, column=0, columnspan=4, sticky=E + N + S)

        self.players_count = db.session.query(User).count()
        self.table = ttk.Treeview(self.canvas, height=5, yscrollcommand=self.scroll.set, columns=("User", "Email", "Score"), style="mystyle.Treeview")
        self.table.grid(row=2, column=0, columnspan=4, padx=20, pady=20)
        self.table.heading("#0", text="Ranking", anchor=CENTER)
        self.table.heading("User", text="User", anchor=CENTER)
        self.table.heading("Email", text="Email", anchor=CENTER)
        self.table.heading("Score", text="Score", anchor=CENTER)

        self.delete_button = Button(text="Delete", command=self.delete_user, font=("Comic Sans MS", 20, "bold"))
        self.delete_button.grid(row=4, column=2)
        self.add_button = Button(text="Add", command=self.add_user, font=("Comic Sans MS", 20, "bold"))
        self.add_button.grid(row=4, column=0, columnspan=2)
        self.edit_button = Button(text="Edit", command=self.edit_user, font=("Comic Sans MS", 20, "bold"))
        self.edit_button.grid(row=4, column=3)
        self.logout = Button(text="Log Out", command=self.logout, font=("Comic Sans MS", 15))
        self.logout.grid(row=0, column=3, sticky=E + N)

        self.filter_entry = Entry(font=("Comic Sans MS", 15))
        self.filter_entry.grid(row=1, column=1, columnspan=2, sticky=E + W)
        self.filter_button = Button(text="Search User", font=("Comic Sans MS", 20, "bold"), command=self.search_user)
        self.filter_button.grid(row=1, column=3)

        self.get_rankings()
        self._apply_row_colors()
        self.screen.mainloop()

    def search_user(self):
        search_data = self.filter_entry.get().lower()
        table_records = self.table.get_children()
        for row in table_records:
            self.table.delete(row)
        top_players = (db.session.query(User).filter(and_(User.user != "admin", User.user.ilike(f"{search_data}%"))).
                       order_by(User.score.desc()).all())
        for rank, player in enumerate(top_players, start=1):
            self.table.insert("", "end", text=rank, values=(player.user, player.email, player.score))
        self._apply_row_colors()

    def add_user(self):
        self.screen.destroy()
        add_screen = AddScreen()
        self._apply_row_colors()

    def edit_user(self):
        selection = self.table.item(self.table.selection())
        print(selection)
        if selection["text"] != "":
            selection = self.table.item(self.table.selection())["values"][0]
            print(selection)
            user = db.session.query(User).filter(User.user == selection).first()
            self.screen.destroy()
            edit_screen = EditScreen(user)
        else:
            messagebox.showerror(title="Error", message="You must select an User")

    def delete_user(self):
        user = self.table.item(self.table.selection())["values"][0]
        if user != "":
            delete_confirm = messagebox.askokcancel(title="Advertising",
                                                    message=f"You are about to delete -> {user}\n"
                                                            f"Are You Sure?")
            if delete_confirm:
                existing_user = db.session.query(User).filter(User.user == user).first()
                db.session.delete(existing_user)
                self.get_rankings()
            else:
                pass
        else:
            messagebox.showerror(title="Error", message="You must select an User")
        self._apply_row_colors()

    def logout(self):
        self.screen.destroy()
        login_screen = LogInScreen()

    def _apply_row_colors(self):
        _apply_row_colors(self.table)

    def get_rankings(self):
        table_records = self.table.get_children()
        for row in table_records:
            self.table.delete(row)
        top_players = db.session.query(User).filter(User.user != "admin").order_by(User.score.desc()).all()
        for rank, player in enumerate(top_players, start=1):
            self.table.insert("", "end", text=rank, values=(player.user, player.email, player.score))


#-------------------PLAYER SCREEN---------------------#

class PlayerScreen:
    def __init__(self, player):
        #--------------------SCREEN--------------------#
        self.screen = Tk()
        self.player = player
        self.screen.title("Snake Tournament")
        self.screen.wm_iconbitmap('resources/icon.ico')
        self.screen.resizable(0, 0)

        self.logo = Canvas(width=200, height=200)
        self.logo_img = PhotoImage(file="resources/logo.png")
        self.logo.create_image(100, 100, image=self.logo_img)
        self.logo.grid(row=0, column=2, pady=25)

        #--------------------LABELS------------------------#
        self.hi_label = Label(text=f"Hi {(self.player.user).title()}!", font=("Comic Sans MS", 25, "bold"))
        self.hi_label.grid(row=1, column=0)

        self.top_label = Label(text=f"TOP 5!", font=("Comic Sans MS", 25, "bold"))
        self.top_label.grid(row=1, column=2, columnspan=3)

        #--------------------TABLE RANKING--------------------#
        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=1, bd=1, relief="solid",
                             font=('Comic Sans MS', 15), rowheight=40)
        self.style.configure("mystyle.Treeview.Heading", highlightthickness=1, bd=1,
                             font=('Comic Sans MS', 25, 'bold'), relief="raised")
        self.canvas = Canvas(self.screen, borderwidth=0, relief="solid")
        self.canvas.grid(row=2, column=2, columnspan=3)

        self.table = ttk.Treeview(self.canvas, height=5, columns=("User", "Score"), style="mystyle.Treeview")
        self.table.grid(row=2, column=2, columnspan=3, padx=20, pady=20)
        self.table.heading("#0", text="Ranking", anchor=CENTER)
        self.table.heading("User", text="User", anchor=CENTER)
        self.table.heading("Score", text="Score", anchor=CENTER)
        #--------------------CURRENT USER RANK--------------------#
        self.rank_frame = LabelFrame(self.screen, text="Your Ranking", font=("Comic Sans MS", 20, "bold"))
        self.rank_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.user_ranking = db.session.query(User).filter(User.score > self.player.score).count()

        self.rank_label = Label(self.rank_frame, text=f"You are in the position #{self.user_ranking + 1}\n"
                                                      f"Your current score is {self.player.score}",
                                font=("Comic Sans MS", 15))
        self.rank_label.grid(row=3, column=0, padx=10, pady=10)

        #--------------------BUTTONS--------------------#
        self.play_button = Button(text="PLAY NOW", font=("Comic Sans MS", 20, "bold"), command=self.run_game)
        self.play_button.grid(row=4, column=2, pady=25, columnspan=2)

        self.logout = Button(text="Log Out", command=self.logout, font=("Comic Sans MS", 15))
        self.logout.grid(row=0, column=4, sticky=E + N)

        self.get_rankings()
        self._apply_row_colors()
        self.screen.mainloop()

    def _apply_row_colors(self):
        _apply_row_colors(self.table)

    def get_rankings(self):
        top_players = db.session.query(User).filter(User.user != "admin").order_by(User.score.desc()).limit(5)
        for rank, player in enumerate(top_players, start=1):
            self.table.insert("", "end", text=rank, values=(player.user, player.score))

    def logout(self):
        self.screen.destroy()
        login_screen = LogInScreen()

    def run_game(self):
        run_snake_game(self.player)
        self.get_rankings()
        self.rank_label.config(text=f"You are in the position #{self.user_ranking + 1}\n"
                                    f"Your High Score is {self.player.score}")




#------------------------LOG IN SCREEN------------------------------#
class LogInScreen:
    def __init__(self):
        #--------------------SCREEN--------------------#
        self.screen = Tk()
        self.screen.title("Snake Tournament")
        self.screen.wm_iconbitmap('resources/icon.ico')
        self.screen.resizable(0, 0)

        self.logo = Canvas(width=200, height=200)
        self.logo_img = PhotoImage(file="resources/logo.png")
        self.logo.create_image(100, 100, image=self.logo_img)
        self.logo.grid(row=0, column=1, pady=25)
        # --------------------LOG IN FRAME--------------------#
        self.frame_login = LabelFrame(self.screen, text="Log In", font=("Comic Sans MS", 20, "bold"))
        self.frame_login.grid(row=1, column=0, columnspan=3, padx=75)

        self.user_label = Label(self.frame_login, text="User:", font=("Comic Sans MS", 15))
        self.user_label.grid(row=2, column=0)
        self.user_entry = Entry(self.frame_login, font=("Comic Sans MS", 10))
        self.user_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        self.password_label = Label(self.frame_login, text="Password:", font=("Comic Sans MS", 15))
        self.password_label.grid(row=3, column=0)
        self.password_entry = Entry(self.frame_login, show="*", font=("Comic Sans MS", 10))
        self.password_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        self.log_in_button = Button(self.frame_login, text="Log In", font=("Comic Sans MS", 10, "bold"), command=self.login)
        self.log_in_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky= W + E)
        # --------------------REGISTER FRAME--------------------#
        self.frame_register = LabelFrame(self.screen, text="Register", font=("Comic Sans MS", 20, "bold"))
        self.frame_register.grid(row=5, column=0, columnspan=3, pady=25, padx=75, sticky=W + E)

        self.register_user_label = Label(self.frame_register, text="User:", font=("Comic Sans MS", 15))
        self.register_user_label.grid(row=6, column=0)
        self.register_user_entry = Entry(self.frame_register, font=("Comic Sans MS", 10))
        self.register_user_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

        self.register_email_label = Label(self.frame_register, text="Email:", font=("Comic Sans MS", 15))
        self.register_email_label.grid(row=7, column=0)
        self.register_email_entry = Entry(self.frame_register, font=("Comic Sans MS", 10))
        self.register_email_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=10)

        self.register_password_label = Label(self.frame_register, text="Password:", font=("Comic Sans MS", 15))
        self.register_password_label.grid(row=8, column=0)
        self.register_password_entry = Entry(self.frame_register, font=("Comic Sans MS", 10))
        self.register_password_entry.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

        self.register_button = Button(self.frame_register, text="Register", command=self.register, font=("Comic Sans MS", 10, "bold"))
        self.register_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

        self.screen.mainloop()

    def login(self):
        user_info = self.user_entry.get().lower()
        password_info = self.password_entry.get()
        user_result = db.session.query(User).filter(User.user == user_info).first()
        if user_result is not None:
            if user_result.user == "admin":
                if password_info == user_result.password:
                    self.screen.destroy()
                    admin_screen = AdminScreen()
                else:
                    messagebox.showerror(title="Error", message="The password or user is incorrect\n")
            else:
                if password_info == user_result.password:
                    self.screen.destroy()
                    player_screen = PlayerScreen(user_result)
                else:
                    messagebox.showerror(title="Error", message="The password or user is incorrect\n")
        else:
            messagebox.showerror(title="Error", message="The password or user is incorrect\n")

    def register(self):
        user_info = self.register_user_entry.get().lower()
        email_info = self.register_email_entry.get().lower()
        password_info = self.register_password_entry.get()
        if user_info != "" and email_info != "" and password_info != "":
            result_user = db.session.query(User).filter(User.user == user_info).first()
            result_email = db.session.query(User).filter(User.email == email_info).first()
            if result_user is None and result_email is None:
                correct_info = messagebox.askokcancel(title="Confirm Info",
                                                      message=f"Do you want to create this user?:\n"
                                                              f"User: {user_info}\n"
                                                              f"Email: {email_info}\n"
                                                              f"Password: {password_info}")
                if correct_info:
                    new_user = User(user=user_info, email=email_info, password=password_info)
                    db.session.add(new_user)
                    db.session.commit()
                    db.session.close()
                    self.register_user_entry.delete(0, END)
                    self.register_email_entry.delete(0, END)
                    self.register_password_entry.delete(0, END)
            elif result_user is not None and result_email is None:
                messagebox.showerror(title="Error", message="User already in use")
            elif result_email is not None and result_user is None:
                messagebox.showerror(title="Error", message="Email already in use")
            else:
                messagebox.showerror(title="Error", message="User and Email already in use")
        else:
            messagebox.showerror(title="Error", message="Missing Info")

