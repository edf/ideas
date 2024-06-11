import boto3
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Toplevel

def get_instances(region_entry, instance_listbox, instance_id_map):
    region = region_entry.get()
    ec2 = boto3.client('ec2', region_name=region)
    try:
        response = ec2.describe_instances()
        instance_listbox.delete(0, tk.END)
        instance_id_map.clear()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), 'Unnamed')
                instance_id_map[f"{instance_name} ({instance_id})"] = instance_id
                instance_listbox.insert(tk.END, f"{instance_name} ({instance_id})")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_instance_select(event, instance_listbox, instance_id_map, tags_display, region_entry, volumes_listbox, volume_id_map):
    selection = event.widget.curselection()
    if selection:
        selected_instance = event.widget.get(selection[0])
        instance_id = instance_id_map[selected_instance]
        get_tags(instance_id, region_entry, tags_display)
        get_volumes(instance_id, region_entry, volumes_listbox, volume_id_map)

def get_tags(instance_id, region_entry, tags_display):
    region = region_entry.get()
    ec2 = boto3.client('ec2', region_name=region)
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        tags = response['Reservations'][0]['Instances'][0].get('Tags', [])
        tags_display.delete('1.0', tk.END)
        for tag in tags:
            tags_display.insert(tk.END, f"{tag['Key']}: {tag['Value']}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_volumes(instance_id, region_entry, volumes_listbox, volume_id_map):
    region = region_entry.get()
    ec2 = boto3.client('ec2', region_name=region)
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        volumes_listbox.delete(0, tk.END)
        volume_id_map.clear()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                for volume in instance.get('BlockDeviceMappings', []):
                    volume_id = volume['Ebs']['VolumeId']
                    volume_id_map[volume_id] = volume_id
                    volumes_listbox.insert(tk.END, volume_id)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_volume_select(event, volumes_listbox, tags_display, region_entry):
    selection = event.widget.curselection()
    if selection:
        selected_volume = event.widget.get(selection[0])
        get_volume_tags(selected_volume, region_entry, tags_display)

def get_volume_tags(volume_id, region_entry, tags_display):
    region = region_entry.get()
    ec2 = boto3.client('ec2', region_name=region)
    try:
        response = ec2.describe_volumes(VolumeIds=[volume_id])
        tags = response['Volumes'][0].get('Tags', [])
        tags_display.delete('1.0', tk.END)
        for tag in tags:
            tags_display.insert(tk.END, f"{tag['Key']}: {tag['Value']}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_tag(instance_listbox, instance_id_map, region_entry, tag_key_entry, tag_value_entry, tags_display):
    region = region_entry.get()
    selection = instance_listbox.curselection()
    if selection:
        selected_instance = instance_listbox.get(selection[0])
        instance_id = instance_id_map[selected_instance]
        tag_key = tag_key_entry.get()
        tag_value = tag_value_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            ec2.create_tags(Resources=[instance_id], Tags=[{'Key': tag_key, 'Value': tag_value}])
            messagebox.showinfo("Success", "Instance tag updated successfully")
            get_tags(instance_id, region_entry, tags_display)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "No instance selected")

def update_volume_tag(volumes_listbox, region_entry, tag_key_entry, tag_value_entry, tags_display):
    region = region_entry.get()
    selection = volumes_listbox.curselection()
    if selection:
        volume_id = volumes_listbox.get(selection[0])
        tag_key = tag_key_entry.get()
        tag_value = tag_value_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            ec2.create_tags(Resources=[volume_id], Tags=[{'Key': tag_key, 'Value': tag_value}])
            messagebox.showinfo("Success", "Volume tag updated successfully")
            get_volume_tags(volume_id, region_entry, tags_display)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "No volume selected")

