import unittest

import numpy as np
from scipy.ndimage import rotate
from tifffile import imread
import Labeling as lb


class LabelingTests(unittest.TestCase):

    def test1(self):
        example2_images = [np.invert(imread("tutorial/up_big.tif"))]
        example2_images[0][example2_images[0] > 0] = 130
        example2_images.append(
            rotate(np.transpose(np.flip(example2_images[0]).copy()), angle=45, reshape=False, mode="constant", cval=0))
        example2_images[1][example2_images[1] > 0] = 131
        example2_images.append(np.transpose(np.flip(example2_images[0]).copy()))
        example2_images[2][example2_images[2] > 0] = 132
        example2_images.append(
            rotate(np.flip(example2_images[0]).copy(), angle=45, reshape=False, mode="constant", cval=0))
        example2_images[3][example2_images[3] > 0] = 133
        example2_images.append(np.flip(example2_images[0]).copy())
        example2_images[4][example2_images[4] > 0] = 134
        example2_images.append(
            rotate(np.transpose(example2_images[0]).copy(), angle=45, reshape=False, mode="constant", cval=0))
        example2_images[5][example2_images[5] > 0] = 135
        example2_images.append(np.transpose(example2_images[0]).copy())
        example2_images[6][example2_images[6] > 0] = 136
        example2_images.append(rotate(example2_images[0], angle=45, reshape=False, mode="constant", cval=0))
        example2_images[7][example2_images[7] > 0] = 137

        merger = lb.Labeling.fromValues(np.zeros((512, 512), np.int32))
        merger.iterate_over_images(example2_images, [str(i) for i in list(range(1, len(example2_images) + 1))])
        img, labeling2 = merger.save_result("example2")
        self.assertListEqual([str(i) for i in list(np.unique(img))], list(labeling2.labelSets.keys()))
        self.assertEqual(len(set([item for sublist in labeling2.labelSets.values() for item in sublist])),
                         len(example2_images))

    def test2(self):
        image = np.ones((3,3))
        labeling = lb.Labeling.fromValues(np.zeros((3, 3), np.int32))
        for i in range(5):
            labeling.add_image(image, str(i))

        img, labeling = labeling.get_result()
        print(img)
        print(vars(labeling))

    def test3(self):
        image = np.ones((3,3))
        labeling = lb.Labeling.fromValues(np.zeros((3, 3), np.int32))
        for i in range(1,5):
            image[0] = i*3
            image[1] = i*3 + 1
            image[2] = i*3 + 2
            labeling.add_image(image, str(i))

        img, labeling = labeling.get_result()
        print(img)
        print(vars(labeling))

    def test4(self):
        image = np.ones((3,3))
        labeling = lb.Labeling.fromValues(np.zeros((3, 3), np.int32))
        for i in range(1,5):
            image[1] = image[1] + 1
            image[2] = image[2] + 2
            labeling.add_image(image, str(i))

        img, labeling = labeling.get_result()
        print(img)
        print(vars(labeling))



if __name__ == '__main__':
    unittest.main()
