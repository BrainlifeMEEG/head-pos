"""
Compute time-varying head positions from cHPI and save them in a .pos file.

This app loads a raw MEG file containing cHPI info, computes cHPI
amplitudes and coil locations over time, derives time-varying head
positions, and saves them.

Inputs:
    - fif: Path to MNE raw .fif file containing cHPI info
    - param_compute_amplitudes_t_step_min: Minimum time step to use to compute cHPI amplitudes. Default is 0.01.
    - param_compute_amplitudes_t_window: Time window to use to estimate the amplitudes. Default is 0.2 (200 ms).
    - param_compute_amplitudes_ext_order: External order for SSS-like interference suppression. Default is 1.
    - param_compute_amplitudes_tmin: Start time in seconds to compute cHPI amplitudes. Default is 0.
    - param_compute_amplitudes_tmax: End time in seconds to compute cHPI amplitudes. Default is None.
    - param_compute_locs_t_step_max: Maximum step to use to compute HPI coils locations. Default is 1.
    - param_compute_locs_too_close: How to handle HPI positions too close to sensors ('raise', 'warning', 'info'). Default is 'raise'.
    - param_compute_locs_adjust_dig: Adjust digitization locations when computing HPI coils locations. Default is False.
    - param_compute_head_pos_dist_limit: Minimum distance (m) to accept for coil position fitting. Default is 0.005.
    - param_compute_head_pos_gof_limit: Minimum goodness of fit to accept for each coil. Default is 0.98.
    - param_compute_head_pos_adjust_dig: Adjust digitization locations when computing head positions. Default is False.

Outputs:
    - out_dir/headshape.pos: Time-varying head positions
    - product.json: Metadata about the head position computation
"""

# Copyright (c) 2026 brainlife.io
#
# Author: Franco Pestilli

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne

# Import shared utilities
from brainlife_utils import (
    load_config,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    require_config_keys,
    read_optional_files,
    define_kwargs
)

# Ensure output directories exist
ensure_output_dirs('out_dir')

# Load configuration
config = load_config()
require_config_keys(config, ['fif'])

# == LOAD DATA ==
data_file = config.pop('fif')
raw = mne.io.read_raw_fif(data_file, allow_maxshield=True)

# Read and save optional files
config = read_optional_files(config, 'out_dir')[0]

# Delete keys values in config.json when this app is executed on Brainlife
kwargs = define_kwargs(config)

# == COMPUTE HEAD POSITIONS ==

# Extract HPI coils amplitudes as a function of time
chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw, t_step_min=kwargs['param_compute_amplitudes_t_step_min'],
                                                   t_window=kwargs['param_compute_amplitudes_t_window'],
                                                   ext_order=kwargs['param_compute_amplitudes_ext_order'],
                                                   tmin=kwargs['param_compute_amplitudes_tmin'],
                                                   tmax=kwargs['param_compute_amplitudes_tmax'])

# Compute time-varying HPI coils locations
chpi_locs = mne.chpi.compute_chpi_locs(raw.info, chpi_amplitudes, t_step_max=kwargs['param_compute_locs_t_step_max'],
                                       too_close=kwargs['param_compute_locs_too_close'], adjust_dig=kwargs['param_compute_locs_adjust_dig'])

# Compute head positions from the coil locations
head_pos_file = mne.chpi.compute_head_pos(raw.info, chpi_locs, dist_limit=kwargs['param_compute_head_pos_dist_limit'],
                                          gof_limit=kwargs['param_compute_head_pos_gof_limit'], adjust_dig=kwargs['param_compute_head_pos_adjust_dig'])

# == SAVE FILE ==
mne.chpi.write_head_pos(os.path.join('out_dir', 'headshape.pos'), head_pos_file)

# == CREATE PRODUCT.JSON ==
product_items = []
add_info_to_product(product_items, 'Head position file was written successfully.', 'success')
create_product_json(product_items)
