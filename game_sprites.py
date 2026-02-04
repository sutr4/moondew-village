import pygame, csv

class Cursor(pygame.sprite.Sprite):
    """This class defines the sprite for the cursor."""
    def __init__(self):
        """This initializer takes no parameters, initializes the cursor's image and rect attributes,
        the hitbox of the cursor and a variable that defines whether or not the cursor is colliding with a sprite or not."""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Set the image and rect attributes for the Cursor
        self.image = pygame.image.load('sprites/Mouse sprites/Triangle Mouse icon 1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (28, 28))
        self.rect = self.image.get_rect()
        
        #Set the hitbox attributes for the Cursor
        self.hitbox = self.rect.copy()
        self.hitbox.w = 1
        self.hitbox.h = 1

        #Instance variable to keep track of whether the Cursor's hitbox is colliding with a sprite on the screen
        self.interacting = False
    
    def show(self, value):
        """This method takes a boolean variable called 'value' as a parameter and makes the cursor's
        image visible/invisible based on the value variable's value."""
        #If value is true, then the image is visible
        #If not, the image is invisible
        if value:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

    def update(self):
        """This method will be automatically called to reposition the cursor sprite and its hitbox on the
        screen to wherever the mouse is."""
        x, y = pygame.mouse.get_pos()
        self.rect.center = (x, y)
        self.hitbox.topleft = (x-6, y-6)

class Player(pygame.sprite.Sprite):
    """This class defines the sprite for the player"""
    def __init__(self, world):
        """This initializer takes the world class as a parameter. This world class is used for player collisions."""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.world = world

        #Instance variables to keep track of which action(up, down, left, right, idle) is being used to know which animation to play
        #Index is which frame of the animation is being played
        self.action = 4
        self.index = 0
        self.dx = 0
        self.dy = 0
        self.update_time = pygame.time.get_ticks()

        self.animation_list = []
        animation_types = ['up', 'down', 'left', 'right', 'idle']
        #For each animation in the animation_types list, it will create a temporary list that will hold 2 images, which are the frames
        #for the animation and then put that list into the self.animation_list list
        for animation in animation_types:
            temp_list = []
            for i in range(2):
                image = pygame.image.load(f'sprites/Player/{animation}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (32, 32))
                temp_list.append(image)
            self.animation_list.append(temp_list)
        
        #Set the image and rect attributes of the Player and the inital x and y positions of the Player
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = 150
        self.rect.centery = 150

        #Set the hitbox attributes of the Player for collisions with the world(ie. walls, water, fences, etc)
        self.hitbox = self.rect.copy()
        self.hitbox.h = 24
        self.hitbox.w = 28

        #Set the farm hitbox attribute of the Player that way only one farm tile can be selected for tilling, harvesting, planting, etc
        self.farm_hitbox = self.rect.copy()
        self.farm_hitbox.h = 1
        self.farm_hitbox.w = 1

    def __animation(self):
        """This method is called automatically in the update() method and is used to continuously change the Player's
        image attribute to play an animation."""
        ANIMATION_COOLDOWN = 375
        self.image = self.animation_list[self.action][self.index]
        #If the tick/time that we are at right now - when we first checked the time > the set animation_cooldown variable, then play the
        #next frame of the animation
        #Basically means every 375ms, change the frame of the animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #If it is at the end of the animation, go back to the beginning and replay the animation again
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def movement(self, moving_left, moving_right, moving_up, moving_down):
        """This method accepts moving_left, moving_right, moving_up, and moving_down as parameters and is used to know which 
        action animation to play."""
        #Instance variables to keep track of what action is playing, if the player is moving up, moving down, moving left, and moving right
        new_action = self.action
        self.moving_left = moving_left
        self.moving_right = moving_right
        self.moving_up = moving_up
        self.moving_down = moving_down

        #Depending of where the play is moving, it changes the new_action variable to a number respective to the action
        if self.moving_down == True:
            new_action = 1
        elif self.moving_up == True:
            new_action = 0
        elif self.moving_right == True:
            new_action = 3
        elif self.moving_left == True:
            new_action = 2
        else:
            new_action = 4
        
        #If the action that wants to be done is not the same as the action that is being done, change the action that is being done
        #to the new action and restart the animation to the new action
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        """This method will be called automatically to reposition the Player sprite on the screen."""
        #Initializes the x and y vector of the Player
        self.dx = 0
        self.dy = 0

        #Updates the hitbox and farm hitbox positions to where the player is
        self.hitbox.topright = (self.rect.x + 30, self.rect.y + 18)
        self.farm_hitbox.centerx = self.rect.centerx
        self.farm_hitbox.centery = self.rect.centery + 14

        #Plays the animation of the action the player is doing
        self.__animation()

        #Depending on where the player is moving, change the x/y vector of the Player
        if self.moving_left:
            self.dx = -1.6
        if self.moving_right:
            self.dx = 1.5
        if self.moving_up:
            self.dy = -1.6
        if self.moving_down:
            self.dy = 1.5

        #If the player is colliding with an object from the world class (ie. fence, water, walls), make it so that the player
        #cannot keep moving
        for tile in self.world.collidable_list:
            if tile[1].colliderect(self.hitbox.x + self.dx, self.hitbox.y, self.hitbox.w, self.hitbox.h):
                self.dx = 0
            if tile[1].colliderect(self.hitbox.x, self.hitbox.y + self.dy, self.hitbox.w, self.hitbox.h):
                self.dy = 0
        
        #If the player is not going outside of the screen, move it
        if ((self.rect.top > 0) and (self.dy < 0)) or \
            ((self.rect.bottom < 720) and (self.dy > 0)):  
            self.rect.centery += self.dy
        if ((self.rect.left > 0) and (self.dx < 0)) or \
            ((self.rect.right < 1280) and (self.dx > 0)):  
            self.rect.centerx += self.dx

class NPC(pygame.sprite.Sprite):
    """This class defines the sprites of the NPCs"""
    def __init__(self, type, x, y, world, state):
        """This initializer takes x and y positions, type, world class, and state as paramters. Depending on the type,
        the image of the NPC will be different. The world parameter is used to add the NPC as a collidable object into the world class
        and the state parameter is used to know what dialog will pop up when you interact with the NPC."""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Instance variable to keep track of the state, world class, and NPC type
        self.state = state
        self.world = world
        self.type = type
        #Create a list for the animations
        self.animation_list = []
        self.index = 0
        #Instance variable to keep track of whether the player and NPC are interacting
        self.interacting = False
        self.update_time = pygame.time.get_ticks()

        cat_types = ['blacknwhite', 'orange', 'grey', 'black']
        #For each cat in the cat_types list, it creates a temporary list that holds 2 images, which are the frames to the idle animation
        #of the cat. It then puts this list into the self.animation_list list
        for cat in cat_types:
            temp_list = []
            for i in range(2):
                image = pygame.image.load(f'sprites/NPC/{cat}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (32, 32))
                temp_list.append(image)
            self.animation_list.append(temp_list)
        
        #Set the image and rect attributes of the NPC
        self.image = self.animation_list[self.type][self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        #Set the interaction hitbox of the NPC so that when the player is colliding with this hitbox, the player can interact with the NPC
        self.interact_hitbox = self.rect.copy()
        self.interact_hitbox.h = 60
        self.interact_hitbox.w = 60
        self.interact_hitbox.centerx = x
        self.interact_hitbox.centery = y

        #Adds the NPC and it's rect attribute to the world class's list of collidable objects
        self.world.collidable_list.append((self.image, self.rect))

    def __animation(self):
        """This method is called automatically in the update() method and is used to continuously change the Player's
        image attribute to play an animation."""
        ANIMATION_COOLDOWN = 375
        self.image = self.animation_list[self.type][self.index]
        #If the tick/time that we are at right now - when we first checked the time > the set animation_cooldown variable, then play the
        #next frame of the animation
        #Basically means every 375ms, change the frame of the animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #If it is at the end of the animation, go back to the beginning and replay the animation again
        if self.index >= len(self.animation_list[self.type]):
            self.index = 0

    def change_interaction(self, value):
        """This method accepts a boolean value parameter and changes the self.interacting variable's value to the value parameter"""
        self.interacting = value
    
    def get_interaction(self):
        """This method returns the self.interacting variabe"""
        return self.interacting
    
    def change_state(self, state):
        """This method accepts a string state parameter and changes the NPC's state to the state parameter"""
        self.state = state
    
    def get_state(self):
        """This method returns the NPC's state"""
        return self.state
    
    def update(self):
        """This method will be called automatically and is used to update the NPC's animation"""
        self.__animation()

class Inventory(pygame.sprite.Sprite):
    """This class defines the Inventory and the inventory sprite of the player"""
    def __init__(self):
        """This initializer sets the player's inventory to be empty and have no items. It makes the starting selected slot, the first slot"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Set the image, rect, and position attributes of the Inventory
        self.image = pygame.image.load('sprites/UI/Inventory/0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 641
        self.rect.centery = 655

        #Instance variable to keep track of which slot the Player has selected
        self.selected_slot = 0

        #Lists to keep track of what items are in the inventory, their slots, and the number of items in each slot
        self.inventory_list = ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty']
        self.inventory_count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.slot_selection_img = []
        #Loads all the images of the highlighted slot in different positions and puts them into the self.slot_selection_img list
        for x in range(9):
            image = pygame.image.load(f'sprites/UI/Inventory/{x}.png').convert_alpha()
            self.slot_selection_img.append(image)

        #Call the load_inventory() method
        self.__load_inventory()

    def __load_inventory(self):
        """This method is used to load the items and their counters in the player's inventory"""
        #Create lists and sprite groups for each slot and their counter
        self.slots = pygame.sprite.Group()
        self.slots_list = []
        self.slot_counts = pygame.sprite.Group()
        self.slot_counts_list = []

        #Goes through every item in the player's inventory, each with their respective number, and calls the Slot and SlotCounter classes
        #and gives them a position, then adding those slots and their counter to their respective list and sprite group
        for x, item in enumerate(self.inventory_list):
            slot = Slot(item, 433 + x*52)
            slot_count = SlotCounter(436 + x*52, self.inventory_count_list[x])

            self.slots.add(slot)
            self.slots_list.append(slot)

            self.slot_counts.add(slot_count)
            self.slot_counts_list.append(slot_count)
    
    def change_opacity(self, change):
        """This method accepts a boolean change parameter and changes the inventory sprite, inventory items, and their counters' opacity"""
        if change:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

        for slot in self.slots_list:
            slot.change_opacity(change)
        
        for slot in self.slot_counts_list:
            slot.change_opacity(change)

    def select_slot(self, slot):
        """This method accepts a integer slot parameter and changes the Inventory's image and attribute depending on the slot parameter"""
        #Changes the image to have the correct slot selected and changes the self.selected_slot variable to the slot parameter
        self.image = self.slot_selection_img[slot]
        self.selected_slot = slot

    def get_slots(self):
        """This method returns the self.slots an self.slots_counts sprite groups"""
        return self.slots, self.slot_counts

    def change_item(self, item):
        """This method accepts an string item parameter and changes the selected slot to the item"""
        #Changes the selected slot in the inventory list to the item and changes the image of the slot to the item
        self.inventory_list[self.selected_slot] = item
        self.slots_list[self.selected_slot].change(item)

    def get_selected(self):
        """This method returns the item that the selected slot is"""
        return self.inventory_list[self.selected_slot]
    
    def get_selected_slot(self):
        """This method returns the number of the selected slot"""
        return self.selected_slot
    
    def get_selected_slot_count(self):
        """This method returns the number of items the selected slot has"""
        return self.inventory_count_list[self.selected_slot]

    def add_item(self, item, amount):
        """This method accepts an item and amount parameter. It adds the item parameter into the player's inventory and
        adds an amount of the amount variable"""
        #If this item already exists in the player's inventory
        if item in self.inventory_list:
            #Go through each slot in the player's inventory, each slot getting it's respective number
            for x, slot in enumerate(self.inventory_list):
                #Instance variable that represents the slot's count
                slot_stack_count = int(self.inventory_count_list[x])
                #If the slot and the item you are adding are equal and the slot's stack is less than 9 (the maximum amount an item can stack)
                if (item == slot) and (slot_stack_count < 9):
                    #If the amount you want to add to the stack + the stack's count is <= 9, add {amount} to the slot's stack
                    if (amount + slot_stack_count) <= 9:
                        self.slot_counts_list[x].add_count(amount)
                        self.inventory_count_list[x] += amount
                    #If the amount you want to add to the stack + the stack's count is > 9, make the stack's count to 9 and create a new variable
                    #that's (the stack's count + the amout you want to add - 9) to know how much should be left
                    #in the new stack and then recall the method with the new amount and end the for loop
                    elif (amount + slot_stack_count) >= 9:
                        new_amount = slot_stack_count + amount - 9
                        self.slot_counts_list[x].change_count(9)
                        self.add_item(item, new_amount)
                    break
                #If the slot and the item you are adding match and the slot's count is max, continue the for loop
                elif (item == slot) and (slot_stack_count == 9):
                    continue
                #If you are at the end of inventory and the slot is empty
                if x == 8 and slot == 'empty':
                    #Go through each slot in the player's inventory, each slot getting it's respective number
                    for y, slot1 in enumerate(self.inventory_list):
                        #If the slot is empty, change that slot in the inventory_list and slots_list to the item, and add the amount that you
                        #are adding to that slot's slot_count_list and inventory_count_list and end the loop
                        if slot1 == "empty":
                            self.inventory_list[y] = item
                            self.slots_list[y].change(item)
                            self.slot_counts_list[y].add_count(amount)
                            self.inventory_count_list[y] += amount
                            break
                    break
        #If the item is not in the player's inventory
        else:
            #Go through each slot in the player's inventory, each slot getting it's respective number
            for x, slot in enumerate(self.inventory_list):
                #If the slot is empty, change that slot in the inventory_list and slots_list to the item, and add the amount that you
                #are adding to that slot's slot_count_list and inventory_count_list and end the loop
                if slot == "empty":
                    self.inventory_list[x] = item
                    self.slots_list[x].change(item)
                    self.slot_counts_list[x].add_count(amount)
                    self.inventory_count_list[x] += amount
                    break

    def remove_item(self, amount, x):
        """This method accepts integer amount and integer x parameters. It is used to remove {amount} amount of items in the {x} slot"""
        #Instance variables to keep track of the stack's count
        stack_count = self.inventory_count_list[x] - amount
        #Remove {amount} from the inventory's count list and the slot's count list
        self.slot_counts_list[x].add_count(-amount)
        self.inventory_count_list[x] -= amount
        
        #If the stack count is 0, change the item in the inventory's list to empty, change the count in the inventory's list to 0,
        #and change the image from the slot to 'empty'(blank)
        if stack_count == 0:
            self.inventory_list[x] = 'empty'
            self.inventory_count_list[x] = 0
            self.slots_list[x].change('empty')

    def use(self, item_or_slot, amount, is_slot):
        """This method accepts item_or_slot, integer amount, and boolean is_slot parameters. It is used to use/remove an item from the
        player's inventory"""
        #If item_or_slot is a number(that represents the slot's number), call the remove_item() method with the amount parameter and 
        #item_or_slot parameter.
        if is_slot:
            self.remove_item(amount, item_or_slot)
        #If item_or_slot is a string(that represents the item's name), go through each slot in the inventory's list, each slot getting
        #it's respective number until the slot and the item match, then call the remove_item() method with the amount parameter and the
        #slot's number
        else:
            for x, slot in enumerate(self.inventory_list):
                if item_or_slot == slot:
                    self.remove_item(amount, x)
                    break
    
    def get_inventory(self):
        """This method returns the inventory list"""
        return self.inventory_list

class Slot(pygame.sprite.Sprite):
    """This class defines the slot sprites of the inventory."""
    def __init__(self, item, x):
        """This initializer takes string item and x position parameter. It uses item to determine what image to show and 
        x position to know the position of the slot"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set the image and rect attributes of the slot
        self.image = pygame.image.load(f'sprites/UI/Items/{item}.png').convert_alpha()
        self.rect = self.image.get_rect()
        #Set the position of the slot's rect
        self.rect.centerx = x
        self.rect.centery = 653

    def change_opacity(self, change):
        """This method accepts a boolean change as a parameter, and is used to change the opacity of the slot."""
        #If change is true, set the image's opacity to 100
        #Otherwise, set the image's opacity to 255
        if change:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

    def change(self, item):
        """This method accepts a string item, and is used to change the image of the slot."""
        #Set the image attribute of the slot
        self.image = pygame.image.load(f'sprites/UI/Items/{item}.png').convert_alpha()

class SlotCounter(pygame.sprite.Sprite):
    """This class defines the slot counter sprites of the inventory"""
    def __init__(self, x, count):
        """This initializer accepts x position, and integer count. It uses the x position to know the position
        of the slot and count parameter to know which image to show"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Instance variable that keeps track of the item's count
        self.count = count

        self.image_list = []
        #Loads all the images (counts from 1 to 9)
        for i in range(10):
            image = pygame.image.load(f'sprites/UI/Item Count/{i}.png').convert_alpha()
            self.image_list.append(image)
        
        #Set the image and rect attributes of the slot counter
        self.image = self.image_list[self.count]
        self.rect = self.image.get_rect()
        #Set the positions of the slot's rect
        self.rect.centerx = x
        self.rect.centery = 660

    def change_opacity(self, change):
        """This method accepts boolean change as a parameter, and is used to change the opacity of the slot counter"""
        #If the change parameter is true, set the slot counter's opacity to 100
        #Otherwise, set the slot counter's opacity to 255
        if change:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

    def add_count(self, amount):
        """This method accepts integer amount as a parameter, and is used to add {amount} to the slot's count"""
        self.count += amount
        #Makes it so that the count cannot be less than 0 or greater than 9
        if self.count < 0:
            self.count = 0
        if self.count > 9:
            self.count = 9
        #Set the image attribute of the slot counter to the correct number
        self.image = self.image_list[self.count]

    def change_count(self, amount):
        """This method accpets integer amount as a paramter, and is used to change the slot's count to {amount}"""
        self.count = amount
        #Set the image attribute of the slot counter to the correct number
        self.image = self.image_list[self.count]

    def get_count(self):
        """This methos returns the slot's count"""
        return self.count

class World():
    """This class defines the collidable objects in the game's world"""
    def __init__(self, screen):
        """This initializer takes a screen surface as a parameter, and draws the collidable objects and puts them in a list"""
        #Instance variables that keep track of the screen surface, the amount of rows and columns on the screen, and the
        #number of different tile types
        self.screen = screen
        self.rows = 23
        self.col = 40
        self.tile_types = 29

        self.map = []
        #Create a list of 23by40 -1s
        for row in range(self.rows):
            r = [-1] * self.col
            self.map.append(r)
        #Load in the level's tiles and create the world
        with open('sprites/Background/world.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.map[x][y] = int(tile)
        
        self.collidable_list = []

        #Load in all the different tile images, scaling them all to 32x32, and putting them in the self.tile_list list
        self.tile_list = []
        for x in range(self.tile_types):
            img = pygame.image.load(f'sprites/Land Sprites/{x}.png').convert()
            img = pygame.transform.scale(img, (32, 32))
            self.tile_list.append(img)

        #Calls the load_map() method
        self.load_map()

    def load_map(self):
        """This method is used to load all the tiles in the self.map list and their rects, and put them into the collidable_list list"""
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x*32
                    img_rect.y = y*32
                    tile_data = (img, img_rect)
                    self.collidable_list.append(tile_data)

    def draw(self):
        """This methos is used to draw all the tiles onto the screen"""
        for tile in self.collidable_list:
            self.screen.blit(tile[0], tile[1])

class Roof(pygame.sprite.Sprite):
    """This class defines the sprites of the house roofs"""
    def __init__(self, type, x, y):
        """This initializer takes a string type and x and y positions as parameters. The type determines what the size
        of the roof will be and the x and y parameters determine the position of the roof"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set the image and rect attributes of the roof
        self.image = pygame.image.load(f'sprites/Land Sprites/roof/{type}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y
    
    def change_opacity(self, change):
        """This method accepts a boolean change as a parameter, and is used to change the opacity of the roof. This method
        gets called when the user collides with the roof and is inside a house"""
        #If the boolean change is true, set the roof's opacity to 50
        #Otherwise if change is false, set the roof's opacity to 255
        if change:
            self.image.set_alpha(50)
        else:
            self.image.set_alpha(255)

class Farmable_Tile(pygame.sprite.Sprite):
    """This class defines the sprites for the farmable tiles"""
    def __init__(self, x, y):
        """This initializer takes an x and y position as parameters and are used to position the tile. It loads all the different
        plant states and dirt tile states"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        #Instance variables that represent the untilled and tilled dirt images
        self.untilled_dirt = pygame.image.load('sprites/Land Sprites/Farming/untilled.png').convert()
        self.tilled_dirt = pygame.image.load('sprites/Land Sprites/Farming/tilled.png').convert()
        
        self.wheat_states = []
        #Loads the 4 different wheat state images and puts them into the self.wheat_states list
        for w in range(4):
            image = pygame.image.load(f'sprites/Land Sprites/Farming/wheat/{w}.png').convert()
            self.wheat_states.append(image)
        
        self.plum_states = []
        #Loads the 4 different plum state images and puts them into the self.plum_states list
        for p in range(4):
            image = pygame.image.load(f'sprites/Land Sprites/Farming/plum/{p}.png').convert()
            self.plum_states.append(image)

        #Instance variables that keep track of the plant's state, the tile's type, and if the tile is watered
        self.plant_state = 0
        self.type = "untiled"
        self.watered = False

        #Set the image and rect attributes of the dirt tile
        self.image = self.untilled_dirt
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    
        #Instance variable that keeps track of if the tile is highlighted
        self.highlighting = False

    def untill(self):
        """This method is used to change the tile's image to untilled"""
        #Set the image attribute to untilled, changes the type to untilled, and set the plant state to 0
        self.image = self.untilled_dirt
        self.type ='untilled'
        self.plant_state = 0

    def till(self):
        """This method is used to change the tile's image to tilled"""
        #Set the image attribute to tilled, change the type to tilled, and set the plant state to 0
        self.image = self.tilled_dirt
        self.type = 'tilled'
        self.plant_state = 0

    def plant_wheat(self):
        """This method is used to change the tile's image to wheat"""
        #Only change the tile's image to wheat if the tile is tilled and return true if the wheat gets planted
        #Otherwise, return false
        if self.type == 'tilled':
            self.image = self.wheat_states[self.plant_state]
            self.type = "wheat"
        
            return True
        else:
            return False
    
    def plant_plum(self):
        """This method is used to change the tile's image to plum"""
        #Only change the tile's image to wheat if the tile is tilled and return true if the plum gets planted
        #Otherwise, return false
        if self.type == 'tilled':
            self.image = self.plum_states[self.plant_state]
            self.type = "plum"
        
            return True
        else:
            return False

    def grow(self):
        """This method is used to change the tile's image to the next stage of the plant"""
        #Only change the tile's image and add 1 to the plant_state variable if the tile has been watered
        if self.watered:
            self.plant_state += 1
            #Makes it so that the plant's state cannot be greater than 3
            if self.plant_state >= 3:
                self.plant_state = 3
            #If the plant's state is <= 3 then change the image to the plant's state and make it so that the plant is no longer watered
            if self.plant_state <= 3:
                if self.type == 'plum':
                    self.image = self.plum_states[self.plant_state]
                if self.type == 'wheat':
                    self.image = self.wheat_states[self.plant_state]
            self.watered = False
    
    def water(self, watering):
        """This method accepts a boolean watering as a parameter, and is used to change the
        self.watered variable to {watering}"""
        self.watered = watering

    def get_type(self):
        """This method returns the tile's type (ie. tilled, untilled, wheat, plum)"""
        return self.type

    def get_state(self):
        """This method returns the tile's plant state"""
        return self.plant_state

class Tile_Outline(pygame.sprite.Sprite):
    """This class defines the farmable tile's outline sprite"""
    def __init__(self, x, y):
        """This initializer takes x and y positions as parameters and are used to position the outline."""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Set the image and rect attributes of the outline
        self.image = pygame.image.load('sprites/Land Sprites/Farming/outline.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        #Instance variable that keeps track of whether or not the tile is being highlighted
        self.highlighting = False

    def highlight(self, highlighting):
        """This method accepts a boolean highlighting as a parameter, and is used to change the opacity of the outline"""
        #If the boolean highlighting is true, set the outline's opacity to 255
        #Otherwise, set the opacity to 0
        self.highlighting = highlighting
        if highlighting:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
    
    def get_highlight(self):
        """This method returns whether or not the tile is being highlighted"""
        return self.highlighting

class Dialog(pygame.sprite.Sprite):
    """This class defines the dialog box sprite"""
    def __init__(self, screen):
        """This initializer accepts a surface screen, initializes the different dialog boxes depending on the cat, and their emotion"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Instance variable that keeps track of the screen surface and current tick
        self.screen = screen
        self.update_time = pygame.time.get_ticks()

        #Sets initial cat_type, emotion, and index values
        self.cat_types = ['blacknwhite', 'orange', 'grey', 'black']
        self.cat_type = 3
        self.emotion = 0
        self.index = 0
        
        #Calls the load_images() method to load all the different dialog box images and set the image and rect attributes
        self.load_images()        
        self.image = self.emotes[self.emotion][self.cat_type][self.index]
        self.rect = self.image.get_rect()

        self.rect.centerx = 640
        self.rect.centery = 604

        #Set initial alpha value to 0 and instance variable that keeps track of whether the dialog box is displaying or not
        self.image.set_alpha(0)
        self.displaying = False

        #Initializes the font, color, text, and dialog
        self.font = pygame.font.Font('sprites/fonts/rainyhearts.ttf', 20)
        self.BROWN = (182, 137, 98)
        self.text = ""
        self.dialog = self.font.render(self.text, 1, self.BROWN)

        #Instance variables that keep track of the stage of dialog that it is at and if the dialog box is done showing all the dialogue
        self.done = False
        self.state = -1

        #Initializes and calls the Heart class for each NPC's hearts
        self.orange_hearts = Hearts(5)
        self.bnw_hearts = Hearts(3)
        self.grey_hearts = Hearts(3)
        self.black_hearts = Hearts(6)

        self.hearts = [self.bnw_hearts, self.orange_hearts, self.grey_hearts, self.black_hearts]

    def load_images(self):
        """This method is used to load all the different dialog box images"""
        self.emotions = ['default', 'angry', 'loving', 'wow', 'excited', 'sleepy']
        self.emotes = []
        #Goes through each feeling for each cat and puts all of the animations for one feeling into a list, then putting that list into a list
        #with all the feelings for that cat, and then puts the list of cats and their feelings into another list called emotes
        #ie. emotes = [black_cat, orange_cat] , black_cat -> [mad, angry, sad], mad -> [frame1, frame2] 
        for feeling in self.emotions:
            temp_list1 = []
            for cat in self.cat_types:
                temp_list = []
                for y in range(2):
                    image = pygame.image.load(f'sprites/UI/Dialog/{cat}/{feeling}/{y}.png').convert_alpha()
                    temp_list.append(image)
                temp_list1.append(temp_list)
            self.emotes.append(temp_list1)

    def animation(self):
        """This method is called automatically in the update() method and is used to continuously change the Player's
        image attribute to play an animation."""
        ANIMATION_COOLDOWN = 500
        self.image = self.emotes[self.emotion][self.cat_type][self.index]
        #Every 500ms, change the frame of the animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #If it has reached the end of the animation, restart from the beginning
        if self.index >= 2:
            self.index = 0
    
    def show(self, change):
        """This method accepts a boolean change as a parameter, and is used to change the opacity of the dialog box and the NPC's hearts"""
        #If the boolean change is true, set the dialog box's opacity to 255, set the displaying boolean to true, and make the 
        #NPC's hearts visible
        #Otherwhise, set the dialog box's opacity to 0, set the displaying boolean to false, make the NPC's hearts invisible, 
        #and reset the state to -1
        if change:
            self.image.set_alpha(255)
            self.displaying = True
            self.hearts[self.cat_type].display(True)
        else:
            self.image.set_alpha(0)
            self.displaying = False
            self.state = -1
            self.hearts[self.cat_type].display(False)

    def display(self, emotion, text, text2, cat_type, done):
        """This method accepts a integer emotion, string text, string text2, integer cat_type, and boolean done as parameters, 
        and use those parameters to determine which dialog box image gets displayed and the text that gets displayed"""
        self.done = done
        self.cat_type = cat_type
        self.emotion = emotion
        self.text = text
        self.text2 = text2
        self.state += 1
        #Calls the show() method and sets it to true
        self.show(True)

    def get_display(self):
        """This method returns a boolean of whether or not the dialog box is being displayed"""
        return self.displaying
    
    def get_done_talking(self):
        """This method returns a boolean of whether or not the dialog box is done displaying dialogue"""
        return self.done

    def get_state(self):
        """This method returns an integer that represents what dialogue stage it is in"""
        return self.state

    def get_hearts(self):
        """This method returns the heart classes of the NPCs"""
        return self.bnw_hearts, self.orange_hearts, self.grey_hearts, self.black_hearts
    
    def update(self):
        """This method will be automatically called and if the displaying boolean is true, it will call the load_images() method,
        the animation() method and render and blit the text"""
        if self.displaying:
            self.load_images()
            self.animation()
            self.dialog = self.font.render(self.text, 1, self.BROWN)
            self.dialog2 = self.font.render(self.text2, 1, self.BROWN)
            self.image.blit(self.dialog, (130, 45))
            self.image.blit(self.dialog2, (130, 65))
    
class Dialogue():
    """This class defines all the different dialogues for the NPCs"""
    def __init__(self):
        """This initializer initializes all the different dialogue stated"""
        self.state_list = ['tutorial', 'wedding_ani', 'oreo_mad', 'mute', 'comfort_oreo', 'waiting oreo response']

        #Calls all the different dialogue methods
        self.tutorial_dialog()
        self.wedding_ani_dialog()
        self.angry_oreo_dialog()
        self.oreo_chessur_pt1()
        self.comforting_oreo_dialog()
        self.waiting_oreo_response()

        self.states = [self.tut_dialog, self.wed_ani_dialog, self.oreo_mad_dialog, self.oreoxchessur_pt1_dialog, self.comfort_dialog, self.waiting_for_oreo_dialog]

    def tutorial_dialog(self):
        """This method is used to define the tutorial dialogue and returns the amount of dialog boxes that will show up"""
        self.tut_dialog = [
                                [0, "Here, you will live the farmer life!", "", 3, False],
                                [0, "You can use the farm to your right as", "your farm", 3, False],
                                [3, "...It hasn't been used in a while...", "", 3, False],
                                [4, "But you can fix it up right?", "", 3, False],
                                [0, "If you cross a couple bridges, you'll", "find Mei!", 3, False],
                                [0, "She sells and buys everything around", "here!", 3, False],
                                [2, "She's so cool!", "", 3, False],
                                [2, "Anyways haha.. My name is Moon! And","you'll probably find Oreo around!", 3, False],
                                [0, "Probably not Chessur though.. she's","always holed up in her house..", 3, False],
                                [0, "Anywho! Here are some items to get","you started for your new journey!", 3, False],
                                [0, "", "", 3, True]
                               ]

        return len(self.tut_dialog)
    
    def wedding_ani_dialog(self):
        """This method is used to define the wedding aniversary wheat delivery dialogue and returns the amount of dialog boxes that will show up"""
        self.wed_ani_dialog = [
                                [5, "Do me a favour would'ya?", "", 2, False],
                                [5, "I've been up all night trying to come up","with the perfect receipe..", 2, False],
                                [5, "It's Mei and Moon's wedding","anniversary tomorrow...", 2, False],
                                [5, "And Moon hired me to bake their cake. I","can't ruin their special day.", 2, False],
                                [5, "Please bring me 5 wheat by tonight.", "", 2, False],
                                [0, "", "", 2, True]
                              ]

        return len(self.wed_ani_dialog)

    def angry_oreo_dialog(self):
        """This method is used to define part 1 of the friendship reconciliation dialogue and returns the amount of dialog boxes that will show up"""
        self.oreo_mad_dialog = [
                                [3, "Oh. Sorry. Did you hear that?", "", 0, False],
                                [1, "I've been wanting to go to this festival", "for 2 weeks.", 0, False],
                                [1, "And Chessur said she would come with", "me as my plus 1", 0, False],
                                [1, "But then all of a sudden, on the day of", "the festival.", 0, False],
                                [1, "She said she won't come!", "", 0, False],
                                [1, "And now I can't go because you can't go", "without a pair.", 0, False],
                                [0, "", "", 0, True]
        ]

        return len(self.oreo_mad_dialog)
    
    def comforting_oreo_dialog(self):
        """This method is used to define part 2 of the friendship reconciliation dialogue and returns the amount of dialog boxes that will show up"""
        self.comfort_dialog = [
                                    [3, "Please take this and buy her milk. It's", "her favourite. And tell her I'm sorry...", 2, False],
                                    [0, "", "", 2, True]
                                    ]
        
        return len(self.comfort_dialog)
    
    def oreo_chessur_pt1(self):
        """This method is used to define part 3 of the friendship reconciliation dialogue and returns the amount of dialog boxes that will show up"""
        self.oreoxchessur_pt1_dialog = [
                                    [3, "Chessur wanted you to give me this?", "Really?", 0, False],
                                    [3, "And she said she was really sorry?", "", 0, False],
                                    [3, "She knows I can't resist milk.. Fine!", "Tell her I forgive her this time.", 0, False],
                                    [0, "", "", 0, True]
        ]

        return len(self.oreoxchessur_pt1_dialog)
    
    def waiting_oreo_response(self):
        """This method is used to define part 4 of the friendship reconciliation dialogue and returns the amount of dialog boxes that will show up"""
        self.waiting_for_oreo_dialog = [
                                        [4, "Really??? Thank you so much! Please take this", "take this and buy whatever you want!!", 2, False],
                                        [0, "", "", 2, True]
                                        ]

    def get_states(self):
        """This method returns all the different dialog states that there are"""
        return self.states

    def get_state_num(self, state):
        """This method accepts a string state as a parameter and returns what state number it is"""
        return self.state_list.index(state)

class Shop(pygame.sprite.Sprite):
    """This class defines the sprite for the Shop"""
    def __init__(self):
        """This initializer initializes the image and rect attributes"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Set the image and rect attributes of the Shop
        self.image = pygame.image.load('sprites/UI/Shop/shop.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.image.set_alpha(0)

        #Instance variable that keeps track of whether or not the shop is being displayed
        self.displaying = False

    def show(self, value):
        """This method accepts a boolean value as a parameter and changes the image's opacity based on it"""
        #If value is true, set the image's opacity to 255 and change the displaying variable to true
        #Otherwise, set the image's opacity to 0 and change the displaying variable to false
        if value:
            self.displaying = True
            self.image.set_alpha(255)
        else:
            self.displaying = False
            self.image.set_alpha(0)
    
    def get_display(self):
        """This method returns a boolean based on if the shop is being displayed or not"""
        return self.displaying

class ShopButton(pygame.sprite.Sprite):
    """This class defines the button sprites for the Shop"""
    def __init__(self, image_num, x, y):
        """This initialize accepts integer image_num, and x and y positions as parameters. It uses image_num to know which button it
        is and x and y parameters to position the buttons"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Instance variable to keep track of the integer image_num
        self.image_num = image_num
        #Lists that determine what the image is displaying and it's price
        self.items = ['wheat', 'wheat', 'wheat_seeds', 'wheat_seeds', 'plum', 'plum', 'plum_seeds',
                      'plum_seeds', 'milk', 'milk', 'egg', 'egg', 'apple', 'apple']
        self.price = [8, 6, 3, 1, 18, 10, 5, 3, 50, 26, 7, 4, 23, 12]

        #If image_num is a positive number, it is a sell button
        #Otherwise if it is an odd number, it is a buy button
        if (self.image_num + 1) % 2 == 0:
            self.type = 'sell'
        else:
            self.type = 'buy'

        #Load all the different button images
        self.images = []
        for g in range(14):
            image = pygame.image.load(f'sprites/UI/Shop/buttons/{g}.png').convert()
            self.images.append(image)
        
        #Set the image and rect attributes of the button
        self.image = self.images[image_num]
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        self.image.set_alpha(0)

        #Instance variables that keep track of whether or not the button is being displayed and whether or not the
        #cursor is hovering over the button
        self.displaying = False
        self.interacting = False

    def change_interaction(self, value):
        """This method accepts a boolean value as a parameter and is used to change the self.interacting variable"""
        #If the boolean value is true, the self.interacting variable is true
        #Otherwise, self.interacting is false
        if value:
            self.interacting = True
        else:
            self.interacting = False
    
    def get_interaction(self):
        """This method returns a boolean that represents whether or not the cursor is hovering over the button"""
        return self.interacting
    
    def show(self, value):
        """This method accepts boolean value as a parameter and is used to change the opacity of the image"""
        #If boolean value is true, set the image's alpha to 255 and set the displaying variable to true
        #Otherwise, set the image's alpha to 0 and the displaying variable to false
        if value:
            self.displaying = True
            self.image.set_alpha(255)
        else:
            self.displaying = False
            self.image.set_alpha(0)

    def get_display(self):
        """This method returns a boolean that represents whether or not the button is being displayed"""
        return self.displaying
    
    def get_button(self):
        """This method returns all the button's attributes. It's type (buy/sell), the item that it is, and the price"""
        return self.type, self.items[self.image_num], self.price[self.image_num]
    
class User_Info(pygame.sprite.Sprite):
    """This class defines the user's information as a sprite"""
    def __init__(self):
        """The intializer initializes the image and rect attributes and holds user information like the day number and coin they have"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Get the ticks
        self.update_time = pygame.time.get_ticks()

        #Calls the Night class to be able to change the time
        self.night = Night()

        #Set the image and rect attributes of the User Info
        self.image = pygame.image.load('sprites/UI/user info.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 84
        self.rect.centery = 120

        #Instance variables that keep track of the amount of coins the user has and what day it is
        self.coins = 25
        self.day = 1    

        #Instance variables that intialize the font and color of the text that will display the coins and day
        self.font = pygame.font.Font('sprites/fonts/sproutLands font.ttf', 8)
        self.BROWN = (182, 137, 98)

        #Instance variables that keep track of whether the user is in the shop menu, and whether or not the image is translucent
        self.in_shop = False
        self.translucent = False

    def shop_view(self, viewing):
        """This method accepts boolean viewing as a parameter is and used to determine whether or not the user is viewing the shop"""
        #If viewing is true, set the self.in_shop variable to true
        #Otherwise, set the variable to fasle
        if viewing:
            self.in_shop = True
        else:
            self.in_shop = False

    def change_opacity(self, change):
        """This method accepts boolean change as a parameter and changes the variable self.translucent to {change}"""
        self.translucent = change
    
    def new_day(self):
        """This method is used to change the day"""
        #Updates the ticks to the current time, makes it not night time anymore and adds 1 to the day counter
        self.update_time = pygame.time.get_ticks()
        self.night.night(False)
        self.day += 1
    
    def change_coins(self, amount):
        """This method accepts integer amount as a parameter and adds {amount} to the coin count"""
        self.coins += amount

    def get_coins(self):
        """This method returns the amount of coins the user has"""
        return self.coins

    def get_day(self):
        """This method returns the day number that it is"""
        return self.day

    def get_night(self):
        """This method returns a boolean that represents if it is night or not"""
        return self.night
    
    def change_time(self):
        """This method is used to change the time to day/night"""
        TIME_SHIFT = 60000
        #Every minute, it goes from night -> day or day -> night
        if pygame.time.get_ticks() - self.update_time > TIME_SHIFT:
            if self.night.get_night():
                self.new_day()
            else:
                self.update_time = pygame.time.get_ticks()
                self.night.night(True)

    def update(self):
        """This method is called automatically and it changes the time of day, updates the transparency of the UI, and updates
        the coin and day counter text"""
        #Calls the change_time() method
        self.change_time()

        #Set the image attribute of the User Info sprite
        self.image = pygame.image.load('sprites/UI/user info.png').convert_alpha()
        #If boolean self.translucent is true, make the image translucent
        #Otherwise, make the image opaque
        if self.translucent:
            self.image.set_alpha(155)
        else:
            self.image.set_alpha(255)

        #Instance variables that represent the day and coin counter in strings and render them
        self.coin_string = str(self.coins)
        self.day_string = "Day " + str(self.day)
        self.coin_text = self.font.render(self.coin_string, 1, self.BROWN)
        self.day_text = self.font.render(self.day_string, 1, self.BROWN)
        
        #If the user is viewing the shop, move the user info sprite to the left of the shop
        #Otherwise, move the user info sprite to the top left of the screen
        if self.in_shop:
            self.rect.centerx = 440
            self.rect.centery = 291
        else:
            self.rect.centerx = 84
            self.rect.centery = 120

        self.image.blit(self.coin_text, (68, 167))
        self.image.blit(self.day_text, (52, 207))

class Night(pygame.sprite.Sprite):
    """This class defines the sprite of the Night time overlay"""
    def __init__(self):
        """This initializer initializes the image and rect attributes"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Set the image and rect attributes of the night time overlay
        self.image = pygame.Surface((1280, 720))
        self.image = self.image.convert_alpha()
        
        self.image.fill((38, 30, 87))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()

        #Instance variable that keeps track of whether or not it is night time
        self.night_time = False
    
    def night(self, night_time):
        """This method accepts boolean night_time and changes the opacity of the image depending on it"""
        #If boolean night_time is true, set the opacity alpha to 150
        #Otherwise, set the opacity alpha to 0
        self.night_time = night_time
        if self.night_time:
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(0)

    def get_night(self):
        """This method returns a boolean that represents whether or not it is night time"""
        return self.night_time

class Bed(pygame.sprite.Sprite):
    """This class defines the sprite of the player's bed"""
    def __init__(self):
        """This initializer initializes the image and rect and hitbox attributes"""
        #Call parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #Set the image and erct and hitbox attributes of the player's bed
        self.image = pygame.image.load('sprites/Land Sprites/bed.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = 112
        self.rect.centery = 128

        #If the player is colliding with this hitbox, the player can interact with the bed
        self.hitbox = self.rect.copy()
        self.hitbox.h = 60
        self.hitbox.w = 60
        self.hitbox.centerx = 112
        self.hitbox.centery = 128

        #Instance variable that determines whether or not the player is colliding with the bed's hitbox
        self.interacting = False

    def is_interacting(self, value):
        """This method accepts boolean value as a parameter and changes self.interacting based on it"""
        #If boolean value is true, self.interacting is true
        #Otherwise, self.interacting is false
        if value:
            self.interacting = True
        else:
            self.interacting = False
    
    def get_interaction(self):
        """This method returns a boolean that represents whether or not the player is colliding with the bed's hitbox"""
        return self.interacting

class Zombie(pygame.sprite.Sprite):
    """This class defines the sprite for the Zombie"""
    def __init__(self):
        """This initializes initializes the image and rect attributes of the zombie and creates the animation list of the zombie"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Instance variables that keep track of what action the zombie is performing, the index of the animation, and sets initial variables
        #for the zombie's x and y vectors.
        self.action = 0
        self.index = 0
        self.dx = 0
        self.dy = 0
        self.update_time = pygame.time.get_ticks()

        self.animation_list = []
        animation_types = ['up', 'down', 'left', 'right']
        #Goes through each animation time and gives them each a list with the frames of the action's animation
        for animation in animation_types:
            temp_list = []
            for i in range(2):
                image = pygame.image.load(f'sprites/NPC/zombie/{animation}/{i}.png').convert_alpha()
                temp_list.append(image)
            self.animation_list.append(temp_list)
        
        #Instance variable that determines what movement stage the zombie is at
        self.movement_stage = 1

        #Set the image, rect, interact hitbox, and hitbox attributes of the zombie
        self.image = self.animation_list[self.action][self.index]
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()

        #If the zombie's hitbox collides with the farmable tile, it untilled the tile
        self.hitbox = self.rect.copy()
        self.hitbox.h = 24
        self.hitbox.w = 28

        #If the player's hitbox collides with the interact hitbox, the player can interact with the zombie
        self.interact_hitbox = self.rect.copy()
        self.interact_hitbox.h = 60
        self.interact_hitbox.w = 60

        #Instance variables that keep track of whether or not the zombie is cured, alive, or being interacting with
        self.cured = False
        self.is_alive = False
        self.interacting = False

    def animation(self):
        """This method is called automatically by the update() method and is used to change the sprite's image continuously to create
        an animation"""
        ANIMATION_COOLDOWN = 375
        self.image = self.animation_list[self.action][self.index]
        #Every 375ms, change the frame of the animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #If the animation is done being played, replay it
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def movement(self, moving_left, moving_right, moving_up, moving_down):
        """This method accept moving_left boolean, moving_right boolean, moving_up boolean, and moving_down booelan as parameters and are
        used to know which action animation to play"""
        #Instance variables to keep track of what action is playing, and if the zombie is moving up, down, left, or right
        new_action = self.action
        self.moving_left = moving_left
        self.moving_right = moving_right
        self.moving_up = moving_up
        self.moving_down = moving_down
        
        ##Depending of where the zombie is moving, it changes the new_action variable to a number respective to the action
        if self.moving_down == True:
            new_action = 1
        elif self.moving_up == True:
            new_action = 0
        elif self.moving_right == True:
            new_action = 3
        elif self.moving_left == True:
            new_action = 2
        else:
            new_action = 4
        
        #If the action that wants to be played is not the same as the action that is currently being playe, change the action to the new one
        #and update the animation to the new one
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def change_alive(self, value):
        """This method accepts boolean value as a parameter and depending on the value, it changes the sprites image and rect attributes,
        and other variable values"""
        #If value is true and the zombie is not cured, make the image visible, the alive variable to true, reposition the zombie to its 
        #staring position, set the cured value to false, and reset the movement stage to 1
        #Otherwise, make the image invisible and the alive variable to false
        if value and not self.cured:
            self.image.set_alpha(255)
            self.is_alive = True
            self.rect.centerx = 176
            self.rect.centery = 680
            self.movement_stage = 1
            self.cured = False
        else:
            self.image.set_alpha(0)
            self.is_alive = False
    
    def cure(self):
        """This method is used to change the cured variable to true and make the zombie no longer alive"""
        self.cured = True
        self.change_alive(False)

    def change_interaction(self, value):
        """This method accepts boolean value as a parameter and changes the self.interacting variable based on it"""
        if value:
            self.interacting = True
        else:
            self.interacting = False
    
    def get_interaction(self):
        """This method returns a boolean that represents whether or not the player is interacting with the zombie"""
        return self.interacting
    
    def get_cure(self):
        """This method returns a boolean that represents whether or not the zombie is cured"""
        return self.cured

    def get_alive(self):
        """This method returns a boolean that represents whether or not the zombie is alive"""
        return self.is_alive

    def update(self):
        """This method is called automatically and is used to reposition the zombie sprite on the screen"""
        #If the zombie is alive
        if self.is_alive:
            
            self.dx = 0
            self.dy = 0
            
            #Reposition the zombie's hitbox and interact hitbox to where the zombie is
            self.hitbox.topright = (self.rect.x + 30, self.rect.y + 18)
            self.interact_hitbox.centerx = self.rect.centerx
            self.interact_hitbox.centery = self.rect.centery

            if self.movement_stage == 1:
                self.movement(False, False, True, False)
                if self.rect.centery <= 260:
                    self.movement_stage = 2

            elif self.movement_stage == 2:
                self.movement(False, True, False, False)
                if self.rect.centerx >= 300:
                    self.movement_stage = 3

            elif self.movement_stage == 3:
                self.movement(False, False, True, False)
                if self.rect.centery <= 210:
                    self.movement_stage = 4
            
            elif self.movement_stage == 4:
                self.movement(False, True, False, False)
                if self.rect.centerx >= 600:
                    self.movement_stage = 5
            
            elif self.movement_stage == 5:
                self.movement(False, False, True, False)
                if self.rect.centery <= 170:
                    self.movement_stage = 6
            
            elif self.movement_stage == 6:
                self.movement(True, False, False, False)
                if self.rect.centerx <= 400:
                    self.movement_stage = 7

            elif self.movement_stage == 7:
                self.movement(False, False, True, False)
                if self.rect.centery <= 140:
                    self.movement_stage = 8
            
            elif self.movement_stage == 8:
                self.movement(False, True, False, False)
                if self.rect.centerx >= 600:
                    self.movement_stage = 9
            
            elif self.movement_stage == 9:
                self.movement(True, False, False, False)
                if self.rect.centerx <= 424:
                    self.movement_stage = 10
            
            elif self.movement_stage == 10:
                self.movement(False, False, False, True)
                if self.rect.centery >= 200:
                    self.movement_stage = 4

            #Plays the zombie's movement animation
            self.animation()
            
            if self.moving_left:
                self.dx = -0.6
            if self.moving_right:
                self.dx = 0.6
            if self.moving_up:
                self.dy = -0.6
            if self.moving_down:
                self.dy = 0.6

            self.rect.centery += self.dy
            self.rect.centerx += self.dx

class Hearts(pygame.sprite.Sprite):
    """This class defines the heart sprites for the NPCs"""
    def __init__(self, heart):
        """This initializer accepts integer heart as a parameter that represents the amount of hearts the NPC has for the player, 
        and initializes the image and rect attributes of the sprite"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load all the heart images
        self.hearts = []
        for x in range(1, 11):
            image = pygame.image.load(f'sprites/UI/Dialog/Hearts/{x}.png')
            self.hearts.append(image)

        #Instance variable that keeps tracks of how many hearts the NPC has for the player
        self.heart = heart
        #Set the image and rect attributes for the sprite
        self.image = self.hearts[self.heart-1]
        self.image.set_alpha(0)

        self.rect = self.image.get_rect()
        self.rect.centerx = 807
        self.rect.centery = 563

    def change_hearts(self, amount):
        """This method accepts integer amount and changes the hearts based on the amount"""
        #Adds {amount} to self.heart and makes it so that there cannot be less than 1 or more than 10 hearts
        self.heart += amount
        if self.heart >= 10:
            self.heart = 10
        elif self.heart <= 1:
            self.heart = 1
        #Set the image attribute of the sprite
        self.image = self.hearts[self.heart-1]
    
    def display(self, value):
        """This method accepts boolean value and changes the opacity of the sprite based on the boolean"""
        if value:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
    
    def get_hearts(self):
        """This method returns the amount of hearts the NPC has for the player"""
        return self.heart

class Menu_Buttons(pygame.sprite.Sprite):
    """This class defines the menu button sprites"""
    def __init__(self, button):
        """This initializes accepts string button and displays a different image based on the value. It also initializes
        the image and rect attributes of the button"""
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        #If it is the play button, set the image and rect attributes for the play button
        if button == 'play':
            self.image = pygame.image.load('sprites/UI/Menu/play button.png').convert_alpha()
            self.rect = self.image.get_rect()

            self.rect.centerx = 615
            self.rect.centery = 548
        #Otherwise, set the image and rect attributes for the settings button
        else:
            self.image = pygame.image.load('sprites/UI/Menu/settings button.png').convert_alpha()
            self.rect = self.image.get_rect()

            self.rect.centerx = 735
            self.rect.centery = 548
        
        #Instance variables that keep track of whether or not the button is being interacted with or if it is displaying
        self.interacting = False
        self.displaying = True

    def display(self, value):
        """This method accepts boolean value as a parameter and changes the button's opacity based on it's boolean"""
        if value:
            self.displaying = True
            self.image.set_alpha(255)
        else:
            self.displaying = False
            self.image.set_alpha(0)

    def is_interacting(self, value):
        """This method accepts boolean value as a parameter and changes the button's self.interacting value based on it"""
        if value:
            self.interacting = True
        else:
            self.interacting = False

    def get_interaction(self):
        """This method returns whether or not the button is being interacted with"""
        return self.interacting