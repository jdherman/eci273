def setup(plt):
  import seaborn as sns
  from IPython.display import set_matplotlib_formats
  set_matplotlib_formats
  set_matplotlib_formats('svg')
  sns.set_style('whitegrid')
  plt.rcParams['figure.figsize'] = (5, 3)
  plt.rcParams['font.size'] = 11
  plt.rcParams['font.family'] = 'OfficinaSanITCBoo'
  plt.rcParams['axes.labelsize'] = 1.1*plt.rcParams['font.size']
  plt.rcParams['axes.titlesize'] = 1.1*plt.rcParams['font.size']
  plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
  plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
  plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']

def plot_format(plt, xgrid=False, title='Title'):
  plt.title(title, family='OfficinaSanITCMedium', loc='left')
  plt.tight_layout()
  plt.gca().xaxis.grid(xgrid)