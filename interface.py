try:
    import streamlit as st
    import cv2
    from PIL import Image
    from detectron2.utils.visualizer import Visualizer
    from detectron2.data import MetadataCatalog

    st.set_page_config(
        page_title="Image Captioning",
        page_icon="📝",
        layout="wide",
    )

    import sys

    sys.path.insert(1, 'Projet_master')
    import modele as md
except Exception as ex:
    st.write(f"Modules are missing {ex}")


@st.cache(allow_output_mutation=True)
def load_captioning_model():
    return md.get_captionning_model()


@st.cache(allow_output_mutation=True)
def load_segmentation_model():
    return md.get_segmentation_model()


seg_model = load_segmentation_model()
cap_model = load_captioning_model()


# color has to be either red, blue, green, orange or violet
def colored_sentece(sentece, colour) -> str:
    return f":{colour}[{sentece}]"


# premier model
def apply_segmentation_model(image, min_boxes, max_boxes):
    boxes, features, proba_cls, instances = md.segment_picture(seg_model, image, MIN_BOXES=min_boxes, MAX_BOXES=max_boxes)
    return boxes, features, proba_cls, instances


def show_boxes(original_image, cv2_image, column, min_boxes, max_boxes):
    boxes, features, proba_cls, instances = apply_segmentation_model(cv2_image, min_boxes, max_boxes)
    pred = instances.to('cpu')
    box_image = Visualizer(original_image, MetadataCatalog.get("vg"), 1)
    box_image = box_image.draw_instance_predictions(instances)
    column.image(box_image.get_image())
    return boxes, features, proba_cls, instances


# second model (a partir des bounding box ?)
def show_caption(model, features, proba_cls, max_detection=50, beam_size=5, max_len=20, out_size=5,place=st):
    ret = md.caption_segmentation(model, features, proba_cls, max_detections=max_detection, beam_size=beam_size, max_len=max_len, out_size=out_size)
    for s, p in ret:
        place.markdown(f"<i><h3>{s}</h3></i>", unsafe_allow_html=True)  # TODO faire un affichage stat des "p" élevé à l'exponentielle


def main():
    st.title("Image captioning application")
    uploaded_image = st.file_uploader("Upload your image", help="Chose an image to caption")

    if uploaded_image is not None:
        tab1, tab2 = st.tabs(["Parameters", "Segmentation and caption"])
        tab1.write("Parameters of the caption")
        beam_size = tab1.slider('Size of the beam search', 1, 20, 5)
        out_size = tab1.slider('How many caption do you want ?', 1, 5, 1)
        min_boxes = tab1.slider('Minimum numbers of boxes generated by the segmentation', 3, 40, 10)
        max_boxes = tab1.slider('Maximum numbers of boxes generated by the segmentation', min_boxes, 100, min_boxes)
        max_len = tab1.slider('maximum length of the caption', 1, 25,
                            10)  # TODO reformuler les phrase de maniere plus courte plutot que de les couper

        # prétaitement sur l'image avant de la passée ?
        col1, col2 = tab2.columns(2)
        col1.subheader("This is the original image")
        original_image = Image.open(uploaded_image)
        img = original_image.save('img.jpg')  # pour pouvoir read l'image avec CV2
        img = cv2.imread("img.jpg")
        col1.image(original_image)

        caption_btn = col1.button("Caption this image !")
        if caption_btn:
            col2.subheader("Image with bounding boxes")
            boxes, features, proba_cls, instances = show_boxes(original_image, img, col2, min_boxes, max_boxes)
            show_caption(model=cap_model, features=features, proba_cls=proba_cls, max_detection=100,
                         beam_size=beam_size, max_len=max_len, out_size=out_size, place=col2)


if __name__ == "__main__":
    main()
