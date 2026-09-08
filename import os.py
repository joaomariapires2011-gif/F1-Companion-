import os
import threading
import pandas as pd
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import fastf1
import fastf1.plotting

# ==========================================
# ⚙️ SETUP E CONFIGURAÇÕES INICIAIS
# ==========================================
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache') 
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("red")

session_telemetry = None
canvas_telemetry = None
canvas_track = None


# ==========================================
# 🏎️ MOTOR DE DADOS E TELEMETRIA
# ==========================================
def load_session_data():
    global session_telemetry
    try:
        app.after(0, lambda: lbl_status.configure(text="⏳ A carregar dados da sessão: Hungarian Grand Prix...", text_color="#aaaaaa"))
        
        session_telemetry = fastf1.get_session(2024, 'Hungary', 'Q') 
        session_telemetry.load(telemetry=True, laps=True, weather=False)
        
        app.after(0, lambda: lbl_status.configure(text="✅ Sessão carregada com sucesso!", text_color="#55ff55"))
        
        # Carregar tabelas e mapas
        fetch_lap_times()
        render_track_map()
    except Exception as e:
        print(f"❌ Erro ao carregar sessão: {e}")
        app.after(0, lambda: lbl_status.configure(text="Erro de conexão à API do FastF1", text_color="#ff5555"))

def fetch_lap_times():
    global session_telemetry
    if session_telemetry is None:
        return
        
    try:
        laps = session_telemetry.laps.pick_quicklaps()
        fastest_laps = laps.groupby('Driver').first().reset_index()
        fastest_laps = fastest_laps.sort_values(by='LapTime')[['Driver', 'LapTime', 'Team']]
        
        formatted_text = "PILOTO | TEMPO DE VOLTA | EQUIPA\n" + "-"*40 + "\n"
        for _, row in fastest_laps.iterrows():
            lap_str = str(row['LapTime']).split('days ')[-1][:11]
            formatted_text += f"{row['Driver']:<6} | {lap_str:<14} | {row['Team']}\n"
            
        app.after(0, lambda: txt_laptimes.delete("1.0", "end"))
        app.after(0, lambda: txt_laptimes.insert("1.0", formatted_text))
    except Exception as e:
        err_msg = str(e)
        app.after(0, lambda msg=err_msg: lbl_status.configure(text=f'Erro ao carregar tempos: {msg}', text_color='#ff5555'))

def render_track_map():
    global session_telemetry, canvas_track
    if session_telemetry is None:
        return
        
    try:
        # Obter a volta mais rápida da sessão para desenhar a pista
        fastest_lap = session_telemetry.laps.pick_fastest()
        tel = fastest_lap.get_telemetry()
        
        x = tel['X']
        y = tel['Y']
        
        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#1e1e1e')
        ax.set_facecolor('#1e1e1e')
        
        # Desenhar a linha do circuito
        ax.plot(x, y, color='#e10600', linewidth=3, label=f"Circuito: {session_telemetry.event['EventName']}")
        
        ax.set_aspect('equal')
        ax.axis('off') # Esconder eixos numéricos para focar no mapa
        ax.set_title(f"Mapa da Pista - {session_telemetry.event['EventName']}", color='white', fontsize=12, fontweight='bold')
        fig.tight_layout()
        
        app.after(0, lambda: display_track_canvas(fig))
    except Exception as e:
        print(f"❌ Erro ao desenhar mapa da pista: {e}")

def display_track_canvas(fig):
    global canvas_track
    if canvas_track:
        canvas_track.get_tk_widget().destroy()
        
    canvas_track = FigureCanvasTkAgg(fig, master=tab_track)
    canvas_track.draw()
    canvas_track.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

def render_telemetry_chart(tel_d1, d1_code, tel_d2, d2_code, event_title):
    global canvas_telemetry
    
    if canvas_telemetry:
        canvas_telemetry.get_tk_widget().destroy()
        
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    
    color_d1 = fastf1.plotting.driver_color(d1_code)
    color_d2 = fastf1.plotting.driver_color(d2_code)
    
    ax.plot(tel_d1['Distance'], tel_d1['Speed'], color=color_d1, label=d1_code, linewidth=2)
    ax.plot(tel_d2['Distance'], tel_d2['Speed'], color=color_d2, label=d2_code, linewidth=2)
    
    ax.set_title(f"Telemetria - Velocidade: {event_title}", color='white')
    ax.set_xlabel("Distância (m)", color='#aaaaaa')
    ax.set_ylabel("Velocidade (km/h)", color='#aaaaaa')
    ax.tick_params(axis='x', colors='#aaaaaa')
    ax.tick_params(axis='y', colors='#aaaaaa')
    ax.grid(color='#444444', linestyle='--', linewidth=0.5)
    
    ax.legend(facecolor='#333333', edgecolor='none', labelcolor='white')
    fig.tight_layout()
    
    canvas_telemetry = FigureCanvasTkAgg(fig, master=tab_telemetry)
    canvas_telemetry.draw()
    canvas_telemetry.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

