#改进日志：现在的想法是做成雷霆战机的那种样子
#首先速度肯定要改，由于是全屏的情况下还要再做考虑（能不能把雷霆战机的屏幕横过来？）
#增加道具，如果飞船接触到道具有加成
#增加不同种类的外星人，不同颜色，不同数值，血量和速度
#背景肯定要更换
#试着将它做成一个安装包的形式，而不是纯代码
#能不能用python写一个植物大战僵尸出来？
#击杀反馈太差没有打击感
#增加飞机的惯性系统
#射击不是单点而是只要按了空格就会发射
#移动改为wasd


import sys

from time import sleep

import pygame

from setting import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = False

        self.play_button = Button(self,  "play")

    def run_game(self):
        while True:
            self._check_events()

            if self.game_active:

             #每次循环时都重绘屏幕
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type ==pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
            if not self.aliens:
                self.bullets.empty()
                self._create_fleet()
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens, True, True)
        

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width -2*alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2*alien_height


    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit

        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):

        if self.stats.ships_left > 0:
        
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)

        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
           

            

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()