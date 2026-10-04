
import enum
from datetime import datetime, timezone
# from time import timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Table,
    Enum,
    null,
)
from sqlalchemy.orm import relationship
from app.db.session import Base


def utcnow():
    return datetime.now(timezone.utc)

# --- Enums ---
class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


# --- Many-to-Many Association Table ---
# Association table connecting Tasks and Labels
task_labels = Table(
    "task_labels",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("label_id", Integer, ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
   __tablename__ = 'users'
   
   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, nullable=False, unique=True)
   hashed_password = Column(String, nullable=False)
   full_name = Column(String,nullable=True)
   role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
   is_active = Column(Boolean,default=True,nullable=False)
   created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
   
   
   
   owned_projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
   assigned_tasks = relationship('Task', back_populates="assignee")
   comments = relationship('Comment', back_populates="author", cascade="all, delete-orphan")
   activity_logs = relationship("ActivityLog", back_populates="user")
   teams = relationship("Team", back_populates="owner")
   
   
   
class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    
    
    
    owner = relationship("User", back_populates="teams")
    projects = relationship("Project", back_populates="team")
    
    
class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False) 
    
    
    owner = relationship("User", back_populates="owned_projects")
    team = relationship("Team", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    
class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="CASCADE"))
    assignee_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    
    

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    labels = relationship("Label", secondary=task_labels, back_populates="tasks")
    
    
    
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete="CASCADE"), nullable= False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    
    
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")
    

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    color_hex = Column(String, default="#6C757D", nullable=False)
    
    
    tasks = relationship("Task", secondary=task_labels, back_populates="labels")
    
    
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)  
    entity_type = Column(String, nullable=False)  
    entity_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    
    
    user = relationship("User", back_populates="activity_logs")