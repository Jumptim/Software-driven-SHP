import numpy as np
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "whitelist_data")

ENCODINGS_FILE = os.path.join(DATA_DIR, "whitelist_encodings.npy")
NAMES_FILE = os.path.join(DATA_DIR, "whitelist_names.npy")
LIST_FILE = os.path.join(DATA_DIR, "whitelist_list.txt")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def update_list_txt(names_file, list_file):
    """Write current names into whitelist_list.txt"""
    if not os.path.exists(names_file):
        with open(list_file, "w", encoding="utf-8") as f:
            f.write("# Whitelist Person List (auto-generated)\nNo entries yet.\n")
        return
    names = np.load(names_file)
    unique = sorted(set(names.tolist()))
    with open(list_file, "w", encoding="utf-8") as f:
        f.write("# Whitelist Person List (auto-generated)\n")
        f.write(f"Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for i, n in enumerate(unique, 1):
            f.write(f"{i}. {n}\n")
    log(f"Updated whitelist_list.txt ({len(unique)} persons)")

def remove_old_images(name):
    """Legacy placeholder – no image deletion used in current version"""
    pass

def save_whitelist_entry(name, embeddings):
    """
    Save or update one person's embeddings.
    If the name already exists, old data will be replaced.
    """
    if embeddings is None or len(embeddings) == 0:
        log("No embeddings to save.")
        return

    # Create data folder if missing
    os.makedirs(DATA_DIR, exist_ok=True)

    # Load existing data
    if os.path.exists(ENCODINGS_FILE) and os.path.exists(NAMES_FILE):
        old_enc = np.load(ENCODINGS_FILE)
        old_names = np.load(NAMES_FILE)

        # Remove old entries of same name
        mask = old_names != name
        encodings = np.vstack([old_enc[mask], embeddings])
        names = np.hstack([old_names[mask], np.array([name]*len(embeddings))])
    else:
        encodings = embeddings
        names = np.array([name]*len(embeddings))

    # Save npy files
    np.save(ENCODINGS_FILE, encodings)
    np.save(NAMES_FILE, names)
    log(f"Saved {len(embeddings)} embeddings for '{name}'")

    # --- Update TXT file automatically ---
    update_list_txt(NAMES_FILE, LIST_FILE)