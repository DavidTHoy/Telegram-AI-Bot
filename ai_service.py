from PIL import Image
from helper_functions import add_html_formatting, split_text
from pipelines import get_summarizer_pipe, get_stable_diffusion_pipe


class AiService:
    STABLE_DIFF_PIPE = None  # get_stable_diffusion_pipe()
    SUMMARIZER_PIPE = get_summarizer_pipe()

    @staticmethod
    def summarize_text(text):
        if len(text) >= 4500:
            all_text_bat = split_text(text)
        else:
            all_text_bat = [text]
        summarized_list_text = [f.get('summary_text') for f in
                                AiService.SUMMARIZER_PIPE(all_text_bat, max_length=1024, do_sample=False,
                                                          truncation=True)]
        return add_html_formatting(summarized_list_text)

    @staticmethod
    def generate_image(prompt, num_images=3, guidance_scale=7.5, num_inference_steps=30, rows=1, cols=3):
        images = AiService.STABLE_DIFF_PIPE([prompt] * num_images, guidance_scale=guidance_scale,
                                            num_inference_steps=num_inference_steps).images
        return AiService.image_grid(images, rows=rows, cols=cols)

    @staticmethod
    def image_grid(imgs, rows, cols):
        assert len(imgs) == rows * cols
        w, h = imgs[0].size
        grid = Image.new('RGB', size=(cols * w, rows * h))
        for i, img in enumerate(imgs):
            grid.paste(img, box=(i % cols * w, i // cols * h))
        return grid
