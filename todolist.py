
# region IMPORT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Date, VARCHAR
from datetime import datetime, timedelta
# endregion IMPORT


Base = declarative_base()
db_filename = "todo.db"
engine = create_engine(f"sqlite:///{db_filename}?check_same_thread=False", echo=False)


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(VARCHAR, default="")
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


class ToDoList:
    def __init__(self, session):
        self.__session = session
        self.__menu = {
            '1': ("Today's tasks", self.__get_today_tasks),
            '2': ("Week's tasks", self.__get_week_tasks),
            '3': ("All tasks", self.__get_all_tasks),
            '4': ("Missed tasks", self.__get_missed_tasks),
            '5': ("Add task", self.__add_task),
            '6': ("Delete task", self.__delete_task),
            '0': ("Exit", ),
        }

    def main_menu_loop(self):
        while True:     # do ... while
            print(*(f"{key}) {value[0]}" for key, value in self.__menu.items()), sep='\n')
            selected_opt = ""
            while selected_opt not in self.__menu:
                selected_opt = input()

            if selected_opt == '0':
                print("Bye!")
                return 0
            else:
                self.__menu[selected_opt][1]()

    def __get_today_tasks(self):
        # rows = session.query(Table).all()
        today = datetime.today().date()
        tasks = self.__session.query(Table).filter(Table.deadline == today).all()
        if len(tasks) > 0:
            print(f"Today {datetime.today().strftime('%d %b')}:\n{tasks}")
            for num in range(len(tasks)):
                print(f"{num + 1}. {str(tasks[num])}")
        else:
            print(f"Today {datetime.today().strftime('%d %b')}:\nNothing to do!")

    def __get_week_tasks(self):
        for i in range(7):
            date = datetime.today().date() + timedelta(days=i)
            tasks = self.__session.query(Table).filter(Table.deadline == date).all()
            print(date.strftime("%A %d %b") + ":")
            if len(tasks) > 0:
                for num in range(len(tasks)):
                    print(f"{num + 1}. {str(tasks[num])}")
            else:
                print("Nothing to do!")
            print()

    def __get_all_tasks(self):
        tasks = self.__session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        if len(tasks) > 0:
            for num in range(len(tasks)):
                date_string = tasks[num].deadline.strftime("%d %b").replace("0", "")
                print(f"{num + 1}. {tasks[num]}. {date_string}")
        else:
            print("Nothing to do!")
        print()

    def __get_missed_tasks(self):
        tasks = self.__session.query(Table).filter(datetime.now().date() > Table.deadline).all()
        print("Missed tasks:")
        if len(tasks) > 0:
            for num in range(len(tasks)):
                date_string = tasks[num].deadline.strftime("%d %b").replace("0", "")
                print(f"{num + 1}. {tasks[num]}. {date_string}")
        else:
            print("Nothing is missed!")
        print()

    def __add_task(self):
        tsk = input("Enter task ")
        dl = input("Enter deadline ")
        new_row = Table(task=tsk, deadline=datetime.strptime(dl, "%Y-%m-%d"))
        self.__session.add(new_row)
        self.__session.commit()
        print("The task has been added!\n")

    def __delete_task(self):
        tasks = self.__session.query(Table).all()
        print("Choose the number of the task you want to delete:")
        if len(tasks) > 0:
            for num in range(len(tasks)):
                date_string = tasks[num].deadline.strftime("%d %b").replace("0", "")
                print(f"{num + 1}. {tasks[num]}. {date_string}")
            delete_task_index = int(input())
            self.__session.delete(tasks[delete_task_index - 1])
            self.__session.commit()
            print("The task has been deleted!")
        else:
            print("Nothing to delete!")
        print()


def main():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sql_session = Session()
    todo_list = ToDoList(sql_session)
    todo_list.main_menu_loop()
    return 0


if __name__ == '__main__':
    main()
