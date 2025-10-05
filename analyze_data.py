"""
Agentic AI Performance Data Analysis Script
分析智能体AI性能数据集并生成HTML可视化看板

Author: AI Assistant
Date: 2025-10-05
Purpose: 读取Excel数据，执行三项数据分析，生成自包含的HTML看板
"""

# 导入必要的库 / Import necessary libraries
import pandas as pd
import json

# 定义常量 / Define constants
EXCEL_FILE = 'first-80-rows-agentic_ai_performance_dataset_20250622.xlsx'
OUTPUT_HTML = 'data-dashboard.html'
HEADER_ROW = 1  # Excel文件的表头在第1行 / Header is at row 1


def load_data():
    """
    加载Excel数据文件 / Load Excel data file

    Returns:
        pandas.DataFrame: 包含所有数据的DataFrame / DataFrame containing all data

    Note:
        使用header=1是因为Excel文件第0行是标题，第1行才是列名
        Using header=1 because row 0 is the title, row 1 contains column names
    """
    df = pd.read_excel(EXCEL_FILE, header=HEADER_ROW)
    return df


def analyze_agent_type_multimodal(df):
    """
    分析各智能体类型中支持多模态的占比，返回TOP3
    Analyze the proportion of multimodal support by agent type, return TOP3

    Args:
        df (pandas.DataFrame): 数据集 / Dataset

    Returns:
        list: TOP3结果列表，每项包含name, proportion, count, total
              List of TOP3 results, each containing name, proportion, count, total
    """
    # 按agent_type分组 / Group by agent_type
    grouped = df.groupby('agent_type')['multimodal_capability']

    # 计算每个agent_type的总数和支持多模态的数量
    # Calculate total count and multimodal count for each agent_type
    total_counts = grouped.count()
    multimodal_counts = grouped.sum()  # True被当作1，False被当作0 / True counts as 1, False as 0

    # 计算占比 / Calculate proportion
    proportions = (multimodal_counts / total_counts * 100).round(2)

    # 创建结果DataFrame并排序 / Create result DataFrame and sort
    results = pd.DataFrame({
        'name': proportions.index,
        'proportion': proportions.values,
        'count': multimodal_counts.values,
        'total': total_counts.values
    })
    results = results.sort_values('proportion', ascending=False).head(3)

    # 转换为字典列表 / Convert to list of dictionaries
    return results.to_dict('records')


def analyze_model_architecture_multimodal(df):
    """
    分析各大模型架构中支持多模态的占比，返回TOP3
    Analyze the proportion of multimodal support by model architecture, return TOP3

    Args:
        df (pandas.DataFrame): 数据集 / Dataset

    Returns:
        list: TOP3结果列表，每项包含name, proportion, count, total
              List of TOP3 results, each containing name, proportion, count, total
    """
    # 按model_architecture分组 / Group by model_architecture
    grouped = df.groupby('model_architecture')['multimodal_capability']

    # 计算每个model_architecture的总数和支持多模态的数量
    # Calculate total count and multimodal count for each model_architecture
    total_counts = grouped.count()
    multimodal_counts = grouped.sum()  # True被当作1，False被当作0 / True counts as 1, False as 0

    # 计算占比 / Calculate proportion
    proportions = (multimodal_counts / total_counts * 100).round(2)

    # 创建结果DataFrame并排序 / Create result DataFrame and sort
    results = pd.DataFrame({
        'name': proportions.index,
        'proportion': proportions.values,
        'count': multimodal_counts.values,
        'total': total_counts.values
    })
    results = results.sort_values('proportion', ascending=False).head(3)

    # 转换为字典列表 / Convert to list of dictionaries
    return results.to_dict('records')


def analyze_task_category_bias_median(df):
    """
    分析各任务类型的bias_detection_score中位数，返回TOP3
    Analyze the median bias_detection_score by task category, return TOP3

    Args:
        df (pandas.DataFrame): 数据集 / Dataset

    Returns:
        list: TOP3结果列表，每项包含name, median
              List of TOP3 results, each containing name, median
    """
    # 按task_category分组并计算bias_detection_score的中位数
    # Group by task_category and calculate median of bias_detection_score
    medians = df.groupby('task_category')['bias_detection_score'].median()

    # 创建结果DataFrame并排序 / Create result DataFrame and sort
    results = pd.DataFrame({
        'name': medians.index,
        'median': medians.values.round(4)
    })
    results = results.sort_values('median', ascending=False).head(3)

    # 转换为字典列表 / Convert to list of dictionaries
    return results.to_dict('records')


