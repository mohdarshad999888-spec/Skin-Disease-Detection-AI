import os
import cv2

def generate_heatmap(img_path):

    # =========================
    # READ IMAGE
    # =========================

    img = cv2.imread(img_path)

    if img is None:
        return ""

    # =========================
    # RESIZE IMAGE
    # =========================

    img = cv2.resize(
        img,
        (300, 300)
    )

    # =========================
    # GRAYSCALE
    # =========================

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # =========================
    # APPLY HEATMAP
    # =========================

    heatmap = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    # =========================
    # BLEND ORIGINAL + HEATMAP
    # =========================

    blended = cv2.addWeighted(
        img,
        0.4,
        heatmap,
        0.6,
        0
    )

    # =========================
    # SAVE FOLDER
    # =========================

    heatmap_folder = os.path.join(
        os.getcwd(),
        "uploads",
        "heatmap"
    )

    os.makedirs(
        heatmap_folder,
        exist_ok=True
    )

    # =========================
    # OUTPUT PATH
    # =========================

    filename = os.path.basename(
        img_path
    )

    output_path = os.path.join(
        heatmap_folder,
        filename
    )

    # =========================
    # SAVE IMAGE
    # =========================

    cv2.imwrite(
        output_path,
        blended
    )

    # =========================
    # RETURN RELATIVE PATH
    # =========================

    return (
        "uploads/heatmap/"
        + filename
    )