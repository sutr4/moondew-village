"""
NAME: TRACY SU
DATE: MAY30 2024
DESC: Stardew Valley remake
"""
import pygame, pygame.mixer, game_sprites, random

class Main():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Moondew Village")

        pygame.mouse.set_visible(False)

        self.__entities()
        self.__soundFX()
        self.__entities_sprites()
        self.__alter()

        pygame.quit()

    def __entities(self):
        self.menu = True
        self.title_screen = True
        self.settings = False
        self.menu_screen = pygame.image.load('sprites/UI/Menu/Menu Screen.png').convert()
        self.settings_screen = pygame.image.load('sprites/UI/Menu/settings.png').convert_alpha()
        self.play_button = game_sprites.Menu_Buttons('play')
        self.settings_button = game_sprites.Menu_Buttons('settings')

        self.background = pygame.image.load('sprites/Background/background.png').convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.screen.blit(self.background, (0,0))

        self.world = game_sprites.World(self.screen)
        
        self.allDirt = pygame.sprite.Group()
        self.dirt_list = []
        self.dirt_outline_list = []
        x_list = [432, 464, 496, 528, 560, 560, 432, 464, 496, 528, 560]
        y_list = [176, 176, 176, 176, 176, 144, 208, 208, 208, 208, 208]
        for x in range(11):
            dirt = game_sprites.Farmable_Tile(x_list[x], y_list[x])
            dirt_outline = game_sprites.Tile_Outline(x_list[x], y_list[x])

            self.dirt_list.append(dirt)
            self.dirt_outline_list.append(dirt_outline)
            self.allDirt.add(dirt, dirt_outline)

        self.my_roof = game_sprites.Roof('big', 176, 144)
        self.roof1 = game_sprites.Roof('big', 944, 80)
        self.roof2 = game_sprites.Roof('small', 1152, 112)
        self.allRoofs = pygame.sprite.Group(self.my_roof, self.roof1, self.roof2)

        self.shop = game_sprites.Shop()
        self.allShopButtons = pygame.sprite.Group()
        self.shop_buttons_list = []
        x_list = [781, 867, 781, 867, 781, 867, 781, 867, 781, 867, 781, 867, 781, 867]
        y_list = [212, 212, 268, 268, 324, 324, 380, 380, 436, 436, 492, 492, 548, 548]
        for x in range(14):
            shop_button = game_sprites.ShopButton(x, x_list[x], y_list[x])
            
            self.shop_buttons_list.append(shop_button)
            self.allShopButtons.add(shop_button)

    def __soundFX(self):
        pygame.mixer.music.load('audio/Stardew Valley Overture.mp3')
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)

        self.farmFX = pygame.mixer.Sound("audio/hoeHit.wav")
        self.farmFX.set_volume(0.07)
        self.harvestFX = pygame.mixer.Sound("audio/harvest.wav")
        self.harvestFX.set_volume(0.1)
        self.plantFX = pygame.mixer.Sound("audio/seeds.wav")
        self.plantFX.set_volume(0.1)

        self.walkingFX = pygame.mixer.Sound("audio/grassyStep.wav")
        self.walkingFX.set_volume(0.01)

        self.waterFX = pygame.mixer.Sound('audio/water_lap1.wav')
        self.waterFX.set_volume(0.1)

        self.dialogInFX = pygame.mixer.Sound('audio/dialogueCharacter.wav')
        self.dialogInFX.set_volume(0.5)
        self.dialogOutFX = pygame.mixer.Sound("audio/dialogueCharacterClose.wav")
        self.dialogOutFX.set_volume(0.05)

        self.giftFX = pygame.mixer.Sound("audio/give_gift.wav")
        self.giftFX.set_volume(0.1)

        self.purchaseFX = pygame.mixer.Sound("audio/purchase.wav")
        self.purchaseFX.set_volume(0.1)
        self.sellFX = pygame.mixer.Sound("audio/sell.wav")
        self.sellFX.set_volume(0.1)

        self.monsterFX = pygame.mixer.Sound("audio/monsterdead.wav")
        self.monsterFX.set_volume(0.05)

        self.roosterFX = pygame.mixer.Sound("audio/rooster.wav")
        self.roosterFX.set_volume(0.1)

    def __entities_sprites(self):
        self.cursor = game_sprites.Cursor()
        self.inventory = game_sprites.Inventory()
        self.slots, self.slot_counts = self.inventory.get_slots()

        self.player = game_sprites.Player(self.world)

        self.grey_cat = game_sprites.NPC(2, 1150, 125, self.world, 'talk')
        self.black_cat = game_sprites.NPC(3, 225, 225, self.world, 'tutorial')
        self.orange_cat = game_sprites.NPC(1, 1200, 600, self.world, 'talk')
        self.blacknwhite_cat = game_sprites.NPC(0, 675, 400, self.world, 'talk')

        self.zombie = game_sprites.Zombie()

        self.dialog_box = game_sprites.Dialog(self.screen)
        self.dialogue = game_sprites.Dialogue()
        self.bnw_hearts, self.orange_hearts, self.grey_hearts, self.black_hearts = self.dialog_box.get_hearts()

        self.user_info = game_sprites.User_Info()
        self.night = self.user_info.get_night()

        self.bed = game_sprites.Bed()

        self.menuSprites = pygame.sprite.Group(self.play_button, self.settings_button, self.cursor)
        self.allSprites = pygame.sprite.Group(self.allDirt, self.orange_cat, self.black_cat, self.grey_cat, self.bed, self.zombie,
                                              self.blacknwhite_cat, self.player, self.allRoofs, self.night, self.inventory,
                                              self.slots, self.slot_counts, self.dialog_box, self.shop, self.allShopButtons,
                                              self.bnw_hearts, self.orange_hearts, self.grey_hearts, self.black_hearts, self.user_info,
                                              self.cursor)
        
        self.cats = [self.black_cat, self.orange_cat, self.grey_cat, self.blacknwhite_cat]

    def __alter(self):
        moving_left = False
        moving_right = False
        moving_up = False
        moving_down = False
        day = 1
        spawn_chance = 1

        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(144)
            
            if self.menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            pygame.mixer.music.fadeout(2000)
                            run = False

                if self.title_screen:
                    self.screen.blit(self.menu_screen, (0,0))
                    self.settings_button.display(True)
                    self.play_button.display(True)

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.settings_button.get_interaction() and event.button == 1:
                                self.settings = True
                                self.title_screen = False
                                self.settings_button.display(False)
                                self.play_button.display(False)
                            
                            if self.play_button.get_interaction() and event.button == 1:
                                self.menu = False
                                self.cursor.show(False)

                if self.settings:
                    self.screen.blit(self.settings_screen, (0,0))
                    
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.title_screen = True
                                self.settings = False
                            
            if not self.menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.mixer.music.fadeout(2000)
                        run = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            moving_up = True
                        if event.key == pygame.K_s:
                            moving_down = True
                        if event.key == pygame.K_a:
                            moving_left = True
                        if event.key == pygame.K_d:
                            moving_right = True

                        if event.key == pygame.K_1:
                            self.inventory.select_slot(0)
                        if event.key == pygame.K_2:
                            self.inventory.select_slot(1)
                        if event.key == pygame.K_3:
                            self.inventory.select_slot(2)
                        if event.key == pygame.K_4:
                            self.inventory.select_slot(3)
                        if event.key == pygame.K_5:
                            self.inventory.select_slot(4)
                        if event.key == pygame.K_6:
                            self.inventory.select_slot(5)
                        if event.key == pygame.K_7:
                            self.inventory.select_slot(6)
                        if event.key == pygame.K_8:
                            self.inventory.select_slot(7)
                        if event.key == pygame.K_9:
                            self.inventory.select_slot(8)

                        for x, dirt in enumerate(self.dirt_outline_list):
                            if event.key == pygame.K_f and dirt.get_highlight():

                                if self.inventory.get_selected() == 'hoe':
                                    if self.dirt_list[x].get_type() == 'wheat' and self.dirt_list[x].get_state() == 3:
                                        self.inventory.add_item('wheat', 1)
                                        self.inventory.add_item('wheat_seeds', random.randint(1, 2))
                                        self.harvestFX.play()
                                    elif self.dirt_list[x].get_type() == 'plum' and self.dirt_list[x].get_state() == 3:
                                        self.inventory.add_item('plum', 1)
                                        self.inventory.add_item('plum_seeds', random.randint(1, 2))
                                        self.harvestFX.play()
                                    else:
                                        self.farmFX.play()
                                    self.dirt_list[x].till()

                                if self.inventory.get_selected() == 'wheat_seeds':
                                    if self.dirt_list[x].plant_wheat():
                                        self.plantFX.play()
                                        self.inventory.use((self.inventory.get_selected_slot()), 1, True)
                                if self.inventory.get_selected() == 'plum_seeds':
                                    if self.dirt_list[x].plant_plum():
                                        self.plantFX.play()
                                        self.inventory.use((self.inventory.get_selected_slot()), 1, True)
                                if self.inventory.get_selected() == 'watering_can':
                                    self.dirt_list[x].water(True)
                                    self.waterFX.play()

                        for cat in self.cats:
                            state = self.dialog_box.get_state()
                            if cat.get_interaction():
                                if cat == self.black_cat:
                                    if cat.get_state() == 'tutorial':
                                        if event.key == pygame.K_f and not self.dialog_box.get_display():
                                            self.dialog_box.display(4, "Welcome to Moondew Village!", '', 3, False)
                                            self.dialogInFX.play()
                                        if event.key == pygame.K_SPACE and self.dialog_box.get_display():
                                            for x in range(self.dialogue.tutorial_dialog()):
                                                if state == x:
                                                    dialog = self.dialogue.get_states()[self.dialogue.get_state_num('tutorial')][x]
                                                    self.dialog_box.display(dialog[0], dialog[1], dialog[2], dialog[3], dialog[4])
                                                    if state == 9:
                                                        self.inventory.add_item('hoe', 1)
                                                        self.inventory.add_item('watering_can', 1)
                                                        self.inventory.add_item('wheat_seeds', 3)
                                                    elif state == 10:
                                                        cat.change_state('talk')

                                    elif cat.get_state() == 'talk' and event.key == pygame.K_f and not self.dialog_box.get_display():
                                        self.dialogInFX.play()
                                        dialog = random.randint(1, 2)
                                        if dialog == 1:
                                            self.dialog_box.display(0, "All crops are harvestable 3 days after", 'being planted!', 3, True)
                                        elif dialog == 2:
                                            self.dialog_box.display(0, "Make sure to water your crops or else", "they won't grow!", 3, True)
                                    
                                    if event.key == pygame.K_g:
                                        self.giftFX.play()
                                        self.dialogInFX.play()
                                        if self.inventory.get_selected() == 'hoe' or self.inventory.get_selected() == 'watering_can':
                                            self.dialog_box.display(3, "You probably shouldn't give me that.", "Can't get another one around here.", 3, True)
                                        elif self.inventory.get_selected() == 'apple':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.black_hearts.change_hearts(-3)
                                            self.dialog_box.display(1, "I hate apples...", '', 3, True)
                                        elif self.inventory.get_selected() != 'empty':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.dialog_box.display(0, "Thanks!", "", 3, True)
                                    
                                elif cat == self.grey_cat:
                                    if cat.get_state() == 'wedding ani delivery':
                                        if event.key == pygame.K_f and not self.dialog_box.get_display():
                                            self.dialogInFX.play()
                                            self.dialog_box.display(5, "Oh hey... new farmer..", "", 2, False)
                                        if event.key == pygame.K_SPACE and self.dialog_box.get_display():
                                            for x in range(self.dialogue.wedding_ani_dialog()):
                                                if state == x:
                                                    dialog = self.dialogue.get_states()[self.dialogue.get_state_num('wedding_ani')][x]
                                                    self.dialog_box.display(dialog[0], dialog[1], dialog[2], dialog[3], dialog[4])
                                                    if state == 5:
                                                        cat.change_state('waiting for wheat')

                                    elif cat.get_state() == 'comfort oreo':
                                        if event.key == pygame.K_f and not self.dialog_box.get_display():
                                            self.dialogInFX.play()
                                            self.dialog_box.display(3, "Oreo seems really mad at me..", "", 2, False)
                                        if event.key == pygame.K_SPACE and self.dialog_box.get_display():
                                            for x in range(self.dialogue.comforting_oreo_dialog()):
                                                if state == x:
                                                    dialog = self.dialogue.get_states()[self.dialogue.get_state_num('comfort_oreo')][x]
                                                    self.dialog_box.display(dialog[0], dialog[1], dialog[2], dialog[3], dialog[4])
                                                    if state == 0:
                                                        self.user_info.change_coins(50)
                                                        self.sellFX.play()
                                                    if state == 1:
                                                        cat.change_state('waiting oreo response')
                                            
                                    elif cat.get_state() == 'waiting oreo response':
                                        if self.blacknwhite_cat.get_state() == 'reconciled':
                                            if event.key == pygame.K_f and not self.dialog_box.get_display():
                                                self.dialogInFX.play()
                                                self.dialog_box.display(3, "What did she say???", "", 2, False)
                                            if event.key == pygame.K_SPACE and self.dialog_box.get_display():
                                                for x in range(self.dialogue.waiting_for_oreo_dialog()):
                                                    dialog = self.dialogue.get_states()[self.dialogue.get_state_num('waiting for oreo')][x]
                                                    self.dialog_box.display(dialog[0], dialog[1], dialog[2], dialog[3], dialog[4])
                                                    if state == 0:
                                                        self.user_info.change_coins(75)
                                                        self.sellFX.play()
                                                        self.grey_hearts.change_hearts(3)
                                                    if state == 1:
                                                        cat.change_state('talk')
                                        else:
                                            if event.key == pygame.K_f and not self.dialog_box.get_display():
                                                self.dialogInFX.play()
                                                self.dialog_box.display(3, "Did you talk to her yet???", "", 2, True)
                                        
                                    elif event.key == pygame.K_f and not self.dialog_box.get_display():
                                        self.dialogInFX.play()
                                        if cat.get_state() == 'waiting for wheat':
                                            if self.inventory.get_selected() == 'wheat' and self.inventory.get_selected_slot_count() >= 5:
                                                self.inventory.use(self.inventory.get_selected_slot(), 5, True)
                                                self.dialog_box.display(0, "Thank you so much! Please take this.", "", 2, True)
                                                self.grey_hearts.change_hearts(3)
                                                self.user_info.change_coins(50)
                                                self.sellFX.play()
                                                cat.change_state('happy delivery')
                                            else:
                                                self.dialog_box.display(5, "Did you get it?", "", 2, True)

                                        elif cat.get_state() == 'talk':
                                            dialog = random.randint(1, 2)
                                            if dialog == 1:
                                                self.dialog_box.display(5, "I am so tired...", "", 2, True)
                                            elif dialog == 2:
                                                self.dialog_box.display(3, "That zombie that comes out at night", "scares me...", 2, True)
                                        elif cat.get_state() == 'happy delivery':
                                            self.dialog_box.display(0, "You're a life-saver!", "", 2, True)
                                        elif cat.get_state() == 'sad delivery':
                                            self.grey_hearts.change_hearts(-2)
                                            self.dialog_box.display(1, "I could've really used those wheat..", '', 2, True)

                                    if event.key == pygame.K_g:
                                        self.giftFX.play()
                                        self.dialogInFX.play()
                                        if self.inventory.get_selected() == 'hoe' or self.inventory.get_selected() == 'watering_can':
                                            self.dialog_box.display(3, "You probably shouldn't give me that.", "Can't get another one around here.", 2, True)
                                        elif self.inventory.get_selected() == 'apple':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.grey_hearts.change_hearts(3)
                                            self.dialog_box.display(4, "I love apples! Thanks!", '', 2, True)
                                        elif self.inventory.get_selected() != 'empty':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.dialog_box.display(0, "Thanks!", "", 2, True)
                                            
                                elif cat == self.orange_cat:
                                    if cat.get_state() == 'talk':
                                        if event.key == pygame.K_f and not self.dialog_box.get_display() and not self.shop.get_display():
                                            self.dialogInFX.play()
                                            dialog = random.randint(1, 2)
                                            if dialog == 1:
                                                self.dialog_box.display(0, "Hi!!!! I'm Mei! If you want to purchase",
                                                                        "or sell anything, press E with me!!", 1, True)
                                            elif dialog == 2:
                                                self.dialog_box.display(0, "The sun is blaring today!", "", 1, True)
                                            
                                    if event.key == pygame.K_e and not self.dialog_box.get_display() and not self.shop.get_display():
                                        self.dialogInFX.play()
                                        self.shop.show(True)
                                        self.cursor.show(True)
                                        self.user_info.shop_view(True)
                                        for x in range(14):
                                            self.shop_buttons_list[x].show(True)
                                        break
                                    
                                    if event.key == pygame.K_e and not self.dialog_box.get_display() and self.shop.get_display():
                                        self.dialogOutFX.play()
                                        self.shop.show(False)
                                        self.cursor.show(False)
                                        self.user_info.shop_view(False)
                                        for x in range(14):
                                            self.shop_buttons_list[x].show(False)
                                        break

                                    if event.key == pygame.K_g:
                                        self.giftFX.play()
                                        self.dialogInFX.play()
                                        if self.inventory.get_selected() == 'hoe' or self.inventory.get_selected() == 'watering_can':
                                            self.dialog_box.display(3, "You probably shouldn't give me that.", "Can't get another one around here.", 1, True)
                                        elif self.inventory.get_selected() == 'plum':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.orange_hearts.change_hearts(2)
                                            self.dialog_box.display(4, "Plums are delicious!", '', 1, True)
                                        elif self.inventory.get_selected() != 'empty':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.dialog_box.display(0, "Thanks!", "", 1, True)

                                elif cat == self.blacknwhite_cat:
                                    if cat.get_state() == 'angry oreo':
                                        if event.key == pygame.K_f and not self.dialog_box.get_display():
                                            self.dialog_box.display(1, "Nothing hurts more than a friend", "disappointing you...", 0, False)
                                            self.dialogInFX.play()
                                        if event.key == pygame.K_SPACE and self.dialog_box.get_display():
                                            for x in range(self.dialogue.angry_oreo_dialog()):
                                                if state == x:
                                                    dialog = self.dialogue.get_states()[self.dialogue.get_state_num('oreo_mad')][x]
                                                    self.dialog_box.display(dialog[0], dialog[1], dialog[2], dialog[3], dialog[4])
                                                    if state == 6:
                                                        cat.change_state('mute')

                                    elif cat.get_state() == 'mute':
                                        if event.key == pygame.K_f and not self.dialog_box.get_display():
                                            self.dialogInFX.play()
                                            if self.inventory.get_selected() == 'milk':
                                                self.dialog_box.display(1, "What do you want..", "", 0, False)
                                                self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            else:
                                                self.dialog_box.display(1, "...", "", 0, True)
                                        if event.key == pygame.K_SPACE and self.dialog_box.get_display():
                                            for x in range(self.dialogue.oreo_chessur_pt1()):
                                                if state == x:
                                                    dialog = self.dialogue.get_states()[self.dialogue.get_state_num('mute')][x]
                                                    self.dialog_box.display(dialog[0], dialog[1], dialog[2], dialog[3], dialog[4])
                                                    if state == 3:
                                                        cat.change_state('reconciled')
                                    
                                    elif event.key == pygame.K_f and not self.dialog_box.get_display():
                                        self.dialogInFX.play()
                                        if cat.get_state() == 'reconciled':
                                            self.dialog_box.display(1, "I guess there's always next year.", "", 0, True)
                                        elif cat.get_state() == 'talk':
                                            self.dialog_box.display(3, "I heard if you feed the zombies milk,", "they disappear for the night.", 0, True)
                                    
                                    if event.key == pygame.K_g:
                                        self.giftFX.play()
                                        self.dialogInFX.play()
                                        if self.inventory.get_selected() == 'hoe' or self.inventory.get_selected() == 'watering_can':
                                            self.dialog_box.display(3, "You probably shouldn't give me that.", "Can't get another one around here.", 0, True)
                                        elif self.inventory.get_selected() == 'milk':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.bnw_hearts.change_hearts(4)
                                            self.dialog_box.display(4, "Thank you so much! How'd you know", 'I loved milk?', 0, True)
                                        elif self.inventory.get_selected() != 'empty':
                                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)
                                            self.dialog_box.display(0, "Thanks!", "", 0, True)

                                if event.key == pygame.K_SPACE and (self.dialog_box.get_display()) and (self.dialog_box.get_done_talking()):
                                    self.dialog_box.show(False)
                                    self.inventory.change_opacity(False)
                                    self.dialogOutFX.play()
                        
                        if event.key == pygame.K_f and self.bed.get_interaction():
                            self.user_info.new_day()
                        
                        if event.key == pygame.K_f and self.zombie.get_interaction() and self.inventory.get_selected() == 'milk':
                            self.zombie.cure()
                            self.inventory.use(self.inventory.get_selected_slot(), 1, True)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            moving_up = False
                        if event.key == pygame.K_s:
                            moving_down = False
                        if event.key == pygame.K_a:
                            moving_left = False
                        if event.key == pygame.K_d:
                            moving_right = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.shop.get_display():
                            for button in self.shop_buttons_list:
                                if button.get_interaction() and event.button == 1:
                                    type, item, price = button.get_button()
                                    if type == 'buy' and self.user_info.get_coins() >= price:
                                        self.user_info.change_coins(-price)
                                        self.inventory.add_item(item, 1)
                                        self.purchaseFX.play()
                                    elif type == 'sell' and item in self.inventory.get_inventory():
                                        self.user_info.change_coins(price)
                                        self.inventory.use(item, 1, False)
                                        self.sellFX.play()
                                
                    if self.dialog_box.get_display() or self.shop.get_display():
                        moving_up = False
                        moving_down = False
                        moving_right = False
                        moving_left = False
                    
                if self.user_info.get_day() != day:
                    self.roosterFX.play()
                    day = self.user_info.get_day()
                    self.zombie.change_alive(False)
                    spawn_chance = random.randint(1, 3)
                    for y, dirt in enumerate(self.dirt_list):
                        self.dirt_list[y].grow()
                    if day == 11:
                        self.grey_cat.change_state('wedding ani delivery')
                    if day == 12:
                        if self.grey_cat.get_state() == 'waiting for wheat':
                            self.grey_cat.change_state('sad delivery')
                        elif self.grey_cat.get_state() == 'wedding ani delivery':
                            self.grey_cat.change_state('talk')
                    if day == 15:
                        self.blacknwhite_cat.change_state('angry oreo')
                        self.grey_cat.change_state('comfort oreo')

                if self.night.get_night() and not self.zombie.get_cure() and not self.zombie.get_alive():
                    if spawn_chance == 1:
                        self.monsterFX.play()
                        self.zombie.change_alive(True)

                self.world.draw()

            self.player.movement(moving_left, moving_right, moving_up, moving_down)

            self.__refresh()
            self.__detect_collision()

    def __detect_collision(self):
        sprites = [self.user_info, self.my_roof, self.roof1, self.roof2]
        for sprite in sprites:
            if self.player.rect.colliderect(sprite):
                sprite.change_opacity(True)
            else:
                sprite.change_opacity(False)

        if (self.inventory.rect.colliderect(self.player.rect)) or (self.dialog_box.get_display()):
            self.inventory.change_opacity(True)
        else:
            self.inventory.change_opacity(False)

        for x, dirt in enumerate(self.dirt_list):
            if (self.player.farm_hitbox.colliderect(dirt)) and (self.inventory.get_selected() == 'hoe' or \
                                                                self.inventory.get_selected() == 'watering_can' or \
                                                                self.inventory.get_selected() == 'wheat_seeds' or \
                                                                self.inventory.get_selected() == 'plum_seeds'):
                self.dirt_outline_list[x].highlight(True)
            else:
                self.dirt_outline_list[x].highlight(False)

            if self.zombie.hitbox.colliderect(dirt) and self.zombie.get_alive():
                self.walkingFX.play()
                dirt.untill()
        
        cats = [self.black_cat, self.orange_cat, self.grey_cat, self.blacknwhite_cat, self.zombie]
        for cat in cats:
            if self.player.rect.colliderect(cat.interact_hitbox):
                cat.change_interaction(True)
            else:
                cat.change_interaction(False)

        if self.shop.get_display():
            for button in self.shop_buttons_list:
                if self.cursor.hitbox.colliderect(button.rect):
                    button.change_interaction(True)
                else:
                    button.change_interaction(False)

        if self.player.rect.colliderect(self.bed.hitbox):
            self.bed.is_interacting(True)
        else:
            self.bed.is_interacting(False)
        
        buttons = [self.play_button, self.settings_button]
        for button in buttons:
            if self.cursor.hitbox.colliderect(button.rect):
                button.is_interacting(True)
            else:
                button.is_interacting(False)

    def __refresh(self):
        if self.menu:
            self.menuSprites.update()
            self.menuSprites.draw(self.screen)
        else:
            self.allSprites.clear(self.screen, self.background)
            self.allSprites.update()
            self.allSprites.draw(self.screen)
        pygame.display.flip()

Main()