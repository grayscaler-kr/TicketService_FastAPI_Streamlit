import streamlit as st

def logout():
    # if st.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "reserve" not in st.session_state:
    st.session_state.reserve = False

# print(st.session_state.page)

if st.session_state.logged_in:
    pg = st.navigation([
        st.Page("streamlit_main.py", title="Main"),
        st.Page(logout, title="Log out"),
        st.Page("streamlit_reserve.py", title="Reservation")
])

else:
    pg = st.navigation([
        st.Page("streamlit_main.py", title="Main"),
        st.Page("streamlit_login.py", title="Login"),
        st.Page("streamlit_user.py", title="Sign up"),
        st.Page("streamlit_reserve.py", title="Reservation")
    ])

pg.run()

# print(st.session_state.logged_in)
