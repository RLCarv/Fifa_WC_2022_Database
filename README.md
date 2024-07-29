# Base de Dados FIFA WC 2022

## Sobre

Cada "endpoint" da aplicação deve efectuar uma ou mais interrogações à base de dados e utilizar os dados obtidos para gerar HTML usando templates Jinja.
Deve colocar as templates de geração de HTML (uma por "endpoint") na pasta `templates`.

### Fontes

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
