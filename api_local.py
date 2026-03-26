from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Usuários Bancários")


class Account(BaseModel):
    id: Optional[int] = None
    number: str
    agency: str
    balance: str
    limit: str


class Card(BaseModel):
    id: Optional[int] = None
    number: str
    limit: str

class News(BaseModel):
    id: Optional[int] = None
    icon: str
    description: str

class Feature(BaseModel):
    id: Optional[int] = None
    icon: str
    description: str

class User(BaseModel):
    id: Optional[int] = None
    name: str
    account: Account
    card: Card
    news: List[News] = []
    features: List[Feature] = []


# --- BANCO DE DADOS FICTÍCIO ---

banco_dados = [
]

# --- ROTAS REST ---
# Rota inicial (GET)
@app.get("/")
def home():
    return {"mensagem": "API está online!"}


@app.get("/users", response_model=List[User])
def listar_usuarios():
    return banco_dados


@app.get("/users/{id}", response_model=User)
def obter_usuario(id: int):
    for user in banco_dados:
        if user["id"] == id:
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


@app.post("/users/", status_code=201)
def criar_usuario(novo_usuario: User):
    if any(u["account"]["number"] == novo_usuario.account.number for u in banco_dados):
        raise HTTPException(status_code=400, detail="Número de conta já cadastrado")

    user_dict = novo_usuario.model_dump()

    # gerar ID de usuário
    if user_dict["id"] is None:
        user_dict["id"] = max([u["id"] for u in banco_dados], default=0) + 1

    # 2gerar ID de conta (usando .get() para evitar KeyError)
    ids_contas = [u["account"].get("id") for u in banco_dados if u["account"].get("id") is not None]
    if user_dict["account"]["id"] is None:
        user_dict["account"]["id"] = max(ids_contas, default=0) + 1

    # gerar ID para cartão
    ids_cards = [u["card"].get("id") for u in banco_dados if u["card"].get("id") is not None]
    if user_dict["card"]["id"] is None:
        user_dict["card"]["id"] = max(ids_cards, default=0) + 1

    # gerar ID para news
    ids_news = [u["news"][0].get("id") for u in banco_dados if u["news"][0].get("id") is not None]
    if user_dict["news"][0]["id"] is None:
        user_dict["news"][0]["id"] = max(ids_news, default=0) + 1

    banco_dados.append(user_dict)
    return user_dict


# 3. UPDATE (Atualizar)
@app.put("/users/{id}", response_model=User)
def atualizar_usuario(id: int, user_atualizado: User):
    for index, user in enumerate(banco_dados):
        if user["id"] == id:
            dados_novos = user_atualizado.model_dump()
            dados_novos["id"] = id  # Garante que o ID não mude
            banco_dados[index] = dados_novos
            return dados_novos

    raise HTTPException(status_code=404, detail="Usuário não encontrado para atualização")

@app.delete("/users/{id}")
def deletar_usuario(id: int):
    for index, user in enumerate(banco_dados):
        if user["id"] == id:
            banco_dados.pop(index)
            return {"mensagem": f"Usuário com ID {id} removido"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

if __name__ == "__main__":
    import uvicorn

    # Lembre-se: rode este script e use o /docs para testar!
    uvicorn.run(app, host="127.0.0.1", port=8000)
