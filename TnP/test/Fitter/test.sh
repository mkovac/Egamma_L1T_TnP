!#/bin/bash

./fit.exe run/test_EB_low.par
cd results
python plot_EG_example.py
cd ..
display results/plots/turnon_plot2018log.png
