import streamlit as st

if "reserve" not in st.session_state:
    st.session_state.reserve = False

if st.session_state.reserve == False:
    st.switch_page("streamlit_login.py")
else:
    # 예약 페이지 설정
    st.title("Reserve Your Ticket")

    # 예약 폼
    name = st.text_input("Name")
    email = st.text_input("Email")
    ticket_count = st.number_input("Number of tickets", min_value=1, max_value=10, value=1)

    if st.button("Submit Reservation"):
        if name and email and ticket_count:
            st.success(f"Reservation successful for {name} with {ticket_count} tickets.")
        else:
            st.error("Please fill all fields.")

