try:
    import streamlit as st
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
except Exception as ex:
    st.write(f"Modules are missing {ex}")

st.set_page_config(
    page_title="Image Captioning",
    page_icon="📝",
    layout="wide",
)


@st.cache(allow_output_mutation=True)
def load_model(model_path):
    pass


# color has to be either red, blue, green, orange or violet
def colored_sentece(sentece, colour) -> str:
    return f":{colour}[{sentece}]"


# premier model
def apply_model(image):
    pass


def show_boxes(image_with_boxes):
    st.image(image_with_boxes)


# second model (a partir des bounding box ?)
def show_caption(text):
    st.write(text)


def main():
    st.title("Image captioning application")
    uploaded_image = st.file_uploader("Upload your image", help="Chose an image to caption")

    if uploaded_image is not None:
        # prétaitement sur l'image avant de la passée ?
        st.subheader("This is the original image")
        st.image(uploaded_image)

        caption_btn = st.button("Caption this image !")
        if caption_btn:
            st.subheader("Image with bounding boxes")
            show_boxes(uploaded_image)
            st.subheader("caption of this image")
            show_caption("click")


if __name__ == "__main__":
    main()
