# SACS - Sistema de Agendamento de Consultas

Projeto desenvolvido por **Lennon Patti** como parte do **Projeto Integrador Transdisciplinar II (PIT II)** do curso de **Sistemas de Informação** da **Universidade Cruzeiro do Sul – UNIFRAN**.

O SACS é uma aplicação web desenvolvida em **Python (Flask)** com **MySQL**, que permite **gerenciar pacientes, profissionais, usuários e consultas médicas**, com sistema de **login e controle de acesso**.

---

## 🚀 Tecnologias utilizadas
- **Python 3.10+**
- **Flask** (framework web)
- **MySQL** (banco de dados)
- **HTML e CSS** (interface simples e responsiva)

---

## ⚙️ Como executar o projeto

1. **Instalar as dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Criar o banco de dados**
   ```bash
   mysql -u root -p < db_schema.sql
   ```

3. **Configurar o acesso ao banco**
   Edite o arquivo `config.py` (ou use variáveis de ambiente):
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'sacs_user',
       'password': '1234',
       'database': 'sacs_db'
   }
   ```

4. **Executar o sistema**
   ```bash
   python app.py
   ```

5. **Acessar no navegador**
   ```
   http://localhost:5000
   ```

---

## 🔑 Credenciais padrão
- **Usuário:** admin@sacs.com  
- **Senha:** 1234  
*(perfil administrador — permite criar novos usuários e profissionais)*

---

## 🗂️ Estrutura do Projeto
```
sacs/
│
├── app.py              # aplicação principal Flask
├── config.py           # configuração de acesso ao MySQL
├── db_schema.sql       # script do banco de dados
├── requirements.txt    # dependências do Python
└── templates/          # páginas HTML
    ├── login.html
    ├── index.html
    ├── pacientes.html
    ├── profissionais.html
    ├── usuarios.html
    ├── consultas.html
    └── agendar.html
```

---

## 🧠 Funcionalidades

✅ **Login e autenticação de usuários**  
- Controle de sessão e redirecionamento automático.  
- Perfis: administrador e usuário comum.  

✅ **Cadastro de pacientes**  
- Inclusão e listagem de pacientes.  

✅ **Cadastro de profissionais** *(somente admin)*  
- Permite cadastrar nome e especialidade.  

✅ **Cadastro de usuários** *(somente admin)*  
- Permite criar novos logins e definir o perfil de acesso.  

✅ **Agendamento de consultas**  
- Associação entre paciente, profissional, data e hora.  
- Exibição de status das consultas.  

✅ **Interface intuitiva e organizada**  
- HTML e CSS limpos, com botões de navegação e feedback visual.  

---

## 🧩 Autor

**Lennon Patti**  
Projeto Integrador Transdisciplinar II – 2025  
Curso de **Sistemas de Informação**  
**Universidade Cruzeiro do Sul – UNIFRAN**

---

## 🧾 Observações finais

O projeto **SACS** foi desenvolvido com fins acadêmicos e tem como objetivo demonstrar, de forma prática, a aplicação dos conceitos de **desenvolvimento web**, **integração com banco de dados relacional** e **controle de autenticação**.

O sistema está preparado para futuras melhorias, como:
- Criptografia de senhas (hash);
- Filtros e relatórios de consultas;
- Painel de administração mais completo.
