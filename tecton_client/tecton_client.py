import asyncio

from tecton_client.http_client import TectonHttpClient
from tecton_client.requests import GetFeaturesRequest
from tecton_client.responses import GetFeaturesResponse


class TectonClient:
    """Class to represent a Tecton Client.

    A `TectonClient` object represents a client that can be used to interact with the Tecton FeatureService API.
    It provides a collection of methods to make HTTP requests to the respective API endpoints and returns the response
    as a Python object.

    Example:
        >>> tecton_client = TectonClient(url, api_key)

    """

    def __init__(self, url: str, api_key: str) -> None:
        """Initialize the parameters required to make HTTP requests.

        Args:
            url (str): The Tecton Base URL
            api_key (str): API Key for authenticating with the FeatureService API. See `Authenticating with an API key
                <https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-inference/\
                reading-online-features-for-inference-using-the-http-api#creating-an-api-key-to-authenticate-to-\
                the-http-api>`_  for more information.
        """
        self._tecton_http_client = TectonHttpClient(url, api_key)
        self._loop = asyncio.new_event_loop()

    def get_features(self, request: GetFeaturesRequest) -> GetFeaturesResponse:
        """Makes a request to the /get-features endpoint and returns the response in the form of a
        :class:`GetFeaturesResponse` object

        Args:
            request (GetFeaturesRequest): The :class:`GetFeaturesRequest` object with the request parameters

        Returns:
            GetFeaturesResponse: The :class:`GetFeaturesResponse` object representing the response from the HTTP API

        Example:
            >>> tecton_client = TectonClient(url, api_key)
            >>> join_key_map = {"example_join_key": "example_join_value"}
            >>> request_context_map = {"example_request_context": "example_string_value"}
            >>> request_data = GetFeatureRequestData(join_key_map, request_context_map)
            >>> request = GetFeaturesRequest(
            ...     feature_service_name="example_feature_service",
            ...     request_data=request_data,
            ...     workspace_name="example_workspace",
            ... )
            >>> response = tecton_client.get_features(request)
            `response.feature_values()` returns a dictionary of {feature_name: `FeatureValue`} pairs.

            To access the values of the features stored as :class:`FeatureValue` objects in the dictionary, use:
            >>> print([feature.feature_value for feature in response.feature_values.values()])
            [1, 2, 3, "test_feature", ["test", "array"]]

        """
        response = self._loop.run_until_complete(
            self._tecton_http_client.execute_request(request.ENDPOINT, request.to_json())
        )
        return GetFeaturesResponse(response)

    @property
    def is_closed(self) -> bool:
        """Returns True if the client has been closed, False otherwise."""
        return self._tecton_http_client.is_closed

    def close(self) -> None:
        """Closes the client, releasing allocated resources and allowing connection reuse.

        Important for proper resource management and graceful termination of the client.

        """
        self._loop.run_until_complete(self._tecton_http_client.close())
        self._loop.close()
