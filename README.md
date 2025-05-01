# ICT12367_movie_review_project
# 🎬 Movie Review Web App

เว็บแอปพลิเคชันสำหรับเพิ่ม ดู แก้ไข และเขียนรีวิวเกี่ยวกับหนัง  
สร้างด้วย Django และใช้ HTML Template แบบแบ่งหน้า

---

## 🗂️ โครงสร้างหน้าหลักของระบบ

| ไฟล์ | หน้าที่ | คำอธิบาย |
|------|---------|-----------|
| `base.html` | Template แม่ | โครงสร้างหลักของทุกหน้า เช่น head/body |
| `home.html` | หน้าแรก | แสดงรายชื่อหนังทั้งหมด (เป็นลิงก์ไปยังหน้ารายละเอียด) |
| `movie_detail.html` | รายละเอียดหนัง | โชว์ชื่อ, เรื่องย่อ และรีวิวทั้งหมดของหนัง |
| `movie_form.html` | ฟอร์มหนัง | สำหรับเพิ่มหรือแก้ไขข้อมูลหนัง |
| `movie_confirm_delete.html` | ยืนยันลบ | ถามก่อนลบหนัง (เพื่อความปลอดภัย) |
| `review_form.html` | ฟอร์มรีวิว | สำหรับเขียนรีวิวให้หนังแต่ละเรื่อง |

---

## 🔁 การทำงานของเว็บ (Flow)

1. เข้า `home.html` เพื่อดูรายชื่อหนังทั้งหมด
2. คลิกชื่อหนัง ➜ เข้า `movie_detail.html` เพื่อดูรายละเอียดและรีวิว
3. กด "Add Review" เพื่อไปยัง `review_form.html`
4. เพิ่มหรือแก้ไขหนังผ่าน `movie_form.html`
5. ลบหนังผ่าน `movie_confirm_delete.html`

---

## 💡 ตัวอย่างโค้ด (สั้น ๆ)

### `home.html`
```html
{% extends 'base.html' %}
{% block content %}
<h2>All Movies</h2>
<ul>
  {% for movie in movies %}
    <li><a href="{% url 'movie_detail' movie.id %}">{{ movie.title }}</a></li>
  {% endfor %}
</ul>
{% endblock %}
