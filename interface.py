import customtkinter as ctk
import sqlite3
import clientes
import veiculos
import servicos

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# --- PALETA SIGOA ---
BG = "#F5F3FF"
SIDEBAR = "#29256F"
SIDEBAR_HOVER = "#5146C8"
PRIMARY = "#5B50D6"
PRIMARY_HOVER = "#473DB7"
CARD = "#FFFFFF"
TEXT = "#17153B"
MUTED = "#77738F"
BORDER = "#E7E3F5"
SOFT = "#EFECFF"
SUCCESS = "#22A06B"
DANGER = "#D94B59"

janela = ctk.CTk()
janela.title("SIGOA - Gestão de Oficina")
janela.geometry("1360x820")
janela.minsize(1180, 700)
janela.configure(fg_color=BG)


def conectar():
    return sqlite3.connect("oficina.db")


def limpar_conteudo():
    for item in area_conteudo.winfo_children():
        item.destroy()


def titulo(texto):
    cab = ctk.CTkFrame(area_conteudo, fg_color="transparent")
    cab.pack(fill="x", padx=30, pady=(25, 12))
    ctk.CTkLabel(cab, text=texto, font=("Segoe UI", 27, "bold"),
                 text_color=TEXT, anchor="w").pack(fill="x")
    ctk.CTkLabel(cab, text="Gerencie as informações da oficina de forma simples e eficiente.",
                 font=("Segoe UI", 12), text_color=MUTED, anchor="w").pack(fill="x", pady=(3,0))


def formulario(altura=560):
    frame = ctk.CTkScrollableFrame(area_conteudo, width=760, height=altura,
                                   fg_color=CARD, corner_radius=18,
                                   border_width=1, border_color=BORDER)
    frame.pack(padx=30, pady=(4, 28), fill="both", expand=True)
    return frame


def campo(pai, texto, largura=500):
    item = ctk.CTkEntry(pai, placeholder_text=texto, width=largura, height=44,
                        corner_radius=10, border_color=BORDER, fg_color="#FAF9FF",
                        text_color=TEXT, placeholder_text_color="#9B97AE",
                        font=("Segoe UI", 13))
    item.pack(pady=7)
    return item


def botao(pai, texto, comando, largura=210):
    item = ctk.CTkButton(pai, text=texto, command=comando, width=largura, height=42,
                         corner_radius=10, fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                         font=("Segoe UI", 13, "bold"))
    item.pack(pady=8)
    return item


def mensagem(pai):
    item = ctk.CTkLabel(pai, text="", font=("Segoe UI", 12), text_color=MUTED)
    item.pack(pady=5)
    return item


def limpar_campos(*campos):
    for item in campos:
        item.delete(0, "end")


def tabela_texto(pai, cabecalho):
    ctk.CTkLabel(pai, text=cabecalho, font=("Consolas", 12, "bold"),
                 text_color=TEXT, anchor="w").pack(fill="x", padx=18, pady=(12, 4))
    caixa = ctk.CTkTextbox(pai, width=680, height=220, font=("Consolas", 12),
                           fg_color="#FAF9FF", text_color=TEXT, corner_radius=10,
                           border_width=1, border_color=BORDER)
    caixa.pack(padx=18, pady=(0, 10), fill="both", expand=True)
    return caixa


def preencher_resultado(caixa, linhas):
    caixa.delete("1.0", "end")
    if not linhas:
        caixa.insert("end", "Nenhum registro encontrado.")
        return
    for linha in linhas:
        caixa.insert("end", " | ".join(str(v) for v in linha) + "\n")


# CLIENTES

def tela_cliente():
    limpar_conteudo()
    titulo("Clientes")
    f = formulario()
    nome = campo(f, "Nome *")
    telefone = campo(f, "Telefone *")
    endereco = campo(f, "Endereço *")
    msg = mensagem(f)

    def cadastrar():
        n, t, e = nome.get().strip(), telefone.get().strip(), endereco.get().strip()
        if not n or not t or not e:
            msg.configure(text="⚠ Preencha Nome, Telefone e Endereço.")
            return
        try:
            clientes.cadastrar_cliente(n, t, e)
            msg.configure(text="✓ Cliente cadastrado com sucesso!")
            limpar_campos(nome, telefone, endereco)
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Cadastrar Cliente", cadastrar)


