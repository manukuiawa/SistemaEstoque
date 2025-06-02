import mysql.connector, os 

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

comprasRealizadas = []

def limparTela(): 
     os.system('cls' if os.name == 'nt' else 'clear')

def conectarBD():
    return mysql.connector.connect(
        host='localhost', 
        database='estoque',
        user='root',
        password='0166'  
)

def listarProdutos(): 
    limparTela()
    conexao = conectarBD()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, quantidade, preco FROM produtos")
    produtos = cursor.fetchall()

    print("-" * 50)
    print(f"{'ID':<5} | {'Produto':<20} | {'Qtd':<5} | {'Preço':<10}")
    print("-" * 50)
    for p in produtos:
        print(f"{p[0]:<5} | {p[1]:<20} | {p[2]:<5} | R${p[3]:<10.2f}")
    print("-" * 50)

    cursor.close()
    conexao.close()

def buscarProduto():
    limparTela()
    conexao = conectarBD()
    cursor = conexao.cursor()

    print("----------Buscar Produto-----------")
    nomeBusca = input("Insira o nome do produto que deseja buscar: ").strip().title()
    
    sql = "SELECT * FROM produtos WHERE nome LIKE %s"
    valor = ("%" + nomeBusca + "%",)

    cursor.execute(sql, valor)
    resultado = cursor.fetchall()

    if resultado:
        for produto in resultado:
            print(f"\nID: {produto[0]}")
            print(f"Nome: {produto[1]}")
            print(f"Descrição: {produto[2]}")
            print(f"Preço: R${produto[3]:.2f}")
            print(f"Quantidade: {produto[4]}")
    else:
        print("Produto não encontrado.")

def adicionarProduto(): 
    limparTela()
    conexao = conectarBD()
    cursor = conexao.cursor()

    print("-------------Adicionar Produto----------------")
    nome = input("Produto: ").strip().title()
    descricao = input("Descrição:  ").strip().capitalize()
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))

    sql = "INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (%s, %s, %s, %s)"
    valores = (nome, descricao, preco, quantidade)

    cursor.execute(sql, valores)
    conexao.commit()

    print("✅ Produto adicionado com sucesso!")

    cursor.close()
    conexao.close()


def deletarProduto(): 
    limparTela()
    listarProdutos()

    conexao = conectarBD()
    cursor = conexao.cursor()

    print("---------Deletar Produto---------")
    idProduto = input("Insira o ID do produto que deseja deletar: ")

    cursor.execute("SELECT * FROM produtos WHERE id = %s", (idProduto, ))
    resultado = cursor.fetchone()

    if resultado: 
        confirmar = input(f"Quer mesmo deletar '{resultado[1]}'? (s/n): ").lower()
        if confirmar == 's': 
            cursor.execute("DELETE FROM produtos WHERE id = %s", (idProduto, ))
            conexao.commit()
            print("✅ Produto deletado com sucesso!")
        else: 
            print("🚫 Cancelado. Produto não foi deletado!")
    else: 
        print("❌ Produto não encontrado!")
    
    cursor.close()
    conexao.close()

def alterarProduto(): 
    limparTela()
    listarProdutos()

    conexao = conectarBD()
    cursor = conexao.cursor()

    print("-----------Alterar Produto-----------")
    idProduto = int(input("Insira o ID do produto que deseja alterar: "))

    print("O que deseja alterar? ")
    print("1. Nome")
    print("2. Descrição")
    print("3. Preço")
    print("4. Quantidade")

    opcao = input("Escolha uma opção: ")

    if opcao == "1": 
        novaAlteracao = input("Novo Nome: ").strip().title()
        campo = "nome"
    elif opcao == "2": 
        novaAlteracao = input("Nova Descrição: ").strip().capitalize()
        campo = "descricao"
    elif opcao == "3": 
        novaAlteracao = float(input("Novo Preço: "))
        campo = "preco"  
    elif opcao == "4": 
        novaAlteracao = int(input("Nova Quantidade: "))
        campo = "quantidade"
    else: 
        print("❌ Opção inválida.")
        cursor.close()
        conexao.close()
        return  

    sql = f"UPDATE produtos SET {campo} = %s WHERE id = %s"
    valores = (novaAlteracao, idProduto)

    cursor.execute(sql, valores)
    conexao.commit()

    print("✅ Produto atualizado com sucesso!")

    cursor.close()
    conexao.close()

