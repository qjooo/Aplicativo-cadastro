# Sistema de Cadastro de Consultas

Um aplicativo para **cadastro de consultas**, com **confirmação automática por e-mail** e **dashboard interativo** para análise dos dados de atendimentos.

---

### Aplicativo de Cadastro (`cadastro.py`)
- Interface desenvolvida com **CustomTkinter**.  
- Cadastro de pacientes com:
  - Nome, e-mail, data da consulta, tipo de tratamento e detalhes.  
  - Escolha do método de pagamento (Pix, Cartão, Dinheiro, etc.).  
  - Suporte a parcelamento no cartão de crédito.  
- Envio automático de **e-mail de confirmação** ao paciente.  
- Salvamento automático dos registros em **consultas.csv**.

### Dashboard de Dados (`app.py`)
- Interface feita com **Streamlit**.  
- Leitura automática do arquivo `consultas.csv`.  
- Exibição de:
  - Lista completa de consultas.  
  - Estatísticas gerais (total, pacientes únicos, retornos etc.).  
  - Gráficos interativos com **Plotly**:
    - Distribuição por tipo de tratamento.  
    - Distribuição por meio de pagamento.  
- Filtros dinâmicos por tipo de tratamento e forma de pagamento.

---

## Tecnologias Utilizadas

- **Python 3.10+**
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Streamlit](https://streamlit.io)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- **smtplib** e **email.mime** (para envio de e-mails)
- **Pandas** e **CSV** (para armazenamento e leitura de dados)
