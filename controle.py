from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QPushButton


#Conectando o banco de dados
banco=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

#Conectando o banco de dados
banco2=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="usuarios"
)

numero_id = 0

def verificar_login():
    usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    cursor = banco2.cursor()
    try:  
        cursor.execute("SELECT senha FROM acesso WHERE login = '{}'".format(usuario))
        senha_bd = cursor.fetchall()
        print(senha_bd[0][0])
        cursor.close()
        
    except:
        print("ERRO")
    if senha == senha_bd[0][0]:
        formulario.show()
        tela_login.close()
    else:
        tela_login.label_3.setText("USUARIO INVALIDO")


def editar_dados():
    global numero_id
#Retorna qual linha foi selecionada
    linha = segunda_tela.tableWidget.currentRow()
 #Inicia a funcao do BD   
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id

#Retorna os dados do BD nas posições
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id


def salvar_valor_editado():
#Pega o numero do ID
    global numero_id

# Ler dados do lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
# Atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria ='{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    banco.commit()
#Atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()


def excluir_dados():
#Limpa da interface grafica   
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)
#Cria vetor paa salvar as coordenadas e selecionar o que sera excluido
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
#Deleta o item selecionado 
    cursor.execute("DELETE FROM produtos WHERE id=" + str(valor_id))
    banco.commit()

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25) #Tamanho do Titulo
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 12) #Tamanho do Texto
#Posicao itens do titulo
    pdf.drawString(10,750, "ID")
    pdf.drawString(60,750, "CODIGO")
    pdf.drawString(150,750, "PRODUTO")
    pdf.drawString(330,750, "PREÇO")
    pdf.drawString(430,750, "CATEGORIA")
#Posicao Itens do Texto
    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(60,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(150,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(330,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(430,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    #print("PDF FOI GERADO COM SUCESSO!")
      


def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    categoria = ""
    
    if formulario.radioButton.isChecked() :
        print("Categoria Informatica selecionada")
        categoria="Informatica"
    elif formulario.radioButton_2.isChecked() :
        print("Categoria Alimentos selecionada")
        categoria="Alimentos"
    else :
        print("Categoria Eletronicos selecionada")
        categoria="Eletronicos"

    print("Código:",linha1)
    print("Descricao:",linha2)
    print("Preco",linha3)

#Executa o comando no SQL
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()

#Limpa os campos digitados apos enviar os dados ao BD
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    

def chama_segunda_tela():
    segunda_tela.show()

#Executa o retorno de dados no SQL
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



#Carregando os aquivos
app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
tela_editar=uic.loadUi("menu_editar.ui")
tela_login=uic.loadUi("acesso.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)
tela_login.pushButton.clicked.connect(verificar_login)

tela_login.show()
app.exec()