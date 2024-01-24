# Visão Geral do Projeto

## Recursos
Este projeto é uma API de gestão de produtos para um e-commerce. Na aplicação, é possível entrar como
cliente, ter acesso à lista de produtos disponíveis, avaliá-los, adicioná-los ao carrinho de compras e
criar uma venda com os produtos selecionados do carrinho (não precisa ser todos).

A aplicação também oferece um sistema de recomendação para produtos com a mesma categoria e conta com
sistema de tags para dar mais informações sobre o produto.

Todas as consultas que retornam várias entidades, como, por exemplo, a página principal da loja - que contém
vários produtos, são paginadas e possuem no máximo até 10 entidades por página. Ou seja, caso a loja
tenha centenas de produtos cadastrados, eles não serão processados e enviados de uma vez só!

Além disso, os valores de algumas entidades são atualizados automaticamente de forma assíncrona! 
Isto é: se um cliente avaliar um produto, o servidor vai recalcular sua avaliação média. 
Se um produto mudar de nome, seu SKU (Unidade de Manutenção de Estoque) vai também ser reprocessado e 
alterado.

Para tornar o processamento da API mais leve e diminuir o tempo de resposta, o sistema conta com um
sistema de cache para as operações de leitura. Ou seja, não é necessário processar a mesma chamada duas vezes.

Alguns recursos são reprocessados com mais frequência que outros. Por exemplo: as informações de um
cliente são mantidas em cache por no máximo 60 segundos, pois têm maior possibilidade de serem alteradas.
Já as informações de um produto são mantidas em cache por algumas horas, pois a chance da descrição de
um produto mudar não é alta.

Por fim, alguns recursos em cache podem variar de acordo com o cliente que está autenticado. Por exemplo:
as informações do carrinho de compras de um cliente são mantidas em um cache específico para cada cliente
individual.

## Privilégios

Como administrador, além de ter acesso a todas essas funcionalidades supracitadas, também tem um maior
poder de administrar os recursos do e-commerce.

Por exemplo: um cliente não pode excluir ou alterar um produto; não pode gerenciar fornecedores.
Mas o administrador da loja pode.

Além de só permitir acesso a certas funcionalidades com permissões extras, o sistema também impede que
clientes comuns tenham mais poder do que deveriam!

Por exemplo: um cliente não pode adicionar um produto no carrinho de outro cliente, ou até mesmo
acessar o carrinho deste outro usuário.

Agora, se você não está autenticado no sistema, também não tem problema! Você ainda tem acesso a ações
de leitura não sensíveis enquanto usuário anônimo, como poder ver os produtos disponíveis,
as avaliações dos usuários etc.

## Entidades

Essa é a visão geral de todos os modelos da aplicação. Mais detalhes sobre os atributos de cada entidade
do sistema e como se relacionam são encontrados no seguinte diagrama:

![uml](./assets/img/3.png)


# Execução
### Algumas orientações:
__Certifique-se que possui o Docker e Docker Compose instalados com os seguinte comandos:__

```shell
docker -v
# Docker version 25.0.0, build e758fe5

docker compose version
# Docker Compose version v2.24.1
```

