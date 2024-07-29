from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
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
