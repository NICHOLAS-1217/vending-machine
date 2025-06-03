import os
from NFA import VendingMachineNFA
from DFA import VendingMachineDFA 


def run_dfa_simulation():
    os.system('cls')
    print("\n" + "="*50)
    vm = VendingMachineDFA()
    
    while True:
        print("\n" + "-"*30)
        vm.display_items()
        print("\nAvailable Operations:")
        print("s <item_number> - Select item")
        print("c <amount> - Insert coin (0.5 or 1.0)")
        print("q - Return to main menu")
        
        user_input = input("\nEnter operation: ").strip().lower()
        
        if user_input == 'q':
            break
        elif user_input.startswith('s '):
            try:
                item_code = user_input.split()[1]
                vm.select_item(item_code)
                input("Press Enter to continue...")
            except IndexError:
                print("❌ Please enter item number, e.g.: s 1")
                input("Press Enter to continue...")
        elif user_input.startswith('c '):
            try:
                coin = float(user_input.split()[1])
                vm.insert_coin(coin)
                input("Press Enter to continue...")
            except (IndexError, ValueError):
                print("❌ Please enter valid amount, e.g.: c 0.5")
                input("Press Enter to continue...")
        else:
            print("❌ Invalid command")
            input("Press Enter to continue...")

def run_nfa_simulation():
    os.system('cls')
    print("\n" + "="*50)
    vm = VendingMachineNFA()
    
    while True:
        print("\n" + "-"*30)
        vm.display_items()
        print("\nAvailable Operations:")
        print("s <item_number> - Select item")
        print("c <amount> - Insert coin (0.5 or 1.0)")
        print("q - Return to main menu")
        
        user_input = input("\nEnter operation: ").strip().lower()
        
        if user_input == 'q':
            break
        elif user_input.startswith('s '):
            try:
                item_code = user_input.split()[1]
                vm.select_item(item_code)
                input("Press Enter to continue...")
            except IndexError:
                print("❌ Please enter item number, e.g.: s 1")
                input("Press Enter to continue...")
        elif user_input.startswith('c '):
            try:
                coin = float(user_input.split()[1])
                vm.insert_coin(coin)
                input("Press Enter to continue...")
            except (IndexError, ValueError):
                print("❌ Please enter valid amount, e.g.: c 0.5")
                input("Press Enter to continue...")
        else:
            print("❌ Invalid command")
            input("Press Enter to continue...")

def main():
    while True:
        os.system('cls')
        print("\n" + "="*50)
        print("Vending Machine Simulator")
        print("1. Run DFA Version")
        print("2. Run NFA Version")
        print("3. Exit")
        
        choice = input("Please select (1-3): ").strip()
        
        if choice == "1":
            run_dfa_simulation()
        elif choice == "2":
            run_nfa_simulation()
        elif choice == "3":
            os.system('cls')
            print("Thank you for using the vending machine!")
            break
        else:
            print("Invalid choice, please try again")
            input("Press Enter to continue...")

if __name__ == "__main__":
   main()