def generate_html(analysis1, analysis2, analysis3, total_rows):
    """
    生成包含所有分析结果和可视化的HTML文件
    Generate HTML file with all analysis results and visualizations

    Args:
        analysis1 (list): 智能体类型多模态占比分析结果 / Agent type multimodal analysis results
        analysis2 (list): 模型架构多模态占比分析结果 / Model architecture multimodal analysis results
        analysis3 (list): 任务类型公正性中位数分析结果 / Task category bias median analysis results
        total_rows (int): 数据集总行数 / Total number of rows in dataset

    Returns:
        str: 完整的HTML内容 / Complete HTML content
    """
    # 读取Chart.js库代码 / Read Chart.js library code
    with open('/tmp/chartjs.min.js', 'r', encoding='utf-8') as f:
        chartjs_code = f.read()

    # 将Python数据转换为JavaScript格式 / Convert Python data to JavaScript format
    data1_js = json.dumps(analysis1, ensure_ascii=False)
    data2_js = json.dumps(analysis2, ensure_ascii=False)
    data3_js = json.dumps(analysis3, ensure_ascii=False)

    # HTML模板 / HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI Performance Dashboard 2025</title>
    <style>
        /* 基础样式 / Base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            line-height: 1.6;
        }}

        /* 容器样式 / Container styles */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }}

        /* 标题样式 / Header styles */
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2em;
        }}

        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        /* 图表容器样式 / Chart container styles */
        .chart-section {{
            margin-bottom: 40px;
            background: #fafbfc;
            padding: 20px;
            border-radius: 8px;
        }}

        .chart-title {{
            color: #34495e;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .chart-container {{
            position: relative;
            height: 300px;
        }}

        /* 信息框样式 / Info box styles */
        .info-box {{
            background: #e8f4f8;
            padding: 15px 20px;
            border-left: 4px solid #3498db;
            margin-top: 30px;
            border-radius: 4px;
        }}

        .info-box p {{
            color: #2c3e50;
            margin: 5px 0;
        }}

        /* 移动端响应式 / Mobile responsive */
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}

            .container {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            .subtitle {{
                font-size: 0.9em;
            }}

            .chart-container {{
                height: 250px;
            }}

            .chart-title {{
                font-size: 1em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Agentic AI Performance Dashboard 2025</h1>
        <p class="subtitle">智能体AI性能数据分析看板</p>

        <div class="info-box">
            <p><strong>数据集总记录数：</strong>{total_rows} 条</p>
            <p><strong>数据来源：</strong>Agentic AI Performance Dataset 2025</p>
        </div>

        <!-- 图表1：智能体类型多模态占比 / Chart 1: Agent Type Multimodal Proportion -->
        <div class="chart-section">
            <h2 class="chart-title">问题1：支持多模态的智能体类型占比 TOP3</h2>
            <div class="chart-container">
                <canvas id="chart1"></canvas>
            </div>
        </div>

        <!-- 图表2：模型架构多模态占比 / Chart 2: Model Architecture Multimodal Proportion -->
        <div class="chart-section">
            <h2 class="chart-title">问题2：支持多模态的大模型架构占比 TOP3</h2>
            <div class="chart-container">
                <canvas id="chart2"></canvas>
            </div>
        </div>

        <!-- 图表3：任务类型公正性中位数 / Chart 3: Task Category Bias Median -->
        <div class="chart-section">
            <h2 class="chart-title">问题3：各任务类型公正性中位数 TOP3</h2>
            <div class="chart-container">
                <canvas id="chart3"></canvas>
            </div>
        </div>
    </div>

    <!-- 嵌入Chart.js库 / Embedded Chart.js Library -->
    <script>
{chartjs_code}
    </script>

    <!-- 数据和图表配置 / Data and Chart Configuration -->
    <script>
        // 数据 / Data
        const data1 = {data1_js};
        const data2 = {data2_js};
        const data3 = {data3_js};

        // 图表1配置：智能体类型多模态占比 / Chart 1 Config: Agent Type Multimodal Proportion
        const chart1Config = {{
            type: 'bar',
            data: {{
                labels: data1.map(item => item.name),
                datasets: [{{
                    label: '多模态支持占比 (%)',
                    data: data1.map(item => item.proportion),
                    backgroundColor: ['#a8dadc', '#457b9d', '#1d3557'],
                    borderWidth: 0,
                    borderRadius: 5
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const item = data1[context.dataIndex];
                                return `占比: ${{item.proportion}}% (${{item.count}}/${{item.total}})`;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: '占比 (%)'
                        }}
                    }}
                }}
            }}
        }};

        // 图表2配置：模型架构多模态占比 / Chart 2 Config: Model Architecture Multimodal Proportion
        const chart2Config = {{
            type: 'bar',
            data: {{
                labels: data2.map(item => item.name),
                datasets: [{{
                    label: '多模态支持占比 (%)',
                    data: data2.map(item => item.proportion),
                    backgroundColor: ['#b8e0d2', '#6a994e', '#386641'],
                    borderWidth: 0,
                    borderRadius: 5
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const item = data2[context.dataIndex];
                                return `占比: ${{item.proportion}}% (${{item.count}}/${{item.total}})`;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: '占比 (%)'
                        }}
                    }}
                }}
            }}
        }};

        // 图表3配置：任务类型公正性中位数 / Chart 3 Config: Task Category Bias Median
        const chart3Config = {{
            type: 'bar',
            data: {{
                labels: data3.map(item => item.name),
                datasets: [{{
                    label: 'Bias Detection中位数',
                    data: data3.map(item => item.median),
                    backgroundColor: ['#ffd6a5', '#fdac7a', '#f08080'],
                    borderWidth: 0,
                    borderRadius: 5
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const item = data3[context.dataIndex];
                                return `中位数: ${{item.median.toFixed(4)}}`;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        max: 1.0,
                        title: {{
                            display: true,
                            text: 'Bias Detection Score (中位数)'
                        }}
                    }}
                }}
            }}
        }};

        // 渲染图表 / Render charts
        window.addEventListener('DOMContentLoaded', function() {{
            new Chart(document.getElementById('chart1'), chart1Config);
            new Chart(document.getElementById('chart2'), chart2Config);
            new Chart(document.getElementById('chart3'), chart3Config);
        }});
    </script>
