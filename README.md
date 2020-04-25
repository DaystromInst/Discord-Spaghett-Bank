**WHEN GENERATING THE OAUTH2 LINK, THE APPLICATION SHOULD HAVE ADMIN PERMISSIONS**

# Main.py

## Global Variables/Files
---

### **BankBook.json**

Json file, stores the wallet information.

- Top level keys are user id numbers
- Each key maps to a name entry and a balance entry


### **data**
Dictionary object to store info from BankBook.json

### **TOKEN**
Const string stores the bot token

### **level_info**
Dictionary object to store mining info from leveling.json.

### **casino**
Object of Gamble class.

# Basic Functions
---

## parse_payment(message)

message: List of strings

Function searches the list for a string that contains only base 10 numbers and no other characters.

returns type int



## ledger()

Overwrites the altered info from data to BankBook.json



# Discord Events and Commands
---

## Events

### on_ready()

Basic event. Pulls info from BankBook.json into data and prints to the console that everything's ready.



## Commands


### help(ctx)

ctx: Context object

Custom help command. Messages the channel with command instructions.


### slots(ctx)
ctx: Context object

Parses out the wager and plants it in the Gamble object.
Subtracts the wager from the user's wallet entry and calls Gamble.roll_slots(player id).
Reacts based on the results.


### stimulus(ctx)

![Meanwhile at Jerome Powell's coke house](https://www.google.com/url?sa=i&url=https%3A%2F%2Fknowyourmeme.com%2Fmemes%2Fmoney-printer-go-brrr&psig=AOvVaw0EKl4D-rJpE_z6_Hd76Kvh&ust=1587347845090000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJCL5Nax8-gCFQAAAAAdAAAAABAg)

ctx: Context object

Admin only command. Inflates the economy, generating an amount of spaghett and putting it into the mentioned account.


### debt(ctx)

ctx: Context object

Admin only command. Deflates the economy, removing an amount of spaghett from the mentioned account.
Passing a positive or negative value to the command should have the same effect because it uses absolute values.



### deposit(ctx)

ctx: Context object

Allows users to pay each other. Calls parse_payment() to determine the amount and then checks if the wallet can finance the payment.



### balance(ctx)

Checks the author's balance and sends it as a message to the channel where it was invoked.



### leave(ctx)

Calls ledger() then closes the client and logs the bot out of discord.



# Command use
---

## debt
`~debt @<the user to tax> <the integer amount of the debt>`

## deposit
`~deposit @<user to pay> <integer amount being paid>`

## stimulus
`~stimulus @<the user to pay> <integer amount to be paid>`

## slots
`~slots <integer spaghett wager>`

in general, the command syntax is `~<command>`

commands not listed in this section take no arguments and therefore can simply be invoked by their name preceded by a tilde (`~`).

---

# Gambler.py (Class Gamble)
---
`self.bets` -> holds wagers keyed to the ID of the users who placed them

## Methods

### `setBet(self, wager, user)`
    Inserts the wager into self.bets and sets the key to user.

### `get_bet(self, user)`
    Simple getter method for wagers.

### `roll_slots(self, user)`
    First checks if a bet exists for the user.
    If `None`, returns an error message

    Rolls 3 random integers 0 - 9 (inclusive)
    If they all match, the player wins.

    *Returns: (winnings or 0), result message, list of numbers rolled*

# Extra Files

## These files aren't included in git for privacy reasons. However they are very necessary so you *will* need to write them.
---

## leveling.json
- Main keys are user IDs.
- Each entry holds another dictionary with keys `time`, `xp`, and `level`.
- `time`: Holds a stringified version of a datetime object containing a time in `"%X"` format.
- `xp`: Holds a float with the amount of xp accrued.


## BankBook.json
- Main keys are also user IDs
- Each entry holds another dictionary with keys `"name"` and `"balance"`
- `"name"`: The individual's display name as a string. Not important but it's there.
- `"balance"`: The spaghett balance as an int.


## token.txt
Simply for holding the app token.
