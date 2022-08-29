import tkinter
import tkinter.messagebox
import customtkinter
import rtadubai
import json
import hashlib

customtkinter.set_appearance_mode("System")

class message_box(customtkinter.CTk):
    def __init__(self, parent, title, message):
        parent.destroy()
        super().__init__()
        self.geometry("400x175")
        self.title(title)
        self.iconphoto(True, tkinter.PhotoImage(file=r"gui\assets\error.png"))
        self.message = customtkinter.CTkLabel(master=self, text=message, text_font=("Roboto Medium", 15))
        self.message.pack(pady=60)
        self.mainloop()

class App(customtkinter.CTk):

    def __init__(self):

        super().__init__()
        self.title("TravelManager")
        self.iconphoto(True, tkinter.PhotoImage(file = r"gui\assets\logo.png"))
        self.geometry("780x520")
        self.resizable(False, False)
        self.login_or_create_account()

    def login_or_create_account(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_loca = customtkinter.CTkFrame(master=self,width=400,height=200,corner_radius=5)
        self.frame_loca.grid(row=0, column=0, sticky="nswe",padx = 20, pady = 20)

        self.label_loca = customtkinter.CTkLabel(master=self.frame_loca,text="TravelManager",text_font=("Roboto Medium", 30))
        self.label_loca.pack(pady=70)

        self.login_button = customtkinter.CTkButton(master=self.frame_loca,text="Login",command=self.login_screen)
        self.login_button.pack(pady=10)

        self.create_account = customtkinter.CTkButton(master=self.frame_loca,text="Create Account",command=self.create_account_screen)
        self.create_account.pack(pady=10)

    def create_account_screen(self):
        pass

    def login_screen(self):
        
        self.frame_loca.destroy()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_login = customtkinter.CTkFrame(master=self,width=400,height=200,corner_radius=5)
        self.frame_login.grid(row=0, column=0, sticky="nswe",padx = 20, pady = 20)

        self.label_login = customtkinter.CTkLabel(master=self.frame_login,text="Login",text_font=("Roboto Medium", 30))
        self.label_login.pack(pady=70)

        self.entry_id = customtkinter.CTkEntry(master=self.frame_login,width=200,placeholder_text="Username")
        self.entry_id.pack(pady=10)

        self.entry_password = customtkinter.CTkEntry(master=self.frame_login,width=200,show="*",placeholder_text="Password")
        self.entry_password.pack(pady=10)

        self.button_login = customtkinter.CTkButton(master=self.frame_login,text="Login",command=self.login)
        self.button_login.pack(pady=10)

    def login(self):

        self.id = self.entry_id.get()
        self.password = self.entry_password.get()

        with open(r"gui\assets\login.json", "r") as f:
            data = json.load(f)
            try:
                if data[self.id]["password"] == hashlib.sha256(self.password.encode()).hexdigest():
                    self.nol_id = data[self.id]["nol"]
                    self.plate = data[self.id]["plate"]
                    self.phone = data[self.id]["number"]
                    try:
                        self.main_screen()
                    except Exception as e:
                        print(e)
                else:
                    message_box(self, "Invalid Login", "Invalid Username or Password")
            except:
                message_box(self, "Invalid Login", "Invalid Username or Password")

    def main_screen(self):

        self.frame_login.destroy()

        # =========== main frames ===========

        self.frame_left = customtkinter.CTkFrame(master=self,width=180,corner_radius=0)
        self.frame_left.pack(side="left",fill="y")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.pack(side="right", padx=20, pady=20,fill="y",anchor="center",ipadx=120)

        # ============ frame left ============
        
        self.label_main = customtkinter.CTkLabel(master=self.frame_left,text="TravelManager",text_font=("Roboto Medium", -18))
        self.label_main.pack(pady=20,padx =20, anchor="center")
    
        self.button_nol = customtkinter.CTkButton(master=self.frame_left,text="Nol",command=self.nol_display)
        self.button_nol.pack(padx=10,pady=15)
    
        self.button_salik = customtkinter.CTkButton(master=self.frame_left,text="Salik",command=lambda: print("Hello, World!"))
        self.button_salik.pack(pady=10,padx=10)

        self.nol_display(k=True)

        # ============ frame right ============

    def nol_display(self, k=False):
        if not k:
            self.frame_display_right_1.destroy()
            self.frame_display_right_2.destroy()
            self.frame_display_right_3.destroy()
            self.view_transactions.destroy()
            # self.frame_display_right_5.destroy()

        self.nol = rtadubai.Nol.Card(int(self.nol_id))

        self.frame_display_right_1 = customtkinter.CTkFrame(master=self.frame_right,corner_radius=10)
        self.frame_display_right_1.pack(fill="x",padx=10,pady=10,anchor="n")

        self.bal = customtkinter.CTkLabel(master=self.frame_display_right_1,text="Balance:",text_font=("Roboto Medium", 0))
        self.bal.pack(side="left",padx=10,pady=10)

        self.bal_show = customtkinter.CTkLabel(master=self.frame_display_right_1,text=f"{self.nol.balance} Dhs",text_font=("Roboto Medium", 25))
        self.bal_show.pack(padx=20,pady=20)

        self.frame_display_right_2 = customtkinter.CTkFrame(master=self.frame_right,corner_radius=10)
        self.frame_display_right_2.pack(fill="x",padx=10,pady=10,anchor="n")

        self.expiry = customtkinter.CTkLabel(master=self.frame_display_right_2,text="Expiry:",text_font=("Roboto Medium", 0))
        self.expiry.pack(side="left",padx=10,pady=10)

        self.expiry_show = customtkinter.CTkLabel(master=self.frame_display_right_2,text=f"{self.nol.expiry}",text_font=("Roboto Medium", 25))
        self.expiry_show.pack(padx=20,pady=20)

        self.frame_display_right_3 = customtkinter.CTkFrame(master=self.frame_right,corner_radius=10)
        self.frame_display_right_3.pack(fill="x",padx=10,pady=10,anchor="n")

        self.pendings = customtkinter.CTkLabel(master=self.frame_display_right_3,text="Pending:",text_font=("Roboto Medium", 0))
        self.pendings.pack(side="left",padx=10,pady=10)

        self.pendings_show = customtkinter.CTkLabel(master=self.frame_display_right_3,text=f"{self.nol.pending}",text_font=("Roboto Medium", 25))
        self.pendings_show.pack(padx=20,pady=20)

        self.view_transactions = customtkinter.CTkButton(master=self.frame_right,text="View Transactions",command=lambda: print("Hello, World!"))
        self.view_transactions.pack(anchor="center",pady=10,padx=10)

    def transactions(self):
        pass

    def run(self):
        
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
