import os
import paramiko
import time

def ssh_connect(hostname, username, key_path):
    try:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, pkey=key)
        return client
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {hostname}")
        return None

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(1)
    return stdout.read().decode("utf-8")

# Server details (replace with your own)
servers = [
    {
        "hostname": "server1.example.com",
        "username": "your_username",
        "key_path": "/path/to/your/private_key1"
    },
    {
        "hostname": "server2.example.com",
        "username": "your_username",
        "key_path": "/path/to/your/private_key2"
    }
]

# Create a dictionary to store server information
server_info = {}

# Connect to servers
for server in servers:
    client = ssh_connect(server["hostname"], server["username"], server["key_path"])
    if client:
        df_output = execute_command(client, "df -Th")
        fstab = execute_command(client, "cat /etc/fstab")
        print(f"Server: {server['hostname']}")
        print("Disk Space Information:")
        print(df_output)
        print("\n/etc/fstab Contents:")
        print(fstab)
        server_info[server["hostname"]] = {
            "disk_space": df_output,
            "fstab_contents": fstab
        }
        client.close()
    else:
        print(f"Failed to establish SSH connection for {server['hostname']}")

# Print server information
for server_name, info in server_info.items():
    print(f"Server: {server_name}")
    print("Disk Space Information:")
    print(info["disk_space"])
    print("\n/etc/fstab Contents:")
    print(info["fstab_contents"])

print("All servers processed.")
