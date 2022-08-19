"""Create services files implementation"""
import os
from src.content_creator import ContentCreator
from src.templates import JUPYTERHUB_SERVICE, JUPYTERHUB_CONFIG, HTTP_PROXY_SERVICE, START_SERVICES_SCRIPT
from src.config import CONFIG


class CreateServices:
    """Exposes methods for file service creation (jupyterhub and configurable-http-proxy)
    """

    def __init__(self, output):
        """Constructor
        """
        self.sfc = ContentCreator()
        self.dir_path = self.sfc.dir_path
        self.output = output

    def create_services_files(self):
        """Creates jupyterhub_config.py and configurable_http_proxy service file
        """
        base_port = 8000
        base_jup_port = 8080
        services = []
        for config in CONFIG:
            services_vars = {}
            service_description = f"Jupyterhub service for {config['env_name']} environment"
            conda_environment = config["conda_path"]
            config_file = os.path.join(
                config["config_file_path"], f"jupyterhub_config_{config['env_name']}.py")
            data = self.sfc.create_jupyterhub_service_content(
                service_description, conda_environment, config_file, JUPYTERHUB_SERVICE)
            jupyter_service =  f"jupyterhub_{config['env_name']}.service"
            jupyter_service_file = os.path.join(
                self.output,jupyter_service)
            self.sfc.create_file(jupyter_service_file, data)
            services_vars['jupyter_service_file'] = jupyter_service
            services_vars["opt_path"] = config["config_file_path"]

            api_port = base_port + 1
            port = base_jup_port + 1
            ld_library_path = config['ld_library_path']
            config_content = self.sfc.create_jupyterhub_config_content(
                api_port, ld_library_path, port, JUPYTERHUB_CONFIG)
            config_file = f"jupyterhub_config_{config['env_name']}.py"
            config_file_name = os.path.join(self.output, config_file)
            self.sfc.create_file(config_file_name, config_content)
            services_vars['config_file'] = config_file
            
            http_service_description = f"Http proxy service for {config['env_name']} environment"
            http_service_content = self.sfc.create_http_proxy_content(
                http_service_description, base_port, api_port, port, HTTP_PROXY_SERVICE)
            http_service_file = f"http_proxy_{config['env_name']}.service"
            http_file_name = os.path.join(self.output, http_service_file)
            self.sfc.create_file(http_file_name, http_service_content)
            services_vars['http_service_file'] = http_service_file

            base_port += 2
            base_jup_port += 2
            services.append(services_vars)

        script_file = os.path.join(self.output, "start_services.sh")
        script_content = self.sfc.create_start_service_script(services, START_SERVICES_SCRIPT)
        self.sfc.create_file(script_file, script_content)



