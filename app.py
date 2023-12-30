import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) n_equipas FROM Equipa)
    JOIN
      (SELECT COUNT(*) n_estadios FROM Estadios)
    JOIN
      (SELECT COUNT(*) n_grupos FROM Grupo)
    JOIN 
      (SELECT COUNT(*) n_jogadores FROM Jogador)
    JOIN 
      (SELECT COUNT(*) n_jogos FROM Jogo)
    JOIN 
      (SELECT COUNT(*) n_canais FROM Canal)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Lista de Estadios
@APP.route('/estadios/')
def list_estadios():
  estadios = db.execute(
      '''
      SELECT *
      FROM Estadios
      ORDER BY nome_estadio
      ''').fetchall()
  return render_template('estadios-list.html', estadios=estadios)
  
# Estádio
@APP.route('/estadios/<expr>/')
def get_estadio(expr):
  estadio = db.execute(
      '''
      select *
      from Estadios
      where nome_estadio = ?
      ''', [expr]).fetchone()

  if estadio is None:
     abort(404, 'Nome do estádio {} não existe.'.format(expr))

  return render_template('estadio.html', estadio=estadio)

# Lista de Canais
@APP.route('/canais/')
def list_canais():
  canais = db.execute(
      '''
      SELECT *
      FROM Contrato
      ORDER BY nome_canal
      ''').fetchall()
  return render_template('canais-list.html', canais=canais)

# Lista de Jogadores
@APP.route('/jogadores/')
def list_jogadores():
  jogadores = db.execute(
      '''
      SELECT *
      FROM Jogador
      ORDER BY jogador_id
      ''').fetchall()
  return render_template('jogador-list.html', jogadores=jogadores)

# Jogador
@APP.route('/jogadores/<int:id>/')
def get_jogador(id):
  jogador = db.execute(
      '''
      SELECT *
      FROM Jogador
      WHERE jogador_id = ?
      ''', [id]).fetchone()

  if jogador is None:
     abort(404, 'Esta id {} de jogador não existe.'.format(id))
  
  return render_template('jogador.html', jogador=jogador)

# Lista de Equipas
@APP.route('/equipas/')
def list_equipas():
  equipas = db.execute(
      '''
      SELECT *
      FROM Equipa
      ORDER BY nome_pais
      ''').fetchall()
  return render_template('equipas-list.html', equipas=equipas)

# Equipa
@APP.route('/equipas/<expr>/')
def get_equipa(expr):
  equipa = db.execute(
      '''
      select *
      from Equipa
      where nome_pais = ?
      ''', [expr]).fetchone()

  if equipa is None:
     abort(404, 'Nome da equipa {} não existe.'.format(expr))

  return render_template('equipa.html', equipa=equipa)

# Lista de Grupos e Jogos
@APP.route('/grupos/')
def list_grupos():
  grupos = db.execute(
      '''
      SELECT *
      FROM Jogo j
       JOIN
       (
           SELECT g.nome_grupo,
                  e.nome_pais
             FROM Grupo g
                  JOIN
                  Equipa e ON g.equipa_1 = e.nome_pais OR 
                              g.equipa_2 = e.nome_pais OR 
                              g.equipa_3 = e.nome_pais OR 
                              g.equipa_4 = e.nome_pais
       )
       ON j.equipa_1 = nome_pais
      ORDER BY nome_grupo,
          match_no;
      ''').fetchall()
  
  grupos_list = db.execute(
      '''
      SELECT *
      FROM Grupo
      ''').fetchall()
  return render_template('grupos-list.html', grupos=grupos, grupos_list=grupos_list)
