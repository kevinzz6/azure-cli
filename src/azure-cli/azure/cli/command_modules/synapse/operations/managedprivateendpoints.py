# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.util import sdk_no_wait
from .._client_factory import cf_synapse_managedprivateendpoints_factory

def create_Managed_private_endpoints(cmd, workspace_name, managed_private_endpoint_name, managed_virtual_network_name, properties, no_wait=False):
    client = cf_synapse_managedprivateendpoints_factory(cmd.cli_ctx, workspace_name)
    return sdk_no_wait(no_wait, client.create,
                       managed_private_endpoint_name, managed_virtual_network_name, properties)
def get_Managed_private_endpoints(cmd, workspace_name, managed_private_endpoint_name, managed_virtual_network_name):
    client = cf_synapse_managedprivateendpoints_factory(cmd.cli_ctx, workspace_name)
    return client.get(managed_private_endpoint_name, managed_virtual_network_name)

def list_Managed_private_endpoints(cmd, workspace_name, managed_virtual_network_name):
    client = cf_synapse_managedprivateendpoints_factory(cmd.cli_ctx, workspace_name)
    return client.list(managed_virtual_network_name)

def delete_Managed_private_endpoints(cmd, workspace_name,managed_private_endpoint_name, managed_virtual_network_name):
    client = cf_synapse_managedprivateendpoints_factory(cmd.cli_ctx, workspace_name)
    return client.delete(managed_private_endpoint_name, managed_virtual_network_name)