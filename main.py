from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
import calculations # استيراد ملف العقل الحسابي

# إعدادات خلفية التطبيق
Window.clearcolor = (0.05, 0.07, 0.1, 1)

class AstroInterface(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_pos = 'bottom_mid' # التبويبات في الأسفل كأغلب تطبيقات الموبايل
        self.engine = calculations.HassanAstroWhitePro()
        
        # --- التبويب الأول: لوحة التحكم الكونية ---
        self.tab1 = TabbedPanelItem(text=self.engine.fx("الرئيسية"))
        layout1 = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # منطقة الإدخال الجغرافي
        geo_box = BoxLayout(size_hint_y=None, height=120, spacing=5)
        self.city_in = TextInput(hint_text=self.engine.fx("المدينة"), multiline=False, font_name="arial.ttf")
        btn_geo = Button(text="🌍", size_hint_x=0.2, background_color=(0.06, 0.72, 0.5, 1))
        btn_geo.bind(on_press=self.run_city_search)
        geo_box.add_widget(btn_geo); geo_box.add_widget(self.city_in)
        layout1.add_widget(geo_box)

        # القائمة الجانبية (Sidebar) مدمجة في الواجهة
        self.sidebar_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        scroll_sidebar = ScrollView()
        scroll_sidebar.add_widget(self.sidebar_layout)
        layout1.add_widget(scroll_sidebar)
        
        self.tab1.add_widget(layout1)
        self.add_widget(self.tab1)

        # --- التبويب الثاني: تحليل الميلاد ---
        self.tab2 = TabbedPanelItem(text=self.engine.fx("تحليل الميلاد"))
        layout2 = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # شبكة إدخال التاريخ
        input_grid = GridLayout(cols=3, size_hint_y=None, height=250, spacing=5)
        self.day_in = TextInput(hint_text="DD", input_filter="int", halign="center")
        self.month_in = TextInput(hint_text="MM", input_filter="int", halign="center")
        self.year_in = TextInput(hint_text="YYYY", input_filter="int", halign="center")
        self.hour_in = TextInput(hint_text="HH", input_filter="int", halign="center")
        self.min_in = TextInput(hint_text="mm", input_filter="int", halign="center")
        self.gmt_in = TextInput(text="3.0", halign="center")
        
        for widget in [self.day_in, self.month_in, self.year_in, self.hour_in, self.min_in, self.gmt_in]:
            input_grid.add_widget(widget)
        layout2.add_widget(input_grid)

        btn_birth = Button(text=self.engine.fx("🚀 تحليل الولادة الشامل"), size_hint_y=None, height=120, 
                           background_color=(0.14, 0.38, 0.92, 1), font_name="arial.ttf")
        btn_birth.bind(on_press=self.run_full_natal)
        layout2.add_widget(btn_birth)
        layout2.add_widget(Label(text=self.engine.fx("أدخل بياناتك لاستخراج الهيلاج والفردارية والمستولي")))
        
        self.tab2.add_widget(layout2)
        self.add_widget(self.tab2)

        # --- التبويب الثالث: الأدوات والمستشار ---
        self.tab3 = TabbedPanelItem(text=self.engine.fx("الأدوات"))
        layout3 = GridLayout(cols=2, padding=10, spacing=10)
        
        tools = [
            ("🤖 المستشار الذكي", (0.54, 0.36, 0.96, 1), self.open_ai_chat),
            ("☀️ عودة الشمس", (1, 0.6, 0, 1), self.open_sr_popup),
            ("🔮 تنجيم ساعي", (0.1, 0.5, 0.2, 1), None),
            ("💍 توافقية", (0.9, 0.2, 0.4, 1), None)
        ]
        
        for name, color, func in tools:
            btn = Button(text=self.engine.fx(name), background_color=color, font_name="arial.ttf")
            if func: btn.bind(on_press=func)
            layout3.add_widget(btn)
            
        self.tab3.add_widget(layout3)
        self.add_widget(self.tab3)

        # تحديث القائمة الجانبية كل دقيقة
        Clock.schedule_interval(lambda dt: self.update_sidebar_ui(), 60)
        # تحميل الموقع المحفوظ
        Clock.schedule_once(lambda dt: self.load_initial_data(), 1)

    def load_initial_data(self):
        cache = self.engine.load_location_cache()
        if cache:
            self.city_in.text = cache['city']
            self.gmt_in.text = str(cache['gmt'])
            self.engine.lat, self.engine.lon = cache['lat'], cache['lon']
        self.update_sidebar_ui()

    def run_city_search(self, instance):
        res = self.engine.fetch_geo_info(self.city_in.text)
        if res['status'] == 'success':
            self.engine.lat, self.engine.lon = res['lat'], res['lon']
            self.gmt_in.text = str(res['gmt'])
            self.engine.save_location_cache(self.city_in.text, res['lat'], res['lon'], res['gmt'])
            self.update_sidebar_ui()
            self.show_message("نجاح", f"تم ضبط الموقع: {self.city_in.text}")

    def update_sidebar_ui(self):
        self.sidebar_layout.clear_widgets()
        jd = self.engine.get_now_jd()
        import swisseph as swe
        sun_pos = float(swe.calc_ut(jd, 0)[0])
        planets = [(0,"الشمس"),(1,"القمر"),(2,"عطارد"),(3,"الزهرة"),(4,"المريخ"),(5,"المشتري"),(6,"زحل")]
        for pid, name in planets:
            text, color = self.engine.get_planet_sidebar_info(jd, pid, name, sun_pos)
            self.sidebar_layout.add_widget(Label(text=text, color=color, font_name="arial.ttf", font_size='18sp'))

    def run_full_natal(self, instance):
        self.show_message("جاري المعالجة", "يتم الآن استخراج الـ 6000 معلومة...")

    def open_ai_chat(self, instance):
        # محادثة بسيطة كمثال للربط
        content = BoxLayout(orientation='vertical', padding=10)
        self.chat_out = Label(text=self.engine.fx("أنا مستشارك الفلكي، كيف أساعدك؟"), font_name="arial.ttf")
        self.chat_in = TextInput(multiline=False, size_hint_y=None, height=100)
        btn = Button(text=self.engine.fx("إرسال"), size_hint_y=None, height=100)
        btn.bind(on_press=self.send_to_ai)
        content.add_widget(self.chat_out); content.add_widget(self.chat_in); content.add_widget(btn)
        Popup(title="AI Consultant", content=content, size_hint=(0.9, 0.8)).open()

    def send_to_ai(self, instance):
        query = self.chat_in.text
        ans = self.engine.ask_astro_ai(query, {"location": self.city_in.text})
        self.chat_out.text = self.engine.fx(ans)
        self.chat_in.text = ""

    def open_sr_popup(self, instance):
        # نافذة عودة الشمس
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        year_in = TextInput(text="2026", multiline=False)
        btn = Button(text=self.engine.fx("بدء الحساب"))
        pop = Popup(title="Solar Return", content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=lambda x: self.start_sr(year_in.text, pop))
        content.add_widget(year_in); content.add_widget(btn)
        pop.open()

    def start_sr(self, year, popup):
        popup.dismiss()
        b_data = {'day':int(self.day_in.text or 1), 'month':int(self.month_in.text or 1), 
                  'year':int(self.year_in.text or 1990), 'hour':int(self.hour_in.text or 12), 
                  'min':int(self.min_in.text or 0), 'gmt':float(self.gmt_in.text or 3)}
        report = self.engine.run_solar_return_engine(int(year), b_data)
        self.show_report_popup(report)

    def show_report_popup(self, text):
        scroll = ScrollView()
        lbl = Label(text=text, font_name="arial.ttf", size_hint_y=None, halign='right', padding=(20,20))
        lbl.bind(texture_size=lbl.setter('height'))
        scroll.add_widget(lbl)
        Popup(title="Report", content=scroll, size_hint=(0.9, 0.8)).open()

    def show_message(self, title, msg):
        Popup(title=self.engine.fx(title), content=Label(text=self.engine.fx(msg), font_name="arial.ttf"), size_hint=(0.7, 0.3)).open()

class MeeqatApp(App):
    def build(self):
        return AstroInterface()

if __name__ == "__main__":
    MeeqatApp().run()
