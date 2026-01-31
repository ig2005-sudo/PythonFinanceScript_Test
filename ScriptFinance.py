import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import yfinance as yf

# 0. THEME
# ---------------------------------------------------------
BG_COLOR = '#1F2630'        
GRAPH_COLOR = '#252e3b'    
TEXT_COLOR = '#E0E0E0'      
GRID_COLOR = '#374151'      

COLOR_UBI = '#FF5252'       
COLOR_TTE = '#69F0AE'       
COLOR_MC  = '#FFB74D'       
COLOR_SAN = '#4FC3F7'      
plt.style.use('dark_background')

# 1. USER DATA
# ---------------------------------------------------------
port_metrics = {
    "Annualized Return": "-14.61%",
    "Annualized Volatility": "22.12%",
    "Sharpe Ratio": "-0.80"
}

data_summary = {
    'Ticker': ['UBI.PA', 'MC.PA', 'SAN.PA', 'TTE.PA'],
    'Name': ['Ubisoft', 'LVMH', 'Sanofi', 'TotalEnergies'],
    'Return': [-0.545027, -0.110825, -0.009974, 0.081493],
    'Volatility': [0.633064, 0.299895, 0.223055, 0.200090]
}
df_summary = pd.DataFrame(data_summary)

# 2. FETCH DATA
# ---------------------------------------------------------
tickers = df_summary['Ticker'].tolist()
print(f"Downloading data for: {tickers}...")
try:
    hist_data = yf.download(tickers, period="1y", interval="1d")['Close']
    normalized_data = (hist_data / hist_data.iloc[0]) * 100
except Exception as e:
    print("Error downloading data. Creating dummy data.")
    dates = pd.date_range(start='2025-01-01', periods=100)
    normalized_data = pd.DataFrame(np.random.randn(100, 4), index=dates, columns=tickers)

# 3. LAYOUT
# ---------------------------------------------------------
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor(BG_COLOR)

gs = gridspec.GridSpec(2, 3, width_ratios=[1, 1, 0.8]) 
ax_scatter = fig.add_subplot(gs[0, :2]) 
ax_lines = fig.add_subplot(gs[1, :2])   

