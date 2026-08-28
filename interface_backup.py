import customtkinter as ctk

# Configuração da aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Janela principal
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
# TELA INICIAL
# ==================================================

def tela_inicial():
    limpar_conteudo()

    titulo = ctk.CTkLabel(
        area_conteudo,
        text="Bem-vindo ao SIGOA",
        font=("Arial", 30, "bold")
    )
    titulo.pack(pady=(100, 15))

    texto = ctk.CTkLabel(
        area_conteudo,
        text="Sistema Integrado de Gestão para Oficina Automotiva",
        font=("Arial", 16)
    )
    texto.pack()

    descricao = ctk.CTkLabel(
        area_conteudo,
        text="Utilize o menu ao lado para acessar as funcionalidades do sistema.",
        font=("Arial", 14)
    )
    descricao.pack(pady=20)


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

    nome = ctk.CTkEntry(
        formulario,
        placeholder_text="Nome *",
        width=430,
        height=40
    )
    nome.pack(pady=(25, 8))

    cpf = ctk.CTkEntry(
        formulario,
        placeholder_text="CPF *",
        width=430,
        height=40
    )
    cpf.pack(pady=8)

    telefone = ctk.CTkEntry(
        formulario,
        placeholder_text="Telefone *",
        width=430,
        height=40
    )
    telefone.pack(pady=8)

    email = ctk.CTkEntry(
        formulario,
        placeholder_text="E-mail",
        width=430,
        height=40
    )
    email.pack(pady=8)

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

    def validar_cliente():
        if nome.get() == "" or cpf.get() == "" or telefone.get() == "":
            mensagem.configure(
                text="⚠ Preencha Nome, CPF e Telefone."
            )
        else:
            mensagem.configure(
                text="✓ Cliente cadastrado com sucesso!"
            )

            nome.delete(0, "end")
            cpf.delete(0, "end")
            telefone.delete(0, "end")
            email.delete(0, "end")

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

    veiculo = ctk.CTkEntry(
        formulario,
        placeholder_text="Veículo *",
        width=450,
        height=40
    )
    veiculo.pack(pady=(25, 8))

    descricao = ctk.CTkEntry(
        formulario,
        placeholder_text="Descrição do serviço *",
        width=450,
        height=40
    )
    descricao.pack(pady=8)

    pecas = ctk.CTkEntry(
        formulario,
        placeholder_text="Peças utilizadas",
        width=450,
        height=40
    )
    pecas.pack(pady=8)

    valor = ctk.CTkEntry(
        formulario,
        placeholder_text="Valor do serviço",
        width=450,
        height=40
    )
    valor.pack(pady=8)

    status = ctk.CTkComboBox(
        formulario,
        values=[
            "Aguardando",
            "Em andamento",
            "Concluído"
        ],
        width=450,
        height=40
    )
    status.set("Selecione o status")
    status.pack(pady=8)

    mensagem_servico = ctk.CTkLabel(
        formulario,
        text="",
        font=("Arial", 13)
    )
    mensagem_servico.pack(pady=5)

    def validar_servico():
        if veiculo.get() == "" or descricao.get() == "":
            mensagem_servico.configure(
                text="⚠ Preencha o veículo e a descrição do serviço."
            )
        else:
            mensagem_servico.configure(
                text="✓ Serviço registrado com sucesso!"
            )

            veiculo.delete(0, "end")
            descricao.delete(0, "end")
            pecas.delete(0, "end")
            valor.delete(0, "end")
            status.set("Selecione o status")

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

logo = ctk.CTkLabel(
    menu,
    text="SIGOA",
    font=("Arial", 30, "bold")
)
logo.pack(pady=(40, 5))

subtitulo = ctk.CTkLabel(
    menu,
    text="Gestão de Oficina",
    font=("Arial", 14)
)
subtitulo.pack(pady=(0, 40))

botao_inicio = ctk.CTkButton(
    menu,
    text="Início",
    width=180,
    height=45,
    command=tela_inicial
)
botao_inicio.pack(pady=10)

botao_clientes = ctk.CTkButton(
    menu,
    text="Clientes",
    width=180,
    height=45,
    command=tela_cliente
)
botao_clientes.pack(pady=10)

botao_servicos = ctk.CTkButton(
    menu,
    text="Serviços",
    width=180,
    height=45,
    command=tela_servico
)
botao_servicos.pack(pady=10)

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

# Mostrar tela inicial
tela_inicial()

# Iniciar programa
janela.mainloop()