from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import enum

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

class Phase(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    phasename: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    villains: so.Mapped[list['Villain']] = so.relationship(back_populates='phase')
    heroes: so.Mapped[list['Hero']] = so.relationship(back_populates='phase')

    def __repr__(self):
        return '<Phase {}>'.format(self.phasename)
    
class Villain(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            unique=True)
    phase_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Phase.id),
                                               index=True)
    
    phase: so.Mapped[Phase] = so.relationship(back_populates='villains')

    def __repr__(self):
        return '<Villain {}>'.format(self.name)
    
class Aspect(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            unique=True)
    heroes: so.Mapped[list['Hero']] = so.relationship(back_populates='default_aspect')

    def __repr__(self):
        return '<Aspect {}>'.format(self.name)

class Hero(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            unique=True)
    phase_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Phase.id),
                                               index=True)
    aspect_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Aspect.id),
                                               index=True)
    phase: so.Mapped[Phase] = so.relationship(back_populates='heroes')
    default_aspect: so.Mapped[Aspect] = so.relationship(back_populates='heroes')

    def __repr__(self):
        return '<Hero {}>'.format(self.name)

    def result_vs_villain(self, villain):
        return db.session.execute(sa.select(Result).where(Result.hero_id == self.id).
                                  where(Result.villain_id == villain.id)).scalar()
    
    def result_as_cell(self, villain):
        r = self.result_vs_villain(villain)
        if r is None:
            return "<td></td>"
        else:
            return r.as_cell()
        
class ResultTypes(enum.Enum):
    win = 1
    loss = 2

class Result(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    hero_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Hero.id),
                                               index=True)
    villain_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Villain.id),
                                               index=True)
    result: so.Mapped[ResultTypes]
    hero: so.Mapped[Hero] = so.relationship()
    villain: so.Mapped[Villain] = so.relationship()

    def __repr__(self):
        return '<Result {} vs {}: {}>'.format(self.hero.name, self.villain.name, self.result)

    def as_cell(self):
        #TODO: this should return some kind of CSS selector
        match self.result:
            case ResultTypes.win:
                return '<td bgcolor="#00ff00">W</td>'
            case ResultTypes.loss:
                return '<td bgcolor="#ff0000">L</td>'
            case _:
                return '<td></td>'
            