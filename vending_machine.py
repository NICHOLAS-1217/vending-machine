import os

# Global variables for both DFA and NFA
items = {
   "1": {"name": "water", "price": 2.00},
   "2": {"name": "soda", "price": 3.50},
   "3": {"name": "chips", "price": 4.50},
   "4": {"name": "chocolate", "price": 6.00},
   "5": {"name": "coffee", "price": 7.50},
   "6": {"name": "juice", "price": 8.50},
   "7": {"name": "sandwich", "price": 9.00},
   "8": {"name": "energy drink", "price": 10.00}
}

valid_coins = [0.5, 1.0]

def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')

def display_items():
   print("\n=== Available Items ===")
   for key, item in items.items():
      print(f"{key}. {item['name']} - RM{item['price']:.2f}")

# =========================== DFA VERSION ===========================
dfa_state = "IDLE"
dfa_selected_item = None
dfa_required_amount = 0
dfa_inserted_amount = 0
dfa_change = 0

def dfa_display_state():
   print(f"DFA Current State: {dfa_state}")
   if dfa_selected_item:
      print(f"Selected Item: {dfa_selected_item['name']} (RM{dfa_selected_item['price']:.2f})")
   else: 
      print("Selected Item: No item selected")
   if dfa_inserted_amount > 0:
      print(f"Amount Inserted: RM{dfa_inserted_amount:.2f}")
   else:
      print("Amount Inserted: RM0.0")
   if dfa_required_amount > 0:
      remaining = max(0, dfa_required_amount - dfa_inserted_amount)
      print(f"Amount Remaining: RM{remaining:.2f}")
   else:
      print("Amount Remaining: RM0.0")

def dfa_select_item(item_code):
   global dfa_state, dfa_selected_item, dfa_required_amount
   
   clear_screen()
   print(f"\n>>> DFA Input: Select item {item_code}")
   
   if dfa_state != "IDLE":
      print("❌ Error: Can only select items in IDLE state")
      return False
   
   if item_code not in items:
      print("❌ Invalid item code")
      return False
   
   # DFA State transition: IDLE -> ITEM_SELECTED
   dfa_selected_item = items[item_code]
   dfa_required_amount = dfa_selected_item["price"]
   dfa_state = "ITEM_SELECTED"
   
   print(f"DFA State Transition: IDLE -> ITEM_SELECTED")
   print(f"Selected: {dfa_selected_item['name']} (RM{dfa_required_amount:.2f})")
   dfa_display_state()
   return True

def dfa_insert_coin(coin_value):
   global dfa_state, dfa_inserted_amount
   
   clear_screen()
   print(f"\n>>> DFA Input: Insert coin RM{coin_value}")
   
   if coin_value not in valid_coins:
      print(f"❌ Invalid coin RM{coin_value} - Returned")
      return False
   
   if dfa_state not in ["ITEM_SELECTED", "PAYMENT_IN_PROGRESS"]:
      print("❌ Error: Please select an item first")
      return False
   
   # DFA State transition
   if dfa_state == "ITEM_SELECTED":
      print("✅ DFA State Transition: ITEM_SELECTED -> PAYMENT_IN_PROGRESS")
      dfa_state = "PAYMENT_IN_PROGRESS"
   
   dfa_inserted_amount += coin_value
   print(f"✅ Coin Accepted: RM{coin_value}")
   
   if dfa_inserted_amount >= dfa_required_amount:
      dfa_dispense_item()
   else:
      print(f"✅ DFA State Remains: PAYMENT_IN_PROGRESS")
      dfa_display_state()
   
   return True

def dfa_dispense_item():
   global dfa_state, dfa_change
   
   print(f"\n>>> DFA Auto Process: Dispensing")
   dfa_state = "DISPENSING"
   print("✅ DFA State Transition: PAYMENT_IN_PROGRESS -> DISPENSING")
   
   dfa_change = dfa_inserted_amount - dfa_required_amount
   print(f"🎉 Dispensing: {dfa_selected_item['name']}")
   print(f"💰 Change: RM{dfa_change:.2f}")
   
   if dfa_change > 0:
      dfa_state = "CHANGE_RETURN"
      print("✅ DFA State Transition: DISPENSING -> CHANGE_RETURN")
      dfa_return_change()
   else:
      dfa_reset_machine()

def dfa_return_change():
   print(f"\n>>> DFA Auto Process: Returning change RM{dfa_change:.2f}")
   print("✅ DFA State Transition: CHANGE_RETURN -> IDLE")
   dfa_reset_machine()

