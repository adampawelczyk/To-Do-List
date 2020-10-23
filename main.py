from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def print_task(self, date=None):
        rows = self.session.query(Table).filter(Table.deadline == date).all()
        if rows:
            i = 1
            for row in rows:
                print(f"{i}. {row}")
                i += 1
        else:
            return -1

    def print_all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if rows:
            i = 1
            for row in rows:
                print(f"{i}. {row}. {row.deadline.strftime('%#d %b')}")
                i += 1
        else:
            return -1

    def print_missed_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        if rows:
            i = 1
            for row in rows:
                print(f"{i}. {row}. {row.deadline.strftime('%#d %b')}")
                i += 1
        else:
            return -1

    def add_task(self, task, deadline):
        new_row = Table(task=task, deadline=deadline)
        self.session.add(new_row)
        self.session.commit()

    def delete_task(self, task_number):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        row_to_delete = rows[task_number - 1]
        self.session.delete(row_to_delete)
        self.session.commit()


to_do_list = ToDoList('todo.db')
while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    choice = input()
    if choice == '1':
        today = datetime.today().date()
        print(f"\nToday {today.strftime('%#d %b')}:")
        if to_do_list.print_task(today) == -1:
            print("Nothing to do!")
        print()
    elif choice == '2':
        day = datetime.today().date()
        for i in range(7):
            print(f"\n{day.strftime('%A %#d %b:')}")
            if to_do_list.print_task(day) == -1:
                print("Nothing to do!")
            day += timedelta(days=1)
        print()
    elif choice == '3':
        print("\nAll tasks:")
        if to_do_list.print_all_tasks() == -1:
            print("Nothing to do!")
        print()
    elif choice == '4':
        print("\nMissed tasks:")
        if to_do_list.print_missed_tasks() == -1:
            print("Nothing is missed!")
        print()
    elif choice == '5':
        new_task = input("\nEnter task: ")
        deadline = input("Enter deadline: ")
        to_do_list.add_task(new_task, datetime.strptime(deadline, '%Y-%m-%d'))
        print("The task has been added!\n")
    elif choice == '6':
        print()
        if to_do_list.print_all_tasks() == -1:
            print("Nothing to delete!\n")
        else:
            print("Choose the number of the task you want to delete:")
            task_to_delete = int(input())
            to_do_list.delete_task(task_to_delete)
            print("The task has been deleted!\n")
    elif choice == '0':
        print("\nBye!")
        exit()
    else:
        print("Unknown option!\n")