def update_chart_for_drivers(d1_code, d2_code):
    global session_telemetry
    if session_telemetry is None:
        app.after(0, lambda: lbl_status.configure(text="⚠️ Aguarda que a sessão acabe de carregar!", text_color="#ffaa00"))
        return

    try:
        laps_d1 = session_telemetry.laps.pick_drivers([d1_code]).dropna(subset=['LapTime'])
        laps_d2 = session_telemetry.laps.pick_drivers([d2_code]).dropna(subset=['LapTime'])

        if laps_d1.empty or laps_d2.empty:
            app.after(0, lambda: lbl_status.configure(text=f"⚠️ Sem voltas válidas para {d1_code} ou {d2_code}.", text_color="#ffaa00"))
            return

        lap_d1 = laps_d1.pick_fastest()
        lap_d2 = laps_d2.pick_fastest()

        tel_d1 = lap_d1.get_telemetry().copy()
        tel_d2 = lap_d2.get_telemetry().copy()

        start_dist_d1 = tel_d1.loc[tel_d1['SessionTime'] >= lap_d1['LapStartTime'], 'Distance'].iloc[0]
        tel_d1['Distance'] = tel_d1['Distance'] - start_dist_d1
        tel_d1 = tel_d1[(tel_d1['SessionTime'] >= lap_d1['LapStartTime']) & (tel_d1['SessionTime'] <= lap_d1['Time'])]

        start_dist_d2 = tel_d2.loc[tel_d2['SessionTime'] >= lap_d2['LapStartTime'], 'Distance'].iloc[0]
        tel_d2['Distance'] = tel_d2['Distance'] - start_dist_d2
        tel_d2 = tel_d2[(tel_d2['SessionTime'] >= lap_d2['LapStartTime']) & (tel_d2['SessionTime'] <= lap_d2['Time'])]

        event_title = f"{session_telemetry.event['EventName']}"

        app.after(0, lambda: render_telemetry_chart(tel_d1, d1_code, tel_d2, d2_code, event_title))
    except Exception as e:
        print(f"❌ Erro na lógica de telemetria: {e}")


# ==========================================
# 🖥️ CONSTRUÇÃO DA INTERFACE
# ==========================================
app = ctk.CTk()
app.title("F1 Companion")
app.geometry("900x650")

top_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
top_frame.pack(fill="x", pady=(15, 5), padx=20)

btn_menu = ctk.CTkButton(top_frame, text="Menu", fg_color="#e10600", hover_color="#990000", width=80, corner_radius=8)
btn_menu.pack(side="left")

lbl_title = ctk.CTkLabel(top_frame, text="F1 COMPANION", text_color="#e10600", font=("Arial", 16, "bold"))
lbl_title.pack(side="right")

tabview = ctk.CTkTabview(app, fg_color="#1e1e1e", segmented_button_selected_color="#e10600", segmented_button_selected_hover_color="#990000")
tabview.pack(fill="both", expand=True, padx=20, pady=10)

tabview.add("Track Map")
tabview.add("Lap Times")
tabview.add("Telemetry")
tabview.set("Telemetry")

tab_track = tabview.tab("Track Map")
tab_telemetry = tabview.tab("Telemetry")
tab_laptimes = tabview.tab("Lap Times")

# --- Aba Lap Times ---
txt_laptimes = ctk.CTkTextbox(tab_laptimes, font=("Consolas", 13), fg_color="#141414")
txt_laptimes.pack(fill="both", expand=True, padx=10, pady=10)
txt_laptimes.insert("1.0", "A carregar tabela de tempos...")

# --- Controlos dentro da Telemetria ---
controls_frame = ctk.CTkFrame(tab_telemetry, fg_color="transparent")
controls_frame.pack(fill="x", pady=10, padx=10)

ctk.CTkLabel(controls_frame, text="Piloto 1:", font=("Arial", 13, "bold")).pack(side="left", padx=(0, 5))
driver1_var = ctk.StringVar(value="NOR")
dropdown_d1 = ctk.CTkComboBox(controls_frame, values=["NOR", "VER", "LEC", "HAM", "SAI", "PIA", "RUS"], variable=driver1_var, width=80, button_color="#e10600")
dropdown_d1.pack(side="left", padx=(0, 20))

ctk.CTkLabel(controls_frame, text="Piloto 2:", font=("Arial", 13, "bold")).pack(side="left", padx=(0, 5))
driver2_var = ctk.StringVar(value="VER")
dropdown_d2 = ctk.CTkComboBox(controls_frame, values=["NOR", "VER", "LEC", "HAM", "SAI", "PIA", "RUS"], variable=driver2_var, width=80, button_color="#e10600")
dropdown_d2.pack(side="left", padx=(0, 20))

btn_comparar = ctk.CTkButton(controls_frame, text="Comparar ⚡", fg_color="#e10600", hover_color="#990000", font=("Arial", 13, "bold"),
                             command=lambda: threading.Thread(target=update_chart_for_drivers, args=(driver1_var.get(), driver2_var.get()), daemon=True).start())
btn_comparar.pack(side="left")

lbl_status = ctk.CTkLabel(app, text="Inicialização do F1 Companion...", font=("Arial", 12))
lbl_status.pack(side="bottom", pady=10)

threading.Thread(target=load_session_data, daemon=True).start()

if __name__ == "__main__":
    app.mainloop()
    app.mainloop()
