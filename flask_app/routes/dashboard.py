from datetime import datetime
from flask import Blueprint, current_app, render_template, request, redirect, url_for
from ..drive_service import list_in_folder, create_json_file, move_file

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
    title_raw = (request.form.get("title") or "").strip()
    normalized_title = (request.form.get("normalized_title") or "").strip()
    description = (request.form.get("description") or "").strip()
    posted_at = (request.form.get("posted_at") or "").strip()

    if not company or not title_raw or not normalized_title or not description:
        return redirect(url_for("ui.index", err="missing"))

    # Default posted_at to today in m/d/yyyy
    if not posted_at:
        posted_at = datetime.now().strftime("%-m/%-d/%Y")  # Linux/Mac; Windows: %#m/%#d/%Y

    cfg = current_app.config

    create_json_file(
        cfg["GDRIVE_JOBDOCS_PENDING_ID"],
        company,
        title_raw,
        normalized_title,
        description,
        posted_at,
        sheet_id=cfg["GOOGLE_SHEET_ID"]
    )

    return redirect(url_for("ui.index", ok="added"))


@bp.post("/mark_processed/<file_id>")
def mark_processed(file_id):
    move_file(file_id, current_app.config["GDRIVE_JOBDOCS_PROCESSED_ID"])
    return redirect(url_for("ui.index", ok="moved"))
