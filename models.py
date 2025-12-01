from sqlalchemy import Column, DateTime, func, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/intergames')

local_session = sessionmaker(bind=engine)
Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(11), unique=True, nullable=False)
    def __repr__(self):
        return f'<Usuario {self.nome}>, email: {self.email}, senha: ({self.senha})>'

class Plataforma(Base):
    __tablename__ = 'plataforma'
    id_plataforma = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    fabricante = Column(String(50), nullable=False)
    def __repr__(self):
        return f'<Plataforma {self.nome}, fabricante: {self.fabricante}, id: {self.id_plataforma}>'

class Genero(Base):
    __tablename__ = 'genero'
    id_genero = Column(Integer, primary_key=True)
    nome = Column(String(30), nullable=False)
    def __repr__(self):
        return f'<Genero {self.nome}, id: {self.id_genero}>'

class Desenvolvedora(Base):
    __tablename__ = 'desenvolvedora'
    id_desenvolvedora = Column(Integer, primary_key=True)
    nome = Column(String(30), nullable=False)
    def __repr__(self):
        return f'<Desenvolvedora {self.nome}>, id: {self.id_desenvolvedora}>'

class Jogo(Base):
    __tablename__ = 'jogo'
    id_jogo = Column(Integer, primary_key=True)
    titulo = Column(String(50), nullable=False)
    descricao = Column(String(250), nullable=False)
    ano_lancamento = Column(String(250), nullable=False)
    url_img = Column(String, nullable=False)
    id_FK_Desenvolvedora = Column(Integer, ForeignKey('desenvolvedora.id_desenvolvedora'))
    id_FK_Genero = Column(Integer, ForeignKey('genero.id_genero'))
    def __repr__(self):
        return f'<Jogo {self.id_jogo}, titulo: {self.titulo}, url_img: {self.url_img}, descricao:{ self.descricao }, ano_lancamento:{ self.ano_lancamento }>'