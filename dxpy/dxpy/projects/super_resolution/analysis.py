COLUMNS = ['IDX', 'TYPE', 'NB_DOWN', 'RMSE', 'PSNR', 'SSIM']

def analysis_one_image(label, target, name):    
    from dxpy.tensor.metrics import psnr, rmse, ssim
    image_type = name[:-2]
    nb_down = int(name[-2:-1])
    return (image_type, nb_down, rmse(label, target), psnr(label, target), ssim(label, target))

def analysis_result(filename, output):
    import pandas as pd
    from tqdm import tqdm
    import numpy as np
    results = np.load(filename)
    nb_images = results['phantom'].shape[0]
    anas = []
    for idx in tqdm(range(nb_images)):
        for k in results.keys():
            if k == 'phantom':
                continue
            anas.append([idx] + list(analysis_one_image(results['phantom'][idx, ...], results[k][idx, ...], name=k)))
    df = pd.DataFrame(data=anas, columns=COLUMNS)
    df.to_csv(output)