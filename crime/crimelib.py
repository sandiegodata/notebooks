#
# Build a function for creating Rhythm Map plots, with common options
#
from math import ceil

def plot_rhythm(df, legends = None, communities = None, incident_type=None, title=None, filename=None,
                axes_fields=['year','week'], ncols  = 2, scale = 1.0, height=2.5):
    
    import numpy as np
    import matplotlib.pyplot as plt

    if not legends:
        legends = sorted([ l for l in df.legend.unique() if l.strip() and l not in ('-', 'ARSON','HOMICIDE') ])

    if not communities:
        communities = [None]

    
    nonnull_l_len = max(len([l for l in legends if l is not None]), 1)
    nonnull_c_len = max(len([ c for c in communities if c is not None]), 1)
   
    c = nonnull_l_len * nonnull_c_len

    nrows = ceil(float(c)/ncols)

    cmap = plt.get_cmap('YlOrRd', 500)

    fig, axes = plt.subplots(nrows=int(nrows), ncols=int(ncols), figsize=(10,10), 
                             squeeze=True, sharex=False, sharey=False)

    try:
        len(axes)
        axes = axes.ravel() # Convert 2D array to 1D
    except TypeError :
        axes = [axes] # subplot returns scalar in c=1 case. 

    
    fig.set_size_inches(12.0*scale,nrows*height*scale)
    
    plt.tight_layout(h_pad=2)
    fig.subplots_adjust(top=0.90)
    i = 0
    
    for community in communities:
        for legend in legends:

            sub = df
            gtitles = []
            
            if legend:
                sub = sub[sub.legend == legend]
                
                gtitles.append(legend.title())

            if community:
                sub = sub[sub.community == community]
                gtitles.append(community)
                
            if incident_type:
                # The type field used to be for CITATIONS, ARREST, etc, but
                # seems to be gone in this version of the dataset. 
                sub = sub[sub.type == incident_type]
               

            
            axes[i].set_title(' / '.join(gtitles))

            if len(sub) < 40:
                i += 1
                continue

            heatg = sub.groupby(axes_fields)
           
            hgcounts = heatg.count()['id'].unstack(axes_fields[0]).fillna(0)

            # Converting to an array puts it into a for that
            # matplotlib expects. This probably only works b/c the
            # hours and days of week are 1-based indexes. 
            axes[i].pcolormesh(np.array(hgcounts.T),cmap=cmap)
            
            i += 1
            
        
    if title:
        fig.suptitle(title, fontsize=18, fontweight='bold')
        
    if filename:
        fig.savefig(filename)
        
