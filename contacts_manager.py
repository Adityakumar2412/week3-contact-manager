# Contact Management System
# Week 3 Project - Contact Management System (The Developers Arena)

import json
import re
from datetime import datetime
import csv
import os

DATA_FILE = "contacts_data.json"


def load_contacts():
    """Load contacts from JSON file if it exists."""
    if not os.path.exists(DATA_FILE):
        print("✅ No existing contacts file found. Starting fresh.")
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} contact(s) from {DATA_FILE}")
        return data
    except (json.JSONDecodeError, OSError):
        print("⚠️ Error reading contacts file. Starting with empty contacts.")
        return {}


def save_contacts(contacts):
    """Save contacts to JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=4)
        print(f"✅ Contacts saved to {DATA_FILE}")
    except OSError as e:
        print("⚠️ Error saving contacts:", e)


def validate_phone(phone):
    """Validate phone number format (10–15 digits)."""
    digits = re.sub(r"\D", "", phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None


def validate_email(email):
    """Validate email format (simple regex)."""
    if not email:
        return True
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def add_contact(contacts):
    """Add a new contact."""
    print("\n--- ADD NEW CONTACT ---")

    # Name
    while True:
        name = input("Enter contact name: ").strip()
        if not name:
            print("Name cannot be empty!")
            continue
        if name in contacts:
            print(f"Contact '{name}' already exists!")
            choice = input("Do you want to update instead? (y/n): ").lower()
            if choice == "y":
                update_contact(contacts, name)
                return
            else:
                return
        break

    # Phone
    while True:
        phone = input("Enter phone number: ").strip()
        ok, cleaned = validate_phone(phone)
        if ok:
            phone = cleaned
            break
        print("Invalid phone number! Please enter 10–15 digits.")

    # Email
    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if validate_email(email):
            break
        print("Invalid email format!")

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"

    now = datetime.now().isoformat()

    contacts[name] = {
        "phone": phone,
        "email": email if email else None,
        "address": address if address else None,
        "group": group,
        "created_at": now,
        "updated_at": now,
    }

    print(f"✅ Contact '{name}' added successfully!")


def search_contacts(contacts, search_term):
    """Return dict of contacts matching search term in name (case-insensitive)."""
    search_term = search_term.lower()
    results = {}
    for name, info in contacts.items():
        if search_term in name.lower():
            results[name] = info
    return results


def display_contact(name, info):
    """Print a single contact in formatted way."""
    print("👤", name)
    print(f"   📞 {info['phone']}")
    if info.get("email"):
        print(f"   📧 {info['email']}")
    if info.get("address"):
        print(f"   📍 {info['address']}")
    print(f"   👥 {info.get('group', 'Other')}")
    print("-" * 40)


def search_contact_menu(contacts):
    """Search contacts by name and display results."""
    if not contacts:
        print("No contacts available.")
        return

    term = input("Enter name to search: ").strip()
    if not term:
        print("Search term cannot be empty!")
        return

    results = search_contacts(contacts, term)
    if not results:
        print("No contacts found.")
        return

    print(f"\nFound {len(results)} contact(s):")
    print("-" * 40)
    for name, info in results.items():
        display_contact(name, info)


def update_contact(contacts, existing_name=None):
    """Update an existing contact."""
    if not contacts:
        print("No contacts to update.")
        return

    if existing_name is None:
        name = input("Enter contact name to update: ").strip()
    else:
        name = existing_name

    if name not in contacts:
        print(f"Contact '{name}' not found.")
        return

    contact = contacts[name]
    print("\n--- CURRENT DETAILS ---")
    display_contact(name, contact)

    print("Leave field empty to keep current value.")

    new_phone = input("New phone (or Enter to keep): ").strip()
    if new_phone:
        ok, cleaned = validate_phone(new_phone)
        if ok:
            contact["phone"] = cleaned
        else:
            print("Invalid phone. Keeping old phone.")

    new_email = input("New email (or Enter to keep): ").strip()
    if new_email:
        if validate_email(new_email):
            contact["email"] = new_email
        else:
            print("Invalid email. Keeping old email.")

    new_address = input("New address (or Enter to keep): ").strip()
    if new_address:
        contact["address"] = new_address

    new_group = input("New group (or Enter to keep): ").strip()
    if new_group:
        contact["group"] = new_group

    contact["updated_at"] = datetime.now().isoformat()
    contacts[name] = contact
    print(f"✅ Contact '{name}' updated successfully!")


def delete_contact(contacts):
    """Delete a contact."""
    if not contacts:
        print("No contacts to delete.")
        return

    name = input("Enter contact name to delete: ").strip()
    if name not in contacts:
        print(f"Contact '{name}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        print(f"🗑️ Contact '{name}' deleted.")
    else:
        print("Delete cancelled.")


def display_all_contacts(contacts):
    """Display all contacts."""
    if not contacts:
        print("No contacts to display.")
        return

    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)
    for name, info in contacts.items():
        display_contact(name, info)


def export_to_csv(contacts, filename="contacts_export.csv"):
    """Export all contacts to a CSV file."""
    if not contacts:
        print("No contacts to export.")
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Email", "Address", "Group"])
            for name, info in contacts.items():
                writer.writerow([
                    name,
                    info.get("phone", ""),
                    info.get("email", "") or "",
                    info.get("address", "") or "",
                    info.get("group", "") or "",
                ])
        print(f"✅ Exported contacts to {filename}")
    except OSError as e:
        print("⚠️ Error exporting CSV:", e)


def show_statistics(contacts):
    """Show basic statistics: total contacts, groups count."""
    total = len(contacts)
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {total}")

    if total == 0:
        return

    groups = {}
    for info in contacts.values():
        g = info.get("group", "Other")
        groups[g] = groups.get(g, 0) + 1

    print("\nContacts by Group:")
    for g, count in groups.items():
        print(f"  {g}: {count} contact(s)")


def main_menu():
    """Main menu loop."""
    contacts = load_contacts()

    while True:
        print("\n" + "=" * 30)
        print("    CONTACT MANAGEMENT SYSTEM")
        print("=" * 30)
        print("1. Add New Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Save & Exit")
        print("=" * 30)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact_menu(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            display_all_contacts(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            show_statistics(contacts)
        elif choice == "8":
            save_contacts(contacts)
            print("👋 Thank you for using Contact Management System!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main_menu()
