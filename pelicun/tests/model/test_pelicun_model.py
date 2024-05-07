# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Leland Stanford Junior University
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of pelicun.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# You should have received a copy of the BSD 3-Clause License along with
# pelicun. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Adam Zsarnóczay
# John Vouvakis Manousakis

"""
These are unit and integration tests on the model module of pelicun.
"""

import os
import tempfile
from copy import deepcopy
import pytest
import numpy as np
import pandas as pd
from pelicun import model
from pelicun import assessment

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=arguments-renamed

# class TestPelicunModel(TestModelModule):
#     @pytest.fixture
#     def pelicun_model(self, assessment_instance):
#         return deepcopy(model.PelicunModel(assessment_instance))

#     def test_init(self, pelicun_model):
#         assert pelicun_model.log_msg
#         assert pelicun_model.log_div

#     def test_convert_marginal_params(self, pelicun_model):
#         # one row, only Theta_0, no conversion
#         marginal_params = pd.DataFrame(
#             [['1.0']],
#             columns=['Theta_0'],
#             index=pd.MultiIndex.from_tuples(
#                 (('A', '0', '1'),), names=('cmp', 'loc', 'dir')
#             ),
#         )
#         units = pd.Series(['ea'], index=marginal_params.index)
#         arg_units = None
#         res = pelicun_model.convert_marginal_params(
#             marginal_params, units, arg_units
#         )

#         # >>> res
#         #             Theta_0
#         # cmp loc dir
#         # A   0   1       1.0

#         assert 'Theta_0' in res.columns
#         assert res.to_dict() == {'Theta_0': {('A', '0', '1'): 1.0}}

#         # many rows, with conversions
#         marginal_params = pd.DataFrame(
#             [
#                 [np.nan, 1.0, np.nan, np.nan, np.nan, np.nan],
#                 ['normal', np.nan, 1.0, np.nan, -0.50, 0.50],
#                 ['lognormal', 1.0, 0.5, np.nan, 0.50, 1.50],
#                 ['uniform', 0.0, 10.0, np.nan, np.nan, np.nan],
#             ],
#             columns=[
#                 'Family',
#                 'Theta_0',
#                 'Theta_1',
#                 'Theta_2',
#                 'TruncateLower',
#                 'TruncateUpper',
#             ],
#             index=pd.MultiIndex.from_tuples(
#                 (
#                     ('A', '0', '1'),
#                     ('B', '0', '1'),
#                     ('C', '0', '1'),
#                     ('D', '0', '1'),
#                 ),
#                 names=('cmp', 'loc', 'dir'),
#             ),
#         )
#         units = pd.Series(['ea', 'ft', 'in', 'in2'], index=marginal_params.index)
#         arg_units = None
#         res = pelicun_model.convert_marginal_params(
#             marginal_params, units, arg_units
#         )

#         expected_df = pd.DataFrame(
#             {
#                 'Family': [np.nan, 'normal', 'lognormal', 'uniform'],
#                 'Theta_0': [1.0000, np.nan, 0.0254, 0.0000],
#                 'Theta_1': [np.nan, 1.000000, 0.500000, 0.0064516],
#                 'Theta_2': [np.nan, np.nan, np.nan, np.nan],
#                 'TruncateLower': [np.nan, -0.1524, 0.0127, np.nan],
#                 'TruncateUpper': [np.nan, 0.1524, 0.0381, np.nan],
#             },
#             index=pd.MultiIndex.from_tuples(
#                 (
#                     ('A', '0', '1'),
#                     ('B', '0', '1'),
#                     ('C', '0', '1'),
#                     ('D', '0', '1'),
#                 ),
#                 names=('cmp', 'loc', 'dir'),
#             ),
#         )

#         pd.testing.assert_frame_equal(
#             expected_df, res, check_index_type=False, check_column_type=False
#         )

#         # a case with arg_units
#         marginal_params = pd.DataFrame(
#             [['500.0,400.00|20,10']],
#             columns=['Theta_0'],
#             index=pd.MultiIndex.from_tuples(
#                 (('A', '0', '1'),), names=('cmp', 'loc', 'dir')
#             ),
#         )
#         units = pd.Series(['test_three'], index=marginal_params.index)
#         arg_units = pd.Series(['test_two'], index=marginal_params.index)
#         res = pelicun_model.convert_marginal_params(
#             marginal_params, units, arg_units
#         )

#         # >>> res
#         #                              Theta_0
#         # cmp loc dir
#         # A   0   1    750,600|40,20

#         # note: '40,20' = '20,10' * 2.00 (test_two)
#         # note: '750,600' = '500,400' * 3.00 / 2.00 (test_three/test_two)

#         expected_df = pd.DataFrame(
#             {
#                 'Theta_0': ['750,600|40,20'],
#             },
#             index=pd.MultiIndex.from_tuples(
#                 (('A', '0', '1'),),
#                 names=('cmp', 'loc', 'dir'),
#             ),
#         )
#         pd.testing.assert_frame_equal(
#             expected_df, res, check_index_type=False, check_column_type=False
#         )
