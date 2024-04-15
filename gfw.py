import subprocess
import os
import click

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

def start_proxy():
    command = ['./hy/hysteria-linux-amd64', '-c', './hy/config.json']

    return_code = subprocess.call(command)

    if return_code == 0:
        click.secho(f"[*] hysteria successfully", fg='green')
    else:
        click.secho(f"[*] Failed run hysteria ...", fg='yellow')


if __name__ == "__main__":

    target_directory = "./hy"
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    download_hysteria(target_directory)
    
    if download_config(target_directory) == 0:
        start_proxy()