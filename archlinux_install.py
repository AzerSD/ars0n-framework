import subprocess, argparse
from time import sleep
from datetime import datetime


#### installer Helper Utils ####
class Timer:
    def __init__(self):
        self.start = datetime.now()
        self.stop = None
    
    def stop_timer(self):
        self.stop = datetime.now()

    def get_start(self):
        return self.start.strftime("%H:%M:%S")

    def get_stop(self):
        return self.stop.strftime("%H:%M:%S")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--vpn', help='Install ProtonVPN Debian Client - https://protonvpn.com', required=False, action='store_true')
    parser.add_argument('--arm', help='Install The Ars0n Framework for ARM Processor', required=False, action='store_true')
    return parser.parse_args()

def get_home_dir():
    get_home_dir = subprocess.run(["echo $HOME"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, shell=True)
    return get_home_dir.stdout.replace("\n", "")

def keystore():
    home_dir = get_home_dir()
    keystore_check = subprocess.run([f"ls {home_dir}/.keys"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    if keystore_check.returncode == 0:
        print("[+] Keys directory found.")
    else:
        print("[!] Keys directory NOT found!  Creating now...")
        subprocess.run([f"mkdir {home_dir}/.keys"], shell=True)
        keystore_check = subprocess.run([f"ls {home_dir}/.keys"], shell=True)
        if keystore_check.returncode == 0:
            print("[+] Keys directory created successfully!")
            slack_key = input("[*] Please enter your Slack Token (ENTER to leave black and add later):\n")
            github_key = input("[*] Please enter your GitHub PAT (ENTER to leave black and add later):\n")
            shodan_key = input("[*] Please enter your Shodan API Key (ENTER to leave black and add later):\n")
            hackerone_user = input("[*] Please enter your HackerOne Username (ENTER to leave black and add later):\n")
            hackerone_key = input("[*] Please enter your HackerOne API Key (ENTER to leave black and add later):\n")
            subprocess.run([f"""echo "{hackerone_user}:{hackerone_key}" > {home_dir}/.keys/.hackerone && echo "{slack_key}" > {home_dir}/.keys/slack_web_hook && echo "github:{github_key}" > {home_dir}/.keys/.keystore && echo "shodan:{shodan_key}" >> {home_dir}/.keys/.keystore"""], shell=True)

def update_apt():
    subprocess.run(["sudo pacman -Syu"], shell=True)

def tools_dir_check():
    home_dir = get_home_dir()
    go_check = subprocess.run([f"ls {home_dir}/Tools"], 
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE, shell=True)
    if go_check.returncode == 0:
        print("[+] Tools folder was found.")
        return True
    print("[!] Tools folder was NOT found.  Creating now...")
    return False

def create_tools_dir():
    home_dir = get_home_dir()
    subprocess.run([f"mkdir {home_dir}/Tools"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools"], shell=True)
    if install_check.returncode == 0:
        print("[+] Tools directory successfully created.")
    else:
        print("[!] Tools directory was NOT successfully created!  Something is really jacked up.  Exiting...")
        exit()

def create_virtualenv():
    home_dir = get_home_dir()
    subprocess.run([f"python3 -m venv {home_dir}/Tools/ars0n_venv"], shell=True)
    install_check = subprocess.run([f"ls {home_dir}/Tools/ars0n_venv"], shell=True)
    if install_check.returncode == 0:
        print("[+] Virtual Environment successfully created.")
    else:
        print("[!] Virtual Environment was NOT successfully created!  Something is really jacked up.  Exiting...")
        exit()

def activate_virtualenv():
    home_dir = get_home_dir()
    subprocess.run([f"source {home_dir}/Tools/ars0n_venv/bin/activate"], shell=True)

def run_server_prompt(args):
    prompt = input("[?] Would you like to run the web application now? (Y/n)")
    if prompt == "Y":
        if args.arm:
            subprocess.run(["chmod 777 run.sh; ./run.sh"], shell=True)
        else:
            subprocess.run(["chmod 777 run.sh; ./run.sh"], shell=True)

#### Utility Functions ####
def flask_cors_check():
    flask_cors_check = subprocess.run([f"pip3 show flask_cors"],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.PIPE,
                                      shell=True)

    if flask_cors_check.returncode == 0:
        print("[+] Flask_CORS is already installed.")
        return True
    print("[!] Flask_CORS is NOT installed.  Installing now...")
    return False

def install_flask_cors():
    install_check = subprocess.run([f"pip3 install flask_cors"],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.PIPE,
                                   shell=True)

    if install_check.returncode == 0:
        print("[+] Flask_CORS was installed successfully!")
    else:
        print("[!] Something went wrong!  Flask_CORS was NOT installed successfully...")  

def main(args):
    print("[+] Starting install script")
    print("[!] WARNING: The install.py script should not be run as sudo.  If you did, ctrl+c and re-run the script as a user.  I'll give you a couple seconds ;)")
    sleep(2)
    starter_timer = Timer()
    keystore()
    update_apt()
    create_virtualenv()
    activate_virtualenv()
    if tools_dir_check() is False:
        create_tools_dir()
    if flask_cors_check() is False:
        install_flask_cors()
    # if awscli_check() is False:
    #     install_awscli()
    # if node_check() is False:
    #     install_node()
    # if npm_check() is False:
    #     install_npm()
    # if mongodb_check() is False:
    #     if args.arm:
    #         install_mongodb()
    #     else:
    #         install_mongodb_arm()
    # if go_check() is False:
    #     install_go()
    # if sublist3r_check() is False:
    #     install_sublist3r()
    # if assetfinder_check() is False:
    #     install_assetfinder()
    # if gau_check() is False:
    #     if args.arm:
    #         install_gau_arm()
    #     else:
    #         install_gau()
    # if crt_check() is False:
    #     install_crt()
    # if shosubgo_check() is False:
    #     install_shosubgo()
    # if subfinder_check() is False:
    #     if args.arm:
    #         install_subfinder()
    #     else:
    #         install_subfinder_arm()
    # if gospider_check() is False:
    #     if args.arm:
    #         install_gospider()
    #     else:
    #         install_gospider_arm()
    # if subdomainizer_check() is False:
    #     install_subdomainizer()
    # if shuffledns_check() is False:
    #     if args.arm:
    #         install_shuffledns()
    #     else:
    #         install_shuffledns_arm()
    # if httprobe_check() is False:
    #     install_httprobe()
    # if tlsscan_check() is False:
    #     if args.arm:
    #         install_tlsscan()
    #     else:
    #         install_tlsscan_arm()
    # if jq_check() is False:
    #     install_jq()
    # if dnmasscan_check() is False:
    #     install_dnmasscan()
    # if nuclei_check() is False:
    #     if args.arm:
    #         install_nuclei()
    #     else:
    #         install_nuclei_arm()
    # if server_check() is False:
    #     install_server()
    # if client_check() is False:
    #     install_client()
    # if args.vpn:
    #     install_protonvpn()
    # if validate_install() is False:
    #     print("[!] Something went wrong!  Please try to run the installer again or open an issue on the repo...")
    #     exit()
    starter_timer.stop_timer()
    # run_server_prompt(args)
    print(f"[+] Done!  Start: {starter_timer.get_start()}  |  Stop: {starter_timer.get_stop()}")

if __name__ == "__main__":
    args = arg_parse()
    main(args)
