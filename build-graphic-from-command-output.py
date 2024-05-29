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
        print(f"Server: {server['hostname']}")
        df_output = execute_command(client, "df -Th | grep nfs")
        print("Disk Space Information:")
        print(df_output)
        for line in df_lines:
            df_columns = line.split()
            print("\tdf_columns\t", end="")
            print(type(df_columns))
            for i, df_column_value in enumerate(df_columns):
               print(f"\t\tcolumn {i}: {df_column_value}")")      
                print("\n/etc/fstab Contents:")
        
        fstab = execute_command(client, "grep ^fs /etc/fstab")
        print("\tfstab\t", end="")
        print(type(fstab))
        fstab_lines = fstab.splitlines()
        for line in fstab_lines:
            fstab_columns = line.split()
            print("\tfstab_columns\t", end="")
            print(type(fstab_columns))
            for i, fstab_column_value in enumerate(fstab_columns):
               print(f"\t\tcolumn {i}: {fstab_column_value}")
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
#print(type(server_info))
#pprint.pprint(server_info)


'''
example output

Server: server0
        df_output
        df_columns      <class 'list'>
                column 0: 127.0.0.1://special
                column 1: nfs4
                column 2: 8.0E
                column 3: 75G
                column 4: 8.0E
                column 5: 1%
                column 6: /special
        df_columns      <class 'list'>
                column 0: 127.0.0.1:/
                column 1: nfs4
                column 2: 8.0E
                column 3: 14T
                column 4: 8.0E
                column 5: 1%
                column 6: /conversion
        df_columns      <class 'list'>
                column 0: 127.0.0.1:/
                column 1: nfs4
                column 2: 8.0E
                column 3: 243G
                column 4: 8.0E
                column 5: 1%
                column 6: /channel
        df_columns      <class 'list'>
                column 0: 127.0.0.1://media
                column 1: nfs4
                column 2: 8.0E
                column 3: 75G
                column 4: 8.0E
                column 5: 1%
                column 6: /media
        df_columns      <class 'list'>
                column 0: 127.0.0.1:/
                column 1: nfs4
                column 2: 8.0E
                column 3: 305G
                column 4: 8.0E
                column 5: 1%
                column 6: /interface
        fstab   <class 'str'>
        fstab_columns   <class 'list'>
                column 0: fs-1:/
                column 1: /channel
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-2://special
                column 1: /special
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-2://media
                column 1: /media
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-3:/
                column 1: /interface
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-4:/
                column 1: /conversion
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
Server: server1
        df_output
        df_columns      <class 'list'>
                column 0: 127.0.0.1:/
                column 1: nfs4
                column 2: 8.0E
                column 3: 243G
                column 4: 8.0E
                column 5: 1%
                column 6: /channel
        df_columns      <class 'list'>
                column 0: 127.0.0.1:/
                column 1: nfs4
                column 2: 8.0E
                column 3: 305G
                column 4: 8.0E
                column 5: 1%
                column 6: /interface
        df_columns      <class 'list'>
                column 0: 127.0.0.1://media
                column 1: nfs4
                column 2: 8.0E
                column 3: 75G
                column 4: 8.0E
                column 5: 1%
                column 6: /media
        df_columns      <class 'list'>
                column 0: 127.0.0.1://special
                column 1: nfs4
                column 2: 8.0E
                column 3: 75G
                column 4: 8.0E
                column 5: 1%
                column 6: /special
        df_columns      <class 'list'>
                column 0: 127.0.0.1:/
                column 1: nfs4
                column 2: 8.0E
                column 3: 14T
                column 4: 8.0E
                column 5: 1%
                column 6: /conversion
        fstab   <class 'str'>
        fstab_columns   <class 'list'>
                column 0: fs-1:/
                column 1: /channel
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-2://special
                column 1: /special
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-2:///media
                column 1: /media
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-3:/
                column 1: /interface
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
        fstab_columns   <class 'list'>
                column 0: fs-4:/
                column 1: /conversion
                column 2: efs
                column 3: _netdev,noresvport,tls
                column 4: 0
                column 5: 0
Server: server0
Disk Space Information:
127.0.0.1://special nfs4      8.0E   75G  8.0E   1% /special
127.0.0.1:/           nfs4      8.0E   14T  8.0E   1% /conversion
127.0.0.1:/           nfs4      8.0E  243G  8.0E   1% /channel
127.0.0.1://media   nfs4      8.0E   75G  8.0E   1% /media
127.0.0.1:/           nfs4      8.0E  305G  8.0E   1% /interface


/etc/fstab Contents that starts with fs:
fs-1:/ /channel efs _netdev,noresvport,tls 0 0
fs-2://special /special  efs _netdev,noresvport,tls 0 0
fs-2://media /media   efs _netdev,noresvport,tls 0 0
fs-3:/ /interface efs _netdev,noresvport,tls 0 0
fs-4:/ /conversion efs _netdev,noresvport,tls 0 0

Server: server1
Disk Space Information:
127.0.0.1:/           nfs4      8.0E  243G  8.0E   1% /channel
127.0.0.1:/           nfs4      8.0E  305G  8.0E   1% /interface
127.0.0.1://media   nfs4      8.0E   75G  8.0E   1% /media
127.0.0.1://special nfs4      8.0E   75G  8.0E   1% /special
127.0.0.1:/           nfs4      8.0E   14T  8.0E   1% /conversion


/etc/fstab Contents that starts with fs:
fs-1:/ /channel efs _netdev,noresvport,tls 0 0
fs-2://special  /special  efs _netdev,noresvport,tls 0 0
fs-2:///media   /media   efs _netdev,noresvport,tls 0 0
fs-3:/ /interface efs _netdev,noresvport,tls 0 0
fs-4:/ /conversion efs _netdev,noresvport,tls 0 0

All servers processed.
'''
