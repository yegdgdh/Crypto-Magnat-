from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
import json, os, random, time

# ПАТЧ ДЛЯ АНДРОИДА (чтобы сохранения работали в APK)
from kivy.utils import platform
if platform == 'android':
    from android.storage import app_storage_path
    SAVE_FILE = os.path.join(app_storage_path(), "crypto_save.json")
else:
    SAVE_FILE = "crypto_save.json"

Window.clearcolor = (0.05, 0.05, 0.1, 1)

LOCATIONS = [
    {"name": "Общага", "cost": 0, "mult": 1.0, "bg": (0.2, 0.15, 0.1, 1), "bonus_type": "none", "bonus_val": 0, "desc": "Стартовая локация"},
    {"name": "Гараж", "cost": 3000, "mult": 1.5, "bg": (0.3, 0.1, 0.05, 1), "bonus_type": "click", "bonus_val": 0.1, "desc": "+10% к силе клика"},
    {"name": "Офис", "cost": 60000, "mult": 2.5, "bg": (0.1, 0.2, 0.4, 1), "bonus_type": "passive", "bonus_val": 0.1, "desc": "+10% к пассиву"},
    {"name": "Дата-Центр", "cost": 1500000, "mult": 4.0, "bg": (0.2, 0.05, 0.3, 1), "bonus_type": "btc", "bonus_val": 0.1, "desc": "+10% к курсу BTC"},
    {"name": "Крипто-город", "cost": 50000000, "mult": 7.0, "bg": (0.3, 0.2, 0.05, 1), "bonus_type": "all", "bonus_val": 0.2, "desc": "+20% ко всему"},
]

ITEMS = [
    {"name": "GTX 1060", "price": 50, "bps": 1, "qty": 0, "type": "bps"},
    {"name": "RTX 3080", "price": 500, "bps": 10, "qty": 0, "type": "bps"},
    {"name": "RTX 4090", "price": 5000, "bps": 100, "qty": 0, "type": "bps"},
    {"name": "ASIC S19", "price": 25000, "bps": 500, "qty": 0, "type": "bps"},
    {"name": "Ферма", "price": 500000, "bps": 5000, "qty": 0, "type": "bps"},
    {"name": "Автокликер", "price": 1000000, "bps": 10, "qty": 0, "type": "autoclick"},
]

ACHIEVEMENTS = [
    {"id": "click100", "name": "100 кликов", "req_type": "clicks", "req": 100, "done": False},
    {"id": "earn1k", "name": "Заработал 1K", "req_type": "total", "req": 1000, "done": False},
    {"id": "earn1m", "name": "Первый миллион", "req_type": "total", "req": 1000000, "done": False},
    {"id": "loc2", "name": "Переезд в гараж", "req_type": "loc", "req": 1, "done": False},
]

BOTS = [
    {"name": "Сатоши Н.", "score": 50000000, "grow": 3000},
    {"name": "Илон Маск", "score": 25000000, "grow": 2000},
    {"name": "Крипто-Кит", "score": 10000000, "grow": 1000},
    {"name": "Хакер 2000", "score": 5000000, "grow": 600},
    {"name": "Крипто-Барон", "score": 3000000, "grow": 400},
    {"name": "Дядя Ваня", "score": 2000000, "grow": 250},
    {"name": "Студент", "score": 1000000, "grow": 150},
    {"name": "Шахтер", "score": 500000, "grow": 100},
    {"name": "Майнер 999", "score": 250000, "grow": 70},
    {"name": "Новичок", "score": 100000, "grow": 40},
    {"name": "Школьник", "score": 50000, "grow": 20},
    {"name": "Чайник", "score": 10000, "grow": 10},
]

class SceneBackground(Widget):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *args):
        self.canvas.clear()
        if self.width == 0: return
        w, h = self.width, self.height
        bg_color = LOCATIONS[self.app.loc_idx]["bg"]
        with self.canvas:
            Color(*bg_color)
            Rectangle(pos=self.pos, size=self.size)
            Color(bg_color[0]+0.1, bg_color[1]+0.1, bg_color[2]+0.1, 0.5)
            Ellipse(pos=(w*0.1, h*0.6), size=(w*0.4, w*0.4))
            Ellipse(pos=(w*0.6, h*0.1), size=(w*0.5, w*0.5))

