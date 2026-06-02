import sqlite3

conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()

def confirmacao_1_2():
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
        return 1
    
    elif confirmacao == 2:
        return 2

# Funcoes de banco de dados

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
    
    produto.id = cursor.lastrowid

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

def excluir_produto_do_banco(produto):
    cursor.execute("DELETE FROM produtos WHERE id = ?",
                   (produto.id,))

    conexao.commit()

    print('Produto removido com sucesso !')


def editar_nome_no_banco(produto, nome_novo):
    cursor.execute("""UPDATE produtos
                   SET nome = ?
                   WHERE id = ?""",
                  (nome_novo, produto.id))

    conexao.commit()

def editar_categoria_no_banco(produto, categoria_nova):
    cursor.execute("""UPDATE produtos
                   SET categoria = ?
                   WHERE id = ?""",
                  (categoria_nova, produto.id))

    conexao.commit()

def editar_quantidade_no_banco(produto, quantidade_nova):
    cursor.execute("""UPDATE produtos
                   SET quantidade = ?
                   WHERE id = ?""",
                  (quantidade_nova, produto.id))

    conexao.commit()

def editar_valor_no_banco(produto, valor_novo):
    cursor.execute("""UPDATE produtos
                   SET valor = ?
                   WHERE id = ?""",
                  (valor_novo, produto.id))

    conexao.commit()

# Classes e funcoes de manipulacao de produtos

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

# Funcoes de interacao com o usuario

