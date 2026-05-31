import json
import sqlite3

conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()

def criar_banco_dados():
    cursor.execute("""CREATE TABLE IF NOT EXISTS produtos(
                   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL UNIQUE,
                   categoria TEXT NOT NULL,
                   quantidade INTEGER NOT NULL,
                   status TEXT NOT NULL,
                   valor FLOAT
                   )""")
    conexao.commit()

def inserir_produto_no_banco(produto):
    cursor.execute("""INSERT INTO produtos
                   (nome, categoria, quantidade, status, valor) VALUES
                   (?, ?, ?, ?, ?)""",
                   (produto.nome, produto.categoria, produto.quantidade, produto.status, produto.valor))
    conexao.commit()

def carregar_banco_dados():
    cursor.execute("""SELECT * FROM produtos""")
    produtos_sql = cursor.fetchall()

    if produtos_sql:
        produtos : list[Produto] = []

        for produto in produtos_sql:
            produto_id, nome, categoria, quantidade, status, valor = produto

            produtos.append(Produto(produto_id, nome, categoria, quantidade, status, valor))

    else:
        produtos : list[Produto] = []

    return produtos

def atualizar_banco_dados(produto):
    cursor.execute("""UPDATE produtos
                   SET status = ?, valor = ?
                   WHERE id = ?""",
                   (produto.status, produto.valor, produto.id))

    conexao.commit()

categorias = ['alimentos',
              'bebidas']

class Produto:
    def __init__(self, id, nome, categoria, quantidade, status, valor):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.status = status
        self.valor = valor

    def to_dict(self):
        produto_to_dict = {}

        produto_to_dict['nome'] = self.nome
        produto_to_dict['categoria'] = self.categoria
        produto_to_dict['quantidade'] = self.quantidade
        produto_to_dict['status'] = self.status
        produto_to_dict['valor'] = self.valor

        return produto_to_dict
    
    def from_dict(produto_dict):
        nome_TO = produto_dict['nome']
        categoria_TO = produto_dict['categoria']
        quantidade_TO = produto_dict['quantidade']
        status_TO = produto_dict['status']

        if 'valor' in produto_dict :
            valor_TO = produto_dict['valor']
        else:
            valor_TO = None

        return Produto(nome_TO, categoria_TO, quantidade_TO, status_TO, valor_TO)

    def __str__(self):
        return f'Produto : {self.nome} | Estoque : {self.quantidade}'

    def detalhar_produto(self):
        print(
                f"Detalhes do produto : \n\n"
                f"ID : {self.id}\n"
                f"Produto : {self.nome}\n"
                f"Status : {self.status}\n"
                f"Categoria : {self.categoria}\n"
                f"Quantidade em Estoque : {self.quantidade}"
            )

        if self.valor != None:
            print(f"Valor : R${self.valor}\n")

    def colocar_a_venda(self, valor):
        self.valor = valor
        self.status = 'FS'

        print("Pronto, agora seu produto está a venda :\n\n")
        self.detalhar_produto()

def carregar_dados_json():
    try:
        with open('produtos.json', 'r', encoding='utf-8') as arquivo_produtos:
            produtos_dict_json = json.load(arquivo_produtos)
            produtos: list[Produto] = []
            
            for produto_dict in produtos_dict_json:
                produto_objeto = Produto.from_dict(produto_dict) 

                produtos.append(produto_objeto)

    except (FileNotFoundError, json.JSONDecodeError):
        produtos: list[Produto] = []

    return produtos

def menu():
    opcoes = (1, 2, 3, 4)

    print("=====    MENU    =====\n\n")
    print(
        "Escolha uma opcao :\n\n"
        "1 - Cadastrar produto\n"
        "2 - Ver produtos\n"
        "3 - Vender produto\n"
        "4 - Sair\n"
    )

    while True:
        try:
            opcao_escolhida = int(input("Digite o numero da opcao que voce quer :"))
        except ValueError:
            print("Opcao inválida, tente novamente.")
            continue

        if opcao_escolhida in opcoes:
            return opcao_escolhida

        else:
            print("Opcao inválida, tente novamente.")

