import streamlit as st
from ultralytics import YOLO
from PIL import Image
from pathlib import Path
import tempfile
import subprocess
import os
import cv2
import time
import io
import shutil


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Basketball Player Detection",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "best.pt"

OUTPUT_DIR = BASE_DIR / "outputs"
IMAGE_OUTPUT_DIR = OUTPUT_DIR / "images"
VIDEO_OUTPUT_DIR = OUTPUT_DIR / "videos"

IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# FFMPEG DETECTION
# ============================================================

FFMPEG_PATH = shutil.which("ffmpeg")

if FFMPEG_PATH is None:
    local_ffmpeg = Path(
        r"C:\Users\me\OneDrive - Faculty Of Engineering (Tanta University)"
        r"\Desktop\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"
    )

    if local_ffmpeg.exists():
        FFMPEG_PATH = str(local_ffmpeg)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None

    return YOLO(str(MODEL_PATH))


model = load_model()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏀 Basketball Player Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">YOLO11m — Object Detection Demo</div>',
    unsafe_allow_html=True
)


# ============================================================
# MODEL CHECK
# ============================================================

if model is None:
    st.error(
        f"❌ Model not found.\n\n"
        f"Expected:\n`{MODEL_PATH}`"
    )
    st.stop()


# ============================================================
# FFMPEG CHECK
# ============================================================

if FFMPEG_PATH is None:
    st.warning(
        "⚠️ FFmpeg was not found. "
        "Video conversion may not be available."
    )
else:
    st.success("✅ FFmpeg detected")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Detection Settings")

    confidence = st.slider(
        "Confidence Threshold",
        min_value=0.05,
        max_value=0.95,
        value=0.25,
        step=0.05
    )

    iou = st.slider(
        "IoU Threshold",
        min_value=0.10,
        max_value=0.90,
        value=0.50,
        step=0.05
    )

    st.divider()

    st.subheader("🎥 Video Settings")

    frame_skip = st.selectbox(
        "Process every N frames",
        options=[1, 2, 3],
        index=0,
        help=(
            "1 = process every frame\n"
            "2 = process every second frame\n"
            "3 = process every third frame"
        )
    )

    video_width = st.selectbox(
        "Output Width",
        options=[None, 640, 768, 960, 1280],
        index=0,
        format_func=lambda x:
            "Original" if x is None else f"{x}px"
    )

    st.divider()

    st.subheader("📦 Model Information")

    st.write("**Model:** YOLO11m")
    st.write(f"**File:** `{MODEL_PATH.name}`")

    if MODEL_PATH.exists():
        size_mb = (
            MODEL_PATH.stat().st_size
            / (1024 * 1024)
        )

        st.write(
            f"**Size:** {size_mb:.2f} MB"
        )

    st.divider()

    st.subheader("🎯 Classes")

    for class_id, class_name in model.names.items():
        st.write(
            f"`{class_id}` — {class_name}"
        )


# ============================================================
# TABS
# ============================================================

image_tab, video_tab = st.tabs(
    [
        "🖼️ Image Detection",
        "🎥 Video Detection"
    ]
)


# ============================================================
# IMAGE DETECTION
# ============================================================

with image_tab:

    st.markdown(
        '<div class="section-title">'
        '🖼️ Upload Basketball Images'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_images = st.file_uploader(
        "Choose one or more images",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],
        accept_multiple_files=True,
        key="image_uploader"
    )

    if uploaded_images:

        st.success(
            f"✅ {len(uploaded_images)} image(s) uploaded"
        )

        st.subheader("👀 Preview")

        preview_columns = st.columns(
            min(3, len(uploaded_images))
        )

        for i, uploaded_file in enumerate(
            uploaded_images
        ):

            image = Image.open(uploaded_file)

            with preview_columns[
                i % len(preview_columns)
            ]:

                st.image(
                    image,
                    caption=uploaded_file.name,
                    use_container_width=True
                )

        st.divider()

        run_images = st.button(
            "🚀 Run Image Detection",
            type="primary",
            key="run_images"
        )

        if run_images:

            progress_bar = st.progress(0)
            status = st.empty()

            results_data = []

            for index, uploaded_file in enumerate(
                uploaded_images
            ):

                status.write(
                    f"🔍 Processing: "
                    f"`{uploaded_file.name}`"
                )

                image_bytes = uploaded_file.getvalue()

                image = Image.open(
                    io.BytesIO(image_bytes)
                ).convert("RGB")

                start_time = time.time()

                results = model.predict(
                    source=image,
                    conf=confidence,
                    iou=iou,
                    verbose=False
                )

                inference_time = (
                    time.time() - start_time
                )

                result = results[0]

                annotated = result.plot()

                annotated_rgb = cv2.cvtColor(
                    annotated,
                    cv2.COLOR_BGR2RGB
                )

                output_path = (
                    IMAGE_OUTPUT_DIR
                    / f"detected_{uploaded_file.name}"
                )

                cv2.imwrite(
                    str(output_path),
                    annotated
                )

                detection_count = 0

                if result.boxes is not None:
                    detection_count = len(
                        result.boxes
                    )

                results_data.append(
                    {
                        "name": uploaded_file.name,
                        "image": annotated_rgb,
                        "detections": detection_count,
                        "time": inference_time,
                        "path": output_path
                    }
                )

                progress_bar.progress(
                    (index + 1)
                    / len(uploaded_images)
                )

            status.success(
                "✅ Image detection completed!"
            )

            st.subheader(
                "🎯 Detection Results"
            )

            for result_data in results_data:

                st.markdown(
                    f"### 📷 "
                    f"{result_data['name']}"
                )

                col1, col2 = st.columns(
                    [3, 1]
                )

                with col1:

                    st.image(
                        result_data["image"],
                        caption="YOLO Detection",
                        use_container_width=True
                    )

                with col2:

                    st.metric(
                        "Objects",
                        result_data["detections"]
                    )

                    st.metric(
                        "Inference",
                        f"{result_data['time']:.3f}s"
                    )

                    with open(
                        result_data["path"],
                        "rb"
                    ) as file:

                        st.download_button(
                            "⬇️ Download Result",
                            data=file.read(),
                            file_name=(
                                result_data["path"].name
                            ),
                            mime="image/jpeg",
                            key=(
                                f"download_"
                                f"{result_data['name']}"
                            )
                        )

                st.divider()


