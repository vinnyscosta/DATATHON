### 📌 **Resumo Atualizado das Rotas da API**  

A API agora permite **gerenciar usuários, notícias, interações e buscar recomendações** do modelo pronto.  

---

## **🔹 Rotas de Usuários**  
📌 **Gerenciamento de usuários e histórico de navegação**  
- `POST /users` → **Cadastrar um usuário** (logado ou anônimo).  
- `GET /users/{user_id}` → **Consultar dados do usuário** (inclui histórico).  
- `POST /users/{user_id}/history` → **Atualizar histórico de leitura do usuário**.  
- `GET /users/{user_id}/history` → **Buscar histórico de leitura do usuário**.  

---

## **🔹 Rotas de Notícias**  
📌 **Gerenciamento das matérias disponíveis**  
- `POST /articles` → **Cadastrar uma nova notícia**.  
- `GET /articles/{article_id}` → **Buscar uma notícia pelo ID**.  
- `GET /articles` → **Listar todas as notícias**.  
- `PUT /articles/{article_id}` → **Atualizar uma notícia existente**.  
- `DELETE /articles/{article_id}` → **Remover uma notícia**.  

---

## **🔹 Rotas de Recomendações**  
📌 **Buscar previsões do modelo treinado**  
- `GET /recommendations/{user_id}` → **Obter recomendações personalizadas para um usuário**.  
- `GET /recommendations/popular` → **Obter notícias populares para novos usuários (cold-start)**.  
- `GET /recommendations/similar/{article_id}` → **Buscar notícias similares a uma notícia específica**.  

---

## **🔹 Rotas de Interações dos Usuários**  
📌 **Registro de interações com as notícias**  
- `POST /interactions` → **Registrar uma interação do usuário** (cliques, tempo de leitura, scroll).  
- `GET /users/{user_id}/interactions` → **Listar todas as interações do usuário**.  