def cadastrar_produto():

    while True:
        try:
            quantidade_de_produtos = int(input("Quantos produtos serao adicionados?"))

            if quantidade_de_produtos < 1:
                print("Resposta inválida, tente novamente.")
                continue
            
            break

        except ValueError:
            print("Resposta inválida, tente novamente.")

    for adicao_produto in range(quantidade_de_produtos):

        produto_cancelado = False

        while True:
            produto_nome = input(
                f"Qual é o {adicao_produto + 1}º produto voce irá adicionar?"
            ).lower().strip()

            if produto_nome.replace(" ", "").isalpha() == False:
                print("ERRO, nao inclua números.")
                continue

            elif any(produto_nome == produto.nome for produto in produtos):
                print('Produto já existente.\n\n'
                      'OPCOES :\n\n'
                      '1 - Substituir por outro\n'
                      '2 - Cancelar o cadastro SOMENTE DESTE PRODUTO.')
                
                while True:
                    try:
                        opcao_produto_existente = int(input('Opcao escolhida : '))
                        while opcao_produto_existente != 1 and opcao_produto_existente != 2:
                            print('Opcao inválida, tente novamente.')
                            opcao_produto_existente = int(input('Opcao escolhida : '))

                        break

                    except ValueError:
                        print('Opcao inválida, tente novamente.')
                        continue
                
                if opcao_produto_existente == 1:
                    continue
                
                elif opcao_produto_existente == 2:
                    produto_cancelado = True

            else:
                break

        if produto_cancelado == False:
            while True:
                print(f'Qual é a categoria do produto?\n'
                    f'Opcoes válidas: {categorias} .')
                
                produto_categoria = input('Escolha uma categoria : ').strip().lower()

                if produto_categoria.replace(" ", "").isalpha() == False or produto_categoria not in categorias:
                    print("ERRO, opcao inválida.")
                    continue
                else:
                    break

            while True:
                try:
                    produto_estoque = int(
                        input("Qual é a quantidade dele em estoque atualmente?")
                    )

                    if produto_estoque < 1:
                        print('Quantidade inválida, é necessário que tenha pelo menos 1 produto em estoque.')
                        continue

                    break
                except ValueError:
                    print("ERRO, Digite a quantidade com numeros INTEIROS.")

            produto_status = "NFS"

            produto = Produto(produto_nome,
                produto_categoria,
                produto_estoque,
                produto_status,
                None)

            produtos.append(produto)
            
            inserir_produto_no_banco(produto)

def encontrar_produto():
    while True:
        produto_encontrado = False
        produto_em_uso = None

        produto = input("Digite o NOME ou ID do produto : ").lower().strip()

        busca_por_id = produto.isdigit()

        if busca_por_id:
            produto = int(produto)

            for produto_check in produtos:
                if produto == produto_check.id:
                    produto_encontrado = True
                    produto_em_uso = produto_check

        else:
            for produto_check in produtos:
                if produto == produto_check.nome:
                    produto_encontrado = True
                    produto_em_uso = produto_check

        if produto_encontrado:
            break

        else:
            if busca_por_id:
                print(
                    f"=======   ERRO   =======\n"
                    f"Seu ID de produto : ({produto}), nao foi encontrado cadastrado no sistema.\n\n"
                    f"1 - Cadastre-o voltando para o Menu\n"
                    f"2 - Corrija o nome do produto."
                    )

            else:
                print(
                    f"=======   ERRO   =======\n"
                    f"Seu produto : ({produto}), nao foi encontrado cadastrado no sistema.\n\n"
                    f"1 - Cadastre-o voltando para o Menu\n"
                    f"2 - Corrija o nome do produto."
                    )


            try:
                while True:
                    opcao_aba_vendas = int(input("Selecione uma opcao."))
                    while opcao_aba_vendas != 1 and opcao_aba_vendas != 2:
                        print("Opcao invalida, selecione 1 ou 2.")
                        opcao_aba_vendas = int(input("Selecione uma opcao."))

                    if opcao_aba_vendas == 1 or opcao_aba_vendas == 2:
                        break

            except ValueError:
                print("Opcao invalida, selecione 1 ou 2.")
                while True:
                    opcao_aba_vendas = int(input("Selecione uma opcao."))
                    while opcao_aba_vendas != 1 and opcao_aba_vendas != 2:
                        print("Opcao invalida, selecione 1 ou 2.")
                        opcao_aba_vendas = int(input("Selecione uma opcao."))

                    if opcao_aba_vendas == 1 or opcao_aba_vendas == 2:
                        break                

            if opcao_aba_vendas == 1:
                return

            if opcao_aba_vendas == 2:
                continue

    return produto_em_uso

def checar_se_ja_anunciado(produto_em_uso):
    if produto_em_uso.status == "FS": 
        print(
            f"Produto já está a venda.\n"
            f"Informacoes do Produto :\n\n"
            f"Produto : {produto_em_uso.nome.title().upper()}\n"
            f"Categoria : {produto_em_uso.categoria.title().upper()}\n"
            f"Quantidade em Estoque : {produto_em_uso.quantidade}\n"
            f"Valor : {produto_em_uso.valor}\n"
        )

        print("1 - Voltar ao Menu\n" "2 - Vender outro produto")

        try:
            while True:
                opcao_se_ja_FS = int(input("Selecione uma opcao."))
                while opcao_se_ja_FS != 1 and opcao_se_ja_FS != 2:
                    print("Opcao invalida, selecione 1 ou 2.")
                    opcao_se_ja_FS = int(input("Selecione uma opcao."))

                if opcao_se_ja_FS == 1 or opcao_se_ja_FS == 2:
                    break

        except ValueError:
            print("ERRO, selecione a opcao 1 ou 2.")
            
            while True:
                opcao_se_ja_FS = int(input("Selecione uma opcao."))
                while opcao_se_ja_FS != 1 and opcao_se_ja_FS != 2:
                    print("Opcao invalida, selecione 1 ou 2.")
                    opcao_se_ja_FS = int(input("Selecione uma opcao."))

                if opcao_se_ja_FS == 1 or opcao_se_ja_FS == 2:
                    break

        if opcao_se_ja_FS == 1:
            return "voltar_menu"

        if opcao_se_ja_FS == 2:
            return "vender_outro_produto"

    return "continuar"

