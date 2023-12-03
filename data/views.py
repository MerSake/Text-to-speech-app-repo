from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from dotenv import load_dotenv
import os
import base64
import boto3

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("/home.html", user=current_user)


@views.route("/T2S_converter", methods=["GET", "POST"])
# @login_required
def T2Sapp():
    if request.method == "POST":
        text_to_convert = request.form.get("text_to_convert")
        lang = request.form.get("languages")
        engine = "neural"
        if lang == "English":
            voiceid = "Joanna"
        elif lang == "Russian":
            voiceid = "Tatyana"
            engine = "standard"
        elif lang == "Spanish":
            voiceid = "Lupe"
        elif lang == "Deutsch":
            voiceid = "Vicki"
        elif lang == "Polish":
            voiceid = "Ola"
        elif lang == "Turkish":
            voiceid = "Filiz"
            engine = "standard"
        print(text_to_convert)
        if text_to_convert:
            env_path = os.path.join(os.path.dirname(__file__), "..")
            dotenv_path = os.path.join(env_path, ".env")
            load_dotenv(dotenv_path)

            aws_access_key_id = os.getenv("aws_access_key_id")
            aws_secret_access_key = os.getenv("aws_secret_access_key")
            polly_client = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name="us-east-1",
            ).client("polly")
            response = polly_client.synthesize_speech(
                VoiceId=voiceid,
                OutputFormat="mp3",
                Text=text_to_convert,
                Engine=engine,
            )

            audio_data = response["AudioStream"].read()
            import base64

            audio_data_base64 = base64.b64encode(audio_data).decode("utf-8")

            return render_template(
                "/Text2Speech-converter.html", audio_data=audio_data_base64
            )
    return render_template("/Text2Speech-converter.html", user=current_user)
