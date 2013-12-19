# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from novaclient import base

from keystoneclient.v2_0 import client




class Provisioner(base.Resource):
    def __repr__(self):
        return "<Host: %s>" % self.host_name

    def _add_details(self, info):
        dico = 'resource' in info and info['resource'] or info
        for (k, v) in dico.items():
            setattr(self, k, v)
    pass

class ProvisionerManager(base.ManagerWithFind):
    resource_class = Provisioner

    def provision(self, host, pcrs, client_info):
        url="/os-tpmprovision"
        
        body={"host": host, "pcrs": pcrs}
        response,data = self.api.client.post(url, body=body)
        keystone = client.Client(username=client_info.user,tenant_id=client_info.tenant_id,auth_url=client_info.auth_url,password=client_info.password)
        id=keystone.attestation.create(hostname = data['hostname'], pcrs = pcrs, auth_type = data['auth_type'], uuid = data['uuid'], pkey = data['pkey'], pure_hash = data['pure_hash'], service = "compute")
        data['id']=id
        return data
    def list(self):
        pass
