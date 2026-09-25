import customtkinter as ctk
import sqlite3
import clientes
import veiculos
import servicos
import pecas
import orcamentos

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("SIGOA - Gestão de Oficina")
janela.geometry("1100x700")


def conectar():
    return sqlite3.connect("oficina.db")


def limpar_conteudo():
    for item in area_conteudo.winfo_children():
        item.destroy()


def titulo(texto):
    ctk.CTkLabel(area_conteudo, text=texto, font=("Arial", 26, "bold")).pack(pady=(22, 12))


def formulario(altura=560):
    frame = ctk.CTkScrollableFrame(area_conteudo, width=700, height=altura)
    frame.pack(padx=20, pady=5, fill="both", expand=True)
    return frame


def campo(pai, texto, largura=500):
    item = ctk.CTkEntry(pai, placeholder_text=texto, width=largura, height=38)
    item.pack(pady=6)
    return item


def botao(pai, texto, comando, largura=210):
    item = ctk.CTkButton(pai, text=texto, command=comando, width=largura, height=38)
    item.pack(pady=7)
    return item


def mensagem(pai):
    item = ctk.CTkLabel(pai, text="", font=("Arial", 13))
    item.pack(pady=5)
    return item


def limpar_campos(*campos):
    for item in campos:
        item.delete(0, "end")


def tabela_texto(pai, cabecalho):
    ctk.CTkLabel(pai, text=cabecalho, font=("Courier New", 13, "bold"), anchor="w").pack(fill="x", padx=15, pady=(10, 2))
    caixa = ctk.CTkTextbox(pai, width=680, height=220, font=("Courier New", 13))
    caixa.pack(padx=15, pady=5, fill="both", expand=True)
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
            pecas.cadastrar_peca(n, int(q), float(v.replace(",", ".")), fo)
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
            orcamentos.cadastrar_orcamento(dt, float(v.replace(",", ".")), vi_num)
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
            orcamentos_list = orcamentos.listar_orcamentos()
            preencher_resultado(caixa, orcamentos_list)
            msg.configure(text="")
        except Exception as erro:
            msg.configure(text=f"⚠ Erro na consulta: {erro}")

    botao(f, "Consultar Orçamentos", consultar)


# MENU
menu = ctk.CTkScrollableFrame(janela, width=230, corner_radius=0)
menu.pack(side="left", fill="y")
ctk.CTkLabel(menu, text="SIGOA", font=("Arial", 30, "bold")).pack(pady=(25, 2))
ctk.CTkLabel(menu, text="Gestão de Oficina", font=("Arial", 14)).pack(pady=(0, 20))

opcoes = (
    ("Cadastrar Cliente", tela_cliente),
    ("Consultar Clientes", tela_consultar_clientes),
    ("Editar Clientes", tela_editar_cliente),
    ("Cadastrar Veículo", tela_veiculo),
    ("Consultar Veículos", tela_consultar_veiculos),
    ("Editar Veículos", tela_editar_veiculo),
    ("Registrar Serviço", tela_servico),
    ("Consultar Serviços", tela_consultar_servicos),
    ("Editar Serviços", tela_editar_servico),
    ("Cadastrar Peça", tela_peca),
    ("Cadastrar Orçamento", tela_orcamento),
    ("Consultar Orçamentos", tela_consulta_geral),
)

for texto, comando in opcoes:
    ctk.CTkButton(menu, text=texto, width=190, height=36, command=comando).pack(pady=4)

ctk.CTkButton(menu, text="Sair", width=190, height=36, command=janela.destroy).pack(pady=20)

area_conteudo = ctk.CTkFrame(janela, corner_radius=0, fg_color="transparent")
area_conteudo.pack(side="right", expand=True, fill="both")

tela_cliente()
janela.mainloop()
