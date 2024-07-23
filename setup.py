import subprocess
import os

#display menu
def main():
        print("\n")
        print("[1] Create New Hostname (automatic reboot)")
        print("[2] Create New sudo User")
        print("[3] Create Swapfile")
        print("[4] Add Additional Networks")
        print("[5] Update & Upgrade")
        print("[6] Install Realtek Drivers")
        print("[0] Exit")
        
        option = input("\nSelect an Option: ")

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
            installRealtekDrivers()
        elif option == '0':
            raise SystemExit
        else:
            print("\nInvalid Option")
            main()
    
#change default hostname
def changeHostname():
    new_hostname = input("Enter a new Hostname: ")
    
    #run hostnamectl and change hostname
    try:
        subprocess.run(['hostnamectl', 'set-hostname', new_hostname], check=True, text=True, capture_output=True)
        input("\npress any key to reboot")
        subprocess.run(['sudo', 'reboot', 'now'])

    except subprocess.CalledProcessError as e:
        print(f"\nFailed to change hostname: {e.stderr}")
        returnToMain()
        
#change default username or create new username
def createNewSuperUser():
    newOrChangeUser = input("\n[1] Create New sudo User\n[2] Rename Default User\nSelect an Option: ")
    currentUser = subprocess.run(['whoami'], capture_output=True, text=True, check=True)
    new_name = input("\nEnter a new Username: ")
    
    #create new user
    if newOrChangeUser == "1":
        try:
            subprocess.run(['sudo', 'useradd', '-m', new_name], check=True)
            subprocess.run(['sudo', 'usermod', '-aG', 'sudo', new_name], check=True)
            subprocess.run(['sudo', 'passwd', new_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"\nAn error occured: {e}")
    
    #rename current user
    elif newOrChangeUser == "2":
        subprocess.run(['sudo', 'usermod', '-l', new_name, 'whoami'],check=True)
    else:
        print("\nInvalid Input, try again...")

    #delete previous user
    deleteUser = input("\nWould you like to delete the prior username?\n[1] Yes\n[2] No\nSelect an Option: ")
    if deleteUser == "1":
        subprocess.run(['sudo', 'su', new_name], check=True)
        subprocess.run(['sudo', 'userdel', '-r', currentUser], check=True)

    elif deleteUser == "2":
        changeUser = input("Would you like to change over to the new User?\n[1] Yes\n[2]No\nSelect an Option: ")
        if changeUser == "1":
            subprocess.run(['sudo', 'su', new_name], check=True)
        elif changeUser == "2":
            returnToMain()
        else:
            print("\nInvalid Input, try again...")
    else:
        print("Invalid Input, try again...")

    returnToMain()

#create swapfile
def createSwapFile():
    print("\n512MB recommended on Zero/Zero2, 1GB on 8GB Models, and 2GB on 1GB-4GB Models")
    enter_size = input("\n[1] 512MB\n[2] 1GB\n[3] 2GB\nSelect an Option: ")
    
    if enter_size == "1":
        size = "512MB"
    elif enter_size == "2":
        size = "1GB"
    elif enter_size == "3":
        size = "2GB"
    else:
        print("\nInvalid Input, try again...")

    addFstab = "/swapfile none swap sw 0 0\n"

    #create swapfile
    try:
        subprocess.run(['sudo', 'fallocate', '-l', size, '/swapfile'], check=True)
        subprocess.run(['sudo', 'chmod', '600', '/swapfile'], check=True)
        subprocess.run(['sudo', 'mkswap', '/swapfile'], check=True)
        subprocess.run(['sudo', 'swapon', '/swapfile'], check=True)
        subprocess.run(['sudo', 'sh', '-c', f'echo "{addFstab.strip()}" >> /etc/fstab'], check=True)
        subprocess.run(['sudo', 'swapon', '--show'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occured: {e}")
    returnToMain()

#add additional networks using nmcli
def addNetworks():
    try:
        subprocess.run(['sudo', 'nmtui'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occured: {e}")
    returnToMain()

#update && upgrade
def updateAndUpgrade():
    try:
        subprocess.run(['sudo', 'update && upgrade'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occured: {e}")
    returnToMain()

#rtl88xxau drivers with option to select old or new
def installRealtekDrivers():
    home_dir = os.path.expanduser("~/")
    driver_dir = os.path.join(home_dir, "rtl8812au")
    
    os.chdir(home_dir)
    
    # Check if directory already exists
    if os.path.exists(driver_dir):
        while True:    
            uninstall = input("\n[1]Continue Installation\n[2]Uninstall and Reinstall\n\nSelect an Option: ")
            if uninstall == "2":
                os.chdir(driver_dir)
                subprocess.run(['sudo', 'make', 'dkms_remove'], check=True)
                break
            elif uninstall == "1":
                break
            else:
                print("\nInvalid Input, try again...")
    else: 
        os.chdir(home_dir)
        subprocess.run(['sudo', 'git', 'clone', 'https://github.com/aircrack-ng/rtl8812au'], check=True)                    
        os.chdir(driver_dir)

    #[1] downloads current & [2] uses backups from same repo
    while True:        
        oldOrNew = input("\n[1]Current\n[2]Backup\n\nSelect an Option: ")
        if oldOrNew == "2":
            subprocess.run(['git', 'reset', '--hard 63cf0b4'], check=True)
            break
        elif oldOrNew == "1":
            break
        else:
            print("\nInvalid Option, try again...")
        
    try:
       subprocess.run(['sudo', 'make', 'dkms_install'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred: {e}")

    returnToMain()

def returnToMain():
    do_continue = input("\n[1]Main Menu\n[2]Exit\nSelect an Option: ")
    if do_continue == "1":
        main()
    else:
        exit()
        

if __name__ == "__main__":
    main()

