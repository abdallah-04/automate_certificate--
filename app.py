import os
import tkinter as tk
from tkinter import ttk, filedialog

BG_COLOR = "#164b92"
LABEL_WIDTH = 15
def run_gui():
    window = tk.Tk()
    window.title("MD ON TOP")
    window.geometry("450x520")
    window.configure(bg=BG_COLOR)

    title_label = tk.Label(
        window,
        text="Certification Info",
        font=("Helvetica", 14, "bold"),
        fg="orange",
        bg=BG_COLOR
    )
    title_label.pack(pady=(15, 10))

    def create_field(parent, label_text, entry_widget=None, is_dropdown=False, values=None, browse=False, initial_value=""):
        frame = tk.Frame(parent, bg=BG_COLOR)
        frame.pack(pady=5, padx=20, anchor="w", fill="x")

        tk.Label(frame, text=label_text, font=("Helvetica", 10, "bold"),
             fg="white", bg=BG_COLOR, width=LABEL_WIDTH, anchor="w").pack(side="left")

        if is_dropdown:
            var = tk.StringVar()
            widget = ttk.Combobox(frame, textvariable=var, values=values, width=25)
        else:
            widget = tk.Entry(frame, width=27)
            widget.insert(0, initial_value)  

        widget.pack(side="left")

        if browse:
            def browse_path():
                path = filedialog.askopenfilename(title="Select Font Path")  
                widget.delete(0, tk.END)
                widget.insert(0, path)

            tk.Button(frame, text="Find", command=browse_path, bg="orange", fg="white", width=10).pack(side="left", padx=5)

        return widget

    workshop_entry = create_field(window, "Workshop Name:")
    cert_type_dropdown = create_field(window, "Certificate Type:", is_dropdown=True,
                                  values=["Certificate", "Badge"])

    sender_entry = create_field(window, "Sender Name:")
    position_entry = create_field(window, "Position:")
    cert_path_entry = create_field(window, "Certificate Path:", browse=True)
    font_path_entry = create_field(window, "Font Path:", browse=True, initial_value=r"C:\Windows\Fonts\times.ttf")

    body_frame = tk.Frame(window, bg=BG_COLOR)
    body_frame.pack(pady=5, padx=20, anchor="w", fill="x")

    tk.Label(body_frame, text="Email Body:", font=("Helvetica", 10, "bold"),
         fg="white", bg=BG_COLOR, width=LABEL_WIDTH, anchor="nw", justify="left").grid(row=0, column=0, sticky="nw")

    email_body_text = tk.Text(body_frame, width=27, height=8, wrap="word")
    email_body_text.grid(row=0, column=1, padx=2)

    def handle_send():
        import main
        import os
        os.environ["certificate_path"] = cert_path_entry.get()
        workshop_name = workshop_entry.get()
        os.environ["BASE_DIR"] = f"./generated_certificates/{workshop_name}"
        os.environ["FONT_PATH"] = font_path_entry.get()
        os.environ["WORKSHOP_NAME"] = workshop_name
        os.environ["CERT_TYPE"] = cert_type_dropdown.get()
        os.environ["SENDER_NAME"] = sender_entry.get()
        os.environ["POSITION"] = position_entry.get()
        os.environ["EMAIL_BODY"] = email_body_text.get("1.0", tk.END)

        main.main()

    send_button = tk.Button(window, text="Send", bg="orange", fg="white", width=10, command=handle_send)
    send_button.pack(pady=20)


    window.mainloop()