# Builds on my original Pomodoro timer (see pomodoro.py). This has start, stop, pause controls.
# It uses callbacks, session_state, status messages and reruns for a better UX
# Requires Streamlit, version >= 1.14.0
import streamlit as st
import time

st.set_page_config(
    page_title='Pomodoro',
    layout='centered',
    page_icon='🍅'
)

import streamlit_debug
streamlit_debug.set(flag=False, wait_for_client=True, host='localhost', port=8765)

st.markdown(
    """
    <style>
    .time {
        font-size: 100px !important;
        font-weight: 700 !important;
        color: #ec5953 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

state = st.session_state
if 'TS' not in state:
    state.TS = 0
if 'STARTED' not in state:
    state.STARTED = False
if 'STOPPED' not in state:
    state.STOPPED = True
if 'PAUSED' not in state:
    state.PAUSED = False

if 'COUNTDOWN' not in state:
    state.COUNTDOWN = '--:--'
if 'INFO' not in state:
    state.INFO = None

def set_states(started=False, stopped=True, paused=False):
    state.STARTED = started
    state.STOPPED = stopped
    state.PAUSED = paused
    
def _stop_cb():
    state.TS = 0
    state.COUNTDOWN = '--:--'
    state.INFO = (st.error, 'Stopped')
    set_states(started=False, stopped=True, paused=False)
def _start_cb(ts):
    if not state.PAUSED:
        state.TS = ts
    state.INFO = (st.info, 'Started')
    set_states(started=True, stopped=False, paused=False)
def _pause_cb():
    state.INFO = (st.warning, 'Paused')
    set_states(started=False, stopped=False, paused=True)

def display_countdown(countdown, st_deltagen=None):
    if not st_deltagen:
        st_deltagen = st.empty()
    return st_deltagen.markdown(
            f"""<p class="time">{countdown}</p>""",
            unsafe_allow_html=True
    )
    
def count_down():
    while True:
        mins, secs = divmod(state.TS, 60)
        state.COUNTDOWN = '{:02d}:{:02d}'.format(mins, secs)
        display_countdown(state.COUNTDOWN, countdown_widget)
        time.sleep(1)
        state.TS -= 1
        if state.TS < 0 or state.STOPPED:
            break
    if state.STARTED:
        set_states(started=False, stopped=True, paused=False)
        state.INFO = (st.success, 'Time Up!')
        st.balloons()
        time.sleep(2)
        st.experimental_rerun()

info = state.INFO[0](f'# Pomodoro {state.INFO[1]}') if state.INFO != None else st.title('Pomodoro')
countdown_widget = display_countdown(state.COUNTDOWN)

c1, _, c3, c4, c5 = st.columns([3,3,2,2,2])
with c1:
    time_minutes = st.number_input('Enter time in minutes ', min_value=0.1, value=25.0)
    time_in_seconds = time_minutes * 60
with c3:
    st.caption('&nbsp;')
    if st.button('⚪ Start', type='primary', on_click=_start_cb, args=(int(time_in_seconds),), disabled=state.STARTED):
        st.experimental_rerun()
with c4:
    st.caption('&nbsp;')
    if st.button('🔴 Stop', on_click=_stop_cb, disabled=state.STOPPED):
        st.snow()
        time.sleep(5)
        state.INFO = None
        st.experimental_rerun()
with c5:
    st.caption('&nbsp;')
    if st.button('🔵 Pause', on_click=_pause_cb, disabled=state.PAUSED or state.STOPPED):
        st.experimental_rerun()

if state.STARTED and (not state.PAUSED):
    count_down()

