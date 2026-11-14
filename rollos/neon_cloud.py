"""Provisionamento inicial de projetos Neon para a conta do próprio usuário.

A chave pessoal é fornecida em tempo de execução e nunca é persistida pelo RollOS.
Para distribuição pública, substituir este fluxo de chave manual pelo OAuth oficial
do Neon após aprovação como parceiro comercial.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import requests


API_BASE = "https://console.neon.tech/api/v2/"


class NeonProvisioningError(RuntimeError):
    """Erro seguro e legível ao provisionar recursos no Neon."""


@dataclass(frozen=True)
class NeonProject:
    project_id: str
    name: str
    region_id: str
    connection_uri: str | None


class NeonProvisioner:
    """Cliente mínimo da Neon Management API, usando a chave do usuário."""

    def __init__(self, api_key: str, session: requests.Session | None = None,
                 timeout: float = 25.0) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("Informe uma chave de API do Neon.")
        self._api_key = api_key.strip()
        self._session = session or requests.Session()
        self._timeout = timeout

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        headers = dict(kwargs.pop("headers", {}))
        headers.update({
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
        })
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
        try:
            response = self._session.request(
                method, urljoin(API_BASE, path.lstrip("/")),
                headers=headers, timeout=self._timeout, **kwargs,
            )
        except requests.RequestException as exc:
            raise NeonProvisioningError(
                "Não foi possível conectar ao Neon. Verifique a internet e tente novamente."
            ) from exc
        if not response.ok:
            detail = ""
            try:
                payload = response.json()
                detail = payload.get("message") or payload.get("error") or ""
            except (ValueError, AttributeError):
                pass
            suffix = f" Detalhe: {detail[:300]}" if detail else ""
            raise NeonProvisioningError(
                f"Neon respondeu com HTTP {response.status_code}.{suffix}"
            )
        try:
            data = response.json()
        except ValueError as exc:
            raise NeonProvisioningError("O Neon retornou uma resposta inválida.") from exc
        if not isinstance(data, dict):
            raise NeonProvisioningError("O Neon retornou um formato inesperado.")
        return data

    def list_organizations(self) -> list[dict[str, str]]:
        data = self._request("GET", "organizations?limit=100")
        rows = data.get("organizations", [])
        if not isinstance(rows, list):
            raise NeonProvisioningError("Não foi possível interpretar as organizações da conta Neon.")
        result: list[dict[str, str]] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            org_id = row.get("id") or row.get("org_id")
            name = row.get("name") or org_id
            if org_id:
                result.append({"id": str(org_id), "name": str(name)})
        if not result:
            raise NeonProvisioningError(
                "Nenhuma organização foi encontrada. Confira se a chave pertence à sua conta Neon."
            )
        return result

    def create_project(
        self, org_id: str, name: str = "rollos-cloud",
        region_id: str = "aws-us-east-1",
    ) -> NeonProject:
        if not org_id or not org_id.strip():
            raise ValueError("Selecione a organização da conta Neon.")
        if not name or len(name) > 256:
            raise ValueError("O nome do projeto deve ter entre 1 e 256 caracteres.")
        if region_id not in {"aws-us-east-1", "aws-us-east-2", "aws-eu-central-1", "aws-ap-southeast-1"}:
            raise ValueError("Região não suportada nesta configuração inicial.")
        data = self._request("POST", "projects", json={
            "project": {
                "name": name.strip(),
                "region_id": region_id,
                "pg_version": 17,
                "branch": {
                    "name": "production",
                    "database_name": "rollos",
                },
            },
            "org_id": org_id,
        })
        project = data.get("project", data)
        if not isinstance(project, dict):
            raise NeonProvisioningError("O Neon não retornou os dados do projeto criado.")
        project_id = project.get("id") or project.get("project_id")
        if not project_id:
            raise NeonProvisioningError(
                "O Neon recebeu a solicitação, mas não retornou o identificador do projeto. "
                "Confira a conta Neon antes de tentar criar novamente."
            )
        connection_uri = None
        uris = data.get("connection_uris") or project.get("connection_uris") or []
        if isinstance(uris, list) and uris:
            first = uris[0]
            if isinstance(first, dict):
                connection_uri = first.get("connection_uri") or first.get("uri")
            elif isinstance(first, str):
                connection_uri = first
        return NeonProject(
            project_id=str(project_id),
            name=str(project.get("name") or name.strip()),
            region_id=str(project.get("region_id") or region_id),
            connection_uri=connection_uri,
        )
