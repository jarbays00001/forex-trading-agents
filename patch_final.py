import os
import re

print("🛠️ Memulai Patch Final...")

# 1. Ubah Prompt di portfolio_manager.py
pm_path = "tradingagents/agents/managers/portfolio_manager.py"
if os.path.exists(pm_path):
    with open(pm_path, "r") as f:
        pm_content = f.read()

    old_text = "- **Investment Thesis**: the evidence that decided it."
    new_text = """- **Investment Thesis**: Start this section IMMEDIATELY with a Markdown table containing your exact entry_price, stop_loss, take_profit, and position_size. Then, write the evidence that decided it."""

    if old_text in pm_content:
        pm_content = pm_content.replace(old_text, new_text)
        with open(pm_path, "w") as f:
            f.write(pm_content)
        print("✅ Prompt di portfolio_manager.py berhasil diperbarui.")
    else:
        print("⚠️ Teks prompt tidak ditemukan, mungkin sudah diubah.")

# 2. Ubah Fungsi Render di structured.py
struct_path = "tradingagents/agents/structured.py"
if os.path.exists(struct_path):
    with open(struct_path, "r") as f:
        struct_content = f.read()

    # Cari fungsi render_pm_decision dan ganti isinya
    pattern = re.compile(r"def render_pm_decision\(decision: PortfolioDecision\) -> str:.*?(?=\ndef |\Z)", re.DOTALL)
    
    new_func = '''def render_pm_decision(decision: PortfolioDecision) -> str:
    rating_str = getattr(decision.rating, 'value', decision.rating)
    return f"""**Rating**: {rating_str}

**Executive Summary**:
{decision.executive_summary}

**Investment Thesis**:
{decision.investment_thesis}

**Time Horizon**: {decision.time_horizon or 'N/A'}
"""'''

    if "def render_pm_decision" in struct_content:
        struct_content = pattern.sub(new_func, struct_content)
        with open(struct_path, "w") as f:
            f.write(struct_content)
        print("✅ Fungsi render_pm_decision di structured.py berhasil diperbarui.")
    else:
        print("⚠️ Fungsi render_pm_decision tidak ditemukan.")

print("🎉 Patch Final selesai! Silakan jalankan TradingAgents lagi.")
