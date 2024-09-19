from datetime import datetime
import requests
from typing import Dict, Any, Optional
from uuid import UUID
from fastapi import HTTPException
from app.config import settings
import json


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class WidgetService:
    def __init__(self):
        self.base_url = settings.WIDGET_SERVICE_URL
        self.headers = {
            "X-API-Key": settings.WIDGET_SERVICE_TOKEN,
            "Content-Type": "application/json",
        }

    def create_widget(self, widget_data: Dict[str, Any]) -> Dict[str, Any]:
        json_data = json.dumps(widget_data, cls=UUIDEncoder)
        response = requests.post(
            f"{self.base_url}/widgets", data=json_data, headers=self.headers
        )
        return self._handle_response(response)

    def update_widget(
        self, widget_id: UUID, widget_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        json_data = json.dumps(widget_data, cls=UUIDEncoder)
        response = requests.put(
            f"{self.base_url}/widgets/{widget_id}", data=json_data, headers=self.headers
        )
        return self._handle_response(response)

    def delete_widget(self, widget_id: UUID) -> Dict[str, Any]:
        response = requests.delete(f"{self.base_url}/widgets/{widget_id}")
        return self._handle_response(response)

    def get_widget_interactions(
        self, widget_id: UUID, client_reference_id: Optional[str] = None
    ) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/widgets/{widget_id}/interactions",
            params={"client_reference_id": client_reference_id},
            headers=self.headers,
        )
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Widget not found")
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Widget service error: {response.text}",
            )


widget_service = WidgetService()
