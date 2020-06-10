from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.theming import ThemeManager
from kivymd.uix.context_menu import MDContextMenu
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.config import Config
from kivy.core.window import Window
import sqlite3
import re

Config.set('graphics', 'resizable',  False )
db_name = "db_travian_test2.db"

class LanguageImage(CircularRippleBehavior, ButtonBehavior, Image):
    pass
class NationCustomIcon(CircularRippleBehavior, ButtonBehavior, Image):
    pass
class NationCustomLabel(CircularRippleBehavior, ButtonBehavior, MDLabel):
    pass
class CustomClock(MDBoxLayout):
    pass
class CustomTableInfo(MDBoxLayout):
    pass
class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


        
class Test(MDApp):
    bkscreencolor = (0, 0.3, 0.8)
    bktablecolor = (0, 0.5, 1, 1)
    rowcolor_1 = (0, 0.75, 1, 1)
    rowcolor_2 = (1,1,1,1)
    textcolor = (1,1,1,1)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (450,810)
        self.screen = Builder.load_file('travian.kv')
        widget_menu = ["'units_gauls'","'units_teutons'","'units_romans'","'bonus_helmet'","'items_nation'","'bonus_artefact'","'bonus_aliance'"]
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings_db WHERE option = 'language'")
        st_language = cursor.fetchone()[0] #мова з налаштувань
        cursor.execute("SELECT value FROM settings_db WHERE option = 'nation'")
        self.st_nation = cursor.fetchone()[0] # нация з налаштувань
        empty = []
        
        for key in widget_menu:
            q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(st_language, key)
            cursor.execute(q)
            a = cursor.fetchone()[0]
            a = a.split(",")
            empty.append(a)
            
        self.gauls_units, self.teutons_units, self.romans_units, self.items_bonus_helmet, self.items_nation, self.items_bonus_artefact, self.items_bonus_aliance = empty[0],empty[1],empty[2],empty[3],empty[4],empty[5],empty[6]
        print(empty)
        print(self.items_nation)
        if self.st_nation == 'Gauls':
            print('gauls')
            self.screen.ids.toolbar.ids.unit_button.text = self.gauls_units[0]
            self.screen.ids.toolbar.ids.nation_button.text = self.items_nation[0]
            self.item_units = self.gauls_units
            self.screen.ids.toolbar.ids.nation_icon.source = "datas/gauls.png"
        elif self.st_nation == 'Teutons':
            print('teutons')
            self.screen.ids.toolbar.ids.unit_button.text = self.teutons_units[0]
            self.screen.ids.toolbar.ids.nation_button.text = self.items_nation[2]
            self.item_units = self.teutons_units
            self.screen.ids.toolbar.ids.nation_icon.source = "datas/teutons.png"
        elif self.st_nation == 'Romans':
            print('romans')
            self.screen.ids.toolbar.ids.unit_button.text = self.romans_units[0]
            self.screen.ids.toolbar.ids.nation_button.text = self.items_nation[1]
            self.item_units = self.romans_units
            self.screen.ids.toolbar.ids.nation_icon.source = "datas/romans.png"
            
        db_widgets_text = {"'house_lvl'": self.screen.ids.house_lvl,
                          "'l_res'":self.screen.ids.l_res,"'l_food'":self.screen.ids.l_food,"'l_iron'":self.screen.ids.l_iron,"'house_lvl'":self.screen.ids.house_lvl,
                          "'l_clay'":self.screen.ids.l_clay,"'l_wood'":self.screen.ids.l_wood,"'l_usefood'":self.screen.ids.l_usefood,"'l_attpow'":self.screen.ids.l_attpow,
                          "'unit_lvl'":self.screen.ids.unit_lvl,"'min_in'":self.screen.ids.time_board.ids.min_in,"'hours_in'":self.screen.ids.time_board.ids.hours_in,
                          "'l_unit_name'":self.screen.ids.l_unit_name, "'l_unit_count'":self.screen.ids.l_unit_count,"'l_def_inf'":self.screen.ids.l_def_inf, "'l_def_cav'":self.screen.ids.l_def_cav,
                          "'l_def'": self.screen.ids.l_def}
        db_widgets_title ={"'calc_button'":self.screen.ids.calc_button}
        for key, values in db_widgets_text.items():
            q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(st_language, key)
            cursor.execute(q)
            new_text = cursor.fetchone()[0]
            values.text = new_text
        for key, values in db_widgets_title.items():
            q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(st_language, key)
            cursor.execute(q)
            values.title = cursor.fetchone()[0]
        conn.close()
        
        self.menu_nation = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.nation_button, items=[{ "text": str(i) } for i in self.items_nation],
                                          use_icon_item = False,position="bottom", width_mult=2, callback = self.set_nation)
        self.menu_house_lvl = MDDropdownMenu(caller=self.screen.ids.house_lvl, items=[{ "text": str(i) } for i in range(21)],width_mult=3,
                                             callback=self.set_houselvl,position="bottom",use_icon_item = False,)
        self.menu_unit_lvl = MDDropdownMenu(caller=self.screen.ids.unit_lvl, items=[{ "text": str(i) } for i in range(21)],width_mult=3,
                                            callback=self.set_unitlvl,position="bottom",use_icon_item = False,)
        self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.item_units],
                                        width_mult=3,position="bottom",use_icon_item = False,)
        self.menu_bonus_aliance = MDDropdownMenu(caller=self.screen.ids.bonus_aliance, items=[{ "text": str(i) } for i in self.items_bonus_aliance],
                                                 width_mult=3,position="bottom",use_icon_item = False,)
        self.menu_bonus_artefact = MDDropdownMenu(caller=self.screen.ids.bonus_artefact, items=[{ "text": str(i) } for i in self.items_bonus_artefact],
                                                  width_mult=3,position="bottom",use_icon_item = False,)
        self.menu_bonus_helmet = MDDropdownMenu(caller=self.screen.ids.bonus_helmet, items=[{ "text": str(i) } for i in self.items_bonus_helmet],
                                                width_mult=3,position="bottom",use_icon_item = False,)
        self.menu_hours = MDDropdownMenu(caller=self.screen.ids.time_board.ids.hours_in, items=[{ "text": str(i) + '\n' + self.screen.ids.time_board.ids.hours_in.text } for i in range(73)],width_mult=2,callback=self.set_hours,
                                         position="bottom",use_icon_item = False,)
        self.menu_min = MDDropdownMenu(caller=self.screen.ids.time_board.ids.min_in, items=[{ "text": str(i) + '\n' + self.screen.ids.time_board.ids.min_in.text } for i in range(60)],width_mult=2,
                                       callback=self.set_min, position="bottom",use_icon_item = False,)
    def set_hours(self, instance):
        def set_hours(interval):
            self.screen.ids.time_board.ids.hours_in.text = instance.text
        Clock.schedule_once(set_hours, 0.5)
        
    def set_min(self, instance,):
        print('1')
        def set_min(interval):
            self.screen.ids.time_board.ids.min_in.text = instance.text
        Clock.schedule_once(set_min, 0.5)
        
    def set_nation(self, instance):
        print('1')
        def set_nation(interval):
            self.screen.ids.toolbar.ids.nation_button.text = instance.text
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("UPDATE settings_db SET value = ? WHERE option = 'nation'",(instance.text,))
            conn.commit()
            if instance.text == 'Romans':
                self.screen.ids.toolbar.ids.nation_icon.source = 'datas/ROMANS_s.png'
                self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.romans_units],width_mult=3,position="bottom",use_icon_item = False,)
                self.screen.ids.toolbar.ids.unit_button.text = self.romans_units[0]
            elif instance.text == 'Teutons':
                self.screen.ids.toolbar.ids.nation_icon.source = 'datas/TEUTONS_s.png'
                self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.teutons_units],width_mult=3,position="bottom",use_icon_item = False,)
                self.screen.ids.toolbar.ids.unit_button.text = self.teutons_units[0]
            elif instance.text == "Gauls":
                self.screen.ids.toolbar.ids.nation_icon.source = 'datas/GAULS_s.png'
                self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.gauls_units],width_mult=3,position="bottom",use_icon_item = False,)
                self.screen.ids.toolbar.ids.unit_button.text = self.gauls_units[0]
        Clock.schedule_once(set_nation, 0.5)
        
    def set_houselvl(self, instance):
        def set_houselvl(interval):
            self.screen.ids.house_lvl.text = instance.text  
        Clock.schedule_once(set_houselvl, 0.5)
        
    def set_unitlvl(self, instance):
        def set_unitlvl(interval):
            self.screen.ids.unit_lvl.text = instance.text
        Clock.schedule_once(set_unitlvl, 0.5)
        
    def build(self):
        Window.size = (450,810)
        return self.screen
    
    def calc_func(self):
        def change_info(interval):
            self.screen.ids.l_food.text = '0'
        Clock.schedule_once(change_info, 0.5)
        
    def change_language_in(self,language):
        def update_screen(interval):
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("UPDATE settings_db SET value = ? WHERE option = 'language'",(language,))
            conn.commit()
            db_widgets_text = {"'nation_button'" : self.screen.ids.toolbar.ids.nation_button,"'unit_button'":self.screen.ids.toolbar.ids.unit_button,"'house_lvl'": self.screen.ids.house_lvl,
                          "'l_res'":self.screen.ids.l_res,"'l_food'":self.screen.ids.l_food,"'l_iron'":self.screen.ids.l_iron,"'house_lvl'":self.screen.ids.house_lvl,
                          "'l_clay'":self.screen.ids.l_clay,"'l_wood'":self.screen.ids.l_wood,"'l_usefood'":self.screen.ids.l_usefood,"'l_attpow'":self.screen.ids.l_attpow,
                          "'unit_lvl'":self.screen.ids.unit_lvl,"'min_in'":self.screen.ids.time_board.ids.min_in,"'hours_in'":self.screen.ids.time_board.ids.hours_in,
                          "'l_unit_name'":self.screen.ids.l_unit_name, "'l_unit_count'":self.screen.ids.l_unit_count,"'l_def_inf'":self.screen.ids.l_def_inf, "'l_def_cav'":self.screen.ids.l_def_cav,
                          "'l_def'": self.screen.ids.l_def}
            db_widgets_title ={"'calc_button'":self.screen.ids.calc_button}
            for key, values in db_widgets_text.items():
                q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(language, key)
                cursor.execute(q)
                print(cursor.fetchone()[0])
                new_text = cursor.fetchone()[0]
                values.text = new_text
            for key, values in db_widgets_title.items():
                q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(language, key)
                cursor.execute(q)
                values.title = cursor.fetchone()[0]
            conn.close()
        Clock.schedule_once(update_screen,0.5)
        
Test().run()
