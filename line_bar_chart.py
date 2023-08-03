#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import sys

def read_csv_data(filename):
    df = pd.read_csv(filename, parse_dates=True, dayfirst=True)
    return df

def format_date(x, pos):
    years = x // 365
    months = (x % 365) // 30
    days = (x % 365) % 30
    return f"{int(years)}y {int(months)}m {int(days)}d"

def calculate_date_difference(df, x_col, y_cols):
    df_copy = df.copy()
    for y_col in y_cols:
        # 将日期列转换为日期类型
        df_copy[x_col] = pd.to_datetime(df_copy[x_col])
        df_copy[y_col] = pd.to_datetime(df_copy[y_col])
        df_copy[y_col] = (df_copy[x_col] - df_copy[y_col]).dt.days
    return df_copy

def plot_bar_chart(df, x_col, y_cols):
    plt.figure(figsize=(10, 6))

    for col in y_cols:
        plt.plot(df[x_col], df[col], marker='o', linestyle='-', linewidth=2, label=f'{col} Line')

    plt.xlabel(x_col)
    plt.ylabel('waited days')
    plt.title('Difference between Columns')
    plt.legend()
    plt.xticks(rotation=45)

    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_date))  # 设置y轴标签显示日期格式

    # 调整y轴刻度间隔
    plt.yticks(plt.yticks()[0][::2])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供要读取的csv文件名作为脚本参数。")
        sys.exit(1)

    input_filename = sys.argv[1]
    data = read_csv_data(input_filename)

    print("读取的数据列：")
    for idx, col in enumerate(data.columns):
        print(f"{idx + 1}. {col}")

    x_col_idx = input(f"请选择作为x轴的列(默认第1列: {data.columns[0]}): ")
    if x_col_idx == "":
        x_col_idx = 1
    else:
        x_col_idx = int(x_col_idx)

    x_col = data.columns[x_col_idx - 1]

    y_cols_input = input(f"需要对哪几列进行绘图(默认为:2,3 ({data.columns[1]},{data.columns[2]})): ")
    if y_cols_input == "":
        y_cols_input = "2,3"

    y_cols_idx = [int(idx) for idx in y_cols_input.split(",") if idx.strip() != ""]
    y_cols = [data.columns[idx - 1] for idx in y_cols_idx]
    print (f"选择的x轴列为: {x_col}")
    print (f"选择的列为: {y_cols}")

    data = calculate_date_difference(data, x_col, y_cols)
    plot_bar_chart(data, x_col, y_cols)

