#
#       Vehicle Dealer Inventory Program (Pure Python)
#       Chris Stanley aka Kryptich
#

from time import sleep

##### The following useful functions are included to simplify error handling further down...

# Simple and tolerant choice way to take yes/no from user
def yesNo(question):
    while True:
        reply = str(input(question+' (Y/N): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

# Make user enter a number
def inputNumber(prompt):
    while True:
        try:
            userInput = int(input(prompt))
        except ValueError:
            print("Please enter numbers only -- no commas, spaces or currency symbol needed.")
            continue
        else:
            return userInput
            break

# global menu function, takes list of options and takes only valid input
def displayMenu(options, choice = 999):
    print("\n:::[MAIN MENU]:::\n")
    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    while choice >= (len(options)+1):
        choice = inputNumber("\nPlease choose an option: ")
    return choice

# Our main vehicle class. Has constructor, creator, display and formatting logic built in.
class Automobile:
    def __init__(self, vin, year, make, model, mileage, color, dtrain = ('N/A'), condition = ("N/A"), value = 0):
        self.vin = vin
        self.year = year
        self.make = make
        self.model = model
        self.mileage = mileage
        self.color = color
        self.dtrain = dtrain
        self.condition = condition
        self.value = value

    @classmethod            # A user interface for adding new vehicles.
    def from_input(cls, vin="", dtrain = ('N/A'), condition = ("N/A"), value = 0):
        if len(vin) < 1:    # this condition so that we can reuse the creator code for updating (existing VIN)
            vin = input("Complete vehicle identification number (VIN): ")
        year = inputNumber("Please enter vehicle year: ")
        make = input("Please enter vehicle make: ")
        model = input("Please enter vehicle model: ")
        mileage = inputNumber("Please enter mileage of vehicle: ")
        color = input("Please enter vehicle color: ")
        # To shorten the process, these values are optional for user to enter. If skipped, defaults are given as defined in function attr
        optionals = yesNo("\nWould you like to add drivetrain, vehicle condition or current value information?")
        if optionals:
            choice = 5
            #################################################### DRIVETRAIN ##########
            dtrain_list = ["2X2", "4x2", "4X4", "6X4"]
            while True:
                choice = inputNumber("\nDRIVETRAIN: Please choose a drivetrain configuration from the list: [1-4]" +
                '\n\n::: OPTIONS :::   [1]: "2x2"     [2]: 4x2     [3]: 4x4     [4]: 6x4   :::   ')
                if (choice > 0) and (choice < 5):
                    dtrain = dtrain_list[choice - 1]
                    break
                else:
                    print ("\nPlease choose valid option!")
            ################################################### CONDITION ############
            choice = 5
            condition_list = ["Junk", "Critical", "Bad", "Poor", "Fair", "Good", "Like New", "New"]
            while True:
                choice = inputNumber("\nCONDITION: Please choose vehicle condition from the list: [1-8]" +
                '\n\n::: OPTIONS :::   1 = Junk, 2 = Critical, 3 = Bad, 4 = Poor, 5 = Fair, 6 = Good, 7 = Like New, 8 = New   :::   ')
                if (choice > 0) and (choice < 9):
                    condition = condition_list[choice - 1]
                    break
                else:
                    print ("\nPlease choose valid option!")
            ################################################### VALUE ################
            value = inputNumber("\nVALUE: Please enter estimate of current value (if unknown, use KBB value): ")
        return cls(vin, year, make, model, mileage, color, dtrain, condition, value)

    def getVin(self):     # to find index for operating on vehicles (remove, update)
        return self.vin

    def Display(self):    # some pretty formatting work
        print("\nVIN:", self.vin.upper(),'\n    ',41*'_','\n')
        print("     Year:    |", self.year)
        print("     Make:    |", self.make.title())
        print("     Model:   |", self.model.title())
        print("     Mileage: |", "{:,}".format(self.mileage))
        print("     Color:   |", self.color.title(),'\n')
        print("     ----------- Other information:  ---------")
        print("     DRIVETRAIN:", self.dtrain, "   CONDITION:", self.condition, "   EST. VALUE:", "${:,.2f}".format(self.value),'\n')

    def Return(self):    # setup return function to pipe data elsewhere (such as file). dictionary worked better for making a string to output to file
        extraditedit = {'\nVIN:        |': self.vin,
                          'Year:       |': self.year,
                          'Make:       |': self.make,
                          'Model:      |': self.model,
                          'Mileage:    |': self.mileage,
                          'Color:      |': self.color,
                          'Drivetrain: |': self.dtrain,
                          'Condition:  |': self.condition,
                          'Value:      |': self.value}
        output = '\n'.join("{!s}  {!r}".format(key,val) for (key,val) in extraditedit.items())
        output = output.replace("'", "")
        return output

#### the inventory. Keeps track of array and facilitates addition, deletion, updating, displaying and exporting of Automobile items.
class Inventory(object):
    def __init__(self):
        self.inventory = []

    def add_item(self, vehicle):
        self.inventory.append(vehicle)

    def update_item(self):
        upd_nominee = input("Please enter the complete VIN number of the automobile you wish to update details for: ")
        for i in range(len(self.inventory)):
            if self.inventory[i].getVin() == upd_nominee.upper():
                print ("\nVehicle",upd_nominee,"was found in list. Enter new attributes:\n")
                self.inventory[i] = Automobile.from_input(upd_nominee)
                print ("\nVehicle",upd_nominee,'was successfully updated.')
                return upd_nominee
                break
        else:
            print('\nVIN of "',upd_nominee,'"not found. Please choose desired option again from menu and ensure correct entry.')

    def add_from_input(self):
        self.inventory.append(Automobile.from_input())

    def display_inventory(self):
        for i in range(len(self.inventory)):
            self.inventory[i].Display()
            sleep(0.3)

    def export_inventory(self):
        userfilename = str(input("\nEnter name to save file (extension will be added automatically): ") + ".txt")
        outfile = open(userfilename, "a")
        outfile.write("\nVEHICLE INVENTORY PROGRAM OUTPUT: \n")
        for i in range(len(self.inventory)):
            outfile.write('\n' + str(self.inventory[i].Return()) + '\n')
        outfile.close()
        input("\nINVENTORY EXPORT SUCCESSFUL. File was saved as '" + userfilename + "'. [ENTER]")

    def remove_item(self):
        del_nominee = input("\nPlease enter the complete VIN number of the automobile you wish to remove from inventory: ")
        for i in range(len(self.inventory)):
            if self.inventory[i].getVin() == del_nominee.upper():
                self.inventory.pop(i)
                print("\nVehicle with VIN of",del_nominee,"was removed from inventory.")
                break
        else:
            print("\nVIN not found. Please try again from menu and ensure correct entry.")


def main():
    # create an empty inventory
    inventory = Inventory()
    # make some automobiles
    inventory.add_item(Automobile("1HGB41JXMN109186", 2007, "Hyundai", "Accord", 185000, "Blue"))
    inventory.add_item(Automobile("1234HJH4891329H2", 1998, "Chevrolet", "Malibu", 213370, "White", "4X2", "Junk", 450))
    inventory.add_item(Automobile("2183945143NG8432", 2013, "Volkswagen", "Beetle", 87000, "Yellow"))
    inventory.add_item(Automobile("1289HOSA394304J9", 2005, "Nissan", "Micra", 259020, "Red", "4X4", "Good", 55000))
    inventory.add_item(Automobile("F43HLASDFO435N43", 2014, "Ford", "Fiesta", 30500, "Gold"))

    # List menu items for function
    menuItems = ['View Inventory','Add Vehicle','Remove Vehicle', 'Update Vehicle Attributes', 'Export to File', 'Quit']

    print("\nAutomobile Inventory System v 1.0")
    while True:
        choice = displayMenu(menuItems);
        if choice == 1:
            print("\nCURRENT AUTO INVENTORY CONTENTS:\n")
            sleep(0.8)
            inventory.display_inventory()
        elif choice == 2:
            print("\nADD NEW VEHICLE TO INVENTORY:\n")
            sleep(0.8)
            inventory.add_from_input()
            print("\nVEHICLE ADDITION SUCCESSFUL. Item can now be found in inventory listing. [ENTER]")
        elif choice == 3:
            inventory.remove_item()
        elif choice == 4:
            inventory.update_item()
        elif choice == 5:
            inventory.export_inventory()
        else:
            check = yesNo("\nARE YOU SURE? All data will be lost. Backup?")
            if check:
                inventory.export_inventory()
            print ("\nPROGRAM UNDERGOING TERMINATION.\n\nFinding eels, filling hovercrafts...\n")
            sleep(1)
            quit()

if __name__ == '__main__':
    main()
