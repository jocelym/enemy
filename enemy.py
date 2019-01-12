"""
Jocelyn Lim
This program implements a finite state machine to run a simple battle game
run by lists, if statements, and user input.
The finite state machine will run the enemy's movements.
The game is turn based, and the player and enemy wil take turns attacking, 
dodging attacks, and seeking aid

"""
import random


#initializing variables
player_location = 10
enemy_location = 0
player_hp = 100
enemy_hp = 100
enemy_states = ["wander", "attack", "evade", "seek aid"]
player_states = ["Move forward", "Move backward", "Attack", "Evade", "Seek first aid", "See rules"]
enemy_state = "wander"
player_has_moved = False
enemy_has_moved = False
is_playing = True
try_again = ""

#function to print rules of the game
def print_rules():
    print "\nMoving forward will increase your location by one unit\n"
    print "Moving backward will decrease your location by one unit\n"
    print "When someone attacks, there is a 90% chance that the opponents HP" 
    print "goes down 20 pts unless the opponent evades.  Attacks can only be" 
    print "successful if the player and the enemy are two or fewer units apart" 
    print "at the beginning of the turn.\n"
    print "When someone evades, there is a 50% chance that the opponent's attack" 
    print "will fail. There is no penalty for evading if the opponent does not"
    print "attack\n"
    print "When someone seeks first aid, they walk away from the opponent 1 unit" 
    print "the first time they perform the action. Then they seek first aid." 
    print "There is a 25% chance that they will regain 50pts of their HP."
    
#function to welcome 
def welcome():
    print "Welcome to enemy!"
    while True:
        see_rules = raw_input("\nWould you like to see rules? (y/n)\n\n").lower()
        
        if see_rules == "y":
            print_rules()
            break
            
        elif see_rules == "n":
            break
        
        else:
            print "\ninvalid raw_input"
        
#outputting enemy and user information
#aquiring user raw_input
def initial_print(p_location, e_location, p_hp, e_hp, player_outputs):
    
    #printint player location, enemy location, player hp and enemy hp
    print "---------------------------------------------------------------------"
    print "Player location:", p_location
    print "Enemy location:", e_location, "\n"
    print "Player hp:", p_hp
    print "Enemy hp:", e_hp, "\n"
    print "Choose an action."
    print "Valid raw_inputs are:"
    
    #printing valid raw_inputs
    for i in range(5):
        print str(i+1) + ". " +  str(player_outputs[i])
        
    
        

#function to allow player to move forward one unit
#takes current location as parameter
#returns location + 1
def move_forward(location):
    location += 1
    return location

#function to allow player to move forward one unit
#takes current location as parameter
#returns location - 1   
def move_backward(location): 
    location -= 1
    return location

#function to allow player to attack
#takes attacker location, defender location and defender hp as parameters
#returns defender hp
def attack(difference, def_hp):
    
    
    #using random numbers to determine whether attack is sucessful
    probability = random.randint(1,10)

    # if player is within two units, attacker will attack
    if difference <= 2: 
        
        #if attack is sucessful, defender hp will decrease by 20
        if probability <= 9:
            print "attack sucessful\n"
            def_hp -= 20

    #if attack is unsucessful, defender hp will remain constant
        else: 
            print "attack unsucessful\n"
            
    #if player is too far, nothing will change       
    else: 
        print "too far away to attack\n"

    #returning defender hp
    return def_hp

#function to allow player to evade
#takes hp as parameter
#returns hp
def evade(hp, difference):
    
    # if player is within two units, attacker will attack
    if difference <= 2:
    
        #using random numbers to determine whether evade is sucessful
        probability = random.randint(1,2)
        
        #if evade is unsucessful hp will decrease by 20
        if probability == 2:
            hp -= 20
            print "evade unsucessful\n"
        
        #if evade is sucessful hp will remain constant
        else:
            print "evade sucessful\n"
            
    #if player is too far, nothing will change       
    else:
        print "too far away to attack\n"
            
    #returns hp value
    return hp 


#function to allow player to seek aid
#takes location and hp as parameters
#returns hp
def seek_aid(att_location, def_location, hp, moved):
    
    #player steps away by one unit if they have not yet moved
    if moved == False and att_location > def_location:
        def_location -= 1
        moved = True
    
    elif moved == False and att_location < def_location:
        def_location += 1
        moved = True
    

    #using random numbers to determine whether find aid is sucessful
    probability = random.randint(1,4)
    
    #if seek aid is sucessful, hp will increase by 50
    if probability == 1:
        hp += 50
        print "seek aid sucessful\n"
    
    #if seek aid in unsucussful, hp remains constant
    else:
        print "seek aid unsucessful\n"
        
    #returns hp
    return def_location, hp, moved


