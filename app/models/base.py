from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CommonMixin:
    """Common methods for all models."""

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.to_dict()}>"
