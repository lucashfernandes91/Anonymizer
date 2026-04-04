# Anonymizer

![Anonymizer](static/logo.png)

## 🌟 Sobre o Projeto

O **Anonymizer** é uma ferramenta poderosa que vai além de simplesmente remover metadados de imagens. Ele oferece:

- 🛡️ Uma camada de anonimização digital instantânea.
- 🔒 Um escudo contra rastreamento invisível em imagens.
- 🧹 Uma forma de zerar completamente o histórico oculto de um arquivo.

Com o Anonymizer, você pode garantir a privacidade total de suas imagens, eliminando qualquer dado sensível que possa estar embutido nelas.

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

## 🚀 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/anonymizer.git
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

- **Python**
- **Django**
- **HTML5**
- **CSS3**
- **JavaScript**

---

## 📂 Estrutura do Projeto

```
.
├── anonymizer/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── __init__.py
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
├── templates/
│   └── home.html
├── db.sqlite3
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

- **Email:** seuemail@exemplo.com
- **LinkedIn:** [Seu Nome](https://www.linkedin.com/in/seu-perfil)
- **GitHub:** [seu-usuario](https://github.com/seu-usuario)