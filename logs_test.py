from nova.api.openstack import extensions
from nova.api.openstack import wsgi


ALIAS = 'os-logs'
authorize = extensions.os_compute_authorizer(ALIAS)


class LogsTestController(wsgi.Controller):

    @extensions.expected_errors(404)
    def index(self, req, server_id):
        pass

    @extensions.expected_errors(404)
    @wsgi.response(204)
    def delete_all(self, req, server_id):
        return {"info": "call the function delete_all"}

    @extensions.expected_errors(404)
    @wsgi.response(204)
    def delete_me(self, req, server_id):
        return {"info": "call the function delete_me"}


class LogsTest(extensions.V21APIExtensionBase):
    """Logs Test support."""

    name = "LogsTest"
    alias = ALIAS
    version = 1

    def get_resources(self):
        resources = [
            extensions.ResourceExtension(
                ALIAS, LogsTestController(),
                collection_actions={'delete_all': 'DELETE'},
                member_actions={'delete_me': 'DELETE'},
                parent=dict(member_name='server', collection_name='servers'))]
        return resources

    def get_controller_extensions(self):
        return []
