import os

# Includes epsilon transitions for change handling

class VendingMachineNFA:
   
   def __init__(self):
      self.items = {
         "1": {"name": "water", "price": 2.00},
         "2": {"name": "soda", "price": 3.50},
         "3": {"name": "chips", "price": 4.50},
         "4": {"name": "chocolate", "price": 6.00},
         "5": {"name": "coffee", "price": 7.50},
         "6": {"name": "juice", "price": 8.50},
         "7": {"name": "sandwich", "price": 9.00},
         "8": {"name": "energy drink", "price": 10.00}
      }
      
      # NFA can be in multiple states simultaneously
      self.current_states = {"IDLE"}
      self.selected_item = None
      self.required_amount = 0
      self.inserted_amount = 0
      self.change = 0
      self.valid_coins = [0.5, 1.0]
      
      print("=== NFA Vending Machine Started ===")
      self.display_current_states()
   
   def display_current_states(self):
      print(f"\nCurrent State Set: {self.current_states}")
      if self.selected_item:
         print(f"Selected Item: {self.selected_item['name']} (RM{self.selected_item['price']:.2f})")
      if self.inserted_amount > 0:
         print(f"Amount Inserted: RM{self.inserted_amount:.2f}")
      if self.required_amount > 0:
         remaining = max(0, self.required_amount - self.inserted_amount)
         print(f"Amount Remaining: RM{remaining:.2f}")
   
   def display_items(self):
      print("\n=== Available Items ===")
      for key, item in self.items.items():
         print(f"{key}. {item['name']} - RM{item['price']:.2f}")
   
   def epsilon_closure(self, states):
      """Calculate epsilon closure - NFA specific feature"""
      closure = set(states)
      
      # Add epsilon transition rules
      if "DISPENSING" in closure and self.change > 0:
         closure.add("CHANGE_CALCULATION")
         print("🔄 Epsilon Transition: DISPENSING -> CHANGE_CALCULATION")
      
      if "CHANGE_CALCULATION" in closure:
         closure.add("CHANGE_RETURN")
         print("🔄 Epsilon Transition: CHANGE_CALCULATION -> CHANGE_RETURN")
      
      return closure
   
   def select_item(self, item_code):
      os.system('cls')
      print(f"\n>>> Input: Select item {item_code}")
      
      if "IDLE" not in self.current_states:
         print("❌ Error: Can only select items in IDLE state")
         return False
      
      if item_code not in self.items:
         print("❌ Invalid item code")
         return False
      
      # NFA state transition
      self.selected_item = self.items[item_code]
      self.required_amount = self.selected_item["price"]
      self.current_states = {"ITEM_SELECTED"}
      
      print(f"✅ NFA State Transition: {{IDLE}} -> {{ITEM_SELECTED}}")
      print(f"Selected: {self.selected_item['name']} (RM{self.required_amount:.2f})")
      self.display_current_states()
      return True
   
   def insert_coin(self, coin_value):
      os.system('cls')
      print(f"\n>>> Input: Insert coin RM{coin_value}")
      
      # Validate coin
      if coin_value not in self.valid_coins:
         print(f"❌ Invalid coin RM{coin_value} - Returned")
         print("Only RM0.5 and RM1.0 coins accepted")
         return False
      
      if not self.current_states.intersection({"ITEM_SELECTED", "PAYMENT_IN_PROGRESS"}):
         print("❌ Error: Please select an item first")
         return False
      
      # NFA state transition - can be in multiple states
      new_states = set()
      
      if "ITEM_SELECTED" in self.current_states:
         new_states.add("PAYMENT_IN_PROGRESS")
         print("✅ NFA State Transition: ITEM_SELECTED -> PAYMENT_IN_PROGRESS")
      
      if "PAYMENT_IN_PROGRESS" in self.current_states:
         new_states.add("PAYMENT_IN_PROGRESS")
      
      self.current_states = new_states
      self.inserted_amount += coin_value
      print(f"✅ Coin Accepted: RM{coin_value}")
      
      # Check if enough money
      if self.inserted_amount >= self.required_amount:
         self.dispense_item()
      else:
         self.display_current_states()
      
      return True
   
   def dispense_item(self):
      print(f"\n>>> Auto Process: Sufficient amount, preparing to dispense")
      
      # NFA state transition
      self.current_states = {"DISPENSING"}
      print("✅ NFA State Transition: PAYMENT_IN_PROGRESS -> DISPENSING")
      
      # Calculate change
      self.change = self.inserted_amount - self.required_amount
      
      print(f"🎉 Dispensing: {self.selected_item['name']}")
      print(f"💰 Change Required: RM{self.change:.2f}")
      
      # Apply epsilon closure for change handling
      self.current_states = self.epsilon_closure(self.current_states)
      
      if self.change > 0:
         self.handle_change()
      else:
         self.reset_machine()
   
   def handle_change(self):
      print(f"\n>>> NFA Auto Change Processing")
      
      # Simulate change handling epsilon transition sequence
      change_coins = []
      remaining_change = self.change
      
      # Prioritize larger denomination coins for change
      while remaining_change >= 1.0:
         change_coins.append(1.0)
         remaining_change -= 1.0
      
      while remaining_change >= 0.5:
         change_coins.append(0.5)
         remaining_change -= 0.5
      
      print(f"🔄 Change Processing (via epsilon transitions):")
      for coin in change_coins:
         print(f"   Returning coin: RM{coin}")
      
      print("✅ Change Processing Complete")
      self.reset_machine()
   
   def reset_machine(self):
      print(f"\n🔄 Transaction Complete, NFA Reset")
      
      # Epsilon transition back to IDLE
      print("🔄 Epsilon Transition: All States -> IDLE")
      self.current_states = {"IDLE"}
      self.selected_item = None
      self.required_amount = 0
      self.inserted_amount = 0
      self.change = 0
      self.display_current_states()
