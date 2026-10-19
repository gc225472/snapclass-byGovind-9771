import streamlit as st
import time

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login,get_teacher_subjects,get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipelines import predict_attendance
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
import numpy as np
from datetime import datetime
from src.database.config import supabase
import pandas as pd

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    # Initialize session state before accessing it
    if "teacher_login_type" not in st.session_state:
        st.session_state["teacher_login_type"] = "login"

    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return

    if st.session_state["teacher_login_type"] == "login":
        teacher_screen_login()

    elif st.session_state["teacher_login_type"] == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"

        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type1 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"

        if st.button('Manage Subjects', type=type1, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type1 = "primary" if st.session_state.current_teacher_tab == 'attendance_record' else "tertiary"

        if st.button('Attendance Record', type=type1, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_record'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_record":
        teacher_tab_attendance_record()

    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AT Atendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not  subjects:
        st.warning('you havent create any subject yet! please create ont to begin!')
        return
    subject_options = {f"{s['name']} -  {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1])

    with col1:
        select_subject_lable = st.selectbox('Select Subject' , options = list(subject_options.keys()))
    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:',width='stretch'):
            add_photos_dialog()

    select_subject_id  = subject_options[select_subject_lable]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')

    c1, c2, c3 = st.columns(3)
    has_photos = bool(st.session_state.attendance_images)
    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:',disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:',disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_id = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_id.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id', select_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    results, attendance_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_id.get(int(student['student_id']), [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "--",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': select_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
    with c3:
            if st.button('Use Voice Attendance', type='primary',width='stretch',icon=':material/mic:'):
                voice_attendance_dialog(select_subject_id)
                




def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1 , col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects',width='stretch')
    with col2:
        if st.button('Create new Subject',width='stretch'):
            create_subject_dialog(teacher_id)

    #List all subjects

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","students",sub['total_students']),
                ("🕰️","Classes",sub['total_classes']),

            ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code = sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback = share_btn
            )
    else:
        st.info("No Subject Found, Create One Above")




def  teacher_tab_attendance_record():
    st.header('Attendandce Record')
    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)
    if not records:
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M%P") if ts else "N'A",
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool((r.get('is_present',False)))
        })
    df = pd.DataFrame(data)

    
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ "
        + summary['Present_Count'].astype(str)
        + "/"
        + summary['Total_Count'].astype(str)
        + " Students"
    )

    display_df = summary.sort_values(
        by='ts_group',
        ascending=False
    )[['Time', 'Subject Code', 'Attendance Stats']]

    st.dataframe(display_df, width='stretch', hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        st.toast("Please fill in all the fields.", icon="⚠️")
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state["user_role"] = "teacher"
        st.session_state["teacher_data"] = teacher
        st.session_state["is_logged_in"] = True
        return True

    st.toast("Invalid username or password", icon="⚠️")
    return False



def teacher_screen_login():
    c1, c2 = st.columns(
        [1, 1],
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go Back To Home",
            type="secondary",
            key="loginbackbtn",
            icon=":material/logout:",
            icon_position="right"
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login your password", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy"
    )

    teacher_password = st.text_input(
        "Enter password",
        placeholder="Enter password",
        type="password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Login",
            type="secondary",
            icon=":material/passkey:",
            icon_position="right",
            width="stretch",
            shortcut="control+enter"
        ):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login Successful", icon="✅")
                time.sleep(1)
                st.rerun()

    with btnc2:
        if st.button(
            "Register",
            type="primary",
            icon=":material/person_add:",
            icon_position="right",
            width="stretch",
            shortcut="control+enter"
        ):
            st.session_state["teacher_login_type"] = "register"
            st.rerun()

    footer_dashboard()


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_password,
    teacher_password_confirm
):
    if not all([
        teacher_username,
        teacher_name,
        teacher_password,
        teacher_password_confirm
    ]):
        return False, "Please fill in all the fields."

    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match."

    if check_teacher_exists(teacher_username):
        return False, "Username already exists. Please choose a different username."

    try:
        create_teacher(
            teacher_username,
            teacher_name,
            teacher_password
        )
        return True, "Teacher registered successfully."

    except Exception as e:
        st.exception(e)
        return False, f"Registration failed: {e}"


def teacher_screen_register():
    c1, c2 = st.columns(
        [1, 1],
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go Back To Home",
            type="secondary",
            key="registerbackbtn",
            icon=":material/logout:",
            icon_position="right"
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register your teacher profile")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy"
    )

    teacher_name = st.text_input(
        "Enter name",
        placeholder="Ananya Roy"
    )

    teacher_password = st.text_input(
        "Enter password",
        placeholder="Enter password",
        type="password"
    )

    teacher_password_confirm = st.text_input(
        "Confirm password",
        placeholder="Confirm password",
        type="password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Register now",
            type="secondary",
            icon=":material/passkey:",
            icon_position="right",
            width="stretch",
            shortcut="control+enter"
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_password,
                teacher_password_confirm
            )

            if success:
                st.success(message)
                time.sleep(2)
                st.session_state["teacher_login_type"] = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/person_add:",
            icon_position="right",
            width="stretch",
            shortcut="control+enter"
        ):
            st.session_state["teacher_login_type"] = "login"
            st.rerun()

    footer_dashboard()
