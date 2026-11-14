import os
import platform
import shutil


def collect_system_info() -> dict[str, str]:
    disk = shutil.disk_usage(os.path.abspath(os.sep))
    return {
        "Sistema hospedeiro": f"{platform.system()} {platform.release()}",
        "Arquitetura": platform.machine(),
        "Processador": platform.processor() or "Não identificado",
        "Python": platform.python_version(),
        "Espaço livre": f"{disk.free / (1024 ** 3):.1f} GB",
    }
