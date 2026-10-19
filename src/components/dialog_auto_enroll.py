
import streamlit as st
import time

from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Enroll in Subject")
def auto_enroll_dialog(subject_code):
    student_data = st.session_state.get('student_data')

    if not student_data or not student_data.get('student_id'):
        st.error("Student ID not found. Please log in again.")
        return

    student_id = student_data['student_id']

    res = (
        supabase.table('subjects')
        .select('subject_id, name')
        .eq('subject_code', subject_code)
        .execute()
    )

    if not res.data:
        st.error('Subject code not found.')

        if st.button('Close'):
            st.query_params.clear()
            st.rerun()

        return

    subject = res.data[0]

    check = (
        supabase.table('subject_students')
        .select('*')
        .eq('subject_id', subject['subject_id'])
        .eq('student_id', student_id)
        .execute()
    )

    if check.data:
        st.info('You are already enrolled!')

        if st.button('Got it!'):
            st.query_params.clear()
            st.rerun()

        return

    st.markdown(
        f'Would you like to enroll in **{subject["name"]}**?'
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks!'):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button(
            'Yes enroll now!',
            type='primary',
            width='stretch'
        ):
            enroll_student_to_subject(
                student_id,
                subject['subject_id']
            )

            st.success('Joined successfully!')
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
