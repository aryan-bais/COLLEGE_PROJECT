from streamlit_webrtc import webrtc_streamer
import streamlit as st


def start_camera():
     webrtc_streamer(
        key="camera",
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        rtc_configuration={
            "iceServers": []  # 🚫 disables TURN/STUN
        }
    )