def dfa_reset_machine():
   global dfa_state, dfa_selected_item, dfa_required_amount, dfa_inserted_amount, dfa_change
   
   print("\n🔄 DFA Transaction Complete, Machine Reset")
   dfa_state = "IDLE"
   dfa_selected_item = None
   dfa_required_amount = 0
   dfa_inserted_amount = 0
   dfa_change = 0
   print("✅ DFA State Transition to: IDLE")
   dfa_display_state()

def run_dfa_simulation():
   clear_screen()
   print("=== DFA Vending Machine Started ===")
   dfa_display_state()
   
   while True:
      display_items()
      print("\n=== DFA Operations ===")
      print("s <item_number> - Select item")
      print("c <amount> - Insert coin (0.5 or 1.0)")
      print("q - Return to main menu")
      
      user_input = input("\nEnter operation: ").strip().lower()
      
      if user_input == 'q':
         break
      elif user_input.startswith('s '):
         try:
            item_code = user_input.split()[1]
            dfa_select_item(item_code)
            input("Press Enter to continue...")
         except IndexError:
            print("❌ Please enter item number, e.g.: s 1")
            input("Press Enter to continue...")
      elif user_input.startswith('c '):
         try:
            coin = float(user_input.split()[1])
            dfa_insert_coin(coin)
            input("Press Enter to continue...")
         except (IndexError, ValueError):
            print("❌ Please enter valid amount, e.g.: c 0.5")
            input("Press Enter to continue...")
      else:
         print("❌ Invalid command")
         input("Press Enter to continue...")

# =========================== NFA VERSION ===========================

# NFA Global Variables
nfa_current_states = {"IDLE"}
nfa_selected_item = None
nfa_required_amount = 0
nfa_inserted_amount = 0
nfa_change = 0

def nfa_display_states():
   print(f"\nNFA Current State Set: {nfa_current_states}")
   if nfa_selected_item:
      print(f"Selected Item: {nfa_selected_item['name']} (RM{nfa_selected_item['price']:.2f})")
   else: 
      print("Selected Item: No item selected")
   if nfa_inserted_amount > 0:
      print(f"Amount Inserted: RM{nfa_inserted_amount:.2f}")
   else: 
      print("Amount Inserted: RM0.0")
   if nfa_required_amount > 0:
      remaining = max(0, nfa_required_amount - nfa_inserted_amount)
      print(f"Amount Remaining: RM{remaining:.2f}")
   else:
      print("Amount Remaining: RM0.0")

def nfa_epsilon_closure(states):
   """NFA epsilon transitions for change handling"""
   closure = set(states)
   
   if "DISPENSING" in closure and nfa_change > 0:
      closure.add("CHANGE_RETURN")
      print("🔄 NFA Epsilon Transition: DISPENSING -> CHANGE_RETURN")
   
   if "CHANGE_RETURN" in closure:
      closure.add("IDLE")
      print("🔄 NFA Epsilon Transition: CHANGE_RETURN -> IDLE")
    
   return closure

def nfa_select_item(item_code):
   global nfa_current_states, nfa_selected_item, nfa_required_amount
   
   clear_screen()
   print(f"\n>>> NFA Input: Select item {item_code}")
   
   if "IDLE" not in nfa_current_states:
      print("❌ Error: Can only select items in IDLE state")
      return False
   
   if item_code not in items:
      print("❌ Invalid item code")
      return False
   
   # NFA State transition
   nfa_selected_item = items[item_code]
   nfa_required_amount = nfa_selected_item["price"]
   nfa_current_states = {"ITEM_SELECTED"}
   
   print(f"✅ NFA State Transition: {{IDLE}} -> {{ITEM_SELECTED}}")
   print(f"Selected: {nfa_selected_item['name']} (RM{nfa_required_amount:.2f})")
   nfa_display_states()
   return True

