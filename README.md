# Compute Head Positions from cHPI

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.499-blue.svg)](https://doi.org/10.25663/brainlife.app.499)

## Description

This app computes time-varying head positions from continuous head-position indicator (cHPI)
signals recorded on an Elekta/MEGIN/Neuromag (or compatible) MEG system
([see the MNE tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/plot_59_head_positions.html)).
It extracts the cHPI coil amplitudes over time with
[`mne.chpi.compute_chpi_amplitudes`](https://mne.tools/stable/generated/mne.chpi.compute_chpi_amplitudes.html),
derives the time-varying coil locations with
[`mne.chpi.compute_chpi_locs`](https://mne.tools/stable/generated/mne.chpi.compute_chpi_locs.html),
and fits the head position over time with
[`mne.chpi.compute_head_pos`](https://mne.tools/stable/generated/mne.chpi.compute_head_pos.html).

The app generates:
- a `.pos` file with the time-varying head positions,
- pass-through copies of the optional calibration, cross-talk, channels, events and destination
  files, when supplied, for use by downstream apps.

## Inputs

- **`fif`** (`neuro/meg/fif`): continuous MEG recording containing cHPI information (required).
- **`calibration`** (`neuro/meg/fif`): optional fine-calibration file bundled with the MEG
  recording; not used by this app's computation, copied through to the output directory for
  downstream apps (e.g. app-maxwell-filter).
- **`crosstalk`** (`neuro/meg/fif`): optional cross-talk compensation file bundled with the MEG
  recording; not used by this app's computation, copied through for downstream apps.
- **`headshape`** (`neuro/meg/fif`): optional head-digitization points bundled with the MEG
  recording; not used to compute the head positions (which are derived from the cHPI coils, not
  from this file), copied through to the output directory and then superseded there by this app's
  computed `.pos` file.
- **`channels`** (`neuro/meg/fif`): optional BIDS `channels.tsv` bundled with the MEG recording;
  not used by this app's computation, copied through for downstream apps.
- **`events`** (`neuro/meg/fif`): optional events file bundled with the MEG recording; read but
  not used by this app, copied through for downstream apps.
- **`destination`** (`neuro/meg/fif`): optional destination transformation `.fif` file bundled
  with the MEG recording; not used by this app's computation, copied through for downstream apps
  (e.g. app-maxwell-filter).
- **`destination_override`** (`neuro/meg/fif-override`): optional destination transformation
  `.fif` file (e.g. computed by app-mean-transformation-matrix) that overrides `destination`
  above; also only passed through, not used by this app.
- **`headshape_override`** (`neuro/meg/fif-override`): optional `.pos`/digitization file that
  overrides `headshape` above; also only passed through.
- **`channels_override`** (`neuro/meg/fif-override`): optional BIDS `channels.tsv` (e.g. computed
  by app-bad-channels) that overrides `channels` above; also only passed through.
- **`events_override`** (`neuro/meg/fif-override`): optional events file that overrides `events`
  above; also only passed through.

## Outputs

- `out_dir/headshape.pos` (`neuro/meg/fif-override`): time-varying head positions, readable with
  [`mne.chpi.read_head_pos`](https://mne.tools/stable/generated/mne.chpi.read_head_pos.html); used
  during bad-channel detection (app-bad-channels) and Maxwell filtering (app-maxwell-filter).
- `out_dir/{calibration_meg.dat, crosstalk_meg.fif, channels.tsv, events.tsv, destination.fif}`:
  pass-through copies of the corresponding optional inputs above, when supplied.
- `product.json`: processing status and metadata for the Brainlife.io interface.

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `param_compute_amplitudes_t_step_min` | `float` | `0.01` | Minimum time step to use to compute cHPI amplitudes. |
| `param_compute_amplitudes_t_window` | `float` | `0.2` | Time window to use to estimate the cHPI amplitudes. |
| `param_compute_amplitudes_ext_order` | `int` | `1` | External order for SSS-like interference suppression used to compute cHPI amplitudes. |
| `param_compute_amplitudes_tmin` | `float` | `0` | Start time of the raw data, in seconds, to use to compute cHPI amplitudes. |
| `param_compute_amplitudes_tmax` | `float` or `null` | `null` | End time of the raw data, in seconds, to use to compute cHPI amplitudes; `null` uses the end of the data. |
| `param_compute_locs_t_step_max` | `float` | `1` | Maximum time step to use to compute HPI coil locations. |
| `param_compute_locs_too_close` | `string` | `"raise"` | How to handle HPI positions too close to sensors when computing HPI coil locations: `"raise"`, `"warning"`, or `"info"`. |
| `param_compute_locs_adjust_dig` | `bool` | `false` | If `true`, adjust the digitization locations used for fitting when computing HPI coil locations. |
| `param_compute_head_pos_dist_limit` | `float` | `0.005` | Minimum distance (m) to accept for coil position fitting when computing head positions. |
| `param_compute_head_pos_gof_limit` | `float` | `0.98` | Minimum goodness of fit to accept for each coil when computing head positions. |
| `param_compute_head_pos_adjust_dig` | `bool` | `false` | If `true`, adjust the digitization locations used for fitting when computing head positions. |

## Usage

### Running on Brainlife.io

1. Register on [brainlife.io](https://brainlife.io).
2. Go to the "Apps" tab, search for "Compute Head Positions from cHPI", and add it to a process in
   a project containing a `neuro/meg/fif` MEG recording with cHPI information (optionally with a
   `neuro/meg/fif-override` bundle for overrides).
3. Set the configuration parameters, or leave the defaults, and submit the process.
4. Download the `.pos` head-position file from the process outputs; use it in app-maxwell-filter
   for head-movement compensation or in app-bad-channels for bad-channel detection.

### Local Testing

```bash
git clone <this-repo-url>
cd head-pos
# create config.json with the same keys as config.json.example, with paths to your input files
# and the parameter values you want
./main
```

## Technical Details

- The Docker image used by `main` is `brainlifemeeg/mne:1.12.1`.

## Authors
- Aurore Bussalb (https://github.com/AuroreBussalb)
- Maximilien Chaumon (https://github.com/dnacombo)

## Citations
1. Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
2. Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project it is helpful to
acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your
code and publications.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
