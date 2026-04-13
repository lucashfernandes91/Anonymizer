# Anonymizer

## 🌟 Sobre o Projeto

O **Anonymizer** é uma ferramenta poderosa que vai além de simplesmente remover metadados de imagens. Ele oferece:

- 🛡️ Uma camada de anonimização digital instantânea.
- 🔒 Um escudo contra rastreamento invisível em imagens.
- 🧹 Uma forma de zerar completamente o histórico oculto de um arquivo.

Com o Anonymizer, você pode garantir a privacidade total de suas imagens, eliminando qualquer dado sensível que possa estar embutido nelas.

Acesse em: **https://anonymizer.com.br**

---

## 🧠 Explicação Técnica

Quando uma imagem é capturada (celular, câmera, print, etc.), ela carrega muito mais do que apenas pixels. Ela pode conter:

- 🌍 Localização GPS exata.
- 📱 Modelo do dispositivo.
- 📅 Data e hora da captura.
- 📷 Configurações da câmera.
- 🆔 Identificadores únicos do arquivo.
- 📝 Histórico de edição.

Essas informações ficam escondidas nos chamados metadados (EXIF). O Anonymizer resolve isso de forma definitiva.

---

## 🔥 O que o Anonymizer faz

O Anonymizer não apenas "remove metadados". Ele faz algo muito mais poderoso:

1. **Reconstrói a imagem do zero**
   - A imagem é reprocessada e convertida para RGB.
   - Um novo arquivo é gerado pixel por pixel.
   - Nenhuma estrutura interna original é reaproveitada.

2. **Elimina completamente qualquer rastro**
   - Todos os metadados são descartados.
   - Nenhuma informação oculta sobrevive.
   - Nem mesmo softwares forenses conseguem recuperar dados anteriores.

3. **Gera uma nova identidade digital**
   - Novo arquivo.
   - Nova estrutura interna.
   - Zero ligação com a origem.

É como se a imagem tivesse sido criada do zero naquele momento.

---

## 🖼️ Resultado Final

Uma imagem:

- Totalmente limpa.
- Irreversivelmente anonimizada.
- Pronta para envio, publicação ou compartilhamento com segurança.

---

## ⚡ Experiência do Usuário (UX)

O fluxo é propositalmente simples:

1. O usuário entra no site.
2. Arrasta a imagem (drag and drop).
3. Solta na área.
4. A limpeza acontece automaticamente.
5. A imagem limpa já fica disponível para download.

- Sem cadastro.
- Sem configuração.
- Sem fricção.

---

## 🌐 API REST

O Anonymizer disponibiliza uma API REST pública para integração programática — sem autenticação, sem cadastro, gratuita.

**Documentação completa:** https://anonymizer.com.br/api-docs/

### Endpoint

```
POST https://anonymizer.com.br/api/
Content-Type: multipart/form-data
```

**Parâmetro:** `image` — arquivo JPG, PNG ou WEBP (máx 10MB)

**Resposta:** arquivo JPEG anonimizado diretamente no corpo da resposta.

### 📋 Headers de resposta

| Header | Descrição |
|---|---|
| `X-Campos-Removidos` | Total de campos EXIF removidos |
| `X-Tem-GPS` | `true` se havia GPS na imagem original |
| `X-Lat` / `X-Lon` | Coordenadas extraídas |
| `X-Dispositivo` | Fabricante e modelo do dispositivo |
| `X-Data-Foto` | Data e hora em que a foto foi tirada |

### 💻 Exemplo cURL

```bash
curl -X POST https://anonymizer.com.br/api/ \
  -F "image=@foto.jpg" \
  --output foto_anonimizada.jpg \
  -D headers.txt
```

### 🐍 Exemplo Python

```python
import requests

with open("foto.jpg", "rb") as f:
    response = requests.post(
        "https://anonymizer.com.br/api/",
        files={"image": f}
    )

if response.status_code == 200:
    with open("foto_anonimizada.jpg", "wb") as out:
        out.write(response.content)
    print("GPS removido:", response.headers.get("X-Tem-GPS"))
    print("Campos removidos:", response.headers.get("X-Campos-Removidos"))
```

### ⚠️ Erros

| Código | Descrição |
|---|---|
| `400` | Imagem inválida, formato não suportado ou arquivo muito grande |
| `429` | Muitas requisições. Aguarde e tente novamente |

---

## 🚀 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/lucashfernandes91/anonymizer.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd anonymizer
   ```

3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # No Windows
   source .venv/bin/activate  # No Linux/Mac
   ```

4. Instale as dependências do projeto:
   ```bash
   uv pip install -r requirements.txt
   ```

5. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário (opcional, para acessar o admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Execute o servidor:
   ```bash
   python manage.py runserver
   ```

8. Acesse o projeto no navegador:
   ```
   http://127.0.0.1:8000
   ```

---

## 🛠️ Tecnologias Utilizadas

- **Python / Django**
- **Pillow** — reconstrução RGB pixel a pixel
- **Django REST Framework** — API REST
- **Nominatim / OpenStreetMap** — reverse geocoding
- **HTML5, CSS3, JavaScript** puro — sem frameworks frontend

---

## 📂 Estrutura do Projeto

```
.
├── apps/
│   └── anonymizer/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── services.py
│       ├── tests.py
│       ├── urls.py
│       ├── views.py
│       ├── migrations/
│       └── static/
│       │    └── anonymizer/
│       │       └── css/
│       │           └── home.css
│       │       └── js/
│       │           └── home.js
│       │       └── img/
│       │           └── favicon.svg
│       │           └── og-image.png
│       └── templates/
│           └── 429.html
│           └── api.html
│           └── home.html
│           └── llms.txt
│           └── robots.txt
│           └── sitemap.xml
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
└── README.md
```

---

## 🤝 Contribuição

Contribuições são sempre bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção de bug:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça o commit das suas alterações:
   ```bash
   git commit -m 'Adiciona minha nova feature'
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

## 📜 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 💬 Contato

- **Email:** lucashfernandes@yahoo.com.br
- **LinkedIn:** [Lucas H. Fernandes](https://www.linkedin.com/in/lucas-holtz/)
- **GitHub:** [lucashfernandes91](https://github.com/lucashfernandes91)
