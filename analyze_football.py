# -*- coding: utf-8 -*-
"""Analisis jaringan football dan dolphins.

Mereproduksi temuan utama Module 1 Network Modeling and Analysis in Python
(University of Michigan): ukuran jaringan, assortativity, broker (constraint),
effective size, dan eksplorasi jaringan dolphins.
"""
import os
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
IMG = os.path.join(BASE, "charts")
os.makedirs(IMG, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["figure.dpi"] = 120

fb1 = nx.read_gml(os.path.join(DATA, "football1.gml"), label="id")
fb2 = nx.read_gml(os.path.join(DATA, "football2.gml"), label="id")
dolph = nx.read_gml(os.path.join(DATA, "dolphins.gml"), label="id")

print("football1:", fb1.number_of_nodes(), "node,", fb1.number_of_edges(), "edge")
print("football2:", fb2.number_of_nodes(), "node,", fb2.number_of_edges(), "edge")
print("dolphins:", dolph.number_of_nodes(), "node,", dolph.number_of_edges(), "edge")

# 1. Assortativity konferensi: mana jaringan yang asli?
conf1 = nx.attribute_assortativity_coefficient(fb1, "conference")
conf2 = nx.attribute_assortativity_coefficient(fb2, "conference")
print(f"conference assortativity football1={conf1:.6f} football2={conf2:.6f}")
assert conf1 > 0.6 and conf2 < 0.05, "pola assortativity tidak sesuai ekspektasi"

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["football1", "football2"], [conf1, conf2], color=["#1D4ED8", "#9CA3AF"])
ax.set_ylabel("Assortativity konferensi")
ax.set_title("football1 jaringan asli, football2 jaringan acak")
for i, v in enumerate([conf1, conf2]):
    ax.text(i, v + 0.02, f"{v:.4f}", ha="center", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(IMG, "01_conference_assortativity.png")); plt.close(fig)

# 2. Assortativity derajat dan kemenangan
deg_ass = nx.degree_assortativity_coefficient(fb1)
wins_ass = nx.numeric_assortativity_coefficient(fb1, "wins")
print(f"degree assortativity={deg_ass:.6f} wins assortativity={wins_ass:.6f}")

# 3. Broker: constraint Burt
constraint = nx.constraint(fb1)
wins = nx.get_node_attributes(fb1, "wins")
losses = nx.get_node_attributes(fb1, "losses")
labels = nx.get_node_attributes(fb1, "label")
df = pd.DataFrame({
    "label": [labels[n] for n in fb1.nodes()],
    "constraint": [constraint[n] for n in fb1.nodes()],
    "wins": [wins[n] for n in fb1.nodes()],
    "losses": [losses[n] for n in fb1.nodes()],
})
df["win_rate"] = df["wins"] / (df["wins"] + df["losses"])
brokers = df[df["constraint"] < 0.15]
print(f"broker (constraint<0.15): {len(brokers)}")
top10 = df.nsmallest(10, "constraint")["win_rate"].mean()
bot10 = df.nlargest(10, "constraint")["win_rate"].mean()
corr = df["constraint"].corr(df["win_rate"])
print(f"win rate 10 broker teratas={top10:.6f} 10 terbawah={bot10:.6f} korelasi={corr:.6f}")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(df["constraint"], df["win_rate"], alpha=0.6, color="#1D4ED8", label="tim")
ax.scatter(brokers["constraint"], brokers["win_rate"], color="#DC2626", s=70, label="broker")
for _, r in brokers.iterrows():
    ax.annotate(r["label"], (r["constraint"], r["win_rate"]), fontsize=8)
ax.set_xlabel("Constraint (Burt)")
ax.set_ylabel("Win rate")
ax.set_title("Broker tidak cenderung lebih sering menang")
ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(IMG, "02_brokers_winrate.png")); plt.close(fig)

# 4. Effective size terendah
eff = nx.effective_size(fb1)
eff_s = pd.Series(eff).sort_values()
print("effective size terendah:", [(labels[n], round(v, 3)) for n, v in eff_s.head(3).items()])
fig, ax = plt.subplots(figsize=(7, 4.5))
bottom = eff_s.head(10)
ax.barh([labels[n] for n in bottom.index], bottom.values, color="#0D9488")
ax.set_xlabel("Effective size")
ax.set_title("10 tim dengan effective size terendah")
fig.tight_layout(); fig.savefig(os.path.join(IMG, "03_effective_size.png")); plt.close(fig)

# 5. Dolphins: distribusi derajat dan smelliness
deg = [d for _, d in dolph.degree()]
smell = [dolph.nodes[n]["smelliness"] for n in dolph.nodes()]
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(deg, bins=12, color="#7C3AED", edgecolor="white")
axes[0].set_xlabel("Derajat"); axes[0].set_ylabel("Jumlah dolphin")
axes[0].set_title("Distribusi derajat jaringan dolphins")
axes[1].hist(smell, bins=12, color="#0D9488", edgecolor="white")
axes[1].set_xlabel("Smelliness"); axes[1].set_ylabel("Jumlah dolphin")
axes[1].set_title("Distribusi smelliness dolphins")
fig.tight_layout(); fig.savefig(os.path.join(IMG, "04_dolphins_dist.png")); plt.close(fig)

dfd = pd.DataFrame({"degree": deg, "smelliness": smell})
print("korelasi smelliness vs derajat:", round(dfd["degree"].corr(dfd["smelliness"]), 6))
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(dfd["smelliness"], dfd["degree"], alpha=0.6, color="#7C3AED")
ax.set_xlabel("Smelliness"); ax.set_ylabel("Derajat")
ax.set_title("Smelliness vs derajat dolphins")
fig.tight_layout(); fig.savefig(os.path.join(IMG, "05_smelliness_degree.png")); plt.close(fig)

# Ringkasan angka kunci
summary = {
    "conference_assortativity_football1": round(conf1, 6),
    "conference_assortativity_football2": round(conf2, 6),
    "degree_assortativity": round(deg_ass, 6),
    "wins_assortativity": round(wins_ass, 6),
    "n_brokers_constraint_lt_0_15": int(len(brokers)),
    "win_rate_top10_brokers": round(float(top10), 6),
    "win_rate_bottom10_brokers": round(float(bot10), 6),
    "constraint_winrate_correlation": round(float(corr), 6),
    "lowest_effective_size": [labels[n] for n in eff_s.head(3).index],
    "smelliness_degree_correlation": round(float(dfd["degree"].corr(dfd["smelliness"])), 6),
}
import json
with open(os.path.join(BASE, "findings.json"), "w") as f:
    json.dump(summary, f, indent=2)
print("findings.json tersimpan")
print("SELESAI")
