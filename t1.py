import pandas as pd
import matplotlib.pyplot as plt

# Load and clean the data
df = pd.read_csv(r"C:\Users\shaha\Desktop\918641_250318_162800_shsh.csv", skiprows=3)
df = df[pd.to_numeric(df['RT'], errors='coerce').notnull()]
df['RT'] = df['RT'].astype(float)
df['correct'] = pd.to_numeric(df['correct'], errors='coerce')
df['trialNo'] = pd.to_numeric(df['trialNo'], errors='coerce')

# Calculate stats
accuracy = df['correct'].mean() * 100
median_rt = df['RT'].median()
mean_rt = df['RT'].mean()

# Prepare precision by condition
precision_by_condition = df.groupby('condition1')['correct'].mean()

# Create subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# === Plot 1: RT over trials ===
axes[0].plot(df['trialNo'].values, df['RT'].values, linewidth=2)
axes[0].set_xlabel('Trial Number', fontsize=14)
axes[0].set_ylabel('Reaction Time (ms)', fontsize=14)
axes[0].set_title('Reaction Time Across Trials', fontsize=18)
axes[0].set_xticks(df['trialNo'].values[::2])  # Optional: every 2 trials
axes[0].grid(True)

# Add stats text on the first plot
stats_text = f"Accuracy: {accuracy:.2f}%\nMedian RT: {median_rt:.2f} ms\nAverage RT: {mean_rt:.2f} ms"
axes[0].text(0.01, 0.99, stats_text, transform=axes[0].transAxes,
             fontsize=14, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))

# === Plot 2: Precision by condition ===
axes[1].bar(precision_by_condition.index, precision_by_condition.values, color='skyblue')
axes[1].set_xlabel('Trial Difficulty', fontsize=14)
axes[1].set_ylabel('Precision', fontsize=14)
axes[1].set_title('Precision by Trial Difficulty', fontsize=18)
axes[1].set_ylim(0, 1)
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
# -------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Path to all user files
user_files = glob.glob(r"C:\Users\shaha\Desktop\t1\*.csv")

# Containers for each user's data
user_rts = {}
user_precisions = {}

for file in user_files:
    user_id = os.path.basename(file).split(".")[0]  # User ID from filename
    df = pd.read_csv(file, skiprows=3)

    # Clean and convert
    df = df[pd.to_numeric(df['RT'], errors='coerce').notnull()]
    df['RT'] = df['RT'].astype(float)
    df['correct'] = pd.to_numeric(df['correct'], errors='coerce')
    df['trialNo'] = pd.to_numeric(df['trialNo'], errors='coerce')

    # Store RT per user
    user_rts[user_id] = (df['trialNo'].values, df['RT'].values)

    # Calculate precision per condition (learn / noise / N_noise)
    precision_by_condition = df.groupby('condition1')['correct'].mean()
    user_precisions[user_id] = precision_by_condition

# ================== Plot 1: RT Progression for all users ==================
plt.figure(figsize=(18, 8))

for file in user_files:
    user_id = os.path.basename(file).split(".")[0]
    df = pd.read_csv(file, skiprows=3)

    # Clean and convert
    df = df[pd.to_numeric(df['RT'], errors='coerce').notnull()]
    df['RT'] = df['RT'].astype(float)
    df['correct'] = pd.to_numeric(df['correct'], errors='coerce')
    df['trialNo'] = pd.to_numeric(df['trialNo'], errors='coerce')

    # Calculate stats per user
    accuracy = df['correct'].mean() * 100
    median_rt = df['RT'].median()
    mean_rt = df['RT'].mean()

    # Plot with user stats in the legend
    plt.plot(df['trialNo'].values, df['RT'].values, linewidth=2,
             label=f"{user_id} | Acc: {accuracy:.1f}% | Med RT: {median_rt:.0f} | Avg RT: {mean_rt:.0f}")

plt.xlabel('Trial Number', fontsize=14)
plt.ylabel('Reaction Time (ms)', fontsize=14)
plt.title('Reaction Time Across Trials - Per User with Stats', fontsize=22)
plt.legend(fontsize=10, loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.show()


# ================== Plot 2: Precision per Condition per User ==================
conditions = ['learn', 'no_noise', 'noise']
n_users = len(user_precisions)
n_conditions = len(conditions)

plt.figure(figsize=(22, 8))
bar_width = 0.2
space_between_users = 0.6  # Space between user groups
colors = plt.cm.tab10.colors

handles = []
bar_positions = []
bar_labels = []

for i, (user_id, precision) in enumerate(user_precisions.items()):
    user_start = i * (n_conditions * bar_width + space_between_users)
    values = [precision.get(cond, 0) for cond in conditions]

    for j, val in enumerate(values):
        pos = user_start + j * bar_width
        bar = plt.bar(pos, val,
                      width=bar_width,
                      color=colors[i % len(colors)],
                      edgecolor='black', linewidth=0.7)  # ✅ התחימה כאן
        bar_positions.append(pos)
        bar_labels.append(conditions[j])

    handles.append(bar[0])  # Add one handle per user for legend

plt.ylabel('Precision', fontsize=14)
plt.title('Precision by Condition - Users Separated', fontsize=22)
plt.ylim(0, 1.1)

# Add the conditions text under each bar
plt.xticks(bar_positions, bar_labels, rotation=45, fontsize=12)

plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add legend with user IDs
plt.legend(handles, list(user_precisions.keys()), title='Users', loc='upper right', fontsize=10)

plt.tight_layout()
plt.show()
