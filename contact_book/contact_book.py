import json
from rich.console import Console
from rich.table import Table
from contact_book.models.contact import Contact
from contact_book.services.db import DB


class ContactBook:

    def __init__(self):
        self.console = Console()
        self.db = DB()

    def print_menu(self):
        self.console.print('[bold italic yellow on red blink]\n======== Menu ========')
        self.console.print(
            '1. Add New Contact\n'
            '2. Show All Contacts\n'
            '3. Search Contact\n'
            '4. Update Contact\n'
            '5. Delete Contact\n'
            '6. Exit\n'
        )

    def add_contact(self):
        self.console.print("[bold green]Enter A New Contact Information")
        name = input("Name: ").strip().title()
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()

        self.db.add_contact(name, phone, email)

    def print_contacts(self):
        table = Table(title="[bold blue]Contacts Table")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Phone", justify="right", style="green")
        table.add_column("Email", style="blue")

        for contact in self.db.get_contacts():
            table.add_row(
                contact.contact_id,
                contact.name,
                contact.phone,
                contact.email
            )

        self.console.print(table)

    def remove_contact(self):
        contact_id = input("Enter Contact ID to delete: ").strip()

        for contact in self.db.get_contacts():
            if contact.contact_id == contact_id:
                self.db.delete_contact(contact_id)
                self.console.print(f"[bold red]Contact with ID {contact_id} deleted successfully.")
                return

        self.console.print(f"[bold yellow]No contact found with ID {contact_id}.")

    def update_contact(self):
        contact_id = input("Enter Contact ID to update: ").strip()

        for contact in self.db.get_contacts():
            if contact.contact_id == contact_id:
                self.console.print(f"[bold green]Leave field empty if you don't want to change it.")

                new_name = input(f"New name [{contact.name}]: ").strip().title()
                new_phone = input(f"New phone [{contact.phone}]: ").strip()
                new_email = input(f"New email [{contact.email}]: ").strip()

                updated_name = new_name if new_name else contact.name
                updated_phone = new_phone if new_phone else contact.phone
                updated_email = new_email if new_email else contact.email

                self.db.update_contact(contact_id, updated_name, updated_phone, updated_email)
                self.console.print(f"[bold green]Contact with ID {contact_id} updated successfully.")
                return

        self.console.print(f"[bold yellow]No contact found with ID {contact_id}.")

    def search_contact(self):
        search = input("Search: ").strip().lower()

        table = Table(title="[bold blue]Found Contacts Table")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Phone", justify="right", style="green")
        table.add_column("Email", style="blue")

        found = False
        for contact in self.db.get_contacts():
            if search in contact.name.lower() or search in contact.email.lower() or search in contact.phone:
                table.add_row(
                    contact.contact_id,
                    contact.name,
                    contact.phone,
                    contact.email
                )
                found = True

        if found:
            self.console.print(table)
        else:
            self.console.print(f"[bold yellow]No matching contact found.")

    def run(self):
        print("Salom, Contact Book Projectga Xush Kelibsiz!")
        while True:
            self.print_menu()

            choice = input("> ")
            if choice == '1':
                self.add_contact()
            elif choice == '2':
                self.print_contacts()
            elif choice == '3':
                self.search_contact()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.remove_contact()
            elif choice == '6':
                self.console.print("[bold red]Chiqmoqda...")
                break
            else:
                self.console.print("[bold red]Noto'g'ri tanlov! Qayta urinib ko'ring.")