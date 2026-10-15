import pandas as pd
import numpy as np


def assign_groups(user_df):
    user_copy = user_df.copy()
    groups = ['control']*(len(user_copy)//2)+['variant']*(len(user_copy)//2)
    np.random.shuffle(groups)
    user_copy['group']=groups
    return user_copy

users = pd.DataFrame({
    'user_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'age': [23, 45, 31, 29, 40, 22, 30, 27],
    'location': ['NY', 'CA', 'TX', 'NY', 'CA', 'TX', 'NY', 'CA']
})

assigned_users = assign_groups(users)
print(assigned_users)
