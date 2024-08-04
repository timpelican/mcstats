from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