# Apply theme to axes
for ax in [ax_scatter, ax_lines]:
    ax.set_facecolor(GRAPH_COLOR)
    ax.grid(True, linestyle=':', color=GRID_COLOR, alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(TEXT_COLOR)
    ax.spines['left'].set_color(TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)

# 4. CHART1 RISK REWARD
# ---------------------------------------------------------
colors = [COLOR_UBI if r < 0 else COLOR_TTE for r in df_summary['Return']]
sizes = [200 if 'UBI' in t else 100 for t in df_summary['Ticker']]

ax_scatter.scatter(df_summary['Volatility'], df_summary['Return'], c=colors, s=sizes, alpha=0.9, edgecolors='white', linewidth=0.8)

for i, txt in enumerate(df_summary['Ticker']):
    ax_scatter.annotate(f"{txt}\n{df_summary['Return'][i]:.1%}", 
                        (df_summary['Volatility'][i]+0.01, df_summary['Return'][i]),
                        fontsize=10, fontweight='bold', color=TEXT_COLOR)

ax_scatter.axhline(0, color=TEXT_COLOR, linewidth=1, linestyle='--')
ax_scatter.set_title('Risk vs. Reward Map', fontsize=14, fontweight='bold', color=TEXT_COLOR)
ax_scatter.set_xlabel('Annualized Volatility (Risk)', fontsize=11, color=TEXT_COLOR)
ax_scatter.set_ylabel('Annualized Return', fontsize=11, color=TEXT_COLOR)
ax_scatter.set_xlim(0, 0.7)

# 5. CHART2 PRICE EVOLUTION
# ---------------------------------------------------------
for col in normalized_data.columns:
    # Assign specific colors and thinner linewidths
    if "UBI" in col:
        line_color = COLOR_UBI
        line_width = 2.0 # Slightly thicker for emphasis
        z_order = 10 
    elif "TTE" in col:
        line_color = COLOR_TTE
        line_width = 1.2 # Thin & Crisp
        z_order = 5
    elif "MC" in col:
        line_color = COLOR_MC 
        line_width = 1.2 # Thin & Crisp
        z_order = 4
    elif "SAN" in col:
        line_color = COLOR_SAN 
        line_width = 1.2 # Thin & Crisp
        z_order = 4
    else:
        line_color = '#888888'
        line_width = 1.0
        z_order = 1
        
    ax_lines.plot(normalized_data.index, normalized_data[col], label=col, color=line_color, linewidth=line_width, zorder=z_order)

ax_lines.axhline(100, color=TEXT_COLOR, linestyle='--', linewidth=1)
ax_lines.set_title('Historical Performance (Base 100)', fontsize=14, fontweight='bold', color=TEXT_COLOR)
ax_lines.set_ylabel('Value (Base 100)', fontsize=11, color=TEXT_COLOR)

# Legend styling
legend = ax_lines.legend(loc='upper left', fontsize=9, facecolor=GRAPH_COLOR, edgecolor=GRID_COLOR)
for text in legend.get_texts():
    text.set_color(TEXT_COLOR)

# 6. REPORT SIDEBAR
# ---------------------------------------------------------
base_x = 0.68

# Header
plt.figtext(base_x, 0.85, "PORTFOLIO REPORT", fontsize=18, fontweight='bold', fontfamily='monospace', color=TEXT_COLOR)
plt.figtext(base_x, 0.83, "-"*28, fontsize=12, fontfamily='monospace', color=GRID_COLOR)

# Portfolio Metrics
y_pos = 0.78
for key, value in port_metrics.items():
    col = COLOR_UBI if '-' in value else COLOR_TTE
    plt.figtext(base_x, y_pos, f"{key}:", fontsize=11, fontfamily='monospace', color=TEXT_COLOR)
    plt.figtext(base_x + 0.15, y_pos, value, fontsize=11, fontfamily='monospace', fontweight='bold', color=col)
    y_pos -= 0.04

plt.figtext(base_x, y_pos, "-"*28, fontsize=12, fontfamily='monospace', color=GRID_COLOR)

# Individual Metrics Table
y_pos -= 0.05
plt.figtext(base_x, y_pos, "INDIVIDUAL METRICS:", fontsize=13, fontweight='bold', fontfamily='monospace', color=TEXT_COLOR)
y_pos -= 0.04
plt.figtext(base_x, y_pos, f"{'Ticker':<8} {'Return':<8} {'Vol.':<8}", fontsize=11, fontfamily='monospace', fontweight='bold', color=TEXT_COLOR)
y_pos -= 0.02

for index, row in df_summary.iterrows():
    ret_str = f"{row['Return']:.1%}"
    vol_str = f"{row['Volatility']:.1%}"
    
    # Text coloring matches graph lines
    if "UBI" in row['Ticker']: text_color = COLOR_UBI
    elif "TTE" in row['Ticker']: text_color = COLOR_TTE
    elif "MC" in row['Ticker']: text_color = COLOR_MC
    elif "SAN" in row['Ticker']: text_color = COLOR_SAN
    else: text_color = TEXT_COLOR

    plt.figtext(base_x, y_pos, f"{row['Ticker']:<8} {ret_str:<8} {vol_str:<8}", fontsize=11, fontfamily='monospace', color=text_color)
    y_pos -= 0.04

# Analysis / Commentary
y_pos -= 0.05
plt.figtext(base_x, y_pos, "> SYSTEM ANALYSIS:", fontsize=12, fontweight='bold', fontfamily='monospace', color='#4FC3F7')
y_pos -= 0.04
notes = (
    "• ALERT: UBI.PA (Red) is\n"
    "  critically underperforming.\n\n"
    "• DEFENSE: TTE.PA (Green) is\n"
    "  the sole positive hedge.\n\n"
    "• NEUTRAL: MC (Gold) and\n"
    "  SAN (Blue) are lagging."
)
plt.figtext(base_x, y_pos, notes, fontsize=11, fontfamily='monospace', color='#B0BEC5', verticalalignment='top')

plt.tight_layout(rect=[0, 0, 0.65, 1])
plt.show()