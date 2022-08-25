"""Templates"""

JUPYTERHUB_SERVICE="""[Unit]
Description={{ service_description }}
After=syslog.target network.target

[Service]
Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/node-v16.16.0-linux-x64/bin:{{ conda_environment }}/bin"
ExecStart={{ conda_environment }}/bin/jupyterhub -f {{ config_file }}

[Install]
WantedBy=multi-user.target
"""
HTTP_PROXY_SERVICE="""[Unit]
Description={{ description }}
After=syslog.target network.target

[Service]
Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/node-v16.16.0-linux-x64/bin"
ExecStart=/opt/node-v16.16.0-linux-x64/bin/configurable-http-proxy --ip=0.0.0.0 --port {{ port }} --api-ip 127.0.0.1 --api-port {{ api_port }} --error-target http://0.0.0.0:{{ jup_port }}/hub/error

[Install]
WantedBy=multi-user.target
"""

JUPYTERHUB_CONFIG="""c.JupyterHub.cleanup_servers = False
c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.auth_token = 'CONFIGPROXY_AUTH_TOKEN'
c.ConfigurableHTTPProxy.api_url = 'http://localhost:{{ api_port }}'
c.Spawner.environment = {
        'LD_LIBRARY_PATH': '{{ ld_library_path }}'
}
c.JupyterHub.hub_connect_ip = '0.0.0.0'
c.JupyterHub.hub_port = {{ port }}
"""

START_SERVICES_SCRIPT="""#/bin/bash
{% for service in services %}
if [[ -d {{ service.conda_path }} ]]; then
  sudo {{ service.conda_path }}/bin/pip install jupyterhub jupyterlab 
  sudo cp -v {{ service.http_service_file }} /etc/systemd/system/
  sudo cp -v {{ service.jupyter_service_file }} /etc/systemd/system/
  sudo cp -v {{ service.config_file }} {{ service.opt_path }}/
fi 
{% endfor %}
sudo systemctl daemon-reload
{% for service in services %}
if [[ -d {{ service.conda_path }} ]]; then
  sudo systemctl start {{ service.http_service_file }}
  sudo systemctl status {{ service.http_service_file }} >> services_output.txt
  sudo systemctl start {{ service.jupyter_service_file }}
  sudo systemctl status {{ service.jupyter_service_file }} >> services_output.txt
fi
{% endfor %}
"""