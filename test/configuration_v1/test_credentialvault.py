from typing import List
from dynatrace import Dynatrace

from dynatrace.configuration_v1.credential_vault import CredentialsResponseElement, CredentialScope, CredentialType
from dynatrace.pagination import PaginatedList



def test_list(dt: Dynatrace):
    credentials = dt.credential_vault.list()

    # type checks
    assert isinstance(credentials, PaginatedList)

    # value checks
    for credential in credentials:
        assert (credential.scope == CredentialScope.SYNTHETIC)
        assert (credential.owner == "bilal.hashmi@dynatrace.com")
        assert (credential.owner_access_only)
        assert (credential.type == CredentialType.USERNAME_PASSWORD)
        break

# test list filtering by credential type username pass
def test_list_filter_type(dt: Dynatrace):
    credentials = dt.credential_vault.list("USERNAME_PASSWORD")

    for c in credentials:
        assert isinstance(c.type, CredentialType)
        assert (c.type == CredentialType.USERNAME_PASSWORD)


    
def test_get(dt: Dynatrace):
    credential = dt.credential_vault.get("CREDENTIALS_VAULT-1A642D7EDEB13FED")

    # type check
    assert isinstance(credential, CredentialsResponseElement)
    assert isinstance(credential.scope, CredentialScope)
    assert isinstance(credential.type, CredentialType)

    # value checks
    assert (credential.name == "bilal2")
    assert (credential.owner == "bilal.hashmi@dynatrace.com")
    assert (credential.description == "No description necessary")
    assert (credential.scope == CredentialScope.SYNTHETIC)
    assert (credential.type == CredentialType.USERNAME_PASSWORD)
    assert (credential.owner_access_only)
