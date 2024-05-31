import pandas as pd

data = [
    {
        'hostname': 'server1.example.com',
        'fstab': (
            'UUID=1234-5678-9abc-def0 / ext4 defaults 1 1\n'
            'nfs-server1:/exported/path1 /mnt1 nfs defaults 0 0\n'
            'nfs-server2:/exported/path2 /mnt2 nfs defaults 0 0\n'
            'nfs-shared:/common/path /mnt3 nfs defaults 0 0'
            ),
        'nfs': (
                'nfs-server1:/exported/path1 /mnt1 nfs4 rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,nolock,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.100,local_lock=none,addr=192.168.1.1 0 0\n'
                'nfs-server2:/exported/path2 /mnt2 nfs4 rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,nolock,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.100,local_lock=none,addr=192.168.1.2 0 0\n'
                'nfs-shared:/common/path /mnt3 nfs4 rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,nolock,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.100,local_lock=none,addr=192.168.1.3 0 0'
                ),
        'df': (
            'nfs-server1:/exported/path1 100G 50G 50G 50% /mnt1\n'
            'nfs-server2:/exported/path2 200G 100G 100G 50% /mnt2\n'
            'nfs-shared:/common/path 300G 150G 150G 50% /mnt3'
            )
    },
    {
        'hostname': 'server2.example.com',
        'fstab': (
             'UUID=abcd-ef01-2345-6789 / ext4 defaults 1 1\n'
             'nfs-server3:/another/path1 /mnt1 nfs defaults 0 0\n'
             'nfs-server4:/another/path2 /mnt2 nfs defaults 0 0\n'
             'nfs-shared:/common/path /mnt3 nfs defaults 0 0'
             ),
        'nfs': (
            'nfs-server3:/another/path1 /mnt1 nfs4 rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,nolock,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.101,local_lock=none,addr=192.168.1.4 0 0\n'
            'nfs-server4:/another/path2 /mnt2 nfs4 rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,nolock,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.101,local_lock=none,addr=192.168.1.5 0 0\n'
            'nfs-shared:/common/path /mnt3 nfs4 rw,relatime,vers=4.1,rsize=1048576,wsize=1048576,namlen=255,hard,nolock,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=192.168.1.101,local_lock=none,addr=192.168.1.6 0 0'
            ),
        'df': (
            'nfs-server3:/another/path1 400G 200G 200G 50% /mnt1\n'
            'nfs-server4:/another/path2 500G 250G 250G 50% /mnt2\n'
            'nfs-shared:/common/path 300G 150G 150G 50% /mnt3'
            )
    }
]

df = pd.DataFrame(data)


### Updated Script to Include Space Used

import re

# Function to parse the NFS output
def parse_nfs_info(nfs_info):
    nfs_entries = []
    lines = nfs_info.split('\n')
    for line in lines:
        match = re.search(r'(\S+):(\S+) (\S+)', line)
        if match:
            nfs_server = match.group(1)
            mount_point = match.group(3)
            nfs_entries.append((nfs_server, mount_point))
    return nfs_entries

# Function to parse the fstab output
def parse_fstab_info(fstab_info):
    fstab_entries = []
    lines = fstab_info.split('\n')
    for line in lines:
        if 'nfs' in line:
            parts = re.split(r'\s+', line)
            device = parts[0]
            mount_point = parts[1]
            fstab_entries.append((device, mount_point))
    return fstab_entries

# Function to parse the df output
def parse_df_info(df_info):
    df_entries = []
    lines = df_info.split('\n')
    for line in lines:
        parts = re.split(r'\s+', line)
        if len(parts) >= 6:
            nfs_server = parts[0]
            total_size = parts[1]
            used_size = parts[2]
            available_size = parts[3]
            percent_used = parts[4]
            mount_point = parts[5]
            df_entries.append((nfs_server, total_size, used_size, available_size, percent_used, mount_point))
    return df_entries

# List to hold the parsed results
parsed_data = []

# Parse each row in the DataFrame
for index, row in df.iterrows():
    hostname = row['hostname']
    nfs_entries = parse_nfs_info(row['nfs'])
    fstab_entries = parse_fstab_info(row['fstab'])
    df_entries = parse_df_info(row['df'])\

    for nfs_server, nfs_mount_point in nfs_entries:
        for device, mount_point in fstab_entries:
            for df_entry in df_entries:
                df_server, total_size, used_size, available_size, percent_used, df_mount_point = df_entry
                if mount_point == nfs_mount_point and df_mount_point == mount_point:
                    parsed_data.append({
                        'hostname': hostname,
                        'nfs_server': nfs_server,
                        'mount_point': mount_point,
                        'device': device,
                        #'total_size': total_size,
                        'used_size': used_size,
                        #'available_size': available_size,
                        #'percent_used': percent_used
                    })

# Create a new DataFrame from the parsed data
parsed_df = pd.DataFrame(parsed_data)

# Display the parsed DataFrame
print(parsed_df)


'''
output

              hostname   nfs_server mount_point                       device used_size
0  server1.example.com  nfs-server1       /mnt1  nfs-server1:/exported/path1       50G
1  server1.example.com  nfs-server2       /mnt2  nfs-server2:/exported/path2      100G
2  server1.example.com   nfs-shared       /mnt3      nfs-shared:/common/path      150G
3  server2.example.com  nfs-server3       /mnt1   nfs-server3:/another/path1      200G
4  server2.example.com  nfs-server4       /mnt2   nfs-server4:/another/path2      250G
5  server2.example.com   nfs-shared       /mnt3      nfs-shared:/common/path      150G

'''
