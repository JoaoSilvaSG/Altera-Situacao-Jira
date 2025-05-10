# Altera-Situacao-Jira

Este script em Python automatiza a transição de status de issues no Jira após um processo de build, atualizando requisitos resolvidos pela programação para o status **"Aguardando Qualidade"**, com base na versão e no nome do produto.

## 📌 Objetivo

Após cada build, é necessário atualizar os requisitos finalizados no Jira para uma nova etapa de QA. Este script:

- Busca todas as issues com status **"Resolved"** e a versão informada.
- Altera essas issues para o status desejado automaticamente.
- Elimina o trabalho manual pós-compilação.

## ⚙️ Funcionamento

1. O script espera dois parâmetros:
   - **versão** (ex: `5.4.2.1`)
   - **produto** (ex: `NeoPlus` ou `NeoPDV`)

2. Ele faz o ajuste da versão conforme regras específicas:
   - `NeoPlus`: versão com **2** pontos (ex: `5.4`)
   - Outros: versão com **3** pontos (ex: `5.4.2`)

3. Busca todas as issues no Jira com:
   - Projeto: `NP` para NeoPlus, `NEO` para os demais.
   - Status: `Resolved`
   - FixVersion igual à versão ajustada.

4. Atualiza o status dessas issues para "Aguardando Qualidade".

## 🔒 Segurança

- A URL base do Jira, login e token estão ocultados por segurança.
- Substitua os valores de `JIRA_BASE_URL`, `JIRA_USER` e `JIRA_TOKEN` por suas credenciais reais no início do script.

