
from src.database.config import supabase
import bcrypt


def hash_pass(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def check_pass(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )


def check_teacher_exists(username: str) -> bool:
    response = (
        supabase.table("teachers")
        .select("username")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    return len(response.data) > 0


def create_teacher(username: str, name: str, password: str):

    print("came to create teacher")
    if check_teacher_exists(username):
        raise ValueError("Username already exists.")

    data = {
        "username": username,
        "name": name,
        "password": hash_pass(password)
    }

    print("Inserting teacher columns:", list(data.keys()))

    try:
        response = (
            supabase.table("teachers")
            .insert(data)
            .execute()
        )

        print("Teacher registered successfully.")
        return response.data

    except Exception as e:
        print("Teacher registration database error:", repr(e))
        raise


def teacher_login(username: str, password: str):
    response = (
        supabase.table("teachers")
        .select("teacher_id, username, name, password")
        .eq("username", username)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    teacher = response.data[0]

    try:
        if check_pass(password, teacher["password"]):
            return {
                "teacher_id": teacher["teacher_id"],
                "username": teacher["username"],
                "name": teacher["name"]
            }

    except (ValueError, TypeError, KeyError) as e:
        print("Password verification error:", repr(e))

    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data if response.data else []

def create_student(new_name,face_embedding=None , voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data

def create_subject(sub_code,name,section,teacher_id):
    data = {"subject_code": sub_code, "name": name, "section": section, "teacher_id": teacher_id}
    response =supabase.table("subjects").insert(data).execute()
    return response


def get_teacher_subjects(teacher_id):
    response = (
        supabase.table('subjects')
        .select('*, subject_students(count), attendance_logs(timestamp)')
        .eq('teacher_id', teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:
        # Correct student count key
        student_data = sub.get('subject_students', [])
        sub['total_students'] = (
            student_data[0].get('count', 0)
            if student_data else 0
        )

        # Count unique class sessions
        attendance = sub.get('attendance_logs', [])
        unique_sessions = {
            log['timestamp']
            for log in attendance
            if log.get('timestamp') is not None
        }

        sub['total_classes'] = len(unique_sessions)

        # Remove nested data if no longer needed
        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects


def enroll_student_to_subject(student_id,subject_id):
    data = {'student_id':student_id,"subject_id":subject_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id,subject_id):
    response = supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data

def get_student_subject(student_id):
    response = supabase.table('subject_students').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*,subjects(*)').eq('student_id',student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*,subjects!inner(*)").eq('subjects.teacher_id',teacher_id).execute()
    return response.data