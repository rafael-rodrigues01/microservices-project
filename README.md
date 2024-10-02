## Projeto 

Para o projeto iremos usar uma combinação de microsserviços para criar uma 
versão reduzida de um dos ecossistemas que temos em produção hoje. Ele será
composto pelos seguintes elementos:

* Aplicação de Webhook
* Aplicação de armazenamento de dados
* Aplicação de streaming para produto
* Banco de Dados SQL (Postgres)
* Banco de Dados NoSQL (MongoDB)
* Serviço de Mensageria (Kafka, RabbitMQ ou Pub/Sub)

![Diagrama do Projeto](https://i.imgur.com/nD3b674.png)

Agora iremos detalhar ponto a ponto as aplicações necessarias.

### Aplicação de Webhook

A aplicação de webhook terá como intuito receber dados criptografados de eventos
de três tipos diferentes e após isso será enviado para um tópico de serviço de 
mensageria.
A aplicação será exposta na porta `:9999` e terá 3 endpoints.

* `POST /person` - Evento do tipo pessoa.

Deverá aceitar uma requisição em formato JSON com os seguintes parâmetros:

| Atributos | Tipo     | Descrição                                        |
|-----------|----------|--------------------------------------------------|
| time      | datetime | Data e hora na qual o evento foi disparado.      |
| body      | str      | Conteudo do evento criptografado no formato RSA. |
| event     | str      | Flag identificadora do evento recebido.          |

O campo `body` deverá ser descripatado e após esse processo será obtido o
payload referente ao evento de person. O evento segue o seguinte schema:

| Atributos  | Tipo  | Descrição                                            |
|------------|-------|------------------------------------------------------|
| person_id  | int   | Identificador unico para a pessoa.                   |
| name       | str   | Nome da pessoa.                                      |
| email      | str   | Email da pessoa.                                     |
| gender     | str   | Genero da pessoa (M ou F).                           |
| birth_date | date  | Data de nascimento no formato YYYY/MM/DD             |
| address    | str   | Endereço residencial da pessoa.                      |
| salary     | float | Valor do salario da pessoa                           |
| cpf        | str   | Codigo do CPF (Cadastro de Pessoa Fisica) da pessoa. |

Após o processo o dado deverá ser encaminhado para o serviço de mensageria em um topico especifico para os eventos de `person`.

* `POST /account` - Evento do tipo conta.

Deverá aceitar uma requisição em formato JSON com os seguintes parâmetros:

| Atributos | Tipo     | Descrição                                        |
|-----------|----------|--------------------------------------------------|
| time      | datetime | Data e hora na qual o evento foi disparado.      |
| body      | str      | Conteudo do evento criptografado no formato RSA. |
| event     | str      | Flag identificadora do evento recebido.          |

O campo `body` deverá ser descripatado e após esse processo será obtido o
payload referente ao evento de account. O evento segue o seguinte schema:

| Atributos         | Tipo  | Descrição                                            |
|-------------------|-------|------------------------------------------------------|
| account_id        | int   | Identificador unico para a pessoa.                   |
| status_id         | int   | Identificador unico para o status.                   |
| due_day           | int   | Dia de vencimento da conta.                          |
| person_id         | int   | Identificador unico para a pessoa.                   |
| balance           | float | Balanço da conta.                                    |
| avaliable_balance | float | Balanço disponivel da conta.                         |

Após o processo o dado deverá ser encaminhado para o serviço de mensageria em um topico especifico para os eventos de `account`.

* `POST /card` - Evento do tipo cartão.

Deverá aceitar uma requisição em formato JSON com os seguintes parâmetros:

| Atributos | Tipo     | Descrição                                        |
|-----------|----------|--------------------------------------------------|
| time      | datetime | Data e hora na qual o evento foi disparado.      |
| body      | str      | Conteudo do evento criptografado no formato RSA. |
| event     | str      | Flag identificadora do evento recebido.          |

O campo `body` deverá ser descripatado e após esse processo será obtido o
payload referente ao evento de card. O evento segue o seguinte schema:

| Atributos         | Tipo  | Descrição                                            |
|-------------------|-------|------------------------------------------------------|
| card_id           | int   | Identificador unico para a cartão.                   |
| card_number       | str   | Numero do cartão.                                    |
| account_id        | int   | Identificador unico para a conta.                    |
| status_id         | int   | Identificador unico para o status.                   |
| limit             | float | Limite do cartão.                                    |
| expiration_date   | str   | Expiração do cartão.                                 |

Após o processo o dado deverá ser encaminhado para o serviço de mensageria em um topico especifico para os eventos de `card`.


### Aplicação de Armazenamento de Dados.

A aplicação de armazenamento de dados tem como intuito receber os dados dos eventos 
de `person`, `account` e `card` e salvar esses dados em um banco `SQL`. Os dados devem
ser inseridos em tabelas referentes ao tipo de evento correspondente. Após salvar o 
dado no banco deverá ser enviado para um topico no serviço de mensageria uma mensagem de confirmação de dado armazenado. Além isso o dado
deverá ser inserido ou atualizado de respeitando a ordem dos eventos recebidos.
A aplicação será exposta na porta `:9998` e terá 3 endpoints.


* `POST /person`
* `POST /account`
* `POST /card`

### Aplicação de streaming para produto.

A aplicação de streaming para produto tem como intuito consolidar dados dos 3 eventos 
em um schema unico para uma futura aplicação de um produto especifico. Esse dado deverá ser armazenado em um banco `NoSQL` utilizando o seguinte schema:

```json
{
    "cpf": "str",
    "nome": "str",
    "id_pessoa": 0,
    "email": "str",
    "genero": "str",
    "data_nascimento": "00/00/0000",
    "endereco": "str",
    "salario": 0.0,
    "contas": [{
        "id_conta": 0,
        "status": 0,
        "dia_vencimento": 0,
        "saldo": 0.0,
        "saldo_disponivel": 0.0
    }]
    "cartoes": [{
        "id_cartao": 0,
        "num_cartao": "str",
        "status": 0,
        "limite": 0.0,
        "data_expiracao": "str"
    }]
}
```

Ao receber um evento de trigger a aplicação deverá buscar no banco `SQL` o dado mais
atual para aquele evento e com isso deverá consolidar o dado no banco `NoSQL`. É 
sugerido que essa aplicação tenha 3 endpoints como as demais aplicações e deverá ser exposta na porta `:9997`.

## Infra

Todas as aplicações deverá seguir o mesmo padrão de infraestrutura. Elas deverão
ter duas instâncias gerenciadas por um `load balance`. 

![Diagrama de Aplicação](https://i.imgur.com/1Tbu9hz.png)

Cada instância de aplicação deverá utilizar as seguintes informações de infraestrutura:
```yml
resources:
    limits:
        cpus: '0.25'
        memory: '0.5GB'
```
As demais dependencias, como bancos de dados e serviços de mensagerias deverão ser hospedadas em containers com infraestrutura maxima:
```yml
resources:
    limits:
        cpus: '0.75'
        memory: '1.5GB'
```
As imagens das aplicações criadas deverão ser disponibilizadas via [docker hub](https://hub.docker.com/) para facilitar avaliação e testes das aplicações.
## Testes Unitários
As aplicações deverão ter testes unitários utilizando alguma ferramenta de testes. 
Os testes deverão ter covarage de 80% da aplicação.
## Monitoramento
Deverá ser criado um painel de monitoramento utilizando as ferramentas de sua escolha
para poder acompanhar as requisições de uma aplicação especifica e acompanhar o fluxo
como todo.