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

## 🏁 Conclusion and Future Work

The PPT-Application project aimed to develop an AI-powered system capable of transforming subject poses and naturally merging them into high-quality reconstructed images. In a society where the demand for personalized content creation and image editing efficiency is rapidly increasing, this project sought to revolutionize image editing quality and productivity.

### Key Outcomes
- Successfully implemented an **End-to-End Image Editing System** that enables users to transform subject poses and reposition them seamlessly within images.
- Utilized **BiRefNet** for precise segmentation and **Stability API-based Inpainting** to maintain high-resolution output with fast processing.

### Identified Limitations
1. **Domain Mismatch in Pose Transfer Models**  
   - DeepFashion dataset's bias towards Western-centric features led to suboptimal results when applied to Eastern facial features.
2. **Processing Speed Constraints**  
   - CPU-based processing significantly limited real-time usability, with an average processing time of 60 seconds per image.

### Recommendations for Overcoming Limitations
1. **Enhanced Data Diversity**  
   - Incorporate diverse datasets representing a wide range of facial features and body types to improve model generalization.
   - Fine-tune the Pose Transfer model with additional datasets focusing on underrepresented groups.
2. **Model Improvement**  
   - Transition from GAN-based models to cutting-edge **Diffusion Models** for improved pose transformation quality and adaptability.
3. **Hardware Optimization**  
   - Adopt GPU-based processing to drastically reduce processing time and enable near-real-time editing.
   - Explore cloud-based deployment with GPU support to make the application accessible to more users without local hardware constraints.

### Future Directions
- Continue developing the Pose Transfer model to better handle a variety of features and poses.
- Integrate real-time editing capabilities with GPU acceleration for improved user experience.
- Expand application functionality to support additional editing tasks such as multi-subject editing and advanced lighting adjustments.
- Explore potential partnerships with fashion, advertising, and content creation industries to adapt the application for professional workflows.

### Final Note
The PPT-Application project has demonstrated the transformative potential of AI-driven image editing technologies while highlighting the challenges of domain adaptation and processing efficiency. This project serves as an essential foundation for future innovations in personalized content creation and advanced editing tools.



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
