# KEVIN BERGERON IT140 AUG-OCT 2024

inventory = [] # used to store inventory collected

# all the data for all the rooms. This will change as the user picks up items.
rooms = {
    "cryochamber" : {"name" : "the Cryochamber", "description" : "The room is cold. The cryopods are running fine as far as you can tell, but you're not the expert. You can see the open one you were in, all your crews' pods, and your lockers.", "east" : "cargo", "west" : "engineering"}, # starting point
    "cargo" : {"name" : "Cargo", "description" : "It is crowded with boxes from floor to ceiling. There's a table with packing supplies and a cabinet with random odds and ends.", "north" : "medical", "west" : "cryochamber", "pickup" : "duct tape"},
    "medical" : {"name" : "Medical", "description" : "The space is sterile and eerily quiet. There is no hum from any machinery or computers, just morbid silence. There's an exam table with fresh paper on it, and a tray of tools next to it.", "south" : "cargo", "west" : "galley", "pickup" : "laser scalpel"},
    "galley" : {"name" : "the Galley", "description" : "It appears as though it was left a bit of a mess by its last user, with an empty plate and mug on the table. There are a few things left on the counter near the coffee maker.", "north" : "bridge", "east" : "medical", "south" : "core", "west" : "cabin", "pickup" : "hand sanitizer"},
    "bridge" : {"name" : "the Bridge", "description" : "The computers are all lit up, navigating on autopilot. There doesn't seem to be any issues here, you're right on course so far as you can tell. You see seats for all the major members of the crew, including the Captain's chair.", "south" : "galley", "pickup" : "fan"},
    "cabin" : {"name" : "the Cabin", "description" : "The lights are out, which is normal for this time of the sol cycle. Each crew member has a bunch with some of their personal effects nearby.", "east" : "galley", "south" : "engineering", "pickup" : "Ol' StarBeast Whiskey"},
    "engineering" : {"name" : "Engineering", "description" : "This is the bowels of the ship, with exposed machinery and greasy gears. You see a wide assortment of tools around to help deal with repairing the engines or hull.", "north" : "cabin", "east" : "cryochamber", "pickup" : "foam sprayer"},
    "core" : {"name" : "the Core", "description" : "It has a singular glowing tube in the center with white and steel panelling throughout the room. There is a large insect-like creature glaringly out of place in this picture. It notices you enter the room and slowly stands up on its hein legs, apparently ready to attack.", "north" : "galley"} # final showdown
}

# will be used to verify valid inputs. This will allow the user to enter a variety of commands and will let us work with a standard via function convert_input()
valid_inputs = {
    "north" : ("north", "n", "up", "u"),
    "east" : ("east", "e", "right", "r"),
    "south" : ("south", "s", "down", "d"),
    "west" : ("west", "w", "left", "l"),
    "pickup" : ("pickup", "p", "pick", "grab", "g", "take", "t"),
    "exit" : ("exit", "esc", "x", "quit", "q")
}

### Message strings ###
start_msg = "You awake groggy and not exactly sure where you are. The room is bright, and as you sit up you can see 6 other pods, on either side of you. You hear a voice, and you remember you're on a space vessel on a long trip home and the computer is giving you instructions:\n'Hello crew member, you have been awoken early because I have detected a presence in our Core that needs to be destroyed. However, there are no defensive capabilities on this ship. You will need to gather some items from the ship and create your own defense. You need:\nThe captain's personal handheld cooling rod (fan to keep cool), the mechanic's foam sprayer (for external repairs), the doctor's laser scalpel (for emergency surgery), the pilot's bottle of whiskey (for recreation), the navigator's hand sanitizer (for his obsessive compulsive disorder), and the engineer's duct tape (to fix just about anything).\nOnce you have collected these items, you can make a weapon to destroy the intruder. Good luck!'"
exit_msg = "You jettison yourself out the airlock to escape the alien but float into space until you die of boredom. Bye!"
inv_msg = "You got the last item! You add the whiskey and hand sanitizer to the foam sprayer, use the duct tape to attach the laser scalpel and fan near the nozzle. You've made a pretty handy flame-thrower! Now, go to the core and kill that alien!"
input_msg = "Here are the options available to you: you can "
input_north = "go [N]orth"
input_east = "go [E]ast"
input_south = "go [S]outh"
input_west = "go [W]est"
input_last = "or e[X]it the game."
err_input = "Invalid command, please try again."
err_direction = "You can't go that way, move in a different direction."
err_pickup = "There is no item to pick up in this room."
end_win = "You used the make-shift weapon to blow fire at the alien! It screeches, writhes in pain burning, and drops lifeless on the hull floor. The computer announces:\n'Thank you for your service, you may return to your cryochamber pod and rest for the remainder of your travels. Have a pleasant day!'"
end_lose = "You approach the alien ill-prepared, without any way to defend yourself. It attacks with a crunching pounce, rips you apart, and you are killed. After a pause, the computer announces:\n'Releasing crew member from cryosleep...'"