# ============================================================
# VIDEO CONVERSION
# ============================================================

def convert_to_browser_mp4(
    input_path,
    output_path
):

    if FFMPEG_PATH is None:
        return False, (
            "FFmpeg executable was not found."
        )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i",
        str(input_path),

        "-c:v",
        "libx264",

        "-preset",
        "fast",

        "-crf",
        "23",

        "-pix_fmt",
        "yuv420p",

        "-c:a",
        "aac",

        "-b:a",
        "128k",

        "-movflags",
        "+faststart",

        str(output_path)
    ]

    try:

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode == 0:
            return True, ""

        return False, process.stderr

    except Exception as e:
        return False, str(e)


# ============================================================
# VIDEO DETECTION
# ============================================================

with video_tab:

    st.markdown(
        '<div class="section-title">'
        '🎥 Upload Basketball Videos'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_videos = st.file_uploader(
        "Choose one or more videos",
        type=[
            "mp4",
            "avi",
            "mov",
            "mkv",
            "webm"
        ],
        accept_multiple_files=True,
        key="video_uploader"
    )

    if uploaded_videos:

        st.success(
            f"✅ {len(uploaded_videos)} video(s) uploaded"
        )

        st.subheader("📊 Video Information")

        for uploaded_file in uploaded_videos:

            file_size_mb = (
                len(uploaded_file.getvalue())
                / (1024 * 1024)
            )

            st.write(
                f"🎥 **{uploaded_file.name}** — "
                f"{file_size_mb:.2f} MB"
            )

        st.divider()

        run_videos = st.button(
            "🚀 Run Video Detection",
            type="primary",
            key="run_videos"
        )

        if run_videos:

            for video_index, uploaded_file in enumerate(
                uploaded_videos
            ):

                st.markdown(
                    f"## 🎥 {uploaded_file.name}"
                )

                input_suffix = Path(
                    uploaded_file.name
                ).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=input_suffix
                ) as temp_input:

                    temp_input.write(
                        uploaded_file.getvalue()
                    )

                    input_path = temp_input.name

                cap = cv2.VideoCapture(
                    input_path
                )

                if not cap.isOpened():

                    st.error(
                        "❌ Could not open video."
                    )

                    try:
                        os.unlink(input_path)
                    except OSError:
                        pass

                    continue

                fps = cap.get(
                    cv2.CAP_PROP_FPS
                )

                if fps <= 0:
                    fps = 30.0

                total_frames = int(
                    cap.get(
                        cv2.CAP_PROP_FRAME_COUNT
                    )
                )

                original_width = int(
                    cap.get(
                        cv2.CAP_PROP_FRAME_WIDTH
                    )
                )

                original_height = int(
                    cap.get(
                        cv2.CAP_PROP_FRAME_HEIGHT
                    )
                )

                duration = (
                    total_frames / fps
                    if fps > 0
                    else 0
                )

                st.write(
                    f"Resolution: "
                    f"**{original_width}×"
                    f"{original_height}**"
                )

                st.write(
                    f"FPS: **{fps:.2f}**"
                )

                st.write(
                    f"Duration: **{duration:.2f}s**"
                )

                output_width = (
                    video_width
                    if video_width is not None
                    else original_width
                )

                output_height = int(
                    original_height
                    * (
                        output_width
                        / original_width
                    )
                )

                output_width -= (
                    output_width % 2
                )

                output_height -= (
                    output_height % 2
                )

                temp_yolo_output = (
                    VIDEO_OUTPUT_DIR
                    / (
                        Path(uploaded_file.name).stem
                        + "_yolo_temp.mp4"
                    )
                )

                final_output = (
                    VIDEO_OUTPUT_DIR
                    / (
                        Path(uploaded_file.name).stem
                        + "_detected.mp4"
                    )
                )

                fourcc = cv2.VideoWriter_fourcc(
                    *"mp4v"
                )

                writer = cv2.VideoWriter(
                    str(temp_yolo_output),
                    fourcc,
                    fps,
                    (
                        output_width,
                        output_height
                    )
                )

                if not writer.isOpened():

                    st.error(
                        "❌ Could not create "
                        "temporary output video."
                    )

                    cap.release()

                    try:
                        os.unlink(input_path)
                    except OSError:
                        pass

                    continue

                progress = st.progress(0)
                status = st.empty()

                frame_number = 0
                processed_frames = 0

                start_time = time.time()

                last_annotated = None

                while True:

                    success, frame = cap.read()

                    if not success:
                        break

                    if frame_number % frame_skip == 0:

                        results = model.predict(
                            source=frame,
                            conf=confidence,
                            iou=iou,
                            verbose=False
                        )

                        result = results[0]

                        annotated = result.plot()

                        if (
                            annotated.shape[1]
                            != output_width
                            or
                            annotated.shape[0]
                            != output_height
                        ):

                            annotated = cv2.resize(
                                annotated,
                                (
                                    output_width,
                                    output_height
                                ),
                                interpolation=cv2.INTER_LINEAR
                            )

                        last_annotated = annotated

                        processed_frames += 1

                    else:

                        if last_annotated is not None:

                            annotated = last_annotated

                        else:

                            annotated = cv2.resize(
                                frame,
                                (
                                    output_width,
                                    output_height
                                )
                            )

                    writer.write(
                        annotated
                    )

                    frame_number += 1

                    if total_frames > 0:

                        progress_value = (
                            frame_number
                            / total_frames
                        )

                        progress.progress(
                            min(
                                progress_value,
                                1.0
                            )
                        )

                    elapsed = (
                        time.time()
                        - start_time
                    )

                    processing_fps = (
                        frame_number / elapsed
                        if elapsed > 0
                        else 0
                    )

                    status.write(
                        f"Processing frame "
                        f"{frame_number}/"
                        f"{total_frames} "
                        f"| "
                        f"{processing_fps:.1f} FPS"
                    )

                cap.release()
                writer.release()

                elapsed_total = (
                    time.time()
                    - start_time
                )

                progress.progress(1.0)

                status.success(
                    "✅ YOLO detection completed!"
                )

                st.success(
                    f"Processed "
                    f"{processed_frames:,} frames "
                    f"in "
                    f"{elapsed_total:.2f} seconds."
                )

                if FFMPEG_PATH is None:

                    st.error(
                        "❌ FFmpeg is not available. "
                        "The video cannot be converted "
                        "to browser-compatible H.264."
                    )

                    if temp_yolo_output.exists():

                        with open(
                            temp_yolo_output,
                            "rb"
                        ) as f:

                            fallback_bytes = f.read()

                        st.download_button(
                            "⬇️ Download YOLO Video",
                            data=fallback_bytes,
                            file_name=(
                                temp_yolo_output.name
                            ),
                            mime="video/mp4",
                            key=(
                                f"fallback_"
                                f"{video_index}"
                            )
                        )

                else:

                    st.info(
                        "🎞️ Converting video to "
                        "browser-compatible H.264..."
                    )

                    conversion_start = time.time()

                    success, error_message = (
                        convert_to_browser_mp4(
                            temp_yolo_output,
                            final_output
                        )
                    )

                    conversion_time = (
                        time.time()
                        - conversion_start
                    )

                    if not success:

                        st.error(
                            "❌ H.264 conversion failed."
                        )

                        st.code(
                            error_message,
                            language="text"
                        )

                    else:

                        st.success(
                            "✅ Video converted successfully "
                            f"in {conversion_time:.2f}s"
                        )

                        st.subheader(
                            "🎯 Detection Result"
                        )

                        with open(
                            final_output,
                            "rb"
                        ) as video_file:

                            video_bytes = (
                                video_file.read()
                            )

                        st.video(
                            video_bytes,
                            format="video/mp4",
                            autoplay=False,
                            muted=False
                        )

                        st.success(
                            "🎬 Detection result is ready — "
                            "press ▶️ to play it directly "
                            "inside Streamlit."
                        )

                        st.download_button(
                            label="⬇️ Download Detected Video",
                            data=video_bytes,
                            file_name=(
                                final_output.name
                            ),
                            mime="video/mp4",
                            key=(
                                f"video_download_"
                                f"{video_index}"
                            )
                        )

                try:
                    os.unlink(input_path)
                except OSError:
                    pass

                try:
                    if temp_yolo_output.exists():
                        temp_yolo_output.unlink()
                except OSError:
                    pass

                st.divider()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        🏀 Basketball Player Detection<br>
        YOLO11m • Computer Vision • Object Detection
    </div>
    """,
    unsafe_allow_html=True
)