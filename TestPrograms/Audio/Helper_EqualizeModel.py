import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.signal import butter, windows, kaiserord, lfilter, firwin, freqz, firwin2, convolve

def equalizeModell(model_is,
                    model_should,
                    nr_of_tabs,
                    spacing="lin",
                    start_frq=200,
                    stop_frq=20000):
        if spacing=="log":
            taps_pos = np.geomspace(start_frq, stop_frq, num=nr_of_tabs)
        elif spacing=="lin":
            taps_pos = np.linspace(start_frq, stop_frq, nr_of_tabs)
        else:
            raise Exception(f"Spacing has to be 'log' or 'lin' and not {spacing}")
            
        func_model_is = interp1d(model_is[:,0],model_is[:,1])
        
        if model_should == "equal":
            func_model_should = interp1d([start_frq,stop_frq],[1,1])
        elif model_should == "1/w":
            func_model_should = interp1d(taps_pos, start_frq/taps_pos)
        elif model_should == "1/w^2":
            func_model_should = interp1d(taps_pos, start_frq**2/taps_pos**2)
        else:
            raise Exception(f"model_should has to be 'equal','1/w' or '1/w^2' and not {model_should}")
            
        taps_pos_between = np.convolve(taps_pos,[0.5,0.5],"valid")
        val_is = func_model_is(taps_pos_between)
        val_should = func_model_should(taps_pos_between) 
        gain = val_should/val_is
        gain_norm = gain / max(gain)
        
        gain_dict = {(taps_pos[i], taps_pos[i+1]): {"band_gain": g
                                                    , "f_type":("kaiser",5)} for i,g in enumerate(gain_norm)}
        fig, ax = plt.subplots()
        ax.plot(model_is[:,0],model_is[:,1])
        ax.vlines(taps_pos,0,1,colors="red",linestyles="dashed")
        
        fig, ax = plt.subplots()
        ax.plot(taps_pos, func_model_should(taps_pos)) 
        
        return gain_dict

frq = np.linspace(200,20000)
model_transducer = np.column_stack((frq.T,200**(2/3)/(frq.T)**(2/3)))
fit_to_type = "1/w^2"
bin_nr = 20
spacing="lin"
gain_dict = equalizeModell(model_transducer,
                            fit_to_type,
                            bin_nr,
                            spacing)
with open(f"Model_2/3_{fit_to_type}_{bin_nr}_{spacing}","w") as f:
    f.writelines(gain_dict)
