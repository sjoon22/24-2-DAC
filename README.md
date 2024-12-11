# PPT-Application: AI-Powered Position / Pose Reconstruction System


## background
With the rise of social media, the demand for advanced photo editing has grown, but most apps offer only basic features like cropping and brightness adjustment. PPT-Application addresses this with an AI-powered solution that transforms subject poses and positions within photos, providing seamless, creative, and precise photo reconstruction.

-------

Key Features:
- Automatically transforms the pose of a person in the image based on a reference pose image provided by the user.
- Repositions the pose-transformed subject to the desired location within the photo.

------
<br>

![inference](images/inference.png)  


-----
<br>

PPT-Application's base model is from 
[Roy et al. (2023)](https://arxiv.org/abs/2202.06777), [code](https://github.com/prasunroy/pose-transfer?tab=readme-ov-file), and we fine-tune it with an additional [dataset](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71704) for multiracial transformation.


## Demo


https://github.com/user-attachments/assets/c2608fdd-ea77-413a-86e9-1d0732d415db


## Citation

```bibtex
@article{roy2022multi,
  title   = {Multi-scale Attention Guided Pose Transfer},
  author  = {Roy, Prasun and Bhattacharya, Saumik and Ghosh, Subhankar and Pal, Umapada},
  journal = {Pattern Recognition},
  volume  = {137},
  pages   = {109315},
  year    = {2023},
  issn    = {0031-3203},
  doi     = {https://doi.org/10.1016/j.patcog.2023.109315}
}
```
