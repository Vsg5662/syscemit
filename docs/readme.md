## Instalação do ambiente virtual do python
Instale o virtualenv em seu ambiente:
```
bash

# apt-get install virtualenvwrapper python3-virtualenv
```

## Criando um ambiente virtual
mkvirtualenv syscemit

## Saindo do ambiente Virtual
deactivate

## Abrindo o ambiente Virtual
workon syscemit

## Iniciando e populando o banco
bash app.sh initdb

## Populando o banco
bash app.sh user create -n admin -l admin -t 1

## Rodando servidor e aplicação
bash app.sh run

## Abrindo modo console
bash app.sh shell