</body>
</html>'''

    return html_content


# 主程序执行块 / Main execution block
if __name__ == '__main__':
    # 步骤1：加载数据 / Step 1: Load data
    print("正在加载数据... / Loading data...")
    df = load_data()
    total_rows = len(df)
    print(f"数据加载成功！共 {total_rows} 条记录 / Data loaded successfully! Total {total_rows} records")

    # 步骤2：执行分析1 - 智能体类型多模态占比 / Step 2: Execute analysis 1 - Agent type multimodal proportion
    print("\n正在分析问题1：智能体类型多模态占比... / Analyzing question 1: Agent type multimodal proportion...")
    result1 = analyze_agent_type_multimodal(df)
    print("TOP3 结果 / TOP3 results:")
    for i, item in enumerate(result1, 1):
        print(f"  {i}. {item['name']}: {item['proportion']}% ({item['count']}/{item['total']})")

    # 步骤3：执行分析2 - 模型架构多模态占比 / Step 3: Execute analysis 2 - Model architecture multimodal proportion
    print("\n正在分析问题2：模型架构多模态占比... / Analyzing question 2: Model architecture multimodal proportion...")
    result2 = analyze_model_architecture_multimodal(df)
    print("TOP3 结果 / TOP3 results:")
    for i, item in enumerate(result2, 1):
        print(f"  {i}. {item['name']}: {item['proportion']}% ({item['count']}/{item['total']})")

    # 步骤4：执行分析3 - 任务类型公正性中位数 / Step 4: Execute analysis 3 - Task category bias median
    print("\n正在分析问题3：任务类型公正性中位数... / Analyzing question 3: Task category bias median...")
    result3 = analyze_task_category_bias_median(df)
    print("TOP3 结果 / TOP3 results:")
    for i, item in enumerate(result3, 1):
        print(f"  {i}. {item['name']}: {item['median']:.4f}")

    # 步骤5：生成HTML看板 / Step 5: Generate HTML dashboard
    print("\n正在生成HTML看板... / Generating HTML dashboard...")
    html_content = generate_html(result1, result2, result3, total_rows)

    # 步骤6：写入文件 / Step 6: Write to file
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n✅ 成功！HTML看板已生成: {OUTPUT_HTML}")
    print(f"✅ Success! HTML dashboard generated: {OUTPUT_HTML}")
    print(f"\n📊 请在浏览器中打开 {OUTPUT_HTML} 查看可视化结果")
    print(f"📊 Please open {OUTPUT_HTML} in a browser to view the visualizations")
