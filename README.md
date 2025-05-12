# Wishlist

Projeto referente à lista de produtos favoritos de clientes.

Este projeto foi desenvolvido com **Python 3.11**, utilizando o framework **Django** e está conteinerizado com **Docker**.

---

## Como rodar o projeto localmente

1. **Build e inicialização dos containers:**

```bash
  docker compose build
  docker compose up
```

O projeto estará disponível em: http://localhost:8000

Acesse o painel de administração em: http://localhost:8000/admin/

2. **Criar um superusuário:**

```bash
  docker compose run web python manage.py createsuperuser
```


## Collection do Postman
Para facilitar os testes locais, há uma collection do Postman no projeto:

Caminho: `postman/wishlist.postman_collection.json`

Como usar:
```
Abra o Postman

Clique em Import > File

Selecione o arquivo acima

Após importar, você poderá testar todos os endpoints da API localmente
```

## Autenticação

A API utiliza autenticação via token.

1. Gere um token acessando o endpoint:

```
  POST /api/token/
```

Use esse token para autenticar todas as requisições protegidas (via header Authorization: Token <seu_token>).


## Endpoints Disponíveis

Autenticação:

- `POST /api/token/` - Gera o token de autenticação

Clientes:

- `GET /api/clients/` - Lista todos os clientes
- `GET /api/clients/<client_id>/` - Detalha um cliente pelo ID
- `POST /api/clients/` - Cria um novo cliente
- `PUT /api/clients/<client_id>/` - Atualiza completamente os dados de um cliente
- `PATCH /api/clients/<client_id>/` - Atualiza parcialmente os dados de um cliente
- `DELETE /api/clients/<client_id>/` - Remove um cliente

Lista de Favoritos:

- `POST /api/clients/<client_id>/favorites/` - Adiciona um produto aos favoritos do cliente.
- `GET /api/clients/<client_id>/favorites/` - Lista os produtos favoritos do cliente.
- `DELETE /api/clients/<client_id>/favorites/<product_id>/` - Remove um produto da lista de favoritos do cliente.


## Rodando os testes

Para executar os testes unitários:

```bash
  docker compose run --rm web pytest
```

