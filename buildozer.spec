

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
import random
import json
import os
import time

class IbadahAssistant(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 30
        
        # نظام الذكر التلقائي
        self.dhikr_label = Label(text="", font_size=24, halign='center')
        self.add_widget(self.dhikr_label)
        
        # نظام الحفظ التكرار الذكي
        self.verse_label = Label(text="", font_size=20, halign='center', text_size=(400, None))
        self.add_widget(self.verse_label)
        
        self.user_input = TextInput(hint_text="أعد كتابة الآية هنا...", multiline=False, size_hint_y=None, height=50)
        self.add_widget(self.user_input)
        
        self.check_btn = Button(text="تحقق", on_press=self.check_verse)
        self.add_widget(self.check_btn)
        
        # إحصائيات
        self.stats_label = Label(text="الأذكار اليوم: 0\nالحفظ اليوم: 0%")
        self.add_widget(self.stats_label)
        
        # التهيئة
        self.load_data()
        self.start_dhikr_rotation()
        
    def load_data(self):
        # قاعدة بيانات الأذكار والآيات
        self.adhkar = [
            "سبحان الله وبحمده",
            "أستغفر الله العظيم",
            "لا إله إلا الله وحده لا شريك له",
            "اللهم صلي على محمد"
        ]
        
        self.verses = {
            "البقرة 255": "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ",
            "الفاتحة 1-7": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ (1) الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ (2) الرَّحْمَٰنِ الرَّحِيمِ (3) مَالِكِ يَوْمِ الدِّينِ (4) إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ (5) اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ (6) صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ (7)"
        }
        
        try:
            with open('ibadah_data.json', 'r') as f:
                self.data = json.load(f)
        except:
            self.data = {"dhikr_count": 0, "memorized": {}}
    
    def save_data(self):
        with open('ibadah_data.json', 'w') as f:
            json.dump(self.data, f)
    
    def start_dhikr_rotation(self):
        Clock.schedule_interval(self.update_dhikr, 30)  # تحديث الذكر كل 30 ثانية
    
    def update_dhikr(self, dt):
        self.dhikr_label.text = random.choice(self.adhkar)
        self.data['dhikr_count'] += 1
        self.update_stats()
    
    def show_random_verse(self):
        verse_ref, verse_text = random.choice(list(self.verses.items()))
        self.current_verse = (verse_ref, verse_text)
        self.verse_label.text = f"{verse_ref}:\n{verse_text}"
    
    def check_verse(self, instance):
        user_text = self.user_input.text.strip()
        _, original_text = self.current_verse
        
        if user_text == original_text:
            self.verse_label.text = "صحيح! أحسنت حفظك"
            # تحديث تقدم الحفظ
            if self.current_verse[0] not in self.data['memorized']:
                self.data['memorized'][self.current_verse[0]] = 0
            self.data['memorized'][self.current_verse[0]] += 1
        else:
            self.verse_label.text = "حاول مرة أخرى:\n" + self.current_verse[1]
        
        self.user_input.text = ""
        self.update_stats()
        Clock.schedule_once(lambda dt: self.show_random_verse(), 3)
    
    def update_stats(self):
        memorized_count = sum(1 for v in self.data['memorized'].values() if v >= 3)
        total_verses = len(self.verses)
        progress = int((memorized_count / total_verses) * 100) if total_verses > 0 else 0
        
        self.stats_label.text = (
            f"الأذكار اليوم: {self.data['dhikr_count']}\n"
            f"الحفظ اليوم: {progress}%\n"
            f"الآيات المحفوظة: {memorized_count}/{total_verses}"
        )
        self.save_data()

class IbadahApp(App):
    def build(self):
        self.title = 'معين الذكر والحفظ'
        return IbadahAssistant()

if __name__ == '__main__':
    IbadahApp().run()
```

### 🌟 مميزات التطبيق:
1. **نظام الذكر التلقائي**:
   - يظهر ذكر مختلف كل 30 ثانية
   - يحسب عدد الأذكار اليومية

2. **مدرب حفظ القرآن الذكي**:
   - يعرض آيات عشوائية للحفظ
   - يتعرف على صحة إعادة كتابتك للآية
   - يتتبع تقدمك في الحفظ

3. **إحصائيات مرئية**:
   - نسبة إنجاز الحفظ اليومي
   - عدد الأذكار
   - تقدمك العام في حفظ الآيات

### 📱 كيفية التحويل لتطبيق على أندرويد:
1. احفظ الكود في ملف باسم `main.py`
2. أنشئ ملف `buildozer.spec` وأضف:
   ```ini
   [app]
   title = معين الذكر
   package.name = ibadahassistant
   package.domain = org.user
   source.dir = .
   source.include_exts = py,png,jpg,kv,atlas,json
   version = 1.0
   requirements = python3,kivy
   orientation = portrait

   [buildozer]
   log_level = 2
   ```
3. نفذ الأمر:
   ```bash
   buildozer android debug deploy run
   ```
