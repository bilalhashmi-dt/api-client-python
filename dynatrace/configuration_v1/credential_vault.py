"""
Copyright 2021 Dynatrace LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from dynatrace.dynatrace_object import DynatraceObject
from enum import Enum
from requests import Response
from typing import List, Optional, Union, Dict, Any

from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class CredentialScope(Enum):
    ALL = "ALL"
    EXTENSION = "EXTENSION"
    SYNTHETIC = "SYNTHETIC"


class CredentialType(Enum):
    CERTIFICATE = "CERTIFICATE"
    USERNAME_PASSWORD = "USERNAME_PASSWORD"
    TOKEN = "TOKEN"


class CredentialVaultService:
    ENDPOINT = "/api/config/v1/credentials"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    
    def list(self, credential_type: Optional[str] = None) -> PaginatedList["CredentialsResponseElement"]:
        """ Lists all credentials for synthetic monitors stored in your environment.

        :param credential_type: OPTIONAL Filters the result by the specified credentials type.

        :return: CredentialsResponse class object list
        """
        params = {"type": credential_type}
        
        return PaginatedList(CredentialsResponseElement, self.__http_client, self.ENDPOINT, target_params=params, list_item="credentials")


    def get(self, _id: str) -> "CredentialsResponseElement":
        """ Gets the metadata of the specified credentials set

        :param id: The Dynatrace entity ID of the required credentials set

        :return: CredentialsResponse class object
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{_id}").json()
        return CredentialsResponseElement(raw_element=response)
    

    def put(self, _id: str, data: Dict[str, Any]) -> "Response":
        """ Updates the specified credentials set

        :param id: The Dynatrace entity ID of the required credentials set
        :param data: The JSON body of the request. Contains parameters of the credentials set.

        :return: 201 returns the ID. 204 returns nothing
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{_id}", params=data, method="PUT")


    def post(self, data: Dict[str, Any]) -> str:
        """ Updates the specified credentials set

        :param data: The JSON body of the request. Contains parameters of the new credentials set.

        :return: the ID of the newly created Credentials Vault object
        """
        return self.__http_client.make_request(path=self.ENDPOINT, params=data, method="POST").json()["id"]


    def delete(self, _id: str) -> "Response":
        """ Deletes the specified credentials set

        :param id: The Dynatrace entity ID of the required credentials set

        :return: no response from API - return Response object
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{_id}", method="DELETE")


class CredentialsResponseElement(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.name: str = raw_element["name"]
        self.id: str = raw_element["id"]
        self.description: str = raw_element["description"]
        self.owner: str = raw_element["owner"]
        self.owner_access_only: bool = raw_element["ownerAccessOnly"]
        self.scope: CredentialScope = CredentialScope(raw_element["scope"])
        self.type: CredentialType = CredentialType(raw_element["type"])

