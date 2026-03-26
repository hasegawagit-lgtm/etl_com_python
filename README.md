
# Pipeline ETL: Personalização de Marketing com IA

Este projeto demonstra um pipeline completo de ETL (Extrair, Transformar, Carregar). O script consome dados de clientes via CSV, utiliza a Inteligência Artificial do Google (Gemini) para gerar mensagens personalizadas de investimento e, por fim, carrega esses dados em uma API REST.

## Fluxo do Projeto

**Extrair**: Leitura de um arquivo dados.csv contendo informações bancárias (nome, conta, agência, saldos).

**Transformar:**
1. Limpeza e padronização de nomes (Proper Case).
2. Formatação de strings (Zfill em agências).
3. Integração com IA: Uso do modelo gemini-1.5-flash para criar dicas de investimento curtas (máx. 100 caracteres) personalizadas para cada usuário.

**Carregar:** Conversão dos dados para o formato JSON esperado pela API e envio via requisições POST.

## Tecnologias Utilizadas
* Python 3.10+
* Pandas: Manipulação e tratamento de dados.
* Google Generative AI (SDK): Geração de conteúdo com IA.
* Requests: Integração com APIs REST.
* Python-dotenv: Gerenciamento de variáveis de ambiente (API Keys).
