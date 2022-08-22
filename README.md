# jupyterhub_server
Scripts to create and start jupyterhub services with multiple conda enviroments 🚀
The files that will be created depends on a configuration file located in src/config.py

### Configuration file located on src/config.py
```python
CONFIG = [
    {   "env_name": "env1",
        "conda_path": "/home/user1/miniconda3/envs/env1",
        "ld_library_path": "/usr/local/cuda-11.0/lib64",
        "config_file_path": "/opt/cryptanalysis_servers_shared_folder/jupyterhub_conf"
    },
    {
        "env_name": "env2",
        "conda_path": "/home/user2/miniconda3/envs/env2",
        "ld_library_path": "/usr/local/cuda-11.0/lib64",
        "config_file_path": "/opt/cryptanalysis_servers_shared_folder/jupyterhub_conf"
    },
]
```
The configuration above will create two configurable-http-proxy services, two jupyterhub services and two jupyterhub_config.py files that will expand the variables needed to be able to use the power of the GPU on the jupyter notebooks (LD_LIBRARY_PATH for example)
If another conda environment is needed, add another dictionary to the CONFIG list with the same keys above. Run the create-files make command again to update all the services and configurations.
### Run the following commands with make
```bash
make install-nodejs # downloads and installs nodejs on the machine in /opt/nodejs...
make create-environment # creates the virtualenv environment to run the scrips (install jinja2)
make create-files # creates the services, configuration files and the script that starts all the services
make start-services # runs the script created by create-files. It copies and starts all the services mentioned on the config.py file
make check-services # reads the output of every service to check if all the services are running.
```