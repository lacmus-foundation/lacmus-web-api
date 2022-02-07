import io
import os
import time
from typing import List

from PIL import Image
import torch

from core.config import WorkerConfig, get_config
from core.api_models.common import Prediction

class Model:
  def __init__(self) -> None:
    config = get_config()
    assert os.path.isfile(config.weights), f"no such file: {config.weights}"
    assert config.iou != None, "iou is None"
    assert config.conf != None, "conf is None"
    assert config.labels != None, "labels is none"
    self.config = config
    self.model = None

  def load(self) -> None:
    self.model = torch.hub.load('./model/yolov5/','custom', source='local',autoshape=True,
                           path=self.config.weights)
    self.model.iou = self.config.iou
    self.model.conf = self.config.conf


  async def infer(self, in_data: bytes) -> List[Prediction]:
    # pre-processing
    img = Image.open(io.BytesIO(in_data))

    # inference
    start_time = time.time()
    result_pandas = self.model(img, size=1984).pandas().xyxy[0]
    print("done in {} s".format(time.time() - start_time), flush=True)

    result_bboxes = [Prediction(xmin=r[1]['xmin'], ymin=r[1]['ymin'],xmax= r[1]['xmax'],ymax= r[1]['ymax'],
                score= r[1]['confidence'],label= r[1]['name'])
     for r in result_pandas.iterrows()]
    return result_bboxes