def comprarProduto():
    global comprasRealizadas  
    limparTela()
    listarProdutos()

    conexao = conectarBD()
    cursor = conexao.cursor()

    print("---------Comprar Produto---------")
    idProduto = input("Digite o ID do produto: ")

    quantidadeDesejada = input("Quantidade para comprar: ")
    if not quantidadeDesejada.isdigit():
        print("❌ Quantidade inválida! Digite um número inteiro positivo.")
        return

    quantidadeDesejada = int(quantidadeDesejada)

    if quantidadeDesejada <= 0:
        print("❌ Quantidade tem que ser maior que zero.")
        return

    cursor.execute("SELECT nome, quantidade, preco FROM produtos WHERE id = %s", (idProduto,))
    produto = cursor.fetchone()

    if produto:
        nome, estoqueAtual, preco = produto
        if estoqueAtual == 0:
            print(f"❌ Produto '{nome}' está esgotado.")
        elif quantidadeDesejada > estoqueAtual:
            print(f"❌ Só tem {estoqueAtual} unidades de '{nome}' no estoque.")
        else:
            novoEstoque = estoqueAtual - quantidadeDesejada
            valorTotal = quantidadeDesejada * preco

            cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (novoEstoque, idProduto))
            conexao.commit()

            print(f"✅ Compra realizada com sucesso!")
        
            print("Informações da Compra")
            print(f"Produto: {nome}")
            print(f"Quantidade comprada: {quantidadeDesejada}")
            print(f"Valor total: R${valorTotal:.2f}")
            print(f"Estoque restante: {novoEstoque}")

            from datetime import datetime
            comprasRealizadas.append({
                "produto": nome,
                "quantidade": quantidadeDesejada,
                "preco_unitario": float(preco),
                "subtotal": float(valorTotal),
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })
    else:
        print("❌ Produto não encontrado.")

    cursor.close()
    conexao.close()

def darDesconto():
    limparTela()
    listarProdutos()

    conexao = conectarBD()
    cursor = conexao.cursor()

    print("--------- Dar Desconto ---------")
    idProduto = input("Digite o ID do produto: ")

    cursor.execute("SELECT nome, preco FROM produtos WHERE id = %s", (idProduto,))
    produto = cursor.fetchone()

    if produto:
        nome, precoAtual = produto
        precoAtual = float(precoAtual)  
        print(f"\nProduto: {nome}")
        print(f"Preço atual: R${precoAtual:.2f}")

        desconto = input("Digite o percentual de desconto (%): ")

        if not desconto.replace('.', '', 1).isdigit():
            print("❌ Valor inválido. Use apenas números.")
            return

        desconto = float(desconto)

        if desconto <= 0 or desconto >= 100:
            print("❌ Desconto deve ser entre 1% e 99%.")
            return

        novoPreco = precoAtual - (precoAtual * desconto / 100)
        cursor.execute("UPDATE produtos SET preco = %s WHERE id = %s", (novoPreco, idProduto))
        conexao.commit()

        print("\n✅ Desconto aplicado com sucesso!")
        print(f"Produto: {nome}")
        print(f"Desconto: {desconto:.1f}%")
        print(f"Preço anterior: R${precoAtual:.2f}")
        print(f"Novo preço:     R${novoPreco:.2f}")
    else:
        print("❌ Produto não encontrado.")

    cursor.close()
    conexao.close()

def notaFiscal(compras, nome_arquivo="nota_fiscal.pdf", desconto=None):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(largura / 2, altura - 2*cm, "Nota Fiscal Eletrônica")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(largura / 2, altura - 2.7*cm, f"Data da Compra: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    c.line(2*cm, altura - 3.2*cm, largura - 2*cm, altura - 3.2*cm)

    y = altura - 4*cm
    total_geral = 0

    for item in compras:
        produto = item['produto']
        qtd = item['quantidade']
        preco_unit = item['preco_unitario']
        subtotal = item['subtotal']
        data = item['data']

        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, f"✅ Produto: {produto}")
        y -= 0.5*cm

        c.setFont("Helvetica", 11)
        c.drawString(2.5*cm, y, f"Quantidade: {qtd}")
        y -= 0.4*cm
        c.drawString(2.5*cm, y, f"Preço unitário: R${preco_unit:.2f}")
        y -= 0.4*cm
        c.drawString(2.5*cm, y, f"Subtotal: R${subtotal:.2f}")
        y -= 0.4*cm
        c.drawString(2.5*cm, y, f"Data da compra: {data}")
        y -= 0.6*cm

       
        c.line(2*cm, y, largura - 2*cm, y)
        y -= 0.6*cm

        total_geral += subtotal

        if y < 5*cm:
            c.showPage()
            y = altura - 3*cm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y, f"✅ Total da Compra: R${total_geral:.2f}")
    y -= 0.5*cm

    y -= 1*cm
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(largura / 2, y, "Obrigada por comprar com a gente.  Volte sempre!")

    c.save()
    print("📄 Nota fiscal gerada com sucesso!")


def menu(): 
    limparTela()
    while True: 
        print("------------Sistema do Estoque----------")
        print("1. Consultar Estoque")
        print("2. Buscar Produto")
        print("3. Adicionar produto")
        print("4. Deletar Produto")
        print("5. Alterar Produto")
        print("6. Comprar")
        print("7. Dar Desconto  ")
        print("8. Gerar Nota Fiscal")
        print("9. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1": 
            listarProdutos()
        elif opcao == "2": 
            buscarProduto()
        elif opcao == "3": 
            adicionarProduto()
        elif opcao == "4": 
            deletarProduto()
        elif opcao == "5": 
            alterarProduto()
        elif opcao == "6": 
            comprarProduto()
        elif opcao == "7": 
            darDesconto()
        elif opcao == "8": 
            notaFiscal(comprasRealizadas)
        elif opcao == "9": 
            print("Obrigada por usar nosso sistema...")
            break