import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("SIGOA - Gestão de Oficina")
janela.geometry("1000x650")

def limpar_conteudo():
    for item in area_conteudo.winfo_children():
        item.destroy()

def criar_titulo(texto, pady=(40, 20)):
    titulo = ctk.CTkLabel(
        area_conteudo,
        text=texto,
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=pady)

def criar_formulario(largura, altura):
    formulario = ctk.CTkFrame(
        area_conteudo,
        width=largura,
        height=altura
    )
    formulario.pack()
    formulario.pack_propagate(False)
    return formulario

def criar_campo(formulario, texto, largura, pady=8):
    campo = ctk.CTkEntry(
        formulario,
        placeholder_text=texto,
        width=largura,
        height=40
    )
    campo.pack(pady=pady)
    return campo

def criar_botao(formulario, texto, comando):
    botao = ctk.CTkButton(
        formulario,
        text=texto,
        width=220,
        height=40,
        command=comando
    )
    botao.pack(pady=10)
    return botao

def limpar_campos(*campos):
    for campo in campos:
        campo.delete(0, "end")

def tela_cliente():
    limpar_conteudo()
    criar_titulo("Cadastro de Cliente")

    formulario = criar_formulario(550, 480)

    nome = criar_campo(formulario, "Nome *", 430, (40, 8))
    telefone = criar_campo(formulario, "Telefone *", 430)
    endereco = criar_campo(formulario, "Endereço *", 430)

    ctk.CTkLabel(
        formulario,
        text="* Campos obrigatórios"
    ).pack(pady=(8, 2))

    mensagem = ctk.CTkLabel(
        formulario,
        text="",
        font=("Arial", 13)
    )
    mensagem.pack(pady=5)

    def validar_cliente():
        nome_valor = nome.get().strip()
        telefone_valor = telefone.get().strip()
        endereco_valor = endereco.get().strip()

        if not nome_valor or not telefone_valor or not endereco_valor:
            mensagem.configure(
                text="⚠ Preencha Nome, Telefone e Endereço."
            )
            return

        try:
            conexao = sqlite3.connect("oficina.db")
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO clientes (nome, telefone, endereco)
                VALUES (?, ?, ?)
                """,
                (nome_valor, telefone_valor, endereco_valor)
            )

            conexao.commit()
            conexao.close()

            mensagem.configure(
                text="✓ Cliente cadastrado com sucesso!"
            )
            limpar_campos(nome, telefone, endereco)

        except sqlite3.Error as erro:
            mensagem.configure(
                text=f"⚠ Erro ao cadastrar cliente: {erro}"
            )

    criar_botao(formulario, "Cadastrar Cliente", validar_cliente)

def tela_servico():
    limpar_conteudo()
    criar_titulo("Registro de Serviço", (35, 20))

    formulario = criar_formulario(570, 520)

    veiculo_id = criar_campo(formulario, "ID do veículo *", 450, (25, 8))
    descricao = criar_campo(formulario, "Descrição do serviço *", 450)
    valor = criar_campo(formulario, "Valor do serviço", 450)
    data = criar_campo(formulario, "Data de entrada *", 450)
    quilometros = criar_campo(formulario, "Quilometragem *", 450)

    mensagem_servico = ctk.CTkLabel(
        formulario,
        text="",
        font=("Arial", 13)
    )
    mensagem_servico.pack(pady=5)

    def validar_servico():
        veiculo_id_valor = veiculo_id.get().strip()
        descricao_valor = descricao.get().strip()
        valor_valor = valor.get().strip()
        data_valor = data.get().strip()
        quilometros_valor = quilometros.get().strip()

        if (
            not veiculo_id_valor
            or not descricao_valor
            or not data_valor
            or not quilometros_valor
        ):
            mensagem_servico.configure(
                text="⚠ Preencha os campos obrigatórios."
            )
            return

        try:
            veiculo_id_numero = int(veiculo_id_valor)
            quilometros_numero = int(quilometros_valor)
            valor_numero = float(valor_valor) if valor_valor else 0

            conexao = sqlite3.connect("oficina.db")
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO servicos
                (descricao, valor, data, quilometros, veiculo_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    descricao_valor,
                    valor_numero,
                    data_valor,
                    quilometros_numero,
                    veiculo_id_numero
                )
            )

            conexao.commit()
            conexao.close()

            mensagem_servico.configure(
                text="✓ Serviço registrado com sucesso!"
            )
            limpar_campos(
                veiculo_id,
                descricao,
                valor,
                data,
                quilometros
            )

        except ValueError:
            mensagem_servico.configure(
                text="⚠ ID do veículo, valor e quilometragem devem ser números."
            )

        except sqlite3.Error as erro:
            mensagem_servico.configure(
                text=f"⚠ Erro ao registrar serviço: {erro}"
            )

    criar_botao(formulario, "Registrar Serviço", validar_servico)

menu = ctk.CTkFrame(
    janela,
    width=230,
    corner_radius=0
)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

ctk.CTkLabel(
    menu,
    text="SIGOA",
    font=("Arial", 30, "bold")
).pack(pady=(40, 5))

ctk.CTkLabel(
    menu,
    text="Gestão de Oficina",
    font=("Arial", 14)
).pack(pady=(0, 40))

for texto, comando in (
    ("Clientes", tela_cliente),
    ("Serviços", tela_servico)
):
    ctk.CTkButton(
        menu,
        text=texto,
        width=180,
        height=45,
        command=comando
    ).pack(pady=10)

ctk.CTkButton(
    menu,
    text="Sair",
    width=180,
    height=40,
    command=janela.destroy
).pack(side="bottom", pady=30)

area_conteudo = ctk.CTkFrame(
    janela,
    corner_radius=0,
    fg_color="transparent"
)
area_conteudo.pack(
    side="right",
    expand=True,
    fill="both"
)

tela_cliente()
janela.mainloop()
