import os
import pathlib
from ServiceConfig import ServiceConfig


class PdfFile:
    def __init__(self, tenant: str):
        self.service_config = ServiceConfig()
        self.tenant = tenant

    def save(self, pdf_file_name: str, file: bytes):
        if not os.path.exists(f"{self.service_config.docker_volume_path}/to_extract"):
            os.mkdir(f"{self.service_config.docker_volume_path}/to_extract")

        if not os.path.exists(
            f"{self.service_config.docker_volume_path}/to_extract/{self.tenant}"
        ):
            os.mkdir(
                f"{self.service_config.docker_volume_path}/to_extract/{self.tenant}"
            )

        path = f"{self.service_config.docker_volume_path}/to_extract/{self.tenant}/{pdf_file_name}"

        file_path_pdf = pathlib.Path(path)
        file_path_pdf.write_bytes(file)