def tela_consultar_clientes():
    limpar_conteudo()
    titulo("Consultar Clientes")
    f = formulario()
    cliente_id = campo(f, "ID do cliente (deixe vazio para listar todos)")
    caixa = tabela_texto(f, "ID | NOME | TELEFONE | ENDEREÇO")
    msg = mensagem(f)

    def consultar():
        try:
            valor = cliente_id.get().strip()
            if valor:
                registro = clientes.buscar_cliente(int(valor))
                preencher_resultado(caixa, [registro] if registro else [])
            else:
                preencher_resultado(caixa, clientes.listar_clientes())
            msg.configure(text="")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro na consulta: {erro}")

    botao(f, "Consultar", consultar)


def tela_editar_cliente():
    limpar_conteudo()
    titulo("Atualizar / Excluir Cliente")
    f = formulario()
    cliente_id = campo(f, "ID do cliente *")
    nome = campo(f, "Novo nome")
    telefone = campo(f, "Novo telefone")
    endereco = campo(f, "Novo endereço")
    msg = mensagem(f)

    def atualizar():
        try:
            i = int(cliente_id.get().strip())
            if not nome.get().strip() or not telefone.get().strip() or not endereco.get().strip():
                msg.configure(text="⚠ Informe todos os novos dados.")
                return
            clientes.atualizar_cliente(i, nome.get().strip(), telefone.get().strip(), endereco.get().strip())
            msg.configure(text="✓ Solicitação de atualização realizada.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    def excluir():
        try:
            clientes.excluir_cliente(int(cliente_id.get().strip()))
            msg.configure(text="✓ Solicitação de exclusão realizada.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Atualizar Cliente", atualizar)
    botao(f, "Excluir Cliente", excluir)


# VEÍCULOS

def tela_veiculo():
    limpar_conteudo()
    titulo("Cadastro de Veículo")
    f = formulario()
    placa = campo(f, "Placa *")
    modelo = campo(f, "Modelo *")
    ano = campo(f, "Ano *")
    cliente_id = campo(f, "ID do cliente *")
    msg = mensagem(f)

    def cadastrar():
        p, m, a, c = placa.get().strip(), modelo.get().strip(), ano.get().strip(), cliente_id.get().strip()
        if not p or not m or not a or not c:
            msg.configure(text="⚠ Preencha todos os campos.")
            return
        try:
            veiculos.cadastrar_veiculo(p, m, int(a), int(c))
            msg.configure(text="✓ Veículo cadastrado com sucesso!")
            limpar_campos(placa, modelo, ano, cliente_id)
        except ValueError:
            msg.configure(text="⚠ Ano e ID do cliente devem ser números.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Cadastrar Veículo", cadastrar)


def tela_consultar_veiculos():
    limpar_conteudo()
    titulo("Consultar Veículos")
    f = formulario()
    veiculo_id = campo(f, "ID do veículo (deixe vazio para listar todos)")
    caixa = tabela_texto(f, "ID | PLACA | MODELO | ANO | CLIENTE")
    msg = mensagem(f)

    def consultar():
        try:
            valor = veiculo_id.get().strip()
            if valor:
                registro = veiculos.buscar_veiculo(int(valor))
                preencher_resultado(caixa, [registro] if registro else [])
            else:
                preencher_resultado(caixa, veiculos.listar_veiculos())
            msg.configure(text="")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro na consulta: {erro}")

    botao(f, "Consultar", consultar)


def tela_editar_veiculo():
    limpar_conteudo()
    titulo("Atualizar / Excluir Veículo")
    f = formulario()
    veiculo_id = campo(f, "ID do veículo *")
    placa = campo(f, "Nova placa")
    modelo = campo(f, "Novo modelo")
    ano = campo(f, "Novo ano")
    cliente_id = campo(f, "Novo ID do cliente")
    msg = mensagem(f)

    def atualizar():
        try:
            veiculos.atualizar_veiculo(
                int(veiculo_id.get().strip()), placa.get().strip(), modelo.get().strip(),
                int(ano.get().strip()), int(cliente_id.get().strip())
            )
            msg.configure(text="✓ Solicitação de atualização realizada.")
        except ValueError:
            msg.configure(text="⚠ ID, ano e ID do cliente devem ser números.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    def excluir():
        try:
            veiculos.excluir_veiculo(int(veiculo_id.get().strip()))
            msg.configure(text="✓ Solicitação de exclusão realizada.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Atualizar Veículo", atualizar)
    botao(f, "Excluir Veículo", excluir)


# SERVIÇOS

def tela_servico():
    limpar_conteudo()
    titulo("Registro de Serviço")
    f = formulario()
    veiculo_id = campo(f, "ID do veículo *")
    descricao = campo(f, "Descrição do serviço *")
    valor = campo(f, "Valor do serviço")
    data = campo(f, "Data de entrada *")
    quilometros = campo(f, "Quilometragem *")
    msg = mensagem(f)

    def cadastrar():
        vi, d, v, dt, q = [x.get().strip() for x in (veiculo_id, descricao, valor, data, quilometros)]
        if not vi or not d or not dt or not q:
            msg.configure(text="⚠ Preencha os campos obrigatórios.")
            return
        try:
            vi_num, q_num = int(vi), int(q)
            v_num = float(v.replace(",", ".")) if v else 0
            if veiculos.buscar_veiculo(vi_num) is None:
                msg.configure(text="⚠ Veículo não encontrado.")
                return
            servicos.cadastrar_servico(d, v_num, dt, q_num, vi_num)
            msg.configure(text="✓ Serviço registrado com sucesso!")
            limpar_campos(veiculo_id, descricao, valor, data, quilometros)
        except ValueError:
            msg.configure(text="⚠ ID, valor e quilometragem devem ser números.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Registrar Serviço", cadastrar)


def tela_consultar_servicos():
    limpar_conteudo()
    titulo("Consultar Serviços")
    f = formulario()
    servico_id = campo(f, "ID do serviço (deixe vazio para listar todos)")
    caixa = tabela_texto(f, "ID | DESCRIÇÃO | VALOR | DATA | KM | VEÍCULO")
    msg = mensagem(f)

    def consultar():
        try:
            valor_id = servico_id.get().strip()
            if valor_id:
                registro = servicos.buscar_servico(int(valor_id))
                preencher_resultado(caixa, [registro] if registro else [])
            else:
                preencher_resultado(caixa, servicos.listar_servicos())
            msg.configure(text="")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro na consulta: {erro}")

    botao(f, "Consultar", consultar)


def tela_editar_servico():
    limpar_conteudo()
    titulo("Atualizar / Excluir Serviço")
    f = formulario()
    servico_id = campo(f, "ID do serviço *")
    descricao = campo(f, "Nova descrição")
    valor = campo(f, "Novo valor")
    data = campo(f, "Nova data")
    quilometros = campo(f, "Nova quilometragem")
    veiculo_id = campo(f, "Novo ID do veículo")
    msg = mensagem(f)

    def atualizar():
        try:
            servicos.atualizar_servico(
                int(servico_id.get().strip()), descricao.get().strip(),
                float(valor.get().strip().replace(",", ".")), data.get().strip(),
                int(quilometros.get().strip()), int(veiculo_id.get().strip())
            )
            msg.configure(text="✓ Solicitação de atualização realizada.")
        except ValueError:
            msg.configure(text="⚠ IDs, valor e quilometragem devem ser números.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    def excluir():
        try:
            servicos.excluir_servico(int(servico_id.get().strip()))
            msg.configure(text="✓ Solicitação de exclusão realizada.")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Atualizar Serviço", atualizar)
    botao(f, "Excluir Serviço", excluir)


# PEÇAS E ORÇAMENTOS - interface usando as tabelas documentadas

def tela_peca():
    limpar_conteudo()
    titulo("Cadastro de Peça")
    f = formulario()
    nome = campo(f, "Nome da peça *")
    quantidade = campo(f, "Quantidade *")
    valor = campo(f, "Valor *")
    fornecedor = campo(f, "Fornecedor *")
    msg = mensagem(f)

    def cadastrar():
        try:
            n, q, v, fo = nome.get().strip(), quantidade.get().strip(), valor.get().strip(), fornecedor.get().strip()
            if not n or not q or not v or not fo:
                msg.configure(text="⚠ Preencha todos os campos.")
                return
            with conectar() as con:
                con.execute("INSERT INTO pecas (nome, quantidade, valor, fornecedor) VALUES (?, ?, ?, ?)",
                            (n, int(q), float(v.replace(",", ".")), fo))
            msg.configure(text="✓ Peça cadastrada com sucesso!")
            limpar_campos(nome, quantidade, valor, fornecedor)
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Cadastrar Peça", cadastrar)


def tela_orcamento():
    limpar_conteudo()
    titulo("Cadastro de Orçamento")
    f = formulario()
    data = campo(f, "Data *")
    valor_total = campo(f, "Valor total *")
    veiculo_id = campo(f, "ID do veículo *")
    msg = mensagem(f)

    def cadastrar():
        try:
            dt, v, vi = data.get().strip(), valor_total.get().strip(), veiculo_id.get().strip()
            if not dt or not v or not vi:
                msg.configure(text="⚠ Preencha todos os campos.")
                return
            vi_num = int(vi)
            if veiculos.buscar_veiculo(vi_num) is None:
                msg.configure(text="⚠ Veículo não encontrado.")
                return
            with conectar() as con:
                con.execute("INSERT INTO orcamentos (data, valor_total, veiculo_id) VALUES (?, ?, ?)",
                            (dt, float(v.replace(",", ".")), vi_num))
            msg.configure(text="✓ Orçamento cadastrado com sucesso!")
            limpar_campos(data, valor_total, veiculo_id)
        except Exception as erro:
            msg.configure(text=f"⚠ Erro: {erro}")

    botao(f, "Cadastrar Orçamento", cadastrar)


def tela_consulta_geral():
    limpar_conteudo()
    titulo("Consulta Geral")
    f = formulario()
    caixa = tabela_texto(f, "ORÇAMENTOS: ID | DATA | VALOR | VEÍCULO | PLACA | CLIENTE")
    msg = mensagem(f)

    def consultar():
        try:
            with conectar() as con:
                linhas = con.execute("""
                    SELECT o.id, o.data, o.valor_total, v.id, v.placa, c.nome
                    FROM orcamentos o
                    JOIN veiculos v ON v.id = o.veiculo_id
                    JOIN clientes c ON c.id = v.cliente_id
                    ORDER BY o.id
                """).fetchall()
            preencher_resultado(caixa, linhas)
            msg.configure(text="")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro na consulta: {erro}")

    botao(f, "Consultar Orçamentos", consultar)


# MENU / DASHBOARD
menu = ctk.CTkScrollableFrame(janela, width=235, corner_radius=0, fg_color=SIDEBAR)
menu.pack(side="left", fill="y")

logo = ctk.CTkFrame(menu, fg_color="transparent")
logo.pack(fill="x", padx=18, pady=(25, 18))
ctk.CTkLabel(logo, text="🚘  SIGOA", font=("Segoe UI", 28, "bold"),
             text_color="white").pack(anchor="w")
ctk.CTkLabel(logo, text="Gestão de Oficina", font=("Segoe UI", 12),
             text_color="#C9C5F2").pack(anchor="w", padx=4)

def menu_secao(texto):
    ctk.CTkLabel(menu, text=texto.upper(), font=("Segoe UI", 10, "bold"),
                 text_color="#B7B2E3").pack(anchor="w", padx=22, pady=(13, 4))

def menu_btn(texto, comando):
    ctk.CTkButton(menu, text=texto, command=comando, width=200, height=35,
                  anchor="w", corner_radius=9, fg_color="transparent",
                  hover_color=SIDEBAR_HOVER, text_color="white",
                  font=("Segoe UI", 12)).pack(padx=12, pady=2)

area_conteudo = ctk.CTkFrame(janela, corner_radius=0, fg_color=BG)
area_conteudo.pack(side="right", expand=True, fill="both")

def consultar_contagem(tabela):
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {tabela}")
        valor = cur.fetchone()[0]
        con.close()
        return valor
    except Exception:
        return 0

def card_dashboard(pai, titulo_card, valor, icone):
    card = ctk.CTkFrame(pai, fg_color=CARD, corner_radius=17,
                        border_width=1, border_color=BORDER)
    card.grid_columnconfigure(1, weight=1)
    ctk.CTkLabel(card, text=icone, width=48, height=48, corner_radius=24,
                 fg_color=SOFT, text_color=PRIMARY,
                 font=("Segoe UI Emoji", 22)).grid(row=0, column=0, rowspan=2, padx=(18,12), pady=18)
    ctk.CTkLabel(card, text=titulo_card, font=("Segoe UI", 12),
                 text_color=MUTED, anchor="w").grid(row=0, column=1, sticky="sw", pady=(14,0))
    ctk.CTkLabel(card, text=str(valor), font=("Segoe UI", 25, "bold"),
                 text_color=TEXT, anchor="w").grid(row=1, column=1, sticky="nw", pady=(0,14))
    return card

def tela_inicio():
    limpar_conteudo()

    cab = ctk.CTkFrame(area_conteudo, fg_color="transparent")
    cab.pack(fill="x", padx=30, pady=(25, 14))
    esquerda = ctk.CTkFrame(cab, fg_color="transparent")
    esquerda.pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(esquerda, text="Bem-vindo ao SIGOA! 👋",
                 font=("Segoe UI", 28, "bold"), text_color=TEXT).pack(anchor="w")
    ctk.CTkLabel(esquerda, text="Aqui você gerencia sua oficina de forma simples e eficiente.",
                 font=("Segoe UI", 12), text_color=MUTED).pack(anchor="w", pady=(3,0))
    ctk.CTkEntry(cab, placeholder_text="⌕  Buscar no sistema...", width=285, height=40,
                 corner_radius=20, fg_color=CARD, border_color=BORDER).pack(side="right", padx=(12,0))

    cards = ctk.CTkFrame(area_conteudo, fg_color="transparent")
    cards.pack(fill="x", padx=30, pady=(0,14))
    for i in range(4):
        cards.grid_columnconfigure(i, weight=1)

    dados = [
        ("Total de Clientes", consultar_contagem("clientes"), "👥"),
        ("Total de Veículos", consultar_contagem("veiculos"), "🚗"),
        ("Serviços", consultar_contagem("servicos"), "🔧"),
        ("Orçamentos", consultar_contagem("orcamentos"), "📋"),
    ]
    for i, (nome, valor, icone) in enumerate(dados):
        card_dashboard(cards, nome, valor, icone).grid(row=0, column=i, sticky="nsew",
                                                       padx=(0 if i == 0 else 6, 0 if i == 3 else 6))

    corpo = ctk.CTkFrame(area_conteudo, fg_color="transparent")
    corpo.pack(fill="both", expand=True, padx=30, pady=(0,28))
    corpo.grid_columnconfigure(0, weight=2)
    corpo.grid_columnconfigure(1, weight=1)
    corpo.grid_rowconfigure(0, weight=1)

    painel = ctk.CTkFrame(corpo, fg_color=CARD, corner_radius=18,
                          border_width=1, border_color=BORDER)
    painel.grid(row=0, column=0, sticky="nsew", padx=(0,7))
    ctk.CTkLabel(painel, text="Acesso rápido", font=("Segoe UI", 18, "bold"),
                 text_color=TEXT).pack(anchor="w", padx=22, pady=(20,4))
    ctk.CTkLabel(painel, text="Escolha uma operação para começar.",
                 font=("Segoe UI", 12), text_color=MUTED).pack(anchor="w", padx=22)

    grade = ctk.CTkFrame(painel, fg_color="transparent")
    grade.pack(fill="both", expand=True, padx=18, pady=18)
    grade.grid_columnconfigure((0,1), weight=1)

    atalhos = [
        ("👤  Cadastrar cliente", tela_cliente),
        ("🚗  Cadastrar veículo", tela_veiculo),
        ("🔧  Registrar serviço", tela_servico),
        ("📋  Novo orçamento", tela_orcamento),
        ("🔎  Consultar clientes", tela_consultar_clientes),
        ("📊  Consultar orçamentos", tela_consulta_geral),
    ]
    for i, (nome, cmd) in enumerate(atalhos):
        ctk.CTkButton(grade, text=nome, command=cmd, height=58, anchor="w",
                      corner_radius=12, fg_color="#FAF9FF", hover_color=SOFT,
                      text_color=TEXT, border_width=1, border_color=BORDER,
                      font=("Segoe UI", 13, "bold")).grid(row=i//2, column=i%2,
                                                         sticky="ew", padx=6, pady=6)

    resumo = ctk.CTkFrame(corpo, fg_color=CARD, corner_radius=18,
                          border_width=1, border_color=BORDER)
    resumo.grid(row=0, column=1, sticky="nsew", padx=(7,0))
    ctk.CTkLabel(resumo, text="Sistema", font=("Segoe UI", 18, "bold"),
                 text_color=TEXT).pack(anchor="w", padx=22, pady=(20,4))
    ctk.CTkLabel(resumo, text="SIGOA • Gestão de Oficina",
                 font=("Segoe UI", 12), text_color=MUTED).pack(anchor="w", padx=22)
    ctk.CTkFrame(resumo, height=2, fg_color=BORDER).pack(fill="x", padx=22, pady=18)
    ctk.CTkLabel(resumo, text="Clientes  •  Veículos\nServiços  •  Peças\nOrçamentos",
                 justify="left", font=("Segoe UI", 14), text_color=TEXT).pack(anchor="w", padx=22)
    ctk.CTkLabel(resumo, text="\nTodos os módulos continuam ligados\nao mesmo banco de dados do projeto.",
                 justify="left", font=("Segoe UI", 11), text_color=MUTED).pack(anchor="w", padx=22)

menu_btn("⌂   Início", tela_inicio)
menu_secao("Clientes")
menu_btn("＋   Cadastrar", tela_cliente)
menu_btn("⌕   Consultar", tela_consultar_clientes)
menu_btn("✎   Editar", tela_editar_cliente)
menu_secao("Veículos")
menu_btn("＋   Cadastrar", tela_veiculo)
menu_btn("⌕   Consultar", tela_consultar_veiculos)
menu_btn("✎   Editar", tela_editar_veiculo)
menu_secao("Serviços")
menu_btn("＋   Registrar", tela_servico)
menu_btn("⌕   Consultar", tela_consultar_servicos)
menu_btn("✎   Editar", tela_editar_servico)
menu_secao("Estoque")
menu_btn("▣   Peças", tela_peca)
menu_secao("Orçamentos")
menu_btn("＋   Cadastrar", tela_orcamento)
menu_btn("⌕   Consultar", tela_consulta_geral)

ctk.CTkButton(menu, text="Sair", command=janela.destroy, width=200, height=38,
              corner_radius=9, fg_color="#443B9F", hover_color="#5A4ED0",
              font=("Segoe UI", 12, "bold")).pack(padx=12, pady=(25,20))

tela_inicio()
janela.mainloop()
