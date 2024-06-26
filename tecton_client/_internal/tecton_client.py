from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import httpx
from httpx import HTTPStatusError

from tecton_client._internal.data_types import (
    GetFeatureServiceMetadataResponse,
    GetFeaturesResponse,
    MetadataOptions,
    RequestOptions,
)
from tecton_client._internal.utils import (
    build_get_feature_service_metadata_request,
    build_get_features_request,
    get_default_headers,
    validate_request_args,
)
from tecton_client.exceptions import convert_exception


class TectonClient:
    """A lightweight http client for interacting with features in Tecton. For the full sdk, use tecton-sdk"""

    def __init__(
        self, url: str, api_key: str, default_workspace_name: Optional[str] = None, client: httpx.Client = None
    ):
        """Constructor for the client

        Args:
            url: base url to your tecton cluster. Ex: http://explore.tecton.ai
            api_key: See https://docs.tecton.ai/docs/ for how to create an api key.
            default_workspace_name: The workspace from which the features will be retrieved.
                Can be over-ridden by individual function calls.
            client: An httpx.Client, allowing you to provide finer-grained customization on the request behavior,
                such as default timeout or connection settings. See https://www.python-httpx.org/ for more info.
        """
        self.url = url
        self.default_workspace_name = default_workspace_name
        self._api_key = api_key
        self._base_url = urljoin(url, "/api/v1/")
        self._paths = {
            "get_features": urljoin(self._base_url, "feature-service/get-features"),
            "get_feature_service_metadata": urljoin(self._base_url, "feature-service/metadata"),
        }

        headers = get_default_headers(api_key)
        if client is None:
            self._client = httpx.Client(headers=headers)
        else:
            self._client = client
            # add the headers to the existing client headers
            self._client.headers.update(headers)

    def get_features(
        self,
        *,
        feature_service_name: Optional[str] = None,
        feature_service_id: Optional[str] = None,
        join_key_map: Optional[Dict[str, Union[int, str, type(None)]]] = None,
        request_context_map: Optional[Dict[str, Any]] = None,
        metadata_options: Optional[MetadataOptions] = None,
        workspace_name: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
        allow_partial_results: bool = False,
    ) -> GetFeaturesResponse:
        validate_request_args(feature_service_id, feature_service_name, workspace_name, self.default_workspace_name)
        if not workspace_name:
            workspace_name = self.default_workspace_name
        request_data = build_get_features_request(
            feature_service_id=feature_service_id,
            feature_service_name=feature_service_name,
            join_key_map=join_key_map,
            request_context_map=request_context_map,
            workspace_name=workspace_name,
            metadata_options=metadata_options,
            allow_partial_results=allow_partial_results,
            request_options=request_options,
        )
        resp = self._client.post(self._paths["get_features"], json=request_data)

        try:
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise convert_exception(exc) from exc

        return GetFeaturesResponse.from_response(resp.json())

    def get_feature_service_metadata(
        self,
        *,
        feature_service_name: Optional[str] = None,
        feature_service_id: Optional[str] = None,
        workspace_name: Optional[str] = None,
    ) -> GetFeatureServiceMetadataResponse:
        validate_request_args(feature_service_id, feature_service_name, workspace_name, self.default_workspace_name)
        if not workspace_name:
            workspace_name = self.default_workspace_name
        request_data = build_get_feature_service_metadata_request(
            feature_service_id=feature_service_id,
            feature_service_name=feature_service_name,
            workspace_name=workspace_name,
        )
        resp = self._client.post(url=self._paths["get_feature_service_metadata"], json=request_data)
        try:
            resp.raise_for_status()
        except HTTPStatusError as exc:
            raise convert_exception(exc) from exc

        return GetFeatureServiceMetadataResponse.from_response(resp.json())
