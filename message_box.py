import customtkinter
class message_box:
    def __init__(self, _, title, message):
        root = customtkinter.CTk()
        root.geometry("400x175")
        root.title(title)
        kelp = customtkinter.CTkFrame(root)
        kelp.pack()
        message = customtkinter.CTkLabel(master=kelp, text=message, text_font=("Roboto Medium", 15))
        message.pack(pady=60)
        root.mainloop()