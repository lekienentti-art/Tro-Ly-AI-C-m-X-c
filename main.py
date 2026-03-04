import flet as ft
import time
import google.generativeai as genai
import threading
import random 

# =======================================================
# 🔑 RỔ CHỨA CHÌA KHÓA (TRẬN ĐỒ BÁT QUÁI API)
DANH_SACH_KEY = [
    "AIzaSyBCCtE4SIPWLbMJYW5JquzdQKPJXXQ4Or0",
    "AIzaSyA5hS2lxTdY72SkLy7oaCfnhdGdkvtboHQ",
    "AIzaSyAVMRajV31z9mDPw46VUavWoNNFWW_YsGU",
    "AIzaSyBBlgiMhOX2HQCM6i3s-cmuFAp73Q_uu_c",
    "AIzaSyDoYcKb4t7bDsKbTKT6y2u4oHHrT2lworM",
    "AIzaSyC7J3JkyFjOVQ1bHiFCK578wq5ixQi3bKM",
    "AIzaSyC5aywbEiMc_BMQZlC1LwSh5H0AHK_02Eg",
    "AIzaSyA7xJu2pz3Q4sDsbGWUFKA6ok8dnngsrm8",
    "AIzaSyDqbY1IEnW5G6VZCKmSztMScaWuy1B5csU",
    "AIzaSyDX1EQWFkbWoUfhW2Qs61XO7A262Hnnr4o",
    "AIzaSyDrXbZDDosZrObEoLZE7joZlnpQbba5tpY",
       "AIzaSyAtb5HBg4GRe0ItrGo-pTM-HjMcTALw248",
]
# =======================================================

