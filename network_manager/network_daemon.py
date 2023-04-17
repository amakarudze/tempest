import os
import psycopg2
import psycopg2.extensions
import subprocess
from multiprocessing import Process

from django.conf import settings


env = os.environ.copy()

conn = psycopg2.connect(
    database=env["DATABASE_NAME"],
    host=env["DATABASE_HOST"],
    port=env["DATABASE_PORT"],
    user=env["DATABASE_USER"],
    password=env["DATABASE_PASSWORD"]
)
cur = conn.cursor()


def task():
    cmd = ["sudo", "nmap", "-O", "--osscan-guess" "192.168.1.0/24"]
    result = subprocess.Popen(cmd, stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print(result)


if __name__ == "__main__":
    process = Process(daemon=True, target=task)
    process.start()
    print("Done")
