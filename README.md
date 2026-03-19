# app-head-pos

Repository of a Brainlife App that computes time varying head positions from `raw.info` provided in the `raw.fif` when the cHPI were recorded 
([see the mne tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/plot_59_head_positions.html#sphx-glr-auto-tutorials-preprocessing-plot-59-head-positions-py)). 

# app-head-pos documentation

1) Compute the cHPI
3) Input file are:
    * a MEG file in `.fif` format containing cHPI information,
    * an optional fine calibration file in `.dat`,
    * an optional crosstalk compensation file in `.fif`,
    * an optional head position file in `.pos`,
    * an optional destination file in `.fif`,
    * an optional events file in `.tsv`,
    * an optional channels file in `.tsv`.
4) Input parameters are:
    * `param_compute_amplitudes_t_step_min`: `float`, minimum time step to use to compute cHPI amplitudes. Default is 0.01.
    * `param_compute_amplitudes_t_window`: `float`, time window to use to estimate the amplitudes. Default is 0.2.
    * `param_compute_amplitudes_ext_order`: `int`, the external order for SSS-like interfence suppression to compute cHPI amplitudes. Default is 1.
    * `param_compute_amplitudes_tmin`: `float`, start time of the raw data to use in seconds to compute cHPI amplitudes. Default is 0.
    * `param_compute_amplitudes_tmax`: `float`, optional, end time of the raw data to use in seconds to compute cHPI amplitudes. Default is `None`.
    * `param_compute_locs_t_step_max`: `float`, maximum step to use to compute HPI coils locations. Default is 1.
    * `param_compute_locs_too_close`: `str`, how to handle HPI positions too close to sensors when computing HPI coils locations. 
Can be 'raise', (default), 'warning', or 'info'.
    * `param_compute_locs_adjust_dig`: `bool`, if True, adjust the digitization locations used for fitting when computing HPI coils locations.
Default is False.
    * `param_compute_head_pos_dist_limit`: `float`, minimum distance (m) to accept for coil position fitting when computing head positions. 
Default is 0.005.
    * `param_compute_head_pos_gof_limit`: `float`, minimum goodness of fit to accept for each coil to compute head positions. Default is 0.98.
    * `param_compute_head_pos_adjust_dig`: `bool`, if True, adjust the digitization locations used for fitting when computing head positions. Default is False.
4) Ouput file is a `.pos` file containing the head positions, which can be read by 
   [`mne.chpi.read_head_pos`](https://mne.tools/stable/generated/mne.chpi.read_head_pos.html?highlight=mne%20chpi%20read_head_pos#mne.chpi.read_head_pos) and will be used in Maxwell Filtering (see the corresponding BL App).

### Authors
- [Aurore Bussalb](aurore.bussalb@icm-institute.org)

### Contributors
- [Aurore Bussalb](aurore.bussalb@icm-institute.org)
- [Maximilien Chaumon](maximilien.chaumon@icm-institute.org)

### Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your code and publications. Copy and past the following lines into your repository when using this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations
1. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [https://doi.org/10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Running the App 

### On Brainlife.io

This App is still private on Brainlife.

### Running Locally (on your machine)

1. git clone this repo
2. Inside the cloned directory, create `config.json` with the same keys as in `config.json.example` but with paths to your input 
   files and values of the input parameters.

```json
{
  "fif": "rest1-raw.fif"
}
```

3. Launch the App by executing `main`

```bash
./main
```

## Output

The output file is `.pos` file.

## Citation

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
