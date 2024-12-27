from pathlib import Path
import pandas as pd
from datetime import date
from sqlalchemy import create_engine, String, Boolean, select, Column, Integer, Date, ForeignKey, PrimaryKeyConstraint, desc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash

pasta_atual = Path(__file__).parent
PATH_TO_BD = pasta_atual / 'bd_Capacita.sqlite'

class Base(DeclarativeBase):
    """Herda todas caracteristicas do SQLAlchemy"""
    pass

# Tabela Usuario
class Usuario(Base):
    """Herda a classe base"""
    __tablename__ = 'usuarios'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String(30), nullable=False)
    senha = mapped_column(String(128), nullable=False)
    email = mapped_column(String(30), nullable=False)
    acesso_gestor = mapped_column(Boolean, default=False)

    def __repr__(self):
        """como vai mostrar ao printar um usuario"""
        return f"Usuario({self.id=}, {self.nome=})"
    
    def define_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
# Tabela Treinamento
class Treinamento(Base):
    __tablename__ = "treinamento"
    id_treinamento = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String, nullable=False)
    dias_validade = mapped_column(Integer, nullable=False)
    tipo_treinamento = mapped_column(String, nullable=False)

    # Relacionamento com Treinamento_Realizado
    lancamentos = relationship("Lancamento", back_populates="treinamento")

# Tabela Funcao
class Funcao(Base):
    __tablename__ = "funcao"
    posicao = mapped_column(Integer, primary_key=True, autoincrement=False)
    descricao = mapped_column(String, nullable=False)

    # Relacionamento com Colaborador
    colaboradores = relationship("Colaborador", back_populates="funcao")

    def __repr__(self):
        """como vai mostrar ao printar uma função"""
        return f"Função({self.posicao=}, {self.descricao=})"

# Tabela Processo
class Processo(Base):
    __tablename__ = "processo"
    cdc = mapped_column(Integer, primary_key=True, autoincrement=False)
    descricao = mapped_column(String, nullable=False)
    processo = mapped_column(String, nullable=False)

    # Relacionamento com Colaborador
    colaboradores = relationship("Colaborador", back_populates="processo")

# Tabela Colaborador
class Colaborador(Base):
    __tablename__ = "colaborador"
    controle = mapped_column(Integer, primary_key=True, autoincrement=False)
    nome = mapped_column(String, nullable=False)
    posicao = mapped_column(Integer, ForeignKey("funcao.posicao"), nullable=False)
    cdc = mapped_column(Integer, ForeignKey("processo.cdc"), nullable=False)
    prazo = mapped_column(Date, nullable=False)
    status = mapped_column(String, nullable=False)

    # Relacionamentos
    funcao = relationship("Funcao", back_populates="colaboradores")
    processo = relationship("Processo", back_populates="colaboradores")
    lancamentos = relationship("Lancamento", back_populates="colaborador")

# Tabela Treinamento_Realizado
class Lancamento(Base):
    __tablename__ = "lancamento"
    id_lancamento = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_treinamento = mapped_column(Integer, ForeignKey("treinamento.id_treinamento"), nullable=False)
    controle = mapped_column(Integer, ForeignKey("colaborador.controle"), nullable=False)
    data_validade = mapped_column(Date, nullable=True)
    data_treinamento = mapped_column(Date, nullable=True)
    status = mapped_column(String, nullable=False)

    # Relacionamentos
    treinamento = relationship("Treinamento", back_populates="lancamentos")
    colaborador = relationship("Colaborador", back_populates="lancamentos")

# Configuração do banco (exemplo com SQLite)
engine = create_engine(f'sqlite:///{PATH_TO_BD}')
# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)


# CRUD Usuarios======================

def deleta_usuario(id):
    with Session(bind=engine) as session:
        comando_sql = select(Usuario).filter_by(id=id)
        usuarios = session.execute(comando_sql).fetchall()
        for usuario in usuarios:
            session.delete(usuario[0])
        session.commit()

# CRUD Salvar======================
def salva_usuario(
        id,
        **kwargs
        ):
        with Session(bind=engine) as session:
            comando_sql = select(Usuario).filter_by(id=id)
            usuario = session.execute(comando_sql).scalar()
            if usuario:
                # Atualiza o usuario existente
                usuario.nome = kwargs.get('nome')
                usuario.define_senha(kwargs.get('senha'))
                usuario.email = kwargs.get('email')
                usuario.acesso_gestor = kwargs.get('acesso_gestor')
            else:
                # Cria um novo usuario
                usuario = Usuario(id=id, **kwargs)
                usuario.define_senha(kwargs.get('senha'))
                session.add(usuario)
            
            try:
                session.commit()
            except Exception as e:
                # Trata exceções, por exemplo, rolando back a transação
                session.rollback()
                raise e
            
