"""Creates the services files"""

import os
from src.create_services import CreateServices


if __name__ == "__main__":
    run_dir = os.path.dirname(os.path.realpath(__file__))
    output = os.path.join(run_dir, "output")
    if not os.path.exists(output):
        os.makedirs(output)
    cs = CreateServices(output)
    print(f"Creating files in {output}")
    cs.create_services_files()
    print("Done!")
