# PPT-Application: AI-Powered Position / Pose Reconstruction System

### 🚀 Project Summary
PPT-Application is an AI-powered image editing tool that allows users to seamlessly modify subject poses and positions in photos. This cutting-edge solution goes beyond traditional photo editing features to offer an intuitive, high-quality experience for both individual and professional users.

-------

### Key Features
- **Pose Transfer**: Automatically modifies a person's pose based on a reference image.
- **Inpainting**: Smoothly fills background after separating the subject.
- **Repositioning**: Places the pose-modified subject into a specified location within the image.

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
