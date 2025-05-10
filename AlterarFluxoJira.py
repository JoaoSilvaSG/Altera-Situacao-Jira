import json
import requests
import sys
from requests.auth import HTTPBasicAuth

JIRA_BASE_URL = ""  # Ex: https://suaempresa.atlassian.net
JIRA_USER = "login"
JIRA_TOKEN = "token"
TRANSITION_ID = "101"  # ID da transição para "Aguardando Qualidade"

def altera_status(issue_key: str, transition_id: str):
    """Altera o status de uma issue no Jira."""
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}/transitions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "transition": {
            "id": transition_id
        }
    })
    response = requests.post(
        url,
        data=payload,
        headers=headers,
        auth=HTTPBasicAuth(JIRA_USER, JIRA_TOKEN)
    )

    if response.status_code != 204:
        print(f"Erro ao alterar {issue_key}: {response.text}")
    else:
        print(f"Issue {issue_key} alterada com sucesso.")

def buscar_issues_por_versao(versao: str, projeto: str):
    """Busca todas as issues com status Resolved e determinada versão."""
    query = (
        f"/rest/api/2/search?"
        f"jql=project={projeto} AND status=Resolved AND fixVersion=\"{versao}\""
        f"&fields=key"
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(
        JIRA_BASE_URL + query,
        headers=headers,
        auth=HTTPBasicAuth(JIRA_USER, JIRA_TOKEN)
    )

    if response.status_code != 200:
        print(f"Erro ao buscar issues: {response.text}")
        return []

    return [issue["key"] for issue in response.json().get("issues", [])]

def tratar_versao(versao: str, produto: str):
    """Ajusta a versão com base na regra de quantidade de pontos. Na nossa situação, a versão normalmente é algo como 2.30.5.10"""
    pontos = versao.count('.')
    limite = 2 if produto.lower() == 'neoplus' else 3

    if pontos > limite:
        partes = versao.split('.')
        return '.'.join(partes[:limite])
    return versao

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <versao> <produto>")
        return

    versao = tratar_versao(sys.argv[1], sys.argv[2])
    produto = sys.argv[2]

    projeto_jira = 'NP' if produto.lower() == 'neoplus' else 'NEO'
    nome_versao_jira = f"{versao} {produto}"

    issues = buscar_issues_por_versao(nome_versao_jira, projeto_jira)
    for issue_key in issues:
        altera_status(issue_key, TRANSITION_ID)

if __name__ == "__main__":
    main()