def menu():
    opcoes = (1, 2, 3, 4, 5, 6)

    print("=====    MENU    =====\n\n")
    print(
        "Escolha uma opcao :\n\n"
        "1 - Cadastrar produto\n"
        "2 - Ver produtos\n"
        "3 - Vender produto\n"
        "4 - Excluir produto\n"
        "5 - Editar produto\n"
        "6 - Sair\n"
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

            produto = Produto(None,
                produto_nome,
                produto_categoria,
                produto_estoque,
                produto_status,
                None)

            inserir_produto_no_banco(produto)

            produtos.append(produto)

            print('Produto cadastrado com sucesso !\n'
                  'Volte ao menu e escolha a opcao "Ver produtos" para ver os detalhes do produto cadastrado.\n')

            input("Pressione ENTER para voltar ao menu...")

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
                    f"1 - Cadastre-o, ou confira o nome/id voltando para o Menu\n"
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
            "Voce CONFIRMA que é este o produto correto?\n"
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

def definir_valor():
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

                    if produto_ver_detalhes == None:
                        return

                    produto_ver_detalhes.detalhar_produto()

                if opcao_ver_detalhes_pdt == 2:
                    return

def editar_produto(produto):
    opcoes = (1, 2, 3, 4, 5)

    while True:
        print(f"""O que voce deseja alterar no produto : [{produto.nome}]?\n\n
            1 - Nome\n
            2 - Categoria\n
            3 - Quantidade\n
            4 - Valor\n
            5 - Nao alterar, e voltar ao menu""")

        while True:
            try:
                opcao_edit_product = int(input('Digite a opcao desejada : '))
                while opcao_edit_product not in opcoes:
                    print('Opcao inválida, tente novamente.')
                    opcao_edit_product = int(input('Digite a opcao desejada : '))

                break

            except ValueError:
                print('Opcao inválida, tente novamente.')
                continue


        if opcao_edit_product == 1:
            editar_nome(produto)            

            print('Nome alterado com sucesso!')
            break

        elif opcao_edit_product == 2:
            editar_categoria(produto)

            print('Categoria alterada com sucesso!')
            break

        elif opcao_edit_product == 3:
            editar_quantidade(produto)

            print('Quantidade alterada com sucesso!')
            break

        elif opcao_edit_product == 4:
            editar_valor(produto)
            
            print('Valor alterado com sucesso!')
            break

        elif opcao_edit_product == 5:
            break

def editar_nome(produto):
    while True:
                print('Para mudar o nome, digite o novo nome do seu produto :\n\n')

                nome_novo = input(': ').lower().strip()

                print(
                f"Voce CONFIRMA que digitou o novo nome : {nome_novo} corretamente?\n"
                f"1 - SIM\n"
                f"2 - NAO"
                )

                conf = confirmacao_1_2()

                if conf == 1:
                    try:
                        editar_nome_no_banco(produto, nome_novo)
                        
                        produto.nome = nome_novo

                        break

                    except sqlite3.IntegrityError:
                        print('Nome de produto já existente, escolha :\n'
                              '1 - Definir outro nome\n'
                              '2 - Voltar ao menu\n')

                        conf2 = confirmacao_1_2()

                        if conf2 == 1:
                            continue

                        elif conf2 == 2:
                            break

                elif conf == 2:
                    continue

def editar_categoria(produto):
    while True:
                print(f'Para mudar a categoria, digite a nova categoria do seu produto dentre as opcoes válidas :\n'
                      f'{categorias}\n\n')

                categoria_nova = input('Digite a categoria desejada: ').lower().strip()

                if categoria_nova in categorias:
                    print(
                    f"Voce CONFIRMA que digitou a categoria nova : {categoria_nova} corretamente?\n"
                    f"1 - SIM\n"
                    f"2 - NAO"
                    )

                    conf = confirmacao_1_2()

                    if conf == 1:
                        produto.categoria = categoria_nova

                        editar_categoria_no_banco(produto, categoria_nova)

                        break

                    elif conf == 2:
                        continue

                else:
                    print('Categoria inválida, tente novamente.')
                    continue

def editar_quantidade(produto):
    while True:
                print(f'Para mudar a quantidade, digite a nova quantidade do seu produto:\n\n')

                while True:
                    try:
                        quantidade_nova = int(input('Digite a quantidade desejada: '))

                        if quantidade_nova < 1:
                            print('Quantidade inválida, tente novamente.')
                            continue

                        else:
                            break

                    except ValueError:
                        print('Quantidade inválida, tente novamente.')
                        continue

                print(
                f"Voce CONFIRMA que digitou a quantidade nova : {quantidade_nova} corretamente?\n"
                f"1 - SIM\n"
                f"2 - NAO"
                )

                conf = confirmacao_1_2()

                if conf == 1:
                    produto.quantidade = quantidade_nova

                    editar_quantidade_no_banco(produto, quantidade_nova)

                    break

                elif conf == 2:
                    continue

def editar_valor(produto):
    while True:
                print(f'Para mudar o valor, digite o novo valor do seu produto:\n\n')

                while True:
                    try:
                        valor_novo = float(input('Digite o valor desejado: R$'))
                        
                        if valor_novo < 1:
                            print('Valor inválido, tente novamente.')
                            continue
                        
                        else:
                            break
                        
                    except ValueError:
                        print('Quantidade inválida, tente novamente.')
                        continue

                print(
                f"Voce CONFIRMA que digitou o valor novo : {valor_novo} corretamente?\n"
                f"1 - SIM\n"
                f"2 - NAO"
                )

                conf = confirmacao_1_2()

                if conf == 1:
                    produto.valor = valor_novo

                    editar_valor_no_banco(produto, valor_novo)

                    break

                elif conf == 2:
                    continue

# inicio do code

criar_banco_dados()
produtos = carregar_banco_dados()

while True:

    opcao = menu()

    if opcao == 1:
        cadastrar_produto()

    elif opcao == 2:
        if produtos:
            print("Atualmente temos os seguintes produtos :\n")
            for posicao, mostrar_produto in enumerate(produtos):
                print(f"{posicao+1}º Produto : {mostrar_produto.nome} [ID : {mostrar_produto.id}]")

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
                    valor = definir_valor()

                    produto_em_uso.colocar_a_venda(valor)

                    atualizar_banco_dados(produto_em_uso)

                    input('Digite ENTER para voltar ao menu...')

                    break

    if opcao == 4:
        while True:
            print('Informe qual produto voce deseja excluir: ')
        
            produto = encontrar_produto()

            if produto == None:
                break

            R_conf_Pdt_op4 = confirmacao_produto(produto)

            if R_conf_Pdt_op4 == "produto_errado":
                continue

            elif R_conf_Pdt_op4 == "produto_correto":
                excluir_produto_do_banco(produto)
                produtos.remove(produto)
                break

        input("Pressione ENTER para voltar ao menu...")

    if opcao == 5:
        print('Para editar seu produto, vamos primeiro definir o produto que voce quer editar.\n\n')

        produto_op5 = encontrar_produto()

        if produto_op5 == None:
            continue

        editar_produto(produto_op5)

    if opcao == 6:
        break

