import customtkinter as ctk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
import csv
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# E-mail
def enviar_email(nome, email, data, tratamento, pagamento):
    corpo = (
        f"Olá {nome}, sua consulta está agendada para o dia {data}.\n"
        f"Tratamento: {tratamento}\n"
        f"Meio de pagamento: {pagamento}\n\n"
        "Atenciosamente,\nH.P. Estética"
    )
    msg = MIMEText(corpo)
    msg["Subject"] = "Confirmação de Consulta"
    msg["From"] = "H.P. Estética"
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("E-Mail", "(Chave de E-Mail)")
            server.send_message(msg)
        return True
    except Exception as e:
        print("Erro:", e)
        return False

# CSV
def salvar_csv(nome, email, data, tratamento, pagamento):
    arquivo = "consultas.csv"
    existe = os.path.isfile(arquivo)
    with open(arquivo, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["Nome", "E-mail", "Data", "Tratamento", "Pagamento"])
        writer.writerow([nome, email, data, tratamento, pagamento])

# Mostrar/ocultar campo de parcelas
def on_pagamento_change(choice):
    if choice == "Cartão Crédito":
        combo_parcelas.pack(pady=10)
    else:
        combo_parcelas.pack_forget()

# Cadastrar
def cadastrar():
    nome = entry_nome.get()
    email = entry_email.get()
    data = entry_data.get()
    tratamento = combo_tratamento.get()
    detalhes = entry_detalhes.get()
    pagamento = combo_pagamento.get()
    parcelas = combo_parcelas.get() if pagamento == "Cartão Crédito" else ""

    if not nome or not email or not data or not tratamento or not detalhes or not pagamento:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    if pagamento == "Cartão Crédito" and not parcelas:
        messagebox.showerror("Erro", "Informe a quantidade de parcelas!")
        return

    tratamento_completo = f"{tratamento} ({detalhes})"
    pagamento_info = f"{pagamento} ({parcelas}x)" if pagamento == "Cartão Crédito" else pagamento
    sucesso_email = enviar_email(nome, email, data, tratamento_completo, pagamento_info)
    salvar_csv(nome, email, data, tratamento_completo, pagamento_info)

    if sucesso_email:
        messagebox.showinfo("Sucesso", f"Consulta de {nome} cadastrada, e-mail enviado e registro salvo!")
    else:
        messagebox.showwarning("Aviso", f"Consulta de {nome} cadastrada e salva, mas o e-mail não pôde ser enviado.")

# Interface
root = ctk.CTk()
root.title("Cadastro de Pacientes - Clínica de Estética")
root.geometry("520x550")

frame = ctk.CTkFrame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

titulo = ctk.CTkLabel(frame, text="Cadastro de Pacientes", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome do Paciente", width=350, height=35)
entry_nome.pack(pady=10)

entry_email = ctk.CTkEntry(frame, placeholder_text="E-mail do Paciente", width=350, height=35)
entry_email.pack(pady=10)

entry_data = ctk.CTkEntry(frame, placeholder_text="Data da Consulta (DD/MM/AAAA)", width=200, height=35)
entry_data.pack(pady=10)

combo_tratamento = ctk.CTkComboBox(frame, values=["Limpeza de Pele", "Harmonização Facial", "Rinomodelação", "Peeling"], width=220, height=35)
combo_tratamento.pack(pady=10)
combo_tratamento.set("Escolha uma Opção")

entry_detalhes = ctk.CTkEntry(frame, placeholder_text="Detalhes do Procedimento (ex: Melasma, Acne...)", width=350, height=35)
entry_detalhes.pack(pady=10)

combo_pagamento = ctk.CTkComboBox(
    frame,
    values=["Pix", "Dinheiro", "Cartão Débito", "Cartão Crédito", "Boleto"],
    width=220,
    height=35,
    command=on_pagamento_change
)
combo_pagamento.pack(pady=10)
combo_pagamento.set("Escolha uma Opção")

combo_parcelas = ctk.CTkComboBox(
    frame, 
    values=["1", "2", "3", "4", "5", "6"],
    width=100, 
    height=35
)

botao = ctk.CTkButton(frame, text="Cadastrar e Enviar E-mail", command=cadastrar)
botao.pack(pady=20)


root.mainloop()