def confirmacao_produto(produto_em_uso):
    while True:
        print(
            f"Produto encontrado e validado no sistema!\n"
            f"Informacoes do Produto :\n\n"
            f"Produto : {produto_em_uso.nome.title().upper()}\n"
            f"Categoria : {produto_em_uso.categoria.title().upper()}\n"
            f"Quantidade em Estoque : {produto_em_uso.quantidade}"
        )

        print(
            "Voce CONFIRMA que é este o produto que voce quer vender?\n"
            "1 - SIM\n"
            "2 - NAO"
        )

        while True:
            try:
                confirmacao = int(input("Escolha uma opcao"))
                while confirmacao != 1 and confirmacao != 2:
                    print("Opcao invalida, selecione 1 ou 2.")
                    confirmacao = int(input("Escolha uma opcao"))

                break

            except ValueError:
                print("ERRO, escolha uma opcao válida.")
                continue

        if confirmacao == 1:
            return "produto_correto"

        if confirmacao == 2:
            return "produto_errado"

def definir_valor(produto_em_uso):
    print(
        "Entao agora vamos definir o valor.\n"
        "Qual sera o VALOR em REAIS do seu produto?"
    )

    while True:
        try:
            valor_do_produto = float(input("R$"))
            
            if valor_do_produto < 0.1:
                print('Valor inválido, o produto precisa custar no mínimo 1 centavo.')
                continue

        except ValueError:
            print("Valor inválido, tente novamente.")
            continue

        print(
            f"Voce CONFIRMA que o valor do produto está CORRETO : {valor_do_produto}?\n"
            f"1 - SIM\n"
            f"2 - NAO\n"
        )

        while True:
            try:
                cfv = int(input("Escolha uma opcao :"))
                while cfv != 1 and cfv != 2:
                    print("Opcao invalida, selecione 1 ou 2.")
                    cfv = int(input("Escolha uma opcao"))

                break

            except ValueError:
                print("ERRO, selecione uma opcao válida.")
                continue

        if cfv == 1:
            print("Valor definido !")
            return valor_do_produto

        else:
            continue

def salvar_dados_em_json():
    produtos_em_json = []

    for produto in produtos:
        produto_dict = produto.to_dict()

        produtos_em_json.append(produto_dict)

    with open('produtos.json', 'w', encoding='utf-8') as arquivo_produtos:
        json.dump(produtos_em_json, arquivo_produtos, indent=4, ensure_ascii=False)

def ver_detalhes_produto():
                while True:
                    try:
                        opcao_ver_detalhes_pdt = int(input('Escolha uma opcao : '))
                        while opcao_ver_detalhes_pdt != 1 and opcao_ver_detalhes_pdt != 2:
                            print('Opcao inválida, tente novamente.')
                            opcao_ver_detalhes_pdt = int(input('Escolha uma opcao : '))
                        
                        break

                    except ValueError:
                        print('Opcao inválida, tente novamente.')
                        continue


                if opcao_ver_detalhes_pdt == 1:
                    print('\nPara ver detalhes :\n')

                    produto_ver_detalhes = encontrar_produto()
                    produto_ver_detalhes.detalhar_produto()

                if opcao_ver_detalhes_pdt == 2:
                    return

# inicio do code

produtos = carregar_dados_json()
criar_banco_dados()

while True:

    opcao = menu()

    if opcao == 1:
        cadastrar_produto()

    elif opcao == 2:
        if produtos:
            print("Atualmente temos os seguintes produtos :\n")
            for posicao, mostrar_produto in enumerate(produtos):
                print(f"{posicao+1}º Produto : {mostrar_produto.nome}")

            print(f"\nTotal de produtos : {len(produtos)}\n")

            print('Deseja ver os detalhes de algum produto?\n'
                  '1 - Sim\n'
                  '2 - Nao\n')
            
            ver_detalhes_produto()

        else:
            print("Ainda nao temos nenhum produto cadastrado.")

        input("Pressione ENTER para voltar ao menu...")

    elif opcao == 3:
        print("Vamos colocar um produto a venda.\n" "Siga as intrucoes :\n")

        while True:
            produto_em_uso = encontrar_produto()

            if produto_em_uso == None:
                break

            resultado_CSJA = checar_se_ja_anunciado(produto_em_uso)

            if resultado_CSJA == "voltar_menu":
                break

            elif resultado_CSJA == "vender_outro_produto":
                continue

            elif resultado_CSJA == "continuar":
                resultado_confirmacao_produto = confirmacao_produto(produto_em_uso)

                if resultado_confirmacao_produto == "produto_errado":
                    continue

                elif resultado_confirmacao_produto == "produto_correto":
                    valor = definir_valor(produto_em_uso)

                    produto_em_uso.colocar_a_venda(valor)

                    atualizar_banco_dados(produto_em_uso)

                    input('Digite ENTER para voltar ao menu...')

                    break

    if opcao == 4:
        break

salvar_dados_em_json()