def edit_tags_popup(instance_id, region_entry):
    def load_tags(tree, instance_id, region_entry):
        region = region_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            tags = response['Reservations'][0]['Instances'][0].get('Tags', [])
            for tag in tags:
                tree.insert('', 'end', values=(tag['Key'], tag['Value']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_tags(tree, instance_id, region_entry):
        region = region_entry.get()
        ec2 = boto3.client('ec2', region_name=region)
        try:
            new_tags = []
            for item in tree.get_children():
                key, value = tree.item(item, 'values')
                new_tags.append({'Key': key, 'Value': value})
            ec2.create_tags(Resources=[instance_id], Tags=new_tags)
            messagebox.showinfo("Success", "Tags updated successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    popup = Toplevel()
    popup.title("Edit Tags")

    tree = ttk.Treeview(popup, columns=('Key', 'Value'), show='headings')
    tree.heading('Key', text='Key')
    tree.heading('Value', text='Value')
    tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    load_tags(tree, instance_id, region_entry)

    add_button = ttk.Button(popup, text="Add Tag", command=lambda: tree.insert('', 'end', values=("", "")))
    add_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    save_button = ttk.Button(popup, text="Save Tags", command=lambda: save_tags(tree, instance_id, region_entry))
    save_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

def create_gui():
    root = ttk.Window(themename="darkly")
    root.title("AWS EC2 Tag Editor")

    instance_id_map = {}
    volume_id_map = {}

    region_label = ttk.Label(root, text="AWS Region:")
    region_label.grid(row=0, column=0, padx=10, pady=10)
    region_entry = ttk.Entry(root)
    region_entry.grid(row=0, column=1, padx=10, pady=10)

    instance_listbox_label = ttk.Label(root, text="Instances:")
    instance_listbox_label.grid(row=1, column=0, padx=10, pady=10)
    instance_listbox = tk.Listbox(root, height=10, width=50)
    instance_listbox.grid(row=1, column=1, padx=10, pady=10)
    instance_listbox.bind('<<ListboxSelect>>', lambda event: on_instance_select(event, instance_listbox, instance_id_map, tags_display, region_entry, volumes_listbox, volume_id_map))

    tag_key_label = ttk.Label(root, text="Tag Key:")
    tag_key_label.grid(row=2, column=0, padx=10, pady=10)
    tag_key_entry = ttk.Entry(root)
    tag_key_entry.grid(row=2, column=1, padx=10, pady=10)

    tag_value_label = ttk.Label(root, text="Tag Value:")
    tag_value_label.grid(row=3, column=0, padx=10, pady=10)
    tag_value_entry = ttk.Entry(root)
    tag_value_entry.grid(row=3, column=1, padx=10, pady=10)

    get_instances_button = ttk.Button(root, text="Get Instances", command=lambda: get_instances(region_entry, instance_listbox, instance_id_map))
    get_instances_button.grid(row=4, column=0, padx=10, pady=10)

    update_tag_button = ttk.Button(root, text="Update Tag", command=lambda: update_tag(instance_listbox, instance_id_map, region_entry, tag_key_entry, tag_value_entry, tags_display))
    update_tag_button.grid(row=4, column=1, padx=10, pady=10)

    exit_button = ttk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=4, column=2, padx=10, pady=10)

    tags_display = tk.Text(root, height=10, width=50)
    tags_display.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    volumes_listbox_label = ttk.Label(root, text="Volumes:")
    volumes_listbox_label.grid(row=6, column=0, padx=10, pady=10)
    volumes_listbox = tk.Listbox(root, height=10, width=50)
    volumes_listbox.grid(row=6, column=1, padx=10, pady=10)
    volumes_listbox.bind('<<ListboxSelect>>', lambda event: on_volume_select(event, volumes_listbox, tags_display, region_entry))

    update_volume_tag_button = ttk.Button(root, text="Update Volume Tag", command=lambda: update_volume_tag(volumes_listbox, region_entry, tag_key_entry, tag_value_entry, tags_display))
    update_volume_tag_button.grid(row=7, column=1, padx=10, pady=10)

    edit_tags_button = ttk.Button(root, text="Edit Tags in Popup", command=lambda: edit_tags_popup(instance_listbox.get(tk.ACTIVE).split(' ')[-1].strip('()'), region_entry))
    edit_tags_button.grid(row=7, column=2, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
