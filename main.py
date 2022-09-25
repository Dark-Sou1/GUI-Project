from re import search
import time
import tkinter
import tkinter.messagebox
import customtkinter
import rtadubai
import json
import hashlib
from PIL import Image, ImageTk
import os

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")
PATH = os.path.dirname(os.path.realpath(__file__))


class message_box():
    def __init__(self, _, title, message):
        root = customtkinter.CTk()
        root.geometry("400x175")
        root.title(title)
        message = customtkinter.CTkLabel(
            master=root, text=message, text_font=("Roboto Medium", 15))
        message.pack(pady=60)
        root.mainloop()


class App(customtkinter.CTk):

    def __init__(self):

        super().__init__()
        self.color_1 = "#333333"
        self.color_2 = "#292929"
        self.color_3 = "gray25"
        self.title("TravelManager")
        self.iconphoto(True, tkinter.PhotoImage(
            file=PATH+r"\assets\images\logo_white.png"))
        self.geometry("780x520")
        self.resizable(False, False)
        self.login_or_create_account()

    def login_or_create_account(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_loca = customtkinter.CTkFrame(
            master=self, width=400, height=200, corner_radius=5)
        self.frame_loca.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.label_loca = customtkinter.CTkLabel(
            master=self.frame_loca, text="TravelManager", text_font=("Roboto Medium", 30))
        self.label_loca.pack(pady=70)

        self.login_button = customtkinter.CTkButton(
            master=self.frame_loca, text="Login", command=self.login_screen)
        self.login_button.pack(pady=10)

        self.create_account_button = customtkinter.CTkButton(
            master=self.frame_loca, text="Create Account", command=self.create_account_screen)
        self.create_account_button.pack(pady=10)

    def create_account_screen(self):

        for widgets in self.winfo_children():
            widgets.destroy()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_create_account = customtkinter.CTkFrame(
            master=self, width=400, height=200, corner_radius=5)
        self.frame_create_account.grid(
            row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.label_create_account = customtkinter.CTkLabel(
            master=self.frame_create_account, text="Create Account", text_font=("Roboto Medium", 30))
        self.label_create_account.pack(pady=40)

        self.entry_id = customtkinter.CTkEntry(
            master=self.frame_create_account, width=200, placeholder_text="Username")
        self.entry_id.pack(pady=10)

        self.entry_password = customtkinter.CTkEntry(
            master=self.frame_create_account, width=200, show="*", placeholder_text="Password")
        self.entry_password.pack(pady=10)

        self.entry_nol = customtkinter.CTkEntry(
            master=self.frame_create_account, width=200, placeholder_text="NOL ID")
        self.entry_nol.pack(pady=10)

        self.entry_plate = customtkinter.CTkEntry(
            master=self.frame_create_account, width=200, placeholder_text="Plate number")
        self.entry_plate.pack(pady=10)

        self.entry_phone = customtkinter.CTkEntry(
            master=self.frame_create_account, width=200, placeholder_text="Phone number (eg: +971561234567")
        self.entry_phone.pack(pady=10)

        self.button_create_account = customtkinter.CTkButton(
            master=self.frame_create_account, text="Create Account", command=self.create_account)
        self.button_create_account.pack(pady=20)

    def create_account(self):

        for i in [self.entry_id, self.entry_password, self.entry_nol, self.entry_plate, self.entry_phone]:
            if i.get() == "":
                message_box(self, "Invalid Input",
                            "Please fill all the fields")
                return
        if len(self.entry_phone.get()) != 13:
            message_box(self, "Invalid Input",
                        "Please enter a valid phone number")
            return
        elif len(self.entry_plate.get()) > 7 or self.entry_plate.get()[0].isdigit():
            message_box(self, "Invalid Input",
                        "Please enter a valid plate number")
            return
        elif rtadubai.Nol.isvalid(self.entry_nol.get()) == False:
            message_box(self, "Invalid Input", "Please enter a valid NOL ID")
            return
        elif len(self.entry_password.get()) < 8:
            message_box(self, "Invalid Input",
                        "Password must be at least 8 characters long")
            return
        elif len(self.entry_id.get()) < 5:
            message_box(self, "Invalid Input",
                        "Username must be at least 5 characters long")
            return
        with open(fr"{PATH}\assets\login.json", "r") as f:
            accounts = json.load(f)
        if self.entry_id.get() in accounts:
            message_box(self, "Invalid Account", "Account already exists")
        else:
            accounts[self.entry_id.get()] = {
                "password": hashlib.sha256(self.entry_password.get().encode()).hexdigest(),
                "nol": self.entry_nol.get(),
                "plate": self.entry_plate.get(),
                "number": self.entry_phone.get()
            }
            with open(fr"{PATH}\assets\login.json", "w") as f:
                json.dump(accounts, f)
            message_box(self, "Account Created",
                        "Account created successfully")
            self.logout()

    def login_screen(self):

        self.frame_loca.destroy()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_login = customtkinter.CTkFrame(
            master=self, width=400, height=200, corner_radius=5)
        self.frame_login.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.label_login = customtkinter.CTkLabel(
            master=self.frame_login, text="Login", text_font=("Roboto Medium", 30))
        self.label_login.pack(pady=70)

        self.entry_id = customtkinter.CTkEntry(
            master=self.frame_login, width=200, placeholder_text="Username")
        self.entry_id.pack(pady=10)

        self.entry_password = customtkinter.CTkEntry(
            master=self.frame_login, width=200, show="*", placeholder_text="Password")
        self.entry_password.pack(pady=10)

        self.button_login = customtkinter.CTkButton(
            master=self.frame_login, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):

        self.id = self.entry_id.get()
        self.password = self.entry_password.get()

        with open(fr"{PATH}\assets\login.json", "r") as f:
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
                    message_box(self, "Invalid Login",
                                "Invalid Username or Password")
            except:
                message_box(self, "Invalid Login",
                            "Invalid Username or Password")

    def settings(self):

        self.settings_button.destroy()

        self.settings_frame = customtkinter.CTkFrame(
            master=self.frame_left, width=140, height=150, corner_radius=5)
        self.settings_frame.pack(anchor="s", padx=20, pady=20, side="bottom")
        self.settings_frame.pack_propagate(False)

        self.close_button = customtkinter.CTkButton(master=self.settings_frame,
                                                    image=self.close, text="", width=10, height=10,
                                                    fg_color=f"{self.color_1}", hover_color=f"{self.color_1}",
                                                    command=self.close_settings)
        self.close_button.pack(pady=3, padx=3, anchor="se")

        self.logout_button = customtkinter.CTkButton(
            master=self.settings_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=0, padx=20)

        self.change_details_button = customtkinter.CTkButton(
            master=self.settings_frame, text="Change Detail", command=lambda: print("Change Details"))
        self.change_details_button.pack(pady=10, padx=20)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.settings_frame,
                                                        values=[
                                                            "Dark", "Light"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.pack(pady=0, padx=20)

    def change_appearance_mode(self, value):
        customtkinter.set_appearance_mode(value)
        if value == "Dark":
            self.color_1 = "#333333"
            self.color_2 = "#292929"
            self.color_3 = "gray25"
            self.iconphoto(True, tkinter.PhotoImage(
                file=PATH+r"\assets\images\logo_white.png"))
        elif value == "Light":
            self.color_1 = "#dbdbdb"
            self.color_2 = "#ebebeb"
            self.color_3 = "#c8c7c7"
            self.iconphoto(True, tkinter.PhotoImage(
                file=PATH+r"\assets\images\logo_dark.png"))
        self.close_button.configure(
            fg_color=f"{self.color_1}", hover_color=f"{self.color_1}")

    def logout(self):

        for widgets in self.winfo_children():
            widgets.destroy()

        self.login_or_create_account()

    def close_settings(self):

        self.settings_frame.destroy()
        self.settings_button = customtkinter.CTkButton(master=self.frame_left, image=self.settings_image, text="settings", width=40, height=40,
                                                       corner_radius=10, fg_color=f"{self.color_2}", hover_color=f"{self.color_3}", text_font=("Roboto Medium", -13),
                                                       command=self.settings)

        self.settings_button.pack(anchor="sw", pady=10, padx=10, side="bottom")

    def main_screen(self):

        self.frame_login.destroy()

        self.settings_image = self.load_image(
            r"\assets\images\settings.png", 30, 30)
        self.close = self.load_image(r"\assets\images\close.png", 10, 10)

        # =========== main frames ===========

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=180, corner_radius=0)
        self.frame_left.pack(side="left", fill="y")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.pack(side="right", padx=20, pady=20,
                              fill="y", anchor="center", ipadx=120)

        # ============ frame left ============

        self.label_main = customtkinter.CTkLabel(
            master=self.frame_left, text="TravelManager", text_font=("Roboto Medium", -18))
        self.label_main.pack(pady=20, padx=20, anchor="center")

        self.button_nol = customtkinter.CTkButton(
            master=self.frame_left, text="Nol", height=32, command=self.nol_display)
        self.button_nol.pack(padx=10, pady=15)

        self.button_salik = customtkinter.CTkButton(
            master=self.frame_left, text="Salik", height=32, command=self.salik_display)
        self.button_salik.pack(pady=10, padx=10)

        self.button_departure = customtkinter.CTkButton(
            master=self.frame_left, text="Departure", height=32, command=self.departure_display)
        self.button_departure.pack(pady=10, padx=10)

        self.button_journey = customtkinter.CTkButton(
            master=self.frame_left, text="Journey", height=32, command=self.journey_display)
        self.button_journey.pack(pady=10, padx=10)

        self.settings_button = customtkinter.CTkButton(master=self.frame_left, image=self.settings_image,
                                                       text="settings", width=40, height=40,
                                                       corner_radius=10, fg_color=f"{self.color_2}",
                                                       hover_color=f"{self.color_3}", text_font=("Roboto Medium", -13),
                                                       command=self.settings)

        self.settings_button.pack(anchor="sw", pady=10, padx=10, side="bottom")

        self.nol_display()

    def journey_display(self):

        for widgets in self.frame_right.winfo_children():
            widgets.destroy()

    def departure_display(self):

        for widgets in self.frame_right.winfo_children():
            widgets.destroy()

        self.frame_right.pack_propagate(False)
        self.frame_dropdown = customtkinter.CTkFrame(
            master=self.frame_right, width=400, height=25)
        self.frame_dropdown.grid(row=0, column=0, pady=10, padx=10)
        self.entry_departure = customtkinter.CTkEntry(
            master=self.frame_dropdown, width=400, placeholder_text="Enter departure")
        self.entry_departure.grid(row=0, column=0, pady=5, padx=5)

        self.button_search = customtkinter.CTkButton(
            master=self.frame_right, text="Search", width=120, command=self.view_results)
        self.button_search.grid(row=0, column=1, pady=15, padx=2, sticky="n")

        self.button_ddd = customtkinter.CTkButton(
            master=self.frame_dropdown, text=". . .", text_font=("Roboto Medium", 10),
            width=300, height=25,
            bg=f"{self.color_2}", fg_color=f"{self.color_3}", command=self.search_departure, corner_radius=5)
        self.button_ddd.grid(row=1, column=0, pady=5, padx=5, ipadx=60)

    def view_results(self):
        self.close_search_deps()
        self.frame_of_doom = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_of_doom.grid(row=1, column=0, pady=10,
                                padx=10, sticky="nswe", columnspan=2, ipady=100)
        self.frame_of_doom.pack_propagate(False)
        self.stop = rtadubai.Stop(self.entry_departure.get())
        self.deps = rtadubai.Shail.departures(self.stop)
        for i in self.deps:

            self.frame_deps = customtkinter.CTkFrame(master=self.frame_of_doom,height=50,corner_radius=0)
            self.frame_deps.pack(pady=10, padx=10,fill="x")
            self.frame_deps.pack_propagate(False)

            self.indicator_color = customtkinter.CTkFrame(master=self.frame_deps,bg_color="#1ab450",fg_color="#1ab450", width=5)
            self.indicator_color.pack(side="left", padx=0, pady=0,fill="y")

    def on_click(self, event):
        self.entry_departure.delete(0, "end")
        self.entry_departure.insert(0, event)


    def search_departure(self):
        try:
            self.frame_of_doom.destroy()
        except:
            pass
        _c = 0
        for widgets in self.frame_dropdown.winfo_children():
            if _c == 0:
                pass
            else:
                widgets.destroy()
            _c += 1

        self.data_dep = self.entry_departure.get()

        self.frame_dropdown.configure(height=720)
        self.frame_dropdown.update()
        self.list_of_deps = rtadubai.Shail.stopnames(self.data_dep)
        c = 2
        for i in self.list_of_deps:
            self.label_deps_dropdown = customtkinter.CTkButton(
                master=self.frame_dropdown, width=300, height=25, text=i, text_font=("Roboto Medium", -10),
                bg=f"{self.color_2}", fg_color=f"{self.color_3}", command=lambda i=i: self.on_click(i), corner_radius=5)
            self.label_deps_dropdown.grid(
                row=c, column=0, pady=3, padx=3, ipadx=60)
            c += 2
        self.button_ddd = customtkinter.CTkButton(
            master=self.frame_dropdown, text="Close", text_font=("Roboto Medium", 10),
            width=300, height=25,
            bg=f"{self.color_2}", fg_color="#C41E3A", hover_color="#D56376", command=self.close_search_deps, corner_radius=5)
        self.button_ddd.grid(row=1, column=0, pady=5, padx=5, ipadx=60)
        self.button_dn = customtkinter.CTkButton(
            master=self.frame_dropdown, text="Refresh", text_font=("Roboto Medium", 10),
            width=300, height=25,
            command=self.search_departure, corner_radius=5)
        self.button_dn.grid(row=2, column=0, pady=5, padx=5, ipadx=60)

    def close_search_deps(self):
        _c = 0
        for widgets in self.frame_dropdown.winfo_children():
            if _c == 0:
                pass
            else:
                widgets.destroy()
            _c += 1
        self.frame_dropdown.configure(height=25)
        self.frame_dropdown.update()
        self.button_ddd = customtkinter.CTkButton(
            master=self.frame_dropdown, text=". . .", text_font=("Roboto Medium", 10),
            width=300, height=25,
            bg=f"{self.color_2}", fg_color=f"{self.color_3}", command=self.search_departure, corner_radius=5)
        self.button_ddd.grid(row=1, column=0, pady=5, padx=5, ipadx=60)

    def nol_display(self):

        for widgets in self.frame_right.winfo_children():
            widgets.destroy()

        self.nol = rtadubai.Nol.Card(self.nol_id)

        self.nol_label = customtkinter.CTkLabel(
            master=self.frame_right, text="Nol", text_font=("Roboto Medium", -21))
        self.nol_label.pack(pady=20, padx=0, anchor="n")

        self.frame_display_right_1 = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=10)
        self.frame_display_right_1.pack(fill="x", padx=10, pady=10, anchor="n")

        self.bal = customtkinter.CTkLabel(
            master=self.frame_display_right_1, text="Balance:", text_font=("Roboto Medium", 0))
        self.bal.pack(side="left", padx=10, pady=10)

        self.bal_show = customtkinter.CTkLabel(
            master=self.frame_display_right_1, text=f"{self.nol.balance} Dhs", text_font=("Roboto Medium", 25))
        self.bal_show.pack(padx=20, pady=20)

        self.frame_display_right_2 = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=10)
        self.frame_display_right_2.pack(fill="x", padx=10, pady=10, anchor="n")

        self.expiry = customtkinter.CTkLabel(
            master=self.frame_display_right_2, text="Expiry:", text_font=("Roboto Medium", 0))
        self.expiry.pack(side="left", padx=10, pady=10)

        self.expiry_show = customtkinter.CTkLabel(
            master=self.frame_display_right_2, text=f"{self.nol.expiry}", text_font=("Roboto Medium", 25))
        self.expiry_show.pack(padx=20, pady=20)

        self.frame_display_right_3 = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=10)
        self.frame_display_right_3.pack(fill="x", padx=10, pady=10, anchor="n")

        self.pendings = customtkinter.CTkLabel(
            master=self.frame_display_right_3, text="Pending:", text_font=("Roboto Medium", 0))
        self.pendings.pack(side="left", padx=10, pady=10)

        self.pendings_show = customtkinter.CTkLabel(
            master=self.frame_display_right_3, text=f"{self.nol.pending}", text_font=("Roboto Medium", 25))
        self.pendings_show.pack(padx=20, pady=20)

        self.view_transactions = customtkinter.CTkButton(
            master=self.frame_right, text="View Transactions", command=self.transactions)
        self.view_transactions.pack(anchor="center", pady=10, padx=10)

    def transactions(self):

        for widgets in self.frame_right.winfo_children():
            widgets.destroy()

        transactions = rtadubai.Nol.transactions(self.nol_id)['Transactions']
        if len(transactions) == 0:
            self.frame_right.pack_propagate(False)
            self.transaction_label = customtkinter.CTkLabel(
                master=self.frame_right, text="No transactions found", text_font=("Roboto Medium", 20))
            self.transaction_label.pack(padx=100)
        else:
            self.scroll_canvas = customtkinter.CTkCanvas(
                master=self.frame_right, highlightbackground=f"{self.color_2}")
            self.scroll_canvas.pack(fill="both", expand=True, side="left")

            my_scroll = customtkinter.CTkScrollbar(
                master=self.frame_right, orientation="vertical", command=self.scroll_canvas.yview)
            my_scroll.pack(fill="y", side="right")

            self.scroll_canvas.configure(yscrollcommand=my_scroll.set)
            self.scroll_canvas.bind("<Configure>", lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")))

            self.transaction_frame = customtkinter.CTkFrame(
                master=self.scroll_canvas, corner_radius=0)

            self.scroll_canvas.create_window(
                (0, 0), window=self.transaction_frame, anchor="nw", width=700)
            for i in transactions:
                self.temp_frame = customtkinter.CTkFrame(
                    master=self.transaction_frame, width=520, height=300)
                self.temp_frame.pack(anchor="w", padx=10, pady=10)
                self.temp_frame.pack_propagate(False)

                self.frame_frame_1 = customtkinter.CTkFrame(
                    master=self.temp_frame)
                self.frame_frame_1.pack(
                    anchor="center", fill="x", padx=10, pady=10)

                self.temp_label_11 = customtkinter.CTkLabel(
                    master=self.frame_frame_1, text="Date:", text_font=("Roboto Medium", 10))
                self.temp_label_11.pack(side="left", padx=10, pady=10)

                self.temp_label_1 = customtkinter.CTkLabel(
                    master=self.frame_frame_1, text=i['Date'], text_font=("Roboto Medium", 18))
                self.temp_label_1.pack(side="left", padx=10, pady=10)

                self.frame_frame_2 = customtkinter.CTkFrame(
                    master=self.temp_frame)
                self.frame_frame_2.pack(
                    anchor="center", fill="x", padx=10, pady=10)

                self.temp_label_22 = customtkinter.CTkLabel(
                    master=self.frame_frame_2, text="Time:", text_font=("Roboto Medium", 10))
                self.temp_label_22.pack(side="left", padx=10, pady=10)

                self.temp_label_2 = customtkinter.CTkLabel(
                    master=self.frame_frame_2, text=i['Time'], text_font=("Roboto Medium", 18))
                self.temp_label_2.pack(side="left", padx=10, pady=10)

                self.frame_frame_3 = customtkinter.CTkFrame(
                    master=self.temp_frame)
                self.frame_frame_3.pack(
                    anchor="center", fill="x", padx=10, pady=10)

                self.temp_label_33 = customtkinter.CTkLabel(
                    master=self.frame_frame_3, text="Amount:", text_font=("Roboto Medium", 10))
                self.temp_label_33.pack(side="left", padx=10, pady=10)

                self.temp_label_3 = customtkinter.CTkLabel(
                    master=self.frame_frame_3, text=i['Amount'], text_font=("Roboto Medium", 18))
                self.temp_label_3.pack(side="left", padx=10, pady=10)

                self.frame_frame_4 = customtkinter.CTkFrame(
                    master=self.temp_frame)
                self.frame_frame_4.pack(
                    anchor="center", fill="x", padx=10, pady=10)

                self.temp_label_44 = customtkinter.CTkLabel(
                    master=self.frame_frame_4, text="Type:", text_font=("Roboto Medium", 10))
                self.temp_label_44.pack(side="left", padx=10, pady=10)
                self._text, self._size = self._split(i['Type'])
                self.temp_label_4 = customtkinter.CTkLabel(
                    master=self.frame_frame_4, text=self._text, text_font=("Roboto Medium", self._size))
                self.temp_label_4.pack(side="left", padx=10, pady=10)

    def _split(self, text):

        if len(text) > 38:
            x = text.split(" ")
            y = len(x)
            z = y//2
            a = ""
            for i in range(len(x)):
                a += x[i]
                if i == z:
                    a += "\n"
                else:
                    a += " "
            return a, 14
        else:
            return text, 18

    def salik_display(self):

        for widgets in self.frame_right.winfo_children():
            widgets.destroy()

        self.salik_expiry = rtadubai.Salik.expiry(self.plate)
        self.salik_balance = rtadubai.Salik.balance_plate(
            self.plate, self.phone)

        self.salik_label = customtkinter.CTkLabel(
            master=self.frame_right, text="Salik", text_font=("Roboto Medium", -21))
        self.salik_label.pack(pady=20, padx=0, anchor="n")

        self.frame_display_right_1 = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=10)
        self.frame_display_right_1.pack(fill="x", padx=10, pady=10, anchor="n")

        self.bal = customtkinter.CTkLabel(
            master=self.frame_display_right_1, text="Balance:", text_font=("Roboto Medium", 0))
        self.bal.pack(side="left", padx=10, pady=10)

        self.bal_show = customtkinter.CTkLabel(
            master=self.frame_display_right_1, text=f"{self.salik_balance} Dhs", text_font=("Roboto Medium", 25))
        self.bal_show.pack(padx=20, pady=20)

        self.frame_display_right_2 = customtkinter.CTkFrame(
            master=self.frame_right, corner_radius=10)
        self.frame_display_right_2.pack(fill="x", padx=10, pady=10, anchor="n")

        self.expiry = customtkinter.CTkLabel(
            master=self.frame_display_right_2, text="Expiry:", text_font=("Roboto Medium", 0))
        self.expiry.pack(side="left", padx=10, pady=10)

        self.expiry_show = customtkinter.CTkLabel(
            master=self.frame_display_right_2, text=f"{self.salik_expiry}", text_font=("Roboto Medium", 25))
        self.expiry_show.pack(padx=20, pady=20)

    def run(self):
        self.mainloop()

    def load_image(self, path, image_size1, image_size2):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size2, image_size1)))


if __name__ == "__main__":
    app = App()
    app.run()
