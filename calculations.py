import swisseph as swe
import os
import json
from datetime import datetime, timezone
import arabic_reshaper
from bidi.algorithm import get_display

class HassanAstroWhitePro:
    def __init__(self):
        # الإحداثيات الافتراضية (طرطوس)
        self.lat = 34.88
        self.lon = 35.88
        self.z_names = ["الحمل", "الثور", "الجوزاء", "السرطان", "الأسد", "العذراء", 
                        "الميزان", "العقرب", "القوس", "الجدي", "الدلو", "الحوت"]
        
        # القواميس السيادية الكبرى
        self.ZODIAC_RULERS = ["المريخ", "الزهرة", "عطارد", "القمر", "الشمس", "عطارد", "الزهرة", "المريخ", "المشتري", "زحل", "زحل", "المشتري"]
        self.EXALTATIONS_DB = {"الحمل": "الشمس", "الثور": "القمر", "السرطان": "المشتري", "العذراء": "عطارد", "الميزان": "زحل", "الجدي": "المريخ", "الحوت": "الزهرة"}
        self.TRIPLICITY_DB = {
            "نار": {"day": "الشمس", "night": "المشتري"},
            "تراب": {"day": "الزهرة", "night": "القمر"},
            "هواء": {"day": "زحل", "night": "عطارد"},
            "ماء": {"day": "الزهرة", "night": "المريخ"}
        }

    def fx(self, text):
        """إصلاح عرض اللغة العربية للأندرويد"""
        if not text: return ""
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    def _safe_float(self, val):
        """دالة المعالجة الجراحية لمنع الانهيار"""
        try:
            if isinstance(val, (list, tuple)): return float(val[0])
            return float(val) if val else 0.0
        except: return 0.0

    def get_now_jd(self):
        now = datetime.now(timezone.utc)
        return swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)

    # --- محرك البحث الجغرافي ---
    def fetch_geo_info(self, city_name):
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder
        import pytz
        try:
            geolocator = Nominatim(user_agent="meeqat_pro_v3")
            location = geolocator.geocode(city_name)
            if location:
                tf = TimezoneFinder()
                tz_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
                gmt = 3.0
                if tz_str:
                    timezone = pytz.timezone(tz_str)
                    gmt = timezone.utcoffset(datetime.now()).total_seconds() / 3600.0
                return {"status": "success", "lat": location.latitude, "lon": location.longitude, "gmt": gmt}
            return {"status": "error"}
        except: return {"status": "error"}

    # --- محرك القائمة الجانبية المطور ---
    def get_planet_sidebar_info(self, jd, p_id, p_ar_name, sun_deg):
        res, _ = swe.calc_ut(jd, p_id)
        lon = self._safe_float(res)
        speed = res[3] if len(res) > 3 else 0.1
        
        sign_idx = int(lon / 30) % 12
        deg = int(lon % 30)
        
        motion_icon = ""
        motion_color = (1, 1, 1, 1)
        if abs(speed) < 0.005: 
            motion_icon = " S"; motion_color = (1, 0.8, 0, 1)
        elif speed < 0:
            motion_icon = " ℞"; motion_color = (1, 0.2, 0.2, 1)
            
        combust = ""
        if p_id != 0:
            diff = abs(lon - sun_deg)
            if diff > 180: diff = 360 - diff
            if diff < 8.5: combust = " 🔥"

        text = f"{p_ar_name}: {self.z_names[sign_idx]} {deg}°{motion_icon}{combust}"
        return self.fx(text), motion_color

    # --- محرك عودة الشمس ---
    def run_solar_return_engine(self, target_year, birth_data):
        try:
            d, m, y = birth_data['day'], birth_data['month'], birth_data['year']
            h, mn, offset = birth_data['hour'], birth_data['min'], birth_data['gmt']
            jd_birth = swe.julday(y, m, d, (h + mn/60.0) - offset)
            sun_target = self._safe_float(swe.calc_ut(jd_birth, swe.SUN))
            
            jd_ret = swe.julday(target_year, m, d, 12)
            for _ in range(40):
                res = swe.calc_ut(jd_ret, swe.SUN)
                sun_now = self._safe_float(res)
                speed = res[3] if len(res) > 3 else 0.9856
                diff = (sun_now - sun_target + 180) % 360 - 180
                if abs(diff) < 0.0000001: break
                jd_ret -= diff / speed

            report = self.fx(f"☀️ عودة الشمس لعام {target_year}\n══════════════\n")
            planets = {0:'الشمس', 1:'القمر', 2:'عطارد', 3:'الزهرة', 4:'المريخ', 5:'المشتري', 6:'زحل'}
            for pid, name in planets.items():
                p_pos = self._safe_float(swe.calc_ut(jd_ret, pid))
                report += self.fx(f"🔹 {name}: {self.z_names[int(p_pos/30)%12]} {int(p_pos%30)}°\n")
            return report
        except: return "خطأ في الحساب"

    # --- حفظ الموقع ---
    def save_location_cache(self, city, lat, lon, gmt):
        with open("location_cache.json", "w") as f:
            json.dump({"city":city, "lat":lat, "lon":lon, "gmt":gmt}, f)

    def load_location_cache(self):
        if os.path.exists("location_cache.json"):
            with open("location_cache.json", "r") as f:
                return json.load(f)
        return None

    # --- استنطاق AI ---
    def ask_astro_ai(self, user_question, astro_data):
        import requests
        API_URL = "https://groq.com"
        API_KEY = "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"
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "أنت مفسر فلكي خبير. أجب بالعربية."},
                {"role": "user", "content": f"المعطيات: {json.dumps(astro_data)}. السؤال: {user_question}"}
            ]
        }
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=20)
            return r.json()['choices'][0]['message']['content']
        except: return "فشل الاتصال بالذكاء الاصطناعي."

    def get_daily_moon_forecast(self, user_sign):
        """تحليل وضع القمر اليوم بالنسبة لبرج المستخدم"""
        jd_now = self.get_now_jd()
        res_m, _ = swe.calc_ut(jd_now, 1) # جلب موقع القمر الآن
        moon_lon = float(res_m)
        moon_sign_idx = int(moon_lon / 30) % 12
        
        # مصفوفة التوقعات بناءً على المسافة بين برج القمر وبرج المستخدم
        user_sign_idx = self.z_names.index(user_sign)
        distance = (moon_sign_idx - user_sign_idx + 12) % 12
        
        forecasts = {
            0: "القمر في برجك: طاقة عالية، بدايات جديدة، وجاذبية مضاعفة.",
            1: "القمر في بيت مالك: تركيز على المكاسب المادية والمصاريف.",
            3: "القمر في بيت عائلتك: تميل للاستقرار المنزلي والهدوء النفسي.",
            6: "القمر في مواجهة برجك: ضغوط في الشراكات، كن دبلوماسياً اليوم.",
            8: "القمر في بيت حظك: وقت مثالي للسفر، التعلم، أو المغامرة.",
            10: "القمر في بيت أمنياتك: دعم من الأصدقاء وتحقيق هدف قريب."
        }
        
        msg = forecasts.get(distance, "يوم هادئ فلكياً؛ ركز على روتينك المعتاد.")
        return self.fx(f"🌙 حالة القمر لك اليوم:\n{msg}")
