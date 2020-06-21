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
Clock.max_iteration = 20
class LanguageImage(CircularRippleBehavior, ButtonBehavior, Image):
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
        if self.st_nation in ["Gauls",'Галлы','Галли']:
            self.screen.ids.toolbar.ids.unit_button.text = self.gauls_units[0]
            self.screen.ids.toolbar.ids.nation_button.text = self.items_nation[0]
            self.item_units = self.gauls_units
            self.screen.ids.toolbar.ids.nation_icon.source = "datas/GAULS_s.png"
        elif self.st_nation in ['Teutons','Германцы','Германці']:
            self.screen.ids.toolbar.ids.unit_button.text = self.teutons_units[0]
            self.screen.ids.toolbar.ids.nation_button.text = self.items_nation[2]
            self.item_units = self.teutons_units
            self.screen.ids.toolbar.ids.nation_icon.source = "datas/TEUTONS_s.png"
        elif self.st_nation in ['Romans','Римляни','Римляне']:
            self.screen.ids.toolbar.ids.unit_button.text = self.romans_units[0]
            self.screen.ids.toolbar.ids.nation_button.text = self.items_nation[1]
            self.item_units = self.romans_units
            self.screen.ids.toolbar.ids.nation_icon.source = "datas/ROMANS_s.png"
        db_widgets_text = {"'l_res'":self.screen.ids.l_res,"'l_food'":self.screen.ids.l_food,"'l_iron'":self.screen.ids.l_iron,"'house_lvl'":self.screen.ids.house_lvl,
                          "'unit_button'":self.screen.ids.toolbar.ids.unit_button,
                          "'artifact'":self.screen.ids.bonus_artefact,"'helmet'":self.screen.ids.bonus_helmet,"'aliance'":self.screen.ids.bonus_aliance,
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
        self.menu_house_lvl = MDDropdownMenu(caller=self.screen.ids.house_lvl, items=[{ "text": str(i) } for i in range(1,21)],width_mult=3,
                                             callback=self.set_houselvl,position="bottom",use_icon_item = False,)
        self.menu_unit_lvl = MDDropdownMenu(caller=self.screen.ids.unit_lvl, items=[{ "text": str(i) } for i in range(21)],width_mult=3,
                                            callback=self.set_unitlvl,position="bottom",use_icon_item = False,)
        self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.item_units],
                                        width_mult=3,position="bottom",use_icon_item = False, callback = self.set_unit)
        self.menu_bonus_aliance = MDDropdownMenu(caller=self.screen.ids.bonus_aliance, items=[{ "text": str(i) } for i in self.items_bonus_aliance],
                                                 width_mult=3,position="bottom",use_icon_item = False,callback = self.set_aliance)
        self.menu_bonus_artefact = MDDropdownMenu(caller=self.screen.ids.bonus_artefact, items=[{ "text": str(i) } for i in self.items_bonus_artefact],
                                                  width_mult=3,position="bottom",use_icon_item = False,callback = self.set_artifact)
        self.menu_bonus_helmet = MDDropdownMenu(caller=self.screen.ids.bonus_helmet, items=[{ "text": str(i) } for i in self.items_bonus_helmet],
                                                width_mult=3,position="bottom",use_icon_item = False,callback = self.set_helmet)
        self.menu_hours = MDDropdownMenu(caller=self.screen.ids.time_board.ids.hours_in, items=[{ "text": str(i) + '\n' + self.screen.ids.time_board.ids.hours_in.text } for i in range(73)],width_mult=2,callback=self.set_hours,
                                         position="bottom",use_icon_item = False,)
        self.menu_min = MDDropdownMenu(caller=self.screen.ids.time_board.ids.min_in, items=[{ "text": str(i) + '\n' + self.screen.ids.time_board.ids.min_in.text } for i in range(60)],width_mult=2,
                                       callback=self.set_min, position="bottom",use_icon_item = False,)
    def set_hours(self, instance):
        def set_hours(interval):
            self.screen.ids.time_board.ids.hours_in.text = instance.text
        Clock.schedule_once(set_hours, 0.05)
        
    def set_min(self, instance,):
        def set_min(interval):
            self.screen.ids.time_board.ids.min_in.text = instance.text
        Clock.schedule_once(set_min, 0.05)
    def set_unit(self, instance):
        def set_unit(interval):
            self.screen.ids.toolbar.ids.unit_button.text = instance.text
        Clock.schedule_once(set_unit, 0.05)   

    def set_nation(self, instance):
        def set_nation(interval):
            self.screen.ids.toolbar.ids.nation_button.text = instance.text
            if instance.text in ['Romans','Римляни','Римляне']:
                self.screen.ids.toolbar.ids.nation_icon.source = 'datas/ROMANS_s.png'
                self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.romans_units],width_mult=3,position="bottom",use_icon_item = False, callback = self.set_unit)
                self.screen.ids.toolbar.ids.unit_button.text = self.romans_units[0]
            elif instance.text in ['Teutons','Германцы','Германці']:
                self.screen.ids.toolbar.ids.nation_icon.source = 'datas/TEUTONS_s.png'
                self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.teutons_units],width_mult=3,position="bottom",use_icon_item = False, callback = self.set_unit)
                self.screen.ids.toolbar.ids.unit_button.text = self.teutons_units[0]
            elif instance.text in ["Gauls",'Галлы','Галли']:
                self.screen.ids.toolbar.ids.nation_icon.source = 'datas/GAULS_s.png'
                self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": str(i) } for i in self.gauls_units],width_mult=3,position="bottom",use_icon_item = False, callback = self.set_unit)
                self.screen.ids.toolbar.ids.unit_button.text = self.gauls_units[0]
        Clock.schedule_once(set_nation, 0)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE settings_db SET value = ? WHERE option = 'nation'",(instance.text,))
        conn.commit()
    def set_aliance(self, instance):
        def set_aliance(interval):
            self.screen.ids.bonus_aliance.text = instance.text  
        Clock.schedule_once(set_aliance, 0.05)
    def set_helmet(self, instance):
        def set_helmet(interval):
            self.screen.ids.bonus_helmet.text = instance.text  
        Clock.schedule_once(set_helmet, 0.05)
    def set_artifact(self, instance):
        def set_artifact(interval):
            self.screen.ids.bonus_artefact.text = instance.text  
        Clock.schedule_once(set_artifact, 0.05)
    def set_houselvl(self, instance):
        def set_houselvl(interval):
            self.screen.ids.house_lvl.text = instance.text  
        Clock.schedule_once(set_houselvl, 0.05)     
    def set_unitlvl(self, instance):
        def set_unitlvl(interval):
            self.screen.ids.unit_lvl.text = instance.text
        Clock.schedule_once(set_unitlvl, 0.05)
        
    def build(self):
        Window.size = (500,810)
        return self.screen
    
    def calc_func(self):
        house_time_reduce = {1:1,2:0.9,3:0.81,4:0.729,5:0.6561,6:0.5905,7:0.5314,8:0.4783,9:0.4305,10:0.3874,11:0.3487,12:0.3138,13:0.2824,14:0.2542,15:0.2288,16:0.2059,17:0.1853,18:0.1668,19:0.1501,20:0.1351}
        house_lvl = re.match(r'\d{2}',self.screen.ids.house_lvl.text) or re.match(r'\d{1}',self.screen.ids.house_lvl.text)
        unit_lvl = re.match(r'\d{2}',self.screen.ids.unit_lvl.text) or re.match(r'\d{1}',self.screen.ids.unit_lvl.text)
        if self.screen.ids.toolbar.ids.nation_button.text in ['Choose nation','Выберите нацию','Виберіть народ']:
            return print('choose unit')
        if self.screen.ids.toolbar.ids.unit_button.text in ['Choose unit','Выбери воина','Вибери воїна']:
            return print('choose unit')
        if house_lvl:
            house_lvl = house_lvl.group(0)
        else:
            return print('choose house lvl')
        if unit_lvl:
            unit_lvl = int(unit_lvl.group(0))
        else:
            print('your unit lvl is 0')
            unit_lvl = 0
        
        craft_time_min = re.match(r'\d{2}',self.screen.ids.time_board.ids.min_in.text) or re.match(r'\d{1}',self.screen.ids.time_board.ids.min_in.text)
        craft_time_hours = re.match(r'\d{2}',self.screen.ids.time_board.ids.hours_in.text) or re.match(r'\d{1}',self.screen.ids.time_board.ids.hours_in.text)
        if craft_time_min:
            craft_time_min = int(craft_time_min.group(0))
        else: 
            craft_time_min = 0
        if craft_time_hours:
            craft_time_hours = int(craft_time_hours.group(0))
        else: craft_time_hours = 0

        craft_time = 60 * int(craft_time_min) + 3600 * int(craft_time_hours)
        total_bonus = 1
        b_aliance = re.match(r'\d{2}',self.screen.ids.bonus_aliance.text) or re.match(r'\d{1}',self.screen.ids.bonus_aliance.text)
        if b_aliance:
            total_bonus -= int(b_aliance.group(0))*0.01

        b_artefact = re.match(r'\d{2}',self.screen.ids.bonus_artefact.text) or re.match(r'\d{1}',self.screen.ids.bonus_artefact.text)
        if b_artefact:
            total_bonus -= int(b_artefact.group(0))*0.01
        
        b_helmet = re.match(r'\d{2}',self.screen.ids.bonus_helmet.text) or re.match(r'\d{1}',self.screen.ids.bonus_helmet.text)
        if b_helmet:
            total_bonus -= int(b_helmet.group(0))*0.01


        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        if self.screen.ids.toolbar.ids.nation_button.text in ["Gauls",'Галлы','Галли']:
            q = "SELECT type,training_time,traning_wood,training_clay,training_iron,training_crop,use_crop,def_inf,def_cav,att_power,unit_name FROM unit_db WHERE unit_id = {0}".format('1'+str(self.menu_unit.items.index({"text": self.screen.ids.toolbar.ids.unit_button.text })))
            cursor.execute(q)
            info = cursor.fetchone()
            print(info)

        elif self.screen.ids.toolbar.ids.nation_button.text in ['Teutons','Германцы','Германці']:
            q = "SELECT type,training_time,traning_wood,training_clay,training_iron,training_crop,use_crop,def_inf,def_cav,att_power,unit_name FROM unit_db WHERE unit_id = {0}".format('3'+str(self.menu_unit.items.index({"text": self.screen.ids.toolbar.ids.unit_button.text })))
            cursor.execute(q)
            info = cursor.fetchone()
            print(info)

        elif self.screen.ids.toolbar.ids.nation_button.text in ['Romans','Римляни','Римляне']:
            q = "SELECT type,training_time,traning_wood,training_clay,training_iron,training_crop,use_crop,def_inf,def_cav,att_power,unit_name FROM unit_db WHERE unit_id = {0}".format('2'+str(self.menu_unit.items.index({"text": self.screen.ids.toolbar.ids.unit_button.text })))
            cursor.execute(q)
            info = cursor.fetchone()
            print(info)
        else:
            return print('choose nation')
        one_unit_time = int(info[1]*house_time_reduce[int(house_lvl)]*total_bonus)
        count_of_unit = int(int(craft_time)/int(one_unit_time))


        print(str(one_unit_time) + ' one unit time ' )
        print(unit_lvl)
        print(str(craft_time) + ' sekund')
        print(str(total_bonus) + 'total bonus')
        def change_info(interval):
            self.screen.ids.l_unit_name.text = str(info[10])
            self.screen.ids.i_unit_count.text ='{0:,}'.format(count_of_unit).replace(',', ' ')
            self.screen.ids.i_def_inf.text = '{0:,}'.format(info[7]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_def_cav.text ='{0:,}'.format(info[8]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_def.text = '{0:,}'.format(info[8]*count_of_unit + info[7]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_attpow.text = '{0:,}'.format(info[9]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_usefood.text = '{0:,}'.format(info[6]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_wood.text = '{0:,}'.format(info[2]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_clay.text = '{0:,}'.format(info[3]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_iron.text = '{0:,}'.format(info[4]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_food.text ='{0:,}'.format(info[5]*count_of_unit).replace(',', ' ')
            self.screen.ids.i_res.text = '{0:,}'.format(info[5]*count_of_unit + info[3]*count_of_unit + info[4]*count_of_unit + info[2]*count_of_unit).replace(',', ' ')
        Clock.schedule_once(change_info, 0.05)
        
    def change_language_in(self,language):
        def update_screen(interval):
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute("UPDATE settings_db SET value = ? WHERE option = 'language'",(language,))
            conn.commit()
            widget_menu = ["'units_gauls'","'units_teutons'","'units_romans'","'bonus_helmet'","'items_nation'","'bonus_artefact'","'bonus_aliance'"]
            db_widgets_texts = {"'nation_button'" : self.screen.ids.toolbar.ids.nation_button,"'unit_button'":self.screen.ids.toolbar.ids.unit_button,
                          "'artifact'":self.screen.ids.bonus_artefact,"'helmet'":self.screen.ids.bonus_helmet,"'aliance'":self.screen.ids.bonus_aliance,
                          "'l_res'":self.screen.ids.l_res,"'l_food'":self.screen.ids.l_food,"'l_iron'":self.screen.ids.l_iron,"'house_lvl'":self.screen.ids.house_lvl,
                          "'l_clay'":self.screen.ids.l_clay,"'l_wood'":self.screen.ids.l_wood,"'l_usefood'":self.screen.ids.l_usefood,"'l_attpow'":self.screen.ids.l_attpow,
                          "'unit_lvl'":self.screen.ids.unit_lvl,"'min_in'":self.screen.ids.time_board.ids.min_in,"'hours_in'":self.screen.ids.time_board.ids.hours_in,
                          "'l_unit_name'":self.screen.ids.l_unit_name, "'l_unit_count'":self.screen.ids.l_unit_count,"'l_def_inf'":self.screen.ids.l_def_inf, "'l_def_cav'":self.screen.ids.l_def_cav,
                          "'l_def'": self.screen.ids.l_def}
            db_widgets_titles ={"'calc_button'":self.screen.ids.calc_button}
            for key, values in db_widgets_texts.items():
                q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(language, key)
                cursor.execute(q)
                new_text = cursor.fetchone()
                if new_text is not None:
                    values.text = new_text[0]
                else: print('here was none {0}'.format(key))
            for key, values in db_widgets_titles.items():
                q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(language, key)
                cursor.execute(q)
                values.title = cursor.fetchone()[0]
            empty = []
            for key in widget_menu:
                q = "SELECT {0} FROM language_db WHERE widget_id = {1}".format(language, key)
                cursor.execute(q)
                a = cursor.fetchone()[0]
                a = a.split(",")
                empty.append(a)
            
            self.gauls_units, self.teutons_units, self.romans_units, self.items_bonus_helmet, self.items_nation, self.items_bonus_artefact, self.items_bonus_aliance = empty[0],empty[1],empty[2],empty[3],empty[4],empty[5],empty[6]
            self.menu_nation = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.nation_button, items=[{ "text": str(i) } for i in self.items_nation],
                                          use_icon_item = False,position="bottom", width_mult=2, callback = self.set_nation)
            self.menu_house_lvl = MDDropdownMenu(caller=self.screen.ids.house_lvl, items=[{ "text": str(i) } for i in range(1,21)],width_mult=3,
                                             callback=self.set_houselvl,position="bottom",use_icon_item = False,)
            self.menu_unit_lvl = MDDropdownMenu(caller=self.screen.ids.unit_lvl, items=[{ "text": str(i) } for i in range(21)],width_mult=3,
                                            callback=self.set_unitlvl,position="bottom",use_icon_item = False,)
            self.menu_unit = MDDropdownMenu(caller=self.screen.ids.toolbar.ids.unit_button,items = [{ "text": '' }],width_mult=3,position="bottom",use_icon_item = False, callback = self.set_unit)
            self.menu_bonus_aliance = MDDropdownMenu(caller=self.screen.ids.bonus_aliance, items=[{ "text": str(i) } for i in self.items_bonus_aliance],
                                                 width_mult=3,position="bottom",use_icon_item = False,callback = self.set_aliance)
            self.menu_bonus_artefact = MDDropdownMenu(caller=self.screen.ids.bonus_artefact, items=[{ "text": str(i) } for i in self.items_bonus_artefact],
                                                  width_mult=3,position="bottom",use_icon_item = False,callback = self.set_artifact)
            self.menu_bonus_helmet = MDDropdownMenu(caller=self.screen.ids.bonus_helmet, items=[{ "text": str(i) } for i in self.items_bonus_helmet],
                                                width_mult=3,position="bottom",use_icon_item = False,callback = self.set_helmet)
            self.menu_hours = MDDropdownMenu(caller=self.screen.ids.time_board.ids.hours_in, items=[{ "text": str(i) + '\n' + self.screen.ids.time_board.ids.hours_in.text } for i in range(73)],width_mult=2,callback=self.set_hours,
                                         position="bottom",use_icon_item = False,)
            self.menu_min = MDDropdownMenu(caller=self.screen.ids.time_board.ids.min_in, items=[{ "text": str(i) + '\n' + self.screen.ids.time_board.ids.min_in.text } for i in range(60)],width_mult=2,
                                       callback=self.set_min, position="bottom",use_icon_item = False,)
            conn.close()
        Clock.schedule_once(update_screen,0.05)
        
Test().run()
