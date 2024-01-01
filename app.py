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
    SELECT *
  FROM (
           SELECT COUNT( * ) n_equipas
             FROM Equipa
       )
       JOIN
       (
           SELECT COUNT( * ) n_estadios
             FROM Estadios
       )
       JOIN
       (
           SELECT COUNT( * ) n_jogadores
             FROM Jogador
       )
       JOIN
       (
           SELECT COUNT( * ) n_jogos
             FROM Jogo
       )
       JOIN
       (
           SELECT sum(resultado_pais_1 + resultado_pais_2) n_gols
             FROM jogo
       )
       JOIN
       (
           SELECT sum(attendance) n_bilhetes
             FROM Jogo
       )
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Fontes
@APP.route('/fontes/')
def get_fontes():
  return render_template('fontes.html')

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
     
  es_jogos = db.execute(
      '''
      SELECT *
      FROM Jogo
      WHERE nome_estadio = ?;
      ''', [expr]).fetchall()
  
  attendance = db.execute(
      '''
      SELECT sum(attendance) AS sum
      FROM Jogo
      WHERE nome_estadio = ?;
      ''', [expr]).fetchone()

  return render_template('estadio.html', estadio=estadio, es_jogos=es_jogos, attendance=attendance)

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
     
  eq_jogos = db.execute(
      '''
      select *
      from Jogo
      where nome_pais_1 = ? or nome_pais_2 = ?
      ''', [expr,expr]).fetchall()
  
  eq_jogador = db.execute(
      '''
      select *
      from Jogador
      where nome_pais = ?
      ''', [expr]).fetchall()

  return render_template('equipa.html', equipa=equipa, eq_jogos=eq_jogos, eq_jogador=eq_jogador)

# Lista de Grupos e Jogos
@APP.route('/grupos/')
def list_grupos():
  grupos_list = db.execute(
      '''
      SELECT e1.nome_grupo,
       e1.nome_pais as pais_1,
       e2.nome_pais as pais_2,
       e3.nome_pais as pais_3,
       e4.nome_pais as pais_4
  FROM Equipa e1
       JOIN
       Equipa e2 ON e1.nome_grupo = e2.nome_grupo
       JOIN
       Equipa e3 ON e2.nome_grupo = e3.nome_grupo
       JOIN
       Equipa e4 ON e3.nome_grupo = e4.nome_grupo
  WHERE e1.nome_pais != e2.nome_pais AND 
       e1.nome_pais != e3.nome_pais AND 
       e1.nome_pais != e4.nome_pais AND 
       e2.nome_pais != e3.nome_pais AND 
       e2.nome_pais != e4.nome_pais AND 
       e3.nome_pais != e4.nome_pais
  GROUP BY e1.nome_grupo;
      ''').fetchall()
  
  grupos = db.execute(
      '''
      SELECT e.nome_grupo, 
       j.*
      FROM Jogo j
       JOIN
       Equipa e ON e.nome_pais = j.nome_pais_1
      ORDER BY match_no;
      ''').fetchall() 
  return render_template('grupos-list.html', grupos=grupos, grupos_list=grupos_list)

# Grupo
@APP.route('/grupos/<expr>/')
def get_grupo(expr):
  gp_name = db.execute(
      '''
      SELECT e.nome_grupo, 
       j.*
      FROM Jogo j
       JOIN
       Equipa e ON e.nome_pais = j.nome_pais_1
      WHERE e.nome_grupo = ?;
      ''', [expr]).fetchone()
  
  gp = db.execute(
      '''
      SELECT e.nome_grupo, 
       j.*
      FROM Jogo j
       JOIN
       Equipa e ON e.nome_pais = j.nome_pais_1
      WHERE e.nome_grupo = ?;
      ''', [expr]).fetchall()

  if gp is None:
     abort(404, 'Nome do grupo {} não existe.'.format(expr))

  return render_template('grupo.html', gp_name=gp_name, gp=gp)

# Jogo
@APP.route('/grupos/<int:id>/')
def get_jogo(id):
  jogo = db.execute(
      '''
      SELECT e.nome_grupo,
       j.*
      FROM Jogo j
       JOIN
       Equipa e ON e.nome_pais = j.nome_pais_1
      WHERE match_no = ?;

      ''', [id]).fetchone()

  if jogo is None:
     abort(404, 'O jogo {} não existe.'.format(id))

  return render_template('jogo.html', jogo=jogo)