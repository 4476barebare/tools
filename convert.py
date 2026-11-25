import pathlib
import vtracer
from PIL import Image

src = pathlib.Path("images")
dst = pathlib.Path("svg")
dst.mkdir(exist_ok=True)

for img in list(src.glob("*.png")) + list(src.glob("*.jpg")):
    im = Image.open(img).convert("RGBA")
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)

    # 半透明のフチを白っぽい縁取りにしないため、透明度を二値化
    a = im.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    im.putalpha(a)

    tmp = dst / "_tmp.png"
    im.save(tmp)

    vtracer.convert_image_to_svg_py(
        str(tmp), str(dst / (img.stem + ".svg")),
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=2,
        color_precision=8,
        layer_difference=8,
        corner_threshold=60,
        length_threshold=4.0,
        splice_threshold=45,
        path_precision=3,
    )
    tmp.unlink()
    print("converted:", img.name)
