class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        
        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 28

        self.ship_speed = 6.0
        self.ship_limit = 3

        self.alien_speed = 10.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1