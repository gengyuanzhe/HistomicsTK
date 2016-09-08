#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from tests import base

import numpy as np
import os
import skimage.io

from histomicstk.preprocessing import color_conversion
from histomicstk.preprocessing import color_normalization


# boiler plate to start and stop the server if needed
def setUpModule():
    base.enabledPlugins.append('HistomicsTK')
    base.startServer()


def tearDownModule():
    base.stopServer()


TEST_DATA_DIR = os.path.join(os.environ['GIRDER_TEST_DATA_PREFIX'],
                             'plugins/HistomicsTK')


class ReinhardNormalizationTest(base.TestCase):

    def test_normalization(self):

        inputImageFile = os.path.join(TEST_DATA_DIR, 'L1.png')

        refImageFile = os.path.join(TEST_DATA_DIR, 'Easy1.png')

        # read input image
        imInput = skimage.io.imread(inputImageFile)[:, :, :3]

        # read reference image
        imReference = skimage.io.imread(refImageFile)[:, :, :3]

        # get mean and stddev of reference image in lab space
        meanRef, stdRef = color_conversion.lab_mean_std(imReference)

        # perform color normalization
        imNmzd = color_normalization.reinhard(imInput, meanRef, stdRef)

        # transform normalized image to LAB color space
        meanNmzd, stdNmzd = color_conversion.lab_mean_std(imNmzd)

        # check if mean and stddev of normalized and reference images are equal
        np.testing.assert_allclose(meanNmzd, meanRef, atol=1e-1)
        np.testing.assert_allclose(stdNmzd, stdRef, atol=1e-1)
