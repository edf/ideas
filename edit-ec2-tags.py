# edit ec2 tags using GUI

import boto3
import tkinter as tk
from tkinter import messagebox

class EC2TagEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AWS EC2 Tag Editor")

        # AWS Region
        self.region_label = tk.Label(root, text="AWS Region:")
        self.region_label.grid(row=0, column=0, padx=10, pady=10)
        self.region_entry = tk.Entry(root)
        self.region_entry.grid(row=0, column=1, padx=10, pady=10)

        # Instance ID (now selected from a listbox)
        self.instance_listbox_label = tk.Label(root, text="Instances:")
        self.instance_listbox_label.grid(row=1, column=0, padx=10, pady=10)
        self.instance_listbox = tk.Listbox(root, height=10, width=50)
        self.instance_listbox.grid(row=1, column=1, padx=10, pady=10)
        self.instance_listbox.bind('<<ListboxSelect>>', self.on_instance_select)

        # Tag Key
        self.tag_key_label = tk.Label(root, text="Tag Key:")
        self.tag_key_label.grid(row=2, column=0, padx=10, pady=10)
        self.tag_key_entry = tk.Entry(root)
        self.tag_key_entry.grid(row=2, column=1, padx=10, pady=10)

        # Tag Value
        self.tag_value_label = tk.Label(root, text="Tag Value:")
        self.tag_value_label.grid(row=3, column=0, padx=10, pady=10)
        self.tag_value_entry = tk.Entry(root)
        self.tag_value_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        self.get_instances_button = tk.Button(root, text="Get Instances", command=self.get_instances)
        self.get_instances_button.grid(row=4, column=0, padx=10, pady=10)

        self.update_tag_button = tk.Button(root, text="Update Tag", command=self.update_tag)
        self.update_tag_button.grid(row=4, column=1, padx=10, pady=10)

        # Tags display
        self.tags_display = tk.Text(root, height=10, width=50)
        self.tags_display.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Volumes listbox
        self.volumes_listbox_label = tk.Label(root, text="Volumes:")
        self.volumes_listbox_label.grid(row=6, column=0, padx=10, pady=10)
        self.volumes_listbox = tk.Listbox(root, height=10, width=50)
        self.volumes_listbox.grid(row=6, column=1, padx=10, pady=10)
        self.volumes_listbox.bind('<<ListboxSelect>>', self.on_volume_select)

        # Buttons for volumes
        self.update_volume_tag_button = tk.Button(root, text="Update Volume Tag", command=self.update_volume_tag)
        self.update_volume_tag_button.grid(row=7, column=1, padx=10, pady=10)

    def get_instances(self):
        region = self.region_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            response = ec2.describe_instances()
            self.instance_listbox.delete(0, tk.END)
            self.instance_id_map = {}
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'Unnamed')
                    self.instance_id_map[f"{instance_name} ({instance_id})"] = instance_id
                    self.instance_listbox.insert(tk.END, f"{instance_name} ({instance_id})")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_instance_select(self, event):
        selection = event.widget.curselection()
        if selection:
            selected_instance = event.widget.get(selection[0])
            instance_id = self.instance_id_map[selected_instance]
            self.instance_id_entry.delete(0, tk.END)
            self.instance_id_entry.insert(0, instance_id)
            self.get_tags()
            self.get_volumes(instance_id)

    def get_tags(self):
        region = self.region_entry.get()
        instance_id = self.instance_id_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            tags = response['Reservations'][0]['Instances'][0].get('Tags', [])
            self.tags_display.delete('1.0', tk.END)
            for tag in tags:
                self.tags_display.insert(tk.END, f"{tag['Key']}: {tag['Value']}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_volumes(self, instance_id):
        region = self.region_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            self.volumes_listbox.delete(0, tk.END)
            self.volume_id_map = {}
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    for volume in instance.get('BlockDeviceMappings', []):
                        volume_id = volume['Ebs']['VolumeId']
                        self.volume_id_map[volume_id] = volume_id
                        self.volumes_listbox.insert(tk.END, volume_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_volume_select(self, event):
        selection = event.widget.curselection()
        if selection:
            selected_volume = event.widget.get(selection[0])
            self.get_volume_tags(selected_volume)

    def get_volume_tags(self, volume_id):
        region = self.region_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            response = ec2.describe_volumes(VolumeIds=[volume_id])
            tags = response['Volumes'][0].get('Tags', [])
            self.tags_display.delete('1.0', tk.END)
            for tag in tags:
                self.tags_display.insert(tk.END, f"{tag['Key']}: {tag['Value']}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_tag(self):
        region = self.region_entry.get()
        instance_id = self.instance_id_entry.get()
        tag_key = self.tag_key_entry.get()
        tag_value = self.tag_value_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            ec2.create_tags(Resources=[instance_id], Tags=[{'Key': tag_key, 'Value': tag_value}])
            messagebox.showinfo("Success", "Instance tag updated successfully")
            self.get_tags()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_volume_tag(self):
        region = self.region_entry.get()
        selection = self.volumes_listbox.curselection()
        if selection:
            volume_id = self.volumes_listbox.get(selection[0])
            tag_key = self.tag_key_entry.get()
            tag_value = self.tag_value_entry.get()
            ec2 = boto3.client('ec2', region_name=region)
            try:
                ec2.create_tags(Resources=[volume_id], Tags=[{'Key': tag_key, 'Value': tag_value}])
                messagebox.showinfo("Success", "Volume tag updated successfully")
                self.get_volume_tags(volume_id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No volume selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = EC2TagEditorApp(root)
    root.mainloop()
