import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

def simulate_ab_test_data(size_control, size_variant, conv_rate_control, conv_rate_variant, seed=None):
    if seed is not None:
        np.random.seed(seed)
        group = np.array(['control']*size_control+['variant']*size_variant)
        conversion = np.concatenate([
            np.random.binomial(n=1, size=size_control, p=conv_rate_control),
            np.random.binomial(n=1, size=size_variant, p=conv_rate_variant)
        ])
    
    data = pd.DataFrame({'group': group, 'conversion': conversion})
    return data

def analyze_ab_test(data):
    group_control = data[data['group'] == 'control']
    group_variant = data[data['group'] == 'variant']
    conv_rate_control = np.mean(group_control['conversion'])
    conv_rate_variant = np.mean(group_variant['conversion'])
    diff = conv_rate_variant - conv_rate_control
    #Обчислення стандартної помилки для кожної групи
    se_control = np.sqrt(conv_rate_control*(1-conv_rate_control)/len(group_control))
    se_variant = np.sqrt(conv_rate_variant*(1-conv_rate_variant)/len(group_variant))
    SE_diff = se_control + se_variant
    #Для 95%-го довірчого інтервалу використовується z-показник, що дорівнює приблизно 1,96
    z_score = stats.norm.ppf(0.975)
    #Обчислення довірчих інтервалів
    ci_low = diff - z_score * SE_diff
    ci_high = diff + z_score * SE_diff
    t_stat, p_value = stats.ttest_ind(group_control['conversion'], group_variant['conversion'])
    
    
    result = {
        'conv_rate_control': conv_rate_control,
        'conv_rate_variant': conv_rate_variant,
        'difference': diff,
        'z_score': z_score,
        'p_value': p_value,
        'ci_low': ci_low,
        'ci_high': ci_high
    }
    return result

def plot_ab_results(data):
    group_data = data.groupby('group')['conversion'].mean().reset_index()
    plt.figure(figsize=(10, 8))
    plt.bar(group_data['group'], group_data['conversion'], color=['skyblue', 'yellow'])
    plt.title('Коефіцієнт конверсії')
    plt.yticks([0.05, 0.1, 0.15, 0.2, 0.25])
    plt.show()

# Simulate data
data = simulate_ab_test_data(
    size_control=1000,
    size_variant=1000,
    conv_rate_control=0.12,
    conv_rate_variant=0.15,
    seed=42
)

result = analyze_ab_test(data)
print(result)
# Plot results
plot_ab_results(data)

# Interpretation and Reporting
interpretation = (
    f"Control group conversion rate: {result['conv_rate_control']:.3f}\n"
    f"Variant group conversion rate: {result['conv_rate_variant']:.3f}\n"
    f"Difference: {result['difference']:.3f}\n"
    f"95% Confidence Interval: [{result['ci_low']:.3f}, {result['ci_high']:.3f}]\n"
    f"p-value: {result['p_value']:.4f}\n"
)
print(interpretation)
if result['p_value'] < 0.05:
    conclusion = "The result is statistically significant. The variant outperforms the control."
else:
    conclusion = "The result is not statistically significant. There is no evidence the variant outperforms the control."
print(conclusion)
