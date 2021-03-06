import pygame
import os
import math
import time
import ui_helper
import game_logic
import map
import random
import generator
import sys
import json


# given an image and an angle this returns the rotated image
# can directly be drawn to screen



def rotate_image(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#does not get called

'''def reset_screen(screen,current_game):
    screen.blit(ui_helper.draw_resources(current_game), (533, 450))
    screen.blit(ui_helper.draw_crew_overview(),(0, 0))
    ship_visual = pygame.Rect(width / 3, 0, width / 3, height / 2)
    pygame.draw.rect(screen, (0, 0, 0), ship_visual)'''

def display_night(screen,night):
    if night is True:
        night_display = pygame.Surface((533, 900))
        night_display.set_alpha(128)
        night_display.fill((0,0,0))
        screen.blit(night_display, ((533 * 2), 0))

def main(username):
    pygame.init()  # turn all of pygame on.
    # init size of the window. The background color is never visible
    width, height = (1600, 900)
    background_color = (0, 0, 0)

    if len(os.listdir(os.path.join(os.getcwd(),"data","savegame"))) < 3:
        generator.crewgen()
        generator.start_state_gen(username)
        generator.mapgen()
    # path to resources (images in this case)
    asset_path = os.path.join(os.getcwd(), "data", "img")

    # init UI elements and provide them with coordinates
    ship = pygame.image.load(os.path.join(asset_path, "ship.png"))
    minimap = pygame.image.load(os.path.join(asset_path, "minimap.jpg"))
    screen = pygame.display.set_mode((width, height))
    current_game = game_logic.game(screen)
    frame = pygame.Surface((width, height))
    managment_UI = pygame.Rect(0, 0, width / 3, height)
    ship_visual = pygame.Rect(width / 3, 0, width / 3, height / 2)
    ressource_visual = pygame.Rect(width / 3, height / 2, width / 3, height / 2)
    ship_movement_UI = pygame.Rect((width / 3) * 2, 0, width / 3, height)
    minimap = pygame.Surface((40,450))
    minimap.fill((43, 132, 216))
    if os.path.isfile(os.path.join(os.getcwd(),"data","savegame","minimap.png")):
        saved_minimap = pygame.image.load(os.path.join(os.getcwd(),"data","savegame","minimap.png"))
        minimap.blit(saved_minimap,(0,0))



    time_display = pygame.image.load(os.path.join(os.getcwd(),"data","img","clock_day.jpg"))


    # fill the screen with said elements
    pygame.display.set_caption("Pirate game")
    frame.fill(background_color)
    pygame.draw.rect(frame, (127, 4, 50), managment_UI)
    pygame.draw.rect(frame, (161, 83, 27), ressource_visual)
    pygame.draw.rect(frame, (43, 132, 216), ship_movement_UI)

    resource_screen = ui_helper.draw_resources(current_game)
   ######### frame.blit(, (533, 450))


    frame.blit(ship, (1250, 350))
    #screen.blit(overlay, (0, 0))
    frame.blit(time_display, (533 + 40, 0))

    # flip displayes everything for the user to see
    pygame.display.flip()

    ship_map_x = 750
    ship_map_y = 350

    if "savegame.json" in os.listdir(os.path.join(os.getcwd(),"data","savegame")):
        savefile = open(os.path.join(os.path.join(os.getcwd(),"data","savegame","savegame.json")))
        data = json.load(savefile)
        if "ship_map_x" in data.keys():
            ship_map_x = data["ship_map_x"]
        if "ship_map_y" in data.keys():
            ship_map_y = data["ship_map_y"]

    # gameloop
    running = True
    in_shop = False
    UI_is_blocked = False
    is_paused = False
    pause_timestamp = None
    is_night = False
    game_over = False
    angle = 0
    dotexists = False
    initx = 0
    inity = 0
    popup = None
    dot_map_x = 0
    dot_map_y = 0
    currentangle = 0
    speed = 4
    rotation_speed = 4
    ship_hit_box = pygame.Rect(1340, 440, 20, 20)
    clock = pygame.time.Clock()
    shop = None
    last_island = {}
    paused_time = 0
    start_time = time.time()
    screen.blit(frame, (0, 0))
    current_game.update_screen(frame)
    current_game.set_minimap(minimap)
    map.mapdraw(ship_map_x, ship_map_y, current_game.get_minimap(),frame)
    sound_time = time.time()
    pygame.mixer.init()

    f = open(os.path.join(os.getcwd(),"data","other", "settings.json"))
    data = json.load(f)
    f.close()
    sound_state = data["sound_state"]
    print(sound_state)
    SONG_END = pygame.USEREVENT + 1
    if sound_state == 1:
        print("sounds")
        seagull_sound = pygame.mixer.Sound(os.path.join(os.path.join(os.getcwd(), "data", "sound", "seagulls.wav")))
        seagull_sound.set_volume(0.2)
        pygame.mixer.Sound.play(seagull_sound)
        print("playing seagull")
        if random.randint(1,2)==1:
            song = pygame.mixer.Sound(os.path.join(os.getcwd(),"data","sound","background1.wav"))
            duration = 60 + 53
            song_loaded = 1
        else:
            song = pygame.mixer.Sound(os.path.join(os.getcwd(), "data", "sound", "background2.wav"))
            duration = 139
            song_loaded = 2
        print("loaded song")
        song.set_volume(0.1)
        pygame.mixer.Sound.play(song)
        print("at_start")

    song_timer = time.time()
    song_pause = 0
    print("past init")

    while running:
        current_game.set_time(time_display)
        if not game_over:
            island = map.collisioncheck(ship_map_x, ship_map_y,)

        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:
                sys.exit(0)
            # at mouseclick:
            # - checks if click was in ship movement window and if so rotates the ship image
            if event.type == pygame.MOUSEBUTTONDOWN and ship_movement_UI.collidepoint(pygame.mouse.get_pos()) and not in_shop and not UI_is_blocked:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                initx, inity = pygame.mouse.get_pos()
                dot_map_x = ship_map_x - 266 + mouse_x - 1066
                dot_map_y = 900 - mouse_y + ship_map_y - 200
                # angle = (180 / math.pi) * -math.atan2((mouse_y - 450), (mouse_x - 1350))
                pygame.draw.rect(frame, (43, 132, 216), ship_movement_UI)
                #screen.blit(overlay, (0, 0))
                pygame.draw.ellipse(frame, (255, 0, 0), pygame.Rect(mouse_x, mouse_y, 10, 10))
                dotexists = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_paused is True and popup:
                        popup = None
                        is_paused = False
                        UI_is_blocked = False
                        if sound_state == 1:
                            water_sound = pygame.mixer.Sound(os.path.join(os.path.join(os.getcwd(), "data", "sound", "water.wav")))
                            water_sound.set_volume(0.5)
                            pygame.mixer.Sound.play(water_sound)

            if event.type == pygame.MOUSEBUTTONDOWN and managment_UI.collidepoint(pygame.mouse.get_pos()) and not in_shop and not UI_is_blocked:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                print("managing")
                if 100<mouse_x<200:
                    i = 0
                    #ability
                    while i<9:
                        button_y = 130+i*100
                        if button_y<mouse_y<(button_y+50):
                            print("send to work")
                            popup = current_game.crew_ability(i)
                            if popup:
                                frame.blit(popup.get_surf(), popup.get_surf().get_rect(center=(800, 450)))
                                popup.set_offset(800, 450)
                                UI_is_blocked = True
                                is_paused = True
                            break
                        i+=1
                #dispatch
                if 475<mouse_x<505:
                    i = 0
                    while i < 9:
                        button_y = 100 + i * 100
                        if button_y < mouse_y < (button_y + 40):
                            print("dispatching")
                            popup = current_game.attempt_dispatch(i)

                            UI_is_blocked = True
                            break
                        i += 1
                if 225<mouse_x<325:
                    i = 0
                    while i<9:
                        button_y = 133+(i*100)
                        if button_y < mouse_y < (button_y+33):
                            popup = current_game.crew_heal_potion(i)
                            UI_is_blocked = True
                            break
                        i+=1

            if event.type == pygame.MOUSEBUTTONDOWN and in_shop:
                if managment_UI.collidepoint(pygame.mouse.get_pos()):
                    item,price = shop.interact(pygame.mouse.get_pos())
                    if shop.is_active():
                        current_game.make_purchase(item, price)
                        frame.blit(shop.get_surface(),(0,0))
                    else:
                        in_shop = False
                        is_paused = False
                    resource_screen = ui_helper.draw_resources(current_game)

            if event.type == pygame.MOUSEBUTTONDOWN and UI_is_blocked:
                popup.is_collide(pygame.mouse.get_pos(),frame,current_game)
                pop_surf = popup.get_surf()
                if pop_surf:
                    frame.blit(pop_surf, pop_surf.get_rect(center=(800, 450)))
                if not popup.is_active() and game_over is False:
                    resource_screen = ui_helper.draw_resources(current_game)
                    UI_is_blocked = False
                    popup = None
                    is_paused = False
                    if sound_state == 1:
                        water_sound = pygame.mixer.Sound(os.path.join(os.path.join(os.getcwd(), "data", "sound", "water.wav")))
                        water_sound.set_volume(0.5)
                        pygame.mixer.Sound.play(water_sound)
                elif not popup.is_active() and game_over is True:
                    running = False

            if time.time() - song_timer > duration:
                if song_loaded == 1:
                    song = pygame.mixer.Sound(os.path.join(os.getcwd(), "data", "sound", "background2.wav"))
                    song.set_volume(0.1)
                    pygame.mixer.Sound.play(song)
                    song_timer = time.time()
                    song_loaded = 2
                    duration = 139
                else:
                    song = pygame.mixer.Sound(os.path.join(os.getcwd(), "data", "sound", "background1.wav"))
                    song.set_volume(0.1)
                    pygame.mixer.Sound.play(song)
                    song_timer = time.time()
                    song_loaded = 1
                    duration = 53 + 60

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if is_paused is False:
                        current_game.set_cord(ship_map_x, ship_map_y)
                        current_game.set_minimap(minimap)
                        popup = ui_helper.popup_window(type=5)
                        frame.blit(popup.get_surf(), popup.get_surf().get_rect(center=(800, 450)))
                        popup.set_offset(800, 450)
                        UI_is_blocked = True
                        is_paused = True


        pygame.display.flip()

        point_hit_box = pygame.Rect(initx, inity, 10, 10)

        # map



        #print("Y: " + str(ship_map_y))
        #print("X: " + str(ship_map_x))


        y_speed = math.sin(math.radians(currentangle + 90))
        x_speed = math.cos(math.radians(currentangle + 90))


        if dotexists and not (ship_hit_box.colliderect(point_hit_box)) and not is_paused and not game_over:
            if ship_map_x > 1200 :
                ship_map_x += -1500
            if ship_map_x < -300:
                ship_map_x += 1500
            initx -= x_speed * speed * current_game.get_speed_multiplier()
            inity += y_speed * speed * current_game.get_speed_multiplier()
            pygame.draw.rect(frame, (43, 132, 216), ship_movement_UI)
            map.mapdraw(ship_map_x,ship_map_y,current_game.get_minimap(),frame)

            pygame.draw.ellipse(frame, (255, 0, 0), pygame.Rect(initx, inity, 10, 10))


            ship_map_x += x_speed * speed
            ship_map_y += y_speed * speed

            angle = (180 / math.pi) * -math.atan2((inity - 450), (initx - 1350))

            # Rotation
            # ----------------------------------------------------------
            if currentangle > -90 and ((angle - 90) - currentangle) < -180:
                currentangle += rotation_speed
            elif currentangle < -90 and ((angle - 90) - currentangle) > 180:
                currentangle -= rotation_speed
            else:
                if currentangle < angle - 90:
                    currentangle += rotation_speed
                elif currentangle > angle - 90:
                    currentangle -= rotation_speed
            if currentangle < -279.5:
                currentangle = 89.5
            elif currentangle > 89.5:
                currentangle = -279.5
            frame.blit(rotate_image(ship, +currentangle), (1250, 350))
            display_night(frame,is_night)
            frame.blit(current_game.get_minimap(), (533, 0))
            frame.blit(time_display,(533 + 40, 0))

        if not UI_is_blocked:
            frame.blit(resource_screen,((533, 450)))

        if island and island != last_island:
            last_island = island
            if island["island_values"]["type"] == 1:
                shop = current_game.island_event(type=island["island_values"]["type"],
                                                 size=island["island_values"]["size"])
                in_shop = True
                is_paused = True
            elif island["island_values"]["type"] == 2:
                popup = current_game.island_event(type=island["island_values"]["type"],
                                                  size=island["island_values"]["size"])
                UI_is_blocked = True
                is_paused = True
            elif island["island_values"]["type"] == 3:
                print("treasure")
                popup = current_game.island_event(type=3, size=island["island_values"]["size"])
                if popup:
                    UI_is_blocked = True
                    is_paused = True
            elif island["island_values"]["type"] == 0:
                popup = current_game.island_event(type=0, size=island["island_values"]["size"])
                if popup:
                    UI_is_blocked = True
                    is_paused = True
            elif island["island_values"]["type"] == 5:
                popup = current_game.island_event(type=5, size=island["island_values"]["size"])
                if popup:
                    UI_is_blocked = True
                    is_paused = True
                    game_over = True



        if is_paused is False and pause_timestamp is not None:
            paused_time+= time.time()-pause_timestamp
            pause_timestamp = None

        if UI_is_blocked or in_shop:
            is_paused = True
            pause_timestamp = time.time()

        if (time.time()-start_time-paused_time)>=5 and not is_night:


            time_display = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "clock_dawn.jpg"))
            frame.blit(time_display,(533+40,0))

        if (time.time()-start_time-paused_time)>=10 and not is_night:
            print("night has come")
            is_night = True

            time_display = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "clock_night.jpg"))
            frame.blit(time_display, (533 + 40, 0))

        if (time.time()-start_time-paused_time)>=15 and is_night:
            time_display = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "clock_sunrise.jpg"))
            frame.blit(time_display, (533 + 40, 0))

        if (time.time()-start_time-paused_time)>=20 and is_night:
            current_game.advance_tick()
            resource_screen = ui_helper.draw_resources(current_game)
            if not in_shop:
                frame.blit(ui_helper.draw_crew_overview(),(0,0))
            frame.blit(resource_screen, (533, 450))
            if UI_is_blocked:
                if popup.is_active():
                    frame.blit(popup.get_surf(), popup.get_surf().get_rect(center=(800, 450)))
            is_night = False
            start_time = time.time()
            time_display = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "clock_sunrise.jpg"))
            frame.blit(time_display, (533 + 40, 0))

        clock.tick(60)
        '''
        if not in_shop and not UI_is_blocked:
            screen.blit(ui_helper.draw_resources(current_game),(533,450))
        '''

        if not in_shop and not UI_is_blocked:
            frame.blit(ui_helper.draw_crew_overview(),(0,0))

        if popup:
            if popup.is_active():
                frame.blit(resource_screen,(533,450))
                frame.blit(time_display, (533 + 40, 0))
                frame.blit(popup.get_surf(), popup.get_surf().get_rect(center=(800, 450)))


        if game_over is False:
            game_over,message = current_game.is_game_over()


            if game_over:
                popup = ui_helper.popup_window(type=6,text=message)
                frame.blit(popup.get_surf(), popup.get_surf().get_rect(center=(800, 450)))
                popup.set_offset(800, 450)
                is_paused = True
                UI_is_blocked = True
        screen.blit(frame, (0, 0))
        pygame.display.flip()


        if (time.time()-sound_time)>30 and random.randint(0,100)>90 and sound_state==1:
            print("seagull")
            pygame.mixer.Sound.play(seagull_sound)
            sound_time = time.time()

    del current_game
    del popup
    del resource_screen
    pygame.quit()






