from api import Pose2Pose
from PIL import Image
import os


p2p = Pose2Pose(pretrained=False)


ckpt_dir = '../output/AsianDeepFashion/ckpt/pretrined'
ckpt_id = 260500
p2p.renderer.load_networks(ckpt_dir, ckpt_id, verbose=True)


conditiondataset_dir = '../datasets/inference/condition'
referencedataset_dir = '../datasets/inference/reference'
save_dir = '../datasets/inference/output'


from api import Pose2Pose
from PIL import Image
import os


p2p = Pose2Pose(pretrained=False)


ckpt_dir = '../output/AsianDeepFashion/ckpt/24'
ckpt_id = 139000
p2p.renderer.load_networks(ckpt_dir, ckpt_id, verbose=True)


conditiondataset_dir = '../datasets/inference/condition'
referencedataset_dir = '../datasets/inference/reference'
save_dir = '../datasets/inference/output'


os.makedirs(save_dir, exist_ok=True)


def filter_jpg_files(directory):
    return [file for file in os.listdir(directory) if file.endswith('.jpg')]

conditions = filter_jpg_files(conditiondataset_dir)
references = filter_jpg_files(referencedataset_dir)


for i in range(min(9, len(conditions), len(references))):
    try:

        condition_path = os.path.join(conditiondataset_dir, conditions[i])
        reference_path = os.path.join(referencedataset_dir, references[i])

        condition = Image.open(condition_path).convert('RGB')  
        reference = Image.open(reference_path).convert('RGB')  


        generated = p2p.transfer_as(condition, reference)


        save_path = os.path.join(save_dir, f"generated_{i+1}.jpg")
        generated.save(save_path)
        print(f"Saved: {save_path}")
    except Exception as e:
        print(f"Error processing {conditions[i]} and {references[i]}: {e}")
~
