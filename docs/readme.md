## Instalação do ambiente virtual do python
Instale o virtualenv em seu ambiente:
```
bash

# apt-get install virtualenvwrapper python3-virtualenv
```

## Criando um ambiente virtual
mkvirtualenv syscemit

## Abrindo o ambiente Virtual
workon syscemit

## Instalando as dependências
pip install -r dev-requirements.txt

## Iniciando e populando o banco
./console initdb

## Populando o banco
./console user create -n admin -l admin -t 1

## Rodando servidor e aplicação
./console run

## Abrindo modo console
./console shell

## Saindo do ambiente Virtual
deactivate
