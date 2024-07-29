# Base de Dados FIFA WC 2022

## Sobre

Projeto de Base de Dados onde utilizei as estatísticas reais da Copa do Mundo FIFA 2022 para criar um website que permite navegar e visualizar de forma simples todos os dados disponíveis.

O projeto foi primariamente desenvolvido em Python e SQL, e utilizei também Templates Jinja para gerar HTMLs utilizando os dados obtidos quando um endpoint faz querries à base de dados.

### Criação da DB

Foi utilizado um ficheiro csv para o povoamento dos dados, criado a partir da base de dados do “FBref.com” e outras fontes. Após isso foi feito um tratamento dos dados, muitos dos quais continham erros como caracteres representados de forma errada, ou virgulas extras.

Para o povoamento dos dados, criei um programa em python utilizando a biblioteca Pandas, que extrai os dados do ficheiro csv para um dataframe (Estrutura de Dados da biblioteca Pandas) e através da seleção de campos especificos e da remoção de entradas duplicadas, cria sub-dataframes correspondentes a cada tabela do modelo relacional, para tabelas que tem um ID proprio, baseado na posição que a entrada se encontrava no CSV. As informações contidas nos sub-dataframes, são inseridas nas tabelas da BD, por comandos SQL, executados usando o modulo sqlite3 do python.

### Fontes

#### Lista de Mundiais Ganhos por cada país:

**https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals**

#### Base de Dados “Fifa WC 2022 Qatar Data Analysis” , criada a partir da base de dados do “FBref.com”, website referência que acompanha as estatísticas dos jogadores e equipas ao redor do mundo:

**https://github.com/shreeparab1890/Fifa-WC-2022-Qatar-Data-Analysis-EDA/blob/main/README.md**

**https://fbref.com/en/comps/1/stats/World-Cup-Stats**

#### Lotação máxima e informações de cada estádio retirados do website oficial da FIFA na época do mundial através do “web.archive.org”:

**https://web.archive.org/web/20221002103900/https://hospitality.fifa.com/2022/en/the-stadiums/**

#### Canais emissores do mundial, países para o qual foram emitidos e o tipo de serviço que foi prestado:

**https://www.sportspromedia.com/insights/analysis/world-cup-2022-guide-teams-sponsors-kit-suppliers-stadiums-broadcasters/?zephr_sso_ott=Ia5v9A**

## Como executar localmente

### Instalação de software

Precisa de ter o Python 3 e o gestor de pacotes pip instalado.
Experimente executar `python3 --version` e `pip3 --version` para saber
se já estão instalados. Em caso negativo, pode por exemplo em Ubuntu
executar:

```
sudo apt-get install python3 python3-pip
```

Tendo Python 3 e pip instalados, deve instalar a biblioteca `Flask` executando o comando:

```
pip3 install --user Flask
```

### Execução de servidor da aplicação

Para iniciar o servidor da aplicação basta executar `python3 server.py` no terminal

De seguida abra no seu browser **http://127.0.0.1:9000** ou **http://localhost:9000**
