import os

root_dir = os.path.dirname(__file__)
data_dir = os.path.join(root_dir, 'data')
results_dir = os.path.join(root_dir, 'results')

for a in [data_dir, results_dir, ]:
    if not os.path.exists(a):
        os.makedirs(a)

if __name__ == '__main__':
    'OK'
