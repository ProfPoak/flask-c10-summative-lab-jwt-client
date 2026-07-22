from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, User, JournalEntry

fake = Faker()

with app.app_context():
    print("Deleting all records...")
    JournalEntry.query.delete()
    User.query.delete()

    print("Creating users...")

    users = []
    usernames = []

    for i in range(20):

        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(
            username=username
        )

        user.password_hash = user.username + 'password'

        users.append(user)

    db.session.add_all(users)

    print("Creating journal entries...")
    journal_entries = []
    for i in range (100):
        entry = fake.paragraph(nb_sentences=6)

        journal_entry = JournalEntry(
            title=fake.sentence(),
            date=fake.date_time_this_year(),
            entry=entry
        )

        journal_entry.user = rc(users)

        journal_entries.append(journal_entry)

    db.session.add_all(journal_entries)

    db.session.commit()
    print("Complete.")