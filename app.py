import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError

from models import local_session, Usuario, Plataforma, Genero, Jogo, Desenvolvedora
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def home():
    return render_template('intergames.html')


@app.route('/add_jogo', methods=['GET', 'POST'])
def post_jogos():
    db_session = local_session()
    if request.method == 'POST':
        if not request.form['form_titulo']:
            flash("Preencha o formulario para o titulo", "danger")
            return redirect(url_for('home'))
        if not request.form['form_descricao']:
            flash("Preencha o formulario para o descricao", "danger")
        if not request.form['form_ano_lancamento']:
            flash("Preencha o formulario para o ano lancamento", "danger")
        if not request.form['form_url_img']:
            flash("Preencha o formulario para a imagem do jogo", "danger")
        if not request.form['form_genero']:
            flash("Escolha o formulario para o genero", "danger")

        dados_jogos = Jogo(
            titulo=request.form['form_titulo'],
            descricao=request.form['form_descricao'],
            ano_lancamento=request.form['form_ano_lancamento'],
            url_img=request.form['form_url_img'],
            id_FK_Genero=int(request.form['form_genero'])
        )
        try:
            db_session.add(dados_jogos)
            db_session.commit()
            flash('Jogo adicionado criado com sucesso', 'success')

            return redirect(url_for('listar_jogos'))
        except SQLAlchemyError as e:
            print(f'Erro na base de dados{e}')
            db_session.rollback()
            return redirect(url_for('listar_jogos'))
        finally:
            db_session.close()

    generos_sql = select(Genero)
    resultado = db_session.execute(generos_sql).scalars().all()

    desenvolvedoras_sql = select(Desenvolvedora)
    resultado2 = db_session.execute(desenvolvedoras_sql).scalars().all()

    plataformas_sql = select(Plataforma)
    resultado3 = db_session.execute(plataformas_sql).scalars().all()

    return render_template('add_jogos.html', var_generos=resultado,
    var_desenvolvedoras=resultado2, var_plataformas=resultado3                       )


@app.route('/jogo')
def listar_jogos():
    db_session = local_session()
    try:
        jogos_sql = select(Jogo)
        resultado = db_session.execute(jogos_sql).scalars()
        print('ddf',resultado)
        return render_template('listar_jogos.html', var_jogos=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de jogo: {e}')
        return redirect(url_for('listar_jogos'))
    except Exception as ex:
        print(f'Erro ao consultar jogo: {ex}')
        return redirect(url_for('listar_jogos'))
    finally:
        db_session.close()


@app.route('/genero', methods=['GET', 'POST'])
def listar_generos():
    db_session = local_session()
    try:
        if request.method == 'POST':
            print('yjh')
            print(request.form.get('form_genero'))

            if request.form.get('form_genero'):
                print('jjh')
                flash("Preencha o formulario para o genero", "danger")
                dados_genero = Genero(nome=request.form['form_genero'])
                db_session.add(dados_genero)
                db_session.commit()
                return redirect(url_for('listar_generos'))


        generos_sql = select(Genero)
        resultado = db_session.execute(generos_sql).scalars().all()
        print('dds',resultado)
        return render_template('listar_generos.html', var_generos=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de genero: {e}')
        return redirect(url_for('listar_generos'))
    except Exception as ex:
        print(f'E'
              f'ultar genero: {ex}')
        return redirect(url_for('listar_generos.'))
    finally:
        db_session.close()

@app.route('/plataforma', methods=['GET', 'POST'])
def listar_plataformas():
    db_session = local_session()
    try:
        if request.method == 'POST':
            if not request.form['form_nome']:
                flash("Preencha o formulario para o nome", "danger")
            if not request.form['form_fabricante']:
                flash("Preencha o formulario para o fabricante", "danger")
            if request.form['form_nome'] and request.form['form_fabricante']:
                dados_fabricante = Plataforma(
                    nome=request.form['form_nome'],
                    fabricante=request.form['form_fabricante']
                )
                db_session.add(dados_fabricante)
                db_session.commit()

        plataformas_sql = select(Plataforma)
        resultado = db_session.execute(plataformas_sql).scalars().all()
        return render_template('listar_plataformas.html', var_plataformas=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de Plataformas: {e}')
        return redirect(url_for('listar_plataformas'))
    except Exception as ex:
        print(f'Erro ao consultar plataformas: {ex}')
        return redirect(url_for('listar_plataformas'))
    finally:
        db_session.close()


@app.route('/desenvolvedora', methods=['GET', 'POST'])
def listar_desenvolvedoras():
    db_session = local_session()
    try:
        if request.method == 'POST':
            print(request.form.get('form_desenvolvedoras'))

            if request.form.get('form_desenvolvedoras'):
                dados_desenvolvedora = Desenvolvedora(nome=request.form['form_nome'])
                db_session.add(dados_desenvolvedora)
                db_session.commit()
                return redirect(url_for('listar_desenvolvedoras'))
            else:
                flash("Preencha o formulario para o nome", "danger")

        desenvolvedoras_sql = select(Desenvolvedora)
        resultado = db_session.execute(desenvolvedoras_sql).scalars().all()
        print("dev", resultado)
        return render_template('listar_desenvolvedoras.html', var_desenvolvedoras=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de desenvolvedoras: {e}')
        return redirect(url_for('home'))
    except Exception as ex:
        print(f'Erro ao consultar desenvolvedoras: {ex}')
        return redirect(url_for('home'))
    finally:
        db_session.close()


@app.route('/detalhes_jogo/<var_id>', methods=['GET'])
def detalhar_jogo(var_id):
    db_session = local_session()
    try:
        detalhes_jogo = (select(Jogo, Genero)
                         .join(Genero, Genero.id_genero==Jogo.id_FK_Genero)
                         .where(Jogo.id_jogo == var_id))
        resultado = db_session.execute(detalhes_jogo).all()

        print("joo", resultado)
        return render_template('detalhes_jogo.html', var_detalhes=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de detalhes jogo: {e}')
        flash('Erro ao consultar detalhes jogo', 'danger')
        return redirect(url_for('listar_jogos'))
    except Exception as ex:
        print(f'Erro ao consultar detalhes jogo: {ex}')
        flash(f'Ocorreu um erro ao consultar detalhes jogo', 'danger')
        return redirect(url_for('listar_jogos'))
    finally:
        db_session.close()






if __name__ == '__main__':
    app.run(debug=True, port=5001)

