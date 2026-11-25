import pathlib
import vtracer
from PIL import Image

src = pathlib.Path("images")
dst = pathlib.Path("svg")
dst.mkdir(exist_ok=True)

for img in list(src.glob("*.png")) + list(src.glob("*.jpg")):
    # 白背景に合成して2倍に拡大
    im = Image.open(img).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    im = bg.convert("RGB").resize(
        (im.width * 2, im.height * 2), Image.LANCZOS
    )
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
