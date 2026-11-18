import os

print("🛠️ Memulai proses patch otomatis...")

# ==========================================
# LANGKAH 2: PATCH FILE schemas.py
# ==========================================
schema_path = "tradingagents/agents/schemas.py"
if os.path.exists(schema_path):
    with open(schema_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    in_class = False
    inserted = False
    
    for line in lines:
        new_lines.append(line)
        # Deteksi awal class PortfolioDecision
        if "class PortfolioDecision" in line:
            in_class = True
        # Deteksi jika class sudah selesai (ketemu class baru atau fungsi baru)
        elif in_class and not inserted and line.strip() and not line.startswith(" "):
            in_class = False
        # Cari tempat untuk menyisipkan field baru di dalam class
        elif in_class and ("time_horizon" in line or "investment_thesis" in line):
            if not inserted:
                new_lines.append('    entry_price: Optional[str] = Field(default=None, description="The absolute entry price")\n')
                new_lines.append('    stop_loss: Optional[str] = Field(default=None, description="The absolute stop loss price")\n')
                new_lines.append('    take_profit: Optional[str] = Field(default=None, description="The absolute take profit price")\n')
                new_lines.append('    position_size: Optional[str] = Field(default=None, description="The position size percentage")\n')
                inserted = True

    if inserted:
        with open(schema_path, "w") as f:
            f.writelines(new_lines)
        print("✅ schemas.py berhasil ditambahkan field SL/TP.")
    else:
        print("⚠️ Field SL/TP mungkin sudah ada atau struktur file berbeda.")
else:
    print("❌ File schemas.py tidak ditemukan!")

# ==========================================
# LANGKAH 3: PATCH FILE structured.py
# ==========================================
struct_path = "tradingagents/agents/structured.py"
if os.path.exists(struct_path):
    with open(struct_path, "r") as f:
        content = f.read()

    start_idx = content.find("def render_pm_decision")
    if start_idx != -1:
        # Cari fungsi berikutnya setelah render_pm_decision
        end_idx = content.find("\ndef ", start_idx + 10)
        if end_idx == -1:
            end_idx = len(content)

        # Kode fungsi baru (Tabel Markdown)
        new_func = '''def render_pm_decision(decision: PortfolioDecision) -> str:
    entry = getattr(decision, 'entry_price', None) or "N/A"
    sl = getattr(decision, 'stop_loss', None) or "N/A"
    tp = getattr(decision, 'take_profit', None) or decision.price_target or "N/A"
    size = getattr(decision, 'position_size', None) or "N/A"

    table = f"""| Parameter | Nilai / Keputusan |
| :--- | :--- |
| **Rating** | {getattr(decision.rating, 'value', decision.rating)} |
| **Entry Price** | {entry} |
| **Stop Loss** | {sl} |
| **Take Profit** | {tp} |
| **Position Size** | {size} |"""

    return f"""{table}

**Executive Summary**:
{decision.executive_summary}

**Investment Thesis**:
{decision.investment_thesis}

**Time Horizon**: {decision.time_horizon or 'N/A'}
'''
        
        new_content = content[:start_idx] + new_func + "\n" + content[end_idx:]
        with open(struct_path, "w") as f:
            f.write(new_content)
        print("✅ structured.py berhasil diubah menjadi format Tabel.")
    else:
        print("⚠️ Fungsi render_pm_decision tidak ditemukan di structured.py.")
else:
    print("❌ File structured.py tidak ditemukan!")

print("🎉 Semua proses patch selesai dengan sukses!")
