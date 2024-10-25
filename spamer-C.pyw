import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import webbrowser
import os
import threading

class SpammerApp:
    def __init__(self, master):
        self.master = master
        master.title("Spammeur d'e-mails Professionnel")
        master.geometry("1000x800")
        
        self.create_background()
        self.show_intro_screen()
        self.master.after(5000, self.create_widgets)
        
        self.stop_sending = False

    def create_background(self):
        self.canvas = tk.Canvas(self.master, bg='#001f3f', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        for _ in range(100):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            size = random.randint(5, 15)
            color = self.generate_gradient_color()
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color)
            self.master.update()
            time.sleep(0.01)

    def generate_gradient_color(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    def show_intro_screen(self):
        self.intro_text = self.canvas.create_text(500, 400, text="SPAMMER D'E-MAILS", 
                                                  font=('Helvetica', 60, 'bold'), fill='#FFD700')
        self.canvas.create_oval(450, 350, 550, 450, fill='', outline='#FFD700', width=3)
        self.master.update()
        time.sleep(0.5)
        self.loading_text = self.canvas.create_text(500, 480, text="Chargement...", 
                                font=('Helvetica', 24), fill='#FFFFFF')
        self.master.update()

    def create_widgets(self):
        self.canvas.delete("all")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Helvetica', 14, 'bold'), relief=tk.RAISED)
        style.configure('TLabel', background='#001f3f', foreground='#FFD700', font=('Helvetica', 14), relief=tk.RAISED)
        style.configure('TEntry', font=('Helvetica', 14), relief=tk.SUNKEN)
        style.configure('TNotebook', background='#001f3f')
        style.configure('TNotebook.Tab', background='#4CAF50', foreground='white', font=('Helvetica', 14, 'bold'))

        main_frame = ttk.Frame(self.canvas, style='TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill='both', padx=20, pady=20)

        email_frame = ttk.Frame(notebook, relief=tk.RAISED, borderwidth=5)
        proxy_frame = ttk.Frame(notebook, relief=tk.RAISED, borderwidth=5)
        features_frame = ttk.Frame(notebook, relief=tk.RAISED, borderwidth=5)
        sent_emails_frame = ttk.Frame(notebook, relief=tk.RAISED, borderwidth=5)
        help_frame = ttk.Frame(notebook, relief=tk.RAISED, borderwidth=5)

        notebook.add(email_frame, text='E-mail')
        notebook.add(proxy_frame, text='Proxys')
        notebook.add(features_frame, text='Fonctionnalités')
        notebook.add(sent_emails_frame, text='E-mails envoyés')
        notebook.add(help_frame, text='Aide')

        # Onglet E-mail
        ttk.Label(email_frame, text="Lien du serveur SMTP:").pack(pady=10)
        self.smtp_server = ttk.Entry(email_frame, width=60)
        self.smtp_server.pack()
        self.smtp_server.insert(0, "smtp.example.com")  # Valeur par défaut

        ttk.Label(email_frame, text="Adresse e-mail de l'expéditeur:").pack(pady=10)
        self.sender_email = ttk.Entry(email_frame, width=60)
        self.sender_email.pack()

        ttk.Label(email_frame, text="Mot de passe de l'expéditeur:").pack(pady=10)
        self.sender_password = ttk.Entry(email_frame, width=60, show="•")
        self.sender_password.pack()

        ttk.Label(email_frame, text="Fichier combolist:").pack(pady=10)
        self.combolist_frame = ttk.Frame(email_frame)
        self.combolist_frame.pack()
        self.combolist_entry = ttk.Entry(self.combolist_frame, width=50)
        self.combolist_entry.pack(side=tk.LEFT)
        self.browse_button = ttk.Button(self.combolist_frame, text="Parcourir", command=self.browse_combolist)
        self.browse_button.pack(side=tk.LEFT, padx=10)
        self.generate_button = ttk.Button(self.combolist_frame, text="Générer", command=self.generate_combolist)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        ttk.Label(email_frame, text="Sujet:").pack(pady=10)
        self.subject = ttk.Entry(email_frame, width=60)
        self.subject.pack()

        ttk.Label(email_frame, text="Message:").pack(pady=10)
        self.message = tk.Text(email_frame, width=60, height=10, relief=tk.SUNKEN, borderwidth=2)
        self.message.pack()

        ttk.Label(email_frame, text="Messages par seconde:").pack(pady=10)
        self.messages_per_second = ttk.Entry(email_frame, width=10)
        self.messages_per_second.pack()
        self.messages_per_second.insert(0, "1")  # Valeur par défaut

        self.send_button = ttk.Button(email_frame, text="Envoyer", command=self.start_sending)
        self.send_button.pack(pady=20)
        
        self.stop_button = ttk.Button(email_frame, text="Arrêter", command=self.stop_sending, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Onglet Proxys
        ttk.Label(proxy_frame, text="Liste de proxys (optionnel):").pack(pady=10)
        self.proxy_text = tk.Text(proxy_frame, width=60, height=15, relief=tk.SUNKEN, borderwidth=2)
        self.proxy_text.pack()
        ttk.Label(proxy_frame, text="Format: ip:port, un par ligne").pack(pady=10)

        # Onglet Fonctionnalités
        ttk.Label(features_frame, text="Mes réseaux sociaux:", font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        social_networks = [
            ("GitHub", "https://github.com/Nyxosv16"),
            ("Tiktok", "https://www.tiktok.com/@k0560173729"),
            ("Discord", "nyxosv19")
        ]

        for network, url in social_networks:
            link = ttk.Label(features_frame, text=f"{network}: {url}", cursor="hand2", foreground="blue")
            link.pack(pady=5)
            link.bind("<Button-1>", lambda e, url=url: webbrowser.open(url))

        # Onglet E-mails envoyés
        self.sent_emails_text = tk.Text(sent_emails_frame, width=80, height=20, relief=tk.SUNKEN, borderwidth=2)
        self.sent_emails_text.pack(pady=10)
        ttk.Label(sent_emails_frame, text="Liste des e-mails envoyés").pack()

        # Onglet Aide
        ttk.Label(help_frame, text="Instructions d'utilisation:", font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Création d'un frame pour les colonnes
        instructions_frame = ttk.Frame(help_frame)
        instructions_frame.pack(pady=10)

        # Colonne 1
        col1 = ttk.Frame(instructions_frame)
        col1.pack(side=tk.LEFT, padx=10)

        ttk.Label(col1, text="Étape 1:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(col1, text="Remplissez les informations du serveur SMTP, de l'expéditeur et du fichier combolist.", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=5)

        ttk.Label(col1, text="Étape 2:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(col1, text="Entrez le sujet et le message de l'e-mail.", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=5)

        ttk.Label(col1, text="Étape 3:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(col1, text="Optionnel: Ajoutez une liste de proxys.", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=5)

        # Colonne 2
        col2 = ttk.Frame(instructions_frame)
        col2.pack(side=tk.LEFT, padx=10)

        ttk.Label(col2, text="Étape 4:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(col2, text="Cliquez sur 'Envoyer' pour commencer l'envoi des e-mails.", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=5)

        ttk.Label(col2, text="Étape 5:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(col2, text="Cliquez sur 'Arrêter' pour arrêter l'envoi des e-mails.", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=5)

        ttk.Label(col2, text="Étape 6:", font=('Helvetica', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(col2, text="Consultez l'onglet 'E-mails envoyés' pour voir la liste des e-mails envoyés.", wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=5)

    def browse_combolist(self):
        filename = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
        if filename:
            self.combolist_entry.delete(0, tk.END)
            self.combolist_entry.insert(0, filename)

    def generate_combolist(self):
        noms = ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent"]
        prenoms = ["Jean", "Pierre", "Michel", "Philippe", "Alain", "Jacques", "Bernard", "Claude", "Daniel", "Christian"]
        domaines = ["gmail.com", "proton.me", "hotmail.com"]
        combolist = [f"{prenom}.{nom}@{random.choice(domaines)}" for nom in noms for prenom in prenoms]
        
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if filename:
            with open(filename, 'w') as file:
                file.write("\n".join(combolist))
            self.combolist_entry.delete(0, tk.END)
            self.combolist_entry.insert(0, filename)
            messagebox.showinfo("Succès", "Combolist générée avec succès.")

    def start_sending(self):
        self.stop_sending = False
        self.send_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.send_emails, daemon=True).start()

    def stop_sending(self):
        self.stop_sending = True
        self.send_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def send_emails(self):
        smtp_server = self.smtp_server.get()
        sender_email = self.sender_email.get()
        sender_password = self.sender_password.get()
        subject = self.subject.get()
        message_body = self.message.get("1.0", tk.END)
        combolist_file = self.combolist_entry.get()
        messages_per_second = float(self.messages_per_second.get())
        proxy_list = self.proxy_text.get("1.0", tk.END).strip().split("\n")

        if not all([smtp_server, sender_email, sender_password, subject, message_body, combolist_file]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            self.send_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            return

        try:
            if not os.path.exists(combolist_file):
                raise FileNotFoundError(f"Le fichier {combolist_file} n'existe pas.")
            
            with open(combolist_file, 'r') as file:
                emails = file.readlines()
            
            server = smtplib.SMTP(smtp_server, 587)
            server.starttls()
            server.login(sender_email, sender_password)

            sent_count = 0
            for email in emails:
                if self.stop_sending:
                    break
                
                email = email.strip()
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(message_body, 'plain'))

                if proxy_list:
                    proxy = random.choice(proxy_list)
                    server.set_debuglevel(1)
                    server.connect(proxy.split(":")[0], int(proxy.split(":")[1]))

                server.send_message(msg)
                sent_count += 1
                self.sent_emails_text.insert(tk.END, f"E-mail envoyé à: {email}\n")
                self.sent_emails_text.see(tk.END)
                self.master.update()
                
                time.sleep(1 / messages_per_second)

            server.quit()
            messagebox.showinfo("Succès", f"{sent_count} e-mails ont été envoyés avec succès.")
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", f"Erreur : {str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")
        finally:
            self.send_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpammerApp(root)
    root.mainloop()
