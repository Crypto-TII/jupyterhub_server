"""Service file creator"""

import os
from jinja2 import Template


class ContentCreator:
    """Uses jinja2 templates to build service files (jupyterhub, configurable-http-proxy)
    """

    def __init__(self):
        self.file_name = os.path.abspath(__file__)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def create_http_proxy_content(description: str, port: str, api_port: str, jup_port: str, template: str) -> str:
        """Creates configurable-http-proxy service file

        Args:
            description (str): description of the service
            port (str): port to be loaded by configurable-http-proxy
            api_port (str): the jupyterhub port
            jup_port (str): the error port for jupyterhub
            template (str): jinja2 template

        Returns:
            str: _description_
        """
        j_template = Template(template)
        content = j_template.render(
            description=description, port=port, api_port=api_port, jup_port=jup_port)
        return content

    @staticmethod
    def create_jupyterhub_config_content(api_port: str, ld_library_path: str, port: str, template: str) -> str:
        """Creates jupyterhub configuration file

        Args:
            api_port (str): the port exposed by jupyterhub
            ld_library_path (str): variable needed to expand it on the configuration file
            port (str): port of the jupyterhub
            template (str): jinja2 template

        Returns:
            str: returns the filled up template
        """
        j_template = Template(template)
        content = j_template.render(
            api_port=api_port, ld_library_path=ld_library_path, port=port)
        return content

    @staticmethod
    def create_jupyterhub_service_content(description: str, conda_env: str, config_file: str, template: str) -> str:
        """Creates jupyterhub service file

        Args:
            description (str): service description
            conda_env (str): conda environment full path
            config_file (str): location of the configuration file
            template (str): jinja2 template

        Returns:
            str: returns the filled up template
        """
        j_template = Template(template)
        content = j_template.render(
            service_description=description,
            conda_environment=conda_env,
            config_file=config_file)

        return content

    @staticmethod
    def create_start_service_script(services: dict, template: str) -> str:
        """_summary_

        Args:
            services (dict): _description_
            template (str): _description_

        Returns:
            str: _description_
        """
        j_template = Template(template)
        content = j_template.render(services=services)
        return content

    @staticmethod
    def create_file(file_name: str, data: str) -> None:
        """Creates a file with the data content

        Args:
            file_name (str): location of the file
            data (str): content of the file
        """
        with open(file_name, "w", encoding='utf-8') as file_buffer:
            file_buffer.write(data)