def salva_funcao(
        posicao,
        **kwargs
        ):
        with Session(bind=engine) as session:
            comando_sql = select(Funcao).filter_by(posicao=posicao)
            funcao = session.execute(comando_sql).scalar()
            if funcao:
                # Atualiza a função existente
                funcao.descricao = kwargs.get('descricao')
            else:
                # Cria uma nova função
                funcao = Funcao(posicao=posicao, **kwargs)
                session.add(funcao)
            
            try:
                session.commit()
            except Exception as e:
                # Trata exceções, por exemplo, rolando back a transação
                session.rollback()
                raise e

def salva_processo(
        cdc,
        **kwargs
        ):
        with Session(bind=engine) as session:
            comando_sql = select(Processo).filter_by(cdc=cdc)
            processo = session.execute(comando_sql).scalar()
            if processo:
                # Atualiza um processo existente
                processo.descricao = kwargs.get('descricao')
                processo.processo = kwargs.get('processo')
            else:
                # Cria um novo processo
                processo = Processo(cdc=cdc, **kwargs)
                session.add(processo)
            
            try:
                session.commit()
            except Exception as e:
                # Trata exceções, por exemplo, rolando back a transação
                session.rollback()
                raise e
            
def salva_treinamento(
        id_treinamento,
        **kwargs
        ):
        with Session(bind=engine) as session:
            comando_sql = select(Treinamento).filter_by(id_treinamento=id_treinamento)
            treinamento = session.execute(comando_sql).scalar()
            if treinamento:
                # Atualiza um treinamento existente
                treinamento.nome = kwargs.get('nome')
                treinamento.dias_validade = kwargs.get('dias_validade')
                treinamento.tipo_treinamento = kwargs.get('tipo_treinamento')
            else:
                # Cria um novo treinamento
                treinamento = Treinamento(**kwargs)
                session.add(treinamento)
            
            try:
                session.commit()
            except Exception as e:
                # Trata exceções, por exemplo, rolando back a transação
                session.rollback()
                raise e
            
def salva_lancamento(
        id_lancamento,
        **kwargs
        ):
        with Session(bind=engine) as session:

            comando_sql = select(Lancamento).filter_by(id_lancamento=id_lancamento)
            lancamento = session.execute(comando_sql).scalar()
            
            if id_lancamento:
                # Atualiza um lançamento de lancamento existente
                lancamento.id_treinamento = kwargs.get('id_treinamento')
                lancamento.controle = kwargs.get('controle')
                lancamento.data_validade = kwargs.get('data_validade')
                lancamento.data_treinamento = kwargs.get('data_treinamento')
                lancamento.status = kwargs.get('status')
            else:
                # Cria um novo lançamento de lancamento
                lancamento = Lancamento(**kwargs)
                session.add(lancamento)
            
            try:
                session.commit()
            except Exception as e:
                # Trata exceções, por exemplo, rolando back a transação
                session.rollback()
                raise e
            
def salva_colaborador(
        controle,
        **kwargs
        ):
        with Session(bind=engine) as session:
            comando_sql = select(Colaborador).filter_by(controle=controle)
            colaborador = session.execute(comando_sql).scalar()
            if colaborador:
                # Atualiza um lançamento de colaborador existente
                colaborador.nome = kwargs.get('nome')
                colaborador.posicao = kwargs.get('posicao')
                colaborador.cdc = kwargs.get('cdc')
                colaborador.prazo = kwargs.get('prazo')
                colaborador.status = kwargs.get('status')
            else:
                # Cria um novo lançamento de colaborador
                colaborador = Colaborador(controle=controle, **kwargs)
                session.add(colaborador)
            
            try:
                session.commit()
            except Exception as e:
                # Trata exceções, por exemplo, rolando back a transação
                session.rollback()
                raise e

# CRUD Buscar======================    
def ler_todos_usuarios():
    with Session(bind=engine) as session:
        resultados = session.query(Usuario).all()
        return resultados
    
def buscar_todos_usuarios():
    with Session(bind=engine) as session:
        resultados = session.query(Usuario).all()
        df = pd.DataFrame([{"id": user.id, "nome": user.nome, "email": user.email} for user in resultados])
        return df
        
