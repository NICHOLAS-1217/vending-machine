import os

# States: IDLE, ITEM_SELECTED, PAYMENT_IN_PROGRESS, DISPENSING, CHANGE_RETURN

class VendingMachineDFA:

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
      
      self.state = "IDLE"
      self.selected_item = None
      self.required_amount = 0
      self.inserted_amount = 0
      self.change = 0
      
      # Define valid coin inputs
      self.valid_coins = [0.5, 1.0]
      
      print("=== DFA Vending Machine Started ===")
      self.display_current_state()
   
   def display_current_state(self):
      print(f"\nCurrent State: {self.state}")
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
   
   def select_item(self, item_code):
      os.system('cls')
      print(f"\n>>> Input: Select item {item_code}")
      
      if self.state != "IDLE":
         print("❌ Error: Can only select items in IDLE state")
         return False
      
      if item_code not in self.items:
         print("❌ Invalid item code")
         return False
      
      # State transition: IDLE -> ITEM_SELECTED
      self.selected_item = self.items[item_code]
      self.required_amount = self.selected_item["price"]
      self.state = "ITEM_SELECTED"
      
      print(f"✅ State Transition: IDLE -> ITEM_SELECTED")
      print(f"Selected: {self.selected_item['name']} (RM{self.required_amount:.2f})")
      self.display_current_state()
      return True
   
   def insert_coin(self, coin_value):
      os.system('cls')
      print(f"\n>>> Input: Insert coin RM{coin_value}")
      
      # Validate coin
      if coin_value not in self.valid_coins:
         print(f"❌ Invalid coin RM{coin_value} - Returned")
         print("Only RM0.5 and RM1.0 coins accepted")
         return False
      
      if self.state not in ["ITEM_SELECTED", "PAYMENT_IN_PROGRESS"]:
         print("❌ Error: Please select an item first")
         return False
      
      # State transition: ITEM_SELECTED/PAYMENT_IN_PROGRESS -> PAYMENT_IN_PROGRESS
      if self.state == "ITEM_SELECTED":
         print("✅ State Transition: ITEM_SELECTED -> PAYMENT_IN_PROGRESS")
         self.state = "PAYMENT_IN_PROGRESS"
      
      self.inserted_amount += coin_value
      print(f"✅ Coin Accepted: RM{coin_value}")
      
      # Check if enough money
      if self.inserted_amount >= self.required_amount:
         self.dispense_item()
      else:
         print(f"✅ State Remains: PAYMENT_IN_PROGRESS")
         self.display_current_state()
      
      return True
   
   def dispense_item(self):
      print(f"\n>>> Auto Process: Sufficient amount, preparing to dispense")
      
      # State transition: PAYMENT_IN_PROGRESS -> DISPENSING
      self.state = "DISPENSING"
      print("✅ State Transition: PAYMENT_IN_PROGRESS -> DISPENSING")
      
      # Calculate change
      self.change = self.inserted_amount - self.required_amount
      
      print(f"🎉 Dispensing: {self.selected_item['name']}")
      print(f"💰 Change: RM{self.change:.2f}")
      
      if self.change > 0:
         # State transition: DISPENSING -> CHANGE_RETURN
         self.state = "CHANGE_RETURN"
         print("✅ State Transition: DISPENSING -> CHANGE_RETURN")
         self.return_change()
      else:
         # State transition: DISPENSING -> IDLE
         self.reset_machine()
   
   def return_change(self):
      print(f"\n>>> Auto Process: Returning change RM{self.change:.2f}")
      
      # State transition: CHANGE_RETURN -> IDLE
      print("✅ State Transition: CHANGE_RETURN -> IDLE")
      self.reset_machine()
   
   def reset_machine(self):
      print("\n🔄 Transaction Complete, Machine Reset")
      self.state = "IDLE"
      self.selected_item = None
      self.required_amount = 0
      self.inserted_amount = 0
      self.change = 0
      print("✅ State Transition to: IDLE")
      self.display_current_state()
