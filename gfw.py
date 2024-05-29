import subprocess
import os
import re
import click

def check_virtual_machine():
    try:
        # Check dmesg for hypervisor keyword
        dmesg_output = subprocess.check_output('dmesg', shell=True).decode('utf-8')
        if re.search(r'hypervisor', dmesg_output, re.IGNORECASE):
            return True

        # Check for hypervisor in /proc/cpuinfo
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        if re.search(r'hypervisor', cpuinfo, re.IGNORECASE):
            return True

        # Check for common VM files
        vm_files = [
            '/sys/class/dmi/id/product_name',
            '/sys/class/dmi/id/sys_vendor',
        ]
        for vm_file in vm_files:
            if os.path.exists(vm_file):
                with open(vm_file, 'r') as f:
                    content = f.read().lower()
                if any(keyword in content for keyword in ['vmware', 'virtual', 'kvm', 'xen', 'qemu']):
                    return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return False

def download_config(dir) -> int:
    config_file_path = os.path.join(dir, 'config.json')
    if os.path.exists(config_file_path):
        click.secho("[*] The config file already exists. No download needed.", fg='green')
        return 0

    urls = {
        "gitlabip": "https://www.gitlabip.xyz/Alvin9999/PAC/master/backup/img/1/2/ip/hysteria/3/config.json",
        "gitlab": "https://gitlab.com/free9999/ipupdate/-/raw/master/backup/img/1/2/ip/hysteria/3/config.json"
    }

    for _, url in urls.items():
        # 为wget命令构建完整的命令行
        command = [
            'wget', '-t', '2', '--no-check-certificate', '-O', 
            os.path.join(dir, 'config.json'), url
        ]
        
        return_code = subprocess.call(command)

        if return_code == 0:
            click.secho(f"[*] Downloaded successfully from {url}", fg='green')
            break
        else:
            click.secho(f"[*] Failed to download from {url}. Trying next source...", fg='yellow')

    if return_code != 0:
        click.secho("[*] All attempts failed.", fg='red')
        return 1
    return 0

def download_hysteria(dir):
    target_file_path = os.path.join(dir, 'hysteria-linux-amd64')
    url = "https://github.com/apernet/hysteria/releases/download/v1.3.5/hysteria-linux-amd64"
    urlavx = "https://github.com/apernet/hysteria/releases/download/v1.3.5/hysteria-linux-amd64-avx"

    if os.path.exists(target_file_path):
        click.secho("[*] The hysteria file already exists. No download needed.", fg='green')
        return

    command = [
        'wget', '-t', '2', '--no-check-certificate', '-O', 
        os.path.join(dir, 'hysteria-linux-amd64'), url
    ]
    return_code = subprocess.call(command)

    if return_code == 0:
        click.secho(f"[*] Downloaded hysteria successfully from {url}", fg='green')
        subprocess.call(['chmod', '+x', './hy/hysteria-linux-amd64'])
    else:
        click.secho(f"[*] Failed to download hysteria from {url}. Trying next source...", fg='yellow')

def download_hysteria_avx(dir):
    target_file_path = os.path.join(dir, 'hysteria-linux-amd64-avx')
    url = "https://github.com/apernet/hysteria/releases/download/v1.3.5/hysteria-linux-amd64-avx"

    if os.path.exists(target_file_path):
        click.secho("[*] The hysteria file already exists. No download needed.", fg='green')
        return

    command = [
        'wget', '-t', '2', '--no-check-certificate', '-O', 
        os.path.join(dir, 'hysteria-linux-amd64-avx'), url
    ]
    return_code = subprocess.call(command)

    if return_code == 0:
        click.secho(f"[*] Downloaded hysteria successfully from {url}", fg='green')
        subprocess.call(['chmod', '+x', './hy/hysteria-linux-amd64-avx'])
    else:
        click.secho(f"[*] Failed to download hysteria from {url}. Trying next source...", fg='yellow')

def start_proxy():
    command = ['./hy/hysteria-linux-amd64', '-c', './hy/config.json']

    return_code = subprocess.call(command)

    if return_code == 0:
        click.secho(f"[*] hysteria successfully", fg='green')
    else:
        click.secho(f"[*] Failed run hysteria ...", fg='yellow')

def start_avxproxy():
    command = ['./hy/hysteria-linux-amd64-avx', '-c', './hy/config.json']

    return_code = subprocess.call(command)

    if return_code == 0:
        click.secho(f"[*] hysteria successfully", fg='green')
    else:
        click.secho(f"[*] Failed run hysteria ...", fg='yellow')


if __name__ == "__main__":

    target_directory = "./hy"
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    vm = check_virtual_machine()
    if vm == True:
        download_hysteria_avx(target_directory)
    else:
        download_hysteria(target_directory)
    
    if download_config(target_directory) == 0:
        if vm == True:
            start_avxproxy()
        else:
            start_proxy()