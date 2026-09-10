import customtkinter as ctk
import sqlite3


# ==================================================
# CONFIGURAÇÃO DA APARÊNCIA
# ==================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==================================================
# JANELA PRINCIPAL
# ==================================================

janela = ctk.CTk()
janela.title("SIGOA - Gestão de Oficina")
janela.geometry("1000x650")


# ==================================================
# LIMPAR ÁREA DE CONTEÚDO
# ==================================================

def limpar_conteudo():
    for item in area_conteudo.winfo_children():
        item.destroy()


# ==================================================
# TELA DE CADASTRO DE CLIENTE
# ==================================================

def tela_cliente():

    limpar_conteudo()

    titulo = ctk.CTkLabel(
        area_conteudo,
        text="Cadastro de Cliente",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=(40, 20))

    formulario = ctk.CTkFrame(
        area_conteudo,
        width=550,
        height=480
    )
    formulario.pack()
    formulario.pack_propagate(False)

    # Nome
    nome = ctk.CTkEntry(
        formulario,
        placeholder_text="Nome *",
        width=430,
        height=40
    )
    nome.pack(pady=(40, 8))

    # Telefone
    telefone = ctk.CTkEntry(
        formulario,
        placeholder_text="Telefone *",
        width=430,
        height=40
    )
    telefone.pack(pady=8)

    # Endereço
    endereco = ctk.CTkEntry(
        formulario,
        placeholder_text="Endereço *",
        width=430,
        height=40
    )
    endereco.pack(pady=8)

    obrigatorios = ctk.CTkLabel(
        formulario,
        text="* Campos obrigatórios"
    )
    obrigatorios.pack(pady=(8, 2))

    mensagem = ctk.CTkLabel(
        formulario,
        text="",
        font=("Arial", 13)
    )
    mensagem.pack(pady=5)

    # ==================================================
    # FUNÇÃO PARA CADASTRAR CLIENTE
    # ==================================================

    def validar_cliente():

        nome_valor = nome.get().strip()
        telefone_valor = telefone.get().strip()
        endereco_valor = endereco.get().strip()

        if (
            nome_valor == ""
            or telefone_valor == ""
            or endereco_valor == ""
        ):
            mensagem.configure(
                text="⚠ Preencha Nome, Telefone e Endereço."
            )
            return

        try:

            conexao = sqlite3.connect("oficina.db")
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO clientes (nome, telefone, endereco)
                VALUES (?, ?, ?)
            """, (
                nome_valor,
                telefone_valor,
                endereco_valor
            ))

            conexao.commit()
            conexao.close()

            mensagem.configure(
                text="✓ Cliente cadastrado com sucesso!"
            )

            # Limpar campos
            nome.delete(0, "end")
            telefone.delete(0, "end")
            endereco.delete(0, "end")

        except sqlite3.Error as erro:

            mensagem.configure(
                text=f"⚠ Erro ao cadastrar cliente: {erro}"
            )

    # Botão
    botao_cadastrar = ctk.CTkButton(
        formulario,
        text="Cadastrar Cliente",
        width=220,
        height=40,
        command=validar_cliente
    )
    botao_cadastrar.pack(pady=10)


# ==================================================
# TELA DE REGISTRO DE SERVIÇO
# ==================================================

def tela_servico():

    limpar_conteudo()

    titulo = ctk.CTkLabel(
        area_conteudo,
        text="Registro de Serviço",
        font=("Arial", 28, "bold")
    )
    titulo.pack(pady=(35, 20))

    formulario = ctk.CTkFrame(
        area_conteudo,
        width=570,
        height=520
    )
    formulario.pack()
    formulario.pack_propagate(False)

    # ID do veículo
    veiculo_id = ctk.CTkEntry(
        formulario,
        placeholder_text="ID do veículo *",
        width=450,
        height=40
    )
    veiculo_id.pack(pady=(25, 8))

    # Descrição
    descricao = ctk.CTkEntry(
        formulario,
        placeholder_text="Descrição do serviço *",
        width=450,
        height=40
    )
    descricao.pack(pady=8)

    # Valor
    valor = ctk.CTkEntry(
        formulario,
        placeholder_text="Valor do serviço",
        width=450,
        height=40
    )
    valor.pack(pady=8)

    # Data
    data = ctk.CTkEntry(
        formulario,
        placeholder_text="Data de entrada *",
        width=450,
        height=40
    )
    data.pack(pady=8)

    # Quilometragem
    quilometros = ctk.CTkEntry(
        formulario,
        placeholder_text="Quilometragem *",
        width=450,
        height=40
    )
    quilometros.pack(pady=8)

    mensagem_servico = ctk.CTkLabel(
        formulario,
        text="",
        font=("Arial", 13)
    )
    mensagem_servico.pack(pady=5)

    # ==================================================
    # FUNÇÃO PARA REGISTRAR SERVIÇO
    # ==================================================

    def validar_servico():

        veiculo_id_valor = veiculo_id.get().strip()
        descricao_valor = descricao.get().strip()
        valor_valor = valor.get().strip()
        data_valor = data.get().strip()
        quilometros_valor = quilometros.get().strip()

        # Verificar campos obrigatórios
        if (
            veiculo_id_valor == ""
            or descricao_valor == ""
            or data_valor == ""
            or quilometros_valor == ""
        ):
            mensagem_servico.configure(
                text="⚠ Preencha os campos obrigatórios."
            )
            return

        try:

            # Converter números
            veiculo_id_numero = int(veiculo_id_valor)
            quilometros_numero = int(quilometros_valor)

            if valor_valor == "":
                valor_numero = 0
            else:
                valor_numero = float(valor_valor)

            # Conectar ao banco
            conexao = sqlite3.connect("oficina.db")
            cursor = conexao.cursor()

            # Inserir serviço
            cursor.execute("""
                INSERT INTO servicos
                (descricao, valor, data, quilometros, veiculo_id)
                VALUES (?, ?, ?, ?, ?)
            """, (
                descricao_valor,
                valor_numero,
                data_valor,
                quilometros_numero,
                veiculo_id_numero
            ))

            conexao.commit()
            conexao.close()

            mensagem_servico.configure(
                text="✓ Serviço registrado com sucesso!"
            )

            # Limpar campos
            veiculo_id.delete(0, "end")
            descricao.delete(0, "end")
            valor.delete(0, "end")
            data.delete(0, "end")
            quilometros.delete(0, "end")

        except ValueError:

            mensagem_servico.configure(
                text="⚠ ID do veículo, valor e quilometragem devem ser números."
            )

        except sqlite3.Error as erro:

            mensagem_servico.configure(
                text=f"⚠ Erro ao registrar serviço: {erro}"
            )

    # Botão
    botao_registrar = ctk.CTkButton(
        formulario,
        text="Registrar Serviço",
        width=220,
        height=40,
        command=validar_servico
    )
    botao_registrar.pack(pady=10)


# ==================================================
# MENU LATERAL
# ==================================================

menu = ctk.CTkFrame(
    janela,
    width=230,
    corner_radius=0
)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)


# Logo
logo = ctk.CTkLabel(
    menu,
    text="SIGOA",
    font=("Arial", 30, "bold")
)
logo.pack(pady=(40, 5))


# Subtítulo
subtitulo = ctk.CTkLabel(
    menu,
    text="Gestão de Oficina",
    font=("Arial", 14)
)
subtitulo.pack(pady=(0, 40))


# ==================================================
# BOTÃO CLIENTES
# ==================================================

botao_clientes = ctk.CTkButton(
    menu,
    text="Clientes",
    width=180,
    height=45,
    command=tela_cliente
)
botao_clientes.pack(pady=10)


# ==================================================
# BOTÃO SERVIÇOS
# ==================================================

botao_servicos = ctk.CTkButton(
    menu,
    text="Serviços",
    width=180,
    height=45,
    command=tela_servico
)
botao_servicos.pack(pady=10)


# ==================================================
# BOTÃO SAIR
# ==================================================

botao_sair = ctk.CTkButton(
    menu,
    text="Sair",
    width=180,
    height=40,
    command=janela.destroy
)
botao_sair.pack(side="bottom", pady=30)


# ==================================================
# ÁREA PRINCIPAL
# ==================================================

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


# ==================================================
# ABRIR CADASTRO DE CLIENTE AO INICIAR
# ==================================================

tela_cliente()


# ==================================================
# INICIAR PROGRAMA
# ==================================================

janela.mainloop()