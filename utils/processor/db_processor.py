import os

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from utils.base_model import BaseModel
from utils.exception.app_exception import AppException
from utils.exception.resource_not_found_exception import ResourceNotFoundException
from utils.file.file_processor import FileProcessor


def get_db_engine():
    db_engine = create_engine("sqlite:///{}".format(os.path.join(FileProcessor.current_path(), "db.sqlite")),
                              echo=False)
    return db_engine


def get_session():
    return sessionmaker(bind=get_db_engine())()


class DBProcessor:
    def get_session(self):
        return get_session()

    def get_engine(self):
        return get_db_engine()

    def initiate_data(self):
        try:
            session = get_session()
            db_engine = get_db_engine()
            BaseModel.metadata.create_all(db_engine)
            print("Creating database")
            # print(color_text(YELLOW_TEXT, "Creating ") + "database")
            print("Database created\n")
            # print("Database " + color_text(GREEN_TEXT, "created\n"))

            print("Setting up runtime vars")
            # print(color_text(GREEN_TEXT, "Setting up") + " runtime vars")

            session.commit()
        except Exception as ex:
            print("Database Connection Failed {}".format(ex))
            raise ex

    def insert(self, model) -> int:
        print(f"Inserting data: {model}")
        session = get_session()
        session.add(model)
        session.commit()
        return model.id

    def get(self, model):
        session = self.get_session()
        return session.query(model).all()

    def find_by_id(self, model, _id: int):
        session = self.get_session()
        result = session.query(model).filter_by(id=_id).first()
        if result is None:
            raise ResourceNotFoundException(model.__class__.__name__, 'id', _id)
        return result

    # TODO: requires additional work
    def update(self, model, update_data):
        session = self.get_session()
        session.commit()

    def remove(self, model, record_id: int):
        session = self.get_session()
        record = session.query(model).get(record_id)
        if record:
            session.delete(record)
            session.commit()
            print(f'Record with id {record_id} has been deleted.')
        else:
            raise AppException(f'Record with id {record_id} was not found.')

    def next_id_for_table(self, model):
        session = self.get_session()
        max_id = session.query(func.max(model.id)).scalar()
        if max_id is None:
            return 1
        return max_id + 1

    def next_order_seq_for_table(self, model):
        session = self.get_session()
        max_seq = session.query(func.max(model.order_seq)).scalar()
        if max_seq is None:
            return 1
        return max_seq + 1

    def swap_order(self, model, id1, id2):
        session = self.get_session()

        # Identify the rows to swap (you can use some criteria to identify the rows)
        row1 = session.query(model).filter_by(id=id1).first()
        row2 = session.query(model).filter_by(id=id2).first()

        # Retrieve the values of the column 'order_seq' from both rows
        value1 = row1.order_seq
        value2 = row2.order_seq

        row1.order_seq = value2
        row2.order_seq = value1

        session.commit()