def main(page: ft.Page):
    page.title = "🤖 TRỢ LÝ AI ĐA NHÂN CÁCH - SẾP HIẾU DUBAI"
    page.window_width = 900
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    chat_session = [None]
    bot_tinh_cach = [""]

    # ==========================================
    # 🎭 MÀN 3: GIAO DIỆN CHAT & THÚ ẢO
    # ==========================================
    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    txt_input = ft.TextField(hint_text="Sếp gõ lệnh vào đây...", expand=True, border_radius=20)
    
    chuong_thu_ao = ft.Container(
        width=200, 
        height=200, 
        bgcolor=ft.Colors.BLUE_GREY_900, 
        border_radius=15,
        alignment=ft.Alignment.CENTER,
        content=ft.Column([
            ft.Icon(ft.Icons.PETS, size=50, color=ft.Colors.ORANGE),
            ft.Text("Chuồng Thú Ảo (V2)", color=ft.Colors.ORANGE, weight="bold")
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    # 🌟 NÚT KÍCH ĐIỆN (LOAD LẠI MÀN HÌNH MÀ KHÔNG MẤT TIN NHẮN)
    def ep_load_man_hinh(e):
        page.update()
        chat_history.update()
        chat_history.controls.append(ft.Text("⚡ Đã chích điện ép tải lại màn hình!", color=ft.Colors.AMBER_400, italic=True))
        page.update()

    btn_load = ft.ElevatedButton("⚡ KÍCH ĐIỆN (LOAD CHỮ)", bgcolor=ft.Colors.AMBER_700, color=ft.Colors.BLACK, on_click=ep_load_man_hinh)

    def send_message(e):
        user_text = txt_input.value.strip()
        if not user_text: return
        
        chat_history.controls.append(ft.Text(f"👤 Sếp: {user_text}", color=ft.Colors.CYAN_ACCENT, weight="bold"))
        txt_input.value = ""
        page.update()

        def fetch_ai():
            thinking_msg = ft.Text("🤖 Bot đang rặn não suy nghĩ... 3s", color=ft.Colors.YELLOW_400, italic=True)
            chat_history.controls.append(thinking_msg)
            page.update() 
            
            for i in range(2, 0, -1):
                time.sleep(1)
                thinking_msg.value = f"🤖 Bot đang rặn não suy nghĩ... {i}s"
                thinking_msg.update() 
            time.sleep(0.5)

            chat_history.controls.remove(thinking_msg)
            
            try:
                if chat_session[0]:
                    key_dang_dung = random.choice(DANH_SACH_KEY).strip()
                    genai.configure(api_key=key_dang_dung)

                    # Gọi API nhả thẳng 1 cục
                    response = chat_session[0].send_message(user_text)
                    chat_history.controls.append(ft.Text(f"🤖 Bot: {response.text}", color=ft.Colors.WHITE))
                    
                    # 🌟 THUẬT TOÁN "NÃO CÁ VÀNG" CHỐNG KHÓA MÕM 🌟
                    # Luôn xóa theo cặp (1 câu hỏi của sếp + 1 câu trả lời của Bot) để không bị lệch nhịp
                    while len(chat_session[0].history) > 10:
                        chat_session[0].history.pop(0) # Xóa câu hỏi cũ nhất
                        chat_session[0].history.pop(0) # Xóa câu trả lời cũ nhất
                        
                else:
                    chat_history.controls.append(ft.Text("⚠️ Chưa kích hoạt AI do thiếu API Key!", color=ft.Colors.RED_400))
            except Exception as ex:
                chat_history.controls.append(ft.Text(f"❌ AI Đang hụt hơi (Lỗi: {ex})", color=ft.Colors.RED_400))
            
            page.update()
            chat_history.update()

        threading.Thread(target=fetch_ai).start()

    btn_send = ft.IconButton(icon=ft.Icons.SEND_ROUNDED, icon_color=ft.Colors.BLUE_400, icon_size=35, on_click=send_message)
    txt_input.on_submit = send_message

    man_chat = ft.Row([
        ft.Column([
            ft.Container(content=chat_history, expand=True, border=ft.border.all(1, ft.Colors.OUTLINE), border_radius=10, padding=10),
            ft.Row([txt_input, btn_send])
        ], expand=True),
        ft.Column([
            chuong_thu_ao,
            btn_load,
            ft.Container(height=10),
            ft.Text("Cảm xúc hiện tại:", italic=True, color=ft.Colors.GREY_400),
            ft.Text("[ĐANG HÓNG CHUYỆN]", weight="bold", color=ft.Colors.GREEN_400)
        ], alignment=ft.MainAxisAlignment.START)
    ], expand=True, visible=False)

    # ==========================================
    # ⏳ MÀN 2: LOADING THAO TÚNG TÂM LÝ
    # ==========================================
    lbl_loading = ft.Text("Đang khởi động lõi lượng tử...", size=20, weight="bold", color=ft.Colors.GREEN_ACCENT_400)
    progress_ring = ft.ProgressRing(width=50, height=50, stroke_width=5, color=ft.Colors.GREEN_ACCENT_400)
    
    man_loading = ft.Column([
        ft.Container(height=150),
        progress_ring,
        ft.Container(height=20),
        lbl_loading
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True, visible=False)

    def chay_loading_gia(e):
        bot_tinh_cach[0] = txt_tinh_cach.value.strip()
        if not bot_tinh_cach[0]:
            bot_tinh_cach[0] = "Một trợ lý ảo thông minh, ngoan ngoãn và hài hước."

        man_khai_sinh.visible = False
        man_loading.visible = True
        page.update()

        cac_buoc_fake = [
            "Đang cấy ghép hệ thần kinh nhân tạo...",
            "Đang trích xuất dữ liệu tính cách...",
            "Đang nạp ngôn ngữ chém gió...",
            "Đồng bộ hóa não bộ Gemini 2.5 Flash hoàn tất!"
        ]
        
        for buoc in cac_buoc_fake:
            time.sleep(1.2)
            lbl_loading.value = buoc
            page.update()
        time.sleep(1)

        try:
            key_khoi_tao = random.choice(DANH_SACH_KEY).strip()
            genai.configure(api_key=key_khoi_tao)

            model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=f"Hãy nhập vai: {bot_tinh_cach[0]}")
            chat_session[0] = model.start_chat(history=[])
        except Exception:
            pass 

        man_loading.visible = False
        man_chat.visible = True
        
        chat_history.controls.append(ft.Text("🤖 Bot: Dạ em đã lên đồ xong! Sếp muốn sai bảo gì em ạ?", color=ft.Colors.GREEN_400, italic=True))
        page.update()

    # ==========================================
    # 🎭 MÀN 1: KHAI SINH (NHẬP TÍNH CÁCH)
    # ==========================================
    txt_tinh_cach = ft.TextField(
        label="Sếp muốn Trợ lý AI này có tính cách thế nào?", 
        hint_text="VD: Hãy làm một cô thư ký Gen Z, hay dỗi, xưng 'em' gọi 'sếp'...",
        multiline=True, 
        min_lines=3, 
        max_lines=5,
        border_color=ft.Colors.BLUE_400
    )
    
    man_khai_sinh = ft.Column([
        ft.Container(height=50),
        ft.Text("🔥 LÒ ĐÚC SIÊU TRỢ LÝ AI 🔥", size=30, weight="bold", color=ft.Colors.BLUE_400),
        ft.Text("Hệ thống độc quyền của Sếp Hiếu Dubai", italic=True, color=ft.Colors.GREY_500),
        ft.Container(height=30),
        txt_tinh_cach,
        ft.Container(height=20),
        ft.ElevatedButton(
            "⚡ KÍCH HOẠT NÃO BỘ TRỢ LÝ", 
            icon=ft.Icons.BOLT, 
            bgcolor=ft.Colors.BLUE_700, 
            color=ft.Colors.WHITE,
            height=50,
            on_click=chay_loading_gia
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

    page.add(man_khai_sinh, man_loading, man_chat)

# Lệnh chạy trên PC (Nếu sếp test trên Pydroid 3 thì tự thêm cái đoạn mở Web vào nhé!)
ft.run(main)