def buscar_todas_funcoes():
    with Session(bind=engine) as session:
        resultados = session.query(Funcao).all()
        df = pd.DataFrame([{"posicao": funcao.posicao, "descricao": funcao.descricao} for funcao in resultados])
        return df
    
def buscar_todos_procesos():
    with Session(bind=engine) as session:
        resultados = session.query(Processo).all()
        df = pd.DataFrame([{"cdc": proc.cdc, "descricao": proc.descricao, "processo": proc.processo} for proc in resultados])
        return df
    
def buscar_todos_lancamentos():
    with Session(bind=engine) as session:
        # Realizando as junções necessárias
        resultados = (session.query(
                Lancamento.id_lancamento,
                Treinamento.id_treinamento,
                Treinamento.nome.label("nome_treinamento"),
                Lancamento.data_treinamento,
                Lancamento.data_validade,
                Colaborador.controle,
                Colaborador.nome.label("nome_colaborador"),
                Colaborador.posicao,
                Funcao.descricao.label("descricao_funcao"),
                Colaborador.cdc,
                Processo.descricao.label("descricao_processo"),
                Processo.processo,
                Lancamento.status
            )
            .join(Lancamento, Treinamento.id_treinamento == Lancamento.id_treinamento)
            .join(Colaborador, Colaborador.controle == Lancamento.controle)
            .join(Funcao, Funcao.posicao == Colaborador.posicao)
            .join(Processo, Processo.cdc == Colaborador.cdc)
            .all()
        )
        if resultados:
            # Convertendo os resultados em um DataFrame
            df = pd.DataFrame([
                {
                    "id_lancamento": row.id_lancamento,
                    "status": "Atrasado" if (row.data_validade <  date.today()) and (row.data_treinamento is None) else row.status,
                    "id_treinamento": row.id_treinamento,
                    "nome_treinamento": row.nome_treinamento,
                    "data_treinamento": row.data_treinamento,
                    "data_validade": row.data_validade,
                    "controle": row.controle,
                    "nome_colaborador": row.nome_colaborador,
                    "posicao": row.posicao,
                    "descricao_funcao": row.descricao_funcao,
                    "cdc": row.cdc,
                    "descricao_processo": row.descricao_processo,
                    "processo": row.processo
                    
                }
                for row in resultados
            ])
            return df.set_index('id_lancamento')
        else:
            return pd.DataFrame()
    
def buscar_detalhes_lancamento(id_treinamento, controle):
    try:
        with Session(bind=engine) as session:
            resultado = (session.query(
                    Lancamento.id_lancamento,
                    Lancamento.data_validade,
                    Lancamento.data_treinamento,
                    Lancamento.status
                )
                .where(Lancamento.id_treinamento == id_treinamento)
                .where(Lancamento.controle == controle)
                .order_by(Lancamento.data_treinamento.desc().nulls_first()) # Prioriza NULLs
                .first()
            )
            # Convertendo os resultados em um DataFrame
            if resultado:
                return pd.DataFrame([
                    {
                    "id_lancamento": resultado.id_lancamento,
                    "data_validade": resultado.data_validade,
                    "data_treinamento": resultado.data_treinamento,
                    "status": resultado.status
                    }])
            else:
                return pd.DataFrame(columns=["id_lancamento", "data_validade", "data_treinamento", "status"])
    except Exception as e:
        print(f"Erro ao buscar detalhes do lançamento: {e}")
        return pd.DataFrame(columns=["id_lancamento", "data_validade", "data_treinamento", "status"])
    
    
def buscar_todos_treinamentos():
    with Session(bind=engine) as session:
        resultados = session.query(Treinamento).all()
        df = pd.DataFrame([{"id_treinamento": trein.id_treinamento, "nome": trein.nome, "dias_validade": trein.dias_validade, "tipo_treinamento": trein.tipo_treinamento} for trein in resultados])
        return df

def buscar_treinamento(id_treinamento):
    with Session(bind=engine) as session:
        resultados = session.query(Treinamento).filter_by(id_treinamento=id_treinamento).scalar()
        df = pd.DataFrame([{"id_treinamento": resultados.id_treinamento, "nome": resultados.nome, "dias_validade": resultados.dias_validade, "tipo_treinamento": resultados.tipo_treinamento}])
        return df
    
def buscar_todos_colaboradores():
    with Session(bind=engine) as session:
        resultados = session.query(Colaborador).all()
        df = pd.DataFrame([{"controle": colab.controle, "nome": colab.nome, "posicao": colab.posicao, "cdc": colab.cdc, "prazo": colab.prazo, "status": colab.status} for colab in resultados])
        return df
    