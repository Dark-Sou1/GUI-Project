import customtkinter
class message_box:
    def __init__(self, _, title, message):
        root = customtkinter.CTk()
        root.geometry("400x175")
        root.title(title)
        message = customtkinter.CTkLabel(master=root, text=message, text_font=("Roboto Medium", 15))
        message.pack(pady=60)
        root.mainloop()