Caso não estejam instalados, instale o __docker engine__ clicando [AQUI](https://docs.docker.com/engine/install/).

### Subir o Ambiente
Antes de poder utilizar a aplicação, é necessário usar o docker para subir os serviços. Para isso,
use o seguinte comando:
```shell
docker compose --env-file dev.env up --build -d

# => [worker internal] load build definition from Dockerfile                                                     0.0s
# => => transferring dockerfile: 411B                                                                            0.0s
# => [worker internal] load metadata for docker.io/library/python:3.12-slim                                      1.5s
# => [worker internal] load metadata for docker.io/library/python:3.12                                           1.5s
# => [worker internal] load .dockerignore                                                                        0.0s

#...
```

Aguarde o docker compose subir todos os serviços. O último a subir é o __drf__.

Quando todos os serviços estiverem no ar, você já poderá acessar o Swagger para visualizar a documentação
completa da api no link: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

![swagger](./assets/img/7.png)

### Criando um Superusuário
Após todos os serviços subirem, será necessário criar um superusuário para poder ter acesso a todos os
serviços da API. Alguns são protegidos de modo que somente administradores podem executar algumas ações,
como registrar um produto no banco de dados.

Para isso, não vamos utilizar o comando padrão do Django para criar um superusuário, pois ele não cria
os relacionamentos entre os modelos necessários. Vamos utilizar o comando 
customizado __createsupercustomer__:

```shell
sudo docker exec drf python3.12 manage.py createsupercustomer --username <nome-de-usuário> --password <senha>

# sudo docker exec drf python3.12 manage.py createsupercustomer --username ajai --password ajai
# Successfully created admin customer!
```

Desa forma, criamos um superusuário (ou supercliente) com nome de usuário __ajai__ e senha __ajai__.

## Applicação OAuth2

Agora, precisamos criar uma aplicação OAuth para nos prover um token de acesso para a próxima etapa.

Mas antes, é necessário fazer login como administrador. Vamos usar a conta que acabamos de criar!
Faça login com o nome de usuário __ajai__ e senha __ajai__ no link:
[http://localhost:8000/admin/](http://localhost:8000/admin/)

![login como ajai](./assets/img/1.png)

Quado fizer login, verá esta tela:

![admin](./assets/img/2.png)

Finalmente podemos criar a API de autenticação para prover o token de acesso!

Para isso, acesse a url [http://localhost:8000/api/o/applications/](http://localhost:8000/api/o/applications/)

Você verá esta tela:

![inicio oauth](./assets/img/4.png)

Clique no link para registrar sua aplicação.

![registrar app](./assets/img/5.png)

__Preencha dessa forma!__ (o nome da aplicação fica a seu critério)

### Agora, é necessário fazer algumas coisas:
- __Salve o Client id e o Client secret (autogerados) no arquivo dev.env para não os perder, dessa forma:__
```dotenv
# ...

CLIENT_ID=yrg2P9W5D5aCmShGdvJj8iWfM1DZUanZajr5rt5v
CLIENT_SECRET=rmoM9UVEI4sgCEPlrTGcHZ8bMcmkvd0jWx2CWzh7d213lWxeW4ZqKNgYbUpnonmyOEXz0ZlyFIXJeqkHvSIqvNaE3WiJYzpsvTZ5raiWCy5guItUjDsSEc8d4Lv7cUKw
```

- __Salvar sua aplicação pressionando o botão de salvar__

![aplicação salva](./assets/img/6.png)

Pronto! Agora o sistema está pronto para gerenciar servir os tokens da autenticação OAuth!

### Recuperar o token de acesso

Neste momento, vá até a interface do Swagger (instrução de como acessar no início do documento) e
navegue até o endpoint nomeado como *__o__*:

![o](./assets/img/9.png)

Altere o Content-Type de *__application/json__* para *__application/x-www-form-urlencoded__*

Agora é só preencher o formulário dessa forma e executá-lo
(use seu Client id, Client secret e informações de usuário):

Copie seu token de acesso (o texto ao lado da chave _access_token_ sem as aspas)

![form](./assets/img/10.png)
![response](./assets/img/11.png)

## Token JWT
### Após recuperar o token de acesso da API do OAuth, é necessário usar esse token para conseguir um token de acesso JWT.

Execute esse comando no seu terminal (usando o access_token recuperado na etapa anterior):

```shell
curl \
-H 'Authorization: Bearer <access_token>' \
http://localhost:8000/api/token/ | json_pp
```

Agora, copie o valor da chave *__access__* no corpo da resposta:
```shell
curl \                                         
-H 'Authorization: Bearer lSUeSo8ZaBRmSeiXS9M3TyACnnQLo9' \
http://localhost:8000/api/token/ | json_pp
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   483  100   483    0     0   9470      0 --:--:-- --:--:-- --:--:--  9470
{
   "access" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2MTM0MDk5LCJpYXQiOjE3MDYxMzM3OTksImp0aSI6IjUyMDBjNTE2YjFmMTQ2MjA5NGU4NDdlZGIyYzk2ZGUwIiwidXNlcl9pZCI6M30.v74tW3kml56JMjDPgi16KvWkR3lRcgAb8Dnb1bViu7M",
   "refresh" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNjIyMDE5OSwiaWF0IjoxNzA2MTMzNzk5LCJqdGkiOiJiNzlhNGYwNDYzNjU0MzViYTBkNDRlOTZkM2UyMTdlOCIsInVzZXJfaWQiOjN9.NM0SxmxIR1qxq-vtzsK5QNC9jaaTgS-MyQQ26_mwG1A"
}
```

Após isso, vá até o topo da interface do Swagger e clique no botão verde em que está escrito
"Authorize" no canto inferior direito:

![authorize](./assets/img/12.png)

E preencha o campo a autenticação JWT com o token que acabou de conseguir:

![jwt](./assets/img/13.png)

## Você está autenticado!
### Como criamos uma conta de admin e acabamos de nos autenticar, temos acesso a todas as rotas da aplicação!

### Agora, só navegar pela documentação da API e utilizá-la!