#function to allow enemy to wander
#takes location parameter
#returns location and current state
def wander(location):
    
    #using random numbers to allow enemy to move randomly
    probability = random.randint(1,2)
    
    #if probability is 2, enemy will move forward
    if probability == 2:
        location = move_forward(location)
        print "enemy moved forward\n"
    
    #if probability is 1, enemy will move backward
    else:
        location = move_backward(location)
        print "enemy moved backward\n"
    
    return location


#aquiring user move
def player_move(player_states):
    
    #retrieving user raw_input as an integer
    #ensuring it is an integer between 1 and 5
    while True:
        
        try:
            user_move = int(raw_input("\n"))
            
            if user_move > 5 or user_move < 1:
        
                print "\nThat is not a valid raw_input"
            
                continue
            
            break
                    
        except ValueError:
            
            print "\nInvalid raw_input"
            
            
    #determing what the user move is using a for loop and looping through all 
    #indexes of the list
    for i in range(len(player_states)):
        
        if user_move == i + 1:
        
            #setting user action as variable
            user_action = player_states[i]
            
            #printing user action
            print "\nyour action is", user_action.lower(), "\n"
            
            #returning user action
            return user_action
            
#function determining enemy move
# takes last state, user action, enemy hp, enemy location, player location, 
# enemy state list, and player state list as arguements
#returns and prints enemy state
def enemy_moves(last_state, player_action, hp, e_location, p_location, enemy_state_list, player_state_list, difference):

    #cycling through two options if state is wander
    if last_state == enemy_state_list[0]:
        
        #if player is two or less units away, enemy will attack
        if difference <= 2:
            enemy_state = enemy_state_list[1]
            

        #if none of the above is applicable, enemy will remain in wander
        else:
            enemy_state = last_state                   


    #cycling through three options if state is attack
    elif last_state == enemy_state_list[1]:
    
        #if player is three or more units away, enemy will wander        
        if difference >= 3:
            enemy_state = enemy_state_list[0]
        
        #if the user attacks, enemy will evade
        elif player_action == player_state_list[2]:
            enemy_state = enemy_state_list[2]
            
        #if none of the above apply, enemy will remain in attack    
        else:
            enemy_state = last_state

    #cycling through three options if state is evade
    elif last_state == enemy_state_list[2]:
        
        #if health is at or below 50, enemy will seek aid
        if hp <= 50:
            enemy_state = enemy_state_list[3]
        
        #if user does not attack, enemy will attack
        elif player_action != player_state_list[2]:
            
            enemy_state = enemy_state_list[1]
        
        #if none of the above is applicable, enemy will remain in evade
        else:
            enemy_state = last_state

    #cycling through two options if state is seek aid
    elif last_state == enemy_state_list[3]:
        
        #if enemy hp is above 50, enemy will wander
        if hp > 50:
            enemy_state = enemy_state_list[0]
            
        #if none of the above is applicable, enemy remains in seek aid state
        else:
            enemy_state = last_state
    
    #printing enemy state
    print "enemy state is", enemy_state.lower(), "\n"
    
    #returning new enemy_state
    return enemy_state
            

    
#main function performing all player moves
#takes enemy location, player location player hp, enemy hp, and enemy current 
#state whether player has moved, player states, enemy states, user move, and 
#enemy move as parameters
#returns player location, enemy location, player hp, enemy hp, and if enemy has 
#moved
def player_execute(p_location, e_location, p_hp, e_hp, has_moved, player_states, enemy_state_list, user_move, enemy_move, difference):
    
    #if user move is move forward, move forward function is called with player 
    #location as a parameter
    #location is saved to a variable
    if user_move == player_states[0]:
        
        p_location = move_forward(p_location)
        
    #if user move is move backward, move backward function is called with player 
    #location as a parameter
    #returned location is saved to a variable
    elif user_move == player_states[1]:
        
        p_location = move_backward(p_location)
        
    #if user move is attack, and enemy doesn't evade attack function is called 
    #with player location
    #enemy location and enemy hp as parameters
    #returned enemy hp is saved to a variable
    elif user_move == player_states[2] and enemy_move != enemy_states[2]:
        
        e_hp = attack(difference, e_hp)
        

    #if user move is evade, evade function is called with player hp as parameter
    #returned hp is saved to a variable
    elif user_move == player_states[3] and enemy_move != enemy_states[1]:
        print "user evaded but enemy did not attack\n"
        
    elif user_move == player_states[3] and enemy_move == enemy_states[1]:
        p_hp = evade(p_hp, difference)
        
    #if user move is seek aid, seek aid function is called with player location
    #and player hp as parameters
    #returned location and hp is saved to a variable
    elif user_move == player_states[4]:
        
        p_location, p_hp, has_moved = seek_aid(e_location, p_location, p_hp, has_moved)
        
    #ensuring the player hp does not exceed 100
    if p_hp > 100:
        p_hp = 100
        print "player hp cannot exceed 100\n"

    #returns player location, enemy location, player hp and enemy location
    return p_location, p_hp, e_hp, has_moved
    
    
