import subprocess
import os

#display menu
def main():
        print("\nSelect an Option")
        print("[1] Create New Hostname")
        print("[2] Create New sudo User")
        print("[3] Create Swapfile")
        print("[4] Add Additional Networks")
        print("[5] Update & Upgrade")
        print("[6] Exit")
        
        option = input("Select an Option: ")

        if option == '1':
            changeHostname()
        elif option == '2':
            createNewSuperUser()
        elif option == '3':
            createSwapFile()
        elif option == '4':
            addNetworks()
        elif option == '5':
            updateAndUpgrade()
        elif option == '6':
            raise SystemExit
        else:
            print("\nInvalid Option")
            main()
    
#change default hostname
def changeHostname():
    new_hostname = input("Enter a new hostname: ")
    
    #run hostnamectl and change hostname
    try:
        result = subprocess.run(['hostnamectl', 'set-hostname', new_hostname], check=True, text=True, capture_output=True)
        reboot = input("Reboot HIGHLY Recommended (y/n): ")
        if reboot == 'y':
            result = subprocess.run(['sudo', 'reboot', 'now'])
        elif reboot == 'n':
            raise SystemExit
        elif reboot != 'y' or reboot != 'n':
            print("y or n")

    except subprocess.CalledProcessError as e:
        print(f"Failed to change hostname: {e.stderr}")
    returnToMain()
        
#create new sudo user and delete default
def createNewSuperUser():
    new_superuser = input("Enter a new Username: ")

    #create the user
    try:
        subprocess.run(['sudo', 'useradd', '-m', new_superuser], check=True)
        subprocess.run(['sudo', 'usermod', '-aG', 'sudo', new_superuser], check=True)
        subprocess.run(['sudo', 'passwd', new_superuser], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occured: {e}")
    returnToMain()

#create swapfile
def createSwapFile():
    new_swapfile_size = input("Enter Swapfile Size (ex: 500M or 1G): ")
    addFstab = "/swapfile none swap sw 0 0\n"

    #create swapfile
    try:
        subprocess.run(['sudo', 'fallocate', '-l', new_swapfile_size, '/swapfile'], check=True)
        subprocess.run(['sudo', 'chmod', '600', '/swapfile'], check=True)
        subprocess.run(['sudo', 'mkswap', '/swapfile'], check=True)
        subprocess.run(['sudo', 'swapon', '/swapfile'], check=True)
        subprocess.run(['sudo', 'sh', '-c', f'echo "{addFstab.strip()}" >> /etc/fstab'], check=True)
        subprocess.run(['sudo', 'swapon', '--show'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occured: {e}")
    returnToMain()

#add additional networks using nmcli
def addNetworks():
    try:
        subprocess.run(['sudo', 'nmtui'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occured: {e}")
    returnToMain()

#update & upgrade
def updateAndUpgrade():
    try:
        subprocess.run(['sudo', 'update && upgrade'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occured: {e}")
    returnToMain()

def returnToMain():
    do_continue = input("\nTask completed\n[1]Main Menu or [2]Exit: ")
    if do_continue == "1":
        main()
    else:
        exit()
        

if __name__ == "__main__":
    main()

