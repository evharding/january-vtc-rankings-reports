import seaborn as sns
import matplotlib.pyplot as plt

def scatter_age_dist(working_set):
  ax = sns.scatterplot(x='Age', y='Distance', hue='Sex', data=working_set)
  for _, row in working_set.iterrows():
    ax.text(row['Age'] + 0.3, row['Distance'] + 0.3 , row['Name'], fontsize=6 )
  return ax

def everyone_plot(nbcers):
  # Summary scatterplot of everyone vs Charlie. Labels make it a little messy
  plt.figure(figsize=(20, 20))
  working_set = nbcers
  ax = sns.scatterplot(x='Age', y='Distance', hue='Sex', data=working_set)
  row = working_set.iloc[0]
  ax.text(row['Age'] + 0.3, row['Distance']+ 0.3, row['Name'])
  ax.set_title('Look How Far Ahead Charlie Is')
  plt.savefig('everyone.png')

def make_scatter(working_set, title, filename):
  plt.figure(figsize=(20, 20))
  ax2 = scatter_age_dist(working_set)
  ax2.set_title(title)
  plt.savefig(filename)