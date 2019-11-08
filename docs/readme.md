# Configuração do Ambiente de Desenvolvimento
## 1. Instalação do ambiente virtual do python
Instale o virtualenv em seu ambiente:
```bash
# apt-get install virtualenvwrapper python3-virtualenv
```

## 1.2 Criando um ambiente virtual
```bash
mkvirtualenv syscemit
```

## 1.3 Abrindo o ambiente Virtual
```bash
workon syscemit
```

## 2. Instalando as dependências
```bash
pip install -r dev-requirements.txt
```

## 3. Iniciando e populando o banco
```bash
./console initdb
```

## 3.1 Criando os scripts de migração do banco de dados.
### 3.1.1 Cria a estrutura dos scripts de migração.
```bash
./console db init
```
### 3.1.2 Verificando por mudanças e criando os scripts dos scripts migração.
```bash
./console db migrate
```
### 3.1.3 Aplica as mudanças.
```bash
./console db upgrade
```

## 3.2 Criando um usuário administrativo.
```bash
./console user create -n admin -l admin -t 1
```

## 3.3 Criando um usuário com perfil de funcionário.
```bash
./console user create -n user -l user -t 2
```

## 3.4 Exibindo os usuários do syscemit.
```bash
./console user list
```

## 3.5 Removendo um usuário do syscemit.
```bash
./console user delete <LOGIN>
```

## 4. Backup e restauração do banco de dados de desenvolvimento.
### 4.1 Realizando o backup do banco de dados de desenvolvimento para um arquivo.
```bash
./seeds/utils/litedump backup seeds/dev-dump storage-dev.db

```

### 4.2 Recuperando o banco de dados desenvolvimento a partir de um arquivo.
```bash
./seeds/utils/litedump restore seeds/dev-dump.gz storage-dev.db
```

## 5. Rodando o servidor de desenvolvimento. Utilize um navegador Web e acesse o sistema através da url [http://localhost:5000](http://localhost:5000)
```bash
./console run
```

## 6. Abrindo um terminal interativo para a interação com sistema. Para sair utilize CTRL+D.
```bash
./console shell
```

## 7. Saindo do ambiente virtual.
```bash
deactivate
```

# Configurando o Ambiente de Produção
## 8. Passos iniciais
Os comandos a seguir deveram ser executados com o usuário root.
Se você estiver utilizando um usuário comum, logue-se utilizando o comando abaixo:
```bash
su -
```

## 8.1 Extraia o arquivo compactado do syscemit para o diretório de instalação.
```bash
tar -xvf syscemit.tar.xz -C /srv
```

## 8.2 Adicione um usuário de sistema para o syscemit.
```bash
adduser --quiet --system --ingroup daemon --no-create-home --home "/srv/syscemit" --shell /bin/bash syscemit
```

# 8.3 Altere as permissões do diretório de instalação do syscemit.
```bash
chown -R syscemit:daemon /srv/syscemit
```

# 8.4 Logue-se com o usuário que acabamos e instale as depêndencias do sistema. Um detalhe é que somente o usuário root pode logar como um usuário de sistema.
```bash
su - syscemit
virtualenv -p /usr/bin/python3 .env
source .env/bin/activate
pip install -r requirements.txt
```

# 8.5 Repita os procedimentos da etapa *3* para criar e popular o banco de dados. Também poderá ser utilizado um backup utilizando o procedimento *4.2*.

# 8.6 Copie os arquivos de inicialização e configuração para seus respectivos diretórios.
```bash
cp docs/syscemit.service /lib/system/system/
cp docs/syscemit /etc/default/syscemit
```

# 8.7 Ative e inicie o serviço. A partir desta etapa você poderá acessar o sistema através de um navegador web.
```bash
systemctl enable syscemit
systemctl start syscemit
```
