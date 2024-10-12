#
# Copyright (c) 2018 Leland Stanford Junior University
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of the SimCenter Backend Applications
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
# this file. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Adam Zsarnóczay
# Kuanshi Zhong
#
# Based on rulesets developed by:
# Karen Angeles
# Meredith Lockhead
# Tracy Kijewski-Correa

import random


def CECB_config(bim: dict) -> str:  # noqa: C901
    """
    Rules to identify a HAZUS CECB configuration based on BIM data.

    Parameters
    ----------
    BIM: dictionary
        Information about the building characteristics.

    Returns
    -------
    config: str
        A string that identifies a specific configuration within this
        building class.

    """
    year = bim['YearBuilt']  # just for the sake of brevity

    # Roof cover
    if bim['RoofShape'] in {'gab', 'hip'}:
        roof_cover = 'bur'
        # Warning: HAZUS does not have N/A option for CECB, so here we use bur
    elif year >= 1975:
        roof_cover = 'spm'
    else:
        # year < 1975
        roof_cover = 'bur'

    # shutters
    if year >= 2000:
        shutters = bim['WindBorneDebris']
    # BOCA 1996 and earlier:
    # Shutters were not required by code until the 2000 IBC. Before 2000, the
    # percentage of commercial buildings that have shutters is assumed to be
    # 46%. This value is based on a study on preparedness of small businesses
    # for hurricane disasters, which says that in Sarasota County, 46% of
    # business owners had taken action to wind-proof or flood-proof their
    # facilities. In addition to that, 46% of business owners reported boarding
    # up their businesses before Hurricane Katrina. In addition, compliance
    # rates based on the Homeowners Survey data hover between 43 and 50 percent.
    elif bim['WindBorneDebris']:
        shutters = random.random() < 0.46
    else:
        shutters = False

    # Wind Debris (widd in HAZSU)
    # HAZUS A: Res/Comm, B: Varies by direction, C: Residential, D: None
    widd = 'C'  # residential (default)
    if bim['OccupancyClass'] in {'RES1', 'RES2', 'RES3A', 'RES3B', 'RES3C', 'RES3D'}:
        widd = 'C'  # residential
    elif bim['OccupancyClass'] == 'AGR1':
        widd = 'D'  # None
    else:
        widd = 'A'  # Res/Comm

    # Window area ratio
    if bim['WindowArea'] < 0.33:
        wwr = 'low'
    elif bim['WindowArea'] < 0.5:
        wwr = 'med'
    else:
        wwr = 'hig'

    if bim['NumberOfStories'] <= 2:
        bldg_tag = 'C.ECB.L'
    elif bim['NumberOfStories'] <= 5:
        bldg_tag = 'C.ECB.M'
    else:
        bldg_tag = 'C.ECB.H'

    # extend the BIM dictionary
    bim.update(
        {
            'RoofCover': roof_cover,
            'Shutters': shutters,
            'WindowAreaRatio': wwr,
            'WindDebrisClass': widd,
        }
    )

    return (
        f"{bldg_tag}."
        f"{roof_cover}."
        f"{int(shutters)}."
        f"{widd}."
        f"{wwr}."
        f"{int(bim['TerrainRoughness'])}"
    )
