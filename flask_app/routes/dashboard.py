from flask import Blueprint, current_app, render_template, request, redirect, url_for
from ..drive_service import list_in_folder, create_text_file, move_file

bp = Blueprint("ui", __name__)

@bp.get("/")
def index():
    cfg = current_app.config
    waiting = list_in_folder(cfg["GDRIVE_JOBDOCS_PENDING_ID"])
    processed = list_in_folder(cfg["GDRIVE_JOBDOCS_PROCESSED_ID"])
    # pass through any msg flags
    ok = request.args.get("ok")
    err = request.args.get("err")
    return render_template("index.html", waiting=waiting, processed=processed, ok=ok, err=err)

@bp.post("/upload")
def upload():
    company = (request.form.get("company") or "").strip()
    title = (request.form.get("title") or "").strip()
    description = (request.form.get("description") or "").strip()

    if not company or not title or not description:
        return redirect(url_for("ui.index", err="missing"))

    create_text_file(current_app.config["GDRIVE_JOBDOCS_PENDING_ID"], company, title, description)
    return redirect(url_for("ui.index", ok="added"))

@bp.post("/mark_processed/<file_id>")
def mark_processed(file_id):
    move_file(file_id, current_app.config["GDRIVE_JOBDOCS_PROCESSED_ID"])
    return redirect(url_for("ui.index", ok="moved"))
