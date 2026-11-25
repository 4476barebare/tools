import pathlib
import vtracer

src = pathlib.Path("images")
dst = pathlib.Path("svg")
dst.mkdir(exist_ok=True)

for img in list(src.glob("*.png")) + list(src.glob("*.jpg")):
    out = dst / (img.stem + ".svg")
    vtracer.convert_image_to_svg_py(
        str(img), str(out),
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=4,
        color_precision=6,
        layer_difference=16,
        path_precision=3,
    )
    print("converted:", img.name)
