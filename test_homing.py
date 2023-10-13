import threading
import DoBotArm as Dbt
import time
from serial.tools import list_ports

def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device

def homing_prompt():
    while (True):
        response = input("Do you wanna home? (y/n)")
        if(response == "y") :
            return True
        elif (response == "n"):
            return False
        else:
            print("Unrecognised response")

#--Main Program--
def main():
    #List selected ports for selection
    port = port_selection()
        
    # Preprogrammed sequence
    homeX, homeY, homeZ = 150, 0, 70
    print("Connecting")
    print("Homing")
    ctrlBot = Dbt.DoBotArm(port, homeX, homeY, homeZ ) #Create DoBot Class Object with home position x,y,z


    ctrlBot.toggleSuction(True)  

    ctrlBot.moveArmXYZ(150, 0, 10)
    time.sleep(1)
    ctrlBot.moveArmXYZ(150, 0, 70)
    ctrlBot.moveArmXYZ(150, 40, 13)
    ctrlBot.toggleSuction(False)

 

    print("Disconnecting")

if __name__ == "__main__":
    main()
