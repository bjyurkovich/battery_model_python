# Battery Model

This repo contains a battery model of a 15Ah LG Chem Automotive Li-Ion (LMO) battery cell.  The model is based on the model derivation from (this work)[http://rave.ohiolink.edu/etdc/view?acc_num=osu1281632214].

The model parameters were identified using a subspace technique found (here)[https://www.researchgate.net/publication/251589129_Linear_parameter_varying_battery_model_identification_using_subspace_methods].  The parameters are simplified in the base model, but can be extended to include, as the paramters can be found in `/data/battery_mappings.mat` which are dependent on current direction and SOC.

## Running the Model
To begin, start your virtual environment:

```bash
virtualenv venv
source venv/bin/activate 
pip install -r requirements.txt
```
> If you don't have `virtualenv`, you may need to `pip install virtualenv`.

Then just run the model:

```bash
python battery_model.py
```

The output is saved in `data/output.mat` and can be imported into MATLAB for plotting and viewing.