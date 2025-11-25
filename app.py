import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError

from models import local_session, Usuario, Plataforma, Genero, Jogo
from sqlalchemy import select

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@app.route('/')
def home():
    return render_template('intergames.html')


@app.route('/add_jogo', methods=['GET', 'POST'])
def \
    post_jogos():
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
            url_img=request.form['form_url_img']
        )
        db_session = local_session()
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

    return render_template('add_jogos.html')


@app.route('/plataforma')
def listar_plataformas():
    db_session = local_session()
    try:
        plataformas_sql = select(Plataforma)
        resultado = db_session.execute(plataformas_sql).scalars()
        return render_template('listar_plataformas.html', var_plataformas=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de Plataformas: {e}')
        return redirect(url_for('listar_plataformas'))
    except Exception as ex:
        print(f'Erro ao consultar plataformas: {ex}')
        return redirect(url_for('listar_plataformas'))
    finally:
        db_session.close()


@app.route('/desenvolvedoras')
def listar_desenvolvedoras():
    return render_template('listar_desenvolvedoras.html')


@app.route('/jogo')
def listar_jogos():
    db_session = local_session()
    try:
        jogos_sql = select(Jogo)
        resultado = db_session.execute(jogos_sql).scalars()
        return render_template('listar_jogos.html', var_jogos=resultado)
    except SQLAlchemyError as e:
        print(f'Erro de jogo: {e}')
        return redirect(url_for('listar_jogos'))
    except Exception as ex:
        print(f'Erro ao consultar jogo: {ex}')
        return redirect(url_for('listar_jogos'))
    finally:
        db_session.close()


@app.route('/genero')
def listar_generos():
    return render_template('listar_generos.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)

