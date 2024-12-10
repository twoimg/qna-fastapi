from app.core.security import check_password_hash, make_password_hash

from app.models.user import User
from app.models.question import Question
from app.models.answer import Answer

from app.schemas.auth import UserCreate
from app.schemas.questions import QuestionCreate, AnswerCreate

from sqlalchemy.orm import Session, joinedload

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Get a user by username

    Parameters:
        db (Session): The database session
        username (str): The username of the user

    Returns:
        User | None: The user with the given username or None if not found
    """
    user = db.query(User).filter(User.username == username).first()
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Get a user by email

    Parameters:
        db (Session): The database session
        email (str): The email of the user

    Returns:
        User | None: The user with the given email or None if not found
    """
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Get a user by id

    Parameters:
        db (Session): The database session
        user_id (int): The id of the user

    Returns:
        User | None: The user with the given id or None if not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    return user

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticate a user by username and password

    Parameters:
        db (Session): The database session
        username (str): The username of the user
        password (str): The password of the user

    Returns:
        User | None: The user if authenticated or None if not
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not check_password_hash(password, user.hashed_password):
        return None
    return user

def verify_unique_user(db: Session, username: str, email: str) -> tuple[bool, str]:
    """
    Verify if a user is unique by username and email

    Parameters:
        db (Session): The database session
        username (str): The username of the user
        email (str): The email of the user

    Returns:
        tuple[bool, str]: A tuple containing a boolean and a message
    """
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if not existing_user:
        return True, "unique"
    
    if existing_user.username == username:
        return False, "Username already exists"
    
    if existing_user.email == email:
        return False, "Email already exists"

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user

    Parameters:
        db (Session): The database session
        user (UserCreate): The user to create

    Returns:
        User: The created user
    """
    hashed_password = make_password_hash(user.password)
    db_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def create_question(db: Session, question: QuestionCreate) -> Question:
    """
    Create a new questions

    Parameters:
        db (Session): The database session
        question (QuestionCreate): The question to create

    Returns:
        Question: The created question
    """
    db_question = Question(
        content=question.question,
        user_id=question.to_user_id,
        is_anonymous=question.isAnonymous
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question

def get_questions_by_username(
        db: Session, username: str, page: int = 1, page_size: int = 10
) -> tuple[list[Question], int] | None:
    """
    Get questions by username

    Parameters:
        db (Session): The database session
        username (str): The username of the user
        page (int): The page number
        page_size (int): The number of questions per page

    Returns:
        tuple[list[Question], int]: A tuple containing a list of questions and the total number of questions
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    offset = (page - 1) * page_size

    total_questions = db.query(Question)\
        .filter(User.username == username)\
        .count()
    
    questions = db.query(Question)\
        .join(User)\
        .options(
            joinedload(Question.answers),
            joinedload(Question.user)
        )\
        .filter(User.username == username)\
        .order_by(Question.created_at.desc())\
        .offset(offset)\
        .limit(page_size)\
        .all()
    
    return questions, total_questions

def get_question_by_id(db: Session, question_id: int) -> Question | None:
    """
    Get a question by id

    Parameters:
        db (Session): The database session
        question_id (int): The id of the question

    Returns:
        Question | None: The question with the given id or None if not found
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    return question

def create_answer(db: Session, question_id: int, user_id: int, answer: AnswerCreate) -> Answer:
    """
    Create a new answer

    Parameters:
        db (Session): The database session
        question_id (int): The id of the question
        answer (AnswerCreate): The answer to create

    Returns:
        Answer: The created answer
    """
    db_answer = Answer(
        content=answer.content,
        user_id=user_id,
        question_id=question_id
    )

    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    return db_answer
