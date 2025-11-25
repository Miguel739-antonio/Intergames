from models import local_session, Usuario, Plataforma, Jogo, Genero
from sqlalchemy import select


def criar_usuario():
    db_session = local_session()
    nome = input('NOME')
    email = input('EMAIL')
    senha = input('SENHA')
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db_session.add(novo_usuario)
    db_session.commit()

def criar_plataforma():
    db_session = local_session()
    nome = input('NOME')
    fabricante = input('FABRICANTE')
    novo_fabricante = Plataforma(nome=nome, fabricante=fabricante)
    db_session.add(novo_fabricante)
    db_session.commit()

def criar_genero():
    db_session = local_session()
    nome = input('NOME')
    novo_genero = Genero(nome=nome)
    db_session.add(novo_genero)
    db_session.commit()

def criar_jogo():
    db_session = local_session()
    titulo = input('TITULO')
    imagen_capa = input('IMAGEN Capa')
    descricao = input('DESCRICAO')
    ano_lancamento = input('ANO LANCAMENTO')
    novo_jogo = Jogo(titulo=titulo, imagen_capa=imagen_capa, descricao=descricao, ano_lancamento=ano_lancamento)
    db_session.add(novo_jogo)
    db_session.commit()

if __name__ == '__main__':
    criar_usuario()