#main function performing all enemy moves
#takes enemy location, player location and enemy hp, and enemy current state 
#as parameters
#returns enemy location, player location and enemy hp, and enemy current state   
def enemy_execute(p_location, e_location, p_hp, e_hp, current_state, user_move, has_moved, enemy_state_list, player_state_list, difference):

    #if enemy state is wander, wander function will be called
    if current_state == enemy_state_list[0]:
        
        #calling wander function with enemy location as parameter
        e_location = wander(e_location)
    
    #if enemy state is attack, and user move is not evade, attack function will
    #be called
    elif current_state == enemy_state_list[1] and user_move != player_state_list[3]:
        
        #calling attack function difference and player hp as parameters
        p_hp = attack(difference, p_hp)
    
    #if enemy state is evade, evade function will be called
    elif current_state == enemy_state_list[2]:
        
        #calling evade function with enemy hp and difference as parameters
        e_hp = evade(e_hp, difference)
    
    #if enemy state is seek first aid, seek aid function will be called
    elif current_state == enemy_state_list[3]:
        
        #calling seek aid function with player location, enemy location, enemy
        #hp, and enemy has moved as parameters
        e_location, e_hp, has_moved = seek_aid(p_location, e_location, e_hp, has_moved)
        
    #ensuring enemy hp does not exceed 100
    if e_hp > 100:
        e_hp = 100
        
        
    #returning enemy location, player hp, and enemy has moved
    return e_location, p_hp, e_hp, has_moved    


def keep_playing(player_hp, enemy_hp, player_location, enemy_location, try_again):

    while True:
        
        try_again = raw_input("Try again?(y/n)\n\n").lower()

        
        if try_again == "y":
            player_hp = 100
            enemy_hp = 100
            player_location = 10
            enemy_location = 0
            
            break
        
        
        elif try_again == "n":
    
            break
        
        else:
            print "\ninvalid raw_input\n"
    
    return player_hp, enemy_hp, player_location, enemy_location, try_again

def main(player_location, enemy_location, player_hp, enemy_hp, enemy_states, player_states, enemy_state, player_has_moved, enemy_has_moved, is_playing, try_again):
    # A while loop to ensure allow the game to continue unless stated otherwise
    while True:
        #calculating difference at the beginning of the turn 
        difference = abs(player_location - enemy_location)
        
        #calling initial print function to output initial information
        initial_print(player_location, enemy_location, player_hp, enemy_hp, player_states)
        #calling user move function to determine user move
        user_move = player_move(player_states)
        #calling enemy state function to determine enemy current state
        enemy_state = enemy_moves(enemy_state, user_move, enemy_hp, enemy_location, player_location, enemy_states, player_states, difference)
        #calling player execute function to execute player move
        player_location, player_hp, enemy_hp, player_has_moved = player_execute(player_location, enemy_location, player_hp, enemy_hp, player_has_moved, player_states, enemy_states, user_move, enemy_state, difference)
        #calling enemy execute function to execute enemy move
        enemy_location, player_hp, enemy_hp, enemy_has_moved = enemy_execute(player_location, enemy_location, player_hp, enemy_hp, enemy_state, user_move, enemy_has_moved, enemy_states, player_states, difference)

        #determining whether the game is over
        #if player hp is lesser than 0, player loses
        if player_hp <= 0:
            
            print "you lose\n"
            
            #determining if the player would like to continue playing
            player_hp, enemy_hp, player_location, enemy_location, try_again = keep_playing(player_hp, enemy_hp, player_location, enemy_location, try_again)
            
            #if player doesnt want to continue, loop breaks and game will end
            if try_again =="n":
                break
        
        #if enemy hp is lesser than 0, player wins
        if enemy_hp <= 0:
            
            print "you win\n"
            
            #determining if the player would like to continue playing
            player_hp, enemy_hp, player_location, enemy_location, try_again = keep_playing(player_hp, enemy_hp, player_location, enemy_location, try_again)
            
            #if player doesnt want to continue, loop breaks and game will end
            if try_again =="n":
                break

    #printing the game has ended
    print "\ngame over!"

#calling a welcome function to welcome player to the game
welcome()

#calling main function executing all player and enemy functions
main(player_location, enemy_location, player_hp, enemy_hp, enemy_states, player_states, enemy_state, player_has_moved, enemy_has_moved, is_playing, try_again)

        
