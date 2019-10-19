## Instalação do ambiente virtual do python
Instale o virtualenv em seu ambiente:
```bash
# apt-get install virtualenvwrapper python3-virtualenv
```

## Criando um ambiente virtual
```bash
mkvirtualenv syscemit
```

## Abrindo o ambiente Virtual
```bash
workon syscemit
```

## Instalando as dependências
```bash
pip install -r dev-requirements.txt
```

## Iniciando e populando o banco
```bash
./console initdb
```

## Criando os scripts de migração do banco de dados.
### Cria a estrutura dos scripts de migração.
```bash
./console db init
```
### Verificando por mudanças e criando os scripts dos scripts migração.
```bash
./console db migrate
```
### Aplica as mudanças. 
```bash
./console db upgrade
```

## Criando um usuário administrativo
```bash
./console user create -n admin -l admin -t 1
```

## Criando um usuário funcionário
```bash
./console user create -n user -l user -t 2
```

## Rodando servidor e aplicação
```bash
./console run
```

## Abrindo modo console
```bash
./console shell
```

## Saindo do ambiente Virtual
```bash
deactivate
```
