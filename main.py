import asyncio
import auth_engine as a
import database as db
import getpass as g
import time as t

def mostrar_menu():
    print('---------- MENU ----------')
    print('---------- ESCOLHA A OPÇÃO ----------')
    print('---------- OPÇÃO 1: Cadastrar ----------')
    print('---------- OPÇÃO 2: Login ----------')
    print('---------- OPÇÃO 3: Sair ----------')

async def loading():
    for i in range(5):
        print("Carregando" + "." * i, end="\r")
        await asyncio.sleep(0.5)

contador_login = 0
ultima_tentativa = 0
TEMPO_RESET = 300

def main():
    while True:
        mostrar_menu()

        try:
            escolha = int(input("Digite sua opção: "))
        except ValueError:
            print("Digite apenas números!")
            continue  # volta para o início do loop

        if escolha == 1:
            asyncio.run(loading())

            print("Você selecionou a opção cadastrar!")
            print("Para o cadastro precisamos que digite seu email e senha.")

            email = input("Digite seu email: ").lower()

            asyncio.run(loading())

            print("Email recebido com sucesso!")

            senha = g.getpass("Digite sua senha: ")

            asyncio.run(loading())

            print('Senha recebida com sucesso!')

            senha_hash = a.hash_password(senha)

            print(f'Para debugging o hash é {senha_hash}')

            db.salvar_usuario(email, senha_hash)
            
        elif escolha == 2:
            global contador_login, ultima_tentativa
            
            agora = t.time()

            if agora - ultima_tentativa > TEMPO_RESET:
                contador_login = 0

            ultima_tentativa = agora

            if contador_login >= 20:
                print("Muitas tentativas. Aguarde 5 minutos.")
                t.sleep(300)

            elif contador_login >= 15:
                print("Muitas tentativas. Aguarde 2 minutos.")
                t.sleep(120)

            elif contador_login >= 10:
                print("Muitas tentativas. Aguarde 30 segundos.")
                t.sleep(30)

            elif contador_login >= 5:
                print("Muitas tentativas. Aguarde 10 segundos.")
                t.sleep(10)

            asyncio.run(loading())
            print("Você selecionou a opção login!")
            print("Para fazer login precisamos que digite seu email e senha.")

            email = input('Digite seu email: ').lower()

            asyncio.run(loading())

            print("Email recebido com sucesso!")

            senha = g.getpass('Digite sua senha: ')

            asyncio.run(loading())
            
            print('Senha recebida com sucesso!')

            senha_hash = a.hash_password(senha)

            print(f'Para debugging o hash é {senha_hash}')

            print(f'Para debugging{db.buscar_usuario(email)}')

            hash_salva = db.buscar_usuario(email)

            if hash_salva is None:
                print("Usuário não encontrado")
                contador_login += 1
            else:
                if a.verify_password(senha, hash_salva):
                    print('Login realizado com sucesso!')
                    contador_login = 0
                else:
                    print('Senha incorreta!')
                    contador_login += 1
                    
        elif escolha == 3:
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()