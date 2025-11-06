import os
import numpy as np
import cv2
import time
from add_whitelist_database import update_list_txt

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE_DIR, "whitelist_data")
IMAGE_DIR = os.path.join(BASE_DIR, "whitelist_images")

ENCODINGS_FILE = os.path.join(DATA_DIR, "whitelist_encodings.npy")
NAMES_FILE     = os.path.join(DATA_DIR, "whitelist_names.npy")
LIST_FILE      = os.path.join(DATA_DIR, "whitelist_list.txt")

def log(msg):
    print(f"[WL] {msg}")

def load_whitelist():
    """Load existing whitelist arrays."""
    if os.path.exists(ENCODINGS_FILE) and os.path.exists(NAMES_FILE):
        return np.load(ENCODINGS_FILE), np.load(NAMES_FILE)
    return np.array([]), np.array([])

# -------------------------------------------------------------------

def show_whitelist():
    """Display current whitelist names."""
    _, names = load_whitelist()
    if len(names) == 0:
        print("No whitelist entries.")
    else:
        print("\nCurrent whitelist persons:")
        for i, n in enumerate(sorted(set(names.tolist())), 1):
            print(f"  {i}. {n}")
        print()
    update_list_txt(NAMES_FILE, LIST_FILE)

# -------------------------------------------------------------------

def delete_person(name):
    """Delete one specific person's data."""
    enc, names = load_whitelist()
    if len(names) == 0:
        print("Whitelist is empty.")
        return
    existing = sorted(set(names.tolist()))
    if name not in existing:
        print(f"'{name}' not found. Existing:", ", ".join(existing))
        return
    mask = names != name
    np.save(ENCODINGS_FILE, enc[mask])
    np.save(NAMES_FILE, names[mask])
    update_list_txt(NAMES_FILE, LIST_FILE)
    print(f"Deleted '{name}' successfully.\n")

# -------------------------------------------------------------------

def merge_single_person(person):
    """Import faces for one selected folder (person)."""
    from insightface.app import FaceAnalysis
    app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
    app.prepare(ctx_id=-1)

    folder_path = os.path.join(IMAGE_DIR, person)
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    if os.path.exists(ENCODINGS_FILE) and os.path.exists(NAMES_FILE):
        all_embs = list(np.load(ENCODINGS_FILE))
        all_names = list(np.load(NAMES_FILE))
    else:
        all_embs, all_names = [], []

    imgs = [f for f in os.listdir(folder_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not imgs:
        print(f"No images in {folder_path}.")
        return

    for file in imgs:
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        if img is None:
            continue
        faces = app.get(img)
        if len(faces) > 0:
            all_embs.append(faces[0].embedding)
            all_names.append(person)
            log(f"Imported {person}/{file}")
        else:
            log(f"No face detected in {person}/{file}")

    if all_embs:
        np.save(ENCODINGS_FILE, np.stack(all_embs))
        np.save(NAMES_FILE, np.array(all_names))
        update_list_txt(NAMES_FILE, LIST_FILE)
        print(f"Added '{person}' successfully.")
    else:
        print(f"No valid face found for '{person}'.")

# -------------------------------------------------------------------

def merge_from_whitelist_images():
    """List folders and allow user to choose one person to import."""
    persons = [d for d in os.listdir(IMAGE_DIR)
               if os.path.isdir(os.path.join(IMAGE_DIR, d))]
    if not persons:
        print("No subfolders found in whitelist_images/.")
        return

    print("\nFolders detected in whitelist_images/:")
    for i, p in enumerate(persons, 1):
        print(f"  {i}. {p}")
    print("  0. Cancel")

    try:
        choice = int(input("Select a person to merge: ").strip() or "0")
    except ValueError:
        print("Invalid input.")
        return

    if choice == 0:
        print("Cancelled.")
        return
    if choice < 1 or choice > len(persons):
        print("Invalid number.")
        return

    person = persons[choice - 1]
    print(f"Importing data for '{person}' ...")
    merge_single_person(person)

# -------------------------------------------------------------------

def main():
    while True:
        print("\n======= WHITELIST MANAGER =======")
        print("1) Show whitelist persons")
        print("2) Merge new data from whitelist_images/")
        print("3) Delete existing person")
        print("4) Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            show_whitelist()
        elif choice == "2":
            merge_from_whitelist_images()
        elif choice == "3":
            show_whitelist()
            n = input("Enter name to delete: ").strip()
            if n:
                delete_person(n)
        elif choice == "4":
            print("Exit Whitelist Manager.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()