def nfa_insert_coin(coin_value):
   global nfa_current_states, nfa_inserted_amount
   
   clear_screen()
   print(f"\n>>> NFA Input: Insert coin RM{coin_value}")
   
   if coin_value not in valid_coins:
      print(f"❌ Invalid coin RM{coin_value} - Returned")
      return False
   
   if not nfa_current_states.intersection({"ITEM_SELECTED", "PAYMENT_IN_PROGRESS"}):
      print("❌ Error: Please select an item first")
      return False
   
   # NFA State transition - can be in multiple states
   new_states = set()
   
   if "ITEM_SELECTED" in nfa_current_states:
      new_states.add("PAYMENT_IN_PROGRESS")
      print("✅ NFA State Transition: ITEM_SELECTED -> PAYMENT_IN_PROGRESS")
   
   if "PAYMENT_IN_PROGRESS" in nfa_current_states:
      new_states.add("PAYMENT_IN_PROGRESS")
   
   nfa_current_states = new_states
   nfa_inserted_amount += coin_value
   print(f"✅ Coin Accepted: RM{coin_value}")
   
   if nfa_inserted_amount >= nfa_required_amount:
      nfa_dispense_item()
   else:
      nfa_display_states()
   
   return True

def nfa_dispense_item():
   global nfa_current_states, nfa_change
   
   print(f"\n>>> NFA Auto Process: Dispensing")
   nfa_current_states = {"DISPENSING"}
   print("✅ NFA State Transition: PAYMENT_IN_PROGRESS -> DISPENSING")
   
   nfa_change = nfa_inserted_amount - nfa_required_amount
   print(f"🎉 Dispensing: {nfa_selected_item['name']}")
   print(f"💰 Change Required: RM{nfa_change:.2f}")
   
   # Apply epsilon closure for change handling
   nfa_current_states = nfa_epsilon_closure(nfa_current_states)
   
   if nfa_change > 0:
      nfa_handle_change()
   else:
      nfa_reset_machine()

def nfa_handle_change():
   print(f"\n>>> NFA Auto Change Processing")
   
   # Calculate change coins
   change_coins = []
   remaining_change = nfa_change
   
   while remaining_change >= 1.0:
      change_coins.append(1.0)
      remaining_change -= 1.0
   
   while remaining_change >= 0.5:
      change_coins.append(0.5)
      remaining_change -= 0.5
   
   print(f"🔄 NFA Change Processing (via epsilon transitions):")
   for coin in change_coins:
      print(f"   Returning coin: RM{coin}")
   
   print("✅ NFA Change Processing Complete")
   nfa_reset_machine()

def nfa_reset_machine():
   global nfa_current_states, nfa_selected_item, nfa_required_amount, nfa_inserted_amount, nfa_change
   
   print(f"\n🔄 NFA Transaction Complete, Machine Reset")
   print("🔄 NFA Epsilon Transition: All States -> IDLE")
   nfa_current_states = {"IDLE"}
   nfa_selected_item = None
   nfa_required_amount = 0
   nfa_inserted_amount = 0
   nfa_change = 0
   nfa_display_states()

def run_nfa_simulation():
   clear_screen()
   print("=== NFA Vending Machine Started ===")
   nfa_display_states()
   
   while True:
      print("\n" + "-"*30)
      display_items()
      print("\nNFA Operations:")
      print("s <item_number> - Select item")
      print("c <amount> - Insert coin (0.5 or 1.0)")
      print("q - Return to main menu")
      
      user_input = input("\nEnter operation: ").strip().lower()
      
      if user_input == 'q':
         break
      elif user_input.startswith('s '):
         try:
               item_code = user_input.split()[1]
               nfa_select_item(item_code)
               input("Press Enter to continue...")
         except IndexError:
               print("❌ Please enter item number, e.g.: s 1")
               input("Press Enter to continue...")
      elif user_input.startswith('c '):
         try:
               coin = float(user_input.split()[1])
               nfa_insert_coin(coin)
               input("Press Enter to continue...")
         except (IndexError, ValueError):
               print("❌ Please enter valid amount, e.g.: c 0.5")
               input("Press Enter to continue...")
      else:
         print("❌ Invalid command")
         input("Press Enter to continue...")

# =========================== MAIN PROGRAM ===========================
def main():
   while True:
      clear_screen()
      print("-"*40)
      print("|📱 Simple Vending Machine Simulator 📱|")
      print("-"*40)
      print("\n1. Run DFA Version")
      print("2. Run NFA Version")
      print("3. Exit")
      
      choice = input("\nPlease select (1-3): ").strip()
      
      if choice == "1":
         run_dfa_simulation()
      elif choice == "2":
         run_nfa_simulation()
      elif choice == "3":
         clear_screen()
         print("Thank you for using the vending machine!")
         break
      else:
         print("Invalid choice, please try again")
         input("Press Enter to continue...")

if __name__ == "__main__":
   main()