def print_options(curr_room):
    """Display the options available to the user"""
    pickup_desc = ""
    print(f"You are in {rooms[curr_room]['name']}.")
    for key, value in rooms[curr_room].items():
        if key == "pickup":
            pickup_desc = "You can see the " + value + " here."
    print(f"{rooms[curr_room]['description']} {pickup_desc}")
    print(input_msg, end='')
    for key in rooms[curr_room].keys():
        if key == "north":
            print(f"{input_north} to {rooms[rooms[curr_room]['north']]['name']}, ", end='')
        if key == "east":
            print(f"{input_east} to {rooms[rooms[curr_room]['east']]['name']}, ", end='')
        if key == "south":
            print(f"{input_south} to {rooms[rooms[curr_room]['south']]['name']}, ", end='')
        if key == "west":
            print(f"{input_west} to {rooms[rooms[curr_room]['west']]['name']}, ", end='')
        if key == "pickup":
            print(f"[P]ickup the {rooms[curr_room]['pickup']} in this room, ", end='')
    print(input_last)
    if 6 - len(inventory) == 0:
        print("You have a bad-ass flame thrower. You had better head to the core and get rid of that alien!")
    elif 6 - len(inventory) == 1:
        print(f"There are 1 item left to collect. You have: {inventory}")
    else:
        print(f"There are {6 - len(inventory)} items left to collect. You have: {inventory}")

def convert_input(curr_room, usr_input):
    """Converts the user's input to something that is easily worked with"""
    usr_input = (usr_input.lower()).split()
    for i in usr_input:
        if i in valid_inputs["north"]:
            return "north"
        if i in valid_inputs["east"]:
            return "east"
        if i in valid_inputs["south"]:
            return "south"
        if i in valid_inputs["west"]:
            return "west"
        if i in valid_inputs["pickup"]:
            return "pickup"
        if i in valid_inputs["exit"]:
            return "exit"
        for key, value in rooms[curr_room].items():
            if i == value:
                return key
    return ""

def move_rooms(curr_room, usr_input):
    """Move the user from room to room. Returns new room"""
    for key, value in rooms[curr_room].items():
        if key == usr_input:
            return value
    print(err_direction)
    return curr_room

def pickup_item(curr_room):
    """Picks up item and adds it to inventory. Returns new inventory item"""
    for key, value in rooms[curr_room].items():
        if key == "pickup":
            inventory.append(value)
            print(f"You pick up the {value}")
            del rooms[curr_room][key]
            if len(inventory) == 6:
                print(inv_msg)
            return
    print(err_pickup)

def main():
    conv_input = ""
    user_input = ""
    current_room = "cryochamber"
    print(start_msg)

    while conv_input != "exit": # loop infinitely, game will exit on game over
        conv_input = ""
        user_input = ""
        print()
        print("*" * 50)
        print_options(current_room)
        user_input = input(">>>>> Pick a command: ")
        print()
        conv_input = convert_input(current_room, user_input)
        if conv_input == "":
            print(err_input)
            continue
        elif conv_input == "exit":
            print(exit_msg)
            continue
        elif conv_input == "pickup":
            pickup_item(current_room)
            continue
        else:
            current_room = move_rooms(current_room, conv_input)
        if current_room == "core":
            if len(inventory) == 6:
                print(end_win)
            else:
                print(end_lose)
            conv_input = "exit"

main()