class Coin(Widget):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.bind(pos=self.draw, size=self.draw)
        self.label = Label(text="B", font_size="100sp", bold=True, color=(1, 0.9, 0.2, 1))
        self.add_widget(self.label)
        
    def draw(self, *args):
        self.canvas.clear()
        if self.width == 0: return
        with self.canvas:
            Color(0, 0, 0, 0.6)
            Ellipse(pos=(self.x+5, self.y-10), size=self.size)
            Color(0.6, 0.4, 0, 1)
            Ellipse(pos=self.pos, size=self.size)
            Color(1, 0.85, 0, 1)
            Ellipse(pos=(self.x+5, self.y+5), size=(self.width-10, self.height-10))
            Color(1, 1, 0.5, 0.5)
            Ellipse(pos=(self.x+self.width*0.2, self.y+self.height*0.6), size=(self.width/3, self.height/3))
        self.label.font_size = f"{int(self.width/2.5)}sp"
        self.label.pos = (self.center_x - self.label.width/2, self.center_y - self.label.height/2)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.app.on_click()
            self.opacity = 0.8
            return True
        return super().on_touch_down(touch)
        
    def on_touch_up(self, touch):
        self.opacity = 1
        return super().on_touch_up(touch)

class CryptoApp(App):
    def build(self):
        self.balance = 0.0
        self.total = 0.0
        self.loc_idx = 0
        self.prestige = 1.0
        self.tab = "shop"
        self.btc_rate = 1.0
        self.boost = 0
        self.total_clicks = 0
        self.buy_count = 0
        self.last_time = time.time()
        self.player_name = "Игрок"
        self.load()
        
        self.root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        top = BoxLayout(size_hint_y=0.12, orientation="horizontal", spacing=10)
        self.bal_lbl = Label(text="0 B", font_size="24sp", color=(0.4, 1, 0.4, 1), bold=True)
        self.rate_lbl = Label(text="BTC x1.0", font_size="14sp", color=(1, 0.8, 0.2, 1))
        self.boost_btn = Button(text="x2", size_hint_x=0.25, background_color=(0.8, 0.2, 0.2, 1))
        self.boost_btn.bind(on_press=self.activate_boost)
        top.add_widget(self.bal_lbl); top.add_widget(self.rate_lbl); top.add_widget(self.boost_btn)
        self.root.add_widget(top)
        
        self.scene_float = FloatLayout(size_hint_y=0.55)
        self.bg = SceneBackground(self)
        self.bg.size_hint = (1, 1)
        self.scene_float.add_widget(self.bg)
        self.coin = Coin(self, size_hint=(None, None))
        self.scene_float.add_widget(self.coin)
        self.scene_float.bind(size=self.size_coin)
        self.root.add_widget(self.scene_float)
        
        tabs = BoxLayout(size_hint_y=0.08, spacing=2)
        colors = [(0.2, 0.5, 0.8, 1), (0.8, 0.5, 0.2, 1), (0.8, 0.2, 0.8, 1), (0.2, 0.8, 0.4, 1), (0.8, 0.8, 0.2, 1), (0.9, 0.4, 0.1, 1), (1, 0.3, 0.3, 1)]
        names = [("shop", "МАГ"), ("loc", "ЛОК"), ("prestige", "ПРЕС"), ("achiev", "ДОСТ"), ("stats", "СТАТ"), ("rank", "РЕЙТ"), ("farm", "ФЕРМА")]
        
        for (t, txt), color in zip(names, colors):
            b = Button(text=txt, background_color=color, bold=True, font_size="10sp")
            b.bind(on_press=lambda x, tab=t: self.switch(tab))
            tabs.add_widget(b)
        self.root.add_widget(tabs)
        
        self.scroll = ScrollView(size_hint_y=0.25)
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.root.add_widget(self.scroll)
        
        self.switch("shop")
        
        Clock.schedule_interval(self.autoclick, 1.0)
        Clock.schedule_interval(self.passive, 1.0)
        Clock.schedule_interval(self.update_rate, 8.0)
        Clock.schedule_interval(self.save, 15.0)
        Clock.schedule_interval(self.bots_grow, 1.0)
        Clock.schedule_once(lambda dt: self.size_coin(), 0)
        return self.root

    def get_loc_bonus(self, btype):
        loc = LOCATIONS[self.loc_idx]
        if loc["bonus_type"] == btype:
            return 1.0 + loc["bonus_val"]
        if loc["bonus_type"] == "all":
            return 1.0 + loc["bonus_val"]
        return 1.0

    def autoclick(self, dt):
        auto_qty = 0
        for i in ITEMS:
            if i["type"] == "autoclick": auto_qty += i["qty"]
        if auto_qty > 0:
            gain = self.total_bps() * 0.01 * auto_qty
            self.balance += gain
            self.total += gain

    def bots_grow(self, dt):
        for b in BOTS: b["score"] += b["grow"] * dt

    def is_first_place(self):
        for b in BOTS:
            if b["score"] > self.total: return False
        return True

    def show_toast(self, msg):
        toast = Label(text=msg, font_size="14sp", color=(1, 1, 0.5, 1), size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'top': 0.98})
        with toast.canvas.before:
            Color(0, 0, 0, 0.8)
            Rectangle(pos=toast.pos, size=toast.size)
        self.root.add_widget(toast)
        Clock.schedule_once(lambda dt: self.root.remove_widget(toast) if toast.parent else None, 2.5)

    def size_coin(self, *args):
        w = self.scene_float.width
        h = self.scene_float.height
        if w == 0 or h == 0: return
        s = min(w, h) * 0.95
        if s > 450: s = 450
        self.coin.size = (s, s)
        y_pos = h * 1.0 - s / 2
        self.coin.pos = (w / 2 - s / 2, y_pos)

    def total_bps(self):
        base = sum(i["bps"] * i["qty"] for i in ITEMS if i["type"] == "bps")
        return base * LOCATIONS[self.loc_idx]["mult"] * self.prestige * self.btc_rate * self.get_boost() * self.get_loc_bonus("passive")

    def switch(self, tab):
        self.tab = tab
        self.grid.clear_widgets()
        
        if tab == "shop":
            for item in ITEMS:
                row = BoxLayout(size_hint_y=None, height=60, spacing=5)
                row.add_widget(Label(text=item["name"], font_size="14sp"))
                b = Button(text=f"{int(item['price'])} B", size_hint_x=0.4, background_color=(0.2, 0.6, 0.2, 1))
                b.bind(on_press=lambda x, i=item: self.buy(i))
                row.add_widget(b)
                self.grid.add_widget(row)
                
        elif tab == "loc":
            for i, loc in enumerate(LOCATIONS):
                card = BoxLayout(size_hint_y=None, height=70, spacing=5, padding=5)
                info = BoxLayout(orientation="vertical")
                info.add_widget(Label(text=loc["name"], font_size="15sp", bold=True))
                info.add_widget(Label(text=loc["desc"], font_size="11sp", color=(0.8, 0.8, 1, 1)))
                card.add_widget(info)
                
                if i > self.loc_idx:
                    b = Button(text=f"{int(loc['cost'])} B", size_hint_x=0.35, background_color=(0.8, 0.4, 0.1, 1))
                    b.bind(on_press=lambda x, idx=i: self.move(idx))
                    card.add_widget(b)
                elif i == self.loc_idx:
                    card.add_widget(Label(text="ТУТ", color=(0.4, 1, 0.4, 1), bold=True, size_hint_x=0.35))
                else:
                    card.add_widget(Label(text="ОТКРЫТО", color=(0.5, 0.5, 0.5, 1), size_hint_x=0.35))
                self.grid.add_widget(card)
                
        elif tab == "prestige":
            row = BoxLayout(size_hint_y=None, height=80)
            if self.total >= 1000000:
                b = Button(text=f"ПРЕСТИЖ +10%\nТекущий x{self.prestige:.1f}", background_color=(0.8, 0.2, 0.8, 1))
                b.bind(on_press=lambda x: self.do_prestige())
                row.add_widget(b)
            else:
                row.add_widget(Label(text=f"Нужно 1,000,000 B\nСейчас: {int(self.total)}", font_size="14sp"))
            self.grid.add_widget(row)
            
        elif tab == "achiev":
            for ach in ACHIEVEMENTS:
                row = BoxLayout(size_hint_y=None, height=50, spacing=5)
                status = "OK" if ach["done"] else "X"
                row.add_widget(Label(text=f"{status} {ach['name']}", font_size="13sp"))
                self.grid.add_widget(row)
                
        elif tab == "stats":
            name_row = BoxLayout(size_hint_y=None, height=60, spacing=5)
            name_row.add_widget(Label(text="Ваш ник:", size_hint_x=0.4, font_size="14sp"))
            self.name_input = TextInput(text=self.player_name, multiline=False, size_hint_x=0.6, font_size="18sp", padding=[10, 10, 10, 10])
            self.name_input.bind(on_text_validate=self.save_name)
            name_row.add_widget(self.name_input)
            self.grid.add_widget(name_row)
            btn_save = Button(text="Сохранить ник", size_hint_y=None, height=40, background_color=(0.2, 0.6, 0.8, 1))
            btn_save.bind(on_press=self.save_name_btn)
            self.grid.add_widget(btn_save)
            row = BoxLayout(size_hint_y=None, height=100, orientation="vertical")
            row.add_widget(Label(text=f"Всего кликов: {self.total_clicks}", font_size="14sp"))
            row.add_widget(Label(text=f"Куплено карт: {self.buy_count}", font_size="14sp"))
            row.add_widget(Label(text=f"Всего заработано: {int(self.total)} B", font_size="14sp"))
            self.grid.add_widget(row)
            
        elif tab == "rank":
            all_players = [(self.player_name, self.total)] + [(b["name"], b["score"]) for b in BOTS]
            all_players.sort(key=lambda x: x[1], reverse=True)
            for i, (name, score) in enumerate(all_players):
                row = BoxLayout(size_hint_y=None, height=45, spacing=5)
                color = (1, 0.8, 0.2, 1) if name == self.player_name else (0.8, 0.8, 0.8, 1)
                medal = "1." if i == 0 else "2." if i == 1 else "3." if i == 2 else ""
                row.add_widget(Label(text=f"{medal}{i+1}. {name}", font_size="13sp", color=color, size_hint_x=0.6))
                row.add_widget(Label(text=f"{self.fmt(score)} B", font_size="13sp", color=color, size_hint_x=0.4))
                self.grid.add_widget(row)
        
        elif tab == "farm":
            if self.is_first_place():
                self.grid.add_widget(Label(text="МОЯ МАЙНИНГ-ФЕРМА", font_size="18sp", color=(1, 0.8, 0.2, 1), bold=True, size_hint_y=None, height=40))
                self.grid.add_widget(Label(text=f"Владелец: {self.player_name}", font_size="14sp", color=(0.8, 0.8, 1, 1), size_hint_y=None, height=30))
                self.grid.add_widget(Label(text="Статус: Работает стабильно", font_size="14sp", color=(0.4, 1, 0.4, 1), size_hint_y=None, height=30))
                self.grid.add_widget(Label(text=f"Стоек: 4 | Карт: {self.buy_count} | ASIC: 8", font_size="14sp", size_hint_y=None, height=30))
            else:
                self.grid.add_widget(Label(text="Ферма откроется,\nкогда вы станете 1 в рейтинге", font_size="16sp", color=(1, 0.5, 0.5, 1)))

        self.update_ui()

    def save_name(self, instance):
        if instance.text.strip():
            self.player_name = instance.text.strip()
            self.show_toast(f"Ник: {self.player_name}")
            self.save()

    def save_name_btn(self, instance):
        if hasattr(self, 'name_input') and self.name_input.text.strip():
            self.player_name = self.name_input.text.strip()
            self.show_toast(f"Ник: {self.player_name}")
            self.save()

    def fmt(self, n):
        if n >= 1e9: return f"{n/1e9:.1f}B"
        if n >= 1e6: return f"{n/1e6:.1f}M"
        if n >= 1e3: return f"{n/1e3:.1f}K"
        return f"{int(n)}"

    def on_click(self):
        gain = 1 * LOCATIONS[self.loc_idx]["mult"] * self.prestige * self.btc_rate * self.get_boost() * self.get_loc_bonus("click")
        self.balance += gain; self.total += gain; self.total_clicks += 1
        if random.random() < 0.03:
            bonus = gain * 10
            self.balance += bonus; self.total += bonus
            self.show_toast(f"ЗОЛОТОЙ КЛИК! +{self.fmt(bonus)} B")
        self.check_achiev()
        self.update_ui()

    def buy(self, item):
        if self.balance >= item["price"]:
            self.balance -= item["price"]; item["qty"] += 1; item["price"] = int(item["price"]*1.15)
            self.buy_count += 1
            self.check_achiev()
            self.switch("shop")

    def move(self, idx):
        if self.balance >= LOCATIONS[idx]["cost"]:
            self.balance -= LOCATIONS[idx]["cost"]; self.loc_idx = idx
            self.bg.draw()
            self.check_achiev()
            self.show_toast(f"Переезд: {LOCATIONS[idx]['name']}!")
            self.switch("loc")

    def do_prestige(self):
        if self.total >= 1000000:
            self.balance = 0; self.total = 0; self.loc_idx = 0; self.prestige += 0.1
            for i in ITEMS: i["qty"] = 0
            self.bg.draw()
            self.switch("prestige")

    def check_achiev(self):
        for ach in ACHIEVEMENTS:
            if ach["done"]: continue
            t = ach["req_type"]
            if t == "clicks" and self.total_clicks >= ach["req"]: ach["done"] = True
            elif t == "total" and self.total >= ach["req"]: ach["done"] = True
            elif t == "loc" and self.loc_idx >= ach["req"]: ach["done"] = True

    def activate_boost(self, *args):
        if time.time() > self.boost: self.boost = time.time() + 60

    def get_boost(self): return 2.0 if time.time() < self.boost else 1.0
    def update_rate(self, dt): 
        self.btc_rate = random.uniform(0.8, 1.5) * self.get_loc_bonus("btc")

    def passive(self, dt):
        bps = self.total_bps()
        if bps > 0:
            self.balance += bps; self.total += bps
            self.update_ui()

    def update_ui(self):
        self.bal_lbl.text = f"{int(self.balance)} B"
        self.rate_lbl.text = f"BTC x{self.btc_rate:.1f}"
        if time.time() < self.boost: 
            self.boost_btn.text = f"{int(self.boost-time.time())}s"
            self.boost_btn.background_color = (0.2, 0.8, 0.2, 1)
        else: 
            self.boost_btn.text = "x2"
            self.boost_btn.background_color = (0.8, 0.2, 0.2, 1)

    def save(self, dt=None):
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump({"b": self.balance, "t": self.total, "l": self.loc_idx, "p": self.prestige, "clicks": self.total_clicks, "buys": self.buy_count, "name": self.player_name, "i": [{"q": x["qty"], "p": x["price"]} for x in ITEMS], "time": time.time(), "bots": [{"n": b["name"], "s": b["score"]} for b in BOTS]}, f)
        except: pass

    def load(self):
        if not os.path.exists(SAVE_FILE): return
        try:
            with open(SAVE_FILE) as f: d = json.load(f)
            self.balance = d.get("b", 0); self.total = d.get("t", 0)
            self.loc_idx = d.get("l", 0); self.prestige = d.get("p", 1.0)
            self.total_clicks = d.get("clicks", 0); self.buy_count = d.get("buys", 0)
            self.player_name = d.get("name", "Игрок")
            self.last_time = d.get("time", time.time())
            for i, it in enumerate(d.get("i", [])):
                if i < len(ITEMS): ITEMS[i]["qty"] = it["q"]; ITEMS[i]["price"] = it["p"]
            saved_bots = d.get("bots", [])
            for sb in saved_bots:
                for b in BOTS:
                    if b["name"] == sb["n"]: b["score"] = sb["s"]
        except: pass

    def on_stop(self): self.save()

if __name__ == "__main__":
